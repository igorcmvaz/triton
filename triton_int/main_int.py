"""
Ponto de Entrada da Edição Internacional (Triton INT).
Entrada direta de dados pluviométricos (modo personalizado padrão) e parâmetros editáveis.
"""

import os
import sys

os.environ["TRITON_EDITION"] = "INT"

from main import main

if __name__ == "__main__":
    main()
