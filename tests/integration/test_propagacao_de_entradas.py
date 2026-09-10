"""Matriz de propagação: cada entrada do usuário move o que deve mover.

Toda desconexão encontrada nesta revisão tem a mesma forma — um valor calculado
corretamente numa etapa e descartado antes de chegar a quem devia consumi-lo. O
assistente de motobomba descartava a altura manométrica; a linha de tratamento
era dimensionada e ignorada; a tipologia de edificação ficava presa num
dicionário local; o percentual de esgoto era sobrescrito pelo valor de recurso.

Nenhuma dessas aparece em teste de fórmula, porque cada parte isolada está
certa. O que as pega é verificar o **percurso**: mexer numa entrada e conferir
que a saída correspondente se moveu.

Este módulo faz isso de forma sistemática. Para cada entrada que o usuário
controla, altera-se o valor e verifica-se que o indicador de destino mudou — e,
onde faz sentido, que mudou no **sentido** certo. Uma ponte que se rompa derruba
a linha correspondente.

O percurso completo do programa:

    Etapa 1  chuva ──────────────┐
    Etapa 2  edificação → demanda ├──→ simulação diária ──┬──→ técnico
    Etapa 2b qualidade → ETAP ────┤                       ├──→ econômico
    Etapa 3  reservatório, custos ┘                       ├──→ ambiental
                                                          └──→ multicritério
"""

from __future__ import annotations

import pytest

pytest.importorskip("PySide6")

from netuno.core.economic import run_economic_analysis  # noqa: E402
from netuno.core.environmental import EnvironmentalConfig, calculate_lca  # noqa: E402
from netuno.core.simulation import SingleTankSimulationResult  # noqa: E402


# ───────────────────────────────── cenário base ────────────────────────────────

def _simulacao(pluvial_l_dia: float = 330.0, potavel_l_dia: float = 330.0):
    """Resultado de simulação com recalque real.

    `total_pumped_liters` em zero não é neutro: sem volume recalcado a altura
    manométrica não tem o que encarecer, e a energia dá zero em qualquer
    desnível.
    """
    r = SingleTankSimulationResult(
        lower_tank_vol=5000.0,
        potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=pluvial_l_dia,
        avg_potable_consumed_l_day=potavel_l_dia,
        avg_spilled_l_day=0.0,
        pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0,
        pct_days_null_satisfaction=5.0,
    )
    r.n_days_simulated = 365
    r.total_pumped_liters = pluvial_l_dia * 365.0
    r.total_pump_cycles = 365
    return r


@pytest.fixture
def janela(qapp):
    from netuno.ui.main_window import MainWindow

    win = MainWindow()
    win.tab_tanks_simulation.last_single_result = _simulacao()
    win.tab_tanks_simulation._is_technical_only = False
    return win


def _econ(cfg, sim=None):
    return run_economic_analysis(cfg, sim or _simulacao())


def _acv(**kwargs):
    base = dict(annual_water_saved_m3=120.0, annual_pump_kwh=150.0)
    base.update(kwargs)
    return calculate_lca(5000.0, base["annual_water_saved_m3"], EnvironmentalConfig(**base))


# ═══════════════ Etapa 1 — a chuva chega a quem depende dela ═══════════════════

def test_a_serie_de_chuva_chega_a_aba_de_qualidade(janela):
    """A precipitação estava fixa em 1.500 mm no cálculo de wash-off."""
    aba = janela.tab_water_quality
    janela.tab_tanks_simulation.precip_data = [2.0] * 365
    seca = aba._precipitacao_anual_mm()
    janela.tab_tanks_simulation.precip_data = [8.0] * 365
    umida = aba._precipitacao_anual_mm()
    assert umida > 3 * seca


def test_a_area_de_captacao_dimensiona_o_filtro_de_entrada(janela):
    """Telhado maior pede filtro maior, e o preço acompanha."""
    from netuno.core.etap_integration import capex_incremental_da_etap

    janela.config.area = 100.0
    pequeno = capex_incremental_da_etap(janela.config)
    janela.config.area = 400.0
    grande = capex_incremental_da_etap(janela.config)
    assert grande > pequeno


# ═════════════ Etapa 2 — edificação, demanda e tipologia ═══════════════════════

