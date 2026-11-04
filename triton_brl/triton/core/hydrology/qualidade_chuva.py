# -*- coding: utf-8 -*-
"""Nível de qualidade (A, B ou C) da chuva por concelho da edição IBE.

Uma só fórmula, num só lugar (a da E-OBS; a da base ibérica, por geometria, está em
``scripts/dados/unidades_iberia.py`` e nos metadados de ``ibe_unidades.db``). O banco (``data/qualidade_eobs_odbl.db``, tabela ``qualidade``), a
interface, o laudo e o manual leem os limiares deste módulo; nenhum outro arquivo repete
«10 %», «15 %», «20 %» ou «25 %».

A medida. ``dtot`` e ``drx`` são diferenças percentuais entre a E-OBS e o Iberia01 (rede densa de
estações da Península), nas mesmas células do concelho, em 1971–2000: ``dtot`` é a diferença do
total anual; ``drx``, a do máximo diário anual. Negativo quer dizer que a E-OBS dá menos chuva que
o Iberia01. É a diferença entre dois produtos de grelha, e não um viés contra a verdade: o Iberia01
também tem erro. Por isso o programa diz «diferença para o Iberia01», nunca «viés».

A fórmula::

    concordância = A se |dtot| <= 10 e |drx| <= 15
                   B se |dtot| <= 20 e |drx| <= 25
                   C nos demais casos
    geometria    = B se n_eff < 3, ou método «centroide», ou série repetida de outro concelho
                   A nos demais casos
    nível        = o pior das duas

A geometria só rebaixa até B: é um risco a priori (uma célula não amostra a variação dentro do
concelho), não uma discrepância medida. O C fica reservado à discrepância medida. Os limiares são
convenção (decisão do debate de 23/10/2026), e não resultado de um ajuste.
"""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, Dict, List, Optional

#: Os limiares, em pontos percentuais, do módulo da diferença. Único lugar onde existem.
LIMIARES: Dict[str, Dict[str, float]] = {
    "A": {"dtot": 10.0, "drx": 15.0},
    "B": {"dtot": 20.0, "drx": 25.0},
}
#: Do melhor para o pior.
NIVEIS = ("A", "B", "C")
#: Menos células efetivas que isto rebaixa a geometria para B.
N_MINIMO_DE_CELULAS = 3
#: Versão do critério; vai para ``metadados.qualidade_versao`` e muda se a fórmula mudar.
VERSAO_DA_QUALIDADE = "1"
REFERENCIA = "Iberia01 v1.0 (DIGITAL.CSIC), 1971–2000"

_ORDEM = {n: i for i, n in enumerate(NIVEIS)}


def _pior(a: str, b: str) -> str:
    return a if _ORDEM[a] >= _ORDEM[b] else b


def nivel_de_concordancia(dtot: float, drx: float) -> str:
    """A, B ou C pelos limiares: só a discrepância medida com o Iberia01."""
    e_tot, e_ext = abs(float(dtot)), abs(float(drx))
    for nivel in ("A", "B"):
        lim = LIMIARES[nivel]
        if e_tot <= lim["dtot"] and e_ext <= lim["drx"]:
            return nivel
    return "C"


def nivel_de_geometria(n_eff: int, metodo: str, repetida: bool) -> str:
    """A ou B (nunca C): o risco a priori de a série não representar o concelho."""
    if int(n_eff) < N_MINIMO_DE_CELULAS or str(metodo) == "centroide" or bool(repetida):
        return "B"
    return "A"


def nivel(dtot: float, drx: float, n_eff: int, metodo: str, repetida: bool = False) -> str:
    """O nível do concelho: o pior da concordância e da geometria."""
    return _pior(nivel_de_concordancia(dtot, drx), nivel_de_geometria(n_eff, metodo, repetida))


def _pct(x: float) -> str:
    """«-15,2 %» (vírgula decimal, espaço antes do %), como no português de Portugal."""
    return f"{float(x):.1f}".replace(".", ",") + " %"


