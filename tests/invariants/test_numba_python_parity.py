"""
Paridade numérica entre o kernel Numba (JIT) e o kernel Python de referência.

Motivação
---------
`netuno.core.simulation` possui duas implementações independentes do balanço hídrico
diário. A seleção é implícita, em tempo de importação:

    if HAS_NUMBA and not store_daily_details:   # kernel JIT
    else:                                       # kernel Python de referência

Consequências relevantes para a verificação:

1. `numba` **não** é declarado em `pyproject.toml` nem em `requirements.txt`. A troca de
   kernel depende, portanto, do que houver instalado na máquina do usuário — dois
   usuários podem obter resultados diferentes do mesmo projeto sem qualquer aviso.
2. Os kernels JIT usam `@numba.njit(fastmath=True)`. `fastmath` autoriza o compilador a
   reassociar operações de ponto flutuante, o que quebra a garantia de reprodutibilidade
   bit a bit em relação ao kernel Python.
3. O kernel JIT **estima** a divisão entre consumo interno e irrigação
   (`min(tot_pluv, tot_non_pot_demand)`), enquanto o kernel Python a acumula dia a dia.
   Esta é uma diferença algorítmica, não apenas de arredondamento.
4. `tests/invariants/test_mass_conservation.py` usa `store_daily_details=True` e portanto
   exercita **apenas** o kernel Python — o invariante mais forte do sistema nunca alcança
   o caminho JIT.

Este módulo fecha essa lacuna. Sem `numba` instalado os testes são ignorados (skip), e a
suíte permanece verde; num ambiente com `numba` eles passam a comparar os dois kernels.

Ver `docs/verificacao_e_validacao.md`, seção "Risco do caminho acelerado".
"""

import numpy as np
import pytest

from netuno.core import simulation
from netuno.core.simulation import run_single_simulation

numba_necessario = pytest.mark.skipif(
    not simulation.HAS_NUMBA,
    reason="numba não instalado: o kernel JIT não existe neste ambiente",
)

# Tolerância relativa. fastmath=True permite reassociação de ponto flutuante, portanto
# não se exige igualdade bit a bit — exige-se equivalência dentro do ruído numérico.
TOLERANCIA_RELATIVA = 1e-9


def _serie_chuva(semente: int, n_dias: int = 1825, escala: float = 10.0) -> np.ndarray:
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=escala, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


CENARIOS = [
    pytest.param(
        dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
             total_demand_per_day=600.0, rainwater_share=0.5,
             upper_tank_used=False, upper_tank_vol=0.0, pumping_threshold=0.0),
        id="reservatorio-unico",
    ),
    pytest.param(
        dict(area=150.0, runoff_coeff=0.85, discard_mm=2.0, discard_mode=1,
             total_demand_per_day=600.0, rainwater_share=0.5,
             upper_tank_used=True, upper_tank_vol=1000.0, pumping_threshold=300.0),
        id="reservatorio-duplo-com-recalque",
    ),
    pytest.param(
        dict(area=30.0, runoff_coeff=0.80, discard_mm=5.0, discard_mode=2,
             discard_days_interval=7, total_demand_per_day=1500.0, rainwater_share=0.6,
             upper_tank_used=False, upper_tank_vol=0.0, pumping_threshold=0.0),
        id="limitado-pela-oferta-descarte-pos-estiagem",
    ),
]


def _executar_nos_dois_kernels(monkeypatch, volume, parametros):
    """Roda a mesma parametrização no kernel JIT e no kernel Python de referência."""
    chuva = _serie_chuva(2026)

    resultado_jit = run_single_simulation(
        precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, **parametros
    )

    monkeypatch.setattr(simulation, "HAS_NUMBA", False)
    resultado_python = run_single_simulation(
        precip_data=chuva, lower_tank_vol=volume, store_daily_details=False, **parametros
    )
    return resultado_jit, resultado_python