def test_a_tipologia_chega_a_configuracao_e_ao_aviso(janela):
    """Ficava presa num dicionário local da aba de edificação."""
    from netuno.core.tariff_category import incompatibilidade_de_categoria

    aba = janela.tab_building
    for tid, avisa in (("res_medio", False), ("hospital", True), ("comercial", True)):
        aba.combo_building_template.setCurrentIndex(aba.combo_building_template.findData(tid))
        aba.get_building_config()
        assert janela.config.building_template_id == tid
        assert bool(incompatibilidade_de_categoria(janela.config)) is avisa, tid


def test_o_volume_pluvial_simulado_rege_o_dimensionamento_da_etap(janela):
    """A aba pedia o volume a um atributo que não existe em NetunoConfig."""
    from netuno.core.etap_integration import volume_pluvial_anual_m3

    janela.tab_tanks_simulation.last_single_result = _simulacao(1000.0)
    volume = volume_pluvial_anual_m3(janela.config, janela.tab_water_quality._simulacao_corrente())
    assert volume == pytest.approx(365.25, rel=1e-6)
    assert volume != 120.0     # o valor de recurso que aparecia sempre


# ═════════ Etapa 2b — qualidade da água move investimento e emissão ════════════

@pytest.mark.parametrize("metodo", ["uv", "ozonio"])
def test_a_desinfeccao_escolhida_encarece_e_emite(janela, metodo):
    aba = janela.tab_water_quality
    aba.combo_disinf.setCurrentIndex(aba.combo_disinf.findData("cloro"))
    aba.on_disinfection_changed()
    base_econ = _econ(janela.config)
    base_acv = _acv(water_quality_disinfection="cloro")

    aba.combo_disinf.setCurrentIndex(aba.combo_disinf.findData(metodo))
    aba.on_disinfection_changed()
    assert _econ(janela.config).capex_total > base_econ.capex_total
    assert _acv(water_quality_disinfection=metodo).annual_treatment_co2_kg > base_acv.annual_treatment_co2_kg


def test_o_filtro_de_polimento_move_investimento_e_manutencao(janela):
    aba = janela.tab_water_quality
    aba.combo_class.setCurrentIndex(aba.combo_class.findData("classe_4"))
    aba.on_class_changed()

    aba.chk_polishing.setChecked(False)
    aba.on_polishing_changed()
    sem = _econ(janela.config)

    aba.chk_polishing.setChecked(True)
    aba.on_polishing_changed()
    com = _econ(janela.config)

    assert com.capex_total > sem.capex_total
    assert com.annual_etap_opex_brl > sem.annual_etap_opex_brl


def test_a_dose_de_cloro_digitada_rege_a_massa_anual(janela):
    aba = janela.tab_water_quality
    aba.txt_cl_dose.setText("3,0")
    aba.recalculate_all()
    dobro = _econ(janela.config).annual_chlorine_kg
    aba.txt_cl_dose.setText("1,5")
    aba.recalculate_all()
    metade = _econ(janela.config).annual_chlorine_kg
    assert dobro == pytest.approx(2 * metade, rel=1e-6)


# ═══════════ Etapa 3 — reservatório, motobomba e custos ════════════════════════

def test_a_altura_manometrica_do_assistente_rege_a_emissao_de_bombeamento(janela):
    """O assistente calculava a altura e a descartava no retorno."""
    from netuno.core.pump_energy import compute_annual_pump_energy
    from netuno.ui.dialogs.pump_wizard_dialog import PumpSelectionWizardDialog

    consumos = []
    for altura in (4.0, 30.0):
        assistente = PumpSelectionWizardDialog(upper_tank_vol=500.0)
        assistente.spin_h_geom.setValue(altura)
        assistente.recalculate()
        dados = assistente.selected_pump_data

        cfg = janela.config
        cfg.pump_power_kw = dados["kw"]
        cfg.pump_flow_rate = dados["flow_lh"]
        cfg.pump_efficiency = float(dados["efficiency"])
        cfg.pump_manometric_head_m = float(dados["manometric_head_m"])
        consumos.append(compute_annual_pump_energy(cfg, _simulacao(), upper_tank_used=True).annual_kwh)

    assert consumos[1] > 3 * consumos[0], consumos


