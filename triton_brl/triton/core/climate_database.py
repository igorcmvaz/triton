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
"""

import os
import unicodedata
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


def _normalize_name(name: str) -> str:
    """Normaliza nome removendo acentos, pontuações e espaços para indexação segura."""
    if not name:
        return ""
    nfkd = unicodedata.normalize("NFD", str(name))
    cleaned = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return cleaned.lower().replace(" ", "").replace("-", "").replace("'", "").replace("_", "")


def get_climate_db_path() -> Optional[str]:
    """Localiza o arquivo do banco de dados SQLite compilado (climbra.db), se existir."""
    global _DB_PATH_CACHE
    if _DB_PATH_CACHE and os.path.isfile(_DB_PATH_CACHE):
        return _DB_PATH_CACHE

    import sys
    pasta_do_executavel = (os.path.dirname(sys.executable)
                           if getattr(sys, "frozen", False) else "")
    raiz_do_programa = os.path.join(os.path.dirname(__file__), "..", "..")

    candidates = [
        os.environ.get("TRITON_CLIMBRA_DB", ""),
        os.environ.get("TRITON_CLIMATE_DB", ""),
        os.path.join(pasta_do_executavel, "data", "climbra.db") if pasta_do_executavel else "",
        os.path.join(pasta_do_executavel, "climbra.db") if pasta_do_executavel else "",
        os.path.join(raiz_do_programa, "data", "climbra.db"),
        os.path.join(raiz_do_programa, "climbra.db"),
        os.path.join(os.getcwd(), "data", "climbra.db"),
        os.path.join(os.getcwd(), "climbra.db"),
    ]
    for cand in candidates:
        if cand and os.path.isfile(cand):
            _DB_PATH_CACHE = os.path.abspath(cand)
            return _DB_PATH_CACHE

    return None


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

    # 1. Prioriza o banco SQLite compilado (climbra.db)
    db_path = get_climate_db_path()
    if db_path:
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute("SELECT city_norm, city FROM climbra_cities;")
            for norm, city in cur.fetchall():
                city_map[norm] = city
            conn.close()
            if city_map:
                _CITY_FILENAME_MAP = city_map
                return city_map
        except Exception:
            pass

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
    Carrega a série diária de chuva da Base Nacional (priorizando climbra.db),
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

    # 1. Tenta carregar do banco SQLite compilado climbra.db
    db_path = get_climate_db_path()
    if db_path:
        try:
            import sqlite3
            import zlib
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()
            cur.execute(
                "SELECT count, data FROM climbra_series WHERE city = ? AND model = ? AND scenario = ?;",
                (matched_city, model_name, scenario_key),
            )
            row = cur.fetchone()
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
