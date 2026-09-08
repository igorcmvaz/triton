"""
Casos analíticos: o motor conferido contra a matemática, não contra outra implementação.

Por que estes casos existem
---------------------------
A verificação externa do Netuno 5 se apoia nos 4.050 resultados do Netuno 4. Mas o
manual do Netuno 4 (junho/2014) delimita o que ele faz: **não possui modulação de
demanda, irrigação nem modos alternativos de descarte de primeira chuva**. Esses
recursos são acréscimos do Netuno 5 e, portanto, *não têm antecessor com que comparar* —
nenhuma execução do programa antigo os verificará.

Para eles o instrumento adequado é outro. Constrói-se um cenário simples o bastante para
que o resultado correto seja **derivável em forma fechada**, e exige-se que o motor o
reproduza. É verificação contra a matemática, e não contra outra implementação — o que
a torna independente inclusive de o Netuno 4 estar certo.

Regra de ouro deste módulo
--------------------------
**Todo valor esperado é derivado na docstring, a partir dos parâmetros, antes de ser
comparado.** Nenhum valor esperado foi obtido rodando o código: isso tornaria o teste
circular, capaz apenas de detectar mudança, jamais erro. O leitor deve poder refazer
cada conta com papel.

Convenções do motor usadas nas derivações
-----------------------------------------
- captação do dia: ``V_cap = P_ef × A × C`` litros, com ``P_ef`` em mm, ``A`` em m²
  (1 mm sobre 1 m² = 1 L);
- descarte no modo 1: ``P_ef = max(0, P − df)`` em todo dia com chuva;
- o extravasamento ocorre **antes** do consumo (*yield after spill*): a cisterna é
  primeiro limitada à capacidade, e só então se consome dela;
- consumo pluvial do dia: ``min(demanda pluvial, volume disponível)``;
- demanda pluvial: ``demanda total × fração pluvial``;
- economia (%): ``consumo pluvial acumulado ÷ demanda total acumulada × 100``.
"""

import numpy as np
import pytest

from netuno.core.simulation import run_single_simulation


# =====================================================================================
# 1. Regime limitado pela oferta — sem acumulação, sem extravasamento
# =====================================================================================

def test_regime_limitado_pela_oferta_tem_solucao_fechada():
    """Quando a captação diária é menor que a demanda pluvial, tudo que entra é
    consumido no mesmo dia: a cisterna nunca acumula e nunca extravasa.

    Parâmetros: P = 2 mm/dia constante, A = 50 m², C = 1,0, descarte 0,
    demanda total 1.000 L/dia, fração pluvial 0,5 → demanda pluvial 500 L/dia.

    Derivação:
        captação diária  = 2 × 50 × 1,0            = 100 L
        100 < 500, logo consome-se 100 L todo dia e o estoque volta a zero
        consumo pluvial  = 100 L/dia
        consumo potável  = 1.000 − 100             = 900 L/dia
        extravasamento   = 0
        economia         = 100 ÷ 1.000 × 100       = 10,0 %
        atendimento      = parcial em todos os dias (0 < 100 < 500) → 100 %
    """
    dias = 365
    resultado = run_single_simulation(
        precip_data=np.full(dias, 2.0), lower_tank_vol=10_000.0,
        area=50.0, runoff_coeff=1.0, discard_mm=0.0,
        total_demand_per_day=1000.0, rainwater_share=0.5,
    )

    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(100.0, rel=1e-12)
    assert resultado.avg_potable_consumed_l_day == pytest.approx(900.0, rel=1e-12)
    assert resultado.avg_spilled_l_day == pytest.approx(0.0, abs=1e-9)
    assert resultado.potential_potable_savings_pct == pytest.approx(10.0, rel=1e-12)
    assert resultado.pct_days_partial_satisfaction == pytest.approx(100.0, rel=1e-12)


# =====================================================================================
# 2. Regime limitado pela demanda — enchimento e extravasamento em regime permanente
# =====================================================================================

