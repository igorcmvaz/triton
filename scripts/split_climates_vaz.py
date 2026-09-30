"""
Script para separação dos arquivos climáticos de cenários futuros (CMIP6 / CLIMBra)
em 3 horizontes temporais para o estudo de tipologias de Vaz:
 - Near Future:   1 de Janeiro de 2015 a 31 de Dezembro de 2044 (30 anos = 10.958 dias)
 - Middle Future: 1 de Janeiro de 2045 a 31 de Dezembro de 2074 (30 anos = 10.957 dias)
 - Far Future:    1 de Janeiro de 2075 a 31 de Dezembro de 2100 (26 anos = 9.496 dias)

Séries Históricas (1980–2013) permanecem íntegras (12.419 dias).
Os arquivos resultantes são gravados na pasta de destino 'TesteMassivo/Netuno_vaz_files_split'.
"""

import os
import sys
import glob
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

NEAR_DAYS = 10958    # 2015-01-01 a 2044-12-31
MIDDLE_DAYS = 10957  # 2045-01-01 a 2074-12-31
FAR_DAYS = 9496      # 2075-01-01 a 2100-12-31 (Total = 31.411 dias)

_proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_INPUT_DIR = os.path.join(_proj_root, "climbra_data")
if not os.path.isdir(DEFAULT_INPUT_DIR):
    _legacy_root = os.path.join(_proj_root, "Netuno future files for 652 cities")
    if os.path.isdir(_legacy_root):
        DEFAULT_INPUT_DIR = _legacy_root
    else:
        DEFAULT_INPUT_DIR = os.path.join(_proj_root, "Replicacao_Projected", "Netuno future files for 652 cities")

DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "estudo_5_tipologias_residenciais",
    "Netuno_vaz_files_split"
)


def _process_climate_file_vaz(args_tuple):
    file_path, output_dir = args_tuple
    fname = os.path.basename(file_path)

    # Se for arquivo Histórico, basta copiar
    if "Histórico" in fname or "Historico" in fname:
        out_path = os.path.join(output_dir, fname)
        shutil.copy2(file_path, out_path)
        return fname, "copied", 1

    # Se for arquivo futuro (SSP245 ou SSP585)
    if "SSP245" in fname or "SSP585" in fname:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [line.strip() for line in f if line.strip()]

        if len(lines) < NEAR_DAYS + MIDDLE_DAYS + FAR_DAYS:
            val_lines = [l for l in lines if not l.startswith("Data") and not l.startswith("#")]
        else:
            val_lines = lines

        near_lines = val_lines[:NEAR_DAYS]
        middle_lines = val_lines[NEAR_DAYS:NEAR_DAYS + MIDDLE_DAYS]
        far_lines = val_lines[NEAR_DAYS + MIDDLE_DAYS:NEAR_DAYS + MIDDLE_DAYS + FAR_DAYS]

        # Nomes dos arquivos de saída
        if "SSP245" in fname:
            fname_near = fname.replace("SSP245.csv", "SSP245_Near.csv").replace("SSP245.txt", "SSP245_Near.txt")
            fname_middle = fname.replace("SSP245.csv", "SSP245_Middle.csv").replace("SSP245.txt", "SSP245_Middle.txt")
            fname_far = fname.replace("SSP245.csv", "SSP245_Far.csv").replace("SSP245.txt", "SSP245_Far.txt")
        else:
            fname_near = fname.replace("SSP585.csv", "SSP585_Near.csv").replace("SSP585.txt", "SSP585_Near.txt")
            fname_middle = fname.replace("SSP585.csv", "SSP585_Middle.csv").replace("SSP585.txt", "SSP585_Middle.txt")
            fname_far = fname.replace("SSP585.csv", "SSP585_Far.csv").replace("SSP585.txt", "SSP585_Far.txt")

        # Fallback de segurança se replace não alterar extensão
        if fname_near == fname:
            base, ext = os.path.splitext(fname)
            fname_near = f"{base}_Near{ext}"
            fname_middle = f"{base}_Middle{ext}"
            fname_far = f"{base}_Far{ext}"

        path_near = os.path.join(output_dir, fname_near)
        path_middle = os.path.join(output_dir, fname_middle)
        path_far = os.path.join(output_dir, fname_far)

        with open(path_near, "w", encoding="utf-8") as f:
            f.write("\n".join(near_lines) + "\n")

        with open(path_middle, "w", encoding="utf-8") as f:
            f.write("\n".join(middle_lines) + "\n")

        with open(path_far, "w", encoding="utf-8") as f:
            f.write("\n".join(far_lines) + "\n")

        return fname, "split", 3

    # Outros arquivos desconhecidos
    out_path = os.path.join(output_dir, fname)
    shutil.copy2(file_path, out_path)
    return fname, "copied", 1


def split_climates_vaz(input_dir=None, output_dir=None, num_workers=None):
    if input_dir is None:
        input_dir = DEFAULT_INPUT_DIR
        if not os.path.exists(input_dir) or len(glob.glob(os.path.join(input_dir, "*.csv"))) == 0:
            for alt_name in ["climbra_data", "Netuno future files for 652 cities"]:
                alt_dir = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "Teste_ArtigoNovo",
                    alt_name
                )
                if os.path.exists(alt_dir):
                    input_dir = alt_dir
                    break

    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    files = sorted(glob.glob(os.path.join(input_dir, "*.csv")) + glob.glob(os.path.join(input_dir, "*.txt")))
    if not files:
        print(f"[ERRO] Nenhum arquivo encontrado em: {input_dir}")
        return

    print("=" * 80)
    print("SEPARAÇÃO DE SÉRIES CLIMÁTICAS FUTURAS (VAZ): NEAR, MIDDLE E FAR FUTURE")
    print("=" * 80)
    print(f" [+] Pasta de Origem: {input_dir}")
    print(f" [+] Pasta de Destino: {output_dir}")
    print(f" [*] Total de Arquivos Brutos: {len(files):,}")

    if num_workers is None:
        num_workers = min(os.cpu_count() or 4, 16)

    print(f" [*] Processando em paralelo ({num_workers} workers)...")
    start_time = time.time()

    tasks = [(f, output_dir) for f in files]
    total_generated = 0
    split_count = 0
    copied_count = 0

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(_process_climate_file_vaz, t): t for t in tasks}
        completed = 0
        for future in as_completed(futures):
            completed += 1
            fname, status, count = future.result()
            total_generated += count
            if status == "split":
                split_count += 1
            else:
                copied_count += 1

            if completed % 5000 == 0 or completed == len(files):
                elapsed = time.time() - start_time
                pct = (completed / len(files)) * 100
                rate = completed / elapsed if elapsed > 0 else 0
                print(f"  Progresso: {completed:,}/{len(files):,} [{pct:.1f}%] | {rate:.1f} arq/s | Gerados: {total_generated:,}")

    elapsed_total = time.time() - start_time
    print("=" * 80)
    print(f"[OK] SEPARAÇÃO CONCLUÍDA EM {elapsed_total:.2f} SEGUNDOS!")
    print(f"     Arquivos Brutos Processados: {len(files):,}")
    print(f"     Séries Divididas (Near/Middle/Far): {split_count:,}")
    print(f"     Séries Históricas Copiadas: {copied_count:,}")
    print(f"     Total de Séries de Saída Prontas: {total_generated:,}")
    print(f"     Pasta: {output_dir}")
    print("=" * 80)


if __name__ == "__main__":
    split_climates_vaz()
