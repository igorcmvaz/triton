"""``marca.aplicar`` (o nome do programa nos textos) e a gravação com as duas extensões de projeto."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from triton import marca


@pytest.fixture
def nome_novo(monkeypatch):
    monkeypatch.setattr(marca, "NOME", "Zyx 9")
    return "Zyx 9"


def test_com_o_nome_atual_o_texto_volta_identico():
    texto = "Sobre o Triton — TRITON (.triton) TritonConfig"
    assert marca.NOME == "Triton"
    assert marca.aplicar(texto) is texto
    assert marca.aplicar(None) is None and marca.aplicar(3) == 3


def test_troca_a_palavra_inteira_e_respeita_maiusculas(nome_novo):
    assert marca.aplicar("Sobre o Triton") == "Sobre o Zyx 9"
    assert marca.aplicar("TRITON — PLANTA 3D") == "ZYX 9 — PLANTA 3D"
    assert marca.aplicar("Triton's convention; (Triton); <b>Triton</b>.") == \
        "Zyx 9's convention; (Zyx 9); <b>Zyx 9</b>."
    assert marca.aplicar("如何引用Triton。") == "如何引用Zyx 9。"
    assert marca.aplicar("regra do Triton.") == "regra do Zyx 9."


@pytest.mark.parametrize("protegido", [
    "projeto.triton", "python -m triton.cli", "TritonConfig", "TRITON_EDITION", "Tritons",
    "manual/Manual-Triton.pdf", "manual/en/Triton-User-Manual.pdf", "Triton-INT", "Triton2.png",
    "Triton.exe", "C:/Programas/Triton/dados", "mailto:x@y.z?subject=Triton%20-%20Tarifa",
    "TRITON-REF", "triton", "x_Triton",
])
def test_nao_toca_em_caminhos_identificadores_e_extensoes(nome_novo, protegido):
    assert marca.aplicar(protegido) == protegido


def test_aplicar_duas_vezes_nao_muda_o_resultado(nome_novo):
    uma = marca.aplicar("Sobre o Triton — TRITON")
    assert marca.aplicar(uma) == uma


def test_extensao_para_salvar_preserva_a_do_projeto_aberto():
    assert marca.extensao_para_salvar("") == marca.EXTENSAO_PROJETO
    assert marca.extensao_para_salvar("C:/x/estudo.NETUNO") == ".netuno"
    assert marca.extensao_para_salvar("estudo.triton") == ".triton"
    assert marca.extensao_para_salvar("serie.csv") == marca.EXTENSAO_PROJETO


def test_filtro_de_salvar_oferece_as_duas_extensoes_sem_mudar_a_chave():
    from triton.ui.translation import tr
    chave = '{0} (*.triton);;{1} (*.json);;CSV legado — não preserva todas as etapas (*.csv)'
    for lang in ("pt", "en", "es", "zh"):
        traduzido = tr(chave, lang)
        assert "(*.triton)" in traduzido, lang      # a busca no catálogo continua funcionando
        filtro = marca.filtro_para_salvar(traduzido, ".netuno")
        assert filtro.startswith("{0} (*.netuno *.triton);;{1} (*.json)")
    assert marca.filtro_para_salvar("{0} (*.triton)").endswith("(*.triton *.netuno)")


def test_salvar_e_reabrir_projeto_netuno(tmp_path: Path):
    """Um .netuno aberto e gravado de novo continua .netuno e reabre com o mesmo conteúdo."""
    from triton.core.parser import export_triton_json, load_triton_project

    exemplo = next(Path(__file__).resolve().parents[2].glob("examples/*.triton"))
    aberto = tmp_path / "estudo.netuno"
    shutil.copyfile(exemplo, aberto)
    proj = load_triton_project(str(aberto))
    destino = tmp_path / ("regravado" + marca.extensao_para_salvar(str(aberto)))
    assert destino.suffix == ".netuno"
    export_triton_json(config=proj["config"], file_path=str(destino),
                       precip_data=proj.get("precip_data"), building_data=proj.get("building_data"))
    assert destino.is_file()
    reaberto = load_triton_project(str(destino))
    assert reaberto["is_json"] is True
    assert reaberto["config"].__dict__.keys() == proj["config"].__dict__.keys()
    assert reaberto["config"].project_name == proj["config"].project_name
    assert reaberto["config"].project_id == proj["config"].project_id
