"""
Propriedades da análise econômico-financeira.

Segue o mesmo método aplicado ao motor hidrológico em `test_scientific_properties.py`:
em vez de conferir números de casos isolados, cada teste afirma uma relação que deve
valer para *qualquer* parametrização válida. Foi esse método que expôs o defeito de
repartição nos kernels acelerados, invisível para os testes de caso então existentes.

As propriedades aqui são as da engenharia econômica clássica — monotonicidade do VPL
nas suas variáveis, ordenação entre paybacks simples e descontado, linearidade do fluxo
de caixa — e não premissas particulares do Netuno. Uma violação indica erro na
implementação do fluxo de caixa, não divergência de cenário.
"""

import pytest

from netuno.core.economic import (
    calculate_economic_indicators,
    run_robust_economic_analysis,
)

# Caso-base deliberadamente viável, para que as variações tenham espaço em ambas as
# direções sem esbarrar em zero.
BASE = dict(
    initial_investment=15000.0,
    annual_water_saved_m3=180.0,
    water_tariff_per_m3=12.0,
    sewage_tariff_per_m3=6.0,
    sewage_mode=1,
    water_tariff_escalation_rate=0.04,
    sewage_tariff_escalation_rate=0.04,
    elec_tariff_escalation_rate=0.04,
    inflation_rate=0.04,
    discount_rate=0.08,
    annual_om_cost_base=150.0,
    pump_power_kw=0.5,
    pump_hours_year=200.0,
    elec_tariff_kwh=0.9,
    analysis_period_years=20,
)


def _vpl(**alteracoes):
    return run_robust_economic_analysis(**{**BASE, **alteracoes}).vpl


# ---------------------------------------------------------------------------------
# Monotonicidade do VPL nas suas variáveis
# ---------------------------------------------------------------------------------

