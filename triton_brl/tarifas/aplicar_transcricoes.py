# -*- coding: utf-8 -*-
"""Aplica ao banco tarifário as tabelas transcritas dos documentos oficiais recebidos.

Cada arquivo `tarifas/transcricoes/<prestador>.json` transcreve **um documento** guardado
em `tarifas/fontes/` e registrado em `fontes/registro.json`. O documento pode trazer
várias tabelas (a SABESP tem uma por região); cada tabela diz a quais municípios se
aplica e traz a residencial e as demais categorias que o documento publica:

    {
      "prestador": "SABESP",
      "registro": [11],                       # itens de fontes/registro.json
      "documento": "NT_1__REAJUSTE....pdf",
      "vigencia": "01/01/2026",
      "fonte_url": "https://...",
      "leitura": "o que o documento é e como foi lido",
      "tabelas": [{
        "rotulo": "Tabela 1 (p. 9): RMSP",
        "uf": "SP",
        "municipios": ["Arujá", "Barueri"],
        "prestador": "...",                    # opcional: corrige o prestador do município
        "abrangencia": "...",                  # opcional: por que vale para estes municípios
        "representativa": "...",               # opcional: a residencial é uma entre várias
        "variantes": {"Área A": EST, ...},     # opcional: as outras tabelas do município
        "situacao": "ruim", "motivo": "...",   # opcional: o documento desmente a base
        "espera": [{"consumo_m3": 10, "conta_agua": 31.15}],  # opcional: a marca só entra se a base divergir
        "residencial": EST, "comercial": EST, "publica": EST, "industrial": EST, "social": EST
      }],
      "conferencia": [...]                     # valores impressos, conferidos pelos testes
    }

Documento geral, que não nomeia cada município (a tabela única de um prestador, a de
uma região ou área), entra com a lista explícita dos municípios a que se aplica e, em
`abrangencia`, a regra que a fundamenta («tabela única da Rio+ Saneamento: todos os
municípios que a base atribui a ela»). A regra vai para o município como
`fonte_abrangencia`, para que se saiba que a ligação documento–município foi deduzida.

Município com mais de uma tabela residencial (tarifa por bairro, por área, «Tarifa 1»
para quem consome pouco) recebe uma **representativa** na residencial, com o motivo em
`representativa`, e as demais em `variantes`. O banco guarda `tarifa_representativa` e
`variantes`; o programa mostra o intervalo entre elas e deixa o usuário escolher.

`EST` é a tabela na forma do documento:

    {"fixo": 40.42, "franquia": 10,                      # mínimo que dá direito a 10 m³
     "faixas": [[10, 20, 5.69], [20, 50, 8.74], [50, null, 10.46]],
     "esgoto_pct": 80}                                   # ou "esgoto_r_m3": 7.10

Com `"retroativa": {"ate": 15, "valor": 73.69}`, quem consome até 15 m³ paga R$ 73,69, e
acima disso todo o volume, desde 0 m³, segue as faixas (a «Tarifa 1» da CEDAE).
Com `"direta": {"minimo": [6, 14.30], "precos": [[7, 2.47], [8, 2.53], …], "acima": 12.72}`,
todo o volume paga o preço do consumo do mês (cobrança direta, DAE Americana e DAEV
Valinhos; `[a, b, p]` vale para uma faixa inteira); `cascata_da_cobranca_direta` a converte
em faixas progressivas que reproduzem a conta de cada m³ inteiro.
Com `"exponencial": {"pb": 9.44, "expoentes": [[0, 20, 1.0], [20, 21, 1.01], …]}`, a água é
`fixo + PB × Cⁿ`, com `n` da faixa de consumo em que C cai (fórmula da CORSAN e da COMUSA);
`faixas` fica vazia.
Sem `franquia`, o `fixo` é taxa de disponibilidade somada ao consumo desde 0 m³; com
`"piso": X`, a conta nunca fica abaixo de X; sem `fixo`, só há faixas. `null` no fim
da última faixa é o teto aberto.

As transcrições são aplicadas da vigência mais antiga para a mais nova: quando chega o
reajuste de um prestador, a transcrição nova entra ao lado da antiga e vence nos
municípios que cobre. A residencial transcrita substitui a do banco e recebe a
procedência (`fonte_documento`, `fonte_registro`, `fonte_tabela`, `vigencia_saneamento`,
`fonte_url`); as demais categorias entram em `categorias`. O antes e o depois ficam em
`transcricoes/historico.json` (cumulativo) e `transcricoes/ALTERACOES.md`; os itens do
registro passam a «transcrito»; `FILA.md` e a lista de coleta são regerados.

Uso
---
    python tarifas/aplicar_transcricoes.py            # confere, não grava
    python tarifas/aplicar_transcricoes.py --aplicar  # grava banco, histórico, registro e fila
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
for _p in (RAIZ, AQUI):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from triton.core.tariff_regimes import (  # noqa: E402
    DISPONIBILIDADE, EXPONENCIAL, FRANQUIA_NO_MINIMO, FRANQUIA_RETROATIVA, PISO_DE_PAGAMENTO, SEM_MINIMO,
    validar_estrutura,
)
from triton.core.tariffs_structure import (  # noqa: E402
    ESGOTO_PERCENTUAL, ESGOTO_POR_M3, EXPOENTE_DE_CONSUMO, FAIXA_PROGRESSIVA, FRANQUIA_DE_CONSUMO_MINIMO,
    PISO_DE_PAGAMENTO as COD_PISO, PRECO_BASE_EXPONENCIAL,
    TAXA_FIXA_DE_DISPONIBILIDADE, TETO_ABERTO_M3,
)
import procedencia as P  # noqa: E402
import registro_de_fontes as R  # noqa: E402

BANCO = os.path.join(RAIZ, "triton", "data", "brazil_cities_tariffs.json")
PASTA = os.path.join(AQUI, "transcricoes")
ALTERACOES = os.path.join(PASTA, "ALTERACOES.md")
HISTORICO = os.path.join(PASTA, "historico.json")
CATEGORIAS = ("comercial", "publica", "industrial", "social")
#: Grau de confiança da residencial que um documento desmente sem trazer a tabela
#: (o motivo vai em `motivo_dado_ruim`; o manual em inglês traduz o grau).
GRAU_CONTRADITO = "D — contradito por documento"
#: O teto aberto como o banco o grava (o mesmo de manual/tabela_de_faixas.py).
TETO = 999999.0
NL = chr(10)


def _real(v: float) -> str:
    return f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def _m3(v: float) -> str:
    return f"{v:g}".replace(".", ",")


def cascata_da_cobranca_direta(direta: dict) -> dict:
    """Converte a cobrança direta (todo o volume pelo preço do consumo) em faixas progressivas.

    `direta` = {"minimo": [ate, valor], "precos": [[C, p] ou [a, b, p], ...], "acima": p}:
    até `ate` m³ paga-se `valor`; com C m³ (inteiro), a conta é C × p(C); acima do último
    volume listado, C × `acima`. A conta de cada m³ inteiro é reproduzida exatamente por
    faixas de 1 m³ nas mudanças de preço (o degrau vira o preço marginal daquele m³);
    entre dois inteiros, a conta é a reta que os une.
    """
    ate, valor = float(direta["minimo"][0]), float(direta["minimo"][1])
    preco = {}
    for linha in direta["precos"]:
        a, b, p = (linha[0], linha[0], linha[1]) if len(linha) == 2 else linha
        for c in range(int(a), int(b) + 1):
            preco[c] = float(p)
    ultimo = max(preco)
    acima = float(direta["acima"])
    conta = {int(ate): valor}
    for c in range(int(ate) + 1, ultimo + 2):
        conta[c] = c * preco.get(c, acima)
    faixas = []
    for c in range(int(ate) + 1, ultimo + 2):
        marginal = round(conta[c] - conta[c - 1], 4)
        if faixas and abs(faixas[-1][2] - marginal) < 1e-9:
            faixas[-1][1] = float(c)
        else:
            faixas.append([float(c - 1), float(c), marginal])
    if abs(faixas[-1][2] - acima) < 1e-9:
        faixas[-1][1] = None
    else:
        faixas.append([float(ultimo + 1), None, acima])
    return {"fixo": valor, "franquia": ate, "faixas": faixas}


def cascata_da_parcela_fixa_por_faixa(fixos: list, faixas: list) -> dict:
    """Parcela fixa que depende da faixa do consumo total, mais parcela variável em cascata.

    `fixos` = [[ate, valor], ..., [None, valor]] (CESAN, Res. ARSP 107/2026: R$ 25,73 até
    10 m³, R$ 30,62 de 11 a 15 m³…); `faixas` = a parcela variável, em cascata. A conta de
    C m³ (inteiro) é fixo(C) + Σ variável; o degrau da parcela fixa entra como preço do
    primeiro m³ de cada faixa nova, e as faixas resultantes reproduzem a conta de cada m³
    inteiro (entre dois inteiros, a reta que os une, como o hidrômetro fatura).
    """
    limites = [float(a) for a, _ in fixos[:-1]]
    novas = []
    for a, b, p in faixas:
        a, b = float(a), (None if b is None else float(b))
        inicio = a
        for i, lim in enumerate(limites):
            if a <= lim < (b if b is not None else float("inf")) and lim + 1 <= (b if b is not None else float("inf")):
                if lim > inicio:
                    novas.append([inicio, lim, p])
                # O m³ que leva o consumo à faixa seguinte paga também o degrau da parcela fixa.
                novas.append([lim, lim + 1.0, round(p + float(fixos[i + 1][1]) - float(fixos[i][1]), 4)])
                inicio = lim + 1.0
        if b is None or b > inicio:
            novas.append([inicio, b, p])
    return {"fixo": float(fixos[0][1]), "faixas": novas}


def montar(est: dict) -> dict:
    """A tabela do documento na codificação do banco (faixas, regime, esgoto, descrição)."""
    if est.get("direta"):
        est = {**est, **cascata_da_cobranca_direta(est["direta"])}
    if est.get("fixo_por_faixa"):
        est = {**est, "faixas_documento": est["faixas"],
               **cascata_da_parcela_fixa_por_faixa(est["fixo_por_faixa"], est["faixas"])}
    fixo = float(est.get("fixo") or 0.0)
    franquia = float(est.get("franquia") or 0.0)
    piso = float(est.get("piso") or 0.0)
    faixas, partes = [], []
    expo = est.get("exponencial")
    retro = est.get("retroativa")
    if retro:
        faixas.append([0.0, float(retro["ate"]), float(retro["valor"]), FRANQUIA_DE_CONSUMO_MINIMO])
        partes.append(f"até {_m3(retro['ate'])} m³: R$ {_real(retro['valor'])}/mês; acima, todo o volume pelas faixas")
    if fixo:
        faixas.append([0.0, 0.0, fixo, TAXA_FIXA_DE_DISPONIBILIDADE])
    if piso:
        faixas.append([0.0, 0.0, piso, COD_PISO])
    if franquia:
        faixas.append([0.0, franquia, 0.0, FAIXA_PROGRESSIVA])
        partes.append(f"0–{_m3(franquia)} m³: R$ {_real(fixo)}/mês")
        regime = FRANQUIA_NO_MINIMO
    elif piso:
        regime = PISO_DE_PAGAMENTO
        partes.append(f"conta mínima R$ {_real(piso)}/mês")
    elif fixo:
        regime = DISPONIBILIDADE
        partes.append(f"fixo R$ {_real(fixo)}/mês")
    elif retro:
        regime = FRANQUIA_RETROATIVA
    else:
        regime = SEM_MINIMO
    if expo:
        # A fórmula exponencial prevalece sobre o regime do fixo (serviço básico).
        regime = EXPONENCIAL
        faixas.append([0.0, TETO, float(expo["pb"]), PRECO_BASE_EXPONENCIAL])
        for a, b, n in expo["expoentes"]:
            faixas.append([float(a), TETO if b is None else float(b), float(n), EXPOENTE_DE_CONSUMO])
        partes.append(f"PB R$ {_real(expo['pb'])} × Cⁿ, n de {_m3(expo['expoentes'][0][2])} a "
                      f"{_m3(max(e[2] for e in expo['expoentes']))}")
    for a, b, preco in est["faixas"]:
        b = TETO if b is None else float(b)
        faixas.append([float(a), b, float(preco), FAIXA_PROGRESSIVA])
        faixa = f"> {_m3(a)} m³" if b >= TETO_ABERTO_M3 else f"{_m3(a)}–{_m3(b)} m³"
        partes.append(f"{faixa}: R$ {_real(preco)}/m³")
    if est.get("direta"):
        # Centenas de faixas de 1 m³: a descrição diz a regra, não cada degrau.
        d = est["direta"]
        partes = [f"0–{_m3(d['minimo'][0])} m³: R$ {_real(d['minimo'][1])}/mês",
                  f"acima, todo o volume pelo preço do consumo (cobrança direta, R$ "
                  f"{_real(d['precos'][0][-1])} a {_real(d['acima'])}/m³), em {len(est['faixas'])} faixas equivalentes"]
    reg = {
        "faixas": faixas,
        "faixas_desc": "; ".join(partes),
        "tarifa_fixa_mensal": fixo or piso,
        "regime_tarifario": regime,
        "consumo_minimo_faturado_m3": franquia or (float(retro["ate"]) if retro else 0.0),
    }
    if "esgoto_r_m3" in est:
        reg.update(esgoto_modo=ESGOTO_POR_M3, esgoto_r_m3=float(est["esgoto_r_m3"]), esgoto_pct=0.0)
        reg["faixas_desc"] += f"; esgoto R$ {_real(est['esgoto_r_m3'])}/m³"
    else:
        reg.update(esgoto_modo=ESGOTO_PERCENTUAL, esgoto_pct=float(est.get("esgoto_pct", 0.0)))
        reg["faixas_desc"] += f"; esgoto {_m3(reg['esgoto_pct'])}% da água"
    if est.get("nota"):
        reg["nota_transcricao"] = est["nota"]
    if est.get("direta") or est.get("fixo_por_faixa"):
        # As faixas são equivalentes, não as do documento: o manual mostra a regra, não os degraus.
        reg["forma_de_cobranca"] = "direta" if est.get("direta") else "fixo_por_faixa"
        reg["cobranca_documento"] = ({"direta": est["direta"]} if est.get("direta") else
                                     {"fixo_por_faixa": est["fixo_por_faixa"], "faixas": est["faixas_documento"]})
    return reg


def carregar_transcricoes() -> list:
    """Todas as transcrições, da vigência mais antiga para a mais nova: a mais nova vence."""
    lista = []
    for caminho in sorted(glob.glob(os.path.join(PASTA, "*.json"))):
        if os.path.basename(caminho) in ("historico.json", "cobertura.json", "imagens_conferidas.json"):
            continue
        with open(caminho, encoding="utf-8") as f:
            t = json.load(f)
        t["_arquivo"] = os.path.relpath(caminho, RAIZ).replace(os.sep, "/")
        lista.append(t)
    return sorted(lista, key=lambda t: (P.data_da_vigencia(t["vigencia"]) or date.min, t["_arquivo"]))


def _resumo(d: dict) -> str:
    esg = (f"esgoto R$ {_real(d.get('esgoto_r_m3') or 0)}/m³" if d.get("esgoto_modo") == ESGOTO_POR_M3
           else f"esgoto {_m3(float(d.get('esgoto_pct') or 0))}%")
    return f"{(d.get('faixas_desc') or '').split('; esgoto')[0]}; {esg}"


def _iguais(a: dict, b: dict) -> bool:
    def norm(d):
        return (json.dumps([[round(float(x), 4) for x in f] for f in d["faixas"]]),
                int(d.get("esgoto_modo") or 1), round(float(d.get("esgoto_pct") or 0), 2),
                round(float(d.get("esgoto_r_m3") or 0), 2))
    return norm(a) == norm(b)


def _categoria(dados: dict, chave: str, cat: str, est: dict, proc: dict) -> dict:
    novo = montar(est)
    erros = [a for a in validar_estrutura(dict(dados, **novo)) if a.gravidade == "erro"]
    if erros:
        raise ValueError(f"{chave} {cat}: {[str(e) for e in erros]}")
    return novo


def _base_ja_confere(dados: dict, espera) -> bool:
    """A residencial da base reproduz as contas que o documento imprime (`espera`)?

    Uma tabela `"situacao": "ruim"` registra que o documento desmente a base *de então*.
    Com `espera` (lista de {"consumo_m3", "conta_agua"[, "esgoto_pct"]}), a marca só entra
    se a base ainda divergir; quando a resolução do prestador já foi transcrita e bate,
    o quadro mais novo não a derruba de volta a dado ruim.
    """
    if not espera:
        return False
    from triton.core.economic import calculate_water_bill
    faixas = [tuple(f) for f in dados.get("faixas") or []]
    for e in espera:
        conta = calculate_water_bill(float(e["consumo_m3"]) * 1000.0, faixas, 1, 0.0)
        if abs(conta - float(e["conta_agua"])) > 0.01:
            return False
        if "esgoto_pct" in e and abs(float(dados.get("esgoto_pct") or 0.0) - float(e["esgoto_pct"])) > 0.5:
            return False
    return True


def _resumo_espera(espera) -> str:
    return "; ".join(f"{_m3(e['consumo_m3'])} m³ = R$ {_real(e['conta_agua'])}" for e in espera)


def aplicar(banco: dict, transcricoes: list) -> list:
    """Aplica tudo e devolve o diário, um dicionário por município e transcrição."""
    cidades = banco["cities"]
    diario = []
    for t in transcricoes:
        for tab in t["tabelas"]:
            for nome in tab["municipios"]:
                chave = f"{tab['uf']} - {nome}"
                if chave not in cidades:
                    raise KeyError(f"{t['_arquivo']}: «{chave}» não está no catálogo")
                dados = cidades[chave]
                proc = {
                    "fonte_documento": t["documento"],
                    "fonte_registro": t["registro"],
                    "fonte_tabela": tab["rotulo"],
                    "fonte_transcricao": t["_arquivo"],
                    "vigencia_saneamento": tab.get("vigencia") or t["vigencia"],
                    "fonte_url": t["fonte_url"],
                }
                if tab.get("abrangencia"):
                    proc["fonte_abrangencia"] = tab["abrangencia"]
                antes = {k: dados.get(k) for k in ("faixas", "faixas_desc", "esgoto_modo", "esgoto_pct",
                                                   "esgoto_r_m3", "prestador_saneamento")}
                entrada = {"municipio": chave, "transcricao": t["_arquivo"], "documento": t["documento"],
                           "tabela": tab["rotulo"], "vigencia": proc["vigencia_saneamento"],
                           "prestador_antes": antes["prestador_saneamento"],
                           "prestador_depois": tab.get("prestador") or antes["prestador_saneamento"],
                           "antes": _resumo(antes), "depois": _resumo(antes), "mudou": False}
                if tab.get("prestador"):
                    dados["prestador_saneamento"] = tab["prestador"]
                if tab.get("situacao") == "ruim" and _base_ja_confere(dados, tab.get("espera")):
                    # O documento desmentia a base de então; outra transcrição já a corrigiu.
                    entrada["depois"] = "base confere com o documento: " + _resumo_espera(tab["espera"])
                elif tab.get("situacao") == "ruim":
                    # O documento desmente a residencial da base, mas não traz a tabela inteira.
                    dados["confianca_grau"] = GRAU_CONTRADITO
                    dados["motivo_dado_ruim"] = tab["motivo"]
                    dados["status_desc_sanitation"] = f"{tab['motivo']} ({t['documento']}, {tab['rotulo']})."
                    entrada["depois"] = "residencial marcada como dado ruim: " + tab["motivo"]
                    entrada["mudou"] = True
                if "residencial" in tab:
                    novo = _categoria(dados, chave, "residencial", tab["residencial"], proc)
                    entrada["mudou"] = not _iguais(antes, novo)
                    entrada["depois"] = _resumo(novo)
                    dados.pop("esgoto_r_m3", None)
                    dados.pop("forma_de_cobranca", None)
                    dados.pop("cobranca_documento", None)
                    dados.update(novo)
                    dados.update(proc)
                    dados["update_status_sanitation"] = "VERIFIED_DOCUMENT"
                    dados["status_desc_sanitation"] = (
                        f"Transcrita de {t['documento']} ({tab['rotulo']}), guardado em tarifas/fontes/.")
                    if str(dados.get("confianca_grau", "")).startswith("D"):
                        dados["confianca_grau"] = "A — alta"  # a tabela documentada substitui o dado ruim
                    dados.pop("motivo_dado_ruim", None)
                    if not tab.get("abrangencia"):
                        dados.pop("fonte_abrangencia", None)
                    # Representativa e alternativas: vêm juntas com a residencial, ou saem.
                    dados.pop("tarifa_representativa", None)
                    dados.pop("variantes", None)
                    if tab.get("representativa"):
                        dados["tarifa_representativa"] = tab["representativa"]
                    if tab.get("variantes"):
                        dados["variantes"] = [dict(_categoria(dados, chave, f"variante {r}", est, proc), rotulo=r, **proc)
                                              for r, est in tab["variantes"].items()]
                elif tab.get("residencial_conferida"):
                    # Forma que EST não descreve (fórmula exponencial da CORSAN): o valor da base
                    # já foi gravado deste documento por script próprio; aqui só entra a procedência.
                    dados.update(proc)
                    dados["update_status_sanitation"] = "VERIFIED_DOCUMENT"
                entrada["mudou_prestador"] = entrada["prestador_antes"] != entrada["prestador_depois"]
                diario.append(entrada)
                categorias = dict(dados.get("categorias") or {})
                for cat in CATEGORIAS:
                    if cat in tab:
                        categorias[cat] = dict(_categoria(dados, chave, cat, tab[cat], proc), **proc)
                if categorias:
                    dados["categorias"] = categorias
    return diario


def acumular(diario: list) -> list:
    """Junta o diário ao histórico. A primeira aplicação de cada transcrição guarda o «antes»;
    as seguintes já encontram o valor novo no banco e não o apagam."""
    historico = []
    if os.path.exists(HISTORICO):
        with open(HISTORICO, encoding="utf-8") as f:
            historico = json.load(f)
    chaves = {(h["municipio"], h["transcricao"], h["vigencia"]) for h in historico}
    hoje = date.today().isoformat()
    for e in diario:
        if (e["municipio"], e["transcricao"], e["vigencia"]) not in chaves:
            historico.append(dict(e, aplicado_em=hoje))
    with open(HISTORICO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(historico, f, ensure_ascii=False, indent=1)
        f.write(NL)
    return historico


def relatorio(historico: list) -> str:
    L = ["# Alterações pelas transcrições", "",
         "Gerado por `tarifas/aplicar_transcricoes.py` a partir de `historico.json`. Não edite à mão.", "",
         "Cada linha é um município conferido contra um documento oficial guardado em "
         "`tarifas/fontes/`. «Confirmada»: a base já tinha os valores do documento. «Corrigida»: "
         "o antes e o depois, na data em que a transcrição foi aplicada.", ""]
    corr = [h for h in historico if h["mudou"] or h["mudou_prestador"]]
    L += [f"Conferências: {len(historico)} · corrigidas: {len(corr)} · "
          f"confirmadas: {len(historico) - len(corr)}", ""]
    if corr:
        L += ["## Corrigidas", "", "| Aplicada | Município | Documento (tabela) | Antes | Depois |",
              "| :--- | :--- | :--- | :--- | :--- |"]
        for h in sorted(corr, key=lambda h: (h["aplicado_em"], h["municipio"])):
            a, b = h["antes"], h["depois"]
            if h["mudou_prestador"]:
                a = f"prestador «{h['prestador_antes']}»; {a}"
                b = f"prestador «{h['prestador_depois']}»; {b}"
            L.append(f"| {h['aplicado_em']} | {h['municipio']} | {h['documento']} ({h['tabela']}) | {a} | {b} |")
        L.append("")
    L += ["## Confirmadas", "", "| Aplicada | Município | Documento (tabela) |", "| :--- | :--- | :--- |"]
    for h in sorted(historico, key=lambda h: (h["aplicado_em"], h["municipio"])):
        if h not in corr:
            L.append(f"| {h['aplicado_em']} | {h['municipio']} | {h['documento']} ({h['tabela']}) |")
    return NL.join(L) + NL


def marcar_registro(transcricoes: list) -> None:
    reg = R.carregar()
    for t in transcricoes:
        n = sum(len(tab["municipios"]) for tab in t["tabelas"])
        cats = sorted({c for tab in t["tabelas"] for c in ("residencial",) + CATEGORIAS if c in tab},
                      key=lambda c: (("residencial",) + CATEGORIAS).index(c))
        # Também é uso a conferência de uma forma que EST não descreve (fórmula exponencial),
        # a marcação de dado ruim e a correção do prestador: o documento entrou no banco.
        outros = [r for tab in t["tabelas"] for r, sim in (("conferência", tab.get("residencial_conferida")),
                                                            ("dado ruim", tab.get("situacao") == "ruim"),
                                                            ("prestador", tab.get("prestador"))) if sim]
        usos = cats + [o for o in dict.fromkeys(outros) if o not in cats]
        for item in reg["itens"]:
            if item["id"] in t["registro"]:
                item["situacao"] = "transcrito" if usos else "consultado"
                item["uso"] = (f"{t['_arquivo']}; {', '.join(usos)}; {n} município(s)" if usos
                               else f"consultado: {t['_arquivo']} não traz tabela aplicável")
    R.gravar(reg)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--aplicar", action="store_true")
    a = ap.parse_args()
    with open(BANCO, encoding="utf-8") as f:
        banco = json.load(f)
    transcricoes = carregar_transcricoes()
    diario = aplicar(banco, transcricoes)
    mudou = sum(1 for d in diario if d["mudou"] or d["mudou_prestador"])
    print(f"{len(transcricoes)} transcrições, {len(diario)} municípios conferidos, "
          f"{mudou} com valores ou prestador alterados")
    if not a.aplicar:
        print("Conferência apenas. Use --aplicar para gravar.")
        return 0
    banco["last_update"] = date.today().isoformat()
    with open(BANCO, "w", encoding="utf-8", newline="\n") as f:
        json.dump(banco, f, ensure_ascii=False, indent=2)
        f.write(NL)
    with open(ALTERACOES, "w", encoding="utf-8", newline="") as f:
        f.write(relatorio(acumular(diario)))
    marcar_registro(transcricoes)   # regera REGISTRO.md e a lista de coleta
    P.gerar_fila()
    print("gravado: banco, transcricoes/ALTERACOES.md e historico.json, registro de fontes, FILA.md, lista de coleta")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