def test_enchimento_e_extravasamento_tem_solucao_fechada():
    """Com captação maior que a demanda, a cisterna enche num dia determinado e a partir
    dali extravasa exatamente o excedente diário.

    Parâmetros: P = 10 mm/dia constante, A = 100 m², C = 1,0, descarte 0,
    demanda total 1.000 L/dia, fração pluvial 0,5, cisterna 5.000 L.

    Derivação:
        captação diária H = 10 × 100 × 1,0 = 1.000 L
        demanda pluvial D = 500 L; excedente diário H − D = 500 L

        O extravasamento antecede o consumo. Seja S o estoque no início do dia:
            após captar: S + H;  se S + H > 5.000, extravasa S + H − 5.000
        Partindo de S = 0, o estoque ao fim do dia k é 500·k enquanto não houver
        extravasamento. No dia 9 tem-se S = 4.000 e S + H = 5.000, que não excede a
        capacidade — logo ainda não há extravasamento e o dia fecha em 4.500 L.
        No dia 10, S + H = 5.500 > 5.000: extravasa 500 L, e assim permanece.

        dias com extravasamento = 365 − 9 = 356
        extravasamento total    = 356 × 500                 = 178.000 L
        consumo pluvial total   = 365 × 500                 = 182.500 L
        conferência do balanço  = 365.000 captados
                                = 182.500 + 178.000 + 4.500 de estoque final ✓
        economia                = 182.500 ÷ 365.000 × 100   = 50,0 %
        atendimento pleno       = todos os dias             = 100 %
    """
    dias = 365
    resultado = run_single_simulation(
        precip_data=np.full(dias, 10.0), lower_tank_vol=5_000.0,
        area=100.0, runoff_coeff=1.0, discard_mm=0.0,
        total_demand_per_day=1000.0, rainwater_share=0.5,
    )

    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(500.0, rel=1e-12)
    assert resultado.avg_spilled_l_day == pytest.approx(178_000.0 / dias, rel=1e-9)
    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-12)
    assert resultado.pct_days_full_satisfaction == pytest.approx(100.0, rel=1e-12)


# =====================================================================================
# 3. Descarte de primeira chuva — a lâmina é subtraída
# =====================================================================================

def test_descarte_subtrai_lamina_em_proporcao_exata():
    """O descarte reduz a captação na proporção exata da lâmina subtraída.

    Parâmetros: P = 10 mm/dia constante, descarte 3 mm, modo 1 (todo evento).

    Derivação:
        sem descarte: P_ef = 10 mm
        com descarte: P_ef = 10 − 3 = 7 mm
        razão entre as captações = 7 ÷ 10 = 0,7 exatamente

        No regime limitado pela oferta (captação abaixo da demanda pluvial), todo o
        captado é consumido, e a razão dos consumos é a mesma razão das captações.

        A = 50 m², C = 1,0 → captação 500 L/dia sem descarte, 350 L/dia com descarte.
        Demanda pluvial = 1.000 L/dia, acima de ambas, garantindo o regime.

    Sob a regra do Netuno 4 (limiar), 10 mm ≥ 3 mm implicaria captar os 10 mm
    integrais, e a razão seria 1,0. Este teste distingue as duas semânticas.
    """
    comum = dict(precip_data=np.full(365, 10.0), lower_tank_vol=50_000.0,
                 area=50.0, runoff_coeff=1.0, discard_mode=1,
                 total_demand_per_day=2000.0, rainwater_share=0.5)

    sem_descarte = run_single_simulation(discard_mm=0.0, **comum)
    com_descarte = run_single_simulation(discard_mm=3.0, **comum)

    assert sem_descarte.avg_pluvial_consumed_l_day == pytest.approx(500.0, rel=1e-12)
    assert com_descarte.avg_pluvial_consumed_l_day == pytest.approx(350.0, rel=1e-12)
    assert (com_descarte.avg_pluvial_consumed_l_day
            / sem_descarte.avg_pluvial_consumed_l_day) == pytest.approx(0.7, rel=1e-12)


def test_descarte_periodico_atinge_apenas_os_dias_previstos():
    """No modo 3 o descarte se repete a cada intervalo configurado, e não todo dia.

    Parâmetros: P = 10 mm/dia constante (chove todos os dias), descarte 4 mm,
    modo 3 com intervalo de 5 dias, A = 50 m², C = 1,0, 100 dias.

    Derivação:
        O motor descarta quando ``i − último_descarte ≥ 5``, partindo de um último
        descarte muito antigo. Logo descarta nos dias 0, 5, 10, … 95 — um a cada
        cinco — totalizando 20 dias em 100.

        captação nos 20 dias com descarte  = (10 − 4) × 50 = 300 L
        captação nos 80 dias sem descarte  =  10      × 50 = 500 L
        captação total = 20 × 300 + 80 × 500 = 6.000 + 40.000 = 46.000 L
        média diária   = 460 L

        Com demanda pluvial de 1.000 L/dia, o regime é limitado pela oferta e todo o
        captado é consumido: consumo médio = 460 L/dia.
    """
    resultado = run_single_simulation(
        precip_data=np.full(100, 10.0), lower_tank_vol=50_000.0,
        area=50.0, runoff_coeff=1.0, discard_mm=4.0,
        discard_mode=3, discard_days_interval=5,
        total_demand_per_day=2000.0, rainwater_share=0.5,
    )
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(460.0, rel=1e-9)


