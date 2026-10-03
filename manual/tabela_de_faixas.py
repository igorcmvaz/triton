# -*- coding: utf-8 -*-
"""A tabela de faixas por município e categoria, para o apêndice de regimes tarifários.

As colunas são os intervalos de consumo na maior discretização que o catálogo pede: a
união dos limites de faixa de todos os prestadores. Se nenhum prestador separa 0 a 5 m³,
a coluna é «0–5»; se algum muda o preço em 6 m³, nasce a coluna «5–6». A grade se
refaz sozinha a cada montagem, de modo que uma tabela nova coletada entra no apêndice
sem que ninguém mexa aqui.

Municípios com a mesma tabela, o mesmo esgoto e a mesma parcela fixa formam uma linha
só, porque as companhias estaduais aplicam uma tabela a dezenas deles. As categorias não
residenciais entram onde foram coletadas (campo ``categorias`` do registro). A fórmula
exponencial da CORSAN não tem preço por faixa e sai numa tabela própria.

O módulo serve aos dois manuais: o texto e o formato de número vêm de quem chama.
"""

from __future__ import annotations

import json
import os
from typing import Callable, Dict, List, Tuple

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BANCO = os.path.join(BASE, "netuno", "data", "brazil_cities_tariffs.json")
TETO = 999999.0
NL = chr(10)
COLUNAS_POR_BLOCO = 10

CATEGORIAS = ("residencial", "comercial", "publica", "industrial", "social")


#: A situação de cada estrutura, pela cor da linha: o PDF pinta o fundo pelo marcador
#: que abre a célula do número, e o Markdown mostra o próprio marcador.
MARCADOR = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}
REGISTRO_DE_FONTES = os.path.join(BASE, "data", "tarifas", "change_tracking_registry.json")


def situacao(dados: dict) -> str:
    """Verde: auditada contra a fonte primária. Amarela: falta confirmar. Vermelha: dado ruim."""
    if dados.get("fonte_documento"):
        return "verde"  # categoria transcrita de uma tabela oficial guardada no repositório
    grau = str(dados.get("confianca_grau") or "")
    if grau.startswith("D"):
        return "vermelho"
    if (grau.startswith("C") or dados.get("status_global") == "MANUAL_REVIEW_NEEDED"
            or dados.get("update_status_sanitation") != "VERIFIED_AUDIT"):
        return "amarelo"
    return "verde"


def _verificacoes() -> Dict[str, str]:
    """{url da fonte: data da última verificação}, do registro de monitoramento."""
    try:
        with open(REGISTRO_DE_FONTES, encoding="utf-8") as f:
            urls = json.load(f).get("monitored_urls", {})
    except (OSError, ValueError):
        return {}
    return {u: str(d.get("last_checked") or "")[:10] for u, d in urls.items()}


def carregar() -> Dict[str, dict]:
    with open(BANCO, encoding="utf-8") as f:
        return json.load(f)["cities"]


def _estruturas(cidades: Dict[str, dict]):
    """(município, dados da categoria, categoria) para toda estrutura do catálogo."""
    for chave, dados in cidades.items():
        yield chave, dados, "residencial"
        for cat, extra in (dados.get("categorias") or {}).items():
            yield chave, dict(dados, **extra), cat


def _exponencial(dados: dict) -> bool:
    return dados.get("regime_tarifario") == "exponencial"


def grade(cidades: Dict[str, dict]) -> List[Tuple[float, float]]:
    """Os intervalos de consumo: a união dos limites de todas as faixas progressivas."""
    limites = {0.0}
    for _, dados, _cat in _estruturas(cidades):
        if _exponencial(dados):
            continue
        for a, b, _v, cod in dados["faixas"]:
            if int(cod) in (0, 1):
                limites.update(x for x in (float(a), float(b)) if x < TETO)
    pontos = sorted(limites)
    return list(zip(pontos, pontos[1:] + [TETO]))


def _preco(faixas, a: float, b: float):
    meio = a + 0.5 if b >= TETO else (a + b) / 2.0
    for x, y, v, cod in faixas:
        if int(cod) in (0, 1) and float(x) < meio <= float(y):
            return float(v)
    return None


