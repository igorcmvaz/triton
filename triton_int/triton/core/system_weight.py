# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo system_weight.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.system.system_weight`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.system.system_weight import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.system.system_weight")
