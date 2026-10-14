"""
Ponto de Entrada da Edição Portugal (Triton POR).
Português de Portugal, valores em euros; precipitação por concelho e tarifários portugueses.
"""

import os
import sys

os.environ["TRITON_EDITION"] = "POR"

from main import main

if __name__ == "__main__":
    main()
