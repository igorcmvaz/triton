# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo pressurizer_catalog.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.hydraulics.pressurizer_catalog`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.hydraulics.pressurizer_catalog import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.hydraulics.pressurizer_catalog")
