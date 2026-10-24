# -*- coding: utf-8 -*-
"""Coleta automática de séries públicas para os parâmetros económicos e de qualidade da edição IBE (Portugal e Espanha).

Cada série fica em dados_automaticos/<id>.json com os dados reduzidos, o endereço, a data de acesso e o SHA-256 da(s) resposta(s) original(is);
o resumo legível vai para dados_automaticos/RESUMO.md. Nada é inventado: se uma fonte falha ou muda de formato, a falha é registada e a série fica «pendente».
Cada série tem um teste interno (função `testar_*`): se o teste falhar, a série é marcada «pendente (teste falhou)» e não é gravada como válida.

Séries (ver FONTES_VERIFICADAS_IBE.md para licença, periodicidade e condições de cada uma):
  Eurostat  nrg_pc_204 (preço da eletricidade doméstica, com e sem impostos), prc_hicp_aind (inflação), sts_copi_q (custo de construção de habitação nova)
  BCE       taxa de refinanciamento
  INE PT    ICCHN base 2021 (total, materiais, mão-de-obra), IPC mensal, IPC anual (água, esgotos, resíduos, eletricidade)
  INE ES    custo unitário do suministro e do saneamento (nacional e por comunidade autónoma), derivado das tabelas 53448 e 53450
  REE       fator de emissão da geração elétrica do sistema peninsular (apidatos.ree.es)
  APA       fator de emissão da eletricidade de Portugal (PDF oficial, lido do endereço publicado na página da APA)
  MITECO    fator de mix elétrico «sin GdO» (Registro de huella de carbono, XLSX)
  ERSE      tarifa transitória BTN ≤ 20,7 kVA (XLSX de «Tarifas e preços»)
  ERSAR     entidade gestora de cada concelho (água, saneamento, resíduos; IQS) e lista de entidades gestoras
  Verificações de texto legal: IVA PT (Lista I), IVA ES (art. 90 e 91 da Ley 37/1992), Regulamento Tarifário dos Serviços de Águas (ERSAR),
  ANQIP ETA 0701, estado da EN 16941-1 (BSI)

Uso:
  python coletar_series_publicas.py                   # tudo, menos o IQS completo da ERSAR (usa a cache se tiver menos de 30 dias)
  python coletar_series_publicas.py --iqs             # força nova recolha do IQS da ERSAR (834 pedidos, com pausa de 0,3 s)
  python coletar_series_publicas.py --so eurostat_inflacao_anual ine_icchn   # só algumas séries (por prefixo de id)
Dependências: Python 3.9+, openpyxl; pdftotext (poppler) ou pypdf para o PDF da APA.
Para acrescentar uma série: criar uma entrada em SERIES e (se a fonte for nova) uma função `ler_*` e um `testar_*`.
"""
import datetime as dt
import hashlib
import io
import itertools
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.request

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import _caminhos as C  # noqa: E402

DEST = C.AUTOMATICOS
UA = "Triton-IBE-coleta/0.2 (pesquisa academica; sem fins comerciais)"
EUROSTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
INE_PT = "https://www.ine.pt/ine/json_indicador/pindica.jsp?op=2&lang=PT&varcd="
INE_ES = "https://servicios.ine.es/wstempus/js/ES/"
AGORA = dt.datetime.now(dt.timezone.utc)
AGORA_S = AGORA.isoformat(timespec="seconds")

MESES = {"janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
         "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12}


# --------------------------------------------------------------------------------------------- utilitários
def sem_acentos(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def baixar(url, aceita="application/json", timeout=90, tentativas=2):
    ultimo = None
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"Accept": aceita, "User-Agent": UA})
            return urllib.request.urlopen(req, timeout=timeout).read()
        except Exception as e:  # noqa
            ultimo = e
            time.sleep(1.5)
    raise ultimo


def texto(b):
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return b.decode("latin-1")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def sha_lista(lista):
    return sha("".join(sorted(lista)).encode("ascii"))


def ultimos(d, n=3):
    return list(d.items())[-n:]


class Pendente(Exception):
    pass


# --------------------------------------------------------------------------------------------- Eurostat
def resumo_eurostat(j):
    ids, tam = j["id"], j["size"]
    cat = {d: j["dimension"][d]["category"] for d in ids}
    indices = {d: {i: k for k, i in cat[d]["index"].items()} for d in ids}
    out = {}
    for n, p in enumerate(itertools.product(*[range(s) for s in tam])):
        v = j["value"].get(str(n)) if isinstance(j["value"], dict) else j["value"][n]
        if v is None:
            continue
        geo = indices["geo"][p[ids.index("geo")]]
        tempo = indices["time"][p[ids.index("time")]]
        out.setdefault(geo, {})[tempo] = v
    return {g: dict(sorted(v.items())) for g, v in out.items()}


def ler_eurostat(s):
    bruto = baixar(s["url"])
    j = json.loads(bruto)
    res = resumo_eurostat(j)
    if set(res) != {"PT", "ES"} or any(len(v) < 4 for v in res.values()):
        raise Pendente("Eurostat não devolveu PT e ES com pelo menos 4 períodos")
    return dict(res=res, shas=[sha(bruto)], atualizado=j.get("updated"), extra={})


# --------------------------------------------------------------------------------------------- BCE
def ler_bce(s):
    bruto = baixar(s["url"])
    j = json.loads(bruto)
    ser = j["dataSets"][0]["series"]
    obs = ser[next(iter(ser))]["observations"]
    tempos = [t["id"] for t in j["structure"]["dimensions"]["observation"][0]["values"]]
    res = {"U2": {tempos[int(k)]: v[0] for k, v in obs.items()}}
    if len(res["U2"]) < 3:
        raise Pendente("BCE devolveu menos de 3 observações")
    return dict(res=res, shas=[sha(bruto)], atualizado=None, extra={})


# --------------------------------------------------------------------------------------------- INE Portugal
def periodo_iso(nome):
    """'Agosto de 2026' -> '2026-08'; '2025' -> '2025'."""
    nome = sem_acentos(nome).strip()
    m = re.match(r"([a-z]+) de (\d{4})$", nome)
    if m and m.group(1) in MESES:
        return f"{m.group(2)}-{MESES[m.group(1)]:02d}"
    return nome


