"""
Propriedades da avaliação de ciclo de vida (ACV simplificada).

Mesmo método de `test_scientific_properties.py` e `test_economic_properties.py`: cada
teste afirma uma relação válida para toda a família de parametrizações, não um número
de um cenário.

As propriedades são as da contabilidade de carbono — não-negatividade das emissões,
monotonicidade do CO₂ incorporado na massa de material, aditividade do inventário,
consistência do saldo líquido — e não premissas particulares do Netuno. Os fatores de
emissão continuam sendo premissas editáveis; o que se verifica aqui é que a aritmética
que os combina está correta.
"""

import pytest

from netuno.core.environmental import (
    EnvironmentalConfig,
    PipeInput,
    calculate_lca,
    run_environmental_sweep,
)


def _config(**alteracoes) -> EnvironmentalConfig:
    padrao = dict(
        lower_tank_vol=5000.0,
        annual_water_saved_m3=120.0,
        annual_pump_kwh=180.0,
        upper_tank_used=True,
        upper_tank_vol_liters=500.0,
        chlorine_dose_mg_l=2.0,
        chlorine_co2_kg_per_kg=25.0,
    )
    padrao.update(alteracoes)
    return EnvironmentalConfig(**padrao)


# ---------------------------------------------------------------------------------
# Não-negatividade
# ---------------------------------------------------------------------------------

@pytest.mark.parametrize("volume", [0.0, 1000.0, 5000.0, 20000.0, 100000.0])
def test_emissoes_nunca_sao_negativas(volume):
    """A1 — Massa e emissão são grandezas físicas não-negativas."""
    resultado = calculate_lca(volume, 120.0, _config(lower_tank_vol=volume))
    for campo in (
        "lower_tank_mass_kg", "upper_tank_mass_kg", "total_pipes_co2_kg",
        "pump_embodied_co2_kg", "total_embodied_co2_kg", "annual_pumping_co2_kg",
        "annual_treatment_co2_kg", "annual_chlorine_kg", "annual_avoided_co2_kg",
    ):
        valor = getattr(resultado, campo)
        assert valor >= 0.0, f"'{campo}' negativo ({valor}) para V = {volume} L"


# ---------------------------------------------------------------------------------
# Monotonicidade
# ---------------------------------------------------------------------------------