def _lim(n: str, chave: str) -> str:
    return f"{LIMIARES[n][chave]:g}".replace(".", ",") + " %"


def motivos_da_geometria(n_eff: int, metodo: str, repetida: bool) -> List[str]:
    out = []
    if int(n_eff) < N_MINIMO_DE_CELULAS:
        out.append("uma só célula de 10 km" if int(n_eff) == 1 else f"apenas {int(n_eff)} células de 10 km")
    if str(metodo) == "centroide":
        out.append("célula escolhida pelo centroide (nenhum centro de célula dentro do concelho)")
    if bool(repetida):
        out.append("série igual à de outro concelho")
    return out


def motivo(dtot: float, drx: float, n_eff: int, metodo: str, repetida: bool = False) -> str:
    """O motivo do nível, em português de Portugal, para o ecrã, o laudo e o banco."""
    niv = nivel(dtot, drx, n_eff, metodo, repetida)
    conc = nivel_de_concordancia(dtot, drx)
    geo = motivos_da_geometria(n_eff, metodo, repetida)
    medida = (f"diferença para o Iberia01: total {_pct(dtot)}, extremos {_pct(drx)} "
              f"(1971–2000, E-OBS menos Iberia01)")
    if niv == "A":
        return (f"A: {int(n_eff)} células de 10 km; {medida}, dentro dos limites do nível A "
                f"({_lim('A', 'dtot')} e {_lim('A', 'drx')}).")
    partes = []
    if conc != "A":
        if conc == "B":
            partes.append(f"{medida}, acima dos limites do nível A ({_lim('A', 'dtot')} e {_lim('A', 'drx')}) "
                          f"e dentro dos do B ({_lim('B', 'dtot')} e {_lim('B', 'drx')})")
        else:
            partes.append(f"{medida}, acima dos limites do nível B ({_lim('B', 'dtot')} e {_lim('B', 'drx')})")
    if geo:
        partes.append("geometria frágil: " + "; ".join(geo))
        if conc == "A":
            partes.append(f"a diferença para o Iberia01 cabe no nível A (total {_pct(dtot)}, extremos {_pct(drx)})")
    return f"{niv}: " + "; ".join(partes) + "."


def descricao_dos_niveis(lingua: str = "pt") -> List[str]:
    """Uma linha por nível, gerada de ``LIMIARES``; é o texto do ecrã, do laudo e do manual."""
    a, b = LIMIARES["A"], LIMIARES["B"]
    f = lambda x: f"{x:g}"  # noqa: E731
    if lingua == "en":
        return [
            f"A: {N_MINIMO_DE_CELULAS} or more grid cells and a difference from Iberia01 of up to {f(a['dtot'])} % in the total "
            f"and {f(a['drx'])} % in the annual maximum daily rainfall.",
            f"B: difference from Iberia01 of up to {f(b['dtot'])} % (total) and {f(b['drx'])} % (extremes); also given to a series with "
            f"fewer than {N_MINIMO_DE_CELULAS} cells, chosen by centroid, or identical to that of another municipality.",
            f"C: difference from Iberia01 above {f(b['dtot'])} % (total) or {f(b['drx'])} % (extremes). Validate with a local series.",
        ]
    if lingua == "es":
        return [
            f"A: {N_MINIMO_DE_CELULAS} o más celdas de la malla y una diferencia con Iberia01 de hasta {f(a['dtot'])} % en el total "
            f"y de hasta {f(a['drx'])} % en la precipitación máxima diaria anual.",
            f"B: diferencia con Iberia01 de hasta {f(b['dtot'])} % (total) y {f(b['drx'])} % (extremos); también reciben B las series con "
            f"menos de {N_MINIMO_DE_CELULAS} celdas, elegidas por el centroide o idénticas a las de otro municipio.",
            f"C: diferencia con Iberia01 superior a {f(b['dtot'])} % (total) o {f(b['drx'])} % (extremos). Valide con una serie local.",
        ]
    if lingua == "zh":
        return [
            f"A：网格单元不少于 {N_MINIMO_DE_CELULAS} 个，且与 Iberia01 的差异在总量上不超过 {f(a['dtot'])} %、"
            f"在年最大日降水量上不超过 {f(a['drx'])} %。",
            f"B：与 Iberia01 的差异在总量上不超过 {f(b['dtot'])} %、在极值上不超过 {f(b['drx'])} %；"
            f"单元少于 {N_MINIMO_DE_CELULAS} 个、按质心选取或与其他市镇序列相同的序列也记为 B。",
            f"C：与 Iberia01 的差异在总量上超过 {f(b['dtot'])} % 或在极值上超过 {f(b['drx'])} %。请用本地序列验证。",
        ]
    return [
        f"A: {N_MINIMO_DE_CELULAS} ou mais células da grelha e diferença para o Iberia01 até {f(a['dtot'])} % no total "
        f"e até {f(a['drx'])} % no máximo diário anual.",
        f"B: diferença para o Iberia01 até {f(b['dtot'])} % no total e até {f(b['drx'])} % nos extremos; recebem também B as séries "
        f"com menos de {N_MINIMO_DE_CELULAS} células, escolhidas pelo centroide ou iguais às de outro concelho.",
        f"C: diferença para o Iberia01 acima de {f(b['dtot'])} % no total ou de {f(b['drx'])} % nos extremos. "
        f"Valide com uma série local.",
    ]