def ler_ine_pt(s):
    bruto = baixar(s["url"])
    j = json.loads(texto(bruto))[0]
    if not j.get("Sucesso", {}) and "Dados" not in j:
        raise Pendente("INE devolveu resposta sem dados")
    res = {}
    for per, linhas in j["Dados"].items():
        for x in linhas:
            rotulo = s["rotulos"].get(x["dim_3"], x["dim_3"])
            if x.get("valor") in (None, ""):  # «sinal_conv» = dado nulo ou não aplicável
                continue
            res.setdefault(rotulo, {})[periodo_iso(per)] = float(x["valor"])
    res = {k: dict(sorted(v.items())) for k, v in res.items()}
    return dict(res=res, shas=[sha(bruto)], atualizado=j.get("DataUltimoAtualizacao"), extra={"indicador": j.get("IndicadorCod"), "descricao": j.get("IndicadorDsg")})


def testar_icchn(r):
    t = r["res"]["Total"]
    ultimo = list(t)[-1]
    assert ultimo >= f"{AGORA.year - 1}-01", "ICCHN sem dados dos últimos 12-24 meses"
    assert 50 < t[ultimo] < 400, "valor do ICCHN fora do intervalo plausível"
    assert t["2021-01"] and abs(sum(v for k, v in t.items() if k.startswith("2021")) / 12 - 100) < 1.0, "a média de 2021 deveria ser ≈ 100 (base 2021)"


def testar_ipc_mensal(r):
    t = r["res"]["Total"]
    assert abs(sum(v for k, v in t.items() if k.startswith("2025")) / 12 - 100) < 1.0, "a média de 2025 deveria ser ≈ 100 (base 2025)"


def testar_ipc_anual(r):
    assert r["res"]["Abastecimento de água (rede)"]["2025"] == 100.0, "base 2025 = 100"


# --------------------------------------------------------------------------------------------- INE Espanha
def ler_ine_es_agua(s):
    """Custo unitário nacional (séries DCEF5, DCEF6) e por comunidade (tabelas 53448 e 53450, derivado)."""
    shas, res = [], {}
    for cod, rot in (("DCEF5", "suministro_nacional_eur_m3"), ("DCEF6", "saneamiento_nacional_eur_m3"), ("DCEF4", "consumo_medio_hogares_l_hab_dia")):
        b = baixar(INE_ES + f"DATOS_SERIE/{cod}?nult=20")
        shas.append(sha(b))
        j = json.loads(b)
        res[rot] = {str(d["Anyo"]): d["Valor"] for d in j["Data"] if d.get("Valor") is not None}
    b48 = baixar(INE_ES + "DATOS_TABLA/53448?nult=1")
    b50 = baixar(INE_ES + "DATOS_TABLA/53450?nult=1")
    shas += [sha(b48), sha(b50)]
    vol, imp_sum, imp_san, ano = {}, {}, {}, None
    for it in json.loads(b48):
        reg, _, rot = it["Nombre"].rpartition(", ")
        v = it["Data"][0]
        ano = v["NombrePeriodo"]
        if rot.startswith("Volumen total de agua registrada"):
            vol[reg] = v["Valor"]
        elif rot.startswith("Importe facturado por el agua suministrada"):
            imp_sum[reg] = v["Valor"]
    for it in json.loads(b50):
        reg, _, rot = it["Nombre"].rpartition(", ")
        if rot.startswith("Importe facturado por alcantarillado"):
            imp_san[reg] = it["Data"][0]["Valor"]
    ccaa = {}
    for reg in vol:
        if reg in imp_sum and reg in imp_san and vol[reg]:
            ccaa[reg] = dict(suministro_eur_m3=round(imp_sum[reg] / vol[reg], 3), saneamiento_eur_m3=round(imp_san[reg] / vol[reg], 3),
                             importe_suministro_miles_eur=imp_sum[reg], importe_saneamiento_miles_eur=imp_san[reg], volumen_miles_m3=vol[reg])
    res["ccaa_derivado"] = {ano: ccaa}
    return dict(res=res, shas=shas, atualizado=None,
                extra={"nota": "Por comunidade: importe facturado ÷ volumen total de agua registrada y distribuida (cálculo nosso, conferido com DCEF5/DCEF6 nacionais)."})


def testar_ine_es_agua(r):
    ano = list(r["res"]["ccaa_derivado"])[0]
    n = r["res"]["ccaa_derivado"][ano]["España"]
    assert abs(n["suministro_eur_m3"] - r["res"]["suministro_nacional_eur_m3"][ano]) < 0.01, "derivado ≠ DCEF5 nacional"
    assert abs(n["saneamiento_eur_m3"] - r["res"]["saneamiento_nacional_eur_m3"][ano]) < 0.01, "derivado ≠ DCEF6 nacional"
    assert len(r["res"]["ccaa_derivado"][ano]) >= 18, "faltam comunidades"



def ler_ine_es_codigos(s):
    import openpyxl
    pagina = texto(baixar(s["url"], aceita="text/html"))
    m = re.search(r'href="(/daco/daco42/codmun/\d{2}codmun\.xlsx)"', pagina)
    if not m:
        raise Pendente("a página do INE não tem ligação para o XLSX de códigos de municípios")
    url_x = "https://www.ine.es" + m.group(1)
    bruto = baixar(url_x, aceita="*/*", timeout=120)
    wb = openpyxl.load_workbook(io.BytesIO(bruto), data_only=True)
    res, titulo = {}, None
    for w in wb:
        for r in w.iter_rows(values_only=True):
            if r[0] and str(r[0]).startswith("Relaci"):
                titulo = str(r[0])
            if r[0] and re.fullmatch(r"\d{2}", str(r[0])) and r[1] and re.fullmatch(r"\d{3}", str(r[1])):
                res[str(r[0]) + str(r[1])] = str(r[3])
    return dict(res={"municipios": dict(sorted(res.items()))}, shas=[sha(bruto)], atualizado=None,
                extra={"url_xlsx": url_x, "titulo": titulo, "n": len(res), "nota": "Código INE de 5 dígitos = CPRO (província) + CMUN (município); o dígito de controlo (DC) não entra."})


def testar_ine_es_codigos(r):
    v = r["res"]["municipios"]
    assert 8000 < len(v) < 8300, f"{len(v)} municípios"
    assert v["28079"] == "Madrid" and v["08019"] == "Barcelona" and v["41091"] == "Sevilla", "códigos de controlo (Madrid, Barcelona, Sevilla)"