def test_o_investimento_informado_muda_o_retorno(janela):
    cfg = janela.config
    cfg.cost_lower_tank = 2000.0
    barato = _econ(cfg)
    cfg.cost_lower_tank = 12000.0
    caro = _econ(cfg)
    assert caro.capex_total > barato.capex_total
    assert caro.vpl < barato.vpl


# ═════════════ tarifas — a estrutura escolhida rege a economia ═════════════════

def test_a_estrutura_tarifaria_rege_a_economia_de_agua(janela):
    """Franquia e disponibilidade diferem só pela tarifa da primeira faixa."""
    cfg = janela.config
    cfg.water_tariffs = [[0.0, 0.0, 40.0, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 5.0, 1]]
    com_franquia = _econ(cfg).annual_water_savings_brl

    cfg.water_tariffs = [[0.0, 0.0, 40.0, -1], [0.0, 999999.0, 5.0, 1]]
    com_disponibilidade = _econ(cfg).annual_water_savings_brl

    # Com franquia, o primeiro bloco não gera economia; com disponibilidade, gera.
    assert com_disponibilidade > com_franquia


def test_o_percentual_de_esgoto_rege_a_economia_total(janela):
    cfg = janela.config
    cfg.water_tariffs = [[0.0, 999999.0, 5.0, 1]]
    cfg.sewage_mode = 1
    cfg.sewage_rate = 0.0
    sem = _econ(cfg).annual_water_savings_brl
    cfg.sewage_rate = 100.0
    com = _econ(cfg).annual_water_savings_brl
    assert com == pytest.approx(2 * sem, rel=1e-6)


# ═══════════════ ambiental — os fatores regem o balanço ════════════════════════

def test_a_rota_de_agua_rege_a_emissao_evitada():
    from netuno.core import water_supply_routes as rotas

    baixa = _acv(potable_water_co2_kg_m3=rotas.co2_evitado_por_m3("vaz_2025_sudeste"))
    alta = _acv(potable_water_co2_kg_m3=rotas.co2_evitado_por_m3("dessalinizacao_termica"))
    assert alta.annual_avoided_co2_kg > 20 * baixa.annual_avoided_co2_kg
    assert alta.environmental_payback_years < baixa.environmental_payback_years


def test_o_fator_da_rede_rege_a_emissao_de_bombeamento():
    limpa = _acv(grid_co2_factor_kg_kwh=0.085)
    suja = _acv(grid_co2_factor_kg_kwh=0.700)
    assert suja.annual_pumping_co2_kg > 7 * limpa.annual_pumping_co2_kg


def test_o_material_do_reservatorio_rege_o_carbono_incorporado():
    pead = _acv(lower_material_key="PEAD")
    concreto = _acv(lower_material_key="CONCRETO")
    assert concreto.total_embodied_co2_kg != pead.total_embodied_co2_kg


# ═══════════ o percurso inteiro, de ponta a ponta ══════════════════════════════

def test_dobrar_o_aproveitamento_move_todos_os_modulos(janela):
    """A verificação de fecho: um sistema que aproveita o dobro tem de aparecer
    diferente em todos os módulos de saída, e nos sentidos certos."""
    pouco, muito = _simulacao(200.0), _simulacao(600.0)

    e_pouco, e_muito = _econ(janela.config, pouco), _econ(janela.config, muito)
    assert e_muito.annual_water_savings_brl > e_pouco.annual_water_savings_brl
    assert e_muito.vpl > e_pouco.vpl

    a_pouco = _acv(annual_water_saved_m3=pouco.annual_pluvial_consumed_m3)
    a_muito = _acv(annual_water_saved_m3=muito.annual_pluvial_consumed_m3)
    assert a_muito.annual_avoided_co2_kg > a_pouco.annual_avoided_co2_kg
    assert a_muito.environmental_payback_years < a_pouco.environmental_payback_years


def test_nenhum_modulo_devolve_valor_nao_finito(janela):
    """Um NaN atravessa o programa inteiro sem erro e contamina o relatório."""
    import math

    econ = _econ(janela.config)
    for campo in ("vpl", "capex_total", "annual_water_savings_brl", "annual_opex_brl",
                  "etap_capex_brl", "annual_etap_opex_brl"):
        valor = getattr(econ, campo)
        assert math.isfinite(valor), campo

    acv = _acv()
    for campo in ("total_embodied_co2_kg", "annual_pumping_co2_kg", "annual_treatment_co2_kg",
                  "annual_avoided_co2_kg", "lifetime_net_co2_saved_kg",
                  "environmental_payback_years", "specific_co2_avoided_g_per_liter"):
        valor = getattr(acv, campo)
        assert math.isfinite(valor), campo


