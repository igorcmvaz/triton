# -*- coding: utf-8 -*-
"""Gera os projetos de exemplo da Edição Portugal (Lisboa, Porto e Funchal).

Nome antigo, mantido para quem ainda o chama: o gerador é ``gerar_exemplos_prt.py``.

    python scripts/gerar_exemplo_portugal.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gerar_exemplos_prt import gerar  # noqa: E402

if __name__ == "__main__":
    gerar()
