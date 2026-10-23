# -*- coding: utf-8 -*-
"""Nível de qualidade (A, B ou C) da chuva por concelho da edição IBE.

Uma só fórmula, num só lugar. O banco (``data/portugal_eobs.db``, tabela ``qualidade``), a
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

def _conectar():
    from triton.core import base_climatica_portugal as _pt
    return _pt._conectar()


def tem_qualidade() -> bool:
    """A base instalada traz a tabela ``qualidade``?"""
    from triton.core import base_climatica_portugal as _pt
    if not _pt.disponivel():
        return False
    try:
        with _conectar() as con:
            return con.execute("SELECT COUNT(*) FROM sqlite_master WHERE name = 'qualidade'").fetchone()[0] == 1
    except Exception:
        return False


@lru_cache(maxsize=1)
def _tabela() -> Dict[str, Dict[str, Any]]:
    cols = ("dtmn", "concelho", "n_eff", "metodo", "repetida", "dtot", "drx", "nivel", "motivo")
    with _conectar() as con:
        linhas = con.execute("SELECT " + ", ".join(cols) + " FROM qualidade").fetchall()
    return {r[1]: dict(zip(cols, r)) for r in linhas}


def qualidade_do_concelho(concelho: str) -> Optional[Dict[str, Any]]:
    """A linha de qualidade do concelho (nível, motivo, medidas), ou None sem a tabela ou sem o concelho."""
    if not tem_qualidade():
        return None
    linha = _tabela().get(concelho)
    return dict(linha) if linha else None


def contagem_por_nivel() -> Dict[str, int]:
    """{'A': n, 'B': n, 'C': n} lido da tabela ``qualidade``; vazio sem a tabela."""
    if not tem_qualidade():
        return {}
    cont = {n: 0 for n in NIVEIS}
    for linha in _tabela().values():
        cont[linha["nivel"]] += 1
    return cont


def metadados_da_qualidade() -> Dict[str, str]:
    """As chaves de ``metadados`` do pacote: pacote_id, versao_eobs, qualidade_versao, limiares..."""
    from triton.core import base_climatica_portugal as _pt
    if not _pt.disponivel():
        return {}
    meta = _pt.metadados()
    chaves = ("pacote_id", "versao_eobs", "sha256_pacote", "qualidade_versao", "limiares", "espanha_locais")
    return {k: meta[k] for k in chaves if k in meta}


def linha_de_cobertura(lingua: str = "pt") -> str:
    """«Cobertura: Portugal continental 278 concelhos (A 45, B 159, C 74); Espanha: 0 locais».

    Os números são lidos do banco (a tabela ``qualidade`` e a chave ``espanha_locais``), nunca
    digitados. Sem a tabela (base antiga ou ausente), a linha diz só o que sabe.
    """
    if not tem_qualidade():
        return ("Coverage: no rainfall quality table in this installation" if lingua == "en"
                else "Cobertura: sem a tabela de qualidade da chuva nesta instalação")
    cont = contagem_por_nivel()
    n = sum(cont.values())
    espanha = metadados_da_qualidade().get("espanha_locais", "0")
    if lingua == "en":
        return (f"Coverage: continental Portugal {n} municipalities (A {cont['A']}, B {cont['B']}, C {cont['C']}); "
                f"Spain: {espanha} sites")
    return (f"Cobertura: Portugal continental {n} concelhos (A {cont['A']}, B {cont['B']}, C {cont['C']}); "
            f"Espanha: {espanha} locais")


def texto_da_qualidade(concelho: str, lingua: str = "pt") -> str:
    """«Qualidade da chuva: nível B. motivo» para o ecrã e o rodapé do laudo; vazio se não houver dado."""
    q = qualidade_do_concelho(concelho)
    if not q:
        return ""
    if lingua == "pt":
        return f"Qualidade da chuva em {concelho}: nível {q['nivel']}. {q['motivo']}"
    return (f"Rainfall quality for {concelho}: level {q['nivel']} (E-OBS minus Iberia01, 1971–2000: total "
            f"{q['dtot']:+.1f} %, extremes {q['drx']:+.1f} %; {int(q['n_eff'])} cell(s)).")