def test_descarte_apos_estiagem_atinge_apenas_o_primeiro_evento():
    """No modo 2 o descarte incide só no primeiro dia de chuva após um dia seco.

    Parâmetros: padrão de 4 dias — 10 mm, 10 mm, 0 mm, 0 mm — repetido 25 vezes
    (100 dias), descarte 4 mm, A = 50 m², C = 1,0.

    Derivação:
        O motor aplica o descarte quando chove e a véspera teve menos de 1 mm.
        No padrão, o primeiro dia de cada ciclo sucede um dia seco: recebe descarte.
        O segundo dia sucede um dia de 10 mm: não recebe.
        Exceção: o dia 0 não tem véspera, e o motor a trata como 0 mm — logo também
        recebe descarte, o que é consistente com o padrão.

        por ciclo: 1 dia com descarte (P_ef = 6 mm) + 1 dia sem (P_ef = 10 mm)
        captação por ciclo = (6 + 10) × 50 = 800 L, em 4 dias
        captação total     = 25 ciclos × 800 = 20.000 L
        média diária       = 200 L

        Demanda pluvial de 1.000 L/dia mantém o regime limitado pela oferta, mas a
        cisterna precisa acumular entre chuvas; com 50.000 L de capacidade e consumo
        diário limitado pela demanda, todo o captado é consumido ao longo do período.
    """
    padrao = np.array([10.0, 10.0, 0.0, 0.0])
    resultado = run_single_simulation(
        precip_data=np.tile(padrao, 25), lower_tank_vol=50_000.0,
        area=50.0, runoff_coeff=1.0, discard_mm=4.0, discard_mode=2,
        total_demand_per_day=2000.0, rainwater_share=0.5,
    )
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(200.0, rel=1e-6)


# =====================================================================================
# 4. Modulação de demanda — o calendário
# =====================================================================================

def test_modulacao_semanal_reproduz_o_total_do_padrao():
    """Em um número inteiro de semanas, cada dia da semana ocorre o mesmo número de
    vezes, e a demanda total é o padrão semanal multiplicado por esse número.

    Parâmetros: padrão de segunda a domingo, em L/dia,
    [100, 200, 300, 400, 500, 600, 700]; 364 dias = 52 semanas exatas.

    Derivação:
        soma do padrão = 100+200+300+400+500+600+700 = 2.800 L por semana
        demanda total  = 52 × 2.800 = 145.600 L, qualquer que seja o dia inicial,
        porque em 52 semanas exatas cada dia da semana aparece 52 vezes.

        Com fração pluvial 0,5 e oferta abundante (P = 100 mm/dia sobre 100 m²,
        ou seja 10.000 L/dia, muito acima de qualquer demanda diária do padrão),
        toda a demanda pluvial é atendida:
            consumo pluvial total = 0,5 × 145.600 = 72.800 L
            economia = 72.800 ÷ 145.600 × 100 = 50,0 %
    """
    padrao = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0]
    dias = 364
    resultado = run_single_simulation(
        precip_data=np.full(dias, 100.0), lower_tank_vol=100_000.0,
        area=100.0, runoff_coeff=1.0, discard_mm=0.0,
        total_demand_per_day=400.0, rainwater_share=0.5,
        demand_mode="weekly", weekly_demands=padrao,
        start_date_str="01/01/1980",
    )

    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-9)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(72_800.0 / dias, rel=1e-9)


