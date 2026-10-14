"""
Ponto de Entrada da Edição Brasil (Triton BRL).
Inclui CLIMBra nacional, catálogo de 652 municípios e tarifas auditadas.
"""

import os
import sys

os.environ["TRITON_EDITION"] = "BRL"

from main import main

if __name__ == "__main__":
    main()
