# -*- coding: utf-8 -*-
"""Fachada de retrocompatibilidade para o módulo study_layout.

O código canônico deste módulo foi organizado no subdomínio correspondente:
    `triton.core.reporting.study_layout`

Todas as exportações são preservadas com identidade de objeto para garantir
100% de compatibilidade com testes, scripts legados e interfaces gráficas.
"""
import sys
import importlib
from triton.core.reporting.study_layout import *  # noqa: F401, F403

sys.modules[__name__] = importlib.import_module("triton.core.reporting.study_layout")
