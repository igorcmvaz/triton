# -*- coding: utf-8 -*-
"""Demanda diária sorteada, para medir quanto a incerteza do consumo desloca o resultado.

O consumo de uma edificação não é o mesmo todo dia: varia com o número de pessoas
em casa, com o fim de semana, com a viagem de férias. Silva e Ghisi (2016)
mediram o efeito dessa variação sobre o dimensionamento e encontraram
deslocamentos de até 4,8 pontos percentuais no potencial de economia e de até
9,4% no volume ideal — o que é grande diante das diferenças que separam um
volume do seguinte.

Este módulo sorteia a demanda dia a dia e roda a simulação muitas vezes, para que
o resultado apareça como faixa, e não como número único.

**A variação diária sozinha quase não move o resultado.** Sorteada de forma
independente a cada dia, ela se cancela ao longo de uma série de trinta anos: com
coeficiente de variação de 20% o potencial de economia oscila cerca de um décimo
de ponto percentual. O que move o resultado é a incerteza do **nível** da
demanda — não saber quanto a edificação consome, em média —, e por isso o perfil
tem os dois parâmetros separados: ``cv_pct``, do dia para o dia, e
``incerteza_da_media_pct``, sorteada uma vez por realização.

**Fica fora da interface, de propósito.** São muitos parâmetros e a leitura pede
cuidado; na tela, ele confundiria mais do que ajudaria. O acesso é pela linha de
comando (`triton stochastic-demand`) e por quem escreve script.

A demanda sorteada entra no motor pelo caminho que já existe, o de demanda
diária: o vetor sorteado vira ``daily_demands``, com ``demand_mode='daily'``.
Nenhuma linha do balanço hídrico muda por causa deste módulo.
"""

from __future__ import annotations

import math
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence

import numpy as np

from triton.core.simulation import run_single_simulation

DISTRIBUICOES = ("normal", "lognormal", "uniforme", "triangular")


@dataclass(frozen=True)
class PerfilDeConsumo:
    """Como o consumo diário varia em torno da média."""
    media_l_dia: float
    cv_pct: float = 20.0
    distribuicao: str = "lognormal"
    #: Probabilidade de um dia sem consumo nenhum — viagem, casa vazia, feriado.
    probabilidade_de_ausencia_pct: float = 0.0
    #: Piso e teto do sorteio, para o consumo não virar valor implausível.
    minimo_l_dia: float = 0.0
    maximo_l_dia: Optional[float] = None
    #: Incerteza do **nível** da demanda, em percentual da média, sorteada uma vez
    #: por realização. É ela que move o resultado: o ruído de um dia para o outro
    #: se cancela ao longo de uma série longa, e a incerteza de quanto a
    #: edificação consome, em média, não se cancela nunca.
    incerteza_da_media_pct: float = 0.0

    def validar(self) -> None:
        if self.media_l_dia <= 0:
            raise ValueError("A média de consumo diário tem de ser positiva.")
        if self.cv_pct < 0:
            raise ValueError("O coeficiente de variação não pode ser negativo.")
        if not 0.0 <= self.probabilidade_de_ausencia_pct <= 100.0:
            raise ValueError("A probabilidade de ausência vai de 0 a 100%.")
        if self.distribuicao not in DISTRIBUICOES:
            raise ValueError(f"Distribuição desconhecida: {self.distribuicao}. "
                             f"Use uma de {', '.join(DISTRIBUICOES)}.")
        if self.maximo_l_dia is not None and self.maximo_l_dia < self.minimo_l_dia:
            raise ValueError("O teto do consumo não pode ser menor que o piso.")
        if self.incerteza_da_media_pct < 0:
            raise ValueError("A incerteza da média não pode ser negativa.")

    def com_media(self, media_l_dia: float) -> "PerfilDeConsumo":
        """O mesmo perfil, com outra média — usado a cada realização."""
        return PerfilDeConsumo(
            media_l_dia=media_l_dia, cv_pct=self.cv_pct, distribuicao=self.distribuicao,
            probabilidade_de_ausencia_pct=self.probabilidade_de_ausencia_pct,
            minimo_l_dia=self.minimo_l_dia, maximo_l_dia=self.maximo_l_dia,
            incerteza_da_media_pct=0.0)