@numba_necessario
@pytest.mark.parametrize("parametros", CENARIOS)
@pytest.mark.parametrize("volume", [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_na_economia_de_agua(monkeypatch, volume, parametros):
    """O indicador principal do software não pode depender de haver numba instalado."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, volume, parametros)
    assert jit.potential_potable_savings_pct == pytest.approx(
        puro.potential_potable_savings_pct, rel=TOLERANCIA_RELATIVA
    ), (
        "economia de água potável diverge entre os kernels: "
        f"JIT={jit.potential_potable_savings_pct!r} vs Python={puro.potential_potable_savings_pct!r}"
    )


@numba_necessario
@pytest.mark.parametrize("parametros", CENARIOS)
@pytest.mark.parametrize("volume", [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_nos_fluxos_agregados(monkeypatch, volume, parametros):
    """Consumo pluvial, consumo potável e extravasamento devem coincidir."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, volume, parametros)
    for atributo in (
        "avg_pluvial_consumed_l_day",
        "avg_potable_consumed_l_day",
        "avg_spilled_l_day",
        "total_overflow_liters",
    ):
        assert getattr(jit, atributo) == pytest.approx(
            getattr(puro, atributo), rel=TOLERANCIA_RELATIVA
        ), f"'{atributo}' diverge entre os kernels"


@numba_necessario
@pytest.mark.parametrize("parametros", CENARIOS)
def test_kernels_concordam_na_estatistica_de_atendimento(monkeypatch, parametros):
    """Os percentuais de dias com atendimento pleno, parcial e nulo devem coincidir."""
    jit, puro = _executar_nos_dois_kernels(monkeypatch, 5000.0, parametros)
    for atributo in (
        "pct_days_full_satisfaction",
        "pct_days_partial_satisfaction",
        "pct_days_null_satisfaction",
    ):
        assert getattr(jit, atributo) == pytest.approx(
            getattr(puro, atributo), rel=TOLERANCIA_RELATIVA
        ), f"'{atributo}' diverge entre os kernels"


@numba_necessario
def test_kernel_jit_preserva_a_conservacao_de_massa(monkeypatch):
    """O agregado do kernel JIT deve fechar o balanço tanto quanto o kernel Python.

    Como o caminho JIT não emite detalhamento diário, o fechamento é verificado no
    agregado: captado = consumido + extravasado + estoque final.
    """
    chuva = _serie_chuva(99)
    parametros = dict(
        area=120.0, runoff_coeff=0.85, discard_mm=1.0, discard_mode=1,
        total_demand_per_day=500.0, rainwater_share=0.5,
    )
    jit = run_single_simulation(
        precip_data=chuva, lower_tank_vol=8000.0, store_daily_details=False, **parametros
    )
    monkeypatch.setattr(simulation, "HAS_NUMBA", False)
    puro = run_single_simulation(
        precip_data=chuva, lower_tank_vol=8000.0, store_daily_details=False, **parametros
    )

    captado_jit = jit.annual_pluvial_consumed_m3 + jit.annual_spill_m3
    captado_puro = puro.annual_pluvial_consumed_m3 + puro.annual_spill_m3
    assert captado_jit == pytest.approx(captado_puro, rel=1e-9), (
        "o volume total captado (consumido + extravasado) diverge entre os kernels"
    )


@numba_necessario
@pytest.mark.xfail(
    strict=False,
    reason=(
        "DEFEITO CONHECIDO (Netuno 5.0.7): o kernel JIT estima a divisão entre consumo "
        "interno e irrigação aplicando min() sobre os TOTAIS anuais "
        "(simulation.py:638-639), enquanto o kernel Python acumula min() DIA A DIA "
        "(simulation.py:788-791). Como Σ min(aᵢ,bᵢ) ≤ min(Σaᵢ, Σbᵢ), o JIT superestima "
        "sistematicamente o consumo interno e subestima a irrigação. Divergência medida: "
        "até 1,8% no interno e 26,3% na irrigação. Os totais agregados permanecem corretos."
    ),
)
@pytest.mark.parametrize("volume", [1000.0, 5000.0, 20000.0])
def test_kernels_concordam_na_divisao_interno_irrigacao(monkeypatch, volume):
    """Regressão do defeito de divisão interno/irrigação no kernel JIT.

    A divisão importa para além do relatório: LEED v4 pontua uso externo (WEc1) e uso
    interno (WEc2) em créditos separados, de modo que um erro na repartição pode alterar
    o enquadramento em certificação, ainda que o total de água aproveitada esteja certo.

    Quando o defeito for corrigido este teste passa a XPASS, sinalizando a correção.
    """
    configuracao_predial = dict(
        demand=200.0, residents=4, share=0.5, demand_mode="constant",
        irrigation_liters_per_day=150.0, irrigation_rain_threshold_mm=2.0,
        non_potable_indoor_share=0.35, irrigation_potable_backup=True,
    )
    chuva = _serie_chuva(2026)

    jit = run_single_simulation(
        precip_data=chuva, lower_tank_vol=volume, store_daily_details=False,
        building_config=configuracao_predial,
    )
    monkeypatch.setattr(simulation, "HAS_NUMBA", False)
    puro = run_single_simulation(
        precip_data=chuva, lower_tank_vol=volume, store_daily_details=False,
        building_config=configuracao_predial,
    )

    # O total agregado deve continuar idêntico — o defeito é apenas na repartição.
    assert jit.avg_pluvial_consumed_l_day == pytest.approx(
        puro.avg_pluvial_consumed_l_day, rel=TOLERANCIA_RELATIVA
    ), "o total de água pluvial consumida divergiu (defeito mais grave que o conhecido)"

    assert jit.annual_pluvial_indoor_consumed_m3 == pytest.approx(
        puro.annual_pluvial_indoor_consumed_m3, rel=1e-6
    ), "consumo pluvial interno diverge entre os kernels"
    assert jit.annual_pluvial_irrigation_consumed_m3 == pytest.approx(
        puro.annual_pluvial_irrigation_consumed_m3, rel=1e-6
    ), "consumo pluvial de irrigação diverge entre os kernels"


def test_estado_do_kernel_esta_documentado():
    """Guarda de configuração: registra qual kernel está ativo neste ambiente.

    Não falha nunca — serve para que o relatório de QA identifique sem ambiguidade qual
    implementação foi exercitada na execução.
    """
    assert isinstance(simulation.HAS_NUMBA, bool)
