"""
Módulo de Acesso e Gerenciamento da Base de dados CLIMBra (CMIP6 / Triton).

A base é extraída do CLIMBra (Ballarin et al., 2023, Scientific Data,
doi:10.1038/s41597-023-01956-z): 19 modelos CMIP6 corrigidos de viés por
Quantile Delta Mapping, em grade de 0,25°. São 37.164 arquivos, um por cidade,
modelo e simulação: 652 cidades × 19 modelos × (histórica 1980–2013, SSP2-4.5 e
SSP5-8.5 de 2015 a 2100). Todos em calendário gregoriano; HadGEM3-GC31-LL, KACE
e UKESM1-0-LL, de calendário nativo de 360 dias, têm um dia a menos no fim.

Não há janelas fixas: versões antigas separavam futuro próximo, médio e
distante em arquivos próprios. O usuário recorta o período que quiser, e
`RECORTES_SUGERIDOS` oferece atalhos de trinta anos, a duração das normais
climatológicas.

Onde ficam as séries compiladas: um banco SQLite por modelo, `data/climbra_<modelo>.db`
(cerca de 40 a 44 MB cada, abaixo do limite de arquivo do GitHub). Se algum modelo
passar do limite, o banco do modelo pode ser dividido por cenário, em
`climbra_<modelo>__<cenário>.db`. O `data/climbra.db` único das versões anteriores
continua sendo lido, quando existe. Ver `scripts/dividir_base_climbra.py`.
"""

import os
import re
import sqlite3
import unicodedata
import zlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

# Modelos GCMs disponíveis na base CMIP6
DEFAULT_CLIMATE_MODEL = "INM-CM4"

CLIMATE_MODELS: List[str] = [
    "INM-CM4",
    "ACCESS-CM2",
    "ACCESS-ESM1-5",
    "CMCC-ESM2",
    "EC-EARTH3",
    "GFDL-CM4",
    "GFDL-ESM4",
    "HadGEM3-GC31-LL",
    "INM-CM5",
    "IPSL-CM6A-LR",
    "KACE",
    "KIOST",
    "MIROC6",
    "MPI-ESM1-2",
    "MRI-ESM2",
    "NESM3",
    "NorESM2-MM",
    "TaiESM1",
    "UKESM1-0-LL",
]

# Definição de Cenários e Horizontes Temporais (CLIMBra / CMIP6)
CLIMATE_SCENARIOS: Dict[str, Dict[str, Any]] = {
    "HIST": {
        "label": "Série Histórica de Referência (01/01/1980 a 31/12/2013)",
        "file_suffix": "Histórico.csv",
        "start_date": "01/01/1980",
        "end_date": "31/12/2013",
        "default_years": 34,
    },
    "SSP245": {
        "label": "SSP2-4.5 — Cenário Intermediário (01/01/2015 a 31/12/2100)",
        "file_suffix": "SSP245.csv",
        "start_date": "01/01/2015",
        "end_date": "31/12/2100",
        "default_years": 86,
    },
    "SSP585": {
        "label": "SSP5-8.5 — Cenário Extremo / Pessimista (01/01/2015 a 31/12/2100)",
        "file_suffix": "SSP585.csv",
        "start_date": "01/01/2015",
        "end_date": "31/12/2100",
        "default_years": 86,
    },
}

#: Atalhos de recorte por simulação, em (rótulo, data inicial, data final). São
#: sugestões: o recorte é livre. Trinta anos é a duração das normais
#: climatológicas da OMM; abaixo de dez, o resultado depende do trecho sorteado.
RECORTES_SUGERIDOS: Dict[str, List[Tuple[str, str, str]]] = {
    "HIST": [
        ("Série completa, 1980–2013", "01/01/1980", "31/12/2013"),
        ("Trinta anos, 1981–2010", "01/01/1981", "31/12/2010"),
    ],
    "SSP245": [
        ("Série completa, 2015–2100", "01/01/2015", "31/12/2100"),
        ("Futuro próximo, 2021–2050", "01/01/2021", "31/12/2050"),
        ("Meados do século, 2041–2070", "01/01/2041", "31/12/2070"),
        ("Fim do século, 2071–2100", "01/01/2071", "31/12/2100"),
    ],
}
RECORTES_SUGERIDOS["SSP585"] = list(RECORTES_SUGERIDOS["SSP245"])