# --------------------------------------------------------------------------------------------- REE (Espanha)
def ler_ree(s):
    base = "https://apidatos.ree.es/es/datos/generacion/"
    q = "?start_date={a}-01-01T00:00&end_date={a}-12-31T23:59&time_trunc=year&geo_trunc=electric_system&geo_limit=peninsular&geo_ids=8741"
    shas, res, emis, gen, atual = [], {}, {}, {}, None
    for ano in range(AGORA.year - 5, AGORA.year):
        try:
            bg = baixar(base + "estructura-generacion" + q.format(a=ano), timeout=120)
            bc = baixar(base + "no-renovables-detalle-emisiones-CO2" + q.format(a=ano), timeout=120)
        except Exception:
            continue
        shas += [sha(bg), sha(bc)]
        jg, jc = json.loads(bg), json.loads(bc)
        g = next(i for i in jg["included"] if i["attributes"]["title"].startswith("Generación total"))["attributes"]["values"]
        e = next(i for i in jc["included"] if i["attributes"]["title"] == "Total tCO2 eq.")["attributes"]["values"]
        f = next(i for i in jc["included"] if i["attributes"]["title"] == "tCO2 eq./MWh")["attributes"]["values"]
        if not (g and e and f):
            continue
        gen[str(ano)], emis[str(ano)] = g[0]["value"], e[0]["value"]
        res[str(ano)] = f[0]["value"]
        atual = jc["data"]["attributes"].get("last-update")
    if len(res) < 3:
        raise Pendente("REE devolveu menos de 3 anos")
    return dict(res={"peninsular_tCO2_MWh": res}, shas=shas, atualizado=atual,
                extra={"geracao_total_MWh": gen, "emissoes_tCO2eq": emis,
                       "nota": "Fator = emissões diretas da geração ÷ geração total, sistema elétrico peninsular (sem Baleares, Canárias, Ceuta e Melilla; sem ciclo de vida; sem importações)."})


def testar_ree(r):
    for ano, f in r["res"]["peninsular_tCO2_MWh"].items():
        assert 0.03 < f < 0.4, f"fator REE {ano} fora do intervalo plausível"
        e, g = r["extra"]["emissoes_tCO2eq"][ano], r["extra"]["geracao_total_MWh"][ano]
        assert abs(e / g - f) < 1e-6, f"fator REE {ano} ≠ emissões/geração"


# --------------------------------------------------------------------------------------------- PDF (APA)
def pdf_para_texto(caminho):
    if shutil.which("pdftotext"):
        r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", caminho, "-"], capture_output=True)
        if r.returncode == 0 and r.stdout:
            return r.stdout.decode("utf-8", "replace")
    try:
        import pypdf
        return "\n".join(p.extract_text() or "" for p in pypdf.PdfReader(caminho).pages)
    except Exception as e:  # noqa
        raise Pendente(f"sem pdftotext nem pypdf utilizáveis ({e})")


def ler_apa(s):
    pagina = texto(baixar(s["url"], aceita="text/html"))
    links = re.findall(r'href="([^"]*fe_gee_eletricidade[^"]*\.pdf)"', pagina)
    if not links:
        raise Pendente("a página da APA não tem ligação para o PDF do fator de emissão")
    url_pdf = links[0]
    bruto = baixar(url_pdf, aceita="application/pdf", timeout=120)
    with tempfile.TemporaryDirectory() as d:
        c = os.path.join(d, "fe.pdf")
        open(c, "wb").write(bruto)
        t = pdf_para_texto(c)
    tabelas, anos, n = [], None, -1
    for ln in t.splitlines():
        m = re.search(r"Regi.o\s+Unidade\s+((?:\d{4}\s*){5,})", ln)
        if m:
            anos = re.findall(r"\d{4}", m.group(1))
            if anos[0] == "2005":
                n += 1
                tabelas.append({})
            continue
        m = re.match(r"\s*(Continente|R\.A\. Madeira|R\.A\. A.ores|Portugal)\s+tCO2 eq\./MWh\s+((?:\d\.\d+\s*)+)$", ln)
        if m and anos and n >= 0:
            vals = re.findall(r"\d\.\d+", m.group(2))
            if len(vals) == len(anos):
                reg = {"R.A. Açores": "R.A. Açores"}.get(m.group(1), m.group(1))
                if reg.startswith("R.A. A"):
                    reg = "R.A. Açores"
                tabelas[n].setdefault(reg, {}).update({a: float(v) for a, v in zip(anos, vals)})
    if len(tabelas) < 2 or "Portugal" not in tabelas[0]:
        raise Pendente("não consegui ler as tabelas T1/T2 do PDF da APA (formato mudou?)")
    ed = re.search(r"Fator de Emiss.o da Eletricidade\s*[–-]?\s*(\d{4})", t)
    return dict(res={"anual": tabelas[0], "media_movel_5_anos": tabelas[1]}, shas=[sha(bruto)], atualizado=None,
                extra={"url_pdf": url_pdf, "edicao": ed.group(1) if ed else None,
                       "nota": "Só emissões diretas da combustão nas centrais (sem extração, transporte de combustíveis nem ciclo de vida); tCO2 eq./MWh de eletricidade PRODUZIDA em Portugal."})


def testar_apa(r):
    p = r["res"]["anual"]["Portugal"]
    assert "2023" in p and abs(p["2023"] - 0.107) < 0.02 or max(p) > "2023", "Portugal 2023 deveria ser ≈ 0,107 tCO2/MWh na edição 2025"
    for reg, v in r["res"]["anual"].items():
        assert all(0 < x < 1 for x in v.values()), f"valores fora de 0–1 em {reg}"
    assert set(r["res"]["anual"]) == {"Continente", "R.A. Madeira", "R.A. Açores", "Portugal"}


# --------------------------------------------------------------------------------------------- MITECO (XLSX)
def ler_miteco(s):
    import openpyxl
    pagina = texto(baixar(s["url"], aceita="text/html"))
    links = re.findall(r'href="([^"]*factoresemision[^"]*\.xlsx)"', pagina)
    if not links:
        raise Pendente("a página do MITECO não tem ligação para o XLSX de factores de emisión")
    url_x = links[0] if links[0].startswith("http") else "https://www.miteco.gob.es" + links[0]
    bruto = baixar(url_x, aceita="*/*", timeout=120)
    wb = openpyxl.load_workbook(io.BytesIO(bruto), data_only=True)
    w = wb["5. Factores de mix eléctricos"]
    res = {}
    for c in range(1, w.max_column + 1):
        ano = w.cell(3, c).value
        if isinstance(ano, int) and 2000 < ano < 2100:
            rot = str(w.cell(4, c + 2).value).strip()
            val = w.cell(4, c + 3).value
            if rot.startswith("Mix sin GdO") and isinstance(val, (int, float)):
                res[str(ano)] = round(float(val), 4)
    rev = []
    for r in wb["7. Revisiones"].iter_rows(min_row=1, max_row=15, values_only=True):
        v = [c for c in r if c is not None]
        if len(v) >= 2 and re.match(r"V\d", str(v[0])):
            rev.append((str(v[0]), str(v[1])[:10]))
    if len(res) < 5:
        raise Pendente("não consegui ler «Mix sin GdO» no XLSX do MITECO")
    return dict(res={"mix_sin_GdO_kgCO2e_kWh": dict(sorted(res.items()))}, shas=[sha(bruto)], atualizado=rev[0][1] if rev else None,
                extra={"url_xlsx": url_x, "versao": rev[0][0] if rev else None, "revisoes": rev[:3],
                       "nota": "«Mix sin GdO» = etiquetado do mix elétrico sem garantias de origem (alcance 2, comercializadoras); não é o mix físico da REE."})


