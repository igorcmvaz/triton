# -*- coding: utf-8 -*-
"""A série de chuva que você tem é longa o bastante para este projeto?

É a pergunta que o revisor faz e que o programa não respondia. Geraldi e Ghisi
(2017, 2018, 2019) responderam-na em artigo: extrai-se subséries de uma série
longa, simula-se cada uma e conta-se com que frequência elas reproduzem o
resultado da série inteira. O comprimento representativo é o menor que reproduz
o resultado na maior parte das vezes.

O método aqui é o dos artigos, com duas diferenças declaradas:

1. A resposta é **deste projeto**, e não da cidade. A série necessária cresce com
   a fração atendível: quanto maior a demanda que se quer cobrir, mais o
   resultado depende de estiagens raras, e mais longa a série precisa ser.
2. O critério de semelhança é explícito e configurável: mesmo volume ideal,
   dentro de uma tolerância em passos da grade, e potencial dentro de uma
   tolerância em pontos percentuais.

O ano tem 365 dias, como no resto do programa, e as janelas deslizam de ano em
ano sobre a série carregada.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence

import numpy as np

from triton.core.simulation import run_single_simulation

DIAS_NO_ANO = 365


@dataclass(frozen=True)
class ResultadoDoComprimento:
    """O que a análise responde, com o que foi usado para responder."""
    anos_da_serie: int
    volume_ideal_l: float
    potencial_no_ideal_pct: float
    comprimento_representativo_anos: Optional[int]
    frequencia_por_comprimento: Dict[int, float]
    janelas_por_comprimento: Dict[int, int]
    confianca_pct: float
    tolerancia_pp: float
    tolerancia_passos: int
    limiar_ganho_pct_m3: float
    amostra_por_comprimento: Optional[int]
    semente: Optional[int]
    volumes_l: List[float] = field(default_factory=list)

    @property
    def serie_e_representativa(self) -> bool:
        """A série carregada basta para este projeto?"""
        return (self.comprimento_representativo_anos is not None
                and self.anos_da_serie >= self.comprimento_representativo_anos)

    def resumo(self) -> str:
        """Uma frase para a tela e para o relatório."""
        anos = self.anos_da_serie
        rep = self.comprimento_representativo_anos
        if rep is None:
            return (f"A série tem {anos} anos e não estabiliza dentro dela: nem o maior "
                    f"comprimento testado reproduz o resultado em {self.confianca_pct:.0f}% "
                    f"das janelas. Trate o volume ideal de {self.volume_ideal_l:,.0f} L como "
                    f"provisório.".replace(",", "."))
        if anos >= rep:
            return (f"A série tem {anos} anos e {rep} bastam para este projeto: "
                    f"ela é representativa.")
        return (f"A série tem {anos} anos, e este projeto precisa de {rep} para "
                f"estabilizar. O volume ideal pode mudar com mais dados.")


def _potencial(serie: np.ndarray, volume: float, parametros: dict) -> float:
    return run_single_simulation(precip_data=serie, lower_tank_vol=float(volume),
                                 **parametros).potential_potable_savings_pct


def volume_ideal(serie: np.ndarray, volumes: Sequence[float], limiar_pct_m3: float,
                 parametros: dict, cache: Optional[dict] = None) -> tuple:
    """O menor volume da grade cujo ganho marginal já caiu abaixo do limiar.

    Devolve ``(volume, potenciais)``. Só simula até encontrar o ideal: a varredura
    inteira não é necessária, e é o que torna a análise viável.
    """
    potenciais: Dict[float, float] = dict(cache or {})

    def pot(v: float) -> float:
        if v not in potenciais:
            potenciais[v] = _potencial(serie, v, parametros)
        return potenciais[v]

    anterior = pot(volumes[0])
    for i in range(1, len(volumes)):
        atual = pot(volumes[i])
        passo_m3 = (volumes[i] - volumes[i - 1]) / 1000.0
        if passo_m3 > 0 and (atual - anterior) / passo_m3 <= limiar_pct_m3:
            return volumes[i], potenciais
        anterior = atual
    return volumes[-1], potenciais


def analisar(
    precipitacao: Sequence[float],
    parametros_da_simulacao: dict,
    *,
    volume_maximo_l: float = 20000.0,
    passo_l: float = 1000.0,
    limiar_ganho_pct_m3: float = 1.0,
    tolerancia_pp: float = 2.0,
    tolerancia_passos: int = 0,
    confianca_pct: float = 90.0,
    amostra_por_comprimento: Optional[int] = None,
    semente: Optional[int] = 42,
    progresso: Optional[Callable[[int, int], None]] = None,
) -> ResultadoDoComprimento:
    """Analisa de quantos anos este projeto precisa.

    ``parametros_da_simulacao`` são os mesmos de ``run_single_simulation``, sem a
    série e sem o volume: área, coeficiente, descarte, demanda e fração.

    ``amostra_por_comprimento`` sorteia esse número de janelas por comprimento,
    em vez de percorrer todas — é o que deixa a análise rápida em séries longas.
    A semente fica registrada no resultado, e o mesmo sorteio se repete.
    """
    serie = np.asarray(precipitacao, dtype=float)
    anos = int(len(serie) // DIAS_NO_ANO)
    if anos < 2:
        raise ValueError("A análise precisa de pelo menos dois anos de série.")

    volumes = [float(v) for v in np.arange(passo_l, volume_maximo_l + passo_l / 2, passo_l)]
    referencia = serie[: anos * DIAS_NO_ANO]
    ideal_ref, potenciais_ref = volume_ideal(referencia, volumes, limiar_ganho_pct_m3,
                                             parametros_da_simulacao)
    if ideal_ref not in potenciais_ref:
        potenciais_ref[ideal_ref] = _potencial(referencia, ideal_ref, parametros_da_simulacao)
    potencial_ref = potenciais_ref[ideal_ref]
    indice_ref = volumes.index(ideal_ref)

    sorteio = np.random.default_rng(semente)
    frequencia: Dict[int, float] = {}
    janelas_contadas: Dict[int, int] = {}
    total_passos = anos - 1
    for i, comprimento in enumerate(range(1, anos), start=1):
        inicios = list(range(0, anos - comprimento + 1))
        if amostra_por_comprimento and len(inicios) > amostra_por_comprimento:
            inicios = sorted(sorteio.choice(inicios, size=amostra_por_comprimento,
                                            replace=False).tolist())
        semelhantes = 0
        for inicio in inicios:
            trecho = serie[inicio * DIAS_NO_ANO: (inicio + comprimento) * DIAS_NO_ANO]
            ideal, potenciais = volume_ideal(trecho, volumes, limiar_ganho_pct_m3,
                                             parametros_da_simulacao)
            if abs(volumes.index(ideal) - indice_ref) > tolerancia_passos:
                continue
            if ideal_ref not in potenciais:
                potenciais[ideal_ref] = _potencial(trecho, ideal_ref, parametros_da_simulacao)
            if abs(potenciais[ideal_ref] - potencial_ref) <= tolerancia_pp:
                semelhantes += 1
        frequencia[comprimento] = round(100.0 * semelhantes / len(inicios), 1)
        janelas_contadas[comprimento] = len(inicios)
        if progresso:
            progresso(i, total_passos)

    # O comprimento representativo é o menor que alcança a confiança e a mantém:
    # um comprimento curto que acerta por acaso não serve de recomendação.
    representativo = None
    for comprimento in range(1, anos):
        if all(frequencia[maior] >= confianca_pct for maior in range(comprimento, anos)):
            representativo = comprimento
            break

    return ResultadoDoComprimento(
        anos_da_serie=anos,
        volume_ideal_l=ideal_ref,
        potencial_no_ideal_pct=round(potencial_ref, 2),
        comprimento_representativo_anos=representativo,
        frequencia_por_comprimento=frequencia,
        janelas_por_comprimento=janelas_contadas,
        confianca_pct=confianca_pct,
        tolerancia_pp=tolerancia_pp,
        tolerancia_passos=tolerancia_passos,
        limiar_ganho_pct_m3=limiar_ganho_pct_m3,
        amostra_por_comprimento=amostra_por_comprimento,
        semente=semente,
        volumes_l=volumes,
    )
