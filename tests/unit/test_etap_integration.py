"""A linha de tratamento deixa de ser uma ilha.

Até a versão 5.0.7 a estação de tratamento de água pluvial era dimensionada
apenas pela aba de Qualidade da Água, que exibia investimento, custo
operacional e emissão — e não os entregava a ninguém. Três campos de
configuração existiam para isso, eram escritos pela interface e não eram lidos
por módulo nenhum: escolher ultravioleta não alterava payback, valor presente
líquido nem emissão anual.

O acoplamento não é uma soma simples, e é isso que estes testes fixam:

* a cloração já era contada pelos dois módulos, de modo que o hipoclorito tem
  de aparecer **uma vez**, não duas;
* «Acessórios» já embutia uma verba de filtração, de modo que a ETAP a
  **substitui** em vez de se empilhar sobre ela;
* desligar a ETAP tem de devolver exatamente o resultado anterior, porque
  estudos já publicados foram rodados assim.
"""

from __future__ import annotations

import pytest

from netuno.core.chlorination import Cloracao
from netuno.core.cost_estimates import verba_generica_de_tratamento_brl
from netuno.core.economic import run_economic_analysis
from netuno.core.environmental import EnvironmentalConfig, calculate_lca
from netuno.core.etap_integration import (
    VOLUME_PLUVIAL_DE_RECURSO_M3,
    dimensionar_etap_do_projeto,
    volume_pluvial_anual_m3,
)
from netuno.core.parser import NetunoConfig
from netuno.core.simulation import SingleTankSimulationResult

VOLUME_M3 = 120.0


def _config_ambiental(**kwargs) -> EnvironmentalConfig:
    base = dict(annual_water_saved_m3=VOLUME_M3)
    base.update(kwargs)
    return EnvironmentalConfig(**base)


def _acv(metodo: str = "cloro", **kwargs):
    return calculate_lca(5000.0, VOLUME_M3, _config_ambiental(water_quality_disinfection=metodo, **kwargs))


# ───────────────────────────── resolução do volume ─────────────────────────────

def test_o_volume_pluvial_vem_da_simulacao_e_nao_de_um_valor_fixo():
    """A aba pedia `annual_pluvial_consumed_m3` à configuração, e o campo não existe.

    É propriedade do RESULTADO da simulação, não de `NetunoConfig`. O `getattr`
    devolvia sempre o valor de recurso, e a ETAP era dimensionada para 120 m³/ano
    qualquer que fosse o projeto.
    """
    assert not hasattr(NetunoConfig(), "annual_pluvial_consumed_m3")

    sim = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=1000.0,
        avg_potable_consumed_l_day=500.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0,
        pct_days_null_satisfaction=5.0,
    )
    assert sim.annual_pluvial_consumed_m3 == pytest.approx(365.25)
    assert volume_pluvial_anual_m3(NetunoConfig(), sim) == pytest.approx(365.25)


def test_sem_simulacao_o_volume_cai_no_valor_de_recurso():
    assert volume_pluvial_anual_m3(NetunoConfig(), None) == VOLUME_PLUVIAL_DE_RECURSO_M3


def test_a_etap_acompanha_o_volume_do_projeto():
    """Dobrar o consumo dobra o consumo de hipoclorito, não o investimento."""
    pequeno = dimensionar_etap_do_projeto(NetunoConfig(), annual_pluvial_m3=100.0)
    grande = dimensionar_etap_do_projeto(NetunoConfig(), annual_pluvial_m3=200.0)
    assert grande.custo_anual_do_cloro == pytest.approx(2 * pequeno.custo_anual_do_cloro)
    assert grande.capex == pytest.approx(pequeno.capex)


# ───────────────────────────── a ACV enxerga a escolha ─────────────────────────

def test_escolher_ultravioleta_muda_a_emissao_da_acv():
    """Era a desconexão principal: a escolha ficava guardada e era ignorada."""
    cloro = _acv("cloro")
    uv = _acv("uv")
    ozonio = _acv("ozonio")

    assert uv.annual_treatment_co2_kg > 10 * cloro.annual_treatment_co2_kg
    assert ozonio.annual_treatment_co2_kg > uv.annual_treatment_co2_kg
    # E o saldo líquido cai, porque a barreira adicional é emissão nova.
    assert uv.net_annual_avoided_co2_kg < cloro.net_annual_avoided_co2_kg
    assert ozonio.environmental_payback_years > cloro.environmental_payback_years