def sortear_media(perfil: PerfilDeConsumo, gerador: np.random.Generator) -> float:
    """A média desta realização, quando o nível da demanda também é incerto."""
    if perfil.incerteza_da_media_pct <= 0:
        return perfil.media_l_dia
    desvio = perfil.media_l_dia * perfil.incerteza_da_media_pct / 100.0
    return float(max(0.0, gerador.normal(perfil.media_l_dia, desvio)))


def sortear_demanda(perfil: PerfilDeConsumo, n_dias: int,
                    gerador: np.random.Generator) -> np.ndarray:
    """Um vetor de consumo diário, em litros por dia."""
    perfil.validar()
    media, desvio = perfil.media_l_dia, perfil.media_l_dia * perfil.cv_pct / 100.0
    if desvio == 0:
        valores = np.full(n_dias, media, dtype=float)
    elif perfil.distribuicao == "normal":
        valores = gerador.normal(media, desvio, n_dias)
    elif perfil.distribuicao == "lognormal":
        # Parâmetros da lognormal que devolvem a média e o desvio pedidos.
        sigma = math.sqrt(math.log(1.0 + (desvio / media) ** 2))
        mu = math.log(media) - sigma ** 2 / 2.0
        valores = gerador.lognormal(mu, sigma, n_dias)
    elif perfil.distribuicao == "uniforme":
        meia_faixa = desvio * math.sqrt(3.0)          # devolve o CV pedido
        valores = gerador.uniform(media - meia_faixa, media + meia_faixa, n_dias)
    else:                                              # triangular simétrica
        meia_faixa = desvio * math.sqrt(6.0)
        valores = gerador.triangular(media - meia_faixa, media, media + meia_faixa, n_dias)

    if perfil.probabilidade_de_ausencia_pct > 0:
        ausentes = gerador.random(n_dias) < perfil.probabilidade_de_ausencia_pct / 100.0
        valores = np.where(ausentes, 0.0, valores)

    valores = np.clip(valores, perfil.minimo_l_dia,
                      perfil.maximo_l_dia if perfil.maximo_l_dia is not None else np.inf)
    return valores


def _percentis(valores: Sequence[float]) -> Dict[str, float]:
    ordenados = np.asarray(sorted(valores), dtype=float)
    return {
        "media": round(float(np.mean(ordenados)), 3),
        "desvio": round(float(np.std(ordenados, ddof=1)) if len(ordenados) > 1 else 0.0, 3),
        "p5": round(float(np.percentile(ordenados, 5)), 3),
        "p50": round(float(np.percentile(ordenados, 50)), 3),
        "p95": round(float(np.percentile(ordenados, 95)), 3),
        "minimo": round(float(ordenados[0]), 3),
        "maximo": round(float(ordenados[-1]), 3),
        "amplitude": round(float(ordenados[-1] - ordenados[0]), 3),
    }


