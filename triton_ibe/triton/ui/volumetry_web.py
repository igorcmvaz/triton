"""Volumetria 3D na aba do programa, pelo mesmo visualizador do HTML exportado.

O visualizador three.js (``web/volumetria``, empacotado em
``triton/data/volumetria``) roda num ``QWebEngineView``: materiais físicos,
céu HDRI, sombras, corte por cota, medição e fluxo animado, iguais aos do
arquivo que o usuário compartilha.

Sem QtWebEngine, ou com ``TRITON_VOLUMETRIA_SIMPLES=1``, a aba usa o
visualizador em QPainter de :mod:`triton.ui.volumetry_view`, que não depende
de GPU nem de Chromium. :func:`criar_painel_de_volumetria` faz a escolha.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Dict, Optional

from PySide6.QtCore import QUrl, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from triton.core.volumetry import Scene
from triton.core.volumetry_export import VIEWER_BUNDLE, scene_payload, viewer_html
from triton.ui.translation import tr


def textos_da_volumetria() -> Dict[str, str]:
    """Rótulos do visualizador no idioma da interface."""
    return {
        "titulo": tr("Volumetria 3D"),
        "dica": tr("Arraste para girar · botão direito para deslocar · roda para aproximar · duplo clique para focar"),
        "iso": tr("Perspectiva"), "planta": tr("Planta"), "frente": tr("Frente"), "lateral": tr("Lateral"),
        "enquadrar": tr("Enquadrar"), "edificacao": tr("Edificação"), "terreno": tr("Terreno"),
        "rotulos": tr("Rótulos"), "fluxo": tr("Fluxo"), "raiox": tr("Raio-X"), "ceu": tr("Céu"),
        "sombras": tr("Sombras"), "corte": tr("Corte por cota"), "medir": tr("Medir"), "foto": tr("Imagem PNG"),
        "telaCheia": tr("Tela cheia"), "tema": tr("Tema"), "painel": tr("Painel"), "sistemas": tr("Sistemas"),
        "componentes": tr("Componentes"), "ficha": tr("Ficha técnica"), "notas": tr("Notas"),
        "semSelecao": tr("Clique numa peça para ver a ficha técnica."),
        "medirDica": tr("Clique em dois pontos para medir. Esc encerra."), "distancia": tr("Distância"),
        "semWebGL": tr("Este computador não oferece WebGL: a volumetria 3D não pode ser desenhada aqui."),
        "creditos": tr("three.js (MIT) · céu «Quarry» do Poly Haven (CC0)"), "cota": tr("cota"),
    }


def web_disponivel() -> bool:
    """QtWebEngine instalado, pacote do visualizador presente e não desligado."""
    if os.environ.get("TRITON_VOLUMETRIA_SIMPLES", "").strip() not in ("", "0"):
        return False
    if not VIEWER_BUNDLE.is_file():
        return False
    try:
        import PySide6.QtWebEngineWidgets  # noqa: F401
    except Exception:
        return False
    return True


class VolumetryWebPanel(QWidget):
    """Aba da volumetria com o visualizador WebGL. Mesma API de ``VolumetryPanel``."""

    #: O botão «Tela cheia» da página pediu (True) ou deixou (False) a tela cheia.
    tela_cheia_pedida = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        from PySide6.QtWebEngineCore import QWebEngineSettings
        from PySide6.QtWebEngineWidgets import QWebEngineView

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.web = QWebEngineView(self)
        settings = self.web.settings()
        settings.setAttribute(QWebEngineSettings.WebGLEnabled, True)
        settings.setAttribute(QWebEngineSettings.Accelerated2dCanvasEnabled, True)
        # Página local e autocontida: nada de rede.
        settings.setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
        layout.addWidget(self.web)
        # A tela cheia do navegador só funciona se o pedido da página for
        # atendido: aceita e deixa a janela decidir como ocupar a tela.
        settings.setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.web.page().fullScreenRequested.connect(self._tela_cheia)
        self.scene: Optional[Scene] = None
        self._carregado = False      # a página do visualizador está aberta e montada
        self._carregando = False     # há um carregamento em curso
        self._cena_na_pagina: Optional[Scene] = None
        self.reserva = None          # VolumetryPanel, se o WebGL faltar
        self._arquivo = Path(tempfile.gettempdir()) / f"triton_volumetria_{os.getpid()}_{id(self)}.html"
        self.web.loadFinished.connect(self._ao_carregar)

    @property
    def view(self):
        """Compatibilidade com ``VolumetryPanel.view.scene``."""
        return self.reserva.view if self.reserva is not None else self

    def set_scene(self, scene: Optional[Scene]) -> None:
        self.scene = scene
        if self.reserva is not None:
            self.reserva.set_scene(scene)
            return
        if scene is None:
            self._carregado = False
            self._cena_na_pagina = None
            self.web.setHtml("<html><body style='font:14px Segoe UI,sans-serif;color:#64748b;display:flex;"
                             "align-items:center;justify-content:center;height:90vh'>"
                             f"{tr('Organize os trechos para ver a volumetria 3D.')}</body></html>")
            return
        if self._carregado:
            self._enviar(scene)
        elif not self._carregando:
            self._carregando = True
            self._cena_na_pagina = scene
            self._arquivo.write_text(viewer_html(scene, textos_da_volumetria()), encoding="utf-8")
            self.web.setUrl(QUrl.fromLocalFile(str(self._arquivo)))
        # Se já está carregando, a cena mais recente é aplicada ao terminar.

    def _enviar(self, scene: Scene) -> None:
        """Troca só a cena na página aberta; a câmera fica onde está."""
        payload = json.dumps(scene_payload(scene), ensure_ascii=True)
        self.web.page().runJavaScript(f"TritonVolumetria.setScene({payload}, {{keepCamera: true}});")
        self._cena_na_pagina = scene

    def _ao_carregar(self, ok: bool) -> None:
        if self._carregado or not self._carregando:
            return  # eventos repetidos, ou a página de aviso sem cena
        self._carregando = False
        if not ok:
            return
        self._carregado = True
        if self.scene is not None and self.scene is not self._cena_na_pagina:
            self._enviar(self.scene)
        # Sem contexto WebGL (driver, área remota, máquina virtual), a página só
        # mostraria um aviso: a aba passa para o visualizador em QPainter.
        self.web.page().runJavaScript(
            "(window.__tritonVolumetria && window.__tritonVolumetria.erro) || ''",
            lambda erro: self._usar_reserva() if erro == "webgl" else None)

    def _usar_reserva(self) -> None:
        if self.reserva is not None:
            return
        from triton.ui.volumetry_view import VolumetryPanel

        self.reserva = VolumetryPanel(self)
        self.layout().addWidget(self.reserva)
        self.web.hide()
        self.reserva.set_scene(self.scene)

    def _tela_cheia(self, request) -> None:
        request.accept()
        self.tela_cheia_pedida.emit(bool(request.toggleOn()))

    def sair_da_tela_cheia(self) -> None:
        """A janela saiu da tela cheia (F11, Esc, botão): a página sai junto."""
        from PySide6.QtWebEngineCore import QWebEnginePage

        self.web.page().triggerAction(QWebEnginePage.ExitFullScreen)

    def closeEvent(self, event) -> None:
        try:
            self._arquivo.unlink(missing_ok=True)
        except OSError:
            pass
        super().closeEvent(event)


def criar_painel_de_volumetria(parent=None) -> QWidget:
    """Visualizador WebGL quando possível; o de QPainter como reserva."""
    if web_disponivel():
        try:
            return VolumetryWebPanel(parent)
        except Exception:
            pass
    from triton.ui.volumetry_view import VolumetryPanel
    return VolumetryPanel(parent)
