"""
Módulo de Acesso e Gerenciamento da Base Climatológica Nacional (CMIP6 / Netuno).

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


def _normalize_name(name: str) -> str:
    """Normaliza nome removendo acentos, pontuações e espaços para indexação segura."""
    if not name:
        return ""
    nfkd = unicodedata.normalize("NFD", str(name))
    cleaned = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return cleaned.lower().replace(" ", "").replace("-", "").replace("'", "").replace("_", "")


def get_climate_database_dir() -> str:
    """Localiza o diretório raiz das séries temporais da base de 652 cidades."""
    global _BASE_DIR_CACHE
    if _BASE_DIR_CACHE and os.path.isdir(_BASE_DIR_CACHE):
        return _BASE_DIR_CACHE

    # Ordem de busca, da mais específica para a mais genérica.
    #
    # A primeira entrada é a localização canônica: a base climática fica na raiz do
    # programa, ao lado do pacote `netuno`. As demais existem para execução a partir
    # de outro diretório de trabalho (scripts de estudo) e para instalações que
    # optem por mantê-la sob `data/`.
    #
    # A variável de ambiente NETUNO_CLIMATE_DATA_DIR tem precedência sobre todas,
    # para instalações que guardem os ~6,5 GB fora da árvore do programa.
    raiz_do_programa = os.path.join(os.path.dirname(__file__), "..", "..")
    # No programa instalado, o código fica em _internal\netuno; a base é
    # instalada ao lado do executável, na pasta do programa.
    import sys
    pasta_do_executavel = (os.path.dirname(sys.executable)
                           if getattr(sys, "frozen", False) else "")
    candidates = [
        os.environ.get("NETUNO_CLIMATE_DATA_DIR", ""),
        os.path.join(pasta_do_executavel, "Netuno future files for 652 cities") if pasta_do_executavel else "",
        os.path.join(raiz_do_programa, "Netuno future files for 652 cities"),
        os.path.join(os.getcwd(), "Netuno future files for 652 cities"),
        os.path.join(raiz_do_programa, "data", "Netuno future files for 652 cities"),
        os.path.join(os.getcwd(), "data", "Netuno future files for 652 cities"),
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
    """Cria um mapa dos nomes normalizados das cidades para os nomes reais de arquivo."""
    global _CITY_FILENAME_MAP
    if _CITY_FILENAME_MAP is not None:
        return _CITY_FILENAME_MAP

    city_map = {}
    base_dir = get_climate_database_dir()
    if os.path.isdir(base_dir):
        try:
            for fname in os.listdir(base_dir):
                if fname.startswith("(Netuno)") and fname.endswith(".csv"):
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
        f"(Netuno){matched_city}_{model_name}_{suffix}",
    ]
    if "Histórico" in suffix:
        direct_candidates.append(f"(Netuno){matched_city}_{model_name}_Historico.csv")

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
            if not fname.startswith("(Netuno)") or not fname.endswith(".csv"):
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
    Carrega a série diária de chuva da Base Nacional, aplicando recorte de datas opcional.

    Retorna:
    - precip_data: np.ndarray com precipitação diária em mm
    - eff_start_date: string "dd/mm/aaaa" da data inicial efetiva do recorte
    - eff_end_date: string "dd/mm/aaaa" da data final efetiva do recorte
    - total_days_file: total de dias disponíveis no arquivo original
    - selected_days: quantidade de dias selecionados após o recorte
    - file_path: caminho absoluto do arquivo carregado
    """
    file_path = get_climate_file_path(city_name, model_name, scenario_key)
    if not file_path or not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Arquivo de série climatológica não encontrado para a cidade '{city_name}', "
            f"modelo '{model_name}' e cenário '{scenario_key}'."
        )

    scenario_info = CLIMATE_SCENARIOS.get(scenario_key, CLIMATE_SCENARIOS["HIST"])
    base_start_date = parse_date_str(scenario_info["start_date"], datetime(1980, 1, 1))

    # Leitura rápida de precipitação diária
    raw_data: List[float] = []
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_s = line.strip()
            if not line_s:
                continue
            try:
                val = float(line_s.replace(",", "."))
                raw_data.append(max(0.0, val))
            except ValueError:
                # Possível cabeçalho textual na primeira linha
                continue

    if not raw_data:
        raise ValueError(f"O arquivo '{file_path}' não contém dados válidos de precipitação.")

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

    sliced_data = np.array(raw_data[idx_start:idx_end], dtype=np.float64)
    selected_days = len(sliced_data)

    eff_start_date_str = eff_start.strftime("%d/%m/%Y")
    eff_end_date_str = (eff_start + timedelta(days=selected_days - 1)).strftime("%d/%m/%Y")

    return (
        sliced_data,
        eff_start_date_str,
        eff_end_date_str,
        total_days_file,
        selected_days,
        file_path,
    )
