# -*- coding: utf-8 -*-
"""Fração atendível por água pluvial: uma convenção só, com a unidade declarada.

A mesma grandeza circulava em duas unidades. A tela de edificação a pede em
percentual; o arquivo de projeto e o motor de cálculo a guardam como fração. Entre
uma ponta e outra, doze pontos do programa adivinhavam a unidade com a mesma regra,
«acima de 1 é percentual». A regra falha exatamente onde não se vê: 1 vira 100%, e
não 1%; 0,5 digitado numa coluna em percentual vira 50%, e não 0,5%.

A convenção agora é esta, e só esta:

- **Onde uma pessoa digita** (telas, tabelas de cenários, planilhas de lote e o
  argumento ``--share`` da linha de comando): percentual, de 0 a 100. 40 é 40%.
- **Onde o programa guarda e calcula** (arquivo de projeto, arquivo de parâmetros,
  ``rainwater_share`` e os vetores semanal, mensal e diário): fração, de 0 a 1.
- **A passagem de uma para outra** é explícita, por :func:`percentual_para_fracao`
  e :func:`fracao_para_percentual`, e nunca por inferência.
- **Valor fora da faixa é recusado**, e não reinterpretado. Um percentual pequeno
  demais para ser plausível, entre 0 e 1, é aceito, mas a interface o assinala.
"""

from __future__ import annotations

import math
from typing import Optional


def validar_fracao(nome: str, valor: float) -> float:
    """Confere que a fração está em [0, 1] e a devolve.

    Um valor entre 1 e 100 é quase sempre um percentual digitado onde se espera
    fração, e a mensagem diz isso; dividi-lo por cem em silêncio é o que esta
    convenção existe para impedir.
    """
    v = float(valor)
    if not math.isfinite(v):
        raise ValueError(f"{nome} não é um número finito ({valor!r}).")
    if 1.0 < v <= 100.0:
        raise ValueError(f"{nome} parece estar em percentual ({v:g}): aqui a fração vai "
                         f"de 0 a 1, por exemplo 0,4 para 40%.")
    if not 0.0 <= v <= 1.0:
        raise ValueError(f"{nome} fora de [0, 1]: {v:g}. Informe 0,4 para 40%.")
    return v


def percentual_para_fracao(nome: str, percentual: float) -> float:
    """40 (%) -> 0,4. Recusa valor fora de [0, 100]."""
    p = float(percentual)
    if not math.isfinite(p):
        raise ValueError(f"{nome} não é um número finito ({percentual!r}).")
    if not 0.0 <= p <= 100.0:
        raise ValueError(f"{nome} fora de [0, 100]: {p:g}%. Informe 40 para 40%.")
    return p / 100.0


def fracao_para_percentual(nome: str, fracao: float) -> float:
    """0,4 -> 40 (%). Recusa valor fora de [0, 1]."""
    return validar_fracao(nome, fracao) * 100.0


#: O aviso nos quatro idiomas da interface. Fica aqui, e não no catálogo da
#: interface, porque é montado com números e o núcleo não importa a camada gráfica.
_MODELOS_DO_AVISO = {
    "pt": "{d}% é menos de 1% da demanda. O campo está em percentual: se quis dizer {e}%, digite {e}.",
    "en": "{d}% is less than 1% of the demand. The field is a percentage: if you meant {e}%, type {e}.",
    "es": "{d}% es menos del 1% de la demanda. El campo está en porcentaje: si quiso decir {e}%, escriba {e}.",
    "zh": "{d}% 不到需求的 1%。此字段为百分比：如果您指的是 {e}%，请输入 {e}。",
}


def aviso_percentual_pequeno(percentual: float, idioma: str = "pt") -> Optional[str]:
    """Texto do aviso quando um percentual está entre 0 e 1, ou None.

    Menos de 1% da demanda atendida por chuva é possível, mas raro; muito mais
    frequente é quem digitou a fração, 0,4, num campo que pede percentual, 40.
    """
    try:
        p = float(percentual)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(p) or not 0.0 < p <= 1.0:
        return None
    decimal = "," if idioma in ("pt", "es") else "."
    exemplo = f"{p * 100.0:g}".replace(".", decimal)
    digitado = f"{p:g}".replace(".", decimal)
    modelo = _MODELOS_DO_AVISO.get(idioma, _MODELOS_DO_AVISO["pt"])
    return modelo.format(d=digitado, e=exemplo)