def testar_miteco(r):
    v = r["res"]["mix_sin_GdO_kgCO2e_kWh"]
    assert all(0.1 < x < 0.6 for x in v.values()), "valores fora de 0,1–0,6 kgCO2e/kWh"
    assert str(AGORA.year - 1) in v or str(AGORA.year - 2) in v, "falta o ano recente"


# --------------------------------------------------------------------------------------------- ERSE (XLSX)
def ler_erse(s):
    import openpyxl
    pagina = texto(baixar(s["url"], aceita="text/html"))
    cand = []
    for h, t in re.findall(r'<a[^>]+href="([^"]+\.xlsx)"[^>]*>(.*?)</a>', pagina, re.S):
        t = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", t))
        m = re.search(r"Quadros de Tarifas.*?vigentes a partir de (\d{1,2}) de (\w+) (?:de )?(\d{4})", t)
        if m and sem_acentos(m.group(2)) in MESES:
            d = dt.date(int(m.group(3)), MESES[sem_acentos(m.group(2))], int(m.group(1)))
            if d <= AGORA.date():
                cand.append((d, h, t))
    if not cand:
        raise Pendente("não encontrei o XLSX «Quadros de Tarifas ... vigentes a partir de» na página da ERSE")
    d, h, t = max(cand)
    url_x = h if h.startswith("http") else "https://www.erse.pt" + h
    bruto = baixar(url_x, aceita="*/*", timeout=120)
    wb = openpyxl.load_workbook(io.BytesIO(bruto), data_only=True)
    w = wb["TVCFtrans_CUR_Continente_BT"]
    lin = [[c for c in r if c is not None] for r in w.iter_rows(values_only=True)]
    ini = next(i for i, r in enumerate(lin) if r and isinstance(r[0], str) and "BTN" in r[0] and "20,7" in r[0] and "2,3" in r[0] and "≤" in r[0] and ">" in r[0])
    pot, simples, bih = {}, None, {}
    modo = None
    for r in lin[ini + 1: ini + 25]:
        if r and isinstance(r[0], str) and "BTN" in r[0]:
            break
        if len(r) == 2 and isinstance(r[0], float) and isinstance(r[1], float) and r[0] < 21:
            pot[str(r[0])] = round(r[1], 4)
        if r and isinstance(r[0], str) and r[0].strip().lower() == "tarifa simples" and len(r) == 2:
            simples = round(r[1], 4)
        if r and isinstance(r[0], str) and r[0].strip() == "Tarifa bi-horária" and len(r) == 3:
            bih["fora_de_vazio"] = round(r[2], 4)
        if bih and r and r[0] == "Horas de vazio" and len(r) == 2 and "vazio" not in bih:
            bih["vazio"] = round(r[1], 4)
    if "6.9" not in pot or simples is None:
        raise Pendente("não consegui ler o termo fixo de 6,9 kVA e a tarifa simples no XLSX da ERSE")
    return dict(res={"BTN_ate_20_7_kVA": {"termo_fixo_EUR_dia": pot, "energia_tarifa_simples_EUR_kWh": simples, "energia_bihoraria_EUR_kWh": bih}},
                shas=[sha(bruto)], atualizado=d.isoformat(),
                extra={"url_xlsx": url_x, "texto_da_ligacao": t, "vigencia_desde": d.isoformat(),
                       "nota": "Tarifa transitória de venda a clientes finais (CUR) em Portugal continental, BTN (≤ 20,7 kVA e > 2,3 kVA). A folha não indica o IVA: tratar como valores sem IVA e confirmar no diploma (Diretiva ERSE)."})


def testar_erse(r):
    b = r["res"]["BTN_ate_20_7_kVA"]
    assert 0.08 < b["energia_tarifa_simples_EUR_kWh"] < 0.4, "energia fora de 0,08–0,40 €/kWh"
    assert 0.05 < b["termo_fixo_EUR_dia"]["6.9"] < 1.2, "termo fixo fora do intervalo"
    assert b["termo_fixo_EUR_dia"]["3.45"] < b["termo_fixo_EUR_dia"]["6.9"] < b["termo_fixo_EUR_dia"]["10.35"], "termo fixo deveria crescer com a potência"


# --------------------------------------------------------------------------------------------- ERSAR
def ler_json_lista(b):
    return json.loads("[" + texto(b).strip().lstrip("﻿").strip().rstrip(",") + "]")


def ler_ersar_lista(s):
    b = baixar(s["url"], timeout=60)
    lst = ler_json_lista(b)
    ents = [dict(entidade=x.get("Nome Entidade", "").strip(), localidade=x.get("Localidade Postal", "").strip(), sitio=x.get("Web Site", "").strip()) for x in lst]
    if len(ents) < 200:
        raise Pendente("lista de entidades da ERSAR com menos de 200 linhas")
    return dict(res={"entidades": ents}, shas=[sha(b)], atualizado=None,
                extra={"n": len(ents), "nota": "Só nome, localidade e sítio; moradas, telefones e e-mails do ficheiro original NÃO são guardados."})


def ler_ersar_cqa(s):
    b = baixar(s["url"], timeout=60)
    lst = ler_json_lista(b)
    ult = max(x["Ano"] for x in lst)
    linhas = {x["Concelho"]: dict(entidade=x["Entidade gestora"], agua_segura_pct=x["Agua Segura"]) for x in lst if x["Ano"] == ult}
    if len(linhas) < 270:
        raise Pendente("menos de 270 concelhos no ano mais recente")
    return dict(res={str(ult): linhas}, shas=[sha(b)], atualizado=None,
                extra={"nota": "Entidade gestora do abastecimento em baixa (relatório de qualidade da água) por concelho."})


