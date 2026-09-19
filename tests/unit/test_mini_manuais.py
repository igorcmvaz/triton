"""Os mini manuais recortam o manual completo sem quebrar nenhuma remissão."""
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "manual"))

import gerar  # noqa: E402
import gerar_mini_manuais as mini  # noqa: E402


@pytest.fixture(scope="module")
def volumes(tmp_path_factory):
    pasta = tmp_path_factory.mktemp("mini")
    original = mini.PASTA
    mini.PASTA = str(pasta)
    try:
        return {titulo: open(mini.montar(arquivo, titulo, caps, aps)[0], encoding="utf-8").read()
                for arquivo, titulo, caps, aps in mini.VOLUMES}
    finally:
        mini.PASTA = original


def test_todo_capitulo_esta_em_algum_volume():
    cobertos = {c for _, _, caps, _ in mini.VOLUMES for c in caps}
    assert cobertos == set(range(1, len(gerar.ESTRUTURA) + 1))


def test_nenhuma_marca_fica_sem_destino(volumes):
    for titulo, texto in volumes.items():
        assert "??" not in texto, titulo
        assert "{{" not in texto, titulo


def test_a_numeracao_das_secoes_e_a_do_manual_completo(volumes):
    numeros = gerar.indice_das_secoes()
    metodo = volumes["O método"]
    assert f"## {numeros['28_energia_de_bombeamento']}. Energia de bombeamento" in metodo
    tutorial = volumes["Tutorial"]
    assert f"## {numeros['07_escolher_o_volume']}. Escolher o volume" in tutorial


def test_remissao_para_outro_volume_diz_qual(volumes):
    tutorial = volumes["Tutorial"]
    assert re.search(r"seção \d+\.\d+ \(volume O método\)", tutorial)
    assert "(volume Tutorial)" not in tutorial