def test_o_polimento_tambem_chega_a_acv():
    sem = _acv("cloro", water_quality_polishing=False)
    com = _acv("cloro", water_quality_polishing=True)
    assert com.annual_treatment_co2_kg > sem.annual_treatment_co2_kg


def test_o_cloro_e_contado_uma_vez_na_acv():
    """Somar o total da ETAP ao termo de cloração contaria o hipoclorito duas vezes.

    Com apenas cloração, a ETAP e o termo antigo têm de coincidir: é essa
    identidade que prova que houve substituição, e não soma.
    """
    cfg = _config_ambiental(water_quality_disinfection="cloro")
    cloracao = Cloracao(
        dose_mg_por_litro=cfg.chlorine_dose_mg_l,
        pureza=cfg.chlorine_product_purity,
        fator_kg_co2e_por_kg_produto=cfg.chlorine_co2_kg_per_kg,
    )
    esperado = cloracao.co2e_anual_kg(VOLUME_M3)
    obtido = calculate_lca(5000.0, VOLUME_M3, cfg).annual_treatment_co2_kg
    assert obtido == pytest.approx(esperado, rel=1e-9)


def test_a_parcela_extra_isola_o_que_nao_e_cloro():
    assert _acv("cloro").etap_extra_co2_kg_yr == pytest.approx(0.0)
    uv = _acv("uv")
    assert uv.etap_extra_co2_kg_yr == pytest.approx(
        uv.annual_treatment_co2_kg - _acv("cloro").annual_treatment_co2_kg, rel=1e-9
    )


def test_desligar_a_etap_devolve_o_resultado_anterior():
    """Estudos já rodados usaram só a cloração, e têm de continuar reproduzíveis."""
    antigo = calculate_lca(5000.0, VOLUME_M3, _config_ambiental(etap_enabled=False, water_quality_disinfection="uv"))
    assert antigo.etap_extra_co2_kg_yr == pytest.approx(0.0)
    assert antigo.annual_treatment_co2_kg == pytest.approx(_acv("cloro").annual_treatment_co2_kg)


def test_o_campo_legado_de_intensidade_continua_mandando():
    """Projetos antigos informavam kg CO2e/m³ diretamente; trocar por baixo mudaria resultados publicados."""
    cfg = _config_ambiental(chemical_treatment_co2_m3=0.5, water_quality_disinfection="ozonio")
    r = calculate_lca(5000.0, VOLUME_M3, cfg)
    assert r.annual_treatment_co2_kg == pytest.approx(0.5 * VOLUME_M3)


def test_o_inventario_nomeia_os_estagios_de_desinfeccao():
    uv = _acv("uv")
    item = next(i for i in uv.inventory_items if "Tratamento" in i.category)
    assert "ultravioleta" in item.source_reference.lower()
    assert any("ultravioleta" in e.lower() for e in uv.etap_disinfection_stages)


# ─────────────────────────── o econômico enxerga a escolha ─────────────────────

def _sim() -> SingleTankSimulationResult:
    return SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=330.0,
        avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0,
        pct_days_null_satisfaction=5.0,
    )


def _econ(metodo: str = "cloro", **kwargs):
    cfg = NetunoConfig()
    cfg.water_quality_disinfection = metodo
    for k, v in kwargs.items():
        setattr(cfg, k, v)
    return run_economic_analysis(cfg, _sim())


def test_a_etap_entra_no_investimento():
    econ = _econ("cloro")
    assert econ.etap_capex_brl > 0.0
    assert econ.etap_disinfection_method == "cloro"


def test_escolher_ultravioleta_encarece_o_investimento_e_o_custeio():
    cloro, uv = _econ("cloro"), _econ("uv")
    assert uv.etap_capex_brl > cloro.etap_capex_brl
    assert uv.capex_total > cloro.capex_total
    assert uv.annual_etap_opex_brl > cloro.annual_etap_opex_brl
    # E a escolha tem de mover o resultado financeiro, que era o ponto.
    assert uv.vpl < cloro.vpl


def test_o_cloro_e_pago_uma_vez_no_economico():
    """Só a cloração: a parcela extra da ETAP tem de ser nula.

    O custeio do hipoclorito já vinha da linha de cloração. Somar o custeio
    total da ETAP o cobraria duas vezes.
    """
    econ = _econ("cloro")
    assert econ.annual_etap_opex_brl == pytest.approx(0.0)
    assert econ.annual_chlorine_cost_brl > 0.0