def ler_ersar_iqs(s, forcar=False):
    cache = os.path.join(DEST, s["id"] + ".json")
    if not forcar and os.path.exists(cache):
        idade = time.time() - os.path.getmtime(cache)
        if idade < 30 * 86400:
            j = json.load(open(cache, encoding="utf-8"))
            return dict(res=j["resumo"], shas=[j["sha256"]], atualizado=j.get("atualizado_pela_fonte"), extra=j.get("extra", {}), de_cache=True)
    base = "https://indicadores-aqs.ersar.pt/api/v1/"
    binit = baixar(base + "initapp", timeout=60)
    init = json.loads(binit)
    ano = init["moments"][-1]
    shas, res = [sha(binit)], {}
    nomes = {1: "agua", 2: "saneamento", 3: "residuos"}
    chave_acess = {1: "AA02b", 2: "AR03b", 3: "RU03b"}
    for c in init["cities"]:
        reg = dict(concelho=c["name"], dico=c["dico"], servicos={})
        for sid, sn in nomes.items():
            b = baixar(base + f"get_city_values?service_id={sid}&system_id=1&city_id={c['id']}&moment={ano}", timeout=60)
            shas.append(sha(b))
            j = json.loads(b)
            re_ = j.get("regulator_entity")
            if not re_:
                continue
            ac = next((i["value"] for i in j["items"] if i["indicator_code"] == chave_acess[sid]), None)
            reg["servicos"][sn] = dict(entidade=re_["entity"], entidade_id=re_["entity_id"], entidade_nome_completo=re_["value"],
                                       modelo_de_gestao=re_["management_model"]["value"], acessibilidade_economica_pct=ac)
            time.sleep(0.3)
        res[str(c["id"])] = reg
    if len(res) < 270:
        raise Pendente("IQS com menos de 270 concelhos")
    return dict(res=res, shas=[sha_lista(shas)], atualizado=None,
                extra={"ano_dos_indicadores": ano, "n_pedidos": len(shas),
                       "nota": "API pública NÃO documentada do painel https://indicadores-aqs.ersar.pt (a mesma que o sítio usa). DICO = código INE de 4 dígitos (distrito+concelho). Acessibilidade económica = encargo anual no rendimento médio disponível (%)."})


def testar_ersar_iqs(r):
    assert len(r["res"]) >= 270 and all("dico" in v for v in r["res"].values())
    n = sum(1 for v in r["res"].values() if {"agua", "saneamento", "residuos"} <= set(v["servicos"]))
    assert n >= 250, f"só {n} concelhos com os três serviços"


# --------------------------------------------------------------------------------------------- verificações de texto legal e documentos
def pagina_texto(url, **kw):
    t = texto(baixar(url, aceita="text/html", timeout=120, **kw))
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    import html as _h
    return _h.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t))), t


def ler_verificacao(s):
    shas, ok = [], {}
    for alvo in s["alvos"]:
        bruto = baixar(alvo["url"], aceita="text/html,application/pdf,*/*", timeout=120)
        shas.append(sha(bruto))
        if alvo["url"].lower().endswith(".pdf"):
            with tempfile.TemporaryDirectory() as d:
                c = os.path.join(d, "x.pdf")
                open(c, "wb").write(bruto)
                x = re.sub(r"\s+", " ", pdf_para_texto(c))
        else:
            import html as _h
            t = re.sub(r"<script.*?</script>|<style.*?</style>", "", texto(bruto), flags=re.S)
            x = _h.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", t)))
        for nome, padrao in alvo["verifica"].items():
            ok[nome] = bool(re.search(padrao, x, re.I))
    return dict(res={"verificacoes": ok}, shas=[sha_lista(shas)], atualizado=None, extra={"alvos": [a["url"] for a in s["alvos"]]})


def testar_verificacao(r):
    falhas = [k for k, v in r["res"]["verificacoes"].items() if not v]
    assert not falhas, "texto legal mudou ou página mudou de formato: " + ", ".join(falhas)


def ler_anqip(s):
    x, t = pagina_texto(s["url"])
    m = re.search(r"ETA 0701\s*-\s*Sistemas de aproveitamento de águas pluviais em edifícios \(Versão (\d+)\)", x)
    m2 = re.search(r"ETA 0702\s*-\s*Certificação de Sistemas de Aproveitamento de Águas Pluviais \(Versão (\d+)\)", x)
    if not m:
        raise Pendente("não encontrei a ETA 0701 na página da ANQIP")
    pdf = re.search(r'href="(https://www\.anqip\.com/storage/[^"]+\.pdf)"[^>]*>\s*ETA 0701', t)
    return dict(res={"ETA_0701_versao": int(m.group(1)), "ETA_0702_versao": int(m2.group(1)) if m2 else None},
                shas=[sha(t.encode("utf-8"))], atualizado=None, extra={"url_pdf_0701": pdf.group(1) if pdf else None})


def ler_bsi(s):
    x, t = pagina_texto(s["url"])
    m = re.search(r"(Withdrawn|Current)[^.]{0,40}?(\d{1,2} \w{3} \d{4})?", x)
    est = "Withdrawn" if re.search(r"Standard\s+Withdrawn", x) else ("Current" if re.search(r"Standard\s+Current", x) else None)
    d = re.search(r"Withdrawn:\s*(\d{1,2} \w{3} \d{4})", x)
    return dict(res={"EN_16941_1_2018_estado_BSI": est, "retirada_em": d.group(1) if d else None}, shas=[sha(t.encode("utf-8"))], atualizado=None, extra={})


# --------------------------------------------------------------------------------------------- catálogo de séries
def eurostat(id, nome, filtro, onde):
    return dict(id=id, nome=nome, url=EUROSTAT + filtro, tipo="eurostat", ler=ler_eurostat, onde_entra=onde, registro_id="EUROSTAT_" + id.split("eurostat_")[-1].upper(),
                licenca="Eurostat: «Reuse of statistical data, metadata, publications, and other dissemination tools published on this website for commercial or non-commercial purposes is authorised provided the source is acknowledged» (copyright-notice, 2026-10-23)")


