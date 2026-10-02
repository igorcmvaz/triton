"""A tipologia da edificação e a categoria tarifária têm de combinar.

O programa oferece oito tipologias — três residenciais unifamiliares, uma
multifamiliar, comercial, escola, hotel e hospital — e cada uma ajusta o consumo
per capita e a fração não potável. Isso sempre funcionou: a demanda muda e
atravessa o programa.

O que não atravessava era a **tipologia em si**. `template_id` era gravado num
dicionário local da aba de edificação e nunca alcançava `NetunoConfig`, de modo
que nenhum outro módulo sabia que tipo de edificação estava sendo estudada.

A consequência é concreta, e é a que estes testes protegem: as 652 estruturas
tarifárias são todas da categoria «Residencial normal». Um estudo de hospital ou
de escola sai com a demanda certa e a **tarifa errada**, e ninguém avisa. Na
Tabela Tarifária CASAN 04/2026 a primeira faixa custa R$ 3,08/m³ no residencial e
R$ 6,81/m³ no comercial, no industrial e no público.

Como a economia é avaliada pela tarifa, subestimá-la subestima a economia na
mesma proporção. Não dá para corrigir o dado — as outras categorias não foram
coletadas — mas dá para tornar a incompatibilidade visível, que é o que impede o
estudo errado de sair calado.
"""

from __future__ import annotations

import pytest

from netuno.core.parser import NetunoConfig
from netuno.core.tariff_category import (
    CATEGORIA_COLETADA,
    CATEGORIA_POR_TIPOLOGIA,
    NOME_DA_TIPOLOGIA,
    categoria_exigida,
    e_residencial,
    incompatibilidade_de_categoria,
)
from netuno.core.tariffs_database import load_tariffs_db

NAO_RESIDENCIAIS = tuple(k for k, v in CATEGORIA_POR_TIPOLOGIA.items() if v != "Residencial")
RESIDENCIAIS = tuple(k for k, v in CATEGORIA_POR_TIPOLOGIA.items() if v == "Residencial")


def _config(template_id: str) -> NetunoConfig:
    cfg = NetunoConfig()
    cfg.building_template_id = template_id
    return cfg


# ────────────────── a tipologia agora existe na configuração ───────────────────

def test_a_configuracao_carrega_a_tipologia():
    """Ficava presa num dicionário local da aba de edificação."""
    assert NetunoConfig().building_template_id == "res_medio"


def test_o_catalogo_de_tipologias_da_interface_esta_todo_mapeado():
    """Uma tipologia sem categoria mapeada passaria sem aviso.

    O mapa é lido da própria aba de edificação, de modo que acrescentar uma
    tipologia lá e esquecer aqui derruba este teste.
    """
    pytest.importorskip("PySide6")
    from netuno.ui.tab_building import BUILDING_TEMPLATES

    ids = {t["id"] for t in BUILDING_TEMPLATES}
    assert ids == set(CATEGORIA_POR_TIPOLOGIA), ids ^ set(CATEGORIA_POR_TIPOLOGIA)
    assert ids == set(NOME_DA_TIPOLOGIA)


# ─────────────────────────── o mapa e o aviso ──────────────────────────────────

def test_as_residenciais_nao_avisam():
    for tid in RESIDENCIAIS:
        assert e_residencial(tid), tid
        assert incompatibilidade_de_categoria(_config(tid)) is None, tid


def test_as_nao_residenciais_avisam():
    """São quatro: comercial, escola, hotel e hospital."""
    assert len(NAO_RESIDENCIAIS) == 4
    for tid in NAO_RESIDENCIAIS:
        aviso = incompatibilidade_de_categoria(_config(tid))
        assert aviso, tid
        assert NOME_DA_TIPOLOGIA[tid] in aviso
        assert categoria_exigida(tid) in aviso


