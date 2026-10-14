# -*- coding: utf-8 -*-
"""Taxas financeiras: uma convenção só, com a unidade declarada.

O programa tinha três leituras da mesma taxa. O arquivo de projeto grava a TMA e
a inflação em % ao mês; a aba econômica integrada sobrescrevia esses campos com a
taxa anual, e o arquivo salvo passava a ter um valor anual sob a chave
«tma_monthly_pct»; e a função de fluxo de caixa adivinhava a unidade, lendo como
fração tudo o que tivesse módulo até 0,5 e como percentual o resto. Uma TMA de
0,5% ao mês chegava lá como 0,5 e virava 50% ao ano.

A convenção agora é esta, e só esta:

- **Interface e arquivo de projeto:** percentual. TMA e inflação em % ao mês
  (a interface permite digitar ao ano e converte); reajustes tarifários em % por
  período de reajuste.
- **Funções de cálculo anual:** fração decimal ao ano, 0,05 para 5%. Um valor que
  pareça percentual é recusado, e não reinterpretado.
- **Conversão entre mês e ano:** composta, ``(1 + i_m)^12 - 1``, e nunca
  multiplicação por doze.
"""

from __future__ import annotations

import math


def pct_para_fracao(percentual: float) -> float:
    """5 (%) -> 0,05."""
    return float(percentual) / 100.0


def mensal_pct_para_anual_pct(mensal_pct: float) -> float:
    """1 (% a.m.) -> 12,68 (% a.a.), por capitalização composta."""
    return ((1.0 + float(mensal_pct) / 100.0) ** 12 - 1.0) * 100.0


def anual_pct_para_mensal_pct(anual_pct: float) -> float:
    """12,68 (% a.a.) -> 1 (% a.m.), a inversa exata da anterior."""
    return ((1.0 + float(anual_pct) / 100.0) ** (1.0 / 12.0) - 1.0) * 100.0


def mensal_pct_para_anual_fracao(mensal_pct: float) -> float:
    """1 (% a.m.) -> 0,1268 (fração ao ano), o que a análise anual recebe."""
    return pct_para_fracao(mensal_pct_para_anual_pct(mensal_pct))


def validar_fracao_anual(nome: str, valor: float) -> float:
    """Confere que uma taxa chegou como fração decimal, e a devolve.

    Recusa valor não finito, valor de -100% ou menos, e valor com módulo acima de
    1, que é quase sempre um percentual digitado onde se espera fração. Uma taxa
    real acima de 100% ao ano não é plausível numa análise de aproveitamento de
    água, e recusá-la é mais seguro do que dividi-la por cem em silêncio.
    """
    v = float(valor)
    if not math.isfinite(v) or v <= -1.0:
        raise ValueError(f"{nome} deve ser um número finito e maior que -100%; "
                         f"recebido {valor!r}.")
    if abs(v) > 1.0:
        raise ValueError(f"{nome} parece estar em percentual ({valor!r}): informe a "
                         "taxa anual como fração decimal, por exemplo 0,05 para 5%.")
    return v