def test_modulacao_mensal_respeita_a_duracao_de_cada_mes():
    """A demanda mensal é ponderada pelo número de dias de cada mês, inclusive em
    fevereiro de ano bissexto.

    Parâmetros: demanda de 100 L/dia em janeiro, 200 em fevereiro, e assim por diante
    até 1.200 em dezembro; ano de 1980, que é bissexto, começando em 01/01.

    Derivação (dias de cada mês em 1980):
        jan 31 ×  100 =  3.100      jul 31 ×  700 = 21.700
        fev 29 ×  200 =  5.800      ago 31 ×  800 = 24.800
        mar 31 ×  300 =  9.300      set 30 ×  900 = 27.000
        abr 30 ×  400 = 12.000      out 31 × 1000 = 31.000
        mai 31 ×  500 = 15.500      nov 30 × 1100 = 33.000
        jun 30 ×  600 = 18.000      dez 31 × 1200 = 37.200

        soma das doze parcelas = 238.400 L, distribuídos em 31+29+31+30+31+30+31+31
        +30+31+30+31 = 366 dias.

        Com oferta abundante e fração pluvial 0,5, a economia é 50,0 % e o consumo
        pluvial total é 119.200 L.

    Um motor que tratasse todos os meses como tendo 30 dias, ou que ignorasse o ano
    bissexto, produziria outro total — daí a escolha de 1980.

    Nota de proveniência: na primeira redação deste caso a soma das doze parcelas foi
    anotada como 237.400 L, por erro de adição manual. O teste reprovou, e a conferência
    mostrou que o valor correto é 238.400 L — ou seja, o defeito estava na derivação e
    não no motor. Fica o registro porque ilustra o que o método faz: obriga a explicitar
    a conta a ponto de o erro, de qualquer um dos dois lados, aparecer.
    """
    mensais = [100.0, 200.0, 300.0, 400.0, 500.0, 600.0,
               700.0, 800.0, 900.0, 1000.0, 1100.0, 1200.0]
    dias = 366
    resultado = run_single_simulation(
        precip_data=np.full(dias, 100.0), lower_tank_vol=200_000.0,
        area=100.0, runoff_coeff=1.0, discard_mm=0.0,
        total_demand_per_day=650.0, rainwater_share=0.5,
        demand_mode="monthly", monthly_demands=mensais,
        start_date_str="01/01/1980",
    )

    assert resultado.potential_potable_savings_pct == pytest.approx(50.0, rel=1e-9)
    assert resultado.avg_pluvial_consumed_l_day == pytest.approx(119_200.0 / dias, rel=1e-9)


# =====================================================================================
# 5. Irrigação — supressão por chuva
# =====================================================================================

def test_irrigacao_e_suprimida_exatamente_nos_dias_de_chuva():
    """A irrigação é suprimida nos dias em que a chuva atinge o limiar configurado.

    Parâmetros: padrão alternado de 5 mm e 0 mm ao longo de 100 dias, limiar de
    supressão 2 mm, irrigação de 150 L/dia.

    Derivação:
        dias com chuva ≥ 2 mm = 50 (os pares do padrão alternado)
        logo a irrigação é suprimida em 50 dias e ativa nos outros 50.

        volume de irrigação suprimido = 50 × 150 = 7.500 L no período
    """
    padrao = np.tile(np.array([5.0, 0.0]), 50)
    configuracao = dict(
        demand=200.0, residents=4, share=0.5, demand_mode="constant",
        irrigation_liters_per_day=150.0, irrigation_rain_threshold_mm=2.0,
        non_potable_indoor_share=0.35, irrigation_potable_backup=True,
    )
    resultado = run_single_simulation(
        precip_data=padrao, lower_tank_vol=50_000.0,
        area=100.0, runoff_coeff=1.0, discard_mm=0.0,
        building_config=configuracao,
    )

    assert resultado.total_irrigation_days_suppressed == 50, (
        f"esperados 50 dias de supressão, obtidos {resultado.total_irrigation_days_suppressed}"
    )


# =====================================================================================
# 6. Reservatório duplo — o recalque é transferência interna
# =====================================================================================

def test_reservatorio_superior_amplo_nao_altera_o_consumo():
    """Um reservatório superior que nunca restringe o recalque não muda o balanço.

    O recalque é transferência entre reservatórios, não entrada nem saída do sistema.
    Se o reservatório superior for grande o bastante para nunca limitar o bombeamento,
    o consumo pluvial total deve ser idêntico ao do arranjo com reservatório único.

    Parâmetros: P = 3 mm/dia constante, A = 100 m², C = 1,0 → 300 L/dia captados;
    demanda pluvial 500 L/dia, mantendo o regime limitado pela oferta.

    Derivação: consumo = captação = 300 L/dia nos dois arranjos.
    """
    comum = dict(precip_data=np.full(365, 3.0), lower_tank_vol=20_000.0,
                 area=100.0, runoff_coeff=1.0, discard_mm=0.0,
                 total_demand_per_day=1000.0, rainwater_share=0.5)

    unico = run_single_simulation(**comum)
    duplo = run_single_simulation(upper_tank_used=True, upper_tank_vol=10_000.0,
                                  pumping_threshold=0.0, **comum)

    assert unico.avg_pluvial_consumed_l_day == pytest.approx(300.0, rel=1e-9)
    assert duplo.avg_pluvial_consumed_l_day == pytest.approx(
        unico.avg_pluvial_consumed_l_day, rel=1e-9
    ), "o reservatório superior alterou o consumo, o que contraria a conservação"