#: Abaixo deste número de anos, a interface avisa que o recorte é curto.
ANOS_MINIMOS_RECOMENDADOS = 10.0

_BASE_DIR_CACHE: Optional[str] = None
_CITY_FILENAME_MAP: Optional[Dict[str, str]] = None
_DB_PATH_CACHE: Optional[str] = None
_LAYOUT_CACHE: Optional[Dict[str, Any]] = None

#: `climbra_<modelo>.db` ou `climbra_<modelo>__<cenário>.db`.
_PADRAO_DA_PARTE = re.compile(r"^climbra_(?P<modelo>.+?)(?:__(?P<cenario>HIST|SSP245|SSP585))?\.db$")
_NOME_DO_BANCO_UNICO = "climbra.db"


def _normalize_name(name: str) -> str:
    """Normaliza nome removendo acentos, pontuações e espaços para indexação segura."""
    if not name:
        return ""
    nfkd = unicodedata.normalize("NFD", str(name))
    cleaned = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return cleaned.lower().replace(" ", "").replace("-", "").replace("'", "").replace("_", "")


def limpar_cache_da_base() -> None:
    """Esquece onde estão os bancos e o índice de cidades (após mudar a pasta ou as variáveis de ambiente)."""
    global _BASE_DIR_CACHE, _CITY_FILENAME_MAP, _DB_PATH_CACHE, _LAYOUT_CACHE
    _BASE_DIR_CACHE = _CITY_FILENAME_MAP = _DB_PATH_CACHE = _LAYOUT_CACHE = None


def _varrer_pasta(pasta: str) -> Optional[Dict[str, Any]]:
    """Bancos CLIMBra de uma pasta: as partes por modelo e, se houver, o banco único antigo."""
    try:
        nomes = sorted(os.listdir(pasta))
    except OSError:
        return None
    partes: Dict[str, Dict[Optional[str], str]] = {}
    legado: Optional[str] = None
    for nome in nomes:
        caminho = os.path.join(pasta, nome)
        if not os.path.isfile(caminho):
            continue
        if nome == _NOME_DO_BANCO_UNICO:
            legado = os.path.abspath(caminho)
            continue
        achado = _PADRAO_DA_PARTE.match(nome)
        if achado:
            partes.setdefault(achado.group("modelo"), {})[achado.group("cenario")] = os.path.abspath(caminho)
    if not partes and not legado:
        return None
    return {"pasta": os.path.abspath(pasta), "partes": partes, "legado": legado}


def _pastas_de_busca() -> List[str]:
    """Pastas onde procurar os bancos, da mais específica para a mais genérica."""
    import sys
    pasta_do_executavel = (os.path.dirname(sys.executable)
                           if getattr(sys, "frozen", False) else "")
    raiz_do_programa = os.path.join(os.path.dirname(__file__), "..", "..")
    pastas = [
        os.environ.get("TRITON_CLIMBRA_DIR", ""),
        os.path.join(pasta_do_executavel, "data") if pasta_do_executavel else "",
        pasta_do_executavel,
        os.path.join(raiz_do_programa, "data"),
        raiz_do_programa,
        os.path.join(os.getcwd(), "data"),
        os.getcwd(),
    ]
    return [p for p in pastas if p]


def _arquivos_do_layout(layout: Dict[str, Any]) -> List[str]:
    arquivos = [c for por_cenario in layout["partes"].values() for c in por_cenario.values()]
    if layout["legado"]:
        arquivos.append(layout["legado"])
    return arquivos


