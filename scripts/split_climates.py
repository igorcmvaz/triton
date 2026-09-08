"""
Script para separação dos arquivos climáticos de cenários futuros (CMIP6 / CLIMBra)
em dois horizontes temporais conforme Tabela 1:
 - Near Future: 1 de Janeiro de 2015 a 31 de Dezembro de 2059 (16.436 dias)
 - Far Future:  1 de Janeiro de 2060 a 31 de Dezembro de 2100 (14.975 dias)

Séries Históricas (1980–2013) permanecem íntegras (12.419 dias).
Os arquivos resultantes são gravados na pasta de destino organizada.
"""

import os
import sys
import glob
import shutil
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

NEAR_DAYS = 16436  # 2015-01-01 a 2059-12-31
FAR_DAYS = 14975   # 2060-01-01 a 2100-12-31 (Total = 31.411 dias)

DEFAULT_INPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Replicacao_Projected",
    "Netuno future files for 652 cities"
)

DEFAULT_OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "Replicacao_Projected",
    "Netuno_future_files_split"
)


def _process_climate_file(args_tuple):
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

        if len(lines) < NEAR_DAYS + FAR_DAYS:
            # Caso tenha formato com cabeçalho ou linhas em branco
            val_lines = [l for l in lines if not l.startswith("Data") and not l.startswith("#")]
        else:
            val_lines = lines

        near_lines = val_lines[:NEAR_DAYS]
        far_lines = val_lines[NEAR_DAYS:NEAR_DAYS + FAR_DAYS]

        # Nomes dos arquivos de saída
        if "SSP245" in fname:
            fname_near = fname.replace("SSP245.csv", "SSP245_Near.csv").replace("SSP245.txt", "SSP245_Near.txt")
            fname_far = fname.replace("SSP245.csv", "SSP245_Far.csv").replace("SSP245.txt", "SSP245_Far.txt")
        else:
            fname_near = fname.replace("SSP585.csv", "SSP585_Near.csv").replace("SSP585.txt", "SSP585_Near.txt")
            fname_far = fname.replace("SSP585.csv", "SSP585_Far.csv").replace("SSP585.txt", "SSP585_Far.txt")

        # Se a substituição não alterou a extensão (ex: .csv ausente), adiciona o sufixo
        if fname_near == fname:
            base, ext = os.path.splitext(fname)
            scenario = "SSP245" if "SSP245" in fname else "SSP585"
            fname_near = f"{base}_Near{ext}"
            fname_far = f"{base}_Far{ext}"

        path_near = os.path.join(output_dir, fname_near)
        path_far = os.path.join(output_dir, fname_far)

        with open(path_near, "w", encoding="utf-8") as f:
            f.write("\n".join(near_lines) + "\n")

        with open(path_far, "w", encoding="utf-8") as f:
            f.write("\n".join(far_lines) + "\n")

        return fname, "split", 2

    # Outros arquivos desconhecidos
    out_path = os.path.join(output_dir, fname)
    shutil.copy2(file_path, out_path)
    return fname, "copied", 1


def split_climates(input_dir=None, output_dir=None, num_workers=None):
    if input_dir is None:
        input_dir = DEFAULT_INPUT_DIR
    if output_dir is None:
        output_dir = DEFAULT_OUTPUT_DIR

    os.makedirs(output_dir, exist_ok=True)

    files = sorted(glob.glob(os.path.join(input_dir, "*.csv")) + glob.glob(os.path.join(input_dir, "*.txt")))
    if not files:
        print(f"[x] Nenhum arquivo encontrado em: {input_dir}")
        return

    workers = num_workers or os.cpu_count() or 4

    print("=" * 80)
    print("SEPARADOR DE ARQUIVOS CLIMATICOS FUTUROS (NEAR & FAR FUTURE)")
    print("=" * 80)
    print(f" [+] Pasta Origem: {input_dir}")
    print(f" [+] Pasta Destino: {output_dir}")
    print(f" [*] Arquivos para processar: {len(files):,}")
    print(f" [*] Near Future: {NEAR_DAYS:,} dias (2015-01-01 a 2059-12-31)")
    print(f" [*] Far Future:  {FAR_DAYS:,} dias (2060-01-01 a 2100-12-31)")
    print(f" [*] Processamento Paralelo: {workers} nucleos")
    print("=" * 80)

    start_time = time.time()
    total_output_files = 0

    tasks = [(fpath, output_dir) for fpath in files]

    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(_process_climate_file, t) for t in tasks]
        for idx, fut in enumerate(as_completed(futures), start=1):
            _, action, count = fut.result()
            total_output_files += count
            if idx % 100 == 0 or idx == len(files):
                elapsed = time.time() - start_time
                print(f" Progresso: {idx:,}/{len(files):,} [{idx/len(files)*100:.1f}%] | Decorrido: {elapsed:.1f}s")

    elapsed = time.time() - start_time
    print("=" * 80)
    print(f"[OK] SEPARACAO CONCLUIDA EM {elapsed:.2f} SEGUNDOS!")
    print(f"     * Arquivos originais processados: {len(files):,}")
    print(f"     * Total de arquivos gerados na pasta destino: {total_output_files:,}")
    print("=" * 80)


if __name__ == "__main__":
    split_climates()
