"""Hidráulica do recalque: altura manométrica, vazão e energia específica.

Até a versão 5.0.8 a energia de bombeamento saía de dois números fixos — vazão
de 2.280 L/h e rendimento de 55% — que não mudavam com a potência escolhida.
Três consequências seguiam disso, e as três estão corrigidas aqui.

**A vazão não acompanhava a potência.** Como o tempo de operação é volume
dividido por vazão, e a vazão era constante, dobrar a potência dobrava a energia.
Na realidade uma bomba maior recalca o mesmo volume em menos tempo, e o consumo
cresce muito menos que a potência.

**A altura manométrica não existia como parâmetro.** Ela é o que de fato governa
o consumo, e estava embutida nos dois números fixos. O par de 2.280 L/h com 55%
implica altura de **67 metros** — altura de edifício alto, não de casa com
cisterna enterrada e caixa no telhado, que fica entre 10 e 15 metros.

**O exportador CAD tinha outra tabela ainda**, com 2.400 L/h para meio CV,
escalando com a potência. Dois caminhos do mesmo programa discordavam sobre a
vazão da mesma bomba.

A física é simples e dispensa tabela:

    potência hidráulica  P_hid = ρ · g · Q · H
    potência elétrica    P_el  = P_hid / η
    energia por m³       e     = P_el / Q = ρ · g · H / η

**A energia específica não depende da vazão.** Ela depende de altura e
rendimento apenas. A vazão determina quanto tempo a bomba fica ligada, e portanto
o número de partidas, mas não o consumo por metro cúbico elevado. É por isso que
uma bomba superdimensionada não gasta mais energia por m³ — ela gasta o mesmo,
em menos tempo, e apenas paga mais caro no investimento.
"""

from __future__ import annotations

from dataclasses import dataclass

DENSIDADE_DA_AGUA_KG_M3 = 1000.0
GRAVIDADE_M_S2 = 9.81
JOULES_POR_KWH = 3.6e6

# Altura manométrica de recurso, em metros de coluna d'água.
#
# Casa de dois pavimentos com cisterna enterrada: cerca de 8 m de desnível
# geométrico entre o nível de sucção e a entrada do reservatório superior, mais
# perdas de carga na ordem de 30% em tubulação corretamente dimensionada. Daí os
# 10 a 12 m. Adota-se 12, o extremo conservador da faixa.
#
# É valor de recurso: quem conhece o desnível do projeto deve informá-lo, porque
# é o parâmetro que mais pesa no consumo.
ALTURA_MANOMETRICA_PADRAO_M = 12.0

# Rendimento do conjunto motobomba, já incluindo motor e parte hidráulica.
# Motobombas residenciais de meio a um CV ficam entre 40% e 60% no ponto de
# operação; o rendimento cresce com o porte.
RENDIMENTO_PADRAO = 0.55

# Tempo perdido em cada partida, em horas, com a bomba consumindo sem entregar
# vazão útil.
TEMPO_DE_PARTIDA_H = 0.03


def energia_especifica_kwh_por_m3(
    altura_manometrica_m: float = ALTURA_MANOMETRICA_PADRAO_M,
    rendimento: float = RENDIMENTO_PADRAO,
) -> float:
    """Energia elétrica por m³ elevado, em kWh/m³.

    ``e = ρ · g · H / η``. Não depende da vazão nem da potência: elevar um metro
    cúbico a uma dada altura custa a mesma energia, seja a bomba grande ou
    pequena. O que muda com a potência é o tempo, não o consumo específico.
    """
    if altura_manometrica_m <= 0:
        return 0.0
    if not 0.0 < rendimento <= 1.0:
        raise ValueError(
            f"Rendimento deve ficar em (0, 1]; recebido {rendimento}. "
            "Use 0,55 para 55%, não 55."
        )
    return (
        DENSIDADE_DA_AGUA_KG_M3
        * GRAVIDADE_M_S2
        * altura_manometrica_m
        / (rendimento * JOULES_POR_KWH)
    )


