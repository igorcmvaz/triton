"""Pressurizadores residenciais de catálogo, e a energia que cada um gasta.

Um pressurizador não trabalha no ponto de melhor rendimento. Ele liga a cada
descarga e fica ligado enquanto a caixa acoplada enche: a energia depende do
tempo ligado, e o tempo depende de quanta água a bomba entrega na pressão de
trabalho. Por isso a escolha do modelo pesa mais que a pressão.

O cálculo usa só dados de fabricante:

- a **curva vazão × pressão** dá a vazão que a bomba consegue entregar na
  pressão de trabalho ``H``;
- a vazão efetiva ``Q`` é a menor entre essa e a do ponto de uso: a boia de uma
  caixa acoplada estrangula a entrada, e bomba maior não enche a caixa mais
  depressa. A ABNT NBR 5626:2020 (6.7.1) deixa ao projeto explicitar as vazões
  nos pontos de utilização, sem tabela; o padrão de 0,15 L/s (9 L/min) é a vazão
  de projeto da bacia com caixa de descarga na Tabela A.1 da edição de 1998, que
  a de 2020 substituiu, conferida na reprodução da documentação técnica UnMEP
  («Vazões e pesos relativos»);
- o **tempo ligado** é ``V/Q``, mais o retardo de desligamento de cada partida
  nos controles eletrônicos;
- a **potência elétrica** é a potência de placa, que é de eixo, dividida pelo
  rendimento do motor da Tabela 13 da ABNT NBR 17094-2.

É o que pede o item 6.5.11.12 da ABNT NBR 5626:2020: o consumo de energia das
bombas de pressurização deve ser minimizado pela escolha do modelo de maior
rendimento entre as alternativas. A mesma norma exige no mínimo duas bombas
(6.5.11.2) e limita a pressão estática nos pontos de utilização a 40 m.c.a.
(6.9.4), com pressão dinâmica mínima de 1 m.c.a. (6.9.2).

A potência de placa é a do ponto nominal, e em vazão baixa o motor puxa um pouco
menos: a estimativa tende a superestimar a energia, e ordena os modelos entre
si melhor do que prevê a leitura de um medidor.

Fontes, todas guardadas em Material_Referencia/Documentos_Consultados/04_EPD_e_Fabricantes:
Komeco (manual TP 820T e TP 825T G2, versão 15.05.07); Cardal (manual do
Pressurizador Potenza, IM 311); Jacuzzi (manual AcquaHouse, mar. 2017, curvas
ensaiadas no Laboratório de Etiquetagem de Bombas da UNIFEI); Syllent/Eberle
(manual Impulse Press, Des. 3I4743); Rowa (manual Linha Tradicional Max Press E
e ficha do Max Press 20E).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from triton.core.pump_hydraulics import rendimento_do_motor

CV_TO_KW = 0.735499

#: Controle de partida
PRESSOSTATO = "pressostato"            # chave de pressão mecânica, com cuba
ELETRONICO = "eletronico"              # transdutor e placa, com retardo
FLUXOSTATO = "fluxostato"              # liga com fluxo, desliga sem fluxo

PERSONALIZADO = "personalizado"


@dataclass(frozen=True)
class Pressurizador:
    chave: str
    rotulo: str
    potencia_cv: float
    controle: str
    #: Curva de catálogo: pares (vazão em L/min, pressão em m.c.a.), vazão crescente.
    curva: Tuple[Tuple[float, float], ...]
    liga_m: Optional[float] = None
    desliga_m: Optional[float] = None
    #: Segundos que a bomba segue ligada depois de fechado o último ponto.
    retardo_s: float = 0.0
    fonte: str = ""

    @property
    def potencia_kw(self) -> float:
        return self.potencia_cv * CV_TO_KW

    @property
    def pressao_maxima_m(self) -> float:
        return max(h for _, h in self.curva)

    @property
    def potencia_eletrica_kw(self) -> float:
        return self.potencia_kw / rendimento_do_motor(self.potencia_kw)

    def vazao_l_min(self, pressao_m: float) -> float:
        """Vazão da curva na pressão pedida; zero acima da pressão máxima."""
        return vazao_na_curva(self.curva, pressao_m)


def vazao_na_curva(curva: Sequence[Tuple[float, float]], pressao_m: float) -> float:
    pontos = sorted(curva)
    if pressao_m >= pontos[0][1]:
        return 0.0 if pressao_m > pontos[0][1] else pontos[0][0]
    for (q1, h1), (q2, h2) in zip(pontos, pontos[1:]):
        if h2 <= pressao_m <= h1:
            if h1 == h2:
                return q2
            return q1 + (q2 - q1) * (h1 - pressao_m) / (h1 - h2)
    return pontos[-1][0]


CATALOGO: Tuple[Pressurizador, ...] = (
    Pressurizador(
        "komeco_tp820t", "Komeco TP 820T, 1/4 CV", 0.25, PRESSOSTATO,
        ((0.0, 27.0), (40.0, 0.0)), liga_m=12.0, desliga_m=24.0,
        fonte="Komeco, manual TP 820T/825T G2: ficha técnica e gráfico vazão × pressão"),
    Pressurizador(
        "cardal_potenza", "Cardal Potenza, 1/3 CV", 1.0 / 3.0, FLUXOSTATO,
        ((0.0, 20.0), (188.0, 0.0)),
        fonte="Cardal, manual do Pressurizador Potenza: especificações e figura 8"),
    Pressurizador(
        "komeco_tp825t", "Komeco TP 825T, 1/2 CV", 0.5, PRESSOSTATO,
        ((0.0, 43.0), (50.0, 0.0)), liga_m=20.0, desliga_m=30.0,
        fonte="Komeco, manual TP 820T/825T G2: ficha técnica e gráfico vazão × pressão"),
    Pressurizador(
        "jacuzzi_5aqh1", "Jacuzzi AcquaHouse 5AQH1, 1/2 CV", 0.5, PRESSOSTATO,
        ((0.0, 33.162), (6.52, 29.52), (12.48, 25.511), (18.08, 22.05),
         (25.02, 19.003), (30.92, 16.515), (36.98, 14.1), (42.63, 11.627),
         (48.95, 8.832), (52.88, 5.293)),
        liga_m=15.3,
        fonte="Jacuzzi, manual AcquaHouse (2017), tabela 3.2 ensaiada na UNIFEI, modelo 220 V"),
    Pressurizador(
        "syllent_impulse", "Syllent Impulse Press, 1/2 CV", 0.5, ELETRONICO,
        ((0.0, 20.0), (7.0, 18.0), (17.0, 16.0), (22.0, 14.0), (27.0, 12.0),
         (30.0, 10.0), (34.0, 8.0), (39.0, 6.0), (41.0, 4.0)),
        retardo_s=10.0,
        fonte="Syllent/Eberle, manual Impulse Press: tabela 3 e retardo de 10 s da seção Operação"),
    Pressurizador(
        "rowa_maxpress20e", "Rowa Max Press 20E, 1/2 CV", 0.5, ELETRONICO,
        ((0.0, 20.0), (83.3, 7.0)),
        fonte="Rowa, manual Max Press E e ficha do 20E: 20 m.c.a. máx., 5.000 L/h a 7 m.c.a."),
)

POR_CHAVE = {p.chave: p for p in CATALOGO}
PADRAO = "komeco_tp820t"

#: Vazão do ponto de uso, em L/min: 0,15 L/s da bacia com caixa de descarga
#: (ABNT NBR 5626:1998, Tabela A.1; a edição de 2020 deixa a vazão ao projeto).
VAZAO_DO_PONTO_PADRAO_L_MIN = 9.0


@dataclass
class EnergiaDoPressurizador:
    chave: str
    rotulo: str
    atende: bool
    vazao_l_min: float          # efetiva: a menor entre a bomba e o ponto
    vazao_da_bomba_l_min: float
    horas_ano: float
    partidas_ano: float
    kwh_ano: float
    kwh_por_m3: float


def _horas(volume_m3_ano, q_l_min, partidas_ano, retardo_s):
    if q_l_min <= 0:
        return 0.0
    return volume_m3_ano * 1000.0 / q_l_min / 60.0 + partidas_ano * retardo_s / 3600.0


def energia(p: Pressurizador, volume_m3_ano: float, pressao_m: float,
            partidas_ano: float,
            vazao_do_ponto_l_min: float = VAZAO_DO_PONTO_PADRAO_L_MIN) -> EnergiaDoPressurizador:
    """Energia anual de um modelo de catálogo na pressão de trabalho pedida."""
    q_bomba = p.vazao_l_min(pressao_m)
    q = min(q_bomba, vazao_do_ponto_l_min) if vazao_do_ponto_l_min > 0 else q_bomba
    horas = _horas(volume_m3_ano, q, partidas_ano, p.retardo_s)
    kwh = p.potencia_eletrica_kw * horas
    return EnergiaDoPressurizador(
        p.chave, p.rotulo, q_bomba > 0, q, q_bomba, horas, partidas_ano, kwh,
        kwh / volume_m3_ano if volume_m3_ano > 0 else 0.0)


def energia_personalizada(potencia_kw: float, vazao_l_min: float, retardo_s: float,
                          volume_m3_ano: float, partidas_ano: float,
                          motor_eff: Optional[float] = None) -> EnergiaDoPressurizador:
    """O mesmo cálculo, com a potência, a vazão e o retardo digitados."""
    eta = motor_eff if motor_eff and motor_eff > 0 else rendimento_do_motor(potencia_kw)
    horas = _horas(volume_m3_ano, vazao_l_min, partidas_ano, retardo_s)
    kwh = potencia_kw / eta * horas if potencia_kw > 0 else 0.0
    return EnergiaDoPressurizador(
        PERSONALIZADO, "Personalizado", vazao_l_min > 0, vazao_l_min, vazao_l_min, horas,
        partidas_ano, kwh, kwh / volume_m3_ano if volume_m3_ano > 0 else 0.0)


def comparar(volume_m3_ano: float, pressao_m: float, partidas_ano: float,
             vazao_do_ponto_l_min: float = VAZAO_DO_PONTO_PADRAO_L_MIN):
    """Todos os modelos do catálogo, do que menos gasta ao que mais gasta."""
    lista = [energia(p, volume_m3_ano, pressao_m, partidas_ano, vazao_do_ponto_l_min)
             for p in CATALOGO]
    return sorted(lista, key=lambda e: (not e.atende, e.kwh_ano))


def menor_que_atende(pressao_m: float,
                     vazao_do_ponto_l_min: float = VAZAO_DO_PONTO_PADRAO_L_MIN) -> Optional[Pressurizador]:
    """O modelo de menor potência que entrega a vazão do ponto na pressão pedida."""
    aptos = [p for p in CATALOGO if p.vazao_l_min(pressao_m) >= vazao_do_ponto_l_min]
    return min(aptos, key=lambda p: (p.potencia_cv, -p.vazao_l_min(pressao_m))) if aptos else None