def test_o_capex_da_etap_desloca_a_verba_generica_de_acessorios():
    """«Acessórios» já embute uma verba de filtração e tratamento.

    Somar o CAPEX inteiro da ETAP sobre ela contaria o filtro duas vezes.
    """
    verba = verba_generica_de_tratamento_brl("UTI")
    assert verba > 0.0

    sem_acessorios = _econ("cloro", cost_accessories=0.0)
    com_acessorios = _econ("cloro", cost_accessories=800.0)
    assert com_acessorios.etap_capex_brl == pytest.approx(sem_acessorios.etap_capex_brl - verba)


def test_desligar_a_etap_zera_as_duas_parcelas_no_economico():
    econ = _econ("uv", etap_enabled=False)
    assert econ.etap_capex_brl == 0.0
    assert econ.annual_etap_opex_brl == 0.0


def test_a_dose_e_a_pureza_do_projeto_chegam_ao_dimensionamento():
    """A ETAP assumia a pureza padrão mesmo com outra configurada.

    A mesma cloração aparecia com massa e custo diferentes em duas telas.
    """
    cfg = NetunoConfig()
    cfg.chlorine_product_purity = 0.65
    padrao = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)

    cfg.chlorine_product_purity = 0.325   # pastilha com metade do cloro ativo
    diluida = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)

    # Metade da pureza exige o dobro do produto para a mesma dose de cloro ativo.
    assert diluida.resultado.annual_chlorine_kg == pytest.approx(
        2 * padrao.resultado.annual_chlorine_kg, rel=1e-9
    )


def test_o_preco_do_cloro_e_o_mesmo_nos_dois_modulos():
    """Estavam em R$ 38,00/kg na aba de qualidade e R$ 25,00/kg no econômico."""
    cfg = NetunoConfig()
    etap = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
    esperado = etap.resultado.annual_chlorine_kg * cfg.chlorine_cost_per_kg
    assert etap.resultado.annual_chlorine_cost_brl == pytest.approx(esperado, rel=1e-9)


def test_a_dose_relatada_vale_para_qualquer_metodo():
    """Valia zero quando o método não era «cloro», embora a cloração seja sempre aplicada."""
    for metodo in ("cloro", "uv", "ozonio"):
        cfg = NetunoConfig()
        cfg.water_quality_disinfection = metodo
        etap = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)
        assert etap.resultado.chlorine_dose_mg_l > 0.0, metodo
        assert etap.resultado.annual_chlorine_kg > 0.0, metodo


def test_descarte_primeiras_aguas_soma_no_capex_da_etap_e_economico():
    cfg = NetunoConfig()
    cfg.discard = 2.0
    cfg.area = 100.0
    cfg.first_flush_system_enabled = False
    etap_sem = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)

    cfg.first_flush_system_enabled = True
    etap_com = dimensionar_etap_do_projeto(cfg, annual_pluvial_m3=VOLUME_M3)

    assert etap_com.first_flush_volume_l == 200.0  # 2.0 mm * 100 m² = 200 L
    assert etap_com.first_flush_capex > 0.0
    assert etap_com.capex == pytest.approx(etap_sem.capex + etap_com.first_flush_capex)


def test_descarte_primeiras_aguas_soma_no_inventario_da_acv():
    cfg_env_sem = EnvironmentalConfig(
        annual_water_saved_m3=VOLUME_M3,
        discard=2.0,
        roof_area_m2=100.0,
        first_flush_system_enabled=False,
    )
    lca_sem = calculate_lca(5000.0, VOLUME_M3, cfg_env_sem)

    cfg_env_com = EnvironmentalConfig(
        annual_water_saved_m3=VOLUME_M3,
        discard=2.0,
        roof_area_m2=100.0,
        first_flush_system_enabled=True,
    )
    lca_com = calculate_lca(5000.0, VOLUME_M3, cfg_env_com)

    # O carbono incorporado de fabricação do descarte aumenta o total_embodied_co2_kg
    assert lca_com.total_embodied_co2_kg > lca_sem.total_embodied_co2_kg
    categorias = [item.category for item in lca_com.inventory_items]
    assert any("Descarte" in cat for cat in categorias)

