# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo chlorination.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.hydrology.chlorination`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.hydrology.chlorination import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.hydrology.chlorination")
