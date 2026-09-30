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


# ── As três frações: interna, externa e total ─────────────────────────────────
#
# A demanda que a chuva pode atender tem duas origens, e só elas são dados:
#
# - a **fração interna** ``f_in`` (``non_potable_indoor_share``): parte do
#   consumo interno, D_in = q × N, que não exige água potável — bacias
#   sanitárias, máquina de lavar;
# - a **demanda externa** ``E`` (``irrigation_liters_per_day``), em L/dia:
#   rega e lavagem de áreas externas, suspensa nos dias de chuva.
#
# A **fração total** ``f`` (``rainwater_share``) é derivada das duas,
#
#     f = (f_in × D_in + E) / (D_in + E),
#
# e é a que se compara com o potencial de economia, cujo denominador é a demanda
# total. Sem demanda externa, f = f_in. Ela fica gravada no projeto para leitura
# e para os arquivos antigos, que só a conheciam, mas não entra no motor quando
# as outras duas existem.

#: Diferença a partir da qual a fração total gravada deixa de concordar com a
#: interna e a externa (0,05 ponto percentual).
TOLERANCIA_ENTRE_FRACOES = 5e-4


def fracao_total(demanda_interna_l_dia: float, fracao_interna: float,
                 demanda_externa_l_dia: float) -> float:
    """f = (f_in·D_in + E) / (D_in + E). Sem demanda nenhuma, devolve f_in."""
    fi = validar_fracao("A fração não potável interna", fracao_interna)
    di = max(0.0, float(demanda_interna_l_dia))
    de = max(0.0, float(demanda_externa_l_dia))
    if di + de <= 0.0:
        return fi
    return (fi * di + de) / (di + de)


def fracao_interna_da_total(demanda_interna_l_dia: float, fracao_total_: float,
                            demanda_externa_l_dia: float) -> float:
    """Inverte :func:`fracao_total`: a f_in que, com E, resulta na f pedida.

    Se a demanda externa sozinha já supera a fração total pedida, não há f_in
    possível; a função recusa em vez de devolver zero em silêncio.
    """
    f = validar_fracao("A fração total atendível", fracao_total_)
    di = max(0.0, float(demanda_interna_l_dia))
    de = max(0.0, float(demanda_externa_l_dia))
    if di <= 0.0:
        return f
    fi = (f * (di + de) - de) / di
    if fi < -TOLERANCIA_ENTRE_FRACOES or fi > 1.0 + TOLERANCIA_ENTRE_FRACOES:
        raise ValueError(
            f"Com {de:g} L/dia de demanda externa e {di:g} L/dia de demanda interna, "
            f"a fração total de {f * 100:.1f}% é impossível: a externa sozinha já "
            f"responde por {de / (di + de) * 100:.1f}% da demanda.")
    return min(1.0, max(0.0, fi))


def conciliar_fracoes(obj, *, demanda_interna_l_dia: Optional[float] = None) -> Optional[str]:
    """Deixa as três frações de um projeto coerentes entre si, e diz o que fez.

    ``obj`` é a configuração do projeto (``NetunoConfig`` ou equivalente, com
    ``rainwater_share``, ``non_potable_indoor_share``, ``potable_indoor_share``,
    ``irrigation_liters_per_day``, ``demand_value`` e ``residents_count``).

    Qual das frações foi editada decide qual se recalcula. A leitura do arquivo
    guarda um retrato, ``_fracoes_lidas``; comparado com ele:

    - mudou só a total (``--share``, ``--set rainwater_share``, cenários):
      a interna é recalculada a partir dela, mantida a externa;
    - mudou a interna ou a externa: a total é recalculada;
    - mudaram as duas e não concordam: é um erro de quem pediu, e se diz qual.

    Sem retrato (configuração montada no código) e em desacordo, vale a total,
    que é a grandeza que as rotinas antigas definem.

    Devolve um aviso legível quando algo foi recalculado por desacordo, ou None.
    """
    if demanda_interna_l_dia is None:
        n = float(getattr(obj, "residents_count", 0) or 0)
        demanda_interna_l_dia = float(getattr(obj, "demand_value", 0.0) or 0.0) * (n if n > 0 else 1.0)
    di = demanda_interna_l_dia
    f = float(obj.rainwater_share)
    fi = float(getattr(obj, "non_potable_indoor_share", f))
    de = float(getattr(obj, "irrigation_liters_per_day", 0.0) or 0.0)
    lidas = getattr(obj, "_fracoes_lidas", None)
    aviso = None

    def _difere(a, b):
        return abs(float(a) - float(b)) > TOLERANCIA_ENTRE_FRACOES

    derivada = fracao_total(di, fi, de)
    if not _difere(derivada, f):
        novo = (derivada, fi, de)
    elif lidas is not None and (_difere(fi, lidas[1]) or _difere(de, lidas[2])) and not _difere(f, lidas[0]):
        novo = (derivada, fi, de)
    elif lidas is not None and _difere(f, lidas[0]) and (_difere(fi, lidas[1]) or _difere(de, lidas[2])):
        raise ValueError(
            f"A fração total ({f * 100:.1f}%) e a interna ({fi * 100:.1f}%) foram alteradas "
            f"juntas e não concordam: com {de:g} L/dia de demanda externa, a interna de "
            f"{fi * 100:.1f}% dá {derivada * 100:.1f}% de total. Altere só uma das duas.")
    else:
        novo = (f, fracao_interna_da_total(di, f, de), de)
        if lidas is None or not _difere(f, lidas[0]):
            aviso = (f"A fração total declarada ({f * 100:.1f}%) não concordava com a interna "
                     f"({fi * 100:.1f}%) e a externa ({de:g} L/dia); vale a total, e a interna "
                     f"passa a {novo[1] * 100:.1f}%.")

    obj.rainwater_share, obj.non_potable_indoor_share, obj.irrigation_liters_per_day = novo
    obj.potable_indoor_share = 1.0 - novo[1]
    try:
        obj._fracoes_lidas = novo
    except AttributeError:
        pass
    return aviso