def test_o_aviso_diz_o_sentido_do_erro():
    """Saber que a tarifa está errada não basta: é preciso saber para que lado.

    As categorias não residenciais são mais caras, logo a economia e o retorno
    estão subestimados — o erro é conservador, e o projetista precisa saber
    disso para julgar se o estudo ainda se sustenta.
    """
    aviso = incompatibilidade_de_categoria(_config("hospital"))
    assert "SUBESTIMADOS" in aviso
    assert "6,81" in aviso and "3,08" in aviso     # a medida, da tabela da CASAN
    assert "Personalizado" in aviso                # e o que fazer a respeito


def test_uma_tipologia_desconhecida_nao_estoura():
    assert categoria_exigida(None) == "Residencial"
    assert categoria_exigida("inventada") == "Residencial"
    assert incompatibilidade_de_categoria(_config("inventada")) is None


# ──────────────────── a premissa do aviso continua verdadeira ──────────────────

def test_o_catalogo_tem_mesmo_uma_categoria_so():
    """O aviso existe porque isto é verdade. Se deixar de ser, ele sai.

    Quando as demais categorias forem coletadas, este teste cai e lembra de
    trocar o aviso por um seletor de categoria.
    """
    cidades = load_tariffs_db()["cities"]
    assert CATEGORIA_COLETADA == "Residencial normal"
    # Nenhum município declara estrutura por categoria.
    assert not any("categorias" in c for c in cidades.values())
    assert all("faixas" in c for c in cidades.values())


# ───────────────────── o percurso, da aba ao painel ────────────────────────────

@pytest.fixture
def janela(qapp):
    pytest.importorskip("PySide6")
    from netuno.ui.main_window import MainWindow

    return MainWindow()


def test_escolher_a_tipologia_na_aba_chega_a_configuracao(janela):
    """Era a desconexão: a demanda atravessava e a tipologia não."""
    aba = janela.tab_building
    for tid in ("hospital", "comercial", "res_medio"):
        idx = aba.combo_building_template.findData(tid)
        assert idx >= 0, tid
        aba.combo_building_template.setCurrentIndex(idx)
        aba.get_building_config()
        assert janela.config.building_template_id == tid


def test_o_painel_economico_avisa_quando_a_tipologia_nao_e_residencial(janela):
    """O aviso precisa estar onde o resultado contaminado é lido."""
    aba, tab = janela.tab_building, janela.tab_economic

    aba.combo_building_template.setCurrentIndex(aba.combo_building_template.findData("res_medio"))
    aba.get_building_config()
    tab.calculate_economics(force=True)
    assert tab.lbl_aviso_categoria.text() == ""

    aba.combo_building_template.setCurrentIndex(aba.combo_building_template.findData("escola"))
    aba.get_building_config()
    tab.calculate_economics(force=True)
    assert "Escola" in tab.lbl_aviso_categoria.text()


def test_o_dialogo_de_tarifas_avisa_da_categoria_antes_da_estrutura(janela):
    """A categoria erra a conta inteira; a estrutura erra um trecho dela."""
    from netuno.ui.dialogs.dialog_economic import DialogTariffs

    janela.config.building_template_id = "hospital"
    dlg = DialogTariffs(config=janela.config)
    dlg._buscar_municipio("Florianópolis")
    assert "Categoria tarifária incompatível" in dlg.lbl_estrutura_aviso.text()


@pytest.mark.parametrize("template_id", NAO_RESIDENCIAIS)
def test_a_international_edition_nao_fala_de_um_catalogo_que_ela_nao_tem(template_id, monkeypatch):
    """Na International Edition a tarifa é digitada pelo usuário, na categoria certa.

    O aviso diz que «o catálogo tem apenas a categoria Residencial», e esse
    catálogo não acompanha a edição: lá ele seria falso, e em português.
    """
    monkeypatch.setenv("NETUNO_EDITION", "INT")
    assert incompatibilidade_de_categoria(_config(template_id)) is None
    monkeypatch.setenv("NETUNO_EDITION", "BRL")
    assert incompatibilidade_de_categoria(_config(template_id))
