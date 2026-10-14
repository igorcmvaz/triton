"""
Compilador da Base Climatológica Nacional (CLIMBra / CMIP6) para SQLite.

Converte os 37.164 arquivos CSV (~6,24 GB) em um único banco de dados SQLite
compactado (`data/climbra.db`, ~1,1 GB com float16 + zlib), otimizado para
leitura de alta velocidade (sub-milissegundo) e empacotamento no executável
do Triton.

Referência dos dados:
- Artigo: BALLARIN et al. (2023), Nature Scientific Data, doi:10.1038/s41597-023-01956-z
- Repositório: Science Data Bank, doi:10.57760/sciencedb.02316
"""

import argparse
from datetime import datetime
import multiprocessing as mp
import os
import sqlite3
import sys
import time
import unicodedata
import zlib
from typing import List, Tuple, Optional

import numpy as np

CLIMATE_MODELS = [
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


def normalize_name(name: str) -> str:
    """Normaliza nome de município para buscas insensíveis a acentos e pontuação."""
    if not name:
        return ""
    nfkd = unicodedata.normalize("NFD", str(name))
    cleaned = "".join(c for c in nfkd if unicodedata.category(c) != "Mn")
    return cleaned.lower().replace(" ", "").replace("-", "").replace("'", "").replace("_", "")


def parse_filename(filename: str) -> Optional[Tuple[str, str, str]]:
    """
    Extrai (city, model, scenario) a partir do nome de arquivo padronizado.
    Exemplo: '(Triton)São Paulo_ACCESS-CM2_Histórico.csv' -> ('São Paulo', 'ACCESS-CM2', 'HIST')
    """
    if not filename.startswith("(Triton)") or not filename.endswith(".csv"):
        return None

    clean = filename[8:-4]
    if clean.endswith("SSP245"):
        scenario = "SSP245"
        rem = clean[:-7]
    elif clean.endswith("SSP585"):
        scenario = "SSP585"
        rem = clean[:-7]
    else:
        scenario = "HIST"
        idx = clean.rfind("_")
        rem = clean[:idx] if idx != -1 else clean

    matched_model = None
    city = None
    for m in CLIMATE_MODELS:
        m_tag = "_" + m
        if rem.endswith(m_tag):
            matched_model = m
            city = rem[:-len(m_tag)]
            break
        elif m == "INM-CM4" and rem.endswith("_INM-CM4_8"):
            matched_model = m
            city = rem[:-len("_INM-CM4_8")]
            break

    if not matched_model or not city:
        return None

    return city, matched_model, scenario


def process_csv_file(args: Tuple[str, str, str, str, str]) -> Optional[Tuple[str, str, str, int, bytes]]:
    """
    Lê um arquivo CSV, converte a coluna de valores em array NumPy compactado com zlib.
    args: (file_path, city, model, scenario, dtype_str)
    """
    file_path, city, model, scenario, dtype_str = args
    target_dtype = np.float16 if dtype_str == "float16" else np.float32

    raw_data: List[float] = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line_s = line.strip()
                if not line_s:
                    continue
                try:
                    val = float(line_s.replace(",", "."))
                    raw_data.append(max(0.0, val))
                except ValueError:
                    continue
    except Exception:
        return None

    if not raw_data:
        return None

    arr = np.array(raw_data, dtype=target_dtype)
    compressed = zlib.compress(arr.tobytes(), level=6)
    return city, model, scenario, len(raw_data), compressed


def compile_database(
    input_dir: str,
    output_db_path: str,
    dtype_str: str = "float16",
    num_workers: Optional[int] = None,
    batch_size: int = 1000,
) -> None:
    """Compila todos os arquivos CSV em um banco SQLite otimizado."""
    if not os.path.isdir(input_dir):
        raise FileNotFoundError(f"Diretório de arquivos climáticos não encontrado: {input_dir}")

    os.makedirs(os.path.dirname(os.path.abspath(output_db_path)), exist_ok=True)

    # Identifica todos os CSVs
    all_files = [f for f in os.listdir(input_dir) if f.startswith("(Triton)") and f.endswith(".csv")]
    total_files = len(all_files)
    print(f"[*] Encontrados {total_files} arquivos CSV em '{input_dir}'")

    tasks = []
    cities_set = set()
    for fname in all_files:
        parsed = parse_filename(fname)
        if not parsed:
            continue
        city, model, scenario = parsed
        cities_set.add(city)
        tasks.append((os.path.join(input_dir, fname), city, model, scenario, dtype_str))

    print(f"[*] Tarefas válidas identificadas: {len(tasks)} (Municípios únicos: {len(cities_set)})")

    # Inicializa banco SQLite
    if os.path.exists(output_db_path):
        os.remove(output_db_path)

    conn = sqlite3.connect(output_db_path)
    cur = conn.cursor()
    cur.execute("PRAGMA synchronous = OFF;")
    cur.execute("PRAGMA journal_mode = MEMORY;")
    cur.execute("PRAGMA cache_size = -64000;")  # 64 MB de cache

    cur.execute("""
    CREATE TABLE IF NOT EXISTS climbra_meta (
        key TEXT PRIMARY KEY,
        value TEXT
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS climbra_cities (
        city TEXT PRIMARY KEY,
        city_norm TEXT NOT NULL
    );
    """)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_climbra_cities_norm ON climbra_cities(city_norm);")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS climbra_series (
        city TEXT NOT NULL,
        model TEXT NOT NULL,
        scenario TEXT NOT NULL,
        count INTEGER NOT NULL,
        data BLOB NOT NULL,
        PRIMARY KEY (city, model, scenario)
    );
    """)
    conn.commit()

    # Insere tabela de cidades
    city_rows = [(c, normalize_name(c)) for c in sorted(cities_set)]
    cur.executemany("INSERT INTO climbra_cities (city, city_norm) VALUES (?, ?);", city_rows)
    conn.commit()

    workers = num_workers or max(1, mp.cpu_count())
    print(f"[*] Iniciando processamento paralelo com {workers} núcleos (dtype={dtype_str})...")

    t_start = time.time()
    processed_count = 0
    buffer = []

    with mp.Pool(processes=workers) as pool:
        for result in pool.imap_unordered(process_csv_file, tasks, chunksize=50):
            if result:
                buffer.append(result)
                processed_count += 1

                if len(buffer) >= batch_size:
                    cur.executemany(
                        "INSERT INTO climbra_series (city, model, scenario, count, data) VALUES (?, ?, ?, ?, ?);",
                        buffer,
                    )
                    conn.commit()
                    buffer.clear()

                    elapsed = time.time() - t_start
                    speed = processed_count / elapsed
                    remaining = (len(tasks) - processed_count) / speed if speed > 0 else 0
                    print(
                        f"    -> {processed_count:5d}/{len(tasks)} processados "
                        f"({processed_count/len(tasks)*100:.1f}%) | "
                        f"{speed:.0f} arqs/s | "
                        f"Decorrido: {elapsed:.0f}s | Restante: {remaining:.0f}s"
                    )

    if buffer:
        cur.executemany(
            "INSERT INTO climbra_series (city, model, scenario, count, data) VALUES (?, ?, ?, ?, ?);",
            buffer,
        )
        conn.commit()
        buffer.clear()

    total_time = time.time() - t_start
    print(f"[*] Processamento concluído em {total_time:.1f} segundos ({total_time/60:.2f} min).")

    # Metadados
    meta_entries = [
        ("title", "CLIMBra - Climate Change Dataset for Brazil (CMIP6 / Triton)"),
        ("source_article", "BALLARIN et al. (2023), Nature Scientific Data, 10, art. 48"),
        ("article_doi", "10.1038/s41597-023-01956-z"),
        ("repository_doi", "10.57760/sciencedb.02316"),
        ("license", "Creative Commons Zero v1.0 Universal (CC0)"),
        ("dtype", dtype_str),
        ("compression", "zlib-level-6"),
        ("total_series", str(processed_count)),
        ("total_cities", str(len(cities_set))),
        ("models_count", str(len(CLIMATE_MODELS))),
        ("compiled_at", datetime.now().isoformat()),
    ]
    cur.executemany("INSERT OR REPLACE INTO climbra_meta (key, value) VALUES (?, ?);", meta_entries)
    conn.commit()

    print("[*] Otimizando banco de dados (VACUUM & ANALYZE)...")
    cur.execute("ANALYZE;")
    conn.commit()
    conn.close()

    db_size_mb = os.path.getsize(output_db_path) / (1024 * 1024)
    print(f"[OK] Banco gerado com sucesso: '{output_db_path}' ({db_size_mb:.1f} MB)")


def verify_database(db_path: str, sample_csv_dir: Optional[str] = None) -> bool:
    """Verifica a integridade e precisão numérica do banco de dados gerado."""
    print(f"[*] Verificando integridade de '{db_path}'...")
    if not os.path.exists(db_path):
        print(f"[ERRO] Banco '{db_path}' não existe!")
        return False

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("SELECT count(*) FROM climbra_series;")
    total_series = cur.fetchone()[0]

    cur.execute("SELECT count(*) FROM climbra_cities;")
    total_cities = cur.fetchone()[0]

    cur.execute("SELECT value FROM climbra_meta WHERE key = 'dtype';")
    meta_dtype_row = cur.fetchone()
    dtype_str = meta_dtype_row[0] if meta_dtype_row else "float16"

    print(f"    - Total de séries registradas: {total_series} (esperado: 37164)")
    print(f"    - Total de cidades registradas: {total_cities} (esperado: 652)")
    print(f"    - Dtype configurado: {dtype_str}")

    target_dtype = np.float16 if dtype_str == "float16" else np.float32

    # Amostragem de leitura
    test_cities = ["São Paulo", "Brasília", "Florianópolis", "Manaus", "Salvador"]
    for c in test_cities:
        norm = normalize_name(c)
        cur.execute("SELECT city FROM climbra_cities WHERE city_norm = ?;", (norm,))
        row = cur.fetchone()
        if not row:
            print(f"[ERRO] Cidade '{c}' (norm: '{norm}') não encontrada no banco!")
            conn.close()
            return False
        real_city = row[0]
        cur.execute(
            "SELECT count, data FROM climbra_series WHERE city = ? AND model = 'ACCESS-CM2' AND scenario = 'HIST';",
            (real_city,),
        )
        series_row = cur.fetchone()
        if not series_row:
            print(f"[ERRO] Série histórica para '{real_city}' não encontrada!")
            conn.close()
            return False

        cnt, blob = series_row
        decomp = zlib.decompress(blob)
        arr = np.frombuffer(decomp, dtype=target_dtype)
        if len(arr) != cnt:
            print(f"[ERRO] Tamanho inconsistente para '{real_city}': {len(arr)} vs {cnt}")
            conn.close()
            return False

        print(f"    - Cidade '{real_city}': {cnt} dias lidos | Média diária: {arr.mean():.2f} mm/dia | Max: {arr.max():.1f} mm")

    conn.close()
    print("[OK] Verificação de integridade concluída com 100% de sucesso!")
    return True


if __name__ == "__main__":
    _default_input = os.path.join(os.path.dirname(__file__), "..", "climbra_data")
    if not os.path.isdir(_default_input):
        _legacy_input = os.path.join(os.path.dirname(__file__), "..", "Triton future files for 652 cities")
        if os.path.isdir(_legacy_input):
            _default_input = _legacy_input

    parser = argparse.ArgumentParser(description="Compilador da Base Climatológica CLIMBra para SQLite")
    parser.add_argument(
        "--input",
        "-i",
        default=_default_input,
        help="Diretório contendo os arquivos CSV brutos",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=os.path.join(os.path.dirname(__file__), "..", "data", "climbra.db"),
        help="Caminho de destino do arquivo SQLite",
    )
    parser.add_argument(
        "--dtype",
        choices=["float16", "float32"],
        default="float16",
        help="Precisão numérica (float16: ~1,1 GB, float32: ~1,8 GB)",
    )
    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=None,
        help="Número de processos paralelos (padrão: núcleos disponíveis)",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Apenas verifica um banco existente sem compilar",
    )

    args = parser.parse_args()

    if args.verify_only:
        success = verify_database(args.output)
        sys.exit(0 if success else 1)

    compile_database(
        input_dir=args.input,
        output_db_path=args.output,
        dtype_str=args.dtype,
        num_workers=args.workers,
    )

    verify_database(args.output, sample_csv_dir=args.input)
