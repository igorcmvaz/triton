"""
Propriedades científicas do motor hidrológico (verificação global baseada em propriedades).

Diferentemente dos testes de caso pontual, cada teste aqui afirma uma propriedade que o
modelo deve satisfazer para *qualquer* parametrização válida. Uma violação indica erro
estrutural no balanço diário, não divergência numérica de um cenário específico.

Os testes são executados em dois regimes, porque a sensibilidade do modelo depende do
regime hidrológico:

- **Limitado pela demanda** (oferta abundante): a economia satura na fração não potável.
  A amplitude do sinal é pequena (~0,02 pp), logo o regime discrimina pouco.
- **Limitado pela oferta** (captação escassa): a economia satura muito abaixo do teto
  não potável e responde fortemente aos parâmetros (~3,8 pp de amplitude). É neste
  regime que erros de balanço se tornam visíveis.

Referência do comportamento esperado: `docs/verificacao_e_validacao.md`.
"""

import numpy as np
import pytest

from netuno.core.simulation import run_single_simulation


def _serie_chuva(escala: float, n_dias: int, semente: int) -> np.ndarray:
    """Série pluviométrica sintética exponencial com dias secos."""
    rng = np.random.default_rng(semente)
    chuva = rng.exponential(scale=escala, size=n_dias)
    chuva[chuva < 1.5] = 0.0
    return chuva


# Regime limitado pela demanda: captação abundante, satura na fração não potável.
REGIME_DEMANDA = dict(
    precip_data=_serie_chuva(12.0, 1825, 2026),
    area=150.0,
    runoff_coeff=0.85,
    discard_mm=2.0,
    discard_mode=1,
    total_demand_per_day=600.0,
    rainwater_share=0.5,
)

# Regime limitado pela oferta: captação escassa, alta sensibilidade paramétrica.
REGIME_OFERTA = dict(
    precip_data=_serie_chuva(4.0, 1825, 7),
    area=30.0,
    runoff_coeff=0.80,
    discard_mm=2.0,
    discard_mode=1,
    total_demand_per_day=1500.0,
    rainwater_share=0.6,
)

REGIMES = [
    pytest.param(REGIME_DEMANDA, id="limitado-pela-demanda"),
    pytest.param(REGIME_OFERTA, id="limitado-pela-oferta"),
]


@pytest.mark.parametrize("regime", REGIMES)
def test_economia_monotona_nao_decrescente_no_volume(regime):
    """P1 — Ampliar a cisterna nunca pode reduzir a economia de água potável.

    Uma violação indicaria que o balanço descarta água já armazenada ao aumentar a
    capacidade, o que é fisicamente impossível num modelo YAS.
    """
    volumes = [0.0, 250.0, 500.0, 1000.0, 2000.0, 5000.0, 10000.0, 25000.0, 60000.0]
    economias = [
        run_single_simulation(lower_tank_vol=v, **regime).potential_potable_savings_pct
        for v in volumes
    ]
    for anterior, seguinte, v_ant, v_seg in zip(economias, economias[1:], volumes, volumes[1:]):
        assert seguinte >= anterior - 1e-9, (
            f"economia caiu de {anterior:.6f}% (V={v_ant} L) para {seguinte:.6f}% (V={v_seg} L)"
        )


@pytest.mark.parametrize("regime", REGIMES)
def test_economia_dentro_dos_limites_fisicos(regime):
    """P2 — A economia é uma fração: pertence a [0, 100] e nunca excede a fração não potável."""
    teto_nao_potavel = regime["rainwater_share"] * 100.0
    for v in [0.0, 1000.0, 10000.0, 100000.0]:
        economia = run_single_simulation(lower_tank_vol=v, **regime).potential_potable_savings_pct
        assert 0.0 <= economia <= 100.0, f"economia fora de [0,100]: {economia}"
        assert economia <= teto_nao_potavel + 1e-9, (
            f"economia {economia:.4f}% excede a fração não potável {teto_nao_potavel:.4f}%"
        )


@pytest.mark.parametrize("regime", REGIMES)
def test_volume_zero_nao_aproveita_agua(regime):
    """P2b — Sem reservatório não há armazenamento, logo não há economia."""
    res = run_single_simulation(lower_tank_vol=0.0, **regime)
    assert res.potential_potable_savings_pct == pytest.approx(0.0, abs=1e-9)
    assert res.avg_pluvial_consumed_l_day == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("regime", REGIMES)