def _layout_dos_bancos() -> Optional[Dict[str, Any]]:
    """Descobre os bancos CLIMBra: `{"pasta", "partes": {modelo: {cenário|None: caminho}}, "legado"}`.

    Ordem: variáveis de ambiente (TRITON_CLIMBRA_DB e TRITON_CLIMATE_DB, que aceitam um arquivo
    ou uma pasta; TRITON_CLIMBRA_DIR, uma pasta), depois as pastas do programa. Vale a primeira
    pasta que tiver bancos. O resultado fica em cache enquanto os arquivos existirem.
    """
    global _LAYOUT_CACHE
    if _LAYOUT_CACHE:
        if all(os.path.isfile(a) for a in _arquivos_do_layout(_LAYOUT_CACHE)):
            return _LAYOUT_CACHE
        _LAYOUT_CACHE = None

    for variavel in ("TRITON_CLIMBRA_DB", "TRITON_CLIMATE_DB"):
        valor = os.environ.get(variavel, "")
        if not valor:
            continue
        achado = None
        if os.path.isdir(valor):
            achado = _varrer_pasta(valor)
        elif os.path.isfile(valor):
            nome = os.path.basename(valor)
            parte = _PADRAO_DA_PARTE.match(nome)
            achado = {"pasta": os.path.dirname(os.path.abspath(valor)), "partes": {}, "legado": None}
            if parte and nome != _NOME_DO_BANCO_UNICO:
                achado["partes"] = {parte.group("modelo"): {parte.group("cenario"): os.path.abspath(valor)}}
            else:
                achado["legado"] = os.path.abspath(valor)
        if achado:
            _LAYOUT_CACHE = achado
            return achado

    for pasta in _pastas_de_busca():
        achado = _varrer_pasta(pasta)
        if achado:
            _LAYOUT_CACHE = achado
            return achado
    return None


def _caminhos_dos_bancos(model_name: str, scenario_key: str) -> List[str]:
    """Bancos que podem ter a série (modelo, cenário), na ordem de preferência.

    Primeiro o banco do modelo dividido por cenário, depois o banco do modelo inteiro e, por
    último, o `climbra.db` único antigo.
    """
    layout = _layout_dos_bancos()
    if not layout:
        return []
    por_cenario = layout["partes"].get(model_name, {})
    caminhos = [por_cenario[c] for c in (scenario_key, None) if c in por_cenario]
    if layout["legado"]:
        caminhos.append(layout["legado"])
    return caminhos


def _abrir_somente_leitura(caminho: str) -> sqlite3.Connection:
    """Abre o banco só para leitura (a pasta de instalação pode ser protegida)."""
    from pathlib import Path
    try:
        return sqlite3.connect(Path(caminho).resolve().as_uri() + "?mode=ro", uri=True)
    except (sqlite3.Error, ValueError):
        return sqlite3.connect(caminho)


def get_climate_db_path() -> Optional[str]:
    """Caminho de um banco SQLite CLIMBra compilado, se existir.

    Com a base dividida por modelo, devolve o banco do modelo padrão (ou do primeiro disponível);
    com o `climbra.db` único antigo, devolve-o. Para todos os arquivos, use `get_climate_db_paths()`.
    """
    global _DB_PATH_CACHE
    if _DB_PATH_CACHE and os.path.isfile(_DB_PATH_CACHE):
        return _DB_PATH_CACHE
    layout = _layout_dos_bancos()
    if not layout:
        return None
    if layout["partes"]:
        modelo = DEFAULT_CLIMATE_MODEL if DEFAULT_CLIMATE_MODEL in layout["partes"] else sorted(layout["partes"])[0]
        por_cenario = layout["partes"][modelo]
        _DB_PATH_CACHE = por_cenario.get(None) or por_cenario[sorted(c for c in por_cenario if c)[0]]
    else:
        _DB_PATH_CACHE = layout["legado"]
    return _DB_PATH_CACHE


def get_climate_db_paths() -> List[str]:
    """Todos os bancos CLIMBra encontrados (as partes por modelo e o banco único antigo, se houver)."""
    layout = _layout_dos_bancos()
    if not layout:
        return []
    return sorted(_arquivos_do_layout(layout))


def get_available_climate_models() -> List[str]:
    """Modelos CMIP6 que têm série nos bancos encontrados, na ordem de `CLIMATE_MODELS`.

    Com o banco único antigo, são os modelos que ele contém. Sem banco nenhum, a lista é vazia.
    """
    layout = _layout_dos_bancos()
    if not layout:
        return []
    modelos = set(layout["partes"])
    if layout["legado"]:
        try:
            conn = _abrir_somente_leitura(layout["legado"])
            try:
                modelos.update(m for (m,) in conn.execute("SELECT DISTINCT model FROM climbra_series;"))
            finally:
                conn.close()
        except sqlite3.Error:
            pass
    return [m for m in CLIMATE_MODELS if m in modelos] + sorted(m for m in modelos if m not in CLIMATE_MODELS)


