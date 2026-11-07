# -*- coding: utf-8 -*-
"""Monta ``entidades.json`` a partir do índice público de tarifários por concelho da ERSAR.

Ferramenta de desenvolvimento (fica fora do Git, como os demais ``tarifas_portugal/*.py``).

Fonte aberta e verificada: a página «Pesquisa por concelho» da ERSAR
(https://www.ersar.pt/pt_consumidor_tarifas-dos-servicos_encargos-tarifarios_pesquisa-por-concelho_ano.html)
carrega o ficheiro ``tarifa-concelho.json``, que liga cada concelho de Portugal continental, por
ano (2024 a 2026) e por serviço (AA água, AR águas residuais, RU resíduos urbanos), à entidade
gestora e à ficha tarifária em PDF. Quem decide o concelho→entidade é esse ficheiro, no ano mais
recente de cada concelho e serviço; nada é inferido do nome da entidade.

O que a ERSAR não cobre (Funchal e Ponta Delgada, regiões autónomas; Leiria na água e saneamento;
Ponte de Lima nos resíduos) vem do próprio documento tarifário (Funchal, Ponta Delgada, Leiria) ou
fica «a identificar».

``entidades.json`` guarda três coisas:
  * ``concelhos``: os 280 concelhos (278 do continente + Funchal e Ponta Delgada), com distrito e a
    ficha ERSAR mais recente de cada serviço;
  * ``entidades``: entidade gestora → serviço → concelhos servidos → documentos;
  * ``documentos``: os documentos de ``fontes/FONTES.tsv`` agrupados por documento lógico (um
    tarifário pode ter vários ficheiros), com entidade, serviços, vigência e se nomeiam o concelho.
Os ``documentos`` são curados à mão (abaixo, ``DOCUMENTOS``) e preservados quando o ficheiro já existe.

Uso (na pasta ``triton_ibe``):
    python tarifas_portugal/importar_ersar.py [--indice caminho/tarifa-concelho.json] [--cabecas cabecas.json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import unicodedata
from collections import defaultdict
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SAIDA = os.path.join(AQUI, "entidades.json")
INDICE = os.path.join(AQUI, "fontes", "_indice_ersar", "tarifa-concelho.json")
URL_INDICE = "https://www.ersar.pt/docs/pesquisa-tarifa-concelho/tarifa-concelho.json"
URL_PAGINA = ("https://www.ersar.pt/pt_consumidor_tarifas-dos-servicos_encargos-tarifarios_"
              "pesquisa-por-concelho_ano.html")
SERVICO = {"AA": "agua", "AR": "saneamento", "RU": "residuos"}
ACESSO = "2026-10-23"

#: Regiões autónomas: fora do índice da ERSAR (a regulação é da ERSARA nos Açores).
ILHAS = {"Funchal": ("Região Autónoma da Madeira", "Ilha da Madeira", "3103"),
         "Ponta Delgada": ("Região Autónoma dos Açores", "Ilha de São Miguel", "4203")}

# --------------------------------------------------------------------------------------------
# Documentos de fontes/FONTES.tsv, um por documento lógico. Cada ``ficheiros`` é o caminho em
# FONTES.tsv. ``concelhos``: os que o documento nomeia (ou o concelho único da entidade);
# ``entidade_toda``: o documento é da entidade e não nomeia concelhos (vale-lhe a ficha ERSAR:
# a aplicação a cada concelho da entidade fica a confirmar). ``tipo``: oficial | secundario |
# indice | fora_do_tema. ``vigencia_inicio`` (ISO) e ``vigencia_precisao`` (dia | mes | ano |
# publicacao): só o que o documento ou o LEIA.md registam; sem isso, o ano do tarifário.
# --------------------------------------------------------------------------------------------
DOCUMENTOS = {
    "porto_geral_2026": {
        "titulo": "Águas e Energia do Porto, Tarifário Geral 2026", "tipo": "oficial",
        "ficheiros": ["Aguas_do_Porto/Tarifario_Geral_2026.pdf"],
        "entidade": "Águas e Energia do Porto", "servicos": ["agua", "saneamento"], "concelhos": ["Porto"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": True},
    "lisboa_epal_2026": {
        "titulo": "EPAL, preços de venda de água, 1.ª edição 2026", "tipo": "oficial",
        "ficheiros": ["EPAL_Lisboa/precos-2026.pdf"],
        "entidade": "EPAL", "servicos": ["agua"], "concelhos": ["Lisboa"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": True},
    "lisboa_cml_2026": {
        "titulo": "CML, tarifários do saneamento e dos resíduos urbanos 2026", "tipo": "oficial",
        "ficheiros": ["CM_Lisboa/tarifario_saneamento_2026.pdf", "CM_Lisboa/tarifario_residuos_urbanos_2026.pdf"],
        "entidade": "CM de Lisboa", "servicos": ["saneamento", "residuos"], "concelhos": ["Lisboa"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": True},
    "funchal_taxas_2026": {
        "titulo": "Câmara Municipal do Funchal, Tabela de Taxas e Outras Receitas Municipais 2026", "tipo": "oficial",
        "ficheiros": ["CM_Funchal/Tabela_de_Taxas_Municipais_2026_.pdf"],
        "entidade": "Câmara Municipal do Funchal", "servicos": ["agua", "saneamento", "residuos"],
        "concelhos": ["Funchal"], "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": True,
        "nota": "A entidade vem do próprio documento (artigos 6.º, 10.º, 56.º e 57.º); o Funchal está fora do índice da ERSAR."},
    "coimbra_agua_saneamento_2026": {
        "titulo": "Águas de Coimbra, tarifários da água e das águas residuais 2026 (Edital n.º 438/2025)", "tipo": "oficial",
        "ficheiros": ["Aguas_de_Coimbra/Edital-n.o-438_2025.pdf", "Aguas_de_Coimbra/Tarifario-Abastecimento-de-Agua.pdf",
                      "Aguas_de_Coimbra/Tarifario-Aguas-Residuais.pdf"],
        "entidade": "Águas de Coimbra", "servicos": ["agua", "saneamento"], "concelhos": ["Coimbra"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False},
    "coimbra_residuos_2026": {
        "titulo": "Câmara Municipal de Coimbra, tarifário de resíduos urbanos 2026 (Edital n.º 433/2025)", "tipo": "oficial",
        "ficheiros": ["Aguas_de_Coimbra/Edital-n.o-433_2025.pdf"],
        "entidade": "CM de Coimbra", "servicos": ["residuos"], "concelhos": ["Coimbra"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False},
    "braga_agere_2026": {
        "titulo": "AGERE, tarifário 2026 (fevereiro)", "tipo": "oficial",
        "ficheiros": ["AGERE_Braga/AGERE_Tarifario-Fev2026.pdf"],
        "entidade": "AGERE", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Braga"],
        "vigencia_inicio": "2026-02-01", "vigencia_precisao": "mes", "transcrito": False},
    "setubal_sms_2026": {
        "titulo": "SMS Setúbal, tarifários 2026 da água, do saneamento e dos resíduos", "tipo": "oficial",
        "ficheiros": ["SMS_Setubal/01-Tarifario-2026_Agua.pdf", "SMS_Setubal/02-Tarifario-2026_Saneamento.pdf",
                      "SMS_Setubal/Tarifario-2026_Residuos-VC.pdf"],
        "entidade": "SM de Setúbal", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Setúbal"],
        "vigencia_inicio": "2026-03-04", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "«Entrada em vigor a partir do dia 04/03/2026», impresso nos três documentos."},
    "leiria_smas_2026": {
        "titulo": "SMAS Leiria, tarifário de água e saneamento 2026", "tipo": "oficial",
        "ficheiros": ["SMAS_Leiria/tarifario_2026_F.pdf"],
        "entidade": "SMAS de Leiria", "servicos": ["agua", "saneamento"], "concelhos": ["Leiria"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "A ERSAR não lista a água e o saneamento de Leiria no índice; a entidade vem do documento. Sem resíduos (a ERSAR indica a CM de Leiria)."},
    "faro_fagar_2026": {
        "titulo": "FAGAR, tarifário para 2026 (água, saneamento e resíduos urbanos)", "tipo": "oficial",
        "ficheiros": ["FAGAR_Faro/tarifario_2026.pdf"],
        "entidade": "FAGAR - Faro", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Faro"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "Documento digitalizado (sem texto): conferido à vista na página 1."},
    "aveiro_adra_2026": {
        "titulo": "AdRA, tarifário 2026", "tipo": "oficial",
        "ficheiros": ["AdRA_Aveiro/ADRA_TARIFARIO2026_H_ONLINE_0.pdf"],
        "entidade": "Águas da Região de Aveiro", "servicos": ["agua", "saneamento"], "entidade_toda": True,
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "«A aplicar a partir de 1 de janeiro de 2026». Não nomeia concelhos."},
    "viseu_smas_2026": {
        "titulo": "Águas de Viseu (SMAS), tarifários de abril de 2026", "tipo": "oficial",
        "ficheiros": ["Aguas_de_Viseu/Tarifarios_Aguas_Viseu-ABR2026.pdf"],
        "entidade": "SMAS de Viseu", "servicos": ["agua", "saneamento"], "concelhos": ["Viseu"],
        "vigencia_inicio": "2026-04-01", "vigencia_precisao": "mes", "transcrito": False},
    "beja_emas_2025": {
        "titulo": "EMAS Beja, tarifário 2025", "tipo": "oficial",
        "ficheiros": ["EMAS_Beja/Tarifario_2025.pdf"],
        "entidade": "EMAS de Beja", "servicos": ["agua", "saneamento"], "concelhos": ["Beja"],
        "vigencia_inicio": "2025-01-01", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "Em vigor desde 01/01/2025 (LEIA.md); a ERSAR já tem ficha de 2026 para a água de Beja."},
    "evora_cm_2025": {
        "titulo": "Câmara Municipal de Évora, tarifário 2025 (água, saneamento e resíduos)", "tipo": "oficial",
        "ficheiros": ["CM_Evora/Tarifario-2025.pdf"],
        "entidade": "CM de Évora", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Évora"],
        "vigencia_inicio": "2025-02-01", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "«Entra em vigor no dia 1 de fevereiro de 2025» (impresso no edital)."},
    "castelo_branco_sm_2026": {
        "titulo": "SM Castelo Branco, tarifário em vigor (publicado em 24/02/2026)", "tipo": "oficial",
        "ficheiros": ["SM_Castelo_Branco/Tarifario_em_vigor_2026-02-24.pdf"],
        "entidade": "SM de Castelo Branco", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Castelo Branco"],
        "vigencia_inicio": "2026-02-24", "vigencia_precisao": "publicacao", "transcrito": False,
        "nota": "A data é a da publicação do documento; o início da vigência não vem impresso."},
    "santarem_aguas_2026": {
        "titulo": "Águas de Santarém, páginas do tarifário geral e do saneamento 2026", "tipo": "oficial",
        "ficheiros": ["Aguas_de_Santarem/tarifario-geral-2026.html", "Aguas_de_Santarem/tarifario-servicos-de-saneamento-2026.html"],
        "entidade": "Águas de Santarém", "servicos": ["agua", "saneamento"], "concelhos": ["Santarém"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "Páginas HTML do sítio da entidade, não um documento assinado."},
    "ponta_delgada_smas_2026": {
        "titulo": "SMAS Ponta Delgada, tarifário 2026 (sem atualização: vale o de 2025)", "tipo": "oficial",
        "ficheiros": ["SMAS_Ponta_Delgada/tarifario-2026.pdf"],
        "entidade": "SMAS de Ponta Delgada", "servicos": ["agua", "saneamento"], "concelhos": ["Ponta Delgada"],
        "vigencia_inicio": "2025-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "O próprio documento diz que em 2026 não houve atualização e que o tarifário em vigor é o de 2025; a data de início de 2025 não vem impressa. Os resíduos não constam."},
    "alto_minho_adam_2026": {
        "titulo": "Águas do Alto Minho, cartaz do tarifário 2026 (água e saneamento)", "tipo": "oficial",
        "ficheiros": ["Aguas_do_Alto_Minho/tarifario_AdM2026_Cartaz.pdf"],
        "entidade": "Águas do Alto Minho", "servicos": ["agua", "saneamento"], "entidade_toda": True,
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "Cartaz da entidade, sem concelhos nomeados; saneamento = 90 % da tarifa variável da água (LEIA.md)."},
    "portalegre_smat_2026": {
        "titulo": "SMAT Portalegre, edital de 2026 (imagens, páginas 1 a 5)", "tipo": "oficial",
        "ficheiros": [f"SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-000{n}.jpg"
                      for n in (1, 2, 3, 4, 5)],
        "entidade": "SMAT de Portalegre", "servicos": ["agua", "saneamento"], "concelhos": ["Portalegre"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "Sem resíduos no edital (LEIA.md)."},
    "guarda_cm_2026": {
        "titulo": "Câmara Municipal da Guarda, Edital n.º 16/2026", "tipo": "oficial",
        "ficheiros": ["CM_Guarda/Edital_16-2026_tarifario.pdf"],
        "entidade": "CM de Guarda", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Guarda"],
        "vigencia_inicio": "2026-02-09", "vigencia_precisao": "dia", "transcrito": False,
        "nota": "Edital da Câmara: «em vigor a partir do dia 09-02-2026» (página 1). Divergência: no índice da ERSAR a água e o saneamento da Guarda, em 2025, são da entidade «Águas Públicas em Altitude»."},
    "vila_real_adin_2026": {
        "titulo": "ADIN (Águas do Interior - Norte), Tarifas 2026", "tipo": "oficial",
        "ficheiros": ["ADIN_Vila_Real/Tarifas_2026.pdf"],
        "entidade": "Águas do Interior - Norte", "servicos": ["agua", "saneamento"], "entidade_toda": True,
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False,
        "nota": "Uma página, sem concelhos nomeados."},
    "vila_real_residuos_2026": {
        "titulo": "Câmara Municipal de Vila Real, tarifário de resíduos 2026", "tipo": "oficial",
        "ficheiros": ["CM_Vila_Real/tarifario_residuos_2026.pdf"],
        "entidade": "CM de Vila Real", "servicos": ["residuos"], "concelhos": ["Vila Real"],
        "vigencia_inicio": "2026-01-01", "vigencia_precisao": "ano", "transcrito": False},
    "braganca_edital_68_2020": {
        "titulo": "Câmara Municipal de Bragança, Edital n.º 68/2020 (água, águas residuais e RSU), reproduzido na ficha APFN", "tipo": "oficial",
        "ficheiros": ["CM_Braganca/APFN_ficha_Braganca_Edital_68-2020.pdf"],
        "entidade": "CM de Bragança", "servicos": ["agua", "saneamento", "residuos"], "concelhos": ["Bragança"],
        "vigencia_inicio": "2021-01-01", "vigencia_precisao": "mes", "transcrito": False,
        "nota": "Em vigor desde janeiro de 2021; falta o tarifário atual. Hoje os resíduos de Bragança são, segundo a ERSAR, de «Resíduos do Nordeste»."},
    "funchal_apfn_2024": {
        "titulo": "Ficha APFN do Funchal (2024), para conferir", "tipo": "secundario",
        "ficheiros": ["_secundarios/APFN_Estudo_Agua_Ficha_2024_290.pdf"], "servicos": [], "concelhos": ["Funchal"]},
    "braganca_apfn_2018": {
        "titulo": "Ficha APFN de Bragança (2018), anterior ao edital de 2020", "tipo": "secundario",
        "ficheiros": ["_secundarios/APFN_ficha_Braganca_2018.pdf"], "servicos": [], "concelhos": ["Bragança"]},
    "fora_do_tema_ipi": {
        "titulo": "Artigo sobre o IPI brasileiro, entregue por engano", "tipo": "fora_do_tema",
        "ficheiros": ["_fora_do_tema/2316,+A+EXTRAFISCALIDADE+TRIBUTÁRIA+DO+IPI.pdf"], "servicos": [], "concelhos": []},
    "indice_ersar": {
        "titulo": "ERSAR, índice de tarifários por concelho (tarifa-concelho.json)", "tipo": "indice",
        "ficheiros": ["_indice_ersar/tarifa-concelho.json"], "servicos": [], "concelhos": []},
}


def sem_acentos(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower().strip()


def concelhos_da_base() -> dict:
    """278 concelhos do continente (base E-OBS do programa) + Funchal e Ponta Delgada."""
    db = os.path.join(RAIZ, "data", "portugal_eobs.db")
    con = sqlite3.connect(db)
    out = {nome: {"distrito": dist, "regiao": "Continente", "dtmn": dtmn}
           for dtmn, nome, dist in con.execute("select dtmn, concelho, distrito from series order by concelho")}
    con.close()
    for nome, (distrito, ilha, dtmn) in ILHAS.items():
        out[nome] = {"distrito": distrito, "regiao": "Região Autónoma", "ilha": ilha, "dtmn": dtmn}
    return out


def vigencia_curta(d: dict) -> str:
    """A vigência como vai em FONTES.tsv: aaaa-mm-dd, aaaa-mm, aaaa ou pub:aaaa-mm-dd."""
    iso, prec = d.get("vigencia_inicio", ""), d.get("vigencia_precisao", "")
    if not iso:
        return ""
    return {"dia": iso, "mes": iso[:7], "ano": iso[:4], "publicacao": "pub:" + iso}.get(prec, iso)


FONTES_TSV = os.path.join(AQUI, "fontes", "FONTES.tsv")
#: colunas de FONTES.tsv: as quatro primeiras são as de sempre (lidas por gerar_apendices.py)
COLUNAS_FONTES = ["caminho", "url", "sha256", "data_coleta", "entidade", "concelhos", "tipo", "vigencia",
                  "confirmado_em", "verificado_por", "redistribuivel"]


def atualizar_fontes_tsv(documentos: dict) -> None:
    """Completa FONTES.tsv com o registo mínimo (11 colunas, sem cabeçalho), preservando o que lá estiver
    em ``confirmado_em``, ``verificado_por`` e ``redistribuivel``. Predefinição: confirmado_em = data da
    coleta; verificado_por vazio; redistribuivel 0 (os documentos de terceiros não vão no instalador)."""
    por_ficheiro = {f: d for d in documentos.values() for f in d["ficheiros"]}
    linhas = []
    with open(FONTES_TSV, encoding="utf-8") as f:
        for linha in f:
            c = linha.rstrip(chr(10)).rstrip(chr(13)).split(chr(9))
            if not c or not c[0]:
                continue
            c += [""] * (11 - len(c))
            d = por_ficheiro.get(c[0])
            if d is None:
                raise SystemExit(f"FONTES.tsv tem {c[0]}, que nenhum documento de entidades.json lista")
            conc = ";".join(d.get("concelhos", [])) or ("entidade inteira: " + d["entidade"] if d.get("entidade_toda") else "")
            c[4], c[5], c[6], c[7] = d.get("entidade", ""), conc, d["tipo"], vigencia_curta(d)
            c[8] = c[8] or c[3]
            c[10] = c[10] or "0"
            linhas.append(c[:11])
    with open(FONTES_TSV, "w", encoding="utf-8", newline="") as f:
        for c in linhas:
            f.write(chr(9).join(c) + chr(10))


def principal(indice_path: str, cabecas_path: str | None) -> None:
    with open(indice_path, "rb") as f:
        bruto = f.read()
    sha = hashlib.sha256(bruto).hexdigest()
    registos = json.loads(bruto.decode("utf-8-sig"))
    base = concelhos_da_base()
    por_norma = {sem_acentos(n): n for n in base}
    cabecas = {}
    if cabecas_path and os.path.isfile(cabecas_path):
        with open(cabecas_path, encoding="utf-8") as f:
            cabecas = json.load(f)

    # última ficha por concelho × serviço × entidade
    ultima = {}
    desconhecidos = set()
    for r in registos:
        nome = por_norma.get(sem_acentos(r["Concelho"]))
        if nome is None:
            desconhecidos.add(r["Concelho"])
            continue
        k = (nome, SERVICO[r["Servico"]], r["Entidade gestora"])
        if k not in ultima or r["Ano"] > ultima[k]["Ano"]:
            ultima[k] = r
    if desconhecidos:
        raise SystemExit(f"concelhos do índice ERSAR fora da base: {sorted(desconhecidos)}")

    # no ano mais recente de cada concelho × serviço
    ano_max = {}
    for (c, s, e), r in ultima.items():
        ano_max[(c, s)] = max(ano_max.get((c, s), "0000"), r["Ano"])
    concelhos = {nome: dict(meta, fichas_ersar={}) for nome, meta in base.items()}
    entidades = defaultdict(lambda: {"fonte": "ersar", "servicos": {}})
    for (c, s, e), r in sorted(ultima.items()):
        if r["Ano"] != ano_max[(c, s)]:
            continue
        ficha = {"entidade": e, "ano": int(r["Ano"]), "url": r["Ficheiro"], "tarifario": r.get("Tarifário", "")}
        h = cabecas.get(r["Ficheiro"])
        if h:
            ficha["http"] = h.get("status")
            if h.get("bytes"):
                ficha["bytes"] = h["bytes"]
        concelhos[c]["fichas_ersar"].setdefault(s, []).append(ficha)
        entidades[e]["servicos"].setdefault(s, {"concelhos": [], "documentos": []})["concelhos"].append(c)

    # documentos curados: preservados se o ficheiro já existe
    documentos = DOCUMENTOS
    if os.path.isfile(SAIDA):
        with open(SAIDA, encoding="utf-8") as f:
            antigo = json.load(f)
        if antigo.get("documentos"):
            documentos = antigo["documentos"]

    # entidades que só o documento revela (fora do índice da ERSAR)
    for did, d in documentos.items():
        e = d.get("entidade")
        if not e or d["tipo"] != "oficial":
            continue
        ent = entidades[e]
        if e not in {x for (_, _, x) in ultima}:
            ent["fonte"] = "documento"
        for s in d["servicos"]:
            alvo = ent["servicos"].setdefault(s, {"concelhos": [], "documentos": []})
            for c in d.get("concelhos", []):
                if c not in alvo["concelhos"]:
                    alvo["concelhos"].append(c)
            alvo["documentos"].append(did)
    # documentos de entidade inteira: ligar a todos os concelhos que a ERSAR lhe atribui
    for did, d in documentos.items():
        if d.get("entidade_toda"):
            for s in d["servicos"]:
                alvo = entidades[d["entidade"]]["servicos"].get(s)
                if alvo and did not in alvo["documentos"]:
                    alvo["documentos"].append(did)
    for e in entidades.values():
        for s in e["servicos"].values():
            s["concelhos"] = sorted(set(s["concelhos"]))

    saida = {
        "_formato": ("Entidade gestora → serviço (água, saneamento, resíduos) → concelhos servidos → documentos de "
                     "fontes/FONTES.tsv. 'concelhos' traz os 280 concelhos (278 do continente + Funchal e Ponta Delgada) "
                     "com distrito e a ficha tarifária ERSAR mais recente de cada serviço. 'entidades' e 'concelhos' saem "
                     "do índice da ERSAR (importar_ersar.py); 'documentos' é curado à mão. Concelho ou serviço sem entidade "
                     "verificada fica sem entrada: o módulo escreve «entidade a identificar»."),
        "_verificacao": {
            "indice_ersar": {"pagina": URL_PAGINA, "url": URL_INDICE, "sha256": sha, "acedido_em": ACESSO,
                             "registos": len(registos), "anos": sorted({r["Ano"] for r in registos}),
                             "ficheiro": "fontes/_indice_ersar/tarifa-concelho.json"},
            "fichas_ersar": ("URL de cada ficha tarifária do índice; 'http' = resposta ao pedido HEAD de "
                             + ACESSO + " (200 = a ficha existe), quando verificada."),
            "ilhas": "Funchal e Ponta Delgada estão fora do índice da ERSAR: a entidade vem do documento arquivado.",
        },
        "documentos": documentos,
        "entidades": {k: entidades[k] for k in sorted(entidades, key=lambda x: sem_acentos(x))},
        "concelhos": {k: concelhos[k] for k in sorted(concelhos, key=sem_acentos)},
    }
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        json.dump(saida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    atualizar_fontes_tsv(documentos)
    print(f"entidades.json: {len(concelhos)} concelhos, {len(entidades)} entidades, {len(documentos)} documentos")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--indice", default=INDICE)
    ap.add_argument("--cabecas", default=None, help="JSON {url: {status, bytes}} da verificação HEAD das fichas")
    a = ap.parse_args()
    principal(a.indice, a.cabecas)