# ═══════ os dois caminhos de execução têm de concordar entre si ════════════════

def _sim_cli():
    from netuno.core.simulation import SingleTankSimulationResult

    r = SingleTankSimulationResult(
        lower_tank_vol=5000.0, potential_potable_savings_pct=50.0,
        avg_pluvial_consumed_l_day=330.0, avg_potable_consumed_l_day=330.0,
        avg_spilled_l_day=0.0, pct_days_full_satisfaction=90.0,
        pct_days_partial_satisfaction=5.0, pct_days_null_satisfaction=5.0,
    )
    r.n_days_simulated = 365
    r.total_pumped_liters = 330.0 * 365
    r.total_pump_cycles = 365
    return r


def test_a_linha_de_comando_honra_a_escolha_de_desinfeccao():
    """O econômico honrava e a ACV não, na MESMA rodada.

    `run_economic_analysis` recebe o `NetunoConfig` inteiro, de modo que a linha
    de comando já cobrava o ozonizador no fluxo de caixa. A ACV montava a própria
    configuração sem os campos de qualidade da água e caía nos padrões, emitindo
    como se fosse só cloração. O relatório saía internamente contraditório.
    """
    from netuno.cli import _environmental_config
    from netuno.core.parser import NetunoConfig

    sim = _sim_cli()
    emissoes = {}
    for metodo in ("cloro", "uv", "ozonio"):
        cfg = NetunoConfig()
        cfg.water_quality_disinfection = metodo
        ambiental = _environmental_config(cfg, sim, 150.0, {})
        assert ambiental.water_quality_disinfection == metodo
        emissoes[metodo] = calculate_lca(ambiental).annual_treatment_co2_kg

    assert emissoes["uv"] > 5 * emissoes["cloro"]
    assert emissoes["ozonio"] > emissoes["uv"]


def test_a_linha_de_comando_usa_o_consumo_especifico_corrigido():
    """Estava congelado em 0,40 kWh/m³, o valor anterior à correção da hidráulica.

    Aquele número dividia pelo rendimento duas vezes e implicava 67 m de altura
    manométrica. A mesma configuração dava emissão de bombeamento diferente na
    tela e no terminal, com fator de 3,7.
    """
    from netuno.cli import _environmental_config
    from netuno.core.parser import NetunoConfig
    from netuno.core.pump_energy import consumo_especifico_padrao_kwh_por_m3

    ambiental = _environmental_config(NetunoConfig(), _sim_cli(), 150.0, {})
    assert ambiental.pump.specific_kwh_per_m3 == pytest.approx(
        consumo_especifico_padrao_kwh_por_m3()
    )
    assert ambiental.pump.specific_kwh_per_m3 < 0.20


def test_a_sobreposicao_legada_vale_so_para_quem_a_declara():
    """Ela tem precedência sobre a linha de tratamento, e portanto a desliga.

    Aplicá-la a todo projeto que não declarasse cloro — a maioria — fazia a
    escolha de desinfecção não surtir efeito ambiental nenhum na linha de comando.
    Projetos que a declaram continuam reproduzindo o resultado histórico.
    """
    from netuno.cli import _environmental_config
    from netuno.core.parser import NetunoConfig

    sim = _sim_cli()
    sem_declaracao = _environmental_config(NetunoConfig(), sim, 150.0, {})
    assert sem_declaracao.chemical_treatment_co2_m3 is None

    legado = _environmental_config(
        NetunoConfig(), sim, 150.0, {"chemical_treatment_co2_m3": 0.02}
    )
    assert legado.chemical_treatment_co2_m3 == pytest.approx(0.02)

    # E o projeto legado ignora a escolha de desinfecção, por desenho.
    cfg = NetunoConfig()
    cfg.water_quality_disinfection = "ozonio"
    com_ozonio = _environmental_config(cfg, sim, 150.0, {"chemical_treatment_co2_m3": 0.02})
    assert calculate_lca(com_ozonio).annual_treatment_co2_kg == pytest.approx(
        calculate_lca(legado).annual_treatment_co2_kg
    )