SERIES = [
    eurostat("eurostat_eletricidade_domestica", "Preço da eletricidade para consumidores domésticos, com impostos (EUR/kWh), banda 2 500–4 999 kWh/ano",
             "nrg_pc_204?format=JSON&lang=EN&geo=PT&geo=ES&nrg_cons=KWH2500-4999&tax=I_TAX&currency=EUR&unit=KWH&sinceTimePeriod=2019-S1", "preço da energia (OPEX da bomba) e custo de energia no ACV"),
    eurostat("eurostat_inflacao_anual", "Inflação anual média (IPCH, todos os bens), variação % ao ano",
             "prc_hicp_aind?format=JSON&lang=EN&geo=PT&geo=ES&coicop=CP00&unit=RCH_A_AVG&sinceTimePeriod=2015", "inflação da análise económica"),
    eurostat("eurostat_preco_eletricidade_sem_impostos", "Preço da eletricidade doméstica sem impostos (EUR/kWh), banda 2 500–4 999 kWh/ano",
             "nrg_pc_204?format=JSON&lang=EN&geo=PT&geo=ES&nrg_cons=KWH2500-4999&tax=X_TAX&currency=EUR&unit=KWH&sinceTimePeriod=2019-S1", "decompor o preço da energia entre energia e impostos"),
    eurostat("eurostat_custo_construcao_habitacao", "Custo de construção de habitação nova, índice trimestral (2021=100), PT e ES",
             "sts_copi_q?format=JSON&lang=EN&geo=PT&geo=ES&indic_bt=COST&unit=I21&cpa2_1=CPA_F41001_X_410014&s_adj=NSA&sinceTimePeriod=2015-Q1", "atualizar o CAPEX no tempo (alternativa ao ICCHN, comparável PT/ES)"),
    dict(id="bce_taxa_refinanciamento", nome="Taxa de juro das operações principais de refinanciamento do BCE (% ao ano)", tipo="bce", ler=ler_bce, registro_id="BCE_MRO",
         url="https://data-api.ecb.europa.eu/service/data/FM/B.U2.EUR.4F.KR.MRR_FR.LEV?format=jsondata&startPeriod=2019-01-01",
         licenca="BCE: «free use of the information obtained directly from it», com citação da fonte e indicação de alterações (ecb.europa.eu, aviso legal, 2026-10-23)",
         onde_entra="referência para a taxa mínima de atratividade"),
    dict(id="ine_pt_icchn", nome="Índice de custo de construção de habitação nova, base 2021 (INE, indicador 0011748): total, materiais, mão-de-obra", tipo="ine_pt", ler=ler_ine_pt, teste=testar_icchn,
         url=INE_PT + "0011748&Dim1=T&Dim2=PT&Dim3=T,1,2", rotulos={"T": "Total", "1": "Materiais", "2": "Mão-de-obra"}, registro_id="INE_ICCHN",
         licenca="INE (conjunto no dados.gov.pt): CC BY 4.0; API: «All data accessed through the API is of public character» e «subject to the terms of use defined by INE»",
         onde_entra="atualizar o CAPEX de Portugal no tempo: preço × I(atual) ÷ I(mês da coleta)"),
    dict(id="ine_pt_ipc_mensal", nome="Índice de preços no consumidor, base 2025 (INE, 0014640): total e produtos energéticos, Portugal", tipo="ine_pt", ler=ler_ine_pt, teste=testar_ipc_mensal,
         url=INE_PT + "0014640&Dim1=T&Dim2=PT&Dim3=T,007", rotulos={"T": "Total", "007": "Produtos energéticos"}, registro_id="INE_IPC",
         licenca="INE: CC BY 4.0 (ver ine_pt_icchn)", onde_entra="atualizar tarifas e OPEX em euros correntes"),
    dict(id="ine_pt_ipc_anual_agua_energia", nome="IPC anual, base 2025 (INE, 0014641): abastecimento de água, recolha de resíduos, recolha de esgotos, eletricidade e total", tipo="ine_pt", ler=ler_ine_pt, teste=testar_ipc_anual,
         url=INE_PT + "0014641&Dim1=T&Dim2=PT&Dim3=T,04411,04420,04431,04510",
         rotulos={"T": "Total", "04411": "Abastecimento de água (rede)", "04420": "Recolha de resíduos sólidos", "04431": "Recolha de esgotos (rede)", "04510": "Eletricidade"}, registro_id="INE_IPC",
         licenca="INE: CC BY 4.0 (ver ine_pt_icchn)", onde_entra="indexar a tarifa de água, saneamento, resíduos e eletricidade de um ano para outro"),
    dict(id="ine_es_agua", nome="INE Espanha: custo unitário do suministro e do saneamiento do agua (EUR/m³), nacional e por comunidade", tipo="ine_es", ler=ler_ine_es_agua, teste=testar_ine_es_agua,
         url=INE_ES + "DATOS_TABLA/53448?nult=1", registro_id="INE_ES_AGUA",
         licenca="INE Espanha, aviso legal: «Creative Commons Reconocimiento 4.0 (CC BY 4.0)» para a informação estatística cuja fonte é o INE",
         onde_entra="preço médio do água e do saneamento da Espanha por comunidade autónoma (referência, não é tarifa municipal)"),
    dict(id="ine_es_codigos_municipios", nome="INE Espanha: relação de municípios e códigos (CPRO+CMUN), 1 de janeiro do ano corrente", tipo="ine_es", ler=ler_ine_es_codigos, teste=testar_ine_es_codigos,
         url="https://www.ine.es/dyngs/INEbase/operacion.htm?c=Estadistica_C&cid=1254736177031&menu=ultiDatos&idp=1254734710990", registro_id="INE_ES_CODMUN",
         licenca="INE Espanha, aviso legal: «Creative Commons Reconocimiento 4.0 (CC BY 4.0)» para a informação estatística cuja fonte é o INE",
         onde_entra="chave de município da Espanha (liga a comunidade/província e a limites do CNIG)"),
    dict(id="ree_fator_emissao_peninsular", nome="REE: fator de emissão da geração elétrica do sistema peninsular (tCO2eq/MWh)", tipo="ree", ler=ler_ree, teste=testar_ree,
         url="https://apidatos.ree.es/es/datos/generacion/no-renovables-detalle-emisiones-CO2", registro_id="REE_EMISSOES",
         licenca="REE: a API «provides a simple REST service to allow third parties to access the backend data»; licença de reutilização NÃO encontrada e o aviso legal geral proíbe a reutilização sem autorização expressa: citar a fonte e confirmar antes de redistribuir",
         onde_entra="carbono operacional da bomba em Espanha (fator por geração; alternativa: MITECO)"),
    dict(id="apa_fator_emissao_pt", nome="APA: fator de emissão de GEE da eletricidade produzida em Portugal (tCO2eq/MWh)", tipo="apa", ler=ler_apa, teste=testar_apa,
         url="https://apambiente.pt/clima/fator-de-emissao-de-gases-de-efeito-de-estufa-para-eletricidade-produzida-em-portugal", registro_id="APA_FE",
         licenca="APA: sem texto de licença na página nem no PDF (nenhuma menção a CC BY); documento público de uma entidade do Estado: citar «APA, Fator de Emissão da Eletricidade»; reutilização geral ao abrigo da Lei 26/2016 (LADA) NÃO verificada",
         onde_entra="carbono operacional da bomba em Portugal"),
    dict(id="miteco_mix_electrico", nome="MITECO: fator de mix elétrico «sin GdO» (kgCO2e/kWh), Registro de huella de carbono", tipo="miteco", ler=ler_miteco, teste=testar_miteco,
         url="https://www.miteco.gob.es/es/cambio-climatico/temas/registro-huella/huella-de-carbonoinscripcion.html", registro_id="MITECO_FE",
         licenca="MITECO: documento oficial «Factores de emisión» do Registro; licença de reutilização do ficheiro NÃO encontrada (a política do portal de dados abertos do MITECO não foi lida): citar a fonte",
         onde_entra="carbono operacional da bomba em Espanha (alcance 2, método de mercado)"),
    dict(id="erse_tarifa_btn", nome="ERSE: tarifa transitória BTN (≤ 20,7 kVA), termo fixo e energia, Portugal continental", tipo="erse", ler=ler_erse, teste=testar_erse,
         url="https://www.erse.pt/atividade/regulacao/tarifas-e-precos-eletricidade/", registro_id="ERSE_TARIFAS",
         licenca="ERSE: licença do ficheiro NÃO encontrada (sem aviso legal localizado no sítio); o valor decorre de diretiva publicada no Diário da República",
         onde_entra="preço regulado da eletricidade (referência; o mercado livre tem ofertas diferentes)"),
    dict(id="ersar_entidades_gestoras", nome="ERSAR: lista de entidades gestoras (nome, localidade, sítio)", tipo="ersar", ler=ler_ersar_lista,
         url="https://www.ersar.pt/docs/Listas/Lista_de_Entidades.json", registro_id="ERSAR_ENTIDADES",
         licenca="ERSAR, Avisos legais: «Os materiais que integram este sítio podem ser copiados ou distribuídos, desde que sejam fornecidas ... Referência ao documento original em www.ersar.pt ... © ERSAR AAAA. Todos os direitos Reservados»",
         onde_entra="lista de entidades gestoras (sítios para o monitor de tarifários)"),
    dict(id="ersar_concelho_entidade_agua", nome="ERSAR: entidade gestora do abastecimento por concelho (relatório de qualidade da água, ano mais recente)", tipo="ersar", ler=ler_ersar_cqa,
         url="https://www.ersar.pt/docs/Listas/Lista_Concelhos_Qualidade_Agua.json", registro_id="ERSAR_CONCELHO_ENTIDADE",
         licenca="ERSAR, Avisos legais (ver ersar_entidades_gestoras)", onde_entra="ligar concelho a entidade gestora da água"),
    dict(id="ersar_concelho_entidade_iqs", nome="ERSAR IQS: entidade gestora de cada concelho para água, saneamento e resíduos (+ código INE DICO)", tipo="ersar_iqs", ler=ler_ersar_iqs, teste=testar_ersar_iqs,
         url="https://indicadores-aqs.ersar.pt/api/v1/initapp", registro_id="ERSAR_IQS",
         licenca="ERSAR, Avisos legais (ver ersar_entidades_gestoras); a API é pública mas NÃO documentada",
         onde_entra="ligar concelho (código INE) à entidade de cada serviço; base da tabela entidades.json"),
    dict(id="verificacao_iva_pt_es", nome="Verificação do texto legal do IVA: Lista I do CIVA (AT) e arts. 90–91 da Ley 37/1992 (BOE) e Ofício-circulado 25031/2024", tipo="verificacao", ler=ler_verificacao, teste=testar_verificacao,
         url="https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/c-iva-listas.aspx", registro_id="IVA_PT",
         licenca="Textos legais oficiais (AT, BOE, DR): reprodução livre de atos oficiais; a versão consolidada do BOE «es informativa y no tiene valor jurídico»",
         onde_entra="alertar se as taxas de IVA (água, saneamento, resíduos, obras, eletricidade) mudarem",
         alvos=[dict(url="https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/c-iva-listas.aspx",
                     verifica={"PT verba 1.7 água (6%)": r"1\.7 - Água, com exce", "PT verba 2.22 resíduos (6%)": r"2\.22 - Presta..es de servi.os relacionadas com a limpeza das vias p.blicas, bem como a recolha",
                               "PT verba 2.27 empreitadas de beneficiação de habitação": r"2\.27 - As empreitadas de benefici", "PT verba 2.35 águas residuais tratadas": r"2\.35 - .guas residuais tratadas",
                               "PT verba 2.38 eletricidade ≤ 6,9 kVA até 200 kWh": r"2\.38 - Fornecimento de eletricidade para consumo", "PT verba 2.42 construção de habitação (DL 97/2026)": r"2\.42\(?\*?\)? - As empreitadas de constru"}),
                dict(url="https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/civa_rep/Pages/iva18.aspx",
                     verifica={"PT art. 18.º taxas 6/13/23": r"taxa de 6%.*taxa de 13%.*taxa de 23%"}),
                dict(url="https://www.boe.es/buscar/act.php?id=BOE-A-1992-28740&p=20260101&tn=1",
                     verifica={"ES art. 90 tipo general 21%": r"Se exigir. al tipo del 21 por ciento", "ES art. 91 agua 10% (aguas aptas para la alimentación humana)": r"Las aguas aptas para la alimentaci.n humana o animal o para el riego",
                               "ES art. 91 saneamiento y residuos 10%": r"recogida o tratamiento de las aguas residuales", "ES art. 91 obras de vivienda 10%": r"Las ejecuciones de obras, con o sin aportaci.n de materiales, consecuencia de contratos directamente formalizados entre el promotor y el contratista que tengan por objeto la construcci.n o rehabilitaci.n de edificaciones",
                               "ES art. 91 renovação/reparação de vivienda 10%": r"Las ejecuciones de obra de renovaci.n y reparaci.n realizadas en edificios"}),
                dict(url="https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/legislacao/instrucoes_administrativas/Documents/Oficio_circulado_25031_2024.pdf",
                     verifica={"OC 25031/2024: abastecimento de água 6% (verba 1.7)": r"abastecimento de .gua.{0,400}taxa\s+reduzida \(6%\)", "OC 25031/2024: saneamento por autarquias fora do campo do imposto": r"fora do campo de aplica..o do imposto"})]),
    dict(id="verificacao_rt_aguas_ersar", nome="Verificação: Regulamento Tarifário dos Serviços de Águas (ERSAR, Reg. 1160/2026) continua listado como o regulamento vigente", tipo="verificacao", ler=ler_verificacao, teste=testar_verificacao,
         url="https://www.ersar.pt/pt_legislacao_legislacao-do-setor_regulamentos-ersar.html", registro_id="ERSAR_RT",
         licenca="ERSAR, Avisos legais (ver ersar_entidades_gestoras); o ato oficial está no Diário da República (diariodarepublica.pt, página dinâmica: aberta no navegador)",
         onde_entra="alertar se sair novo regulamento tarifário ou alteração",
         alvos=[dict(url="https://www.ersar.pt/pt_legislacao_legislacao-do-setor_regulamentos-ersar.html",
                     verifica={"Regulamento n.º 1160/2026 listado": r"Regulamento n\.. 1160/2026, de 10 de setembro", "sumário: regras de definição, cálculo, revisão, atualização e publicitação das tarifas": r"definição, cálculo, revisão, atualização e publicitação das tarifas"})]),
    dict(id="anqip_eta_0701", nome="ANQIP: versões publicadas da ETA 0701 (SAAP em edifícios) e ETA 0702", tipo="anqip", ler=ler_anqip,
         url="https://anqip.pt/pt/comissoes-tecnicas-e-especificacoes-anqip", registro_id="ANQIP_ETA0701",
         licenca="ANQIP: licença/direitos de reprodução da ETA NÃO encontrados (o PDF é de acesso livre); citar «ANQIP, ETA 0701, versão N»",
         onde_entra="norma técnica portuguesa de aproveitamento de água da chuva"),
    dict(id="bsi_en_16941_1_estado", nome="Estado da EN 16941-1:2018 (BSI Knowledge)", tipo="bsi", ler=ler_bsi,
         url="https://knowledge.bsigroup.com/products/on-site-non-potable-water-systems-systems-for-the-use-of-rainwater", registro_id="EN_16941_1",
         licenca="BSI: página de catálogo (sem reutilização de texto da norma)", onde_entra="saber se a EN 16941-1 citada é a edição vigente"),
]


