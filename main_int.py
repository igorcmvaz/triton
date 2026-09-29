"""
Ponto de Entrada da Edição Internacional (Netuno 5 INT).
Entrada direta de dados pluviométricos (modo personalizado padrão) e parâmetros editáveis.
"""

import os
import sys

os.environ["NETUNO_EDITION"] = "INT"

from main import main

if __name__ == "__main__":
    main()