def limiares_em_texto() -> str:
    """Os limiares em JSON ordenado; é o valor de ``metadados.limiares``."""
    return json.dumps(LIMIARES, sort_keys=True, separators=(",", ":"))


# ── Leitura do banco ─────────────────────────────────────────────────────────────────────────

#: A tabela da concordância E-OBS menos Iberia01 mora num ficheiro ODbL à parte (decisão de 25/10/2026),
#: ao lado da base E-OBS; a qualidade por município da base ibérica mora em ``ibe_unidades.db``.
ARQUIVO_DA_QUALIDADE = "qualidade_eobs_odbl.db"


def _iberica_ok() -> bool:
    try:
        from triton.core import base_climatica_iberica as _ib
        return _ib.disponivel()
    except Exception:
        return False


def _conectar():
    """Liga ao ficheiro ODbL da qualidade da E-OBS (ao lado de ``portugal_eobs.db``)."""
    import os
    import sqlite3
    from triton.core import base_climatica_portugal as _pt
    base = _pt.caminho_da_base()
    if base is None:
        raise FileNotFoundError("A base E-OBS não está instalada.")
    arq = os.path.join(os.path.dirname(base), ARQUIVO_DA_QUALIDADE)
    if not os.path.isfile(arq):
        raise FileNotFoundError(f"O ficheiro {ARQUIVO_DA_QUALIDADE} não está instalado.")
    return sqlite3.connect(f"file:{arq}?mode=ro", uri=True)


def tem_qualidade_eobs() -> bool:
    """A tabela de concordância da E-OBS (ficheiro ODbL separado) está instalada?"""
    from triton.core import base_climatica_portugal as _pt
    if not _pt.disponivel():
        return False
    try:
        with _conectar() as con:
            return con.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'qualidade'").fetchone()[0] == 1
    except Exception:
        return False


def tem_qualidade() -> bool:
    """Há nível de qualidade A/B/C instalado: o da base ibérica (por município) ou o da E-OBS."""
    return _iberica_ok() or tem_qualidade_eobs()


@lru_cache(maxsize=1)
def _tabela() -> Dict[str, Dict[str, Any]]:
    cols = ("dtmn", "concelho", "n_eff", "metodo", "repetida", "dtot", "drx", "nivel", "motivo")
    with _conectar() as con:
        linhas = con.execute("SELECT " + ", ".join(cols) + " FROM qualidade").fetchall()
    return {r[1]: dict(zip(cols, r)) for r in linhas}


def qualidade_do_concelho(concelho: str) -> Optional[Dict[str, Any]]:
    """A linha de qualidade do concelho na base E-OBS, ou None sem a tabela ou sem o concelho."""
    if not tem_qualidade_eobs():
        return None
    linha = _tabela().get(concelho)
    return dict(linha) if linha else None


