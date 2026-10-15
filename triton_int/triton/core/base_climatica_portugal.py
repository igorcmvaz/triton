# -*- coding: utf-8 -*-
"""Base de precipitação diária por concelho da Edição Portugal (PRT).

A base (``data/portugal_eobs.db``) é compilada por ``scripts/compilar_base_eobs_portugal.py``
a partir da E-OBS v33.0e (grade de 0,1°, 1950–2025) e dos limites da CAOP2025: a série de
cada concelho é a média das células da grade com centro dentro do município. Os Açores
ficam fora do domínio da E-OBS e aparecem como não cobertos, sem série emprestada.

A interface usa o mesmo painel da base nacional brasileira: o «modelo» é a própria E-OBS
(série observada) e o «cenário», ``EOBS``. ``carregar_serie`` devolve a mesma tupla que
``climate_database.load_national_climate_series``, para que o resto do programa não
precise saber de qual base a série veio.
"""

from __future__ import annotations

import os
import sqlite3
import sys
import zlib
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

import numpy as np

#: O que a configuração do projeto grava em ``climate_model`` e ``climate_scenario``.
MODELO_EOBS = "E-OBS v33.0e"
CENARIO_EOBS = "EOBS"
#: Atalhos de recorte: as normais climatológicas de trinta anos e o período mais recente.
RECORTES = [
    ("Normal 1991–2020", "01/01/1991", "31/12/2020"),
    ("Normal 1981–2010", "01/01/1981", "31/12/2010"),
    ("Normal 1971–2000", "01/01/1971", "31/12/2000"),
    ("Normal 1961–1990", "01/01/1961", "31/12/1990"),
    ("Últimos 30 anos (1996–2025)", "01/01/1996", "31/12/2025"),
]
INICIO_PADRAO, FIM_PADRAO = "01/01/1991", "31/12/2020"
CONCELHO_PADRAO, DISTRITO_PADRAO = "Lisboa", "Lisboa"
_ARQUIVO = "portugal_eobs.db"


def caminho_da_base() -> Optional[str]:
    """O arquivo da base, no programa compilado ou no código-fonte; None se não houver."""
    pasta_do_executavel = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else ""
    raiz = os.path.join(os.path.dirname(__file__), "..", "..")
    candidatos = [
        os.environ.get("TRITON_PORTUGAL_DB", ""),
        os.path.join(pasta_do_executavel, "_internal", "data", _ARQUIVO) if pasta_do_executavel else "",
        os.path.join(pasta_do_executavel, "data", _ARQUIVO) if pasta_do_executavel else "",
        os.path.join(raiz, "data", _ARQUIVO),
        os.path.join(os.getcwd(), "data", _ARQUIVO),
    ]
    for c in candidatos:
        if c and os.path.isfile(c):
            return os.path.abspath(c)
    return None


def _conectar():
    caminho = caminho_da_base()
    if caminho is None:
        raise FileNotFoundError("A base de precipitação de Portugal (data/portugal_eobs.db) não está instalada.")
    return sqlite3.connect(f"file:{caminho}?mode=ro", uri=True)


@lru_cache(maxsize=1)
def _indice() -> Tuple[Tuple[str, str, str, str], ...]:
    """(dtmn, concelho, distrito, região) de cada concelho com série."""
    with _conectar() as con:
        return tuple(con.execute("SELECT dtmn, concelho, distrito, regiao FROM series ORDER BY distrito, concelho"))


def disponivel() -> bool:
    return caminho_da_base() is not None


def distritos() -> List[str]:
    """Distritos do Continente e ilhas da Madeira com série, em ordem alfabética."""
    return sorted({d for _, _, d, _ in _indice()})


def concelhos(distrito: Optional[str] = None) -> List[str]:
    """Concelhos com série, de um distrito ou de todos."""
    return sorted(c for _, c, d, _ in _indice() if distrito is None or d == distrito)


def distrito_do_concelho(concelho: str) -> Optional[str]:
    for _, c, d, _ in _indice():
        if c == concelho:
            return d
    return None


def nao_cobertos() -> List[Dict[str, str]]:
    """Concelhos sem série (fora do domínio da E-OBS), com o motivo."""
    with _conectar() as con:
        return [dict(zip(("dtmn", "concelho", "distrito", "regiao", "motivo"), r))
                for r in con.execute("SELECT * FROM nao_cobertos ORDER BY concelho")]


def metadados() -> Dict[str, str]:
    with _conectar() as con:
        return dict(con.execute("SELECT chave, valor FROM metadados"))


def _data(texto: Optional[str], padrao: datetime) -> datetime:
    from triton.core.climate_database import parse_date_str
    return parse_date_str(texto, padrao) if texto else padrao


def carregar_serie(concelho: str, inicio: Optional[str] = None,
                   fim: Optional[str] = None) -> Tuple[np.ndarray, str, str, int, int, str]:
    """A série diária do concelho (mm), recortada; a mesma tupla da base brasileira.

    Devolve ``(precipitação, início efetivo, fim efetivo, dias na base, dias no recorte,
    identificador)``. Dia sem dado em todas as células do concelho vem como NaN: o motor o
    recusa como falha, em vez de tratá-lo como dia seco.
    """
    with _conectar() as con:
        linha = con.execute("SELECT inicio, dias, dados, dtmn FROM series WHERE concelho = ?", (concelho,)).fetchone()
    if linha is None:
        raise FileNotFoundError(f"O concelho «{concelho}» não tem série na base de Portugal.")
    ini_base, dias, blob, dtmn = linha
    serie = np.frombuffer(zlib.decompress(blob), dtype=np.float32).astype(np.float64)
    base0 = datetime.fromisoformat(ini_base)
    base1 = base0 + timedelta(days=dias - 1)
    a = max(base0, min(_data(inicio, base0), base1))
    b = max(a, min(_data(fim, base1), base1))
    i0, i1 = (a - base0).days, (b - base0).days + 1
    recorte = serie[i0:i1]
    return (recorte, a.strftime("%d/%m/%Y"), b.strftime("%d/%m/%Y"), int(dias), int(len(recorte)),
            f"E-OBS v33.0e/{dtmn}")
