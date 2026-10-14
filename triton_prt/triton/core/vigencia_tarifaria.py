# -*- coding: utf-8 -*-
"""Reajuste da tarifa contado a partir da vigência da tabela.

A tabela tarifária de um município vale desde uma data (a vigência da resolução de onde
foi transcrita). Um estudo feito depois dela encontra a tarifa já reajustada: com
reajuste anual de 5% e uma tabela de dezembro de 2024, um estudo de outubro de 2026 já
paga um reajuste a mais, e o próximo vem em dezembro de 2026, não doze meses depois do
início do estudo.

Por isso o projeto guarda duas datas:

- ``tariff_vigencia``: desde quando vale a tabela de água e esgoto (do catálogo, ou
  digitada);
- ``data_base_estudo``: a data do estudo, gravada no projeto para que o resultado não
  mude conforme o dia em que o arquivo é reaberto.

Entre as duas cabem ``n`` períodos de reajuste completos (``tariff_escalation`` meses
cada): a tarifa do estudo é a da tabela × (1 + reajuste)ⁿ, e os reajustes seguintes
caem nos aniversários da vigência. Sem uma das datas, ou com vigência posterior à
data-base, nada muda: é o comportamento anterior, e o de projetos antigos.

O reajuste passado usa a mesma taxa configurada para o futuro: é uma estimativa,
declarada, não o reajuste que de fato houve.
"""

from __future__ import annotations

import re
from datetime import date
from typing import Any, Optional, Tuple

_MESES = {m: i + 1 for i, m in enumerate(
    "janeiro fevereiro março abril maio junho julho agosto setembro outubro novembro dezembro".split())}
_MESES["marco"] = 3


def data_da_vigencia(texto: Any) -> Optional[date]:
    """A data de um texto de vigência do catálogo, ou None.

    Aceita «01/12/2025», «12/2025», «dezembro de 2025» e «2026». Só o ano vale como
    1º de julho, o meio do ano: o erro máximo fica em seis meses para cada lado.
    """
    s = str(texto or "").strip().lower()
    if not s:
        return None
    m = re.search(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", s)
    if m:
        try:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except ValueError:
            return None
    m = re.search(r"\b(\d{1,2})/(\d{4})\b", s)
    if m and 1 <= int(m.group(1)) <= 12:
        return date(int(m.group(2)), int(m.group(1)), 1)
    m = re.search(r"(" + "|".join(_MESES) + r")\s+de\s+(\d{4})", s)
    if m:
        return date(int(m.group(2)), _MESES[m.group(1)], 1)
    anos = re.findall(r"\b(20\d\d)\b", s)
    if anos:
        return date(int(max(anos)), 7, 1)
    return None


def _meses_entre(inicio: date, fim: date) -> int:
    """Meses completos de ``inicio`` a ``fim`` (zero se ``fim`` vem antes)."""
    meses = (fim.year - inicio.year) * 12 + (fim.month - inicio.month)
    if fim.day < inicio.day:
        meses -= 1
    return max(0, meses)


def meses_desde_a_vigencia(cfg: Any) -> int:
    """Meses completos entre a vigência da tabela e a data-base do estudo."""
    vig = data_da_vigencia(getattr(cfg, "tariff_vigencia", ""))
    base = data_da_vigencia(getattr(cfg, "data_base_estudo", ""))
    if not vig or not base:
        return 0
    return _meses_entre(vig, base)


def reajustes_desde_a_vigencia(cfg: Any) -> int:
    """Quantos reajustes (de ``tariff_escalation`` meses) já caíram até a data-base."""
    intervalo = max(1, int(float(getattr(cfg, "tariff_escalation", 12) or 12)))
    return meses_desde_a_vigencia(cfg) // intervalo


def fatores_desde_a_vigencia(cfg: Any) -> Tuple[float, float]:
    """(fator da água, fator do esgoto) que levam a tabela da vigência à data-base."""
    n = reajustes_desde_a_vigencia(cfg)
    if n <= 0:
        return 1.0, 1.0
    w = float(getattr(cfg, "water_tariff_escalation", 5.0) or 0.0) / 100.0
    s = float(getattr(cfg, "sewage_tariff_escalation", 5.0) or 0.0) / 100.0
    return (1.0 + w) ** n, (1.0 + s) ** n


def resumo_da_atualizacao(cfg: Any) -> str:
    """Uma linha para as telas e o relatório: o que foi aplicado, ou por que não."""
    vig = data_da_vigencia(getattr(cfg, "tariff_vigencia", ""))
    base = data_da_vigencia(getattr(cfg, "data_base_estudo", ""))
    if not vig:
        return "sem data de vigência: a tabela entra como está, e o reajuste conta do início do estudo"
    if not base:
        return "sem data-base do estudo: a tabela entra como está"
    n = reajustes_desde_a_vigencia(cfg)
    fw, _ = fatores_desde_a_vigencia(cfg)
    texto = f"tabela vigente desde {vig:%d/%m/%Y}; estudo em {base:%d/%m/%Y}"
    if n <= 0:
        return texto + ": nenhum reajuste a aplicar"
    return texto + f": {n} reajuste(s) aplicado(s), tarifa × {fw:.4f}".replace(".", ",")
