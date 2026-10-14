"""Os resultados que o relatório (PDF/HTML), o JSON e o CAD mostram para um volume.

Até a 1.0.0 a aba de relatórios lia a economia por ``tab_economic.last_econ_res``,
atributo que a aba econômica não define: o laudo saía com investimento, VPL e TIR
iguais a zero, como se calculados. Para volumes fora da varredura, interpolava
potencial, VPL e investimento entre os volumes vizinhos. E escolhia o volume do
otimizador depois de já ter lido os indicadores hídricos de outro.

A regra aqui é a do programa todo: o que aparece vem do cálculo, para o volume do
relatório; o que não foi calculado fica ``None``, e o documento diz «Não calculado».
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

#: Texto dos documentos quando o indicador não foi calculado para o volume.
NAO_CALCULADO = "Não calculado"
NAO_CALCULADO_EN = "Not calculated"

#: Indicadores hídricos que o relatório mostra; ``None`` quando não simulados.
CHAVES_HIDRICAS = ("potential_pct", "pluv_day", "potable_day", "spill_day", "sat_full", "sat_null")
#: Indicadores econômicos que o relatório mostra; ``None`` quando não calculados.
CHAVES_ECONOMICAS = ("capex", "annual_gross", "vpl", "tir", "payback_s", "payback_d")

_TOLERANCIA_L = 0.5


def texto_nao_calculado(lang: Optional[str] = None) -> str:
    """«Não calculado», em inglês quando o documento é em inglês."""
    return NAO_CALCULADO_EN if lang == "en" else NAO_CALCULADO


def _mesmo_volume(a: Any, b: Any) -> bool:
    try:
        return abs(float(a) - float(b)) < _TOLERANCIA_L
    except (TypeError, ValueError):
        return False


def _numero(valor: Any) -> Optional[float]:
    try:
        v = float(valor)
    except (TypeError, ValueError):
        return None
    return v if v == v and v not in (float("inf"), float("-inf")) else None


def volume_do_relatorio(
    selecionado: Optional[float] = None,
    tipo: str = "economic",
    topsis: Any = None,
    otimo_economico: Optional[float] = None,
    otimo_ambiental: Optional[float] = None,
    single: Any = None,
    sweep: Any = None,
) -> Optional[float]:
    """O volume que o relatório documenta, decidido antes de ler qualquer indicador.

    Ordem: o escolhido pelo usuário; o ótimo do tipo de laudo (ambiental no laudo
    ambiental, econômico nos demais) pelo otimizador ou pela aba que o calculou; a
    simulação única; o ótimo técnico da varredura. Sem nada disso, ``None``: o laudo
    não inventa um volume.
    """
    if selecionado is not None:
        return float(selecionado)
    candidatos = list(getattr(topsis, "candidates", None) or [])
    if candidatos:
        indice = getattr(topsis, "environmental_best_index" if tipo == "environmental"
                         else "financial_best_index", None)
        if indice is not None and 0 <= int(indice) < len(candidatos):
            return float(candidatos[int(indice)].lower_tank_vol)
    otimo = otimo_ambiental if tipo == "environmental" else otimo_economico
    if otimo is not None and float(otimo) > 0:
        return float(otimo)
    if single is not None:
        return float(single.lower_tank_vol)
    if sweep is not None:
        otimo_tecnico = getattr(sweep, "optimal_lower_tank_vol", None)
        if otimo_tecnico:
            return float(otimo_tecnico)
        positivos = [r.lower_tank_vol for r in (getattr(sweep, "results_by_volume", None) or [])
                     if r.lower_tank_vol > 0]
        if positivos:
            return float(positivos[0])
    return None


def indicadores_hidricos(volume: Optional[float], sweep: Any = None, single: Any = None) -> Dict[str, Optional[float]]:
    """Potencial, consumos e atendimento do volume, como a simulação os calculou.

    Procura o volume na varredura e na simulação única. Fora delas, nada é
    interpolado: os indicadores ficam ``None``.
    """
    vazio: Dict[str, Optional[float]] = {k: None for k in CHAVES_HIDRICAS}
    if volume is None:
        return vazio
    linhas: Iterable[Any] = list(getattr(sweep, "results_by_volume", None) or [])
    if single is not None:
        linhas = list(linhas) + [single]
    r = next((r for r in linhas if _mesmo_volume(r.lower_tank_vol, volume)), None)
    if r is None:
        return vazio
    return {
        "potential_pct": _numero(getattr(r, "potential_potable_savings_pct", None)),
        "pluv_day": _numero(getattr(r, "avg_pluvial_consumed_l_day", None)),
        "potable_day": _numero(getattr(r, "avg_potable_consumed_l_day", None)),
        "spill_day": _numero(getattr(r, "avg_spilled_l_day", None)),
        "sat_full": _numero(getattr(r, "pct_days_full_satisfaction", None)),
        "sat_null": _numero(getattr(r, "pct_days_null_satisfaction", None)),
    }


def indicadores_economicos(
    volume: Optional[float],
    varredura_economica: Optional[Dict[Any, Dict[str, Any]]] = None,
    ultimo: Any = None,
    volume_do_ultimo: Optional[float] = None,
    topsis: Any = None,
    cenarios: Optional[Iterable[Dict[str, Any]]] = None,
) -> Dict[str, Optional[float]]:
    """Investimento, economia do 1º ano, VPL, TIR e paybacks do volume.

    Fontes, na ordem: o resultado da análise do volume ativo (``last_result``), se for
    este volume, que é o que a Etapa 5 mostra nos indicadores; a varredura econômica
    da Etapa 5 (``last_sweep_econ_results``); a linha do otimizador
    (``last_scenario_results``) e, por fim, o candidato TOPSIS com o mesmo volume. As
    duas últimas não trazem o payback simples (o «payback» do otimizador é o
    descontado, ou o simples quando aquele não existe). Fora delas, ``None``.
    """
    vazio: Dict[str, Optional[float]] = {k: None for k in CHAVES_ECONOMICAS}
    if volume is None:
        return vazio
    if ultimo is not None and volume_do_ultimo is not None and _mesmo_volume(volume_do_ultimo, volume):
        fluxos = list(getattr(ultimo, "annual_cash_flows", None) or [])
        bruto = _numero(getattr(fluxos[1], "total_gross_savings_brl", None)) if len(fluxos) > 1 else None
        return {
            "capex": _numero(getattr(ultimo, "total_investment", None)),
            "annual_gross": bruto,
            "vpl": _numero(getattr(ultimo, "vpl", None)),
            "tir": _numero(getattr(ultimo, "tir_pct", None)),
            "payback_s": _numero(getattr(ultimo, "payback_simple_years", None)),
            "payback_d": _numero(getattr(ultimo, "payback_discounted_years", None)),
        }
    for linha in (varredura_economica or {}).values():
        if isinstance(linha, dict) and _mesmo_volume(linha.get("volume_l"), volume):
            bruto_mensal = _numero(linha.get("gross_monthly"))
            return {
                "capex": _numero(linha.get("capex")),
                "annual_gross": bruto_mensal * 12.0 if bruto_mensal is not None else None,
                "vpl": _numero(linha.get("vpl")),
                "tir": _numero(linha.get("tir")),
                "payback_s": _numero(linha.get("payback_simple")),
                "payback_d": _numero(linha.get("payback_discounted")),
            }
    for linha in list(cenarios or []):
        if isinstance(linha, dict) and _mesmo_volume(linha.get("vol"), volume):
            bruto_mensal = _numero(linha.get("gross_m"))
            return {
                "capex": _numero(linha.get("capex")),
                "annual_gross": bruto_mensal * 12.0 if bruto_mensal is not None else None,
                "vpl": _numero(linha.get("vpl")),
                "tir": _numero(linha.get("tir")),
                "payback_s": None,
                "payback_d": _numero(linha.get("payback_discounted")),
            }
    for c in list(getattr(topsis, "candidates", None) or []):
        if _mesmo_volume(c.lower_tank_vol, volume):
            return {
                "capex": _numero(getattr(c, "capex_brl", None)),
                "annual_gross": None,
                "vpl": _numero(getattr(c, "vpl_brl", None)),
                "tir": _numero(getattr(c, "irr_pct", None)),
                "payback_s": None,
                "payback_d": _numero(getattr(c, "discounted_payback_years", None)),
            }
    return vazio


def demanda_total_diaria(config: Any) -> Optional[float]:
    """Demanda total da edificação em L/dia, pelo projeto: per capita × moradores ou total.

    ``None`` quando o projeto não a declara; o desenho não supõe 1.000 L/dia.
    """
    if config is None:
        return None
    try:
        valor = float(getattr(config, "demand_value", 0.0) or 0.0)
    except (TypeError, ValueError):
        return None
    if valor <= 0:
        return None
    # demand_type 0: per capita (L/hab/dia); 1: total da edificação (L/dia).
    if int(getattr(config, "demand_type", 0) or 0) == 0:
        moradores = float(getattr(config, "residents_count", 0) or 0)
        return valor * moradores if moradores > 0 else None
    return valor


#: As moedas que a Etapa 3 oferece, na ordem da lista antiga (o índice ``currency``).
MOEDAS = (("BRL", "R$"), ("USD", "$"), ("EUR", "€"), ("GBP", "£"), ("CNY", "¥"))


def moeda_do_projeto(ui_state: Optional[Dict[str, Any]]) -> Optional[Dict[str, str]]:
    """O código e o símbolo da moeda gravados no projeto (``ui_state.stage3``).

    ``None`` quando o arquivo não a declara (CSV legado, projeto da CLI): a saída
    diz «moeda do projeto», e não supõe o real.
    """
    etapa3 = dict((ui_state or {}).get("stage3") or {})
    codigo = etapa3.get("currency_code")
    if not codigo and etapa3.get("currency") is not None:
        try:
            indice = int(etapa3.get("currency"))
        except (TypeError, ValueError):
            indice = -1
        codigo = MOEDAS[indice][0] if 0 <= indice < len(MOEDAS) else None
    simbolo = dict(MOEDAS).get(str(codigo or ""))
    return {"code": str(codigo), "symbol": simbolo} if simbolo else None


def resultados_para_csv_legado(sweep: Any = None, single: Any = None) -> list:
    """As linhas de resultado do CSV do Netuno 4: a varredura, ou a simulação única.

    Sem varredura, o CSV saía sem nenhuma linha de resultado, mesmo com a
    simulação de um volume feita.
    """
    linhas = list(getattr(sweep, "results_by_volume", None) or [])
    if not linhas and single is not None:
        linhas = [single]
    return linhas
