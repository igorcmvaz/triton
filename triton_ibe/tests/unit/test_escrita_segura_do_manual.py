# -*- coding: utf-8 -*-
"""Rodar um gerador do manual não pode desfazer revisão feita à mão.

A auditoria regenerou as tabelas e os apêndices e encontrou dez arquivos em que
os números batiam, mas as legendas, as figuras e os cabeçalhos revisados tinham
sumido. A gravação passou a recusar sobrescrever conteúdo diferente.
"""

import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
sys.path.insert(0, MANUAL)

try:
    from escrita_segura import DIVERGENTE, GRAVADO, IGUAL, gravar
except ModuleNotFoundError:
    pytest.skip("geradores do manual nao versionados (ficam no disco do mantenedor)", allow_module_level=True)


def test_arquivo_novo_e_gravado(tmp_path):
    alvo = tmp_path / "tabela.md"
    assert gravar(str(alvo), "a\n") == GRAVADO
    assert alvo.read_text(encoding="utf-8") == "a\n"


def test_conteudo_igual_nao_mexe_e_limpa_lateral(tmp_path):
    alvo = tmp_path / "tabela.md"
    alvo.write_text("a\n", encoding="utf-8")
    (tmp_path / "tabela.md.gerado").write_text("velho", encoding="utf-8")
    assert gravar(str(alvo), "a\n") == IGUAL
    assert not (tmp_path / "tabela.md.gerado").exists()


def test_conteudo_diferente_nao_sobrescreve_a_revisao(tmp_path, monkeypatch):
    monkeypatch.delenv("TRITON_REGERAR", raising=False)
    alvo = tmp_path / "tabela.md"
    alvo.write_text("<!-- tabela: legenda revisada -->\n| a |\n", encoding="utf-8")
    assert gravar(str(alvo), "| a |\n") == DIVERGENTE
    assert "legenda revisada" in alvo.read_text(encoding="utf-8")
    assert (tmp_path / "tabela.md.gerado").read_text(encoding="utf-8") == "| a |\n"


def test_regerar_de_proposito_sobrescreve(tmp_path, monkeypatch):
    monkeypatch.setenv("TRITON_REGERAR", "1")
    alvo = tmp_path / "tabela.md"
    alvo.write_text("revisado\n", encoding="utf-8")
    assert gravar(str(alvo), "gerado\n") == GRAVADO
    assert alvo.read_text(encoding="utf-8") == "gerado\n"


@pytest.mark.parametrize("gerador", ["gerar_tabelas.py", "gerar_apendices.py",
                                     "gerar_casos.py"])
def test_geradores_do_manual_gravam_pela_escrita_segura(gerador):
    """Nenhum gerador escreve markdown do manual abrindo o arquivo diretamente."""
    texto = open(os.path.join(MANUAL, gerador), encoding="utf-8").read()
    diretas = re.findall(r'open\([^)]*,\s*"w"[^)]*\)', texto)
    # gerar_casos grava os arquivos .triton por outro caminho, que não são texto
    # revisado à mão; o README e o apêndice passam pela escrita segura.
    assert not diretas, (gerador, diretas)
    assert "from escrita_segura import gravar" in texto


def test_nao_ha_versao_gerada_pendente_de_revisao():
    """Um `.gerado` esquecido é uma divergência que ninguém conferiu."""
    pendentes = []
    for base, _, arquivos in os.walk(MANUAL):
        pendentes += [os.path.join(base, a) for a in arquivos if a.endswith(".gerado")]
    assert not pendentes, pendentes