def test_vpl_cresce_com_a_tarifa_de_agua():
    """E1 — Água mais cara torna o aproveitamento mais valioso."""
    valores = [_vpl(water_tariff_per_m3=t) for t in (4.0, 8.0, 12.0, 20.0, 30.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-6, f"VPL caiu com tarifa maior: {valores}"


def test_vpl_decresce_com_o_investimento_inicial():
    """E2 — O mesmo benefício por um custo maior nunca vale mais."""
    valores = [_vpl(initial_investment=i) for i in (5000.0, 15000.0, 30000.0, 60000.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-6, f"VPL subiu com investimento maior: {valores}"


def test_vpl_decresce_com_a_taxa_de_desconto():
    """E3 — Descontar mais o futuro reduz o valor presente de benefícios futuros."""
    valores = [_vpl(discount_rate=d) for d in (0.02, 0.05, 0.08, 0.12, 0.20)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-6, f"VPL subiu com TMA maior: {valores}"


def test_vpl_cresce_com_o_volume_de_agua_economizada():
    """E4 — Economizar mais água nunca reduz o retorno."""
    valores = [_vpl(annual_water_saved_m3=v) for v in (0.0, 60.0, 120.0, 240.0, 480.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-6, f"VPL caiu com mais água economizada: {valores}"


def test_vpl_decresce_com_o_custo_de_operacao():
    """E5 — OPEX maior reduz o retorno."""
    valores = [_vpl(annual_om_cost_base=c) for c in (0.0, 150.0, 500.0, 1500.0)]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte <= anterior + 1e-6, f"VPL subiu com OPEX maior: {valores}"


# ---------------------------------------------------------------------------------
# Relações estruturais
# ---------------------------------------------------------------------------------

def test_payback_descontado_nunca_precede_o_simples():
    """E6 — Descontar o fluxo só pode atrasar a recuperação do investimento."""
    for tarifa in (8.0, 12.0, 20.0, 35.0):
        resultado = run_robust_economic_analysis(**{**BASE, "water_tariff_per_m3": tarifa})
        if resultado.payback_simple_years is None or resultado.payback_discounted_years is None:
            continue
        assert resultado.payback_discounted_years >= resultado.payback_simple_years - 1e-9, (
            f"payback descontado ({resultado.payback_discounted_years:.4f}) precede o simples "
            f"({resultado.payback_simple_years:.4f}) com tarifa {tarifa}"
        )


def test_paybacks_nunca_sao_negativos():
    """E7 — Tempo de retorno é uma duração; não existe retorno antes do desembolso."""
    for investimento in (1000.0, 15000.0, 100000.0):
        resultado = run_robust_economic_analysis(**{**BASE, "initial_investment": investimento})
        for rotulo, valor in (("simples", resultado.payback_simple_years),
                              ("descontado", resultado.payback_discounted_years)):
            if valor is not None:
                assert valor >= 0.0, f"payback {rotulo} negativo: {valor}"


def test_sem_economia_de_agua_o_projeto_nao_se_paga():
    """E8 — Sem benefício não há retorno: o VPL não pode ser positivo."""
    resultado = run_robust_economic_analysis(**{
        **BASE, "annual_water_saved_m3": 0.0, "annual_iptu_savings": 0.0,
    })
    assert resultado.vpl <= 0.0, (
        f"VPL positivo ({resultado.vpl:.2f}) sem nenhuma água economizada"
    )


def test_vpl_e_linear_no_escalonamento_do_projeto():
    """E9 — O VPL é linear no fluxo de caixa.

    Dobrar simultaneamente investimento, água economizada e custos operacionais
    equivale a dois projetos idênticos, e deve dobrar o valor presente líquido.
    """
    simples = run_robust_economic_analysis(**BASE)
    dobrado = run_robust_economic_analysis(**{
        **BASE,
        "initial_investment": BASE["initial_investment"] * 2,
        "annual_water_saved_m3": BASE["annual_water_saved_m3"] * 2,
        "annual_om_cost_base": BASE["annual_om_cost_base"] * 2,
        "pump_hours_year": BASE["pump_hours_year"] * 2,
    })
    assert dobrado.vpl == pytest.approx(simples.vpl * 2, rel=1e-6), (
        f"VPL não escalou linearmente: {simples.vpl:.4f} -> {dobrado.vpl:.4f}"
    )


def test_horizonte_maior_nao_reduz_o_vpl_de_projeto_rentavel():
    """E10 — Se o fluxo anual é positivo, estender o horizonte só acrescenta valor."""
    valores = [
        run_robust_economic_analysis(**{**BASE, "water_tariff_per_m3": 25.0,
                                        "analysis_period_years": anos}).vpl
        for anos in (5, 10, 20, 30)
    ]
    for anterior, seguinte in zip(valores, valores[1:]):
        assert seguinte >= anterior - 1e-6, (
            f"VPL caiu ao estender o horizonte num projeto rentável: {valores}"
        )


def test_tir_e_coerente_com_o_sinal_do_vpl():
    """E11 — TIR e VPL concordam: VPL > 0 à TMA implica TIR acima da TMA."""
    for tarifa in (6.0, 12.0, 25.0, 40.0):
        resultado = run_robust_economic_analysis(**{**BASE, "water_tariff_per_m3": tarifa})
        if resultado.tir_pct is None:
            continue
        tma_pct = BASE["discount_rate"] * 100.0
        if resultado.vpl > 1.0:
            assert resultado.tir_pct >= tma_pct - 1e-6, (
                f"VPL positivo ({resultado.vpl:.2f}) com TIR ({resultado.tir_pct:.4f}%) "
                f"abaixo da TMA ({tma_pct:.2f}%), tarifa {tarifa}"
            )


def test_reprodutibilidade_exata():
    """E12 — Determinismo: mesma entrada, mesma saída."""
    a = run_robust_economic_analysis(**BASE)
    b = run_robust_economic_analysis(**BASE)
    assert a.vpl == b.vpl
    assert a.tir_pct == b.tir_pct
    assert a.payback_simple_years == b.payback_simple_years


# ---------------------------------------------------------------------------------
# Validação de entrada
# ---------------------------------------------------------------------------------

@pytest.mark.parametrize("campo", [
    "initial_investment", "annual_water_saved_m3", "water_tariff_per_m3",
    "annual_om_cost_base", "pump_power_kw",
])
def test_entradas_negativas_sao_rejeitadas(campo):
    """E13 — Grandezas físicas e monetárias negativas não são aceitas silenciosamente."""
    with pytest.raises(ValueError):
        run_robust_economic_analysis(**{**BASE, campo: -1.0})


def test_horizonte_invalido_e_rejeitado():
    """E14 — O horizonte de análise deve ser um número inteiro positivo de anos."""
    for invalido in (0, -5):
        with pytest.raises(ValueError):
            run_robust_economic_analysis(**{**BASE, "analysis_period_years": invalido})


# ---------------------------------------------------------------------------------
# Indicadores simplificados
# ---------------------------------------------------------------------------------

def test_indicadores_simples_acompanham_o_investimento():
    """E15 — O payback do cálculo simplificado cresce com o investimento."""
    paybacks = []
    for investimento in (5000.0, 10000.0, 20000.0, 40000.0):
        resultado = calculate_economic_indicators(
            initial_investment=investimento,
            annual_water_saved_m3=200.0,
            water_tariff_per_m3=14.0,
            analysis_period_years=20,
            discount_rate=0.08,
        )
        if resultado.payback_simple_years is not None:
            paybacks.append(resultado.payback_simple_years)
    assert len(paybacks) >= 2, "nenhum payback pôde ser comparado"
    for anterior, seguinte in zip(paybacks, paybacks[1:]):
        assert seguinte >= anterior - 1e-9, f"payback caiu com investimento maior: {paybacks}"


def test_indicadores_simples_e_robusto_concordam_no_sinal_do_vpl():
    """E16 — Os dois caminhos de cálculo econômico não podem discordar sobre viabilidade.

    `calculate_economic_indicators` e `run_robust_economic_analysis` são
    implementações distintas do mesmo fluxo de caixa, com granularidades diferentes.
    Não se exige igualdade numérica — os modelos de OPEX diferem —, mas discordar
    sobre o *sinal* do VPL significaria dizer ao usuário que o mesmo projeto é
    viável ou inviável conforme a tela consultada.
    """
    for tarifa, investimento in ((25.0, 8000.0), (5.0, 60000.0)):
        simples = calculate_economic_indicators(
            initial_investment=investimento,
            annual_water_saved_m3=200.0,
            water_tariff_per_m3=tarifa,
            annual_om_cost=150.0,
            discount_rate=0.08,
            analysis_period_years=20,
        )
        robusto = run_robust_economic_analysis(**{
            **BASE,
            "initial_investment": investimento,
            "annual_water_saved_m3": 200.0,
            "water_tariff_per_m3": tarifa,
            "sewage_tariff_per_m3": 0.0,
            "sewage_mode": 0,
            "annual_om_cost_base": 150.0,
            "pump_power_kw": 0.0,
            "pump_hours_year": 0.0,
        })
        # Faixa neutra: VPLs próximos de zero não caracterizam discordância.
        if abs(simples.npv) < 500.0 or abs(robusto.vpl) < 500.0:
            continue
        assert (simples.npv > 0) == (robusto.vpl > 0), (
            f"os dois cálculos discordam sobre a viabilidade com tarifa {tarifa} e "
            f"investimento {investimento}: simplificado={simples.npv:.2f}, "
            f"robusto={robusto.vpl:.2f}"
        )
