"""Funções implementadas e sem nenhum chamador.

A varredura de desconexões encontrou seis. Duas eram minhas e já têm consumidor.
Das quatro restantes, duas tinham um lugar claro para servir e foram ligadas;
duas não têm consumidor plausível sem construir uma tela que ninguém pediu, e
ficam **verificadas** enquanto o destino delas não é decidido — uma função órfã
que ninguém testa é a que quebra em silêncio quando alguém finalmente a chama.

| Função | Destino |
| :--- | :--- |
| `get_available_climate_cities` | ligada ao combo de cidade da Etapa 1 |
| `search_cities` | ligada à busca de município do diálogo de tarifas |
| `save_costs_database` | sem editor de custos na interface; verificada |
| `get_tank_linear_regression` | diagnóstico do modelo de preço; verificada |
"""

from __future__ import annotations

import json

import pytest

from netuno.core.climate_database import get_available_climate_cities
from netuno.core.cost_estimates import (
    LOWER_TANK_PRICE_TABLE,
    get_tank_linear_regression,
    load_costs_database,
    save_costs_database,
)
from netuno.core.tariffs_database import get_available_ufs, get_cities_by_uf, search_cities


# ─────────────────── ligada: as cidades ofertadas têm série de chuva ───────────

def test_toda_cidade_ofertada_no_combo_tem_serie_climatica():
    """O mesmo combo escolhe a série de precipitação e a tarifa.

    Era povoado só pela base de TARIFAS. As duas coincidem hoje, mas nada
    garantia isso: acrescentar um município à base tarifária o faria aparecer na
    lista climática sem série para carregar, e o usuário só descobriria ao
    tentar simular.
    """
    com_serie = set(get_available_climate_cities())
    assert len(com_serie) > 100

    ofertadas = []
    for uf_code, _nome in get_available_ufs():
        ofertadas.extend(get_cities_by_uf(uf_code))
    assert ofertadas

    sem_serie = sorted({c for c in ofertadas if c not in com_serie})
    assert not sem_serie, f"ofertadas sem série climática: {sem_serie[:10]}"


# ───────────────────── ligada: a busca de município funciona ───────────────────

def test_a_busca_encontra_municipio_pelo_nome():
    achados = search_cities("Florian")
    assert achados
    assert any("Florian" in c.get("municipio", "") for c in achados)
    for c in achados:
        assert c.get("uf"), c


def test_a_busca_encontra_pela_prestadora():
    """Quem procura pela concessionária não tinha caminho nenhum."""
    achados = search_cities("CASAN")
    assert achados
    assert all(c.get("uf") == "SC" for c in achados)


def test_a_busca_respeita_o_limite_e_a_consulta_vazia():
    assert search_cities("") == []
    assert search_cities("   ") == []
    assert len(search_cities("a", limit=5)) <= 5


def test_a_busca_devolve_o_que_o_combo_precisa():
    """Sem UF e município a busca não teria como posicionar os dois combos."""
    for c in search_cities("Joinville"):
        assert c.get("uf")
        assert c.get("municipio")


# ─────────────── verificadas: sem consumidor, mas não sem contrato ─────────────

def test_a_regressao_de_preco_descreve_a_tabela_que_a_originou():
    """Devolve inclinação, intercepto e R² do modelo linear de preço por volume.

    Não tem superfície de exibição na interface. O contrato fica fixado para
    quando tiver: R² entre 0 e 1, e inclinação positiva, porque tanque maior não
    custa menos.
    """
    reg = get_tank_linear_regression("PEAD")
    assert reg["slope_r_per_l"] > 0.0
    assert 0.0 <= reg["r_squared"] <= 1.0
    assert reg["material"] == "PEAD"
    assert reg["is_upper"] is False

    # O ajuste descreve a tabela: o preço previsto para o maior volume tabelado
    # não pode divergir dela por mais de um terço.
    maior_vol, maior_preco = max(LOWER_TANK_PRICE_TABLE, key=lambda p: p[0])
    previsto = reg["slope_r_per_l"] * maior_vol + reg["intercept_r"]
    assert abs(previsto - maior_preco) / maior_preco < 0.34


def test_o_material_mais_caro_tem_inclinacao_maior():
    pead = get_tank_linear_regression("PEAD")["slope_r_per_l"]
    inox = get_tank_linear_regression("ACO_INOX")["slope_r_per_l"]
    assert inox > pead


def test_gravar_o_banco_de_custos_preserva_o_que_foi_gravado(tmp_path, monkeypatch):
    """Metade escrita de `load_costs_database`, sem editor na interface.

    O teste escreve num arquivo temporário: gravar sobre o banco do repositório
    alteraria os custos de todos os projetos.
    """
    import netuno.core.cost_estimates as ce

    destino = tmp_path / "costs_database.json"
    monkeypatch.setattr(ce, "COSTS_FILE_PATH", destino)

    dados = load_costs_database()
    dados["labor_percentage"] = 0.42
    assert save_costs_database(dados) is True
    assert destino.is_file()

    relido = json.loads(destino.read_text(encoding="utf-8"))
    assert relido["labor_percentage"] == pytest.approx(0.42)
    assert "typology_subsystems_configs" in relido


# ──────────────── a busca chega a tela e move os dois combos ───────────────────

@pytest.fixture
def dialogo_tarifas(qapp):
    pytest.importorskip("PySide6")
    from netuno.core.parser import NetunoConfig
    from netuno.ui.dialogs.dialog_economic import DialogTariffs

    return DialogTariffs(config=NetunoConfig())


def test_a_busca_posiciona_os_dois_combos(dialogo_tarifas):
    """Era o ponto: a seleção exigia saber a UF antes de achar o município."""
    dialogo_tarifas.txt_busca_municipio.setText("Joinville")
    dialogo_tarifas._buscar_municipio("Joinville")

    assert dialogo_tarifas.combo_uf.currentData() == "SC"
    assert dialogo_tarifas.combo_city.currentData() == "Joinville"
    assert "Joinville" in dialogo_tarifas.lbl_busca_resultado.text()


def test_a_busca_ignora_consulta_curta_demais(dialogo_tarifas):
    """Duas letras casariam com centenas de municípios, e a escolha seria arbitrária."""
    uf_antes = dialogo_tarifas.combo_uf.currentData()
    dialogo_tarifas._buscar_municipio("Jo")
    assert dialogo_tarifas.combo_uf.currentData() == uf_antes
    assert dialogo_tarifas.lbl_busca_resultado.text() == ""


def test_a_busca_avisa_quando_nao_encontra(dialogo_tarifas):
    dialogo_tarifas._buscar_municipio("Zzzzqqq")
    assert dialogo_tarifas.lbl_busca_resultado.text()


def test_a_busca_pela_prestadora_tambem_move_os_combos(dialogo_tarifas):
    dialogo_tarifas._buscar_municipio("CASAN")
    assert dialogo_tarifas.combo_uf.currentData() == "SC"
    assert dialogo_tarifas.combo_city.currentData()