def contagem_por_nivel() -> Dict[str, int]:
    """{'A': n, 'B': n, 'C': n}: dos municípios da base ibérica ou, sem ela, da tabela da E-OBS; vazio sem nenhuma."""
    if _iberica_ok():
        from triton.core import base_climatica_iberica as _ib
        return _ib.contagem_por_nivel()
    if not tem_qualidade_eobs():
        return {}
    cont = {n: 0 for n in NIVEIS}
    for linha in _tabela().values():
        cont[linha["nivel"]] += 1
    return cont


def metadados_da_qualidade() -> Dict[str, str]:
    """As chaves do ficheiro ODbL da qualidade: qualidade_versao, limiares, espanha_locais (contagem real)..."""
    if not tem_qualidade_eobs():
        return {}
    with _conectar() as con:
        return dict(con.execute("SELECT chave, valor FROM metadados"))


def linha_de_cobertura(lingua: str = "pt") -> str:
    """«Cobertura: Portugal 308 locais, Espanha 8131 locais; chuva Iberia01 ...» (base ibérica) ou a linha da E-OBS.

    Os números são lidos do banco, nunca digitados. Sem nenhuma tabela, a linha diz só o que sabe.
    """
    if _iberica_ok():
        from triton.core import base_climatica_iberica as _ib
        return _ib.linha_de_cobertura(lingua)
    if not tem_qualidade_eobs():
        return {"en": "Coverage: no rainfall quality table in this installation",
                "es": "Cobertura: sin la tabla de calidad de la lluvia en esta instalación",
                "zh": "覆盖范围：本安装中没有降雨质量表"}.get(lingua, "Cobertura: sem a tabela de qualidade da chuva nesta instalação")
    cont = contagem_por_nivel()
    n = sum(cont.values())
    espanha = metadados_da_qualidade().get("espanha_locais", "0")
    if lingua == "en":
        return (f"Coverage: continental Portugal {n} municipalities (A {cont['A']}, B {cont['B']}, C {cont['C']}); "
                f"Spain: {espanha} sites")
    if lingua == "es":
        return (f"Cobertura: Portugal continental {n} municipios (A {cont['A']}, B {cont['B']}, C {cont['C']}); "
                f"España: {espanha} sitios")
    if lingua == "zh":
        return (f"覆盖范围：葡萄牙大陆 {n} 个市镇（A {cont['A']}、B {cont['B']}、C {cont['C']}）；"
                f"西班牙：{espanha} 个站点")
    return (f"Cobertura: Portugal continental {n} concelhos (A {cont['A']}, B {cont['B']}, C {cont['C']}); "
            f"Espanha: {espanha} locais")


def texto_da_qualidade(concelho: str, lingua: str = "pt") -> str:
    """«Qualidade da chuva: nível B. motivo» para o ecrã e o rodapé do laudo; vazio se não houver dado."""
    q = qualidade_do_concelho(concelho)
    if not q:
        return ""
    if lingua == "pt":
        return f"Qualidade da chuva em {concelho}: nível {q['nivel']}. {q['motivo']}"
    if lingua == "es":
        return (f"Calidad de la lluvia en {concelho}: nivel {q['nivel']} (E-OBS menos Iberia01, 1971–2000: total "
                f"{q['dtot']:+.1f} %, extremos {q['drx']:+.1f} %; {int(q['n_eff'])} celda(s)).")
    if lingua == "zh":
        return (f"{concelho}的降雨质量：{q['nivel']} 级（E-OBS 减 Iberia01，1971–2000 年：总量 "
                f"{q['dtot']:+.1f} %，极值 {q['drx']:+.1f} %；{int(q['n_eff'])} 个网格单元）。")
    return (f"Rainfall quality for {concelho}: level {q['nivel']} (E-OBS minus Iberia01, 1971–2000: total "
            f"{q['dtot']:+.1f} %, extremes {q['drx']:+.1f} %; {int(q['n_eff'])} cell(s)).")