def climate_database_available() -> bool:
    """Há base CLIMBra utilizável: bancos compilados ou a pasta de CSV soltos?"""
    return bool(_layout_dos_bancos()) or os.path.isdir(get_climate_database_dir())


def get_climate_database_dir() -> str:
    """Localiza o diretório raiz das séries temporais da base de 652 cidades."""
    global _BASE_DIR_CACHE
    if _BASE_DIR_CACHE and os.path.isdir(_BASE_DIR_CACHE):
        return _BASE_DIR_CACHE

    # Ordem de busca, da mais específica para a mais genérica.
    #
    # A primeira entrada é a localização canônica: a base climática fica na raiz do
    # programa, ao lado do pacote `triton`. As demais existem para execução a partir
    # de outro diretório de trabalho (scripts de estudo) e para instalações que
    # optem por mantê-la sob `data/`.
    #
    # A variável de ambiente TRITON_CLIMATE_DATA_DIR tem precedência sobre todas,
    # para instalações que guardem os ~6,5 GB fora da árvore do programa.
    raiz_do_programa = os.path.join(os.path.dirname(__file__), "..", "..")
    # No programa instalado, o código fica em _internal\triton; a base é
    # instalada ao lado do executável, na pasta do programa.
    import sys
    pasta_do_executavel = (os.path.dirname(sys.executable)
                           if getattr(sys, "frozen", False) else "")
    candidates = [
        os.environ.get("TRITON_CLIMATE_DATA_DIR", ""),
        # Localização padrão nova: climbra_data
        os.path.join(pasta_do_executavel, "climbra_data") if pasta_do_executavel else "",
        os.path.join(raiz_do_programa, "climbra_data"),
        os.path.join(os.getcwd(), "climbra_data"),
        os.path.join(raiz_do_programa, "data", "climbra_data"),
        os.path.join(os.getcwd(), "data", "climbra_data"),
        # Compatibilidade com instalações existentes da 1.0.0
        os.path.join(pasta_do_executavel, "Triton future files for 652 cities") if pasta_do_executavel else "",
        os.path.join(raiz_do_programa, "Triton future files for 652 cities"),
        os.path.join(os.getcwd(), "Triton future files for 652 cities"),
        os.path.join(raiz_do_programa, "data", "Triton future files for 652 cities"),
        os.path.join(os.getcwd(), "data", "Triton future files for 652 cities"),
    ]
    candidates = [c for c in candidates if c]

    for cand in candidates:
        norm_path = os.path.abspath(cand)
        if os.path.isdir(norm_path):
            _BASE_DIR_CACHE = norm_path
            return norm_path

    # Fallback para o primeiro caminho candidato absoluto
    fallback = os.path.abspath(candidates[0])
    _BASE_DIR_CACHE = fallback
    return fallback


def _build_city_filename_map() -> Dict[str, str]:
    """Cria um mapa dos nomes normalizados das cidades para os nomes reais de arquivo ou registro."""
    global _CITY_FILENAME_MAP
    if _CITY_FILENAME_MAP is not None:
        return _CITY_FILENAME_MAP

    city_map = {}

    # 1. Prioriza os bancos SQLite compilados (um por modelo, ou o climbra.db único antigo).
    #    Todos os bancos trazem a tabela completa de cidades; basta ler o primeiro que responder.
    layout = _layout_dos_bancos()
    candidatos = []
    if layout:
        if get_climate_db_path():
            candidatos.append(get_climate_db_path())
        candidatos += [c for c in _arquivos_do_layout(layout) if c not in candidatos]
    for db_path in candidatos:
        try:
            conn = _abrir_somente_leitura(db_path)
            try:
                for norm, city in conn.execute("SELECT city_norm, city FROM climbra_cities;"):
                    city_map[norm] = city
            finally:
                conn.close()
        except Exception:
            city_map = {}
            continue
        if city_map:
            _CITY_FILENAME_MAP = city_map
            return city_map

    # 2. Fallback: lê do diretório de arquivos CSV soltos
    base_dir = get_climate_database_dir()
    if os.path.isdir(base_dir):
        try:
            for fname in os.listdir(base_dir):
                if fname.startswith("(Triton)") and fname.endswith(".csv"):
                    clean = fname[8:].replace(".csv", "")
                    parts = clean.split("_")
                    if parts:
                        city_part = parts[0]
                        norm = _normalize_name(city_part)
                        if norm and norm not in city_map:
                            city_map[norm] = city_part
        except Exception:
            pass

    _CITY_FILENAME_MAP = city_map
    return city_map


