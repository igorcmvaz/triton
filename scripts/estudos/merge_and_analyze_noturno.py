"""
=======================================================================================================
NETUNO 5 -- CONSOLIDAÇÃO DOS CHUNKS E GERAÇÃO DAS ANÁLISES DO ESTUDO EXPANDIDO DE 5 TIPOLOGIAS
=======================================================================================================
"""

import os
import sys
import time
import glob
import json
import gc
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "estudo_5_tipologias_residenciais", "estudo_vaz")
CHUNKS_DIR = os.path.join(OUTPUT_DIR, "chunks")
FINAL_PARQUET = os.path.join(OUTPUT_DIR, "estudo_vaz_consolidado.parquet")


def merge_chunks_to_consolidated_parquet():
    print("=" * 90)
    print("NETUNO 5 -- CONSOLIDAÇÃO STREAMING DE CHUNKS PARQUET DO ESTUDO DE 5 TIPOLOGIAS")
    print("=" * 90)

    chunk_files = sorted(glob.glob(os.path.join(CHUNKS_DIR, "*.parquet")))
    print(f" [*] Total de arquivos chunk encontrados: {len(chunk_files):,}")

    if not chunk_files:
        print("[AVISO] Nenhum chunk encontrado para consolidação.")
        return False

    start = time.time()
    first_table = pq.read_table(chunk_files[0])
    canonical_schema = first_table.schema.remove_metadata()
    writer = pq.ParquetWriter(FINAL_PARQUET, canonical_schema, compression="snappy")
    total_rows = 0

    print(" [*] Lendo e integrando chunks em streaming...")
    for i, c_path in enumerate(chunk_files, start=1):
        t = pq.read_table(c_path)
        total_rows += t.num_rows

        if t.schema != canonical_schema:
            try:
                cols = []
                for field in canonical_schema:
                    if field.name in t.column_names:
                        col = t[field.name].cast(field.type)
                    else:
                        col = pa.nulls(t.num_rows, type=field.type)
                    cols.append(col)
                t = pa.Table.from_arrays(cols, schema=canonical_schema)
            except Exception:
                t = t.replace_schema_metadata(None)

        writer.write_table(t)
        del t
        if i % 25 == 0 or i == len(chunk_files):
            gc.collect()
            print(f"  --> Integrado chunk {i:,}/{len(chunk_files):,} | Total acumulado: {total_rows:,} registros", flush=True)

    writer.close()
    del writer
    gc.collect()

    print("=" * 90)
    print(f"[OK] PARQUET CONSOLIDADO GERADO COM SUCESSO EM {time.time() - start:.2f} SEGUNDOS!")
    print(f"[*] Total final de registros: {total_rows:,}")
    print(f"[*] Tamanho do arquivo final: {os.path.getsize(FINAL_PARQUET)/(1024*1024*1024):.2f} GB")
    print("=" * 90)
    return True


if __name__ == "__main__":
    merge_chunks_to_consolidated_parquet()