def test_co2_incorporado_cresce_com_o_volume_da_cisterna():
    """A2 — Cisterna maior exige mais material, logo mais carbono incorporado."""
    valores = []
    for volume in (0.0, 1000.0, 3000.0, 8000.0, 20000.0, 50000.0):
        valores.append(calculate_lca(volume, 120.0, _config(lower_tank_vol=volume))
                       .total_embodied_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-9, (
            f"CO2 incorporado caiu com cisterna maior: {valores}"
        )


def test_co2_evitado_cresce_com_a_agua_aproveitada():
    """A3 — Substituir mais água de rede evita mais emissão de tratamento."""
    valores = []
    for agua in (0.0, 30.0, 90.0, 200.0, 500.0):
        valores.append(calculate_lca(5000.0, agua, _config(annual_water_saved_m3=agua))
                       .annual_avoided_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-9, f"CO2 evitado caiu com mais água: {valores}"


def test_emissao_de_bombeamento_cresce_com_o_consumo_eletrico():
    """A4 — Mais energia de recalque, mais emissão operacional."""
    valores = []
    for kwh in (0.0, 50.0, 200.0, 800.0):
        valores.append(calculate_lca(5000.0, 120.0, _config(annual_pump_kwh=kwh))
                       .annual_pumping_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-9, f"emissão de bombeamento não cresceu: {valores}"


def test_comprimento_de_tubulacao_nao_reduz_o_carbono_incorporado():
    """A5 — Mais metros de tubo nunca reduzem o material empregado."""
    valores = []
    for comprimento in (0.0, 10.0, 40.0, 120.0):
        config = _config(pipes=[PipeInput(diameter_mm=100, length_m=comprimento)])
        valores.append(calculate_lca(5000.0, 120.0, config).total_pipes_co2_kg)
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-9, f"CO2 das tubulações caiu com mais tubo: {valores}"


# ---------------------------------------------------------------------------------
# Consistência interna
# ---------------------------------------------------------------------------------

def test_saldo_liquido_e_a_diferenca_entre_evitado_e_operacional():
    """A6 — O saldo líquido fecha com as suas parcelas.

    saldo = evitado − (bombeamento + tratamento)
    """
    for volume, agua in ((2000.0, 60.0), (8000.0, 200.0), (25000.0, 400.0)):
        resultado = calculate_lca(volume, agua,
                                  _config(lower_tank_vol=volume, annual_water_saved_m3=agua))
        esperado = (resultado.annual_avoided_co2_kg
                    - resultado.annual_pumping_co2_kg
                    - resultado.annual_treatment_co2_kg)
        assert resultado.net_annual_avoided_co2_kg == pytest.approx(esperado, rel=1e-9, abs=1e-9), (
            f"saldo líquido não fecha para V={volume}, água={agua}: "
            f"{resultado.net_annual_avoided_co2_kg} != {esperado}"
        )


def test_inventario_detalhado_soma_o_carbono_incorporado():
    """A7 — O detalhamento por item reconstitui o total incorporado.

    Um inventário que não soma o próprio total inviabiliza auditoria da ACV.
    """
    resultado = calculate_lca(8000.0, 200.0, _config(lower_tank_vol=8000.0))
    if not resultado.inventory_items:
        pytest.skip("inventário detalhado não disponível nesta configuração")

    soma = sum(item.embodied_co2_kg for item in resultado.inventory_items)
    assert soma == pytest.approx(resultado.total_embodied_co2_kg, rel=1e-6), (
        f"itens do inventário somam {soma:.4f} kg, total declarado "
        f"{resultado.total_embodied_co2_kg:.4f} kg"
    )


def test_inventario_detalhado_reconstitui_o_saldo_operacional():
    """A7b — As parcelas operacionais do inventário reconstituem o saldo anual.

    No inventário, emissões evitadas entram com sinal negativo em `annual_op_co2_kg`,
    de modo que o saldo líquido anual é o simétrico da soma das parcelas operacionais.
    Verificar esse lado é mais exigente que o incorporado: envolve bombeamento,
    dosagem química e água evitada, com convenções de sinal distintas.
    """
    resultado = calculate_lca(8000.0, 200.0, _config(lower_tank_vol=8000.0))
    if not resultado.inventory_items:
        pytest.skip("inventário detalhado não disponível nesta configuração")

    soma_operacional = sum(item.annual_op_co2_kg for item in resultado.inventory_items)
    assert -soma_operacional == pytest.approx(
        resultado.net_annual_avoided_co2_kg, rel=1e-6, abs=1e-9
    ), (
        f"parcelas operacionais somam {soma_operacional:.4f} kg/ano; saldo líquido "
        f"declarado é {resultado.net_annual_avoided_co2_kg:.4f} kg/ano"
    )


def test_a_cloracao_nao_depende_do_reservatorio_superior():
    """A8 — A cloração acompanha o tratamento, e não a caixa superior.

    Até setembro de 2026 esta propriedade dizia o contrário, e a ACV perdia o
    cloro ao desmarcar a caixa enquanto o econômico continuava a pagá-lo.
    """
    com = calculate_lca(5000.0, 150.0, _config(upper_tank_used=True))
    sem = calculate_lca(5000.0, 150.0, _config(upper_tank_used=False))
    assert sem.annual_chlorine_kg > 0.0
    assert sem.annual_chlorine_kg == com.annual_chlorine_kg


def test_payback_ambiental_nao_e_negativo():
    """A9 — Tempo de retorno ambiental é uma duração."""
    for volume in (1000.0, 5000.0, 20000.0):
        resultado = calculate_lca(volume, 150.0, _config(lower_tank_vol=volume))
        assert resultado.environmental_payback_years >= 0.0, (
            f"payback ambiental negativo ({resultado.environmental_payback_years}) "
            f"para V = {volume} L"
        )


def test_viabilidade_ambiental_concorda_com_o_saldo_acumulado():
    """A10 — O selo de viabilidade não pode contradizer o balanço de carbono."""
    for volume, agua in ((500.0, 10.0), (5000.0, 150.0), (50000.0, 400.0)):
        resultado = calculate_lca(volume, agua,
                                  _config(lower_tank_vol=volume, annual_water_saved_m3=agua))
        if abs(resultado.lifetime_net_co2_saved_kg) < 1e-6:
            continue
        assert resultado.is_environmentally_viable == (resultado.lifetime_net_co2_saved_kg > 0), (
            f"selo de viabilidade ({resultado.is_environmentally_viable}) contradiz o saldo "
            f"acumulado ({resultado.lifetime_net_co2_saved_kg:.4f} kg) para V = {volume} L"
        )


def test_reprodutibilidade_exata():
    """A11 — Determinismo."""
    a = calculate_lca(6000.0, 180.0, _config())
    b = calculate_lca(6000.0, 180.0, _config())
    assert a.total_embodied_co2_kg == b.total_embodied_co2_kg
    assert a.net_annual_avoided_co2_kg == b.net_annual_avoided_co2_kg


# ---------------------------------------------------------------------------------
# Varredura ambiental
# ---------------------------------------------------------------------------------

def test_varredura_preserva_a_monotonicidade_do_carbono_incorporado():
    """A12 — A varredura ambiental herda a monotonicidade do cálculo individual."""
    mapa_de_volumes = [(0.0, 0.0), (1000.0, 40.0), (3000.0, 80.0),
                       (8000.0, 110.0), (20000.0, 130.0)]
    resultado = run_environmental_sweep(mapa_de_volumes, _config())
    assert len(resultado.sweep_details) == len(mapa_de_volumes)

    incorporado = [d["lca_result"].total_embodied_co2_kg for d in resultado.sweep_details]
    for anterior, seguinte in zip(incorporado, incorporado[1:]):
        assert seguinte >= anterior - 1e-9, (
            f"CO2 incorporado caiu ao longo da varredura: {incorporado}"
        )


def test_varredura_concorda_com_o_calculo_individual():
    """A13 — Varrer volumes equivale a calcular cada volume isoladamente.

    Se divergirem, a varredura estaria propagando estado entre alternativas — o mesmo
    tipo de erro que produziu a divergência de repartição nos kernels acelerados.
    """
    mapa_de_volumes = [(2000.0, 60.0), (9000.0, 140.0)]
    config = _config()
    varredura = run_environmental_sweep(mapa_de_volumes, config)

    for (volume, agua), detalhe in zip(mapa_de_volumes, varredura.sweep_details):
        isolado = calculate_lca(volume, agua, config)
        assert detalhe["lca_result"].total_embodied_co2_kg == pytest.approx(
            isolado.total_embodied_co2_kg, rel=1e-9
        ), f"varredura diverge do cálculo isolado em V = {volume} L"