def find_matching_climate_city_name(city_name: str) -> Optional[str]:
    """Encontra o nome exato da cidade conforme indexado nos arquivos de clima."""
    city_map = _build_city_filename_map()
    norm = _normalize_name(city_name)
    return city_map.get(norm)


def get_available_climate_cities() -> List[str]:
    """Retorna a lista ordenada de todas as cidades disponíveis na base climática nacional."""
    city_map = _build_city_filename_map()
    return sorted(list(set(city_map.values())))


def get_climate_file_path(
    city_name: str,
    model_name: str = "ACCESS-CM2",
    scenario_key: str = "HIST",
) -> Optional[str]:
    """
    Retorna o caminho do arquivo CSV correspondente à cidade, modelo e cenário.
    Tolera pequenas variações de acentuação e encoding no sistema de arquivos.
    """
    base_dir = get_climate_database_dir()
    if not os.path.isdir(base_dir):
        return None

    matched_city = find_matching_climate_city_name(city_name) or city_name
    scenario_info = CLIMATE_SCENARIOS.get(scenario_key, CLIMATE_SCENARIOS["HIST"])
    suffix = scenario_info["file_suffix"]

    # Tentativas diretas
    direct_candidates = [
        f"(Triton){matched_city}_{model_name}_{suffix}",
    ]
    if "Histórico" in suffix:
        direct_candidates.append(f"(Triton){matched_city}_{model_name}_Historico.csv")

    for dc in direct_candidates:
        direct_path = os.path.join(base_dir, dc)
        if os.path.exists(direct_path):
            return direct_path

    # Busca resiliente a encoding (ex: 'Histórico' vs 'Histrico' em Windows)
    norm_city = _normalize_name(matched_city)
    norm_model = _normalize_name(model_name)
    norm_suffix = _normalize_name(suffix.replace(".csv", ""))

    try:
        for fname in os.listdir(base_dir):
            if not fname.startswith("(Triton)") or not fname.endswith(".csv"):
                continue
            clean = fname[8:-4]
            parts = clean.split("_")
            if len(parts) >= 3:
                f_city = _normalize_name(parts[0])
                f_model = _normalize_name(parts[1])
                f_scen = _normalize_name("_".join(parts[2:]))
                if f_city == norm_city and f_model == norm_model:
                    if norm_suffix in f_scen or f_scen in norm_suffix:
                        return os.path.join(base_dir, fname)
    except Exception:
        pass

    return None


def parse_date_str(d_str: str, default: datetime) -> datetime:
    """Converte string de data flexível (dd/mm/aaaa, aaaa-mm-dd ou aaaa) para objeto datetime."""
    if not d_str:
        return default
    s = str(d_str).strip()
    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    # Se fornecido apenas o ano (ex: "1995")
    if s.isdigit() and len(s) == 4:
        return datetime(int(s), 1, 1)
    return default


