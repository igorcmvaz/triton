"""Hidráulica do recalque: altura manométrica, vazão e energia específica.

Modelagem física implementada:
    potência hidráulica  P_hid = ρ · g · Q · H
    potência elétrica    P_el  = P_hid / η
    energia por m³       e     = P_el / Q = ρ · g · H / η

A energia específica por m³ elevado depende exclusivamente da altura manométrica (H)
e do rendimento global (η), enquanto a vazão nominal (Q) define o tempo de bombeamento.
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

# Rendimento da BOMBA, isto é, da parte hidráulica: potência hidráulica
# entregue dividida pela potência mecânica no eixo. Não inclui o motor.
#
# A distinção importa. A potência de placa de um motor é, por definição da
# ABNT NBR 17094-2:2016, a potência mecânica no eixo — a mesma norma manda
# marcar o rendimento na placa como grandeza separada. Logo `ρ·g·H/η_bomba`
# devolve energia DE EIXO por metro cúbico, e a energia que o medidor
# registra é essa dividida ainda pelo rendimento do motor.
#
# Conferido contra catálogo: a Dancor CP-4R de 1/2 CV dá 8,4 m³/h a 6 m.c.a.
# e 0,4 m³/h a 22 m.c.a.; ajustada a parábola H = H₀ − kQ², a 12 m.c.a. ela
# entrega 6,65 m³/h, o que são 217 W hidráulicos contra 370 W de placa —
# rendimento de bomba de 0,59 naquele ponto.
RENDIMENTO_DA_BOMBA_PADRAO = 0.55

#: Mantido pelo nome antigo para não quebrar quem importe daqui. É o
#: rendimento da bomba, e não o do conjunto.
RENDIMENTO_PADRAO = RENDIMENTO_DA_BOMBA_PADRAO

# Rendimento nominal mínimo a plena carga de motores de indução monofásicos
# de 2 polos, linha IR1, conforme a Tabela 13 da ABNT NBR 17094-2:2016.
# Motobombas residenciais são de 2 polos, 3.450 rpm.
#
# A linha IR2, de alto rendimento (Tabela 14), dá 72% para o mesmo 1/2 CV.
# Adota-se a IR1 por ser o piso normativo e o que se encontra em motobomba de
# prateleira; quem tiver motor IR2 informa o valor marcado na placa.
RENDIMENTO_DO_MOTOR_IR1_2POLOS = (
    (0.18, 0.500),   # 1/4 CV
    (0.25, 0.555),   # 1/3 CV
    (0.37, 0.605),   # 1/2 CV
    (0.55, 0.640),   # 3/4 CV
    (0.75, 0.693),   # 1 CV
    (1.10, 0.715),   # 1,5 CV
    (1.50, 0.724),   # 2 CV
    (2.20, 0.765),   # 3 CV
    (3.00, 0.775),   # 4 CV
    (3.70, 0.785),   # 5 CV
)

# Tempo perdido em cada partida, em horas, com a bomba consumindo sem entregar
# vazão útil.
TEMPO_DE_PARTIDA_H = 0.03


def energia_especifica_kwh_por_m3(
    altura_manometrica_m: float = ALTURA_MANOMETRICA_PADRAO_M,
    rendimento: float = RENDIMENTO_DA_BOMBA_PADRAO,
    rendimento_do_motor_: float = 1.0,
) -> float:
    """Energia por m³ elevado, em kWh/m³.

    ``e = ρ · g · H / (η_bomba · η_motor)``. Não depende da vazão nem da
    potência: elevar um metro cúbico a uma dada altura custa a mesma energia,
    seja a bomba grande ou pequena. O que muda com a potência é o tempo.

    Com ``rendimento_do_motor_ = 1`` — o padrão — devolve a energia **de eixo**,
    que é o que o rendimento da bomba sozinho permite calcular. Para a energia
    que o medidor registra, informe também o rendimento do motor, que sai de
    :func:`rendimento_do_motor` ou da placa.
    """
    if altura_manometrica_m <= 0:
        return 0.0
    if not 0.0 < rendimento <= 1.0:
        raise ValueError(
            f"Rendimento deve ficar em (0, 1]; recebido {rendimento}. "
            "Use 0,55 para 55%, não 55."
        )
    if not 0.0 < rendimento_do_motor_ <= 1.0:
        raise ValueError(
            f"Rendimento do motor deve ficar em (0, 1]; recebido {rendimento_do_motor_}."
        )
    return (
        DENSIDADE_DA_AGUA_KG_M3
        * GRAVIDADE_M_S2
        * altura_manometrica_m
        / (rendimento * rendimento_do_motor_ * JOULES_POR_KWH)
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


def rendimento_do_motor(potencia_kw: float) -> float:
    """Rendimento do motor pela Tabela 13 da ABNT NBR 17094-2:2016.

    A norma manda, para potências fora da tabela, adotar o maior dos dois
    rendimentos vizinhos quando a potência estiver no ponto médio ou acima, e
    o menor quando estiver abaixo do ponto médio.

    Fora da faixa tabelada, vale o extremo mais próximo.
    """
    if potencia_kw <= 0:
        return RENDIMENTO_DO_MOTOR_IR1_2POLOS[2][1]
    faixas = RENDIMENTO_DO_MOTOR_IR1_2POLOS
    if potencia_kw <= faixas[0][0]:
        return faixas[0][1]
    if potencia_kw >= faixas[-1][0]:
        return faixas[-1][1]
    for (p_inf, e_inf), (p_sup, e_sup) in zip(faixas, faixas[1:]):
        if p_inf <= potencia_kw <= p_sup:
            meio = (p_inf + p_sup) / 2.0
            return e_sup if potencia_kw >= meio else e_inf
    return RENDIMENTO_DA_BOMBA_PADRAO


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


def energia_especifica_a_partir_da_vazao(
    potencia_kw: float,
    vazao_l_h: float,
    rendimento_do_motor_: float = 1.0,
) -> float:
    """Energia por m³ quando a vazão de operação é conhecida.

    ``e_eixo = P / Q``, e ``e_elétrica = P / (Q · η_motor)``.

    A potência de placa é a potência mecânica no **eixo**, por definição da ABNT
    NBR 17094-2:2016, que manda marcar o rendimento na placa como grandeza
    separada. O rendimento **da bomba** já está embutido no fato de um motor de
    P kW no eixo fazer a bomba entregar Q m³/h naquela altura: dividir por ele
    outra vez contaria a perda hidráulica duas vezes. O rendimento do **motor**,
    esse sim, ainda falta, e é o que separa a energia de eixo da energia que o
    medidor registra.

    Com ``rendimento_do_motor_ = 1`` — o padrão — devolve energia de eixo.
    """
    if potencia_kw <= 0 or vazao_l_h <= 0:
        return 0.0
    if not 0.0 < rendimento_do_motor_ <= 1.0:
        raise ValueError(
            f"Rendimento do motor deve ficar em (0, 1]; recebido {rendimento_do_motor_}."
        )
    return potencia_kw / (vazao_l_h / 1000.0) / rendimento_do_motor_

