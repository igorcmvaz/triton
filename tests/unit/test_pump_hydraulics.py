"""Verificação da hidráulica do recalque.

Até a versão 5.0.8 a bomba era um número solto: vazão de 2.280 L/h e rendimento
de 55%, fixos, qualquer que fosse a potência escolhida. Disso decorriam quatro
defeitos, e estes testes fixam a correção de cada um.

1. A vazão não acompanhava a potência, de modo que dobrar a potência dobrava a
   energia — quando na prática a bomba maior recalca o mesmo volume em menos
   tempo.
2. A altura manométrica não existia como parâmetro, embora seja o que governa o
   consumo. O par de valores fixos implicava 67 metros.
3. O exportador CAD tinha uma segunda tabela de vazão, que discordava da
   primeira para a mesma bomba.
4. A conta de energia dividia pelo rendimento uma segunda vez, superestimando o
   bombeamento em 1/η.
"""

from __future__ import annotations

import pytest

from netuno.core.pump_energy import CV_TO_KW, consumo_especifico_padrao_kwh_por_m3
from netuno.core.pump_hydraulics import (
    ALTURA_MANOMETRICA_PADRAO_M,
    energia_especifica_a_partir_da_vazao,
    energia_especifica_kwh_por_m3,
    ponto_de_operacao,
    rendimento_tipico,
    vazao_l_por_h,
)


def test_energia_especifica_e_rho_g_h_sobre_eta():
    """Confere contra a conta feita à mão, em unidades do SI."""
    esperado = 1000.0 * 9.81 * 12.0 / (0.55 * 3.6e6)
    assert energia_especifica_kwh_por_m3(12.0, 0.55) == pytest.approx(esperado)


def test_energia_especifica_nao_depende_da_potencia():
    """É o ponto central: elevar 1 m³ a uma altura custa o mesmo, com bomba grande ou pequena.

    O que muda com a potência é o tempo de operação, não o consumo por metro
    cúbico. Uma bomba superdimensionada custa mais no investimento, não na conta
    de luz por m³ elevado.
    """
    a = ponto_de_operacao(0.25 * CV_TO_KW, 12.0, rendimento=0.55)
    b = ponto_de_operacao(2.00 * CV_TO_KW, 12.0, rendimento=0.55)
    assert a.energia_especifica_kwh_m3 == pytest.approx(b.energia_especifica_kwh_m3)
    # Mas a bomba grande recalca muito mais depressa.
    assert b.vazao_l_h > 7 * a.vazao_l_h


def test_a_vazao_acompanha_a_potencia():
    """Era o defeito principal: 2.280 L/h valia de 1/4 a 2 CV."""
    vazoes = [vazao_l_por_h(cv * CV_TO_KW, 12.0, 0.55) for cv in (0.25, 0.5, 1.0, 2.0)]
    assert vazoes == sorted(vazoes)
    # Proporcional à potência, para altura e rendimento fixos.
    assert vazoes[3] == pytest.approx(8 * vazoes[0], rel=1e-6)


def test_a_vazao_cai_quando_a_altura_sobe():
    alta = vazao_l_por_h(0.5 * CV_TO_KW, 8.0, 0.55)
    baixa = vazao_l_por_h(0.5 * CV_TO_KW, 30.0, 0.55)
    assert alta > 3 * baixa


def test_rendimento_cresce_com_o_porte():
    """Tratar toda bomba com 55% penalizava a grande, que é a mais eficiente."""
    valores = [rendimento_tipico(cv * CV_TO_KW) for cv in (0.25, 0.5, 1.0, 1.5, 2.0)]
    assert valores == sorted(valores)
    assert all(0.3 < v <= 0.8 for v in valores)


def test_rendimento_fora_da_faixa_falha_com_mensagem_util():
    """O engano provável é escrever 55 em vez de 0,55."""
    with pytest.raises(ValueError, match="0,55"):
        energia_especifica_kwh_por_m3(12.0, 55.0)


def test_energia_pela_vazao_nao_divide_por_eta_de_novo():
    """A potência de placa é o que o motor consome: e = P/Q, e nada mais.

    A conta anterior fazia P x horas / η, dividindo pela perda uma segunda vez.
    Com η de 60%, superestimava em 67%.
    """
    potencia_kw, vazao_l_h = 0.7355, 3000.0
    correta = energia_especifica_a_partir_da_vazao(potencia_kw, vazao_l_h)
    assert correta == pytest.approx(0.7355 / 3.0)

    antiga = potencia_kw * (1000.0 / vazao_l_h) / 0.60
    assert antiga == pytest.approx(correta / 0.60)


def test_as_duas_formas_coincidem_no_ponto_de_operacao():
    """ρ·g·H/η e P/Q dão o mesmo quando Q é a vazão que a bomba entrega em H.

    Se divergirem, alguma das duas está errada — e é essa coerência que permite
    usar uma quando a vazão é declarada e a outra quando não é.
    """
    potencia_kw, altura, eta = 0.5 * CV_TO_KW, 12.0, 0.55
    vazao = vazao_l_por_h(potencia_kw, altura, eta)
    assert energia_especifica_a_partir_da_vazao(potencia_kw, vazao) == pytest.approx(
        energia_especifica_kwh_por_m3(altura, eta), rel=1e-9
    )


def test_altura_padrao_e_de_casa_e_nao_de_predio():
    """O par de valores fixos anterior implicava 67 m, cinco vezes o desnível real."""
    assert 8.0 <= ALTURA_MANOMETRICA_PADRAO_M <= 15.0
    implicada_pelo_valor_antigo = 0.3334 * 0.55 / (1000.0 * 9.81 / 3.6e6)
    assert implicada_pelo_valor_antigo > 4 * ALTURA_MANOMETRICA_PADRAO_M


def test_consumo_de_recurso_e_plausivel_para_recalque_residencial():
    """Entre 0,05 e 0,20 kWh/m³ para um desnível de casa.

    Fora dessa faixa o número denuncia altura ou rendimento errados. O valor
    antigo, de 0,40, ficava muito acima.
    """
    valor = consumo_especifico_padrao_kwh_por_m3()
    assert 0.05 < valor < 0.20, valor


def test_o_exportador_cad_usa_a_mesma_vazao():
    """Havia uma segunda tabela ali, com 2,4 m³/h para meio CV."""
    from netuno.core.cad_exporter import calculate_forchheimer_pumping_diameters

    resultado = calculate_forchheimer_pumping_diameters(pump_hp="1/2", daily_pumped_volume_l=1000.0)
    esperado_m3_h = vazao_l_por_h(0.5 * CV_TO_KW) / 1000.0
    obtido = resultado.get("flow_m3_h", resultado.get("q_m3_h"))
    assert obtido == pytest.approx(esperado_m3_h, rel=1e-6)
