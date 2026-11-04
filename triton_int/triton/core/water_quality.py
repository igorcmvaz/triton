# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo water_quality.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.hydrology.water_quality`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.hydrology.water_quality import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.hydrology.water_quality")
