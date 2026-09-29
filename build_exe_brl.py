"""
Script de Compilação do Netuno 5 — Edição Brasil (Netuno_5_BRL).
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import build_exe

if __name__ == "__main__":
    sys.argv = [sys.argv[0], "--edition=brl"] + [a for a in sys.argv[1:] if not a.startswith("--edition")]
    build_exe.main()
