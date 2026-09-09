"""Verificacao da captura de avisos do Qt.

O aviso ``QFont::setPointSize: Point size <= 0 (-1)`` enchia o console sem que
se soubesse a origem. Nenhuma chamada a ``setPointSize`` existe em ``netuno/``,
e todas as construcoes de ``QFont`` usam tamanho literal positivo — o aviso vem
de dentro do Qt e nao se reproduz na construcao das telas.

O que se protege aqui e a ferramenta que torna o aviso localizavel: capturar a
pilha na primeira ocorrencia e nao repetir a mensagem nas seguintes.
"""

from __future__ import annotations

import os

import pytest

pytest.importorskip("PySide6")

from PySide6.QtCore import qWarning  # noqa: E402

from netuno.ui import qt_diagnostics  # noqa: E402


@pytest.fixture(autouse=True)
def _estado_limpo(tmp_path, monkeypatch):
    """Cada teste comeca sem historico e grava o log em pasta temporaria."""
    qt_diagnostics._JA_REGISTRADOS.clear()
    qt_diagnostics._CONTAGEM.clear()
    monkeypatch.setattr(qt_diagnostics, "_CAMINHO_DO_LOG", str(tmp_path / "avisos_qt.log"))
    yield
    qt_diagnostics._JA_REGISTRADOS.clear()
    qt_diagnostics._CONTAGEM.clear()


def test_conta_todas_as_ocorrencias_mas_registra_uma_vez(qapp):
    qt_diagnostics.instalar_captura_de_avisos()
    mensagem = "QFont::setPointSize: Point size <= 0 (-1), must be greater than 0"

    for _ in range(7):
        qWarning(mensagem)

    contagem = qt_diagnostics.contagem_de_avisos()
    assert contagem[mensagem] == 7, "todas as ocorrencias precisam ser contadas"
    assert qt_diagnostics._JA_REGISTRADOS == {mensagem}, "so a primeira gera registro"


def test_avisos_distintos_sao_registrados_separadamente(qapp):
    qt_diagnostics.instalar_captura_de_avisos()
    qWarning("primeiro aviso")
    qWarning("segundo aviso")
    qWarning("primeiro aviso")

    contagem = qt_diagnostics.contagem_de_avisos()
    assert contagem["primeiro aviso"] == 2
    assert contagem["segundo aviso"] == 1
    assert len(qt_diagnostics._JA_REGISTRADOS) == 2


def test_a_pilha_python_e_gravada(qapp):
    """Sem a pilha, o aviso continua sendo ruido: e ela que localiza a origem."""
    qt_diagnostics.instalar_captura_de_avisos()

    def funcao_com_nome_reconhecivel():
        qWarning("aviso de teste com pilha")

    funcao_com_nome_reconhecivel()

    caminho = qt_diagnostics._CAMINHO_DO_LOG
    assert os.path.isfile(caminho)
    with open(caminho, "r", encoding="utf-8") as arquivo:
        texto = arquivo.read()
    assert "aviso de teste com pilha" in texto
    assert "funcao_com_nome_reconhecivel" in texto, (
        "a pilha precisa nomear o quadro que provocou o aviso"
    )


def test_resumo_vazio_quando_nao_houve_aviso():
    assert qt_diagnostics.resumo_dos_avisos() == ""


def test_resumo_lista_cada_aviso_com_a_contagem(qapp):
    qt_diagnostics.instalar_captura_de_avisos()
    qWarning("aviso repetido")
    qWarning("aviso repetido")
    qWarning("aviso unico")

    resumo = qt_diagnostics.resumo_dos_avisos()
    assert "2 vezes: aviso repetido" in resumo
    assert "1 vez: aviso unico" in resumo


def test_nenhuma_chamada_a_setpointsize_no_pacote():
    """A causa do aviso nao esta no codigo do Netuno — e isso precisa continuar verdade.

    Se alguem introduzir uma chamada a setPointSize, ela passa a ser suspeita
    numero um, e este teste faz a ligacao entre o sintoma e a mudanca.
    """
    raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pacote = os.path.join(raiz, "netuno")

    ocorrencias = []
    for pasta, _, arquivos in os.walk(pacote):
        for nome in arquivos:
            if not nome.endswith(".py"):
                continue
            if nome == "qt_diagnostics.py":
                # O proprio modulo de diagnostico cita o aviso em prosa.
                continue
            caminho = os.path.join(pasta, nome)
            with open(caminho, "r", encoding="utf-8") as arquivo:
                for numero, linha in enumerate(arquivo, start=1):
                    if "setPointSize" in linha and not linha.lstrip().startswith("#"):
                        ocorrencias.append(f"{os.path.relpath(caminho, raiz)}:{numero}")

    assert not ocorrencias, (
        "setPointSize introduzido em netuno/ — provavel causa do aviso do Qt: "
        f"{ocorrencias}"
    )
