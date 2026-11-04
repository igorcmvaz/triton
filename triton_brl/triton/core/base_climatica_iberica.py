# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo base_climatica_iberica.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.climate.base_climatica_iberica`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.climate.base_climatica_iberica import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.climate.base_climatica_iberica")