def linhas(cidades: Dict[str, dict]):
    """Agrupa as estruturas iguais. Devolve [(prestador, categoria, municípios, dados)]."""
    grupos: Dict[str, list] = {}
    for chave, dados, cat in _estruturas(cidades):
        if _exponencial(dados):
            continue
        assinatura = json.dumps([dados.get("prestador_saneamento"), cat, dados["faixas"],
                                 dados.get("esgoto_modo"), dados.get("esgoto_pct"),
                                 dados.get("esgoto_r_m3"), situacao(dados),
                                 dados.get("vigencia_saneamento"), dados.get("fonte_url")],
                                sort_keys=True)
        grupos.setdefault(assinatura, [dados.get("prestador_saneamento") or "—", cat, [], dados])
        grupos[assinatura][2].append(f"{dados.get('municipio')} ({dados.get('uf')})")
    ordem = {c: i for i, c in enumerate(CATEGORIAS)}
    return sorted(grupos.values(), key=lambda g: (g[0].lower(), ordem.get(g[1], 9), g[2][0]))


def _municipios(lista: List[str], e_mais: str = "") -> str:
    """Todos os municípios, por extenso: cada um dos 652 tem de ser achado na tabela."""
    return ", ".join(sorted(lista))


def cobertura(cidades: Dict[str, dict]) -> Dict[str, Dict[str, int]]:
    """{categoria: {situação: municípios}}, com «nao_coletada» para a categoria ausente."""
    conta = {c: {"verde": 0, "amarelo": 0, "vermelho": 0, "nao_coletada": 0} for c in CATEGORIAS}
    for dados in cidades.values():
        extra = dados.get("categorias") or {}
        for cat in CATEGORIAS:
            if cat == "residencial":
                conta[cat][situacao(dados)] += 1
            elif cat in extra:
                conta[cat][situacao(dict(dados, **extra[cat]))] += 1
            else:
                conta[cat]["nao_coletada"] += 1
    return conta


def nao_coletadas(cidades: Dict[str, dict]):
    """[(prestador, categoria, municípios)] das categorias sem tabela, por prestador."""
    grupos: Dict[Tuple[str, str], List[str]] = {}
    for dados in cidades.values():
        extra = dados.get("categorias") or {}
        for cat in CATEGORIAS[1:]:
            if cat not in extra:
                chave = (dados.get("prestador_saneamento") or "—", cat)
                grupos.setdefault(chave, []).append(f"{dados.get('municipio')} ({dados.get('uf')})")
    ordem = {c: i for i, c in enumerate(CATEGORIAS)}
    return sorted(((p, c, m) for (p, c), m in grupos.items()),
                  key=lambda g: (g[0].lower(), ordem[g[1]]))


