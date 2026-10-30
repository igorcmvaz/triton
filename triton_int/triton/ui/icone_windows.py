# -*- coding: utf-8 -*-
"""Ícone da janela na barra de tarefas do Windows, independente do plugin de imagens do Qt.

O Qt já usa o ``QIcon`` da aplicação; este módulo grava o ícone também pelo Win32
(``WM_SETICON`` com os tamanhos que o Windows pede), de modo que a barra de tarefas e o
Alt+Tab o mostrem mesmo quando o ``QIcon`` sair vazio no programa instalado.
"""
from __future__ import annotations

import os
import sys

_CONSERVADOS: list = []  # as alças vivem enquanto o programa roda


def _caminho_do_icone() -> str | None:
    from triton.ui.translation import get_resource_path
    for nome in ("triton.ico", "icon.ico"):
        caminho = get_resource_path(os.path.join("icons", nome))
        if os.path.isfile(caminho):
            return caminho
    return None


def aplicar_icone_da_janela(janela) -> bool:
    """Define o ícone grande e o pequeno da janela via Win32; ``False`` fora do Windows ou se falhar."""
    if not sys.platform.startswith("win"):
        return False
    try:
        import ctypes
        from ctypes import wintypes
        caminho = _caminho_do_icone()
        if caminho is None:
            return False
        usuario = ctypes.windll.user32
        usuario.LoadImageW.restype = wintypes.HANDLE
        usuario.LoadImageW.argtypes = [wintypes.HINSTANCE, wintypes.LPCWSTR, wintypes.UINT,
                                       ctypes.c_int, ctypes.c_int, wintypes.UINT]
        usuario.SendMessageW.argtypes = [wintypes.HWND, wintypes.UINT, wintypes.WPARAM, wintypes.LPARAM]
        hwnd = int(janela.winId())
        image_icon, load_from_file = 1, 0x0010
        wm_seticon, icon_small, icon_big = 0x0080, 0, 1
        ok = False
        for papel, cx, cy in ((icon_big, usuario.GetSystemMetrics(11), usuario.GetSystemMetrics(12)),
                              (icon_small, usuario.GetSystemMetrics(49), usuario.GetSystemMetrics(50))):
            alca = usuario.LoadImageW(None, caminho, image_icon, cx, cy, load_from_file)
            if alca:
                _CONSERVADOS.append(alca)
                usuario.SendMessageW(hwnd, wm_seticon, papel, alca)
                ok = True
        return ok
    except Exception:
        return False
