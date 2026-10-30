# -*- coding: utf-8 -*-
"""Move a tabela ``qualidade`` (derivada do Iberia01, ODbL) de ``data/portugal_eobs.db`` para ``data/qualidade_eobs_odbl.db``.

Decisão do titular de 25/10/2026: a tabela derivada do Iberia01 fica num ficheiro separado do programa, sob ODbL, com
atribuição. A E-OBS (``portugal_eobs.db``) fica só com as séries. O número de locais de Espanha passa a ser a contagem
real de ``ibe_unidades.db`` (e não 0). Idempotente: se a tabela já foi movida, não faz nada.

    python scripts/separar_qualidade_odbl.py
"""
import sqlite3
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
EOBS, SAIDA, UNIDADES = DATA / "portugal_eobs.db", DATA / "qualidade_eobs_odbl.db", DATA / "ibe_unidades.db"
CHAVES = ("qualidade_versao", "qualidade_referencia", "limiares", "espanha_locais")
AVISO = "Contains information from Iberia01, made available under the Open Database License (ODbL 1.0)."
CITACAO = ("Herrera, S., Cardoso, R. M., Soares, P. M. M., Espírito-Santo, F., Viterbo, P., Gutiérrez, J. M. (2019). "
           "Iberia01: a new gridded dataset of daily precipitation and temperatures over Iberia. Earth System Science "
           "Data, 11, 1947-1956. doi:10.5194/essd-11-1947-2019")


def main():
    src = sqlite3.connect(EOBS)
    if not src.execute("SELECT 1 FROM sqlite_master WHERE name = 'qualidade'").fetchone():
        print("A tabela qualidade já não está em portugal_eobs.db.")
        return
    SAIDA.unlink(missing_ok=True)
    dst = sqlite3.connect(SAIDA)
    dst.execute(src.execute("SELECT sql FROM sqlite_master WHERE name = 'qualidade'").fetchone()[0])
    dst.executemany("INSERT INTO qualidade VALUES (?,?,?,?,?,?,?,?,?)", src.execute("SELECT * FROM qualidade").fetchall())
    dst.execute("CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT)")
    meta = dict(src.execute("SELECT chave, valor FROM metadados"))
    espanha = "0"
    if UNIDADES.exists():
        espanha = dict(sqlite3.connect(UNIDADES).execute("SELECT chave, valor FROM metadados"))["espanha_locais"]
    linhas = {k: meta[k] for k in CHAVES if k in meta}
    linhas["espanha_locais"] = espanha
    linhas.update({"licenca": "ODbL 1.0", "citacao": CITACAO, "aviso": AVISO,
                   "nota": "Derivada do Iberia01 (diferença E-OBS menos Iberia01, 1971-2000). Ficheiro separado do programa, sob ODbL."})
    dst.executemany("INSERT INTO metadados VALUES (?,?)", linhas.items())
    dst.commit()
    dst.close()
    src.execute("DROP TABLE qualidade")
    src.executemany("DELETE FROM metadados WHERE chave = ?", [(k,) for k in CHAVES])
    src.commit()
    src.execute("VACUUM")
    src.close()
    print(f"{SAIDA.name}: {SAIDA.stat().st_size / 1024:.0f} KiB; {EOBS.name}: {EOBS.stat().st_size / 2 ** 20:.2f} MiB; "
          f"Espanha: {espanha} locais")


if __name__ == "__main__":
    sys.exit(main())