def test_saturacao_em_teto_finito(regime):
    """P3 — A economia converge: dobrar um reservatório já enorme não muda o resultado."""
    grande = run_single_simulation(lower_tank_vol=1_000_000.0, **regime)
    enorme = run_single_simulation(lower_tank_vol=5_000_000.0, **regime)
    assert enorme.potential_potable_savings_pct == pytest.approx(
        grande.potential_potable_savings_pct, abs=0.5
    ), "a economia não convergiu para um teto estável"


@pytest.mark.parametrize("regime", REGIMES)
def test_reprodutibilidade_exata(regime):
    """P4 — O motor é determinístico: mesma entrada produz saída bit a bit idêntica."""
    a = run_single_simulation(lower_tank_vol=5000.0, **regime)
    b = run_single_simulation(lower_tank_vol=5000.0, **regime)
    assert a.potential_potable_savings_pct == b.potential_potable_savings_pct
    assert a.total_overflow_liters == b.total_overflow_liters


@pytest.mark.parametrize("regime", REGIMES)
def test_economia_nao_decrescente_na_area_de_captacao(regime):
    """P5 — Ampliar a área de captação nunca reduz a economia."""
    economias = []
    for area in [25.0, 50.0, 100.0, 200.0, 400.0]:
        parametros = {**regime, "area": area}
        economias.append(
            run_single_simulation(lower_tank_vol=5000.0, **parametros).potential_potable_savings_pct
        )
    for anterior, seguinte in zip(economias, economias[1:]):
        assert seguinte >= anterior - 1e-9, f"economia caiu ao ampliar a área: {economias}"


@pytest.mark.parametrize("regime", REGIMES)
def test_descarte_de_primeira_chuva_nao_aumenta_economia(regime):
    """P6 — Descartar mais água de first flush nunca pode aumentar o aproveitamento."""
    economias = []
    for descarte in [0.0, 1.0, 2.0, 5.0, 10.0]:
        parametros = {**regime, "discard_mm": descarte}
        economias.append(
            run_single_simulation(lower_tank_vol=5000.0, **parametros).potential_potable_savings_pct
        )
    for anterior, seguinte in zip(economias, economias[1:]):
        assert seguinte <= anterior + 1e-9, f"economia subiu ao descartar mais: {economias}"


@pytest.mark.parametrize("regime", REGIMES)
def test_extravasamento_nao_crescente_no_volume(regime):
    """P7 — Ampliar a cisterna nunca pode aumentar o extravasamento."""
    extravasamentos = [
        run_single_simulation(lower_tank_vol=v, **regime).total_overflow_liters
        for v in [250.0, 1000.0, 4000.0, 16000.0, 64000.0]
    ]
    for anterior, seguinte in zip(extravasamentos, extravasamentos[1:]):
        assert seguinte <= anterior + 1e-6, f"extravasamento subiu com V maior: {extravasamentos}"


@pytest.mark.parametrize("volume", [1000.0, 5000.0, 20000.0])
@pytest.mark.parametrize("area", [80.0, 300.0])
@pytest.mark.parametrize("descarte", [0.0, 3.0])
def test_balanco_de_massa_fecha_em_grade_de_parametros(volume, area, descarte):
    """P8 — Conservação de massa em grade paramétrica.

    Complementa `test_mass_conservation.py`, que verifica uma única parametrização:
    aqui o fechamento é exigido em 12 combinações de volume, área e descarte.
    """
    parametros = {**REGIME_DEMANDA, "area": area, "discard_mm": descarte}
    res = run_single_simulation(lower_tank_vol=volume, store_daily_details=True, **parametros)

    estoque_anterior = 0.0
    for dia in res.daily_results:
        entradas = estoque_anterior + dia.harvested_liters
        saidas = dia.lower_tank_end_liters + dia.pluvial_consumed_liters + dia.spilled_liters
        assert entradas == pytest.approx(saidas, abs=1e-6), (
            f"balanço não fecha (V={volume}, A={area}, descarte={descarte}): "
            f"entradas={entradas!r} saídas={saidas!r}"
        )
        estoque_anterior = dia.lower_tank_end_liters


def test_serie_sem_chuva_nao_produz_aproveitamento():
    """P9 — Sem precipitação não há captação, economia nem extravasamento."""
    parametros = {**REGIME_DEMANDA, "precip_data": np.zeros(365)}
    res = run_single_simulation(lower_tank_vol=5000.0, **parametros)
    assert res.potential_potable_savings_pct == 0.0
    assert res.avg_pluvial_consumed_l_day == 0.0
    assert res.total_overflow_liters == 0.0


