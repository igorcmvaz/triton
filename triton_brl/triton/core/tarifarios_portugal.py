# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo tarifarios_portugal.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.tariffs.tarifarios_portugal`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.tariffs.tarifarios_portugal import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.tariffs.tarifarios_portugal")
