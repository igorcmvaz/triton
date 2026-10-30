# -*- coding: utf-8 -*-
"""Base de precipitação diária da Península Ibérica e ilhas (Edição Ibérica, IBE), a partir do Iberia01.

Os dados vêm em ficheiros SEPARADOS do programa, sob a ODbL 1.0 (a licença do Iberia01), compilados por
``scripts/dados/compilar_base_iberia01.py`` e ``compilar_ilhas_era5.py`` (pasta da IBE):

- ``chuva_iberia01_p1.db`` ... ``p4.db``: uma linha por célula de 0,1° (série diária, inteiros de 0,1 mm, zlib);
- ``chuva_ilhas_era5.db``: nós de 0,25° da reanálise ERA5 para Canárias, Madeira e Açores (nível C);
- ``ibe_unidades.db``: municípios (chave = código INE, ``ES-28079``, ou DTMN, ``PT-1106``), pesos município->células,
  nível de qualidade A/B/C e metadados (citação, licença, SHA-256);
- ``iberia01_partes.json``: manifesto das partes (como o ``climbra_partes.json``).

A série de um município é a soma ponderada das suas células, calculada na leitura. Municípios de nome repetido
(há centenas em Espanha) distinguem-se sempre pelo código. A E-OBS (``base_climatica_portugal``) continua como
fonte opcional, não comercial; este módulo não depende dela. Nas edições BRL e INT estes ficheiros não existem e
``disponivel()`` devolve False.
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import sys
import unicodedata
import zlib
from datetime import datetime, timedelta
from functools import lru_cache
from typing import Dict, List, Optional, Tuple

import numpy as np

#: O que a configuração do projeto grava em ``climate_model`` e ``climate_scenario``.
MODELO_IBERIA01 = "Iberia01 v1.0"
CENARIO_IBERIA01 = "IBERIA01"
#: Atalhos de recorte (o Iberia01 vai de 1971 a 2015: a normal 1991-2020 não existe).
RECORTES = [
    ("Normal 1986–2015", "01/01/1986", "31/12/2015"),
    ("Normal 1971–2000", "01/01/1971", "31/12/2000"),
    ("Série completa (1971–2015)", "01/01/1971", "31/12/2015"),
]
INICIO_PADRAO, FIM_PADRAO = "01/01/1986", "31/12/2015"
UNIDADE_PADRAO, REGIAO_PADRAO = "PT-1106", "PT|Lisboa"

_UNIDADES = "ibe_unidades.db"
_MANIFESTO = "iberia01_partes.json"
_ILHAS = "chuva_ilhas_era5.db"
_NOME_DAS_PARTES = "chuva_iberia01_{}.db"
PAISES = {"PT": "Portugal", "ES": "España"}
_NAO_NUMERO = 65535
_RE_CODIGO = re.compile(r"\b(PT|ES)-(\d{4,5})\b")

CITACAO = ("Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019). "
           "Iberia01: a new gridded dataset of daily precipitation and temperatures over Iberia. Earth System Science "
           "Data, 11, 1947-1956. doi:10.5194/essd-11-1947-2019")
AVISO_LICENCA = "Contains information from Iberia01, made available under the Open Database License (ODbL 1.0)."


# ── Localização dos ficheiros ───────────────────────────────────────────────────────────────

def pastas_candidatas() -> List[str]:
    pasta_exe = os.path.dirname(sys.executable) if getattr(sys, "frozen", False) else ""
    raiz = os.path.join(os.path.dirname(__file__), "..", "..")
    cand = [os.environ.get("TRITON_IBERIA_DADOS", "")]
    if pasta_exe:
        cand += [os.path.join(pasta_exe, "_internal", "data"), os.path.join(pasta_exe, "data")]
    cand += [os.path.join(raiz, "data"), os.path.join(os.getcwd(), "data")]
    return [os.path.abspath(c) for c in cand if c]


def pasta_dos_dados() -> Optional[str]:
    """A pasta que tem ``ibe_unidades.db``; None se a instalação não traz a base ibérica."""
    for p in pastas_candidatas():
        if os.path.isfile(os.path.join(p, _UNIDADES)):
            return p
    return None


def _caminho(nome: str) -> Optional[str]:
    p = pasta_dos_dados()
    if p is None:
        return None
    f = os.path.join(p, nome)
    return f if os.path.isfile(f) else None


def disponivel() -> bool:
    """O banco de unidades e ao menos uma parte de chuva do Iberia01 estão instalados."""
    return pasta_dos_dados() is not None and bool(partes_instaladas())


def manifesto() -> Dict:
    f = _caminho(_MANIFESTO)
    if f is None:
        return {}
    with open(f, encoding="utf-8") as h:
        return json.load(h)


def partes_instaladas() -> List[str]:
    """Nomes (p1, p2...) das partes do Iberia01 presentes na pasta de dados."""
    man = manifesto()
    saida = []
    for p in man.get("partes", []):
        if _caminho(p["arquivo"]):
            saida.append(re.search(r"_(p\d+)\.db$", p["arquivo"]).group(1))
    return saida


def _conectar(nome: str):
    f = _caminho(nome)
    if f is None:
        raise FileNotFoundError(f"A base de precipitação ibérica ({nome}) não está instalada.")
    return sqlite3.connect(f"file:{f}?mode=ro", uri=True)


def _unidades_con():
    return _conectar(_UNIDADES)


def limpar_cache() -> None:
    for fn in (_tabela, _por_codigo, _celula_info, _serie_da_celula):
        fn.cache_clear()


# ── Índice: países, regiões, municípios, busca ──────────────────────────────────────────────

def _sem_acentos(t: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", t.lower()) if unicodedata.category(c) != "Mn")


@lru_cache(maxsize=1)
def _tabela() -> Tuple[dict, ...]:
    cols = ("codigo", "pais", "regiao", "provincia", "nome", "populacao", "fonte", "cobertura", "metodo",
            "celulas_dentro", "dist_celula_km", "nivel", "motivo")
    with _unidades_con() as con:
        linhas = con.execute("SELECT " + ", ".join(cols) + " FROM unidade ORDER BY pais, regiao, nome, codigo").fetchall()
    return tuple(dict(zip(cols, r)) for r in linhas)


@lru_cache(maxsize=1)
def _por_codigo() -> Dict[str, dict]:
    return {u["codigo"]: u for u in _tabela()}


def paises() -> List[Tuple[str, str]]:
    """[(sigla, nome)] dos países com unidades: Portugal e España."""
    presentes = {u["pais"] for u in _tabela()}
    return [(s, n) for s, n in PAISES.items() if s in presentes]


def regioes(pais: Optional[str] = None) -> List[Tuple[str, str]]:
    """[(chave 'PT|Lisboa', rótulo 'Portugal · Lisboa')] de distritos/ilhas (PT) e comunidades autónomas (ES)."""
    vistas, saida = set(), []
    for u in _tabela():
        if pais and u["pais"] != pais:
            continue
        k = f"{u['pais']}|{u['regiao']}"
        if k not in vistas:
            vistas.add(k)
            saida.append((k, f"{PAISES[u['pais']]} · {u['regiao']}"))
    return sorted(saida, key=lambda t: _sem_acentos(t[1]))


def unidades(regiao: Optional[str] = None) -> List[dict]:
    """As unidades de uma região (chave 'PT|Lisboa') ou todas, por nome."""
    if regiao is None:
        return list(_tabela())
    pais, _, reg = regiao.partition("|")
    return sorted((u for u in _tabela() if u["pais"] == pais and u["regiao"] == reg),
                  key=lambda u: (_sem_acentos(u["nome"]), u["codigo"]))


def unidade(codigo: str) -> Optional[dict]:
    return _por_codigo().get(codigo)


def rotulo(codigo_ou_unidade) -> str:
    """«Madrid [ES-28079]»: o texto que o projeto grava em ``climate_city_name`` (nome legível e código sem ambiguidade)."""
    u = unidade(codigo_ou_unidade) if isinstance(codigo_ou_unidade, str) else codigo_ou_unidade
    return f"{u['nome']} [{u['codigo']}]"


def resolver(texto: str) -> Optional[str]:
    """O código da unidade que o texto designa: código puro, «Nome [código]» ou nome único (sem distinção de acentos).

    Nome repetido (mais de uma unidade) não é resolvido: devolve None, e quem chama pede o código.
    """
    if not texto:
        return None
    t = texto.strip()
    m = _RE_CODIGO.search(t.upper())
    if m:
        cod = f"{m.group(1)}-{m.group(2)}"
        if cod in _por_codigo():
            return cod
    chave = _sem_acentos(t)
    achadas = [u["codigo"] for u in _tabela() if _sem_acentos(u["nome"]) == chave]
    return achadas[0] if len(achadas) == 1 else None


def candidatos(texto: str) -> List[dict]:
    """As unidades cujo nome é exatamente o texto (para mensagens de ambiguidade)."""
    chave = _sem_acentos(texto.strip())
    return [u for u in _tabela() if _sem_acentos(u["nome"]) == chave]


def buscar(texto: str, limite: int = 50) -> List[dict]:
    """Busca por nome (contém, sem acentos) ou por código; as de nome que começa pelo texto vêm primeiro."""
    t = texto.strip()
    if not t:
        return []
    m = re.fullmatch(r"(?:(PT|ES)-)?(\d{4,5})", t.upper())
    if m:
        return [u for u in _tabela() if u["codigo"].endswith("-" + m.group(2))
                and (not m.group(1) or u["pais"] == m.group(1))][:limite]
    chave = _sem_acentos(t)
    comeca, contem = [], []
    for u in _tabela():
        n = _sem_acentos(u["nome"])
        if n.startswith(chave):
            comeca.append(u)
        elif chave in n:
            contem.append(u)
    return (comeca + contem)[:limite]


def nao_cobertas() -> List[dict]:
    """Unidades sem série (Ceuta e Melilla, fora da grade), com o motivo."""
    return [u for u in _tabela() if u["cobertura"] == "nenhuma"]


def fonte_da_unidade(codigo: str) -> str:
    """«iberia01», «era5» ou «nenhuma»."""
    u = unidade(codigo)
    return u["cobertura"] if u else "nenhuma"


def metadados() -> Dict[str, str]:
    with _unidades_con() as con:
        return dict(con.execute("SELECT chave, valor FROM metadados"))


def pacote() -> Dict[str, str]:
    """Identificação do pacote: ``pacote_id``, ``sha256_pacote`` (conteúdo das células), fonte, licença e citação."""
    meta = metadados()
    return {k: meta.get(k, "") for k in ("pacote_id", "sha256_pacote", "fonte", "licenca", "periodo", "citacao",
                                         "aviso", "ilhas_fonte", "ilhas_citacao")}


# ── Qualidade (tabela no ficheiro ODbL de unidades) ─────────────────────────────────────────

def qualidade(codigo: str) -> Optional[Dict[str, str]]:
    u = unidade(codigo)
    if not u or not u["nivel"]:
        return None
    return {"nivel": u["nivel"], "motivo": u["motivo"], "metodo": u["metodo"], "fonte": u["cobertura"]}


def contagem_por_nivel(pais: Optional[str] = None, regiao: Optional[str] = None) -> Dict[str, int]:
    cont = {"A": 0, "B": 0, "C": 0}
    for u in _tabela():
        if pais and u["pais"] != pais:
            continue
        if regiao and u["regiao"] != regiao:
            continue
        if u["nivel"] in cont:
            cont[u["nivel"]] += 1
    return cont


def contagens() -> Dict[str, int]:
    """Contagens reais para a linha de cobertura: unidades por país e por tipo de cobertura."""
    c = {"PT": 0, "ES": 0, "iberia01": 0, "era5": 0, "nenhuma": 0}
    for u in _tabela():
        c[u["pais"]] += 1
        c[u["cobertura"]] += 1
    return c


# ── Células e séries ─────────────────────────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def _celula_info() -> Dict[int, Tuple[str, str]]:
    """id da célula -> (fonte, parte)."""
    with _unidades_con() as con:
        return {r[0]: (r[1], r[2]) for r in con.execute("SELECT id, fonte, parte FROM celula")}


def _arquivo_da_parte(fonte: str, parte: str) -> str:
    return _ILHAS if fonte == "era5" else _NOME_DAS_PARTES.format(parte)


@lru_cache(maxsize=4096)
def _serie_da_celula(celula: int) -> Tuple[np.ndarray, str, int]:
    """(série em mm, início ISO, dias) de uma célula; NaN onde o inteiro é o código de falha."""
    fonte, parte = _celula_info()[celula]
    arq = _arquivo_da_parte(fonte, parte)
    if _caminho(arq) is None:
        raise FileNotFoundError(f"A parte «{arq}» da base de precipitação ibérica não está instalada "
                                f"(instale o componente de dados correspondente).")
    with _conectar(arq) as con:
        inicio, dias, passo, blob = con.execute(
            "SELECT inicio, dias, passo_mm, dados FROM celula WHERE id = ?", (celula,)).fetchone()
    planos = np.frombuffer(zlib.decompress(blob), dtype=np.uint8).reshape(2, dias)
    q = planos.T.copy().view(np.uint16).reshape(dias)
    v = q.astype(np.float64) * passo
    v[q == _NAO_NUMERO] = np.nan
    v.setflags(write=False)
    return v, inicio, int(dias)


def celulas_da_unidade(codigo: str) -> List[Tuple[int, float]]:
    with _unidades_con() as con:
        return list(con.execute("SELECT celula, peso FROM unidade_celula WHERE codigo = ? ORDER BY celula", (codigo,)))


def _data(texto: Optional[str], padrao: datetime) -> datetime:
    from triton.core.climate_database import parse_date_str
    return parse_date_str(texto, padrao) if texto else padrao


def serie_completa(codigo: str) -> Tuple[np.ndarray, str]:
    """A série diária inteira (mm) da unidade e a data inicial ISO."""
    u = unidade(codigo)
    if u is None:
        raise FileNotFoundError(f"O código «{codigo}» não existe na base ibérica.")
    if u["cobertura"] == "nenhuma":
        raise FileNotFoundError(f"{u['nome']} [{codigo}] não tem série: {u['motivo']}.")
    cel = celulas_da_unidade(codigo)
    if not cel:
        raise FileNotFoundError(f"{u['nome']} [{codigo}] não tem células associadas na base.")
    acum, inicio, dias = None, None, 0
    pesos = sum(p for _, p in cel)
    for c, p in cel:
        v, ini, n = _serie_da_celula(c)
        acum = v * (p / pesos) if acum is None else acum + v * (p / pesos)
        inicio, dias = ini, n
    return acum, inicio


def carregar_serie(unidade_ou_texto: str, inicio: Optional[str] = None,
                   fim: Optional[str] = None) -> Tuple[np.ndarray, str, str, int, int, str]:
    """A série diária do município (mm), recortada; a mesma tupla da CLIMBra e da E-OBS.

    ``unidade_ou_texto``: código («ES-28079»), «Nome [código]» ou nome único. Devolve ``(precipitação, início
    efetivo, fim efetivo, dias na base, dias no recorte, identificador)``. Nome ambíguo levanta ``ValueError``
    com as alternativas; unidade sem cobertura levanta ``FileNotFoundError``.
    """
    codigo = resolver(unidade_ou_texto)
    if codigo is None:
        alt = candidatos(unidade_ou_texto)
        if len(alt) > 1:
            raise ValueError(f"O nome «{unidade_ou_texto}» é ambíguo ({len(alt)} municípios); use o código: " +
                             ", ".join(f"{u['codigo']} ({u['provincia']})" for u in alt[:8]))
        raise FileNotFoundError(f"«{unidade_ou_texto}» não existe na base de precipitação ibérica.")
    serie, ini_base = serie_completa(codigo)
    dias = len(serie)
    base0 = datetime.fromisoformat(ini_base)
    base1 = base0 + timedelta(days=dias - 1)
    a = max(base0, min(_data(inicio, base0), base1))
    b = max(a, min(_data(fim, base1), base1))
    i0, i1 = (a - base0).days, (b - base0).days + 1
    fonte = "ERA5" if fonte_da_unidade(codigo) == "era5" else MODELO_IBERIA01
    return (np.array(serie[i0:i1]), a.strftime("%d/%m/%Y"), b.strftime("%d/%m/%Y"), int(dias), int(i1 - i0),
            f"{fonte}/{codigo}")


# ── Textos de fonte, licença e cobertura ─────────────────────────────────────────────────────

def texto_da_fonte(codigo: str, lingua: str = "pt") -> str:
    """Fonte e licença da série do município, para o ecrã e o rodapé do laudo."""
    f = fonte_da_unidade(codigo)
    if f == "era5":
        return {"en": "Source: ERA5 reanalysis (0.25°, Copernicus C3S, CC BY 4.0, via Open-Meteo); outside the Iberia01 domain. "
                      "Quality C: not validated locally.",
                "es": "Fuente: reanálisis ERA5 (0,25°, Copernicus C3S, CC BY 4.0, vía Open-Meteo); fuera del dominio de Iberia01. "
                      "Calidad C: sin validación local."}.get(
            lingua, "Fonte: reanálise ERA5 (0,25°, Copernicus C3S, CC BY 4.0, via Open-Meteo); fora do domínio do Iberia01. "
                    "Qualidade C: sem validação local.")
    return {"en": "Source: Iberia01 v1.0 (Herrera et al. 2019, ESSD, doi:10.5194/essd-11-1947-2019), ODbL 1.0. " + AVISO_LICENCA,
            "es": "Fuente: Iberia01 v1.0 (Herrera et al. 2019, ESSD, doi:10.5194/essd-11-1947-2019), ODbL 1.0. " + AVISO_LICENCA}.get(
        lingua, "Fonte: Iberia01 v1.0 (Herrera et al. 2019, ESSD, doi:10.5194/essd-11-1947-2019), ODbL 1.0. " + AVISO_LICENCA)


def linha_de_cobertura(lingua: str = "pt") -> str:
    """«Cobertura: Portugal 308 locais, Espanha 8 131 locais; chuva Iberia01 8 319, ERA5 (nível C) 118, sem série 2». Lida do banco."""
    if not disponivel():
        return ""
    c = contagens()
    if lingua == "en":
        return (f"Coverage: Portugal {c['PT']} sites, Spain {c['ES']} sites; Iberia01 rainfall {c['iberia01']}, "
                f"ERA5 (level C) {c['era5']}, no series {c['nenhuma']}")
    if lingua == "es":
        return (f"Cobertura: Portugal {c['PT']} sitios, España {c['ES']} sitios; lluvia Iberia01 {c['iberia01']}, "
                f"ERA5 (nivel C) {c['era5']}, sin serie {c['nenhuma']}")
    return (f"Cobertura: Portugal {c['PT']} locais, Espanha {c['ES']} locais; chuva Iberia01 {c['iberia01']}, "
            f"ERA5 (nível C) {c['era5']}, sem série {c['nenhuma']}")