# --------------------------------------------------------------------------------------------- execução
def processar(s, args):
    try:
        if s["tipo"] == "ersar_iqs":
            r = ler_ersar_iqs(s, forcar="--iqs" in args)
        else:
            r = s["ler"](s) if "alvos" not in s else s["ler"](s)
        teste = s.get("teste")
        if teste:
            teste(r)
        reg = dict(id=s["id"], nome=s["nome"], url=s["url"], licenca=s["licenca"], onde_entra=s["onde_entra"], acesso=AGORA_S,
                   sha256=r["shas"][0] if len(r["shas"]) == 1 else sha_lista(r["shas"]), n_respostas=len(r["shas"]),
                   atualizado_pela_fonte=r.get("atualizado"), extra=r.get("extra", {}), resumo=r["res"])
        if not r.get("de_cache"):
            json.dump(reg, open(os.path.join(DEST, s["id"] + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        return reg, None
    except AssertionError as e:
        return None, f"teste falhou: {e}"
    except Pendente as e:
        return None, f"pendente: {e}"
    except Exception as e:  # noqa
        return None, f"{type(e).__name__}: {e}"


def linha_ultimos(res):
    out = []
    for k, v in res.items():
        if isinstance(v, dict) and v and all(not isinstance(x, (dict, list)) for x in v.values()):
            out.append(f"- {k}: " + ", ".join(f"{t} = {x}" for t, x in ultimos(v)))
        elif isinstance(v, dict) and v:
            out.append(f"- {k}: {len(v)} entradas")
        else:
            out.append(f"- {k}: {v if not isinstance(v, list) else str(len(v)) + ' itens'}")
    return out


def main(args):
    os.makedirs(DEST, exist_ok=True)
    so = [a for a in args if not a.startswith("--")]
    if "--so" in args:
        so = args[args.index("--so") + 1:]
    linhas = ["# Séries públicas coletadas automaticamente", "", f"Coletado em {AGORA_S}. Reexecutar `python coletar_series_publicas.py` para atualizar. "
              "Cada série tem teste interno; se falhar, fica «pendente» e o ficheiro anterior (se existir) não é sobrescrito.", ""]
    estados = {}
    for s in SERIES:
        if so and not any(s["id"].startswith(p) for p in so):
            continue
        t0 = time.time()
        reg, erro = processar(s, args)
        dur = time.time() - t0
        if reg:
            estados[s["registro_id"]] = dict(estado="ok", sha256=reg["sha256"], data=AGORA_S)
            linhas += [f"## {s['nome']}", f"- Fonte: {s['url']}", f"- Licença: {s['licenca']}", f"- Entra em: {s['onde_entra']}",
                       f"- SHA-256 da(s) resposta(s): `{reg['sha256'][:16]}…` ({reg['n_respostas']} resposta(s)); atualizado pela fonte: {reg['atualizado_pela_fonte']}"]
            linhas += linha_ultimos(reg["resumo"])
            if reg["extra"].get("nota"):
                linhas.append(f"- Nota: {reg['extra']['nota']}")
            linhas.append("")
            print(f"ok     {s['id']} ({dur:.0f} s)")
        else:
            estados[s["registro_id"]] = dict(estado="pendente: " + erro, sha256=None, data=AGORA_S)
            linhas += [f"## {s['nome']}", f"- **Pendente**: {erro}. Fonte: {s['url']}", ""]
            print(f"FALHOU {s['id']}: {erro}")
    if not so:
        open(os.path.join(DEST, "RESUMO.md"), "w", encoding="utf-8").write("\n".join(linhas))
    # atualiza o registo legível por máquina, se existir
    cam = os.path.join(DEST, "registro_fontes.json")
    if os.path.exists(cam):
        reg = json.load(open(cam, encoding="utf-8"))
        n = 0
        for f in reg.get("fontes", []):
            e = estados.get(f.get("id"))
            if e:
                f["ultimo_teste_automatico"] = e
                n += 1
        json.dump(reg, open(cam, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"registro_fontes.json atualizado em {n} entradas")


if __name__ == "__main__":
    main(sys.argv[1:])