# ---------------------------------------------------------------------------------
# P10 — Semântica do descarte de primeira chuva
#
# Trava uma decisão de modelagem, não um detalhe de implementação. O descarte subtrai
# a lâmina da precipitação do evento — `Pef = max(0, Pt − df)` — porque a água desviada
# para o dispositivo não chega à cisterna.
#
# O Netuno 4 usava outro tratamento: `df` como limiar, aproveitando `Pt` integralmente
# sempre que `Pt ≥ df`. A diferença é deliberada e responde por cerca de 46% do viés
# medido contra o Netuno 4 (ver docs/verificacao_e_validacao.md §5.5).
#
# Estes testes existem para que a semântica não seja revertida por engano, ao ser
# confundida com defeito.
# ---------------------------------------------------------------------------------

def test_descarte_subtrai_a_lamina_e_nao_atua_como_limiar():
    """P10 — Com chuva uniforme acima do limiar, o descarte reduz proporcionalmente.

    Sob o tratamento por limiar do Netuno 4, uma série em que toda chuva excede `df`
    seria aproveitada integralmente e o descarte não teria efeito algum. Sob a
    subtração, cada evento perde exatamente `df` mm.
    """
    chuva = np.full(730, 10.0)  # todo dia chove 10 mm, sempre acima do descarte
    parametros = dict(
        precip_data=chuva, area=100.0, runoff_coeff=1.0, discard_mode=1,
        total_demand_per_day=2000.0, rainwater_share=1.0,
    )

    sem_descarte = run_single_simulation(lower_tank_vol=1e9, discard_mm=0.0, **parametros)
    com_descarte = run_single_simulation(lower_tank_vol=1e9, discard_mm=2.0, **parametros)

    assert com_descarte.avg_pluvial_consumed_l_day < sem_descarte.avg_pluvial_consumed_l_day, (
        "o descarte não reduziu o aproveitamento: o motor está tratando `df` como "
        "limiar (comportamento do Netuno 4) em vez de subtrair a lâmina"
    )

    # Com área de 100 m², coeficiente 1,0 e reservatório irrestrito, subtrair 2 mm
    # equivale a 200 L/dia a menos de captação.
    perda_observada = (sem_descarte.avg_pluvial_consumed_l_day
                       - com_descarte.avg_pluvial_consumed_l_day)
    assert perda_observada == pytest.approx(200.0, rel=1e-3), (
        f"perda de {perda_observada:.2f} L/dia; esperada 200 L/dia (2 mm × 100 m² × 1,0)"
    )


def test_chuva_abaixo_do_descarte_nao_e_captada():
    """P10b — Evento menor que a lâmina de descarte não rende captação alguma."""
    chuva = np.full(365, 1.5)  # todo evento abaixo do descarte de 3 mm
    resultado = run_single_simulation(
        precip_data=chuva, lower_tank_vol=10000.0, area=100.0, runoff_coeff=1.0,
        discard_mm=3.0, discard_mode=1, total_demand_per_day=500.0, rainwater_share=1.0,
    )
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(0.0, abs=1e-9)


@pytest.mark.parametrize("modo,descricao", [
    (1, "todos os eventos"),
    (2, "primeiro evento após estiagem"),
    (3, "periodicidade de manutenção"),
])
def test_modos_de_descarte_diferem_apenas_na_frequencia(modo, descricao):
    """P10c — Os modos mudam em quais dias o descarte age, não a fórmula.

    Numa série com dias secos intercalados, o modo 1 descarta em todo evento e os
    modos 2 e 3 em subconjuntos dele. Logo o modo 1 nunca aproveita mais água que os
    demais sob a mesma lâmina.
    """
    rng = np.random.default_rng(11)
    chuva = rng.exponential(scale=8.0, size=1095)
    chuva[rng.random(1095) < 0.45] = 0.0  # intercala estiagens

    parametros = dict(
        precip_data=chuva, lower_tank_vol=8000.0, area=120.0, runoff_coeff=0.9,
        discard_mm=4.0, discard_days_interval=7,
        total_demand_per_day=700.0, rainwater_share=0.5,
    )

    todos_os_eventos = run_single_simulation(discard_mode=1, **parametros)
    avaliado = run_single_simulation(discard_mode=modo, **parametros)

    assert avaliado.avg_pluvial_consumed_l_day >= (
        todos_os_eventos.avg_pluvial_consumed_l_day - 1e-9
    ), (
        f"o modo {modo} ({descricao}) aproveitou menos água que o modo 1, que descarta "
        "em todos os eventos — a frequência de descarte está invertida"
    )
