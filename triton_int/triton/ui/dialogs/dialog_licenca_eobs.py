# -*- coding: utf-8 -*-
"""Aviso de licença da E-OBS, no primeiro arranque da edição IBE/PRT (uma vez por instalação).

Duas respostas, sem terceira por defeito: «uso de pesquisa ou educação» e «uso comercial». A escolha
fica na configuração do utilizador (``triton.core.licenca_eobs``). Os textos estão em português de
Portugal e não passam pelo catálogo ``tr``: a edição é em português, e a licença vale em qualquer língua.
"""
from __future__ import annotations

from PySide6.QtWidgets import QMessageBox

from triton.core import licenca_eobs as L


def montar_aviso(parent=None) -> tuple:
    """A caixa e os dois botões (pesquisa, comercial), sem a mostrar. Serve também aos testes."""
    caixa = QMessageBox(parent)
    caixa.setIcon(QMessageBox.Information)
    caixa.setWindowTitle(L.TITULO_DO_AVISO)
    caixa.setText(L.texto_do_aviso())
    b_pesquisa = caixa.addButton(L.RESPOSTAS[L.USO_PESQUISA], QMessageBox.AcceptRole)
    b_comercial = caixa.addButton(L.RESPOSTAS[L.USO_COMERCIAL], QMessageBox.ActionRole)
    return caixa, b_pesquisa, b_comercial


def perguntar_uso(parent=None, armazem=None):
    """Mostra o aviso e grava a resposta. Devolve 'pesquisa', 'comercial' ou None (fechou sem escolher)."""
    caixa, b_pesquisa, b_comercial = montar_aviso(parent)
    caixa.exec()
    clicado = caixa.clickedButton()
    uso = L.USO_PESQUISA if clicado is b_pesquisa else L.USO_COMERCIAL if clicado is b_comercial else None
    if uso is None:
        return None
    L.gravar_escolha(uso, armazem)
    depois = L.texto_depois_da_escolha(uso)
    if depois:
        QMessageBox.warning(parent, L.TITULO_DO_AVISO, depois)
    return uso


def perguntar_uso_se_necessario(parent=None, armazem=None):
    """No primeiro arranque da edição com a E-OBS: pergunta uma vez. Nas outras edições, não faz nada."""
    if not L.precisa_perguntar(armazem):
        return None
    return perguntar_uso(parent, armazem)