def load_national_climate_series(
    city_name: str,
    model_name: str = DEFAULT_CLIMATE_MODEL,
    scenario_key: str = "HIST",
    start_date_str: Optional[str] = None,
    end_date_str: Optional[str] = None,
) -> Tuple[np.ndarray, str, str, int, int, str]:
    """
    Carrega a série diária de chuva da Base Nacional (priorizando os bancos compilados),
    aplicando recorte de datas opcional.

    Retorna:
    - precip_data: np.ndarray com precipitação diária em mm
    - eff_start_date: string "dd/mm/aaaa" da data inicial efetiva do recorte
    - eff_end_date: string "dd/mm/aaaa" da data final efetiva do recorte
    - total_days_file: total de dias disponíveis no arquivo original
    - selected_days: quantidade de dias selecionados após o recorte
    - file_path: caminho do arquivo ou identificador canônico da série carregada
    """
    matched_city = find_matching_climate_city_name(city_name)
    if not matched_city:
        matched_city = city_name

    scenario_info = CLIMATE_SCENARIOS.get(scenario_key, CLIMATE_SCENARIOS["HIST"])
    base_start_date = parse_date_str(scenario_info["start_date"], datetime(1980, 1, 1))

    raw_data: Optional[np.ndarray] = None
    file_path: Optional[str] = None

    # 1. Tenta carregar dos bancos SQLite compilados (um por modelo; ou o climbra.db único antigo)
    for db_path in _caminhos_dos_bancos(model_name, scenario_key):
        try:
            conn = _abrir_somente_leitura(db_path)
            try:
                row = conn.execute(
                    "SELECT count, data FROM climbra_series WHERE city = ? AND model = ? AND scenario = ?;",
                    (matched_city, model_name, scenario_key),
                ).fetchone()
            finally:
                conn.close()
            if row:
                cnt, blob = row
                raw_decomp = zlib.decompress(blob)
                target_dtype = np.float16 if len(raw_decomp) == cnt * 2 else np.float32
                raw_data = np.frombuffer(raw_decomp, dtype=target_dtype).astype(np.float64)

                # Identifica file_path (se existir no disco ou caminho canônico para metadados e relatórios)
                candidate_csv = get_climate_file_path(city_name, model_name, scenario_key)
                if candidate_csv and os.path.exists(candidate_csv):
                    file_path = candidate_csv
                else:
                    suffix = scenario_info["file_suffix"]
                    file_path = os.path.join(os.path.dirname(db_path), f"(Triton){matched_city}_{model_name}_{suffix}")
                break
        except Exception:
            raw_data = None

    # 2. Fallback para arquivo CSV solto no disco
    if raw_data is None:
        file_path = get_climate_file_path(city_name, model_name, scenario_key)
        if not file_path or not os.path.exists(file_path):
            raise FileNotFoundError(
                f"Arquivo de série climatológica não encontrado para a cidade '{city_name}', "
                f"modelo '{model_name}' e cenário '{scenario_key}'."
            )

        csv_vals: List[float] = []
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_s = line.strip()
                if not line_s:
                    continue
                try:
                    val = float(line_s.replace(",", "."))
                    csv_vals.append(max(0.0, val))
                except ValueError:
                    # Possível cabeçalho textual na primeira linha
                    continue

        if not csv_vals:
            raise ValueError(f"O arquivo '{file_path}' não contém dados válidos de precipitação.")

        raw_data = np.array(csv_vals, dtype=np.float64)

    total_days_file = len(raw_data)
    base_end_date = base_start_date + timedelta(days=total_days_file - 1)

    # Aplicação de recorte temporal por datas
    target_start = parse_date_str(start_date_str, base_start_date) if start_date_str else base_start_date
    target_end = parse_date_str(end_date_str, base_end_date) if end_date_str else base_end_date

    # Ajuste de limites para não ultrapassar a série original
    if target_start > target_end:
        target_start, target_end = target_end, target_start

    eff_start = max(base_start_date, min(target_start, base_end_date))
    eff_end = max(eff_start, min(target_end, base_end_date))

    idx_start = max(0, (eff_start - base_start_date).days)
    idx_end = min(total_days_file, (eff_end - base_start_date).days + 1)

    if idx_start >= total_days_file:
        idx_start = 0
    if idx_end <= idx_start:
        idx_end = total_days_file

    sliced_data = raw_data[idx_start:idx_end]
    selected_days = len(sliced_data)

    eff_start_date_str = eff_start.strftime("%d/%m/%Y")
    eff_end_date_str = (eff_start + timedelta(days=selected_days - 1)).strftime("%d/%m/%Y")

    return (
        sliced_data,
        eff_start_date_str,
        eff_end_date_str,
        total_days_file,
        selected_days,
        file_path or "",
    )