def secao(cidades: Dict[str, dict], T: Dict[str, str], num: Callable[[float, int], str]) -> List[str]:
    """As linhas Markdown da seção. `T` traz os textos; `num(valor, casas)` o número."""
    intervalos = grade(cidades)
    grupos = linhas(cidades)

    def rotulo(a, b):
        return f"> {num(a, 0)}" if b >= TETO else f"{num(a, 0)}–{num(b, 0)}"

    def fixo(dados):
        partes = []
        for a, b, v, cod in dados["faixas"]:
            if int(cod) == -1:
                partes.append(num(v, 2))
            elif int(cod) == -2:
                partes.append(T["retroativa"].format(num(b, 0), num(v, 2)))
            elif int(cod) == -3:
                partes.append(T["piso"].format(num(v, 2)))
        return "; ".join(partes) or "—"

    def esgoto(dados):
        if dados.get("esgoto_modo") == 2:
            return T["esgoto_m3"].format(num(float(dados.get("esgoto_r_m3") or 0), 2))
        return f"{num(float(dados.get('esgoto_pct') or 0), 0)}%"

    L = ["", T["titulo"], ""] + T["texto"] + [""]
    conta = cobertura(cidades)
    total = len(cidades)
    L += [T["cob_texto"].format(total, total * len(CATEGORIAS)), "",
          f"<!-- tabela: {T['cob_legenda']} -->",
          "| " + " | ".join(T["cob_cab"]) + " |",
          "| :--- | ---: | ---: | ---: | ---: | ---: |"]
    for cat in CATEGORIAS:
        n = conta[cat]
        L.append(f"| {T['cat_' + cat]} | {n['verde']} | {n['amarelo']} | {n['vermelho']} | "
                 f"{n['nao_coletada']} | {sum(n.values())} |")
    L.append("")
    L += [f"<!-- tabela: {T['legenda_id']} -->",
          "| " + " | ".join([T["n"], T["prestador"], T["categoria"], T["fixo"], T["esgoto"]]) + " |",
          "| ---: | :--- | :--- | :--- | :--- |"]
    for i, (prestador, cat, municipios, dados) in enumerate(grupos, 1):
        L.append(f"| {MARCADOR[situacao(dados)]} {i} | {prestador}: {_municipios(municipios, T['e_mais'])} | "
                 f"{T['cat_' + cat]} | {fixo(dados)} | {esgoto(dados)} |")
    L.append("")
    blocos = [intervalos[i:i + COLUNAS_POR_BLOCO] for i in range(0, len(intervalos), COLUNAS_POR_BLOCO)]
    for k, bloco in enumerate(blocos, 1):
        legenda = T["legenda"].format(k, len(blocos), rotulo(*bloco[0]).replace("> ", ""),
                                      rotulo(*bloco[-1]).replace("> ", ""))
        cab = [T["n"]] + [rotulo(a, b) for a, b in bloco]
        L += [f"<!-- tabela: {legenda} -->",
              "| " + " | ".join(cab) + " |",
              "| " + " | ".join(["---:"] * len(cab)) + " |"]
        for i, (_p, _c, _m, dados) in enumerate(grupos, 1):
            celulas = [f"{MARCADOR[situacao(dados)]} {i}"]
            for a, b in bloco:
                p = _preco(dados["faixas"], a, b)
                celulas.append("—" if p is None else num(p, 2))
            L.append("| " + " | ".join(celulas) + " |")
        L.append("")

    faltam: Dict[Tuple[str, str], List[str]] = {}
    for prestador, cat, municipios in nao_coletadas(cidades):
        faltam.setdefault((prestador, _municipios(municipios)), []).append(T["cat_" + cat])
    if faltam:
        L += [T["falta_texto"], "", f"<!-- tabela: {T['falta_legenda']} -->",
              "| " + " | ".join(T["falta_cab"]) + " |", "| :--- | :--- |"]
        for (prestador, municipios), cats in sorted(faltam.items(), key=lambda kv: kv[0][0].lower()):
            L.append(f"| {MARCADOR['vermelho']} {prestador}: {municipios} | {', '.join(cats)} |")
        L.append("")

    verificadas = _verificacoes()
    L += [T["data_texto"], "", f"<!-- tabela: {T['data_legenda']} -->",
          "| " + " | ".join(T["data_cab"]) + " |", "| ---: | :--- | :--- | :--- |"]
    for i, (_p, _c, _m, dados) in enumerate(grupos, 1):
        cor = situacao(dados)
        vigencia = str(dados.get("vigencia_saneamento") or "—").replace("|", "/")
        quando = verificadas.get(dados.get("fonte_url") or "", "") or "—"
        if T.get("data_dia_mes_ano") and len(quando) == 10:
            quando = "/".join(reversed(quando.split("-")))
        L.append(f"| {MARCADOR[cor]} {i} | {vigencia} | {quando} | {T['situacao_' + cor]} |")
    L.append("")

    # A fórmula exponencial, à parte.
    exp: Dict[str, list] = {}
    for chave, dados, cat in _estruturas(cidades):
        if not _exponencial(dados):
            continue
        pb = next(float(v) for a, b, v, cod in dados["faixas"] if int(cod) == 2)
        sb = sum(float(v) for a, b, v, cod in dados["faixas"] if int(cod) == -1)
        assin = json.dumps([cat, pb, sb, dados.get("esgoto_r_m3")])
        exp.setdefault(assin, [cat, pb, sb, dados.get("esgoto_r_m3"), [], dados])
        exp[assin][4].append(f"{dados.get('municipio')} ({dados.get('uf')})")
    if exp:
        L += [T["exp_texto"], "", f"<!-- tabela: {T['exp_legenda']} -->",
              "| " + " | ".join(T["exp_cab"]) + " |", "| :--- | :--- | ---: | ---: | ---: |"]
        ordem = {c: i for i, c in enumerate(CATEGORIAS)}
        for cat, pb, sb, esg, municipios, _d in sorted(exp.values(), key=lambda e: (e[1], ordem.get(e[0], 9))):
            L.append(f"| {_municipios(municipios, T['e_mais'])} | {T['cat_' + cat]} | "
                     f"{num(pb, 2)} | {num(sb, 2)} | {num(float(esg or 0), 2)} |")
        L.append("")
    return L
