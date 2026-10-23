# -*- coding: utf-8 -*-
"""O menu Ajuda abre o relatório de verificação, e não o aviso de ausência.

O diálogo procurava um arquivo de nome antigo e mostrava sempre «relatório
de validação não encontrado». O teste garante que o caminho resolvido existe.
"""

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
pytest.importorskip("PySide6")


@pytest.mark.parametrize("sufixo", ["", "_en"])
def test_o_relatorio_de_verificacao_e_encontrado(sufixo):
    from triton.ui.dialogs.dialog_validation_report import caminho_do_relatorio
    caminho = caminho_do_relatorio(sufixo)
    assert caminho is not None
    assert caminho.exists()
    assert "Verificação" in caminho.read_text(encoding="utf-8")[:200]
