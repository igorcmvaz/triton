"""Contrato único dos relatórios do Triton Desktop e Web.

O desktop é a interface de referência. Os adaptadores web apenas transformam
seus dados para ``project_data`` e chamam este mesmo serviço.
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from triton.core.report_generator import (
    generate_environmental_html_report,
    generate_executive_html_report,
    generate_research_html_report,
)
from triton.ui.translation import get_current_lang, set_current_lang


REPORT_TYPE_ALIASES = {
    "economic": "economic",
    "executive": "economic",
    "client": "economic",
    "environmental": "environmental",
    "esg": "environmental",
    "lca": "environmental",
    "research": "research",
    "scientific": "research",
    "academic": "research",
}

# O idioma ainda é uma preferência global da camada de apresentação. O lock
# impede que duas requisições web simultâneas misturem idiomas no mesmo laudo.
_REPORT_LANGUAGE_LOCK = RLock()


def normalize_report_type(report_type: str | None) -> str:
    """Normaliza nomes aceitos pelas duas interfaces para os três laudos oficiais."""
    key = (report_type or "economic").strip().lower()
    try:
        return REPORT_TYPE_ALIASES[key]
    except KeyError as exc:
        raise ValueError(f"Tipo de relatório inválido: {report_type}") from exc


def generate_report_html(
    report_type: str,
    project_data: dict[str, Any],
    *,
    lang: str | None = None,
    sim_result: Any = None,
    econ_result: Any = None,
    lca_result: Any = None,
    esg_result: Any = None,
) -> str:
    """Gera o documento oficial usando exatamente o mesmo caminho em desktop e web."""
    canonical = normalize_report_type(report_type)
    with _REPORT_LANGUAGE_LOCK:
        previous_lang = get_current_lang()
        if lang:
            set_current_lang(lang)
        try:
            from triton.core.licenca_eobs import inserir_aviso_vermelho
            return inserir_aviso_vermelho(
                _gerar_html(canonical, project_data, sim_result, econ_result, lca_result, esg_result),
                (project_data or {}).get("audit_context") or {}, get_current_lang() == "en")
        finally:
            if lang:
                set_current_lang(previous_lang)


def _gerar_html(canonical, project_data, sim_result, econ_result, lca_result, esg_result) -> str:
    if canonical == "environmental":
        return generate_environmental_html_report(
            project_data, sim_result=sim_result, econ_result=econ_result,
            lca_result=lca_result, esg_result=esg_result)
    if canonical == "research":
        return generate_research_html_report(
            project_data, sim_result=sim_result, econ_result=econ_result, lca_result=lca_result)
    return generate_executive_html_report(project_data, sim_result=sim_result, econ_result=econ_result)