def vazao_l_por_h(
    potencia_kw: float,
    altura_manometrica_m: float = ALTURA_MANOMETRICA_PADRAO_M,
    rendimento: float = RENDIMENTO_PADRAO,
) -> float:
    """Vazão que a bomba entrega naquela altura, em L/h.

    ``Q = P · η / (ρ · g · H)``. É aqui que a potência entra: ela determina a
    vazão, e portanto o tempo de operação e o número de partidas.
    """
    if potencia_kw <= 0 or altura_manometrica_m <= 0:
        return 0.0
    vazao_m3_s = (potencia_kw * 1000.0 * rendimento) / (
        DENSIDADE_DA_AGUA_KG_M3 * GRAVIDADE_M_S2 * altura_manometrica_m
    )
    return vazao_m3_s * 3600.0 * 1000.0


def rendimento_tipico(potencia_kw: float) -> float:
    """Rendimento do conjunto em função do porte.

    Motobombas pequenas são menos eficientes: o rendimento cresce com a
    potência. Tratar todas com 55% penaliza a bomba grande, que na prática é a
    mais eficiente. A faixa adotada, de 40% a 65%, cobre o que se observa em
    motobombas residenciais e prediais de pequeno porte.
    """
    if potencia_kw <= 0:
        return RENDIMENTO_PADRAO
    if potencia_kw <= 0.20:      # até cerca de 1/4 CV
        return 0.40
    if potencia_kw <= 0.40:      # até cerca de 1/2 CV
        return 0.50
    if potencia_kw <= 0.80:      # até cerca de 1 CV
        return 0.55
    if potencia_kw <= 1.20:      # até cerca de 1,5 CV
        return 0.60
    return 0.65


@dataclass(frozen=True)
class PontoDeOperacao:
    """O que a bomba faz naquela altura, com a potência escolhida."""

    potencia_kw: float
    altura_manometrica_m: float
    rendimento: float
    vazao_l_h: float
    energia_especifica_kwh_m3: float

    @property
    def horas_por_m3(self) -> float:
        if self.vazao_l_h <= 0:
            return 0.0
        return 1000.0 / self.vazao_l_h


def ponto_de_operacao(
    potencia_kw: float,
    altura_manometrica_m: float = ALTURA_MANOMETRICA_PADRAO_M,
    rendimento: float | None = None,
) -> PontoDeOperacao:
    """Resolve vazão, rendimento e energia específica a partir da potência.

    Quando ``rendimento`` é omitido, adota-se o típico para aquele porte.
    """
    eta = rendimento if rendimento is not None else rendimento_tipico(potencia_kw)
    return PontoDeOperacao(
        potencia_kw=potencia_kw,
        altura_manometrica_m=altura_manometrica_m,
        rendimento=eta,
        vazao_l_h=vazao_l_por_h(potencia_kw, altura_manometrica_m, eta),
        energia_especifica_kwh_m3=energia_especifica_kwh_por_m3(altura_manometrica_m, eta),
    )


def energia_especifica_a_partir_da_vazao(potencia_kw: float, vazao_l_h: float) -> float:
    """Energia por m³ quando a vazão de operação é conhecida: ``e = P / Q``.

    A potência de placa é o que o motor **consome**. O rendimento já está
    embutido no fato de uma bomba de P kW entregar Q m³/h naquela altura, de
    modo que dividir por η outra vez conta a perda duas vezes.

    Era esse o defeito da conta anterior, que fazia ``P x horas / η`` e
    superestimava a energia de bombeamento em ``1/η`` — 67% com o rendimento de
    60% do teste, 82% com os 55% do padrão antigo.
    """
    if potencia_kw <= 0 or vazao_l_h <= 0:
        return 0.0
    return potencia_kw / (vazao_l_h / 1000.0)