def simular(
    precipitacao: Sequence[float],
    volume_l: float,
    perfil: PerfilDeConsumo,
    parametros_da_simulacao: dict,
    *,
    realizacoes: int = 100,
    semente: Optional[int] = 42,
) -> Dict[str, object]:
    """Roda a simulação muitas vezes, cada uma com a demanda sorteada de novo.

    Devolve os percentis do potencial de economia, dos dias plenamente atendidos e
    do extravasamento, mais o resultado determinístico com a demanda média, que é
    a referência de comparação.
    """
    perfil.validar()
    if realizacoes < 1:
        raise ValueError("É preciso ao menos uma realização.")
    serie = np.asarray(precipitacao, dtype=float)
    parametros = dict(parametros_da_simulacao)
    parametros.pop("total_demand_per_day", None)
    parametros.pop("daily_demands", None)
    parametros.pop("daily_residents", None)
    parametros.pop("demand_mode", None)

    determinístico = run_single_simulation(
        precip_data=serie, lower_tank_vol=float(volume_l),
        total_demand_per_day=perfil.media_l_dia, **parametros)

    gerador = np.random.default_rng(semente)
    potenciais: List[float] = []
    plenos: List[float] = []
    extravasados: List[float] = []
    consumos: List[float] = []
    for _ in range(realizacoes):
        desta_vez = perfil.com_media(sortear_media(perfil, gerador))
        demanda = sortear_demanda(desta_vez, len(serie), gerador)
        r = run_single_simulation(
            precip_data=serie, lower_tank_vol=float(volume_l),
            demand_mode="daily", daily_demands=demanda.tolist(),
            daily_residents=[1.0], total_demand_per_day=perfil.media_l_dia,
            **parametros)
        potenciais.append(r.potential_potable_savings_pct)
        plenos.append(r.pct_days_full_satisfaction)
        extravasados.append(r.avg_spilled_l_day)
        consumos.append(float(np.mean(demanda)))

    return {
        "volume_l": float(volume_l),
        "realizacoes": realizacoes,
        "semente": semente,
        "perfil": {
            "media_l_dia": perfil.media_l_dia, "cv_pct": perfil.cv_pct,
            "distribuicao": perfil.distribuicao,
            "probabilidade_de_ausencia_pct": perfil.probabilidade_de_ausencia_pct,
            "incerteza_da_media_pct": perfil.incerteza_da_media_pct,
        },
        "consumo_medio_sorteado_l_dia": round(statistics.fmean(consumos), 2),
        "deterministico": {
            "potencial_pct": round(determinístico.potential_potable_savings_pct, 3),
            "dias_plenos_pct": round(determinístico.pct_days_full_satisfaction, 3),
            "extravasado_l_dia": round(determinístico.avg_spilled_l_day, 3),
        },
        "potencial_pct": _percentis(potenciais),
        "dias_plenos_pct": _percentis(plenos),
        "extravasado_l_dia": _percentis(extravasados),
    }


def volume_ideal_por_realizacao(
    precipitacao: Sequence[float],
    perfil: PerfilDeConsumo,
    parametros_da_simulacao: dict,
    *,
    volumes_l: Sequence[float],
    limiar_ganho_pct_m3: float = 1.0,
    realizacoes: int = 30,
    semente: Optional[int] = 42,
) -> Dict[str, object]:
    """O volume ideal de cada realização: mede o quanto a decisão de projeto oscila.

    É a segunda metade do achado de Silva e Ghisi: a incerteza do consumo desloca
    não só o desempenho, mas o volume que se escolheria.
    """
    perfil.validar()
    serie = np.asarray(precipitacao, dtype=float)
    parametros = dict(parametros_da_simulacao)
    for chave in ("total_demand_per_day", "daily_demands", "daily_residents", "demand_mode"):
        parametros.pop(chave, None)

    gerador = np.random.default_rng(semente)
    ideais: List[float] = []
    for _ in range(realizacoes):
        desta_vez = perfil.com_media(sortear_media(perfil, gerador))
        demanda = sortear_demanda(desta_vez, len(serie), gerador).tolist()
        anterior = None
        escolhido = float(volumes_l[-1])
        for i, v in enumerate(volumes_l):
            pot = run_single_simulation(
                precip_data=serie, lower_tank_vol=float(v), demand_mode="daily",
                daily_demands=demanda, daily_residents=[1.0],
                total_demand_per_day=perfil.media_l_dia, **parametros
            ).potential_potable_savings_pct
            if anterior is not None:
                passo_m3 = (float(volumes_l[i]) - float(volumes_l[i - 1])) / 1000.0
                if passo_m3 > 0 and (pot - anterior) / passo_m3 <= limiar_ganho_pct_m3:
                    escolhido = float(v)
                    break
            anterior = pot
        ideais.append(escolhido)
    return {"realizacoes": realizacoes, "semente": semente,
            "volume_ideal_l": _percentis(ideais),
            "volumes_distintos": sorted(set(ideais))}
