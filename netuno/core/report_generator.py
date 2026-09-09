"""
Módulo Core de Geração de Relatórios Gerenciais e Científicos (PDF / HTML / Laudos Técnicos).
Suporta dois modelos principais de exportação:
1. Relatório Econômico (Clientes) — Dashboard Executivo de 1 Página A4.
2. Relatório de Pesquisa (Acadêmico/Engenharia) — Relatório Técnico-Científico Detalhado com ACV,
   gráficos dinâmicos em SVG, tabelas de varredura, análise de sensibilidade e equações.
"""

import os
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
import base64
from html import escape
from datetime import datetime
from typing import Dict, Any, Optional

from netuno.core.parser import format_ptbr
from netuno import APP_VERSION_LABEL
from netuno.ui.translation import tr, get_current_lang, _translate_composite, _SPANISH_PHRASES, _CHINESE_PHRASES


def _localize_report_markup(html: str) -> str:
    """Aplica o glossário de interface também às partes estáticas do relatório."""
    lang = get_current_lang()
    if lang == "es":
        html = _translate_composite(html, _SPANISH_PHRASES)
    elif lang == "zh":
        html = _translate_composite(html, _CHINESE_PHRASES)
    return html.replace('lang="pt-BR"', f'lang="{lang}"')


def generate_executive_html_report(project_data: Dict[str, Any], sim_result: Optional[Any] = None, econ_result: Optional[Any] = None) -> str:
    """
    Gera um Relatório Gerencial Executivo em Página Única A4 (1-Page Dashboard),
    diagramado profissionalmente para apresentação a clientes, diretoria, órgãos ambientais e prefeituras.
    """
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    # Extração e formatação de dados da edificação e projeto
    project_name = escape(str(project_data.get("project_name", "Projeto Netuno")))
    ref_code = escape(str(project_data.get("ref_code", "NET-5026-UFSC")))
    rain_file = escape(str(project_data.get("rain_file", "Série Climatológica")))
    audit = project_data.get("audit_context", {}) or {}
    climate_location = escape(str(audit.get("climate_location", "-")))
    climate_basis = escape(str(audit.get("climate_basis", "Série observada")))
    climate_period = escape(str(audit.get("climate_period", "-")))
    analysis_years = escape(str(audit.get("analysis_period_years", 20)))
    area = project_data.get("area", 100.0)
    runoff = project_data.get("runoff", COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard = project_data.get("discard", 2.0)
    residents = project_data.get("residents", 4)
    demand = project_data.get("demand", 200.0)
    raw_share = project_data.get("share", 0.40)
    if isinstance(raw_share, (int, float)):
        share = raw_share * 100.0 if raw_share <= 1.0 else raw_share
    else:
        share = "-"
    
    # Extração do resultado do balanço hídrico
    lower_vol = project_data.get("lower_vol", 2000.0)
    potential_pct = project_data.get("potential_pct", 0.0)
    pluv_day = project_data.get("pluv_day", 0.0)
    potable_day = project_data.get("potable_day", 0.0)
    spill_day = project_data.get("spill_day", 0.0)
    sat_full = project_data.get("sat_full", 0.0)
    sat_null = project_data.get("sat_null", 0.0)
    
    # Extração dos dados econômicos
    capex = project_data.get("capex", 8950.0)
    annual_gross = project_data.get("annual_gross", 3240.0)
    vpl = project_data.get("vpl", 24150.0)
    tir = project_data.get("tir", 34.2)
    
    raw_payback_s = project_data.get("payback_s", "--")
    raw_payback_d = project_data.get("payback_d", "--")

    # Formatação estrita em pt-BR (ponto milhar, vírgula decimal)
    lower_vol_str = format_ptbr(lower_vol, 0)
    potential_pct_str = format_ptbr(potential_pct, 1)
    
    area_str = f"{format_ptbr(area, 1)} m²" if isinstance(area, (int, float)) else "-"
    runoff_str = format_ptbr(runoff, 2) if isinstance(runoff, (int, float)) else "-"
    discard_str = f"{format_ptbr(discard, 1)} mm" if isinstance(discard, (int, float)) else "-"
    residents_str = f"{int(residents)} pessoas" if isinstance(residents, (int, float)) else "-"
    demand_str = f"{format_ptbr(demand, 0)} L/hab/dia" if isinstance(demand, (int, float)) else "-"
    share_str = format_ptbr(share, 0) if isinstance(share, (int, float)) else "-"
    share_label_str = f" ({share_str}%)" if isinstance(share, (int, float)) else ""

    if isinstance(demand, (int, float)) and isinstance(residents, (int, float)) and isinstance(share, (int, float)):
        pluvial_daily_demand = (demand * residents * share / 100.0)
        pluvial_daily_demand_str = f"{format_ptbr(pluvial_daily_demand, 0)} L/dia"
    else:
        pluvial_daily_demand_str = "-"

    pluv_day_str = format_ptbr(pluv_day, 1)
    potable_day_str = format_ptbr(potable_day, 1)
    spill_day_str = format_ptbr(spill_day, 1)
    sat_full_str = format_ptbr(sat_full, 1)
    sat_null_str = format_ptbr(sat_null, 1)
    
    capex_str = format_ptbr(capex, 2)
    annual_gross_str = format_ptbr(annual_gross, 2)
    vpl_str = format_ptbr(vpl, 2)
    tir_str = format_ptbr(tir, 1)
    
    if isinstance(raw_payback_s, (int, float)):
        payback_s_str = format_ptbr(raw_payback_s, 1)
    else:
        payback_s_str = str(raw_payback_s).replace('.', ',')

    if isinstance(raw_payback_d, (int, float)):
        payback_d_str = format_ptbr(raw_payback_d, 1)
    else:
        payback_d_str = str(raw_payback_d).replace('.', ',')

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Laudo Técnico Executivo - Netuno 5</title>
    <style>
        @page {{ size: A4 landscape; margin: 5mm 8mm; }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        html, body {{
            margin: 0; padding: 0;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, Helvetica, sans-serif;
            color: #0f172a; background-color: #ffffff;
            font-size: 10pt; line-height: 1.4;
        }}
        .page-container {{ width: 100%; max-width: 1100px; margin: 0 auto; padding: 0; }}
        @media screen {{
            body {{
                background-color: #f1f5f9;
                padding: 16px 12px;
            }}
            .page-container {{
                background: #ffffff;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border-radius: 6px;
                padding: 20px 24px;
            }}
        }}
        @media print {{
            body {{ background: #ffffff; padding: 0; }}
            .page-container {{ box-shadow: none; border-radius: 0; padding: 0; margin: 0 auto; max-width: 100%; }}
        }}
        .header-table {{
            width: 100%; border-collapse: collapse; margin-bottom: 10px;
            border-bottom: 2.5px solid #0369a1; padding-bottom: 7px;
        }}
        .header-table td {{ vertical-align: middle; border: none; padding: 0; }}
        .brand-title h1 {{
            margin: 0; font-size: 17.5pt; color: #0369a1; font-weight: 800;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .brand-title p {{ margin: 3px 0 0 0; font-size: 9.8pt; color: #475569; font-weight: 600; }}
        .doc-meta {{ text-align: right; }}
        .doc-meta p {{ margin: 3px 0 0 0; font-size: 9.8pt; color: #64748b; }}
        .doc-meta b {{ color: #0f172a; }}

        .audit-strip {{ width: 100%; border-collapse: separate; border-spacing: 5px; margin: 0 -5px 12px; }}
        .audit-strip td {{ width: 25%; background: #f8fafc; border: 1px solid #e2e8f0; padding: 7px 10px; color: #334155; font-size: 8.8pt; border-radius: 4px; }}
        .audit-strip b {{ display: block; color: #0369a1; font-size: 8pt; text-transform: uppercase; margin-bottom: 3px; font-weight: 700; }}

        .kpi-row {{ display: flex; width: 100%; margin-bottom: 12px; gap: 10px; }}
        .kpi-card {{
            flex: 1; background-color: #f8fafc; border: 1px solid #e2e8f0;
            border-radius: 6px; padding: 13px 10px; text-align: center; border-top: 4px solid #0369a1;
        }}
        .kpi-card.green {{ border-top-color: #059669; background-color: #f0fdf4; }}
        .kpi-card.blue {{ border-top-color: #0284c7; background-color: #f0f9ff; }}
        .kpi-card.amber {{ border-top-color: #d97706; background-color: #fffbeb; }}
        .kpi-label {{ font-size: 8.8pt; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 5px; }}
        .kpi-value {{ font-size: 17pt; font-weight: 800; color: #0f172a; margin-bottom: 4px; }}
        .kpi-sub {{ font-size: 8.2pt; color: #64748b; }}

        .section-header {{
            background-color: #0369a1; color: #ffffff; font-size: 10pt; font-weight: 700;
            padding: 6px 10px; border-radius: 4px; margin-bottom: 6px;
            text-transform: uppercase; letter-spacing: 0.3px;
        }}
        .grid-3col {{ width: 100%; border-collapse: collapse; margin-bottom: 12px; }}
        .grid-3col td {{ width: 33.33%; vertical-align: top; border: none; padding: 0 5px; }}
        .grid-3col td:first-child {{ padding-left: 0; }}
        .grid-3col td:last-child {{ padding-right: 0; }}

        .data-table {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
        .data-table th {{
            background-color: #f1f5f9; color: #334155; font-weight: 700;
            text-align: left; padding: 6.5px 8px; border: 1px solid #cbd5e1;
        }}
        .data-table td {{ padding: 6.2px 8px; border: 1px solid #e2e8f0; color: #1e293b; }}
        .data-table, .data-table th, .data-table td {{ page-break-inside: avoid; break-inside: avoid; }}
        .data-table tr:nth-child(even) td {{ background-color: #f8fafc; }}
        .val-bold {{ font-weight: 700; color: #0f172a; }}
        .val-green {{ font-weight: 700; color: #059669; }}

        .bottom-grid {{ width: 100%; border-collapse: collapse; margin-top: 6px; margin-bottom: 12px; }}
        .bottom-grid td {{ vertical-align: top; border: none; padding: 0 5px; }}
        .bottom-grid td:first-child {{ padding-left: 0; width: 60%; }}
        .bottom-grid td:last-child {{ padding-right: 0; width: 40%; }}

        .statement-box {{
            background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3.5px solid #16a34a;
            border-radius: 5px; padding: 10px 12px; font-size: 8.8pt;
        }}
        .statement-box h4 {{ margin: 0 0 4px 0; color: #15803d; font-size: 9.5pt; }}
        .statement-box p {{ margin: 0; color: #166534; line-height: 1.35; }}

        .disclaimer-box {{
            background-color: #fffbebf5; border: 1px solid #fef3c7; border-left: 3.5px solid #d97706;
            border-radius: 5px; padding: 10px 12px; font-size: 8.4pt; color: #78350f;
        }}
        .disclaimer-box h4 {{ margin: 0 0 4px 0; color: #b45309; font-size: 9pt; font-weight: bold; }}
        .disclaimer-box p {{ margin: 0; line-height: 1.3; }}

        .footer-table {{
            width: 100%; border-collapse: collapse; margin-top: 10px;
            border-top: 1.5px solid #cbd5e1; padding-top: 6px; font-size: 8.2pt; color: #64748b;
        }}
        .footer-table td {{ border: none; padding: 0; vertical-align: bottom; }}
        .sig-line {{ border-top: 1px solid #94a3b8; width: 170px; margin-top: 22px; margin-bottom: 3px; }}
    </style>
</head>
<body>
    <div class="page-container">
        <table class="header-table">
            <tr>
                <td class="brand-title" style="width: 55%;">
                    <h1>Laudo Técnico Executivo (Paisagem A4)</h1>
                    <p>Netuno 5 — Aproveitamento de Água de Chuva | Empreendimento: <b>{project_name}</b></p>
                </td>
                <td class="doc-meta" style="width: 45%;">
                    <p>Ref. Projeto: <b>{ref_code}</b> | Emissão: <b>{date_str}</b></p>
                    <p>Conformidade Normativa: <b>ABNT NBR 15527:2019 & NBR 5626</b></p>
                </td>
            </tr>
        </table>

        <table class="audit-strip"><tr>
            <td><b>Localidade climática</b>{climate_location}</td>
            <td><b>Base climática</b>{climate_basis}</td>
            <td><b>Período da série</b>{climate_period}</td>
            <td><b>Horizonte econômico</b>{analysis_years} anos</td>
        </tr></table>

        <div class="kpi-row">
            <div class="kpi-card green">
                <div class="kpi-label">Volume Recomendado</div>
                <div class="kpi-value">{lower_vol_str} L</div>
                <div class="kpi-sub">Reservatório Inferior</div>
            </div>
            <div class="kpi-card green">
                <div class="kpi-label">Economia Potável</div>
                <div class="kpi-value">{potential_pct_str}%</div>
                <div class="kpi-sub">Substituição da Concessionária</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">VPL (20 anos)</div>
                <div class="kpi-value">R$ {vpl_str}</div>
                <div class="kpi-sub">Retorno Líquido Atualizado</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-label">Payback Estimado</div>
                <div class="kpi-value">{payback_s_str} anos</div>
                <div class="kpi-sub">{payback_d_str} anos descontado</div>
            </div>
        </div>

        <table class="grid-3col">
            <tr>
                <td>
                    <div class="section-header">1. Edificação & Hidrologia</div>
                    <table class="data-table">
                        <tr><th>Parâmetro Técnico</th><th>Valor</th></tr>
                        <tr><td>Série Pluviométrica</td><td class="val-bold">{rain_file}</td></tr>
                        <tr><td>Área de Captação</td><td class="val-bold">{area_str}</td></tr>
                        <tr><td>Coef. Escoamento (C)</td><td>{runoff_str}</td></tr>
                        <tr><td>Descarte First Flush</td><td>{discard_str}</td></tr>
                        <tr><td>População Atendida</td><td>{residents_str}</td></tr>
                        <tr><td>Demanda Pluvial Alvo{share_label_str}</td><td class="val-bold">{pluvial_daily_demand_str}</td></tr>
                    </table>
                </td>
                <td>
                    <div class="section-header">2. Balanço Hídrico Simulado</div>
                    <table class="data-table">
                        <tr><th>Indicador Operacional</th><th>Desempenho</th></tr>
                        <tr><td>Volume Cisterna</td><td class="val-bold">{lower_vol_str} L</td></tr>
                        <tr><td>Economia de Potável</td><td class="val-green">{potential_pct_str}%</td></tr>
                        <tr><td>Consumo Médio Pluvial</td><td class="val-bold">{pluv_day_str} L/dia</td></tr>
                        <tr><td>Consumo Médio Potável</td><td>{potable_day_str} L/dia</td></tr>
                        <tr><td>Volume Extravasado</td><td>{spill_day_str} L/dia</td></tr>
                        <tr><td>Garantia Plena (100%)</td><td class="val-bold">{sat_full_str}% dos dias</td></tr>
                    </table>
                </td>
                <td>
                    <div class="section-header">3. Viabilidade Econômica</div>
                    <table class="data-table">
                        <tr><th>Indicador Financeiro</th><th>Resultado</th></tr>
                        <tr><td>Investimento CAPEX</td><td class="val-bold">R$ {capex_str}</td></tr>
                        <tr><td>Economia Bruta 1º Ano</td><td class="val-green">R$ {annual_gross_str} / ano</td></tr>
                        <tr><td>Payback Simples</td><td>{payback_s_str} anos</td></tr>
                        <tr><td>Payback Descontado</td><td>{payback_d_str} anos</td></tr>
                        <tr><td>VPL (20 Anos)</td><td class="val-green">R$ {vpl_str}</td></tr>
                        <tr><td>TIR (% a.a.)</td><td class="val-bold">{tir_str}% a.a.</td></tr>
                    </table>
                </td>
            </tr>
        </table>

        <table class="bottom-grid">
            <tr>
                <td>
                    <div class="statement-box">
                        <h4>📌 Parecer Técnico de Engenharia Hídrica & Sustentabilidade</h4>
                        <p>
                            Nas premissas registradas, o sistema pluvial apresenta economia potável modelada de <b>{potential_pct_str}%</b>,
                            VPL de <b>R$ {vpl_str}</b> e amortização do capital (payback simples) em <b>{payback_s_str} anos</b>. Esses indicadores comprovam a
                            elevada atratividade técnica e financeira, garantindo segurança hídrica e mitigação tarifária conforme as diretrizes da ABNT NBR 15527.
                        </p>
                    </div>
                </td>
                <td>
                    <div class="disclaimer-box">
                        <h4>⚠️ Termo de Responsabilidade Técnica & Validação</h4>
                        <p>
                            O Netuno 5 é uma ferramenta computacional de auxílio ao dimensionamento. <b>Cabe ao(à) profissional habilitado(a)</b> validar as premissas executivas, interferências de rede e conformidade com a legislação local.
                        </p>
                    </div>
                </td>
            </tr>
        </table>

        <table class="footer-table">
            <tr>
                <td style="width: 55%;">
                    <div><b>{tr('Grupo de Pesquisa Gestão do Espaço Sustentável | UFSC')}</b></div>
                    <div>{APP_VERSION_LABEL} Engine — {tr('Documento Executivo A4 Paisagem')}</div>
                </td>
                <td style="width: 45%; text-align: right;">
                    <div style="display: inline-block; text-align: center;">
                        <div class="sig-line"></div>
                        <div><b>{tr('Responsável Técnico(a) / Engenheiro(a)')}</b></div>
                        <div>{tr('CREA / Registro Profissional')}</div>
                    </div>
                </td>
            </tr>
    </div>
</body>
</html>"""
    return _localize_report_markup(html)


def generate_environmental_html_report(
    project_data: Dict[str, Any],
    sim_result: Optional[Any] = None,
    econ_result: Optional[Any] = None,
    lca_result: Optional[Any] = None,
    esg_result: Optional[Any] = None,
) -> str:
    """
    Gera o Relatório Técnico de Desempenho Ambiental, ACV e Sustentabilidade ESG (Padrão A4 Retrato).
    Apresenta de forma clara e rigorosa:
    - Indicadores-chave de mitigação climática e conservação hídrica;
    - Inventário do Ciclo de Vida (ICV / LCI — ISO 14040/14044);
    - Balanço de Carbono e Payback Ecológico detalhado;
    - Matriz de Certificações Ambientais e Enquadramento ESG (LEED v4, AQUA-HQE, Casa Azul CAIXA, GRI 303);
    - Gráficos analíticos de ACV e parecer técnico conclusivo.
    """
    from netuno.core.environmental import calculate_lca, EnvironmentalConfig, empty_environmental_result
    from netuno.core.esg_certifications import calculate_esg_certifications

    report_lang = get_current_lang()
    is_en = report_lang == "en"
    date_str = datetime.now().strftime("%d/%m/%Y" if not is_en else "%Y-%m-%d")

    # Extração de dados da edificação e simulação
    project_name = escape(str(project_data.get("project_name", "Projeto Netuno")))
    ref_code = escape(str(project_data.get("ref_code", "NET-5026-UFSC")))
    rain_file = escape(str(project_data.get("rain_file", "Série Climatológica")))
    audit = project_data.get("audit_context", {}) or {}
    climate_location = escape(str(audit.get("climate_location", "-")))
    climate_basis = escape(str(audit.get("climate_basis", "Observed series" if is_en else "Série observada")))
    climate_period = escape(str(audit.get("climate_period", "-")))
    tariff_location = escape(str(audit.get("tariff_location", "-")))
    area = project_data.get("area", 100.0)
    runoff = project_data.get("runoff", COEFICIENTE_DE_ESCOAMENTO_PADRAO)
    discard = project_data.get("discard", 2.0)
    residents = project_data.get("residents", 4)
    demand = project_data.get("demand", 200.0)
    raw_share = project_data.get("share", 0.40)
    if isinstance(raw_share, (int, float)):
        share = raw_share * 100.0 if raw_share <= 1.0 else raw_share
    else:
        share = "-"

    lower_vol = float(project_data.get("lower_vol", 0.0) or 0.0)
    potential_pct = float(project_data.get("potential_pct", 0.0) or 0.0)
    pluv_day = float(project_data.get("pluv_day", 0.0) or 0.0)
    potable_day = float(project_data.get("potable_day", 0.0) or 0.0)
    spill_day = float(project_data.get("spill_day", 0.0) or 0.0)
    sat_full = float(project_data.get("sat_full", 0.0) or 0.0)
    sat_null = float(project_data.get("sat_null", 0.0) or 0.0)

    annual_pluvial_m3 = (pluv_day * 365.25) / 1000.0
    annual_potable_m3 = (potable_day * 365.25) / 1000.0
    annual_spill_m3 = (spill_day * 365.25) / 1000.0
    total_annual_demand_m3 = annual_pluvial_m3 + annual_potable_m3

    # Obtenção dos resultados de ACV
    if lca_result is None:
        if lower_vol > 0 or annual_pluvial_m3 > 0:
            lca_result = calculate_lca(lower_vol, annual_pluvial_m3 if annual_pluvial_m3 > 0 else 100.0, EnvironmentalConfig())
        else:
            lca_result = empty_environmental_result()

    # Obtenção dos resultados ESG
    if esg_result is None:
        esg_result = calculate_esg_certifications(
            potable_savings_pct=potential_pct,
            annual_pluvial_consumed_m3=annual_pluvial_m3,
            annual_potable_consumed_m3=annual_potable_m3,
            net_co2e_saved_kg_lifetime=lca_result.lifetime_net_co2_saved_kg if lca_result else 0.0,
            project_lifetime_years=20,
            has_irrigation_demand=True
        )

    # Formatação numérica
    lower_vol_str = format_ptbr(lower_vol, 0)
    potential_pct_str = format_ptbr(potential_pct, 1)
    area_str = f"{format_ptbr(area, 1)} m²" if isinstance(area, (int, float)) else "-"
    runoff_str = format_ptbr(runoff, 2) if isinstance(runoff, (int, float)) else "-"
    discard_str = f"{format_ptbr(discard, 1)} mm" if isinstance(discard, (int, float)) else "-"
    residents_str = f"{int(residents)} {'pessoas' if not is_en else 'occupants'}" if isinstance(residents, (int, float)) else "-"
    demand_str = f"{format_ptbr(demand, 0)} L/hab/dia" if isinstance(demand, (int, float)) else "-"
    share_str = f"{format_ptbr(share, 0)}%" if isinstance(share, (int, float)) else "-"

    pluv_day_str = format_ptbr(pluv_day, 1)
    pluv_ann_str = format_ptbr(annual_pluvial_m3, 1)
    potable_day_str = format_ptbr(potable_day, 1)
    potable_ann_str = format_ptbr(annual_potable_m3, 1)
    spill_day_str = format_ptbr(spill_day, 1)
    sat_full_str = format_ptbr(sat_full, 1)

    # Métricas de ACV
    embodied_co2_str = format_ptbr(lca_result.total_embodied_co2_kg, 1)
    ann_pumping_co2_str = format_ptbr(lca_result.annual_pumping_co2_kg, 1)
    ann_treatment_co2_str = format_ptbr(lca_result.annual_treatment_co2_kg, 1)
    ann_avoided_co2_str = format_ptbr(lca_result.annual_avoided_co2_kg, 1)
    net_ann_co2_val = lca_result.net_annual_avoided_co2_kg
    net_ann_co2_str = (
        f"-{format_ptbr(net_ann_co2_val, 1)}" if net_ann_co2_val >= 0 else f"+{format_ptbr(abs(net_ann_co2_val), 1)}"
    )
    lifetime_net_co2_val = lca_result.lifetime_net_co2_saved_kg
    lifetime_net_co2_str = (
        f"-{format_ptbr(lifetime_net_co2_val, 0)}" if lifetime_net_co2_val >= 0 else f"+{format_ptbr(abs(lifetime_net_co2_val), 0)}"
    )
    
    pb_val = lca_result.environmental_payback_years
    if pb_val is not None and pb_val > 0 and pb_val < 90:
        payback_env_str = f"{format_ptbr(pb_val, 1)} {'anos' if not is_en else 'years'}"
    else:
        payback_env_str = f"> 50 {'anos' if not is_en else 'years'}" if pb_val is not None else "--"

    g_l_val = lca_result.specific_co2_avoided_g_per_liter
    specific_g_l_str = f"{format_ptbr(g_l_val, 2)} g CO2e/L" if g_l_val is not None else "--"

    # Cloração
    cl2_dose_str = format_ptbr(lca_result.chlorine_dose_mg_l, 2)
    cl2_kg_yr_str = format_ptbr(lca_result.annual_chlorine_kg, 3)

    # Tabela de itens do ICV
    # Convenção estrita: Emitido para a atmosfera = Positivo (+) / Vermelho (ruim)
    #                   Retirado/Evitado da atmosfera = Negativo (-) / Verde (bom)
    icv_rows = []
    for item in lca_result.inventory_items:
        cat_name = tr(item.category, lang=report_lang)
        emb_val = f"+{format_ptbr(item.embodied_co2_kg, 1)} kg" if item.embodied_co2_kg > 0 else "--"
        
        if item.annual_op_co2_kg > 0:
            op_val = f"+{format_ptbr(item.annual_op_co2_kg, 1)} kg/ano"
            op_class = "val-red"
        elif item.annual_op_co2_kg < 0:
            op_val = f"{format_ptbr(item.annual_op_co2_kg, 1)} kg/ano"
            op_class = "val-green"
        else:
            op_val = "--"
            op_class = ""

        if item.lifetime_net_co2_kg > 0:
            net_val = f"+{format_ptbr(item.lifetime_net_co2_kg, 1)} kg"
            net_class = "val-red"
        elif item.lifetime_net_co2_kg < 0:
            net_val = f"{format_ptbr(item.lifetime_net_co2_kg, 1)} kg"
            net_class = "val-green"
        else:
            net_val = "--"
            net_class = ""

        src_name = escape(tr(item.source_reference, lang=report_lang))
        qty_name = escape(item.quantity_str)
        icv_rows.append(
            f"<tr>"
            f"<td class='val-bold'>{cat_name}</td>"
            f"<td>{qty_name}</td>"
            f"<td style='text-align: right;' class='val-red'>{emb_val}</td>"
            f"<td style='text-align: right;' class='{op_class}'>{op_val}</td>"
            f"<td style='text-align: right;' class='{net_class}'>{net_val}</td>"
            f"<td style='font-size: 6.8pt; color: #64748b;'>{src_name}</td>"
            f"</tr>"
        )
    icv_rows_html = "".join(icv_rows) if icv_rows else "<tr><td colspan='6' style='text-align:center;'>Nenhum item computado no inventário.</td></tr>"

    # Gráficos ambientais embutidos
    chart_list = project_data.get("report_charts", []) or []
    env_charts = [c for c in chart_list if c.get("chapter") == "environmental"]
    charts_html = ""
    if env_charts:
        chart_cards = []
        for ch in env_charts:
            c_title = escape(ch.get("title", "Gráfico Ambiental"))
            c_src = ch.get("data", "")
            chart_cards.append(
                f"<div class='chart-card'>"
                f"<div class='chart-title'>{c_title}</div>"
                f"<img src='{c_src}' alt='{c_title}' class='chart-img'/>"
                f"</div>"
            )
        charts_html = f"<div class='charts-grid'>{''.join(chart_cards)}</div>"

    # Selos e badges ESG
    aqua_stars = "⭐" * esg_result.aqua.stars if esg_result.aqua.stars > 0 else "—"

    doc_title = "Relatório de Desempenho Ambiental, ACV e Sustentabilidade ESG" if not is_en else "Environmental Performance, LCA and ESG Sustainability Report"
    doc_subtitle = "Avaliação de Ciclo de Vida (ACV/LCA), Pegada de Carbono e Certificações Sustentáveis" if not is_en else "Life Cycle Assessment (LCA), Carbon Footprint and Sustainable Certifications"

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{doc_title} - Netuno 5</title>
    <style>
        @page {{ size: A4 portrait; margin: 8mm 10mm; }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        html, body {{
            margin: 0; padding: 0;
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Arial, sans-serif;
            color: #0f172a; background-color: #ffffff;
            font-size: 8pt; line-height: 1.3;
        }}
        .page-container {{ width: 100%; max-width: 780px; margin: 0 auto; padding: 2px; }}
        @media screen {{
            body {{
                background-color: #f1f5f9;
                padding: 16px 8px;
            }}
            .page-container {{
                background: #ffffff;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
                border-radius: 6px;
                padding: 24px 28px;
            }}
        }}
        @media print {{
            body {{ background: #ffffff; padding: 0; }}
            .page-container {{ box-shadow: none; border-radius: 0; padding: 2px; margin: 0 auto; max-width: 100%; }}
        }}
        .header-table {{
            width: 100%; border-collapse: collapse; margin-bottom: 8px;
            border-bottom: 2.5px solid #059669; padding-bottom: 4px;
        }}
        .header-table td {{ vertical-align: middle; border: none; padding: 0; }}
        .doc-title h1 {{
            margin: 0; font-size: 13pt; color: #047857; font-weight: 800;
            text-transform: uppercase; letter-spacing: 0.5px;
        }}
        .doc-title p {{ margin: 1px 0 0 0; font-size: 7.5pt; color: #64748b; font-weight: 600; }}
        .audit-strip {{ width: 100%; border-collapse: separate; border-spacing: 4px; margin: 0 -4px 8px; }}
        .audit-strip td {{ width: 25%; background: #f8fafc; border: 1px solid #e2e8f0; padding: 4px 6px; color: #334155; font-size: 6.6pt; }}
        .audit-strip b {{ display: block; color: #047857; font-size: 6.2pt; text-transform: uppercase; }}
        
        .kpi-row {{ display: flex; width: 100%; margin-bottom: 8px; gap: 5px; }}
        .kpi-card {{
            flex: 1; background-color: #f8fafc; border: 1px solid #e2e8f0;
            border-radius: 5px; padding: 5px 6px; text-align: center; border-top: 3px solid #059669;
        }}
        .kpi-card.emerald {{ border-top-color: #059669; background-color: #ecfdf5; }}
        .kpi-card.blue {{ border-top-color: #0284c7; background-color: #f0f9ff; }}
        .kpi-card.amber {{ border-top-color: #d97706; background-color: #fffbeb; }}
        .kpi-card.purple {{ border-top-color: #7c3aed; background-color: #faf5ff; }}
        .kpi-card.cyan {{ border-top-color: #0891b2; background-color: #ecfeff; }}
        
        .kpi-label {{ font-size: 6.5pt; font-weight: 700; color: #475569; text-transform: uppercase; margin-bottom: 1px; }}
        .kpi-value {{ font-size: 11pt; font-weight: 800; color: #0f172a; margin-bottom: 1px; }}
        .kpi-sub {{ font-size: 6pt; color: #64748b; }}

        .section-header {{
            background-color: #047857; color: #ffffff; font-size: 7.8pt; font-weight: 700;
            padding: 3px 6px; border-radius: 3px; margin-top: 6px; margin-bottom: 4px;
            text-transform: uppercase; letter-spacing: 0.3px;
        }}
        .section-header.blue {{ background-color: #0369a1; }}
        .section-header.dark {{ background-color: #334155; }}

        .grid-2col {{ width: 100%; border-collapse: collapse; margin-bottom: 6px; }}
        .grid-2col td {{ width: 50%; vertical-align: top; border: none; padding: 0 3px; }}
        .grid-2col td:first-child {{ padding-left: 0; }}
        .grid-2col td:last-child {{ padding-right: 0; }}

        .data-table {{ width: 100%; border-collapse: collapse; font-size: 7.2pt; margin-bottom: 4px; }}
        .data-table th {{
            background-color: #f1f5f9; color: #334155; font-weight: 700;
            text-align: left; padding: 2.5px 4px; border: 1px solid #cbd5e1;
        }}
        .data-table td {{ padding: 2.5px 4px; border: 1px solid #e2e8f0; color: #1e293b; }}
        .data-table, .data-table th, .data-table td {{ page-break-inside: avoid; break-inside: avoid; }}
        .data-table tr:nth-child(even) td {{ background-color: #f8fafc; }}

        .val-bold {{ font-weight: 700; color: #0f172a; }}
        .val-green {{ font-weight: 700; color: #059669; }}
        .val-red {{ font-weight: 700; color: #dc2626; }}
        .val-blue {{ font-weight: 700; color: #0284c7; }}

        .esg-grid {{ display: flex; gap: 5px; margin-bottom: 6px; }}
        .esg-card {{
            flex: 1; border: 1px solid #cbd5e1; border-radius: 5px; padding: 5px 7px;
            background-color: #f8fafc;
        }}
        .esg-card h4 {{ margin: 0 0 2px 0; font-size: 7.5pt; color: #047857; font-weight: 700; }}
        .esg-card p {{ margin: 0; font-size: 6.8pt; color: #334155; line-height: 1.2; }}
        .esg-badge {{
            display: inline-block; padding: 1px 5px; border-radius: 3px; font-size: 6.5pt;
            font-weight: 700; background-color: #dcfce7; color: #166534; margin-top: 2px;
        }}

        .statement-box {{
            background-color: #f0fdf4; border: 1px solid #bbf7d0; border-left: 3px solid #16a34a;
            border-radius: 4px; padding: 5px 8px; margin-top: 5px; font-size: 7.2pt;
        }}
        .statement-box h4 {{ margin: 0 0 2px 0; color: #15803d; font-size: 7.8pt; }}
        .statement-box p {{ margin: 0; color: #166534; line-height: 1.25; }}

        .eq-box {{
            background-color: #f8fafc; border: 1px solid #e2e8f0; border-left: 3px solid #0891b2;
            border-radius: 4px; padding: 4px 8px; margin-top: 4px; margin-bottom: 4px; font-size: 6.8pt; color: #334155;
        }}

        .disclaimer-box {{
            background-color: #fffbeb; border: 1px solid #fef3c7; border-left: 3px solid #d97706;
            border-radius: 4px; padding: 4px 7px; margin-top: 5px; font-size: 6.8pt; color: #78350f;
        }}
        .disclaimer-box h4 {{ margin: 0 0 1px 0; color: #b45309; font-size: 7.2pt; font-weight: bold; }}
        .disclaimer-box p {{ margin: 0; line-height: 1.2; }}

        .charts-grid {{ display: flex; gap: 8px; margin-top: 4px; margin-bottom: 6px; }}
        .chart-card {{ flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 4px; text-align: center; }}
        .chart-title {{ font-size: 6.8pt; font-weight: 700; color: #475569; margin-bottom: 2px; }}
        .chart-img {{ width: 100%; max-height: 170px; object-fit: contain; }}

        .footer-table {{
            width: 100%; border-collapse: collapse; margin-top: 6px;
            border-top: 1px solid #cbd5e1; padding-top: 3px; font-size: 6.8pt; color: #64748b;
        }}
        .footer-table td {{ border: none; padding: 0; vertical-align: bottom; }}
        .sig-line {{ border-top: 1px solid #94a3b8; width: 170px; margin-top: 10px; margin-bottom: 2px; }}
    </style>
</head>
<body>
    <div class="page-container">
        <table class="header-table">
            <tr>
                <td class="doc-title" style="width: 70%;">
                    <h1>{doc_title}</h1>
                    <p style="font-size: 8.5pt; color: #0f172a;">{'Projeto' if not is_en else 'Project'}: <b>{project_name}</b></p>
                    <p>{doc_subtitle}</p>
                    <p><b>ISO 14040 / ISO 14044 · ABNT NBR 15527:2019 · GHG Protocol</b></p>
                </td>
                <td style="width: 30%; text-align: right; font-size: 7pt; color: #475569;">
                    <div>Ref: <b style="color: #0f172a;">{ref_code}</b></div>
                    <div>{'Data' if not is_en else 'Date'}: <b>{date_str}</b></div>
                    <div>{APP_VERSION_LABEL}</div>
                </td>
            </tr>
        </table>

        <table class="audit-strip"><tr>
            <td><b>{'Localidade climática' if not is_en else 'Climate location'}</b>{climate_location}</td>
            <td><b>{'Base climática' if not is_en else 'Climate basis'}</b>{climate_basis}</td>
            <td><b>{'Período da série' if not is_en else 'Series period'}</b>{climate_period}</td>
            <td><b>{'Base tarifária' if not is_en else 'Tariff location'}</b>{tariff_location}</td>
        </tr></table>

        <!-- LINHA DE CARDS DE KPI AMBIENTAIS -->
        <div class="kpi-row">
            <div class="kpi-card emerald">
                <div class="kpi-label">{'Cisterna / Economia' if not is_en else 'Tank / Savings'}</div>
                <div class="kpi-value">{lower_vol_str} L</div>
                <div class="kpi-sub"><b>{potential_pct_str}%</b> {'de substituição' if not is_en else 'potable replaced'}</div>
            </div>
            <div class="kpi-card blue">
                <div class="kpi-label">{'Carbono Incorporado' if not is_en else 'Embodied Carbon'}</div>
                <div class="kpi-value">{embodied_co2_str} kg</div>
                <div class="kpi-sub">{'Fabricação e Materiais' if not is_en else 'Materials & Equipment'}</div>
            </div>
            <div class="kpi-card emerald">
                <div class="kpi-label">{'CO2 Evitado / Ano' if not is_en else 'Avoided CO2 / Yr'}</div>
                <div class="kpi-value">{net_ann_co2_str} kg/ano</div>
                <div class="kpi-sub">{'Saldo Líquido Operacional' if not is_en else 'Net Annual Balance'}</div>
            </div>
            <div class="kpi-card cyan">
                <div class="kpi-label">{'Saldo 20 Anos (Líquido)' if not is_en else '20-Year Net Carbon'}</div>
                <div class="kpi-value">{lifetime_net_co2_str} kg</div>
                <div class="kpi-sub">{'Mitigação Total na Vida Útil' if not is_en else 'Lifetime Net Mitigation'}</div>
            </div>
            <div class="kpi-card amber">
                <div class="kpi-label">{'Payback Ambiental' if not is_en else 'Carbon Payback'}</div>
                <div class="kpi-value">{payback_env_str}</div>
                <div class="kpi-sub">{specific_g_l_str} {'evitado' if not is_en else 'avoided'}</div>
            </div>
        </div>

        <!-- SEÇÃO 1: CARACTERIZAÇÃO DO SISTEMA & HIDROLOGIA -->
        <table class="grid-2col">
            <tr>
                <td>
                    <div class="section-header">1. {'Parâmetros da Edificação & Demanda' if not is_en else '1. Building & Demand Inputs'}</div>
                    <table class="data-table">
                        <tr><th>{'Parâmetro' if not is_en else 'Parameter'}</th><th>{'Valor' if not is_en else 'Value'}</th></tr>
                        <tr><td>{'Série Pluviométrica' if not is_en else 'Rainfall Series'}</td><td class="val-bold">{rain_file}</td></tr>
                        <tr><td>{'Área de Captação (Telhado)' if not is_en else 'Catchment Area (Roof)'}</td><td class="val-bold">{area_str}</td></tr>
                        <tr><td>{'Coeficiente de Escoamento (C)' if not is_en else 'Runoff Coefficient (C)'}</td><td>{runoff_str}</td></tr>
                        <tr><td>{'Descarte Inicial (First Flush)' if not is_en else 'First Flush Discard'}</td><td>{discard_str}</td></tr>
                        <tr><td>{'Ocupantes / População' if not is_en else 'Occupants'}</td><td>{residents_str}</td></tr>
                        <tr><td>{'Demanda per capita' if not is_en else 'Per-capita Demand'}</td><td>{demand_str}</td></tr>
                        <tr><td>{'Fração Pluvial Alvo' if not is_en else 'Rainwater Target Share'}</td><td class="val-bold">{share_str}</td></tr>
                    </table>
                </td>
                <td>
                    <div class="section-header">2. {'Desempenho Hídrico (Modelo YAS)' if not is_en else '2. Hydraulic Balance (YAS Model)'}</div>
                    <table class="data-table">
                        <tr><th>{'Indicador Hídrico' if not is_en else 'Hydraulic Indicator'}</th><th>{'Resultado' if not is_en else 'Result'}</th></tr>
                        <tr><td>{'Volume da Cisterna' if not is_en else 'Storage Tank Volume'}</td><td class="val-bold">{lower_vol_str} Litros</td></tr>
                        <tr><td>{'Economia de Água Potável' if not is_en else 'Potable Savings'}</td><td class="val-green">{potential_pct_str}%</td></tr>
                        <tr><td>{'Consumo Pluvial Anual' if not is_en else 'Annual Pluvial Use'}</td><td class="val-bold">{pluv_ann_str} m³/ano ({pluv_day_str} L/dia)</td></tr>
                        <tr><td>{'Demanda Potável Residual' if not is_en else 'Residual Potable Demand'}</td><td>{potable_ann_str} m³/ano ({potable_day_str} L/dia)</td></tr>
                        <tr><td>{'Extravasamento Anual' if not is_en else 'Annual Overflow'}</td><td>{format_ptbr(annual_spill_m3, 1)} m³/ano ({spill_day_str} L/dia)</td></tr>
                        <tr><td>{'Atendimento Hídrico Integral' if not is_en else 'Full Reliability Days'}</td><td class="val-bold">{sat_full_str}% {'dos dias' if not is_en else 'of days'}</td></tr>
                        <tr><td>{'Água Total Demandada' if not is_en else 'Total Water Demand'}</td><td>{format_ptbr(total_annual_demand_m3, 1)} m³/ano</td></tr>
                    </table>
                </td>
            </tr>
        </table>

        <!-- SEÇÃO 2: INVENTÁRIO DO CICLO DE VIDA (ICV / LCI) -->
        <div class="section-header dark">3. {'Inventário do Ciclo de Vida (ICV / LCI — ISO 14040 / ISO 14044)' if not is_en else '3. Life Cycle Inventory (LCI — ISO 14040/14044)'}</div>
        <table class="data-table">
            <thead>
                <tr>
                    <th style="width: 26%;">{'Componente / Fase' if not is_en else 'Component / Phase'}</th>
                    <th style="width: 22%;">{'Quantidade / Dimensão' if not is_en else 'Quantity / Size'}</th>
                    <th style="width: 13%; text-align: right;">{'CO2 Inicial' if not is_en else 'Embodied CO2'}</th>
                    <th style="width: 13%; text-align: right;">{'CO2 Op./Ano' if not is_en else 'Op. CO2/Yr'}</th>
                    <th style="width: 13%; text-align: right;">{'Saldo 20 Anos' if not is_en else '20-Yr Balance'}</th>
                    <th style="width: 13%;">{'Fonte / Inventário' if not is_en else 'Source / Reference'}</th>
                </tr>
            </thead>
            <tbody>
                {icv_rows_html}
            </tbody>
        </table>

        <!-- SEÇÃO 3: BALANÇO DE EMISSÕES & EQUAÇÕES -->
        <div class="section-header">4. {'Balanço de Carbono, Payback Ecológico & Metodologia' if not is_en else '4. Carbon Balance, Eco-Payback & Methodology'}</div>
        <table class="data-table">
            <thead>
                <tr>
                    <th>{'Emissão Incorporada Total' if not is_en else 'Total Embodied Carbon'}</th>
                    <th>{'Bombeamento Anual' if not is_en else 'Annual Pumping'}</th>
                    <th>{'Tratamento / Cloração' if not is_en else 'Chlorination / Treatment'}</th>
                    <th>{'Crédito Água Evitada' if not is_en else 'Avoided Water Credit'}</th>
                    <th>{'Saldo Anual Líquido' if not is_en else 'Net Annual Saved'}</th>
                    <th>{'Payback Ambiental' if not is_en else 'Eco-Payback'}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="val-red">+{embodied_co2_str} kg CO2e</td>
                    <td class="val-red">+{ann_pumping_co2_str} kg/ano</td>
                    <td class="val-red">+{ann_treatment_co2_str} kg/ano ({cl2_kg_yr_str} kg Cl2/ano)</td>
                    <td class="val-green">-{ann_avoided_co2_str} kg/ano</td>
                    <td class="{'val-green' if net_ann_co2_val >= 0 else 'val-red'}">{net_ann_co2_str} kg CO2e/ano</td>
                    <td class="val-bold">{payback_env_str}</td>
                </tr>
            </tbody>
        </table>

        <div class="eq-box">
            <b>{'Fórmula e Convenção do Balanço de Carbono:' if not is_en else 'Carbon Balance Formulation & Convention:'}</b> 
            <i>{'Convenção oficial: Carbono emitido para a atmosfera é POSITIVO (+) em vermelho (impacto ambiental); carbono evitado ou retirado da atmosfera é NEGATIVO (-) em verde (benefício ecológico).' if not is_en else 'Official convention: Carbon emitted to atmosphere is POSITIVE (+) in red (environmental impact); carbon avoided/removed from atmosphere is NEGATIVE (-) in green (ecological benefit).'}</i><br/>
            <i>{'Saldo 20 Anos (kg CO2e) = CO2 Incorporado (+) + [CO2 Bombeamento (+) + CO2 Cloração (+) - CO2 Evitado da Rede (-)] × 20 anos.' if not is_en else '20-Year Net Balance (kg CO2e) = Embodied CO2 (+) + [Pumping CO2 (+) + Treatment CO2 (+) - Avoided Grid Water (-)] × 20 yrs.'}</i>
            {'O payback ambiental representa o tempo necessário para que as emissões evitadas pela água pluvial compensem integralmente o carbono incorporado nos materiais.' if not is_en else 'Environmental payback represents the time required for operational avoided emissions to offset initial material embodied carbon.'}
        </div>

        {charts_html}

        <!-- SEÇÃO 4: MATRIZ ESG & CERTIFICAÇÕES AMBIENTAIS -->
        <div class="section-header blue">5. {'Avaliação ESG & Certificações Ambientais' if not is_en else '5. ESG Rating & Green Building Certifications'}</div>
        <div class="esg-grid">
            <div class="esg-card">
                <h4>🏛️ LEED v4 / v4.1 (WE)</h4>
                <p><b>{esg_result.leed.total_leed_we_points} de 8 {'pontos (Máx: 8 pts)' if not is_en else 'points (Max: 8 pts)'}</b></p>
                <div class="esg-badge">{'Tirou' if not is_en else 'Scored'} {esg_result.leed.total_leed_we_points}/8 pts ({esg_result.leed.badge_label})</div>
                <p style="margin-top: 3px;">WEc1 (Ext.): {esg_result.leed.outdoor_water_points}/2 pts | WEc2 (Int.): {esg_result.leed.indoor_water_points}/6 pts</p>
            </div>
            <div class="esg-card">
                <h4>🌿 Processo AQUA-HQE</h4>
                <p><b>{'Nível' if not is_en else 'Level'}: {esg_result.aqua.performance_level}</b> {aqua_stars}</p>
                <p style="margin-top: 3px;">{esg_result.aqua.description}</p>
            </div>
            <div class="esg-card">
                <h4>🏠 Selo Casa Azul CAIXA</h4>
                <p><b>{'Graduação' if not is_en else 'Rating'}: {esg_result.casa_azul.category}</b></p>
                <div class="esg-badge">+{esg_result.casa_azul.points_awarded} {'pontos CAIXA' if not is_en else 'points'}</div>
                <p style="margin-top: 3px;">{esg_result.casa_azul.description}</p>
            </div>
            <div class="esg-card">
                <h4>💧 GRI 303 & Water Positive</h4>
                <p><b>{format_ptbr(esg_result.annual_potable_saved_m3, 1)} m³/ano</b> {'preservados' if not is_en else 'preserved'}</p>
                <div class="esg-badge">Ratio: {format_ptbr(esg_result.water_positive_ratio, 2)}x</div>
                <p style="margin-top: 3px;">{format_ptbr(esg_result.lifetime_potable_saved_m3, 0)} m³ {'em 20 anos' if not is_en else 'over 20 yrs'}</p>
            </div>
        </div>

        <div class="statement-box">
            <h4>🌿 {'Síntese Executiva ESG & Descarbonização' if not is_en else 'ESG Executive Synthesis & Decarbonization'}</h4>
            <p>
                {esg_result.esg_summary_text}
                {' O sistema pluvial desempenha papel essencial na mitigação de escassez hídrica urbana e resiliência climática, proporcionando redução direta de emissões de Escopo 3.' if not is_en else ' The rainwater harvesting system plays a vital role in urban water security and climate resilience, contributing directly to Scope 3 GHG mitigation.'}
            </p>
        </div>

        <div class="disclaimer-box">
            <h4>⚠️ {'Termo de Responsabilidade Técnica & Conformidade Metodológica:' if not is_en else 'Technical Responsibility & Methodological Notice:'}</h4>
            <p>
                {'Este laudo ambiental foi gerado pelo Netuno 5 seguindo as diretrizes das normas ABNT NBR 15527:2019 e ISO 14040/14044 (ACV simplificada). Os fatores de emissão adotados representam cenários médios de triagem de engenharia e devem ser validados pelo(a) especialista ambiental e projetista responsável de acordo com as EPDs dos fornecedores e matriz regional da concessionária.' if not is_en else 'This environmental report was generated by Netuno 5 following ABNT NBR 15527:2019 and ISO 14040/14044 guidelines. Emission factors represent screening engineering scenarios and must be validated by the responsible environmental professional against supplier EPDs and local utility grid parameters.'}
            </p>
        </div>

        <table class="footer-table">
            <tr>
                <td style="width: 50%;">
                    <div><b>{'Grupo de Pesquisa Gestão do Espaço Sustentável | UFSC' if not is_en else 'Sustainable Space Management Research Group | UFSC'}</b></div>
                    <div>{APP_VERSION_LABEL} — {'Laudo Ambiental e ESG gerado automaticamente' if not is_en else 'Environmental & ESG Report automatically generated'}</div>
                </td>
                <td style="width: 50%; text-align: right;">
                    <div style="display: inline-block; text-align: center;">
                        <div class="sig-line"></div>
                        <div><b>{'Responsável Técnico(a) / Especialista Ambiental' if not is_en else 'Responsible Technical Engineer / Environmental Analyst'}</b></div>
                        <div>{'CREA / CRQ / Registro Profissional' if not is_en else 'Professional Engineering / Environmental Board Registration'}</div>
                    </div>
                </td>
            </tr>
        </table>
    </div>
</body>
</html>"""
    return _localize_report_markup(html)


def generate_research_html_report(
    project_data: Dict[str, Any],
    sim_result: Optional[Any] = None,
    econ_result: Optional[Any] = None,
    lca_result: Optional[Any] = None,
) -> str:
    """
    Gera o Relatório Técnico-Científico de Pesquisa Completo (Padrão A4 Retrato),
    eliminando espaços em branco excessivos, ajustando gráficos em escala proporcional
    rigorosa (sempre contidos na largura A4 menos margens) e fornecendo descrições
    detalhadas e discussões técnicas para todas as variáveis hidrológicas, econômicas
    e ambientais (ACV/LCA).
    """
    from netuno.core.environmental import empty_environmental_result

    report_lang = get_current_lang()
    is_en = report_lang == "en"
    text = {
        "title": ("Relatório Técnico-Científico de Pesquisa", "Technical and Scientific Research Report"),
        "subtitle": ("Avaliação integrada de desempenho hídrico, viabilidade econômico-financeira e Análise do Ciclo de Vida (ACV).", "Integrated assessment of water performance, economic feasibility and life-cycle assessment (LCA)."),
        "reference": ("Código de referência", "Reference code"),
        "issued": ("Data de emissão", "Issue date"),
        "standard": ("Referência normativa", "Standards basis"),
        "summary": ("1. Síntese Comparativa para Tomada de Decisão", "1. Comparative Decision Summary"),
        "summary_text": (
            "Este relatório consolida a análise técnico-científica do sistema de aproveitamento de água de chuva, "
            "integrando a simulação hidrológica contínua (Modelo YAS — Yield After Spillage), a avaliação de viabilidade "
            "econômico-financeira por fluxo de caixa descontado e a Análise do Ciclo de Vida (ACV) simplificada. Os dados "
            "fornecem rastreabilidade completa das premissas de projeto conforme as diretrizes da norma ABNT NBR 15527:2019. "
            "Em vez de declarar uma solução universalmente ótima, o documento compara configurações de reservatório e explicita como "
            "cada critério altera o desempenho hídrico, o retorno financeiro e o balanço de gases de efeito estufa (GEE).",
            "This report consolidates the technical-scientific analysis of the rainwater harvesting system, integrating continuous "
            "hydrological simulation (YAS Model — Yield After Spillage), economic-financial feasibility via discounted cash flow, "
            "and simplified Life Cycle Assessment (LCA). The data provides complete traceability of project assumptions according "
            "to ABNT NBR 15527:2019 guidelines. Decision-making balances technical supply reliability, financial returns, and "
            "greenhouse gas (GHG) emission mitigation. Rather than declaring one universally optimal solution, the report compares "
            "storage configurations and makes the consequences of each decision criterion explicit."
        ),
        "scope": ("2. Escopo e Dados de Entrada da Edificação", "2. Scope and Building Input Data"),
        "method": ("3. Método, Fronteiras e Critérios de Comparação", "3. Method, Boundaries and Comparison Criteria"),
        "catalog": ("4. Sistemas Representativos e Diferenças Principais", "4. Representative Systems and Main Differences"),
        "hydraulic": ("5. Comparação de Desempenho Hídrico (Modelo YAS)", "5. Hydraulic Performance Comparison (YAS Model)"),
        "alternatives": ("6. Decisão Multicritério, Ranking e Trade-offs", "6. Multi-Criteria Decision, Ranking and Trade-offs"),
        "financial": ("7. Comparação Econômico-Financeira", "7. Economic and Financial Comparison"),
        "environmental": ("8. Comparação Ambiental por ACV Simplificada", "8. Environmental Comparison by Simplified LCA"),
        "uncertainty": ("9. Sensibilidade, Incertezas e Limitações", "9. Sensitivity, Uncertainty and Limitations"),
        "conclusion": ("10. Conclusões e Protocolo de Escolha", "10. Conclusions and Selection Protocol"),
        "references": ("11. Rastreabilidade, Referências e Responsabilidade Técnica", "11. Traceability, References and Professional Responsibility"),
        "parameter": ("Parâmetro / Indicador", "Parameter / Indicator"),
        "value": ("Valor Adotado", "Value"),
        "interpretation": ("Descrição Técnica e Papel no Dimensionamento", "Technical Description & Design Purpose"),
        "rain": ("Série pluviométrica", "Rainfall time series"),
        "area": ("Área de captação (telhado)", "Roof catchment area"),
        "runoff": ("Coeficiente de escoamento (Runoff C)", "Runoff coefficient (C)"),
        "discard": ("Descarte inicial (First Flush)", "First flush discard"),
        "occupants": ("População / Ocupantes", "Occupants / Inhabitants"),
        "demand": ("Demanda per capita", "Per-capita daily demand"),
        "share": ("Fração destinada à água pluvial", "Rainwater target share"),
        "tank": ("Volume da alternativa de referência", "Reference alternative storage volume"),
        "saving": ("Economia potencial de água potável", "Potential potable-water savings"),
        "pluvial": ("Consumo médio de água pluvial", "Average rainwater consumption"),
        "potable": ("Consumo complementar da rede pública", "Potable mains backup consumption"),
        "spill": ("Extravasamento médio (Overflow)", "Average overflow spill"),
        "full": ("Dias com atendimento integral (100%)", "Days with full supply (100%)"),
        "none": ("Dias sem atendimento (0%)", "Days without supply (0%)"),
        "volume": ("Volume Reservatório", "Storage Volume"),
        "use": ("Uso Pluvial Anual", "Annual Rainwater Use"),
        "capex": ("Investimento inicial (CAPEX)", "Initial investment (CAPEX)"),
        "gross": ("Economia bruta no 1º ano", "First-year gross savings"),
        "npv": ("Valor Presente Líquido (VPL em 20 anos)", "Net Present Value (NPV over 20 yrs)"),
        "irr": ("Taxa Interna de Retorno (TIR)", "Internal Rate of Return (IRR)"),
        "payback": ("Payback simples / descontado", "Simple / discounted payback"),
        "embodied": ("Carbono incorporado inicial (Embodied CO2e)", "Initial embodied carbon (Embodied CO2e)"),
        "pump": ("Emissões anuais de bombeamento elétrico", "Annual pump operational emissions"),
        "avoided": ("Emissões anuais evitadas (Rede pública)", "Annual avoided public grid emissions"),
        "net": ("Saldo anual líquido de CO2e evitado", "Annual net avoided carbon balance"),
        "life": ("Saldo acumulado em 20 anos (Vida Útil)", "Cumulative 20-year net CO2e balance"),
        "env_payback": ("Payback ambiental (Retorno de Carbono)", "Environmental payback period"),
        "not_configured": ("A ACV não foi configurada explicitamente; os indicadores ambientais permanecem em zero.", "LCA has not been explicitly configured; environmental indicators remain zero."),
        "prepared": ("Documento gerado automaticamente pelo Netuno 5 — Engine de Pesquisa e Engenharia Hídrica.", "Document generated automatically by Netuno 5 — Research & Water Engineering Engine."),
    }
    def t(key):
        source, english = text[key]
        if report_lang == "en":
            return english
        if report_lang == "pt":
            return source
        return tr(source, lang=report_lang)

    def number(value, default=0.0):
        try:
            if isinstance(value, str):
                value = value.strip().replace('.', '').replace(',', '.')
            return float(value)
        except (TypeError, ValueError):
            return default

    def num(value, decimals=1):
        return format_ptbr(number(value), decimals)

    safe = lambda value: escape(str(value if value not in (None, "") else "-"))

    lower_vol = number(project_data.get("lower_vol"))
    pluv_day = number(project_data.get("pluv_day"))
    potable_day = number(project_data.get("potable_day"))
    spill_day = number(project_data.get("spill_day"))
    potential_pct = number(project_data.get("potential_pct"))
    sat_full = number(project_data.get("sat_full"))
    sat_null = number(project_data.get("sat_null"))
    share = number(project_data.get("share"))
    if 0.0 < share <= 1.0:
        share *= 100.0
    annual_pluvial_m3 = pluv_day * 365.0 / 1000.0
    annual_spill_m3 = spill_day * 365.0 / 1000.0
    annual_potable_m3 = potable_day * 365.0 / 1000.0

    lca_result = lca_result or empty_environmental_result()
    lca_configured = any((
        lca_result.total_embodied_co2_kg,
        lca_result.annual_pumping_co2_kg,
        lca_result.annual_avoided_co2_kg,
        lca_result.lifetime_net_co2_saved_kg,
    ))

    topsis_candidates_data = project_data.get("topsis_candidates", []) or []
    if topsis_candidates_data:
        topsis_rows_html = "".join(
            f"<tr {'style=\"background-color: #dcfce7; font-weight: bold;\"' if row.get('is_best') else ''}>"
            f"<td><b>{num(row.get('volume'), 0)} L</b></td>"
            f"<td>{num(row.get('saving'), 1)}%</td>"
            f"<td>{num(row.get('water_m3'), 1)} m&sup3;/"+("ano" if not is_en else "yr")+"</td>"
            f"<td>R$ {num(row.get('capex'), 2)}</td>"
            f"<td>R$ {num(row.get('vpl'), 2)}</td>"
            f"<td>{num(row.get('co2'), 1)} kg</td>"
            f"<td>{num(row.get('score'), 2)}</td>"
            f"<td><b>#{row.get('rank')}</b></td>"
            f"</tr>"
            for row in topsis_candidates_data
        )

    def number(value, default=0.0):
        try:
            if isinstance(value, str):
                value = value.strip().replace('.', '').replace(',', '.')
            return float(value)
        except (TypeError, ValueError):
            return default

    def num(value, decimals=1):
        return format_ptbr(number(value), decimals)

    safe = lambda value: escape(str(value if value not in (None, "") else "-"))

    lower_vol = number(project_data.get("lower_vol"))
    pluv_day = number(project_data.get("pluv_day"))
    potable_day = number(project_data.get("potable_day"))
    spill_day = number(project_data.get("spill_day"))
    potential_pct = number(project_data.get("potential_pct"))
    sat_full = number(project_data.get("sat_full"))
    sat_null = number(project_data.get("sat_null"))
    share = number(project_data.get("share"))
    if 0.0 < share <= 1.0:
        share *= 100.0
    annual_pluvial_m3 = pluv_day * 365.0 / 1000.0
    annual_spill_m3 = spill_day * 365.0 / 1000.0
    annual_potable_m3 = potable_day * 365.0 / 1000.0

    lca_result = lca_result or empty_environmental_result()
    lca_configured = any((
        lca_result.total_embodied_co2_kg,
        lca_result.annual_pumping_co2_kg,
        lca_result.annual_avoided_co2_kg,
        lca_result.lifetime_net_co2_saved_kg,
    ))

    topsis_candidates_data = project_data.get("topsis_candidates", []) or []
    report_mcdm_method = str(project_data.get("mcdm_method", "topsis") or "topsis").lower()
    score_heading = (
        ("Aceitabilidade SMAA-VIKOR" if not is_en else "SMAA-VIKOR Acceptability")
        if report_mcdm_method == "smaa_vikor"
        else ("Escore TOPSIS" if not is_en else "TOPSIS Score")
    )
    score_suffix = "%" if report_mcdm_method == "smaa_vikor" else ""
    if topsis_candidates_data:
        topsis_rows_html = "".join(
            f"<tr {'style=\"background-color: #dcfce7; font-weight: bold;\"' if row.get('is_best') else ''}>"
            f"<td><b>{num(row.get('volume'), 0)} L</b></td>"
            f"<td>{num(row.get('saving'), 1)}%</td>"
            f"<td>{num(row.get('water_m3'), 1)} m&sup3;/"+("ano" if not is_en else "yr")+"</td>"
            f"<td>R$ {num(row.get('capex'), 2)}</td>"
            f"<td>R$ {num(row.get('vpl'), 2)}</td>"
            f"<td>{num(row.get('co2'), 1)} kg</td>"
            f"<td>{num(row.get('score'), 2)}{score_suffix}</td>"
            f"<td><b>#{row.get('rank')}</b></td>"
            f"</tr>"
            for row in topsis_candidates_data
        )
        topsis_full_table = (
            "<table style='width: 100%; border-collapse: collapse; margin-top: 6px;'>"
            "<thead><tr>"
            f"<th>{'Volume Cisterna' if not is_en else 'Tank Volume'}</th>"
            f"<th>{'Economia (%)' if not is_en else 'Savings (%)'}</th>"
            f"<th>{'Uso Pluvial' if not is_en else 'Rainwater Use'}</th>"
            f"<th>CAPEX</th>"
            f"<th>VPL (20 yrs)</th>"
            f"<th>{'Saldo CO2e' if not is_en else 'CO2e Saved'}</th>"
            f"<th>{score_heading}</th>"
            f"<th>Rank</th>"
            "</tr></thead><tbody>"
            f"{topsis_rows_html}"
            "</tbody></table>"
        )
    else:
        sweep_rows = project_data.get("sweep_points", []) or []
        if sweep_rows:
            sweep_html = "".join(
                f"<tr><td><b>{num(row.get('volume'), 0)} L</b></td><td>{num(row.get('saving'), 2)}%</td>"
                f"<td>{num(row.get('pluvial_m3'), 1)} m<sup>3</sup>/" + ("ano" if not is_en else "yr") + "</td>"
                f"<td>{num(row.get('spill_m3'), 1)} m<sup>3</sup>/" + ("ano" if not is_en else "yr") + "</td></tr>"
                for row in sweep_rows
            )
        else:
            sweep_html = f"<tr><td colspan='4'>{'Não há alternativas de varredura disponíveis para este relatório.' if not is_en else 'No sweep alternatives were available for this report.'}</td></tr>"
        topsis_full_table = (
            "<table style='width: 100%; border-collapse: collapse; margin-top: 6px;'>"
            "<thead><tr>"
            f"<th>{t('volume')}</th>"
            f"<th>{t('saving')}</th>"
            f"<th>{t('use')}</th>"
            f"<th>{t('spill')}</th>"
            "</tr></thead><tbody>"
            f"{sweep_html}"
            "</tbody></table>"
        )

    date_str = datetime.now().strftime("%d/%m/%Y")
    payback_s = safe(project_data.get("payback_s", "--"))
    payback_d = safe(project_data.get("payback_d", "--"))
    lang = report_lang
    annual_word = "year" if is_en else tr("ano", lang=report_lang)
    env_status = "" if lca_configured else f"<div class='notice'>{t('not_configured')}</div>"
    charts = project_data.get("report_charts", []) or []
    captured_figure_count = len(charts)

    # HTML Visual Fallbacks — Otimizados em Proporção (Compactos & 100% Compatíveis com Qt)
    svg_water_balance = f"""
    <table style='width:100%; border:1px solid #cbd5e1; border-collapse:collapse; background-color:#f8fafc; margin:10px 0;'>
        <tr>
            <td colspan='3' style='background-color:#e2e8f0; padding:6px 10px; border-bottom:1px solid #cbd5e1; font-weight:bold; font-size:9pt; color:#0369a1; text-align:center;'>
                {"Balanço Volumétrico Hídrico Anual Estimado" if not is_en else "Estimated Annual Water Balance"}
            </td>
        </tr>
        <tr>
            <td style='width:33%; padding:8px; text-align:center;'>
                <div style='background-color:#0284c7; color:white; padding:8px; border-radius:4px;'>
                    <div style='font-size:7pt; font-weight:bold; text-transform:uppercase;'>{"Atendimento Pluvial" if not is_en else "Rainwater Share"}</div>
                    <div style='font-size:14pt; font-weight:bold; margin:2px 0;'>{num(potential_pct, 1)}%</div>
                </div>
            </td>
            <td style='width:33%; padding:8px; text-align:center;'>
                <div style='background-color:#059669; color:white; padding:8px; border-radius:4px;'>
                    <div style='font-size:7pt; font-weight:bold; text-transform:uppercase;'>{"Volume Aproveitado" if not is_en else "Utilized Volume"}</div>
                    <div style='font-size:14pt; font-weight:bold; margin:2px 0;'>{num(annual_pluvial_m3, 1)} m<sup>3</sup>/{"ano" if not is_en else "yr"}</div>
                    <div style='font-size:7pt;'>({num(pluv_day, 1)} L/{"dia" if not is_en else "day"})</div>
                </div>
            </td>
            <td style='width:33%; padding:8px; text-align:center;'>
                <div style='background-color:#d97706; color:white; padding:8px; border-radius:4px;'>
                    <div style='font-size:7pt; font-weight:bold; text-transform:uppercase;'>{"Volume Extravasado" if not is_en else "Overflow Volume"}</div>
                    <div style='font-size:14pt; font-weight:bold; margin:2px 0;'>{num(annual_spill_m3, 1)} m<sup>3</sup>/{"ano" if not is_en else "yr"}</div>
                    <div style='font-size:7pt;'>({num(spill_day, 1)} L/{"dia" if not is_en else "day"})</div>
                </div>
            </td>
        </tr>
    </table>
    """

    embodied_co2 = lca_result.total_embodied_co2_kg
    lifetime_co2 = lca_result.lifetime_net_co2_saved_kg
    lifetime_is_benefit = lifetime_co2 >= 0
    lifetime_prefix = "+" if lifetime_co2 > 0 else ""
    lifetime_title = (
        ("Ano 20 — Benefício Líquido Acumulado" if not is_en else "Year 20 — Cumulative Net Benefit")
        if lifetime_is_benefit else
        ("Ano 20 — Impacto Líquido Acumulado" if not is_en else "Year 20 — Cumulative Net Impact")
    )
    lifetime_description = (
        ("Crédito operacional supera impactos incorporados e operacionais" if not is_en else "Operational credit exceeds embodied and operational impacts")
        if lifetime_is_benefit else
        ("Impactos incorporados e operacionais superam o crédito modelado" if not is_en else "Embodied and operational impacts exceed the modeled credit")
    )
    lifetime_box_bg = "#dcfce7" if lifetime_is_benefit else "#fee2e2"
    lifetime_box_border = "#86efac" if lifetime_is_benefit else "#fca5a5"
    lifetime_box_color = "#16a34a" if lifetime_is_benefit else "#dc2626"

    svg_co2_trajectory = f"""
    <table style='width:100%; border:1px solid #bbf7d0; border-collapse:collapse; background-color:#f0fdf4; margin:10px 0;'>
        <tr>
            <td colspan='2' style='background-color:#dcfce7; padding:8px 12px; border-bottom:1px solid #bbf7d0; font-weight:bold; font-size:10pt; color:#15803d; text-align:center;'>
                {"Trajetória do Saldo Acumulado de Carbono no Ciclo de Vida (20 Anos)" if not is_en else "20-Year Lifetime Cumulative Net Carbon Trajectory"}
            </td>
        </tr>
        <tr>
            <td style='width:50%; padding:10px; vertical-align:top; border-right:1px solid #bbf7d0;'>
                <div style='background-color:#fee2e2; border:1px solid #fca5a5; border-radius:4px; padding:10px; text-align:center;'>
                    <div style='font-size:8pt; font-weight:bold; color:#991b1b; text-transform:uppercase;'>{"Ano 0 — Impacto Inicial (Berço ao Portão)" if not is_en else "Year 0 — Initial Footprint (Cradle-to-Gate)"}</div>
                    <div style='font-size:16pt; font-weight:bold; color:#dc2626; margin:4px 0;'>-{num(embodied_co2, 1)} kg CO2e</div>
                    <div style='font-size:8pt; color:#7f1d1d;'>{"Emissões incorporadas de fabricação e transporte" if not is_en else "Embodied manufacturing and transport emissions"}</div>
                </div>
            </td>
            <td style='width:50%; padding:10px; vertical-align:top;'>
                <div style='background-color:{lifetime_box_bg}; border:1px solid {lifetime_box_border}; border-radius:4px; padding:10px; text-align:center;'>
                    <div style='font-size:8pt; font-weight:bold; color:{lifetime_box_color}; text-transform:uppercase;'>{lifetime_title}</div>
                    <div style='font-size:16pt; font-weight:bold; color:{lifetime_box_color}; margin:4px 0;'>{lifetime_prefix}{num(lifetime_co2, 1)} kg CO2e</div>
                    <div style='font-size:8pt; color:#334155;'>{lifetime_description}</div>
                </div>
            </td>
        </tr>
    </table>
    """

    figure_number = 0
    figure_notes = {
        "Desempenho hídrico: potencial de economia": (
            "Mostra o ganho de substituição de água potável à medida que a capacidade de armazenamento aumenta.",
            "Shows the gain in potable-water substitution as storage capacity increases.",
        ),
        "Desempenho hídrico: ganho marginal": (
            "Evidencia os rendimentos decrescentes e o ponto em que aumentar a cisterna produz pouco ganho hídrico adicional.",
            "Highlights diminishing returns and where additional tank capacity yields little extra hydraulic benefit.",
        ),
        "Desempenho hídrico: consumo pluvial e extravasamento": (
            "Compara a água efetivamente aproveitada com a parcela extravasada em cada capacidade avaliada.",
            "Compares effectively used rainwater with overflow at each evaluated capacity.",
        ),
        "Desempenho hídrico: atendimento anual": (
            "Apresenta a regularidade de atendimento integral, parcial e nulo ao longo da série simulada.",
            "Presents the frequency of full, partial, and zero supply over the simulated series.",
        ),
        "Avaliação econômica: sensibilidade do VPL": (
            "Indica quais premissas financeiras mais alteram o VPL e, portanto, merecem validação prioritária.",
            "Indicates which financial assumptions most affect NPV and therefore deserve priority validation.",
        ),
        "Avaliação econômica: VPL por volume": (
            "Permite comparar o retorno financeiro das capacidades sem confundir maior economia hídrica com maior VPL.",
            "Compares financial returns across capacities without confusing greater water savings with higher NPV.",
        ),
        "Decisão multicritério: desempenho TOPSIS": (
            "Exibe o escore de compromisso de cada alternativa sob os pesos informados; diferenças pequenas devem ser tratadas como proximidade, não superioridade absoluta.",
            "Shows each alternative's compromise score under the stated weights; small differences indicate proximity, not absolute superiority.",
        ),
        "Decisão multicritério: proximidade por eixo": (
            "Separa a proximidade aos referenciais técnico, econômico e ambiental para tornar os trade-offs visíveis.",
            "Separates proximity to technical, economic, and environmental references so trade-offs remain visible.",
        ),
        "ACV: comparação ambiental": (
            "Compara impactos incorporados, emissões operacionais e créditos ambientais dentro da fronteira adotada.",
            "Compares embodied impacts, operational emissions, and environmental credits within the adopted boundary.",
        ),
        "ACV: emissões com e sem aproveitamento": (
            "Contrasta os cenários com e sem aproveitamento de água de chuva durante o horizonte analisado.",
            "Contrasts scenarios with and without rainwater harvesting over the analysis horizon.",
        ),
        "ACV: balanço acumulado de CO2 por volume": (
            "Mostra como o saldo climático acumulado varia entre as capacidades de cisterna avaliadas.",
            "Shows how cumulative climate balance varies across evaluated tank capacities.",
        ),
    }
    figure_titles_en = {
        "Desempenho hídrico: potencial de economia": "Hydraulic performance: water-saving potential",
        "Desempenho hídrico: ganho marginal": "Hydraulic performance: marginal gain",
        "Desempenho hídrico: consumo pluvial e extravasamento": "Hydraulic performance: rainwater use and overflow",
        "Desempenho hídrico: atendimento anual": "Hydraulic performance: annual supply reliability",
        "Avaliação econômica: sensibilidade do VPL": "Economic assessment: NPV sensitivity",
        "Avaliação econômica: VPL por volume": "Economic assessment: NPV by capacity",
        "Decisão multicritério: desempenho TOPSIS": "Multi-criteria decision: TOPSIS performance",
        "Decisão multicritério: proximidade por eixo": "Multi-criteria decision: proximity by dimension",
        "ACV: comparação ambiental": "LCA: environmental comparison",
        "ACV: emissões com e sem aproveitamento": "LCA: emissions with and without rainwater harvesting",
        "ACV: balanço acumulado de CO2 por volume": "LCA: cumulative CO2 balance by capacity",
    }
    figure_titles_pt = {
        "Desempenho hídrico: potencial de economia": "Economia de água potável por capacidade",
        "Desempenho hídrico: ganho marginal": "Ganho hídrico marginal por capacidade",
        "Desempenho hídrico: consumo pluvial e extravasamento": "Uso pluvial e extravasamento por capacidade",
        "Desempenho hídrico: atendimento anual": "Atendimento anual por capacidade",
        "Decisão multicritério: desempenho TOPSIS": "Desempenho TOPSIS por capacidade",
        "Decisão multicritério: proximidade por eixo": "Proximidade multicritério por eixo",
        "Avaliação econômica: sensibilidade do VPL": "Sensibilidade do VPL",
        "Avaliação econômica: VPL por volume": "VPL por capacidade",
        "ACV: comparação ambiental": "Comparação ambiental da ACV",
        "ACV: emissões com e sem aproveitamento": "Emissões com e sem aproveitamento",
        "ACV: balanço acumulado de CO2 por volume": "Balanço acumulado de CO2 por capacidade",
    }

    def chart_gallery(chapter: str, prefix: str, fallback_html: str) -> str:
        nonlocal figure_number
        selected = [
            chart for chart in charts
            if chart.get("chapter") == chapter
            or (not chart.get("chapter") and chart.get("title", "").startswith(prefix))
        ]
        if not selected:
            return f"<section class='section'>{fallback_html}</section>" if fallback_html else ""

        figure_sections = []
        heading = "Figures generated for this chapter" if is_en else "Figuras geradas para este capítulo"
        for chart_index, chart in enumerate(selected):
            figure_number += 1
            raw_title = str(chart.get('title', ''))
            title = safe(
                figure_titles_en.get(raw_title, raw_title)
                if is_en else figure_titles_pt.get(raw_title, raw_title)
            )
            figure_label = f"{'Figure' if is_en else 'Figura'} {figure_number} — {title}"
            note_pair = figure_notes.get(raw_title, (
                "Representação gráfica dos resultados calculados para as premissas deste estudo.",
                "Graphical representation of results calculated under this study's assumptions.",
            ))
            note = note_pair[1] if is_en else note_pair[0]
            source = (
                "Source: results calculated by Netuno 5 from this study's inputs."
                if is_en else
                str(chart.get("source") or "Fonte: resultados calculados pelo Netuno 5 a partir das entradas deste estudo.")
            )
            if not is_en and not source.lower().startswith("fonte:"):
                source = f"Fonte: {source}"
            heading_html = f"<h3>{heading}</h3>" if chart_index == 0 else ""
            chapter_break = "<div style='page-break-before: always;'></div>" if chart_index == 0 else ""
            figure_sections.append(
                f"{chapter_break}"
                f"<section class='section'>"
                f"{heading_html}"
                f"<div class='fig-container-single' style='width:90%; margin-left:auto; margin-right:auto;'>"
                f"<div class='chart-fig-card'>"
                f"<div class='chart-title-above' style='padding-left:64px;'>{figure_label}</div>"
                f"<div style='text-align:center; padding:4px;'><img src='{escape(chart.get('data', ''), quote=True)}' width='520' alt='{title}' style='display:block; margin:0 auto; max-width:100%; height:auto;'/></div>"
                f"<div style='padding:5px 64px; border-top:1px solid #e2e8f0; font-size:7.5pt; color:#334155; text-align:left;'><b>{'Reading:' if is_en else 'Leitura:'}</b><br/>{safe(note)}<br/><span style='color:#64748b;'>{source}</span></div>"
                f"</div></div>"
                f"</section>"
            )
        return "".join(figure_sections)

    hydraulic_charts = chart_gallery(
        "hydraulic", "Desempenho hídrico", svg_water_balance
    )
    decision_charts = chart_gallery(
        "decision", "Decisão multicritério", ""
    )
    economic_charts = chart_gallery(
        "economic", "Avaliação econômica", ""
    )
    environmental_charts = chart_gallery(
        "environmental", "ACV", svg_co2_trajectory
    )

    def normalized_chart_chapter(chart):
        chapter = chart.get("chapter")
        if chapter:
            return chapter
        title = chart.get("title", "")
        if title.startswith("Desempenho hídrico"):
            return "hydraulic"
        if title.startswith("Decisão multicritério"):
            return "decision"
        if title.startswith("Avaliação econômica"):
            return "economic"
        if title.startswith("ACV"):
            return "environmental"
        return "other"

    figure_chapter_labels = {
        "hydraulic": ("Desempenho hídrico", "Hydraulic performance"),
        "decision": ("Decisão multicritério", "Multi-criteria decision"),
        "economic": ("Avaliação econômica", "Economic assessment"),
        "environmental": ("Análise ambiental", "Environmental assessment"),
        "other": ("Outras análises", "Other analyses"),
    }
    ordered_figures = [
        chart
        for chapter in ("hydraulic", "decision", "economic", "environmental", "other")
        for chart in charts
        if normalized_chart_chapter(chart) == chapter
    ]
    figure_catalog_rows = "".join(
        "<tr>"
        f"<td><b>{index}</b></td>"
        f"<td>{safe(figure_titles_en.get(str(chart.get('title', '')), str(chart.get('title', ''))) if is_en else figure_titles_pt.get(str(chart.get('title', '')), str(chart.get('title', ''))))}</td>"
        f"<td>{safe(figure_chapter_labels[normalized_chart_chapter(chart)][1 if is_en else 0])}</td>"
        "</tr>"
        for index, chart in enumerate(ordered_figures, start=1)
    )
    figure_catalog_html = ""
    if figure_catalog_rows:
        figure_catalog_html = f"""
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{'Lista de Figuras Geradas' if not is_en else 'List of Generated Figures'}</h2>
    <p class='chapter-intro'>
        {'As figuras abaixo foram calculadas pelo Netuno 5 a partir das mesmas entradas e alternativas apresentadas nas tabelas. A numeração segue a ordem de leitura dos capítulos.' if not is_en else 'The figures below were calculated by Netuno 5 from the same inputs and alternatives presented in the tables. Numbering follows the chapter reading order.'}
    </p>
    <table>
        <thead><tr><th style='width:10%;'>Nº</th><th>{'Figura' if not is_en else 'Figure'}</th><th style='width:28%;'>{'Capítulo temático' if not is_en else 'Thematic chapter'}</th></tr></thead>
        <tbody>{figure_catalog_rows}</tbody>
    </table>
</section>
"""

    optima = project_data.get("optima", {}) or {}
    technical_optimum = optima.get("technical", {})
    economic_optimum = optima.get("economic", {})
    environmental_optimum = optima.get("environmental", {})
    balanced_optimum = optima.get("balanced", {})
    mcdm_method = str(project_data.get("mcdm_method", "topsis") or "topsis").lower()
    is_smaa_vikor = mcdm_method == "smaa_vikor"
    mcdm_samples = int(number(project_data.get("mcdm_num_simulations"), 0.0))
    decision_label_pt = "Compromisso robusto SMAA-VIKOR" if is_smaa_vikor else "Compromisso TOPSIS"
    decision_label_en = "SMAA-VIKOR robust compromise" if is_smaa_vikor else "TOPSIS compromise"
    decision_rationale_pt = (
        "maior aceitabilidade de primeiro lugar sob pesos estocásticos"
        if is_smaa_vikor else "maior proximidade ponderada ao ideal"
    )
    decision_rationale_en = (
        "highest first-rank acceptability under stochastic weights"
        if is_smaa_vikor else "highest weighted closeness to the ideal"
    )
    method_note_pt = (
        f"O SMAA-VIKOR executou {mcdm_samples:,} simulações Monte Carlo, amostrando um vetor de pesos no simplex e recalculando o ranking VIKOR em cada amostra. A alternativa destacada é a de maior aceitabilidade de primeiro lugar; não existe um perfil único de pesos.".replace(",", ".")
        if is_smaa_vikor
        else "O TOPSIS normaliza os critérios e calcula proximidade a uma solução ideal construída. O ranking muda quando pesos, alternativas ou dados mudam; por isso, o primeiro colocado deve ser lido como compromisso sob as preferências informadas."
    )
    method_note_en = (
        f"SMAA-VIKOR ran {mcdm_samples:,} Monte Carlo simulations, sampling one simplex weight vector and recalculating the VIKOR ranking in each sample. The highlighted alternative has the highest first-rank acceptability; there is no single weight profile."
        if is_smaa_vikor
        else "TOPSIS normalizes criteria and measures closeness to a constructed ideal solution. Rankings change when weights, alternatives, or data change; the first-ranked option is therefore a compromise under the stated preferences."
    )

    def candidate_for_volume(volume):
        if not topsis_candidates_data:
            return {}
        target = number(volume, float("nan"))
        if target != target:
            return {}
        return min(
            topsis_candidates_data,
            key=lambda row: abs(number(row.get("volume")) - target),
        )

    role_specs = (
        ("technical", "Referência técnica", "Technical reference", technical_optimum,
         "maior potencial hídrico observado", "highest observed water-saving potential"),
        ("economic", "Referência econômica", "Economic reference", economic_optimum,
         "maior VPL no horizonte", "highest NPV over the horizon"),
        ("environmental", "Referência ambiental", "Environmental reference", environmental_optimum,
         "melhor saldo climático no ciclo de vida", "best life-cycle climate balance"),
        ("balanced", decision_label_pt, decision_label_en, balanced_optimum,
         decision_rationale_pt, decision_rationale_en),
    )
    representative_systems = []
    systems_by_volume = {}
    for role, label_pt, label_en, optimum, rationale_pt, rationale_en in role_specs:
        if not optimum:
            continue
        volume = number(optimum.get("volume"))
        candidate = dict(candidate_for_volume(volume))
        candidate.update({key: value for key, value in optimum.items() if value is not None})
        candidate.setdefault("volume", volume)
        candidate.setdefault("water_m3", candidate.get("water_saved", 0.0))
        candidate.setdefault("co2", 0.0)
        candidate.setdefault("vpl", 0.0)
        candidate.setdefault("capex", 0.0)
        volume_key = round(volume, 6)
        if volume_key in systems_by_volume:
            systems_by_volume[volume_key]["roles"].append(role)
            systems_by_volume[volume_key]["labels"].append(label_en if is_en else label_pt)
            systems_by_volume[volume_key]["rationales"].append(rationale_en if is_en else rationale_pt)
            continue
        candidate["roles"] = [role]
        candidate["labels"] = [label_en if is_en else label_pt]
        candidate["rationales"] = [rationale_en if is_en else rationale_pt]
        representative_systems.append(candidate)
        systems_by_volume[volume_key] = candidate

    if not representative_systems and topsis_candidates_data:
        ranked = sorted(topsis_candidates_data, key=lambda row: number(row.get("rank"), 9999.0))
        representative_systems = [dict(row, roles=["balanced"], labels=[decision_label_en if is_en else decision_label_pt], rationales=[decision_rationale_en if is_en else decision_rationale_pt]) for row in ranked[:1]]

    def format_optional(value, decimals=1, suffix=""):
        if value in (None, "", "--"):
            return "--"
        return f"{num(value, decimals)}{suffix}"

    def system_label(system):
        return " + ".join(system.get("labels", [])) or ("Alternativa" if not is_en else "Alternative")

    representative_rows = "".join(
        "<tr>"
        f"<td><b>{safe(system_label(system))}</b><br/><small>{safe('; '.join(system.get('rationales', [])))}</small></td>"
        f"<td><b>{num(system.get('volume'), 0)} L</b></td>"
        f"<td>{num(system.get('saving'), 1)}%</td>"
        f"<td>{num(system.get('water_m3', system.get('water_saved')), 1)} m&sup3;/{annual_word}</td>"
        f"<td>R$ {num(system.get('capex'), 2)}</td>"
        f"<td>R$ {num(system.get('vpl'), 2)}</td>"
        f"<td>{num(system.get('co2'), 1)} kg CO2e</td>"
        f"<td>{format_optional(system.get('score'), 3)}</td>"
        "</tr>"
        for system in representative_systems
    ) or f"<tr><td colspan='8'>{'Execute a análise multicritério para preencher a comparação.' if not is_en else 'Run the multi-criteria analysis to populate the comparison.'}</td></tr>"

    representative_table = (
        "<table class='comparison-table'><thead><tr>"
        f"<th>{'Papel na decisão' if not is_en else 'Decision role'}</th>"
        f"<th>{'Cisterna' if not is_en else 'Tank'}</th>"
        f"<th>{'Economia' if not is_en else 'Savings'}</th>"
        f"<th>{'Uso pluvial' if not is_en else 'Rainwater use'}</th>"
        "<th>CAPEX</th><th>VPL / NPV</th><th>CO2e</th><th>TOPSIS</th>"
        f"</tr></thead><tbody>{representative_rows}</tbody></table>"
    )

    sweep_points_data = project_data.get("sweep_points", []) or []
    def sweep_for_volume(volume):
        if not sweep_points_data:
            return {}
        return min(sweep_points_data, key=lambda row: abs(number(row.get("volume")) - number(volume)))

    hydraulic_rows = "".join(
        "<tr>"
        f"<td><b>{safe(system_label(system))}</b></td>"
        f"<td>{num(system.get('volume'), 0)} L</td>"
        f"<td>{num(system.get('saving'), 1)}%</td>"
        f"<td>{num(system.get('water_m3', system.get('water_saved')), 1)} m&sup3;/{annual_word}</td>"
        f"<td>{format_optional(system.get('potable_m3', sweep_for_volume(system.get('volume')).get('potable_m3')), 1, ' m&sup3;/' + annual_word)}</td>"
        f"<td>{format_optional(system.get('overflow_m3', sweep_for_volume(system.get('volume')).get('spill_m3')), 1, ' m&sup3;/' + annual_word)}</td>"
        f"<td>{format_optional(sweep_for_volume(system.get('volume')).get('sat_full'), 1, '%')}</td>"
        "</tr>"
        for system in representative_systems
    )
    hydraulic_table = (
        "<table class='comparison-table'><thead><tr>"
        f"<th>{'Sistema / papel' if not is_en else 'System / role'}</th><th>{'Cisterna' if not is_en else 'Tank'}</th>"
        f"<th>{'Economia' if not is_en else 'Savings'}</th><th>{'Uso pluvial' if not is_en else 'Rainwater use'}</th>"
        f"<th>{'Água potável' if not is_en else 'Potable water'}</th><th>{'Extravasamento' if not is_en else 'Overflow'}</th>"
        f"<th>{'Atend. integral' if not is_en else 'Full supply'}</th>"
        f"</tr></thead><tbody>{hydraulic_rows or '<tr><td colspan=\"7\">--</td></tr>'}</tbody></table>"
    )

    best_vpl = max((number(system.get("vpl")) for system in representative_systems), default=0.0)
    economic_rows = "".join(
        "<tr>"
        f"<td><b>{safe(system_label(system))}</b></td><td>{num(system.get('volume'), 0)} L</td>"
        f"<td>R$ {num(system.get('capex'), 2)}</td><td>R$ {num(system.get('vpl'), 2)}</td>"
        f"<td>R$ {num(number(system.get('vpl')) - best_vpl, 2)}</td>"
        f"<td>{format_optional(system.get('discounted_payback'), 1, ' ' + ('anos' if not is_en else 'years'))}</td>"
        f"<td>{format_optional(system.get('irr'), 1, '%')}</td>"
        "</tr>"
        for system in representative_systems
    )
    economic_table = (
        "<table class='comparison-table'><thead><tr>"
        f"<th>{'Sistema / papel' if not is_en else 'System / role'}</th><th>{'Cisterna' if not is_en else 'Tank'}</th>"
        f"<th>CAPEX</th><th>VPL / NPV</th><th>{'Dif. para maior VPL' if not is_en else 'Gap to highest NPV'}</th>"
        f"<th>{'Payback desc.' if not is_en else 'Discounted payback'}</th><th>TIR / IRR</th>"
        f"</tr></thead><tbody>{economic_rows or '<tr><td colspan=\"7\">--</td></tr>'}</tbody></table>"
    )

    best_co2 = max((number(system.get("co2")) for system in representative_systems), default=0.0)
    environmental_rows = "".join(
        "<tr>"
        f"<td><b>{safe(system_label(system))}</b></td><td>{num(system.get('volume'), 0)} L</td>"
        f"<td>{num(system.get('co2'), 1)} kg CO2e</td>"
        f"<td>{num(number(system.get('co2')) - best_co2, 1)} kg CO2e</td>"
        f"<td>{('benefício líquido modelado' if number(system.get('co2')) > 0 else 'impacto líquido modelado') if not is_en else ('modeled net benefit' if number(system.get('co2')) > 0 else 'modeled net impact')}</td>"
        "</tr>"
        for system in representative_systems
    )
    environmental_table = (
        "<table class='comparison-table'><thead><tr>"
        f"<th>{'Sistema / papel' if not is_en else 'System / role'}</th><th>{'Cisterna' if not is_en else 'Tank'}</th>"
        f"<th>{'Saldo no ciclo de vida' if not is_en else 'Life-cycle balance'}</th>"
        f"<th>{'Dif. para melhor saldo' if not is_en else 'Gap to best balance'}</th>"
        f"<th>{'Leitura' if not is_en else 'Interpretation'}</th>"
        f"</tr></thead><tbody>{environmental_rows or '<tr><td colspan=\"5\">--</td></tr>'}</tbody></table>"
    )

    def metric_range(key, fallback_key=None):
        values = [number(system.get(key, system.get(fallback_key) if fallback_key else 0.0)) for system in representative_systems]
        return (min(values), max(values)) if values else (0.0, 0.0)

    volume_range = metric_range("volume")
    saving_range = metric_range("saving")
    capex_range = metric_range("capex")
    vpl_range = metric_range("vpl")
    co2_range = metric_range("co2")
    distinct_system_count = len(representative_systems)

    if distinct_system_count > 1:
        comparison_conclusion = (
            f"As referências correspondem a {distinct_system_count} configurações distintas, entre <b>{num(volume_range[0], 0)} e {num(volume_range[1], 0)} L</b>. "
            f"Nesse conjunto, a economia varia de <b>{num(saving_range[0], 1)}% a {num(saving_range[1], 1)}%</b>, o CAPEX de "
            f"<b>R$ {num(capex_range[0], 2)} a R$ {num(capex_range[1], 2)}</b>, o VPL de <b>R$ {num(vpl_range[0], 2)} a R$ {num(vpl_range[1], 2)}</b> "
            f"e o saldo climático de <b>{num(co2_range[0], 1)} a {num(co2_range[1], 1)} kg CO2e</b>. Essas amplitudes são o núcleo da decisão; "
            "nenhum indicador, isoladamente, representa todos os objetivos.",
            f"The references correspond to {distinct_system_count} distinct configurations between <b>{num(volume_range[0], 0)} and {num(volume_range[1], 0)} L</b>. "
            f"Within this set, savings range from <b>{num(saving_range[0], 1)}% to {num(saving_range[1], 1)}%</b>, CAPEX from "
            f"<b>BRL {num(capex_range[0], 2)} to BRL {num(capex_range[1], 2)}</b>, NPV from <b>BRL {num(vpl_range[0], 2)} to BRL {num(vpl_range[1], 2)}</b>, "
            f"and the climate balance from <b>{num(co2_range[0], 1)} to {num(co2_range[1], 1)} kg CO2e</b>. These ranges are the core of the decision; "
            "no single indicator represents all objectives."
        )
    else:
        comparison_conclusion = (
            "Os critérios representativos convergem para a mesma capacidade nesta execução. Isso reduz a divergência entre os objetivos, "
            "mas não elimina incertezas de dados, pesos, tarifas, clima ou fatores ambientais.",
            "The representative criteria converge on the same capacity in this run. This reduces divergence among objectives but does not "
            "remove uncertainty in data, weights, tariffs, climate, or environmental factors."
        )

    decision_conclusion = comparison_conclusion

    if is_smaa_vikor:
        sample_text = f"{mcdm_samples:,}".replace(",", ".") if mcdm_samples else "--"
        weights_table = (
            "<table><thead><tr>"
            f"<th>{'Método robusto' if not is_en else 'Robust method'}</th>"
            f"<th>{'Configuração estocástica' if not is_en else 'Stochastic configuration'}</th>"
            "</tr></thead><tbody><tr>"
            f"<td>SMAA-VIKOR</td><td>{sample_text} "
            f"{'simulações Monte Carlo; um vetor de pesos no simplex e um ranking VIKOR por simulação' if not is_en else 'Monte Carlo simulations; one simplex weight vector and one VIKOR ranking per simulation'}</td>"
            "</tr></tbody></table>"
        )
    else:
        criterion_labels = project_data.get("topsis_criterion_labels", []) or []
        criterion_weights = project_data.get("topsis_criterion_weights", []) or []
        weight_rows = "".join(
            f"<tr><td>{safe(label)}</td><td>{num(number(weight) * 100.0, 1)}%</td></tr>"
            for label, weight in zip(criterion_labels, criterion_weights)
        )
        if not weight_rows:
            weight_rows = (
                f"<tr><td colspan='2'>{'Pesos detalhados não estavam disponíveis no estado salvo; consultar a tela TOPSIS.' if not is_en else 'Detailed weights were not available in the saved state; consult the TOPSIS screen.'}</td></tr>"
            )
        weights_table = (
            "<table><thead><tr>"
            f"<th>{'Critério TOPSIS' if not is_en else 'TOPSIS criterion'}</th>"
            f"<th>{'Peso efetivo' if not is_en else 'Effective weight'}</th>"
            f"</tr></thead><tbody>{weight_rows}</tbody></table>"
        )

    current_year = datetime.now().year

    html = f"""<!DOCTYPE html>
<html lang='{lang}'>
<head>
<meta charset='UTF-8'>
<title>{t('title')} - Netuno 5</title>
<style>
@page {{ size: A4 portrait; margin: 10mm 12mm 12mm; }}
* {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
body {{
    margin: 0; padding: 0;
    color: #0f172a; background: #ffffff;
    font-family: 'Segoe UI', Arial, Helvetica, sans-serif;
    font-size: 9pt; line-height: 1.35;
}}
.report {{ width: 100%; max-width: 790px; margin: 0 auto; }}
@media screen {{
    body {{
        background-color: #f1f5f9;
        padding: 20px 10px;
    }}
    .report {{
        background: #ffffff;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border-radius: 6px;
        padding: 32px 36px;
    }}
}}
@media print {{
    body {{ background: #ffffff; padding: 0; }}
    .report {{ margin: 0 auto; padding: 0; box-shadow: none; border-radius: 0; max-width: 100%; }}
}}

/* ── CAPA ── */
.cover-page {{
    text-align: center;
    padding: 40px 30px;
}}
.cover-institution {{
    font-size: 12pt; font-weight: bold; color: #0f172a; line-height: 1.4;
    text-transform: uppercase; margin-bottom: 40px;
    border-bottom: 2px solid #0284c7; padding-bottom: 12px;
}}
.cover-tag {{
    display: inline-block; padding: 5px 14px; background-color: #0284c7; color: white;
    font-size: 9pt; font-weight: bold; border-radius: 20px; letter-spacing: 1px; margin-bottom: 20px;
}}
.cover-title {{
    font-size: 22pt; font-weight: bold; color: #0f2b54; margin: 0 0 15px;
    line-height: 1.25; letter-spacing: -0.5px;
}}
.cover-subtitle {{
    font-size: 10pt; color: #475569; max-width: 600px; margin: 0 auto 40px; line-height: 1.5;
}}
.cover-meta {{
    background-color: #ffffff; border: 1px solid #cbd5e1; border-left: 5px solid #0284c7;
    padding: 16px 20px; margin: 0 auto 30px; max-width: 580px; text-align: left;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}}
.cover-meta-table {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
.cover-meta-table td {{ padding: 5px 8px; border: none; vertical-align: middle; color: #334155; }}
.cover-footer {{
    font-size: 9pt; font-weight: bold; color: #64748b; text-transform: uppercase;
    letter-spacing: 1px; margin-top: 40px;
}}

/* ── CABEÇALHO DA PÁGINA DE METADADOS & KPIS (PÁGINA 2) ── */
.meta-page {{
    padding-top: 10px;
}}
.header-banner {{
    background-color: #0f2b54;
    color: #ffffff; padding: 12px 16px; border-radius: 5px;
    margin-bottom: 12px; border-bottom: 3px solid #0284c7;
}}
.header-banner h1 {{
    margin: 0; font-size: 14pt; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;
}}
.header-banner p {{ margin: 2px 0 0 0; font-size: 9pt; opacity: 0.92; }}

/* Grid de Metadados em Tabela */
.meta-tbl {{
    width: 100%; border-collapse: collapse; margin-bottom: 12px;
    background-color: #f8fafc; border: 1px solid #cbd5e1; border-radius: 4px;
}}
.meta-tbl td {{
    width: 25%; padding: 6px 10px; border-right: 1px solid #e2e8f0; font-size: 9pt; vertical-align: top;
}}
.meta-tbl td:last-child {{ border-right: 0; }}
.meta-tbl b {{ display: block; color: #0369a1; font-size: 7pt; text-transform: uppercase; margin-bottom: 2px; }}

/* KPI Bar em Tabela */
.kpis-tbl {{ width: 100%; border-collapse: collapse; margin-bottom: 14px; }}
.kpis-tbl td {{ width: 25%; padding: 3px; vertical-align: top; }}
.kpi-card {{
    background-color: #f8fafc; border: 1px solid #cbd5e1; border-top: 3.5px solid #0284c7;
    border-radius: 4px; padding: 8px; text-align: center; height: 100%;
}}
.kpi-card.green {{ border-top-color: #059669; background-color: #f0fdf4; }}
.kpi-card.purple {{ border-top-color: #7c3aed; background-color: #faf5ff; }}
.kpi-card label {{ display: block; color: #475569; font-size: 7pt; font-weight: 700; text-transform: uppercase; }}
.kpi-card strong {{ display: block; color: #0f172a; font-size: 12pt; margin: 2px 0; font-weight: 800; }}
.kpi-card span {{ color: #64748b; font-size: 7pt; }}

/* ── SEÇÕES / CAPÍTULOS TCC ── */
.section {{
    margin: 15px 0 10px;
    page-break-inside: auto;
}}
h2 {{
    margin: 0 0 10px; padding: 6px 10px;
    background: #0f2b54; color: #ffffff;
    font-size: 10pt; font-weight: 700; border-radius: 3px;
    text-transform: uppercase; letter-spacing: 0.3px;
    page-break-after: avoid; break-after: avoid;
}}
h3 {{
    margin: 10px 0 5px; color: #0369a1; font-size: 9pt;
    border-bottom: 1px solid #bae6fd; padding-bottom: 3px;
    page-break-after: avoid; break-after: avoid;
}}
.chapter-intro {{ margin: 0 0 8px; font-size: 8.2pt; color: #475569; }}
.comparison-table {{ font-size: 7.2pt; table-layout: fixed; }}
.comparison-table th, .comparison-table td {{ padding: 4px 4px; word-wrap: break-word; }}
.comparison-table th:first-child, .comparison-table td:first-child {{ width: 22%; }}
.comparison-table small {{ color: #64748b; font-size: 6.5pt; line-height: 1.2; }}
.decision-note {{
    background: #eff6ff; border: 1px solid #bfdbfe; border-left: 4px solid #2563eb;
    padding: 7px 9px; margin: 7px 0 10px; color: #1e3a8a; font-size: 8pt;
}}
.method-grid {{ width: 100%; border-collapse: separate; border-spacing: 5px; margin: 0 -5px 7px; }}
.method-grid td {{ width: 33.33%; background: #f8fafc; border: 1px solid #cbd5e1; padding: 7px; }}
.method-grid strong {{ display: block; color: #0369a1; margin-bottom: 3px; }}
.limitations li {{ margin-bottom: 5px; }}

/* Tabelas Principais */
table {{ width: 100%; border-collapse: collapse; font-size: 8pt; margin-bottom: 6px; }}
thead {{ display: table-header-group; }}
tr {{ page-break-inside: avoid; break-inside: avoid; }}
th {{
    background-color: #eaf1f8; color: #1e293b; font-weight: 700;
    text-align: left; padding: 4px 6px; border: 1px solid #cbd5e1;
}}
td {{ padding: 4px 6px; border: 1px solid #e2e8f0; vertical-align: top; }}
tr:nth-child(even) td {{ background-color: #f8fafc; }}

/* Caixas de Discussão Técnica */
.disc-box {{
    background-color: #f8fafc; border-left: 3.5px solid #0369a1;
    border-radius: 0 4px 4px 0; padding: 6px 9px; margin: 6px 0 10px;
    font-size: 8pt; color: #1e293b; line-height: 1.35;
}}
.disc-box.green {{ border-left-color: #059669; background-color: #f0fdf4; }}
.disc-box.purple {{ border-left-color: #7c3aed; background-color: #faf5ff; }}
.disc-box h4 {{ margin: 0 0 2px 0; color: #0369a1; font-size: 8pt; font-weight: 700; }}
.disc-box.green h4 {{ color: #15803d; }}
.disc-box.purple h4 {{ color: #6b21a8; }}
.disc-box p {{ margin: 0 0 3px 0; }}
.disc-box p:last-child {{ margin-bottom: 0; }}

.notice {{ padding: 6px 8px; border-left: 4px solid #d97706; background: #fffbeb; color: #92400e; margin-bottom: 6px; font-size: 8pt; }}

/* Cartões de Gráficos e Imagens com Título ACIMA da Figura */
.fig-container-single {{
    width: 100%; text-align: center; margin: 8px 0 10px; page-break-inside: avoid; break-inside: avoid;
}}
.chart-fig-card {{
    border: 1px solid #cbd5e1; border-radius: 4px; background: #ffffff;
    padding: 0; text-align: center; page-break-inside: avoid; break-inside: avoid;
    box-sizing: border-box; width: 100%; max-width: 100%; overflow: hidden;
}}
.chart-title-above {{
    margin: 0; padding: 5px 8px;
    background-color: #f1f5f9; border-bottom: 1.5px solid #cbd5e1;
    color: #0f2b54; font-size: 9pt; font-weight: bold; text-align: left;
}}
.chart-img-fitted {{
    width: 100% !important; max-width: 100% !important;
    height: auto !important; max-height: 280px !important;
    object-fit: contain !important; display: block; margin: 4px auto; padding: 4px;
}}

/* Rodapé e Assinaturas com Espaço Ampliado */
.footer-sig {{
    margin-top: 60px; border-top: 1px solid #cbd5e1; padding-top: 10px;
    display: flex; justify-content: space-between; font-size: 8pt; color: #64748b;
}}
ul {{ margin: 4px 0 0 16px; padding: 0; }}
li {{ margin-bottom: 2px; }}
</style>
</head>
<body>
<main class='report'>

<!-- ══════════════════════════════════════════════════════════
     CAPA DO RELATÓRIO CIENTÍFICO (TCC) — PÁGINA 1
     ══════════════════════════════════════════════════════════ -->
<div class='cover-page'>
    <div class='cover-institution'>
        UNIVERSIDADE FEDERAL DE SANTA CATARINA — UFSC<br/>
        CENTRO TECNOLÓGICO — CTC<br/>
        GRUPO DE PESQUISA GESTÃO DO ESPAÇO SUSTENTÁVEL — GES
    </div>

    <div class='cover-center'>
        <div class='cover-tag'>NETUNO 5 — {'COMPARATIVE SYSTEMS STUDY' if is_en else 'ESTUDO COMPARATIVO DE SISTEMAS'}</div>
        <h1 class='cover-title'>{t('title').upper()}</h1>
        <p class='cover-subtitle'>
            {"Comparação integrada de configurações de aproveitamento de água de chuva: desempenho hídrico, diferenças econômico-financeiras, impactos ambientais e trade-offs multicritério" if not is_en else "Integrated comparison of rainwater harvesting configurations: hydraulic performance, economic and financial differences, environmental impacts, and multi-criteria trade-offs"}
        </p>
    </div>

    <div class='cover-meta'>
        <table class='cover-meta-table'>
            <tr><td style='width: 38%; font-weight: bold;'>Código de Referência:</td><td>{safe(project_data.get('ref_code', '-'))}</td></tr>
            <tr><td style='font-weight: bold;'>Nome do Projeto:</td><td>{safe(project_data.get('project_name', 'Projeto Netuno'))}</td></tr>
            <tr><td style='font-weight: bold;'>Diretrizes Normativas:</td><td>ABNT NBR 15527:2019 | ISO 14040/14044</td></tr>
            <tr><td style='font-weight: bold;'>Data de Emissão:</td><td>{date_str}</td></tr>
            <tr><td style='font-weight: bold;'>Responsabilidade Técnica:</td><td>Pesquisador(a) / Engenheiro(a) Responsável</td></tr>
        </table>
    </div>

    <div class='cover-footer'>
        Florianópolis – SC<br/>
        {current_year}
    </div>
</div>

{figure_catalog_html}

<!-- ══════════════════════════════════════════════════════════
     METADADOS E KPIS EXECUTIVOS — PÁGINA 2
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<div class='meta-page'>
    <div class='header-banner'>
        <h1>{t('title')}</h1>
        <p>{t('subtitle')}</p>
    </div>

    <table class='meta-tbl'>
        <tr>
            <td><b>{t('reference')}</b><br/>{safe(project_data.get('ref_code', '-'))}</td>
            <td><b>{t('issued')}</b><br/>{date_str}</td>
            <td><b>{t('standard')}</b><br/>ABNT NBR 15527:2019</td>
            <td><b>Motor / Engine</b><br/>Netuno 5 (YAS)</td>
        </tr>
        <tr>
            <td><b>{'Localidade' if not is_en else 'Location'}</b><br/>{safe(project_data.get('audit_context', {}).get('climate_location', '-'))}</td>
            <td><b>{'Base climática' if not is_en else 'Climate basis'}</b><br/>{safe(project_data.get('audit_context', {}).get('climate_basis', '-'))}</td>
            <td><b>{'Período da série' if not is_en else 'Series period'}</b><br/>{safe(project_data.get('audit_context', {}).get('climate_period', '-'))}</td>
            <td><b>{'Figuras incorporadas' if not is_en else 'Embedded figures'}</b><br/>{len(ordered_figures)}</td>
        </tr>
    </table>

    <table class='kpis-tbl'>
        <tr>
            <td>
                <div class='kpi-card green'>
                    <label>{'Sistemas representativos' if not is_en else 'Representative systems'}</label><br/>
                    <strong>{distinct_system_count}</strong>
                    <span>{'configurações distintas' if not is_en else 'distinct configurations'}</span>
                </div>
            </td>
            <td>
                <div class='kpi-card green'>
                    <label>{'Faixa de cisternas' if not is_en else 'Tank range'}</label><br/>
                    <strong>{num(volume_range[0], 0)}-{num(volume_range[1], 0)} L</strong>
                    <span>{'referências por objetivo' if not is_en else 'objective-based references'}</span>
                </div>
            </td>
            <td>
                <div class='kpi-card'>
                    <label>{'Faixa de VPL' if not is_en else 'NPV range'}</label><br/>
                    <strong>R$ {num(vpl_range[0], 0)} a {num(vpl_range[1], 0)}</strong>
                    <span>{'horizonte informado' if not is_en else 'reported horizon'}</span>
                </div>
            </td>
            <td>
                <div class='kpi-card purple'>
                    <label>{'Faixa de saldo climático' if not is_en else 'Climate balance range'}</label><br/>
                    <strong>{num(co2_range[0], 1)} a {num(co2_range[1], 1)} kg</strong>
                    <span>CO2e {'no ciclo de vida' if not is_en else 'over the life cycle'}</span>
                </div>
            </td>
        </tr>
    </table>

    <div class='disc-box green' style='margin-top: 15px;'>
        <h4>📌 {"Orientações sobre a Estruturação Científica do Relatório" if not is_en else "Guidelines on Scientific Report Structure"}</h4>
        <p>
            {"A leitura começa pelas diferenças entre sistemas e só então aprofunda os eixos hídrico, econômico e ambiental. Os termos referência técnica, econômica e ambiental identificam resultados de critérios diferentes; compromisso TOPSIS identifica a alternativa mais próxima do ideal ponderado, não um ótimo absoluto." if not is_en else "The report starts with differences among systems and then examines the hydraulic, economic and environmental dimensions. Technical, economic and environmental references are criterion-specific results; the TOPSIS compromise is the alternative closest to the weighted ideal, not an absolute optimum."}
        </p>
        <p>
            {f"Foram incorporadas <b>{captured_figure_count} figuras calculadas</b>, distribuídas nos capítulos temáticos com legenda, leitura e fonte." if not is_en else f"The report includes <b>{captured_figure_count} calculated figures</b>, distributed across thematic chapters with captions, interpretation, and source."}
        </p>
    </div>
</div>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 1: RESUMO EXECUTIVO — PÁGINA 3
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('summary')}</h2>
    <div class='disc-box green'>
        <h4>📌 {"Síntese de Engenharia Hídrica & Integração Multicritério" if not is_en else "Executive Water Engineering & Multi-Criteria Synthesis"}</h4>
        <p>{t('summary_text')}</p>
    </div>

    <h3>{"1.1 Quadro comparativo das referências de decisão" if not is_en else "1.1 Comparison of decision references"}</h3>
    {representative_table}
    <div class='decision-note'>{comparison_conclusion[1] if is_en else comparison_conclusion[0]}</div>
    <h3>{"1.2 Como interpretar este relatório" if not is_en else "1.2 How to read this report"}</h3>
    <p class='chapter-intro'>
        {"Cada linha representa uma configuração física de cisterna sob as mesmas premissas de chuva, demanda, tarifa e ACV. Quando dois critérios apontam o mesmo volume, seus papéis são consolidados na mesma linha. Valores de VPL e CO2e podem ser negativos; isso é informação de desempenho, não erro de apresentação." if not is_en else "Each row represents a physical tank configuration under the same rainfall, demand, tariff, and LCA assumptions. When two criteria point to the same volume, their roles are combined in one row. NPV and CO2e values may be negative; that is performance information, not a presentation error."}
    </p>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 2: ESCOPO E DADOS DE ENTRADA — PÁGINA 4
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('scope')}</h2>
    <p style='margin-bottom: 6px; font-size: 8pt; color: #475569;'>
        {"Este capítulo detalha as premissas físicas e operacionais da edificação, os dados pluviométricos históricos adotados para a localidade e os parâmetros normativos de captação conforme a norma ABNT NBR 15527:2019." if not is_en else "This chapter details the physical and operational premises of the building, the historical rainfall data adopted for the location, and the normative catchment parameters according to ABNT NBR 15527:2019."}
    </p>
    <table>
        <thead>
            <tr>
                <th style='width: 55%;'>Dado / Parâmetro</th>
                <th style='width: 45%;'>Valor</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>{t('rain')}</b></td>
                <td><b>{safe(project_data.get('rain_file', '-'))}</b></td>
            </tr>
            <tr>
                <td><b>{t('area')}</b></td>
                <td><b>{num(project_data.get('area'), 1)} m²</b></td>
            </tr>
            <tr>
                <td><b>{t('runoff')}</b></td>
                <td><b>{num(project_data.get('runoff'), 2)}</b></td>
            </tr>
            <tr>
                <td><b>{t('discard')}</b></td>
                <td><b>{num(project_data.get('discard'), 1)} mm</b></td>
            </tr>
            <tr>
                <td><b>{t('occupants')}</b></td>
                <td><b>{num(project_data.get('residents'), 0)} {"pessoas" if not is_en else "people"}</b></td>
            </tr>
            <tr>
                <td><b>{t('demand')}</b></td>
                <td><b>{num(project_data.get('demand'), 0)} L/{"hab/dia" if not is_en else "person/day"}</b></td>
            </tr>
            <tr>
                <td><b>{t('share')}</b></td>
                <td><b>{num(share, 0)}%</b></td>
            </tr>
            <tr>
                <td><b>{'Localidade / estação climática' if not is_en else 'Climate location / station'}</b></td>
                <td><b>{safe(project_data.get('audit_context', {}).get('climate_location', '-'))}</b></td>
            </tr>
            <tr>
                <td><b>{'Modelo e cenário climático' if not is_en else 'Climate model and scenario'}</b></td>
                <td><b>{safe(project_data.get('audit_context', {}).get('climate_basis', '-'))}</b></td>
            </tr>
            <tr>
                <td><b>{'Período climático analisado' if not is_en else 'Analyzed climate period'}</b></td>
                <td><b>{safe(project_data.get('audit_context', {}).get('climate_period', '-'))}</b></td>
            </tr>
            <tr>
                <td><b>{'Horizonte econômico' if not is_en else 'Economic horizon'}</b></td>
                <td><b>{num(project_data.get('audit_context', {}).get('analysis_period_years', 20), 0)} {'anos' if not is_en else 'years'}</b></td>
            </tr>
            <tr>
                <td><b>{'Localidade tarifária' if not is_en else 'Tariff location'}</b></td>
                <td><b>{safe(project_data.get('audit_context', {}).get('tariff_location', '-'))}</b></td>
            </tr>
        </tbody>
    </table>
    <h3>{"2.1 Configuração física comum às alternativas" if not is_en else "2.1 Physical configuration shared by alternatives"}</h3>
    <table>
        <thead><tr><th>{"Componente / condição" if not is_en else "Component / condition"}</th><th>{"Valor registrado" if not is_en else "Recorded value"}</th></tr></thead>
        <tbody>
            <tr><td>{"Reservatório superior em uso" if not is_en else "Upper tank in use"}</td><td>{("Sim" if project_data.get('system_design', {}).get('upper_used') else "Não") if not is_en else ("Yes" if project_data.get('system_design', {}).get('upper_used') else "No")}</td></tr>
            <tr><td>{"Volume do reservatório superior" if not is_en else "Upper-tank volume"}</td><td>{num(project_data.get('system_design', {}).get('upper_volume_l'), 0)} L</td></tr>
            <tr><td>{"Potência nominal da bomba" if not is_en else "Nominal pump power"}</td><td>{safe(project_data.get('system_design', {}).get('pump_power_cv', '-'))} CV / {num(project_data.get('system_design', {}).get('pump_power_kw'), 3)} kW</td></tr>
            <tr><td>{"Vazão nominal da bomba" if not is_en else "Nominal pump flow"}</td><td>{num(project_data.get('system_design', {}).get('pump_flow_l_h'), 0)} L/h</td></tr>
            <tr><td>{"Quantidade de bombas" if not is_en else "Pump count"}</td><td>{num(project_data.get('system_design', {}).get('pump_count'), 0)}</td></tr>
            <tr><td>{"Limiar de acionamento informado" if not is_en else "Reported activation threshold"}</td><td>{safe(project_data.get('system_design', {}).get('pump_threshold_pct', '-'))}%</td></tr>
        </tbody>
    </table>
    <p class='chapter-intro'>{"Na comparação, o volume da cisterna inferior varia; os demais parâmetros permanecem constantes, salvo indicação explícita nos dados do cenário." if not is_en else "In the comparison, lower-tank volume varies; other parameters remain constant unless scenario data explicitly state otherwise."}</p>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 3: MÉTODO E CRITÉRIOS
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('method')}</h2>
    <p class='chapter-intro'>
        {"O estudo mantém constantes as premissas da edificação e varia a capacidade do reservatório inferior. Para cada capacidade, o Netuno calcula o balanço hídrico diário, associa os fluxos econômicos e estima o balanço climático. A comparação só é válida dentro da grade e das fronteiras declaradas." if not is_en else "The study holds building assumptions constant and varies lower-tank capacity. For each capacity, Netuno calculates the daily water balance, associates financial cash flows, and estimates the climate balance. Comparisons are valid only within the declared grid and boundaries."}
    </p>
    <table class='method-grid'><tr>
        <td><strong>{"Eixo hídrico" if not is_en else "Hydraulic dimension"}</strong><br/>{"Modelo YAS diário; economia potável, uso pluvial, extravasamento e regularidade de atendimento." if not is_en else "Daily YAS model; potable savings, rainwater use, overflow, and supply reliability."}</td>
        <td><strong>{"Eixo econômico" if not is_en else "Economic dimension"}</strong><br/>{"CAPEX, economia tarifária, VPL, TIR e payback, todos condicionados ao horizonte e às premissas financeiras." if not is_en else "CAPEX, tariff savings, NPV, IRR, and payback, all conditional on the time horizon and financial assumptions."}</td>
        <td><strong>{"Eixo ambiental" if not is_en else "Environmental dimension"}</strong><br/>{"ACV simplificada: carbono incorporado, operação e crédito por água potável substituída." if not is_en else "Simplified LCA: embodied carbon, operation, and credit for displaced potable water."}</td>
    </tr></table>
    <h3>{"3.1 Critérios e pesos efetivos" if not is_en else "3.1 Criteria and effective weights"}</h3>
    {weights_table}
    <div class='decision-note'>
        {method_note_en if is_en else method_note_pt}
    </div>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 4: CATÁLOGO COMPARATIVO
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('catalog')}</h2>
    <p class='chapter-intro'>
        {"As configurações abaixo são pontos de referência para discussão, não recomendações automáticas. Elas condensam os volumes que se destacam em objetivos diferentes e evitam repetir dezenas de linhas da varredura antes de o leitor compreender as diferenças relevantes." if not is_en else "The configurations below are reference points for discussion, not automatic recommendations. They condense the capacities that stand out under different objectives and avoid presenting dozens of sweep rows before the reader understands the relevant differences."}
    </p>
    {representative_table}
    <h3>{"4.1 Amplitude observada entre os sistemas" if not is_en else "4.1 Observed range across systems"}</h3>
    <div class='disc-box purple'><p>{comparison_conclusion[1] if is_en else comparison_conclusion[0]}</p></div>
    <h3>{"4.2 Regra de leitura" if not is_en else "4.2 Reading rule"}</h3>
    <ul>
        <li>{"Referência técnica: privilegia desempenho hídrico observado; não implica melhor retorno financeiro." if not is_en else "Technical reference: prioritizes observed hydraulic performance; it does not imply the best financial return."}</li>
        <li>{"Referência econômica: privilegia o maior VPL nas premissas vigentes; pode reduzir desempenho hídrico ou ambiental." if not is_en else "Economic reference: prioritizes the highest NPV under current assumptions; it may reduce hydraulic or environmental performance."}</li>
        <li>{"Referência ambiental: privilegia o melhor saldo climático modelado; depende fortemente da fronteira e dos fatores de emissão." if not is_en else "Environmental reference: prioritizes the best modeled climate balance; it depends strongly on boundaries and emission factors."}</li>
        <li>{(decision_label_en if is_en else decision_label_pt)}: {("resume a frequência de primeiro lugar sob os pesos amostrados; não substitui justificativa de engenharia." if not is_en else "summarizes first-rank frequency under sampled weights; it does not replace engineering justification.") if is_smaa_vikor else ("combina os critérios conforme os pesos; não substitui justificativa de engenharia." if not is_en else "combines criteria according to weights; it does not replace engineering justification.")}</li>
    </ul>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 5: DESEMPENHO HÍDRICO (YAS)
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('hydraulic')}</h2>
    <p style='margin-bottom: 6px; font-size: 8pt; color: #475569;'>
        {"Análise computacional da simulação estocástica/contínua diária do reservatório (Algoritmo YAS — Yield After Spillage). Apresenta os indicadores operacionais de suprimento hídrico e a disposição sequencial das figuras de desempenho hídrico." if not is_en else "Computational analysis of continuous daily tank simulation (YAS Algorithm — Yield After Spillage). Presents operational water supply indicators and sequential layout of hydraulic performance figures."}
    </p>
    {hydraulic_table}

    <div class='disc-box'>
        <h4>📊 {"Discussão Técnica sobre o Balanço Hídrico (Modelo YAS)" if not is_en else "Technical Discussion on Hydrological Water Balance (YAS Model)"}</h4>
        <p>
            {"A simulação contínua diária pelo modelo YAS (Yield After Spillage) contabiliza o armazenamento ao longo da série histórica. "
             "O aumento da cisterna tende a ampliar o uso pluvial e reduzir o extravasamento, mas os ganhos marginais diminuem à medida que chuva, área de captação e demanda passam a limitar o sistema. "
             "A tabela deve ser lida horizontalmente: mostra quanto desempenho hídrico se ganha ou perde ao migrar entre as referências, sem pressupor que a maior cisterna seja a melhor escolha global."
             if not is_en else
             "The continuous daily YAS (Yield After Spillage) simulation tracks storage over the climate series. A larger tank tends to increase rainwater use and reduce overflow, but marginal gains decline as rainfall, catchment area, and demand become limiting factors. Read the table horizontally: it shows the hydraulic gain or loss when moving among references without assuming that the largest tank is the best overall choice."}
        </p>
    </div>

</section>
{hydraulic_charts}

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 4: VARREDURA E TOPSIS — PÁGINA 6
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('alternatives')}</h2>
    <p style='margin-bottom: 6px; font-size: 8pt; color: #475569;'>
        {"Avaliação multicritério das alternativas varridas. O ranking agrega preferências; as tabelas de diferenças preservam os valores físicos e econômicos que o escore normalizado, sozinho, não comunica." if not is_en else "Multi-criteria evaluation of swept alternatives. The ranking aggregates preferences; difference tables preserve physical and economic values that the normalized score alone does not communicate."}
    </p>
    
    <div style='font-weight: bold; margin-bottom: 4px; color: #0369a1;'>
        {"6.1 Referências por objetivo e compromisso ponderado" if not is_en else "6.1 Objective-based references and weighted compromise"}
    </div>
    {representative_table}

    <div class='disc-box purple' style='margin-top: 6px;'>
        <h4>⚖️ {(f"Discussão de Decisão Multicritério ({'SMAA-VIKOR' if is_smaa_vikor else 'TOPSIS'} & Trade-off)" if not is_en else f"Multi-Criteria Decision Discussion ({'SMAA-VIKOR' if is_smaa_vikor else 'TOPSIS'} & Trade-offs)")}</h4>
        <p>
            {f"A <b>referência técnica</b> representa o destaque hídrico do conjunto; a <b>referência econômica</b>, o maior VPL; a <b>referência ambiental</b>, o melhor saldo climático modelado; e o <b>{decision_label_pt.lower()}</b>, {decision_rationale_pt}. "
             f"{decision_conclusion[0]}"
             if not is_en else
             f"The <b>technical reference</b> represents the hydraulic highlight of the set; the <b>economic reference</b>, the highest NPV; the <b>environmental reference</b>, the best modeled climate balance; and the <b>{decision_label_en.lower()}</b>, {decision_rationale_en}. {decision_conclusion[1]}"}
        </p>
    </div>

    <div style='font-weight: bold; margin: 8px 0 4px; color: #0369a1;'>
        {"6.2 Matriz de decisão e ranking de todas as alternativas" if not is_en else "6.2 Decision matrix and ranking of all alternatives"}
    </div>
    {topsis_full_table}
</section>
{decision_charts}

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 5: AVALIAÇÃO ECONÔMICA — PÁGINA 7
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('financial')}</h2>
    <p style='margin-bottom: 6px; font-size: 8pt; color: #475569;'>
        {"Estudo de viabilidade econômico-financeira baseado na metodologia do Fluxo de Caixa Descontado (FCD) ao longo do horizonte analítico de 20 anos, incorporando reajustes tarifários e taxa de desconto." if not is_en else "Economic-financial feasibility study based on Discounted Cash Flow (DCF) over a 20-year analytical horizon, incorporating tariff escalation and discount rates."}
    </p>
    {economic_table}

    <div class='disc-box'>
        <h4>💰 {"Discussão Técnica sobre Viabilidade Financeira & Fluxo de Caixa" if not is_en else "Technical Discussion on Financial Feasibility & Cash Flow"}</h4>
        <p>
            {"A análise usa Fluxo de Caixa Descontado no horizonte informado. A coluna diferença para o maior VPL quantifica o custo de oportunidade financeiro de privilegiar outro objetivo. "
             "VPL positivo indica retorno acima da taxa de desconto nas premissas adotadas; VPL negativo indica que a alternativa não recupera o custo de oportunidade modelado. "
             "TIR e payback devem ser comparados com a taxa mínima de atratividade, o horizonte e o risco dos parâmetros, sem linguagem automática de aprovação do investimento. "
             "Estrutura tarifária oficial auditada e validada em 27/08/2026 (recomenda-se confirmar a vigência de eventuais reajustes recentes homologados)."
             if not is_en else
             "The analysis uses Discounted Cash Flow over the reported horizon. The gap-to-highest-NPV column quantifies the financial opportunity cost of prioritizing another objective. Positive NPV indicates a return above the discount rate under the stated assumptions; negative NPV means the modeled opportunity cost is not recovered. IRR and payback must be compared with the hurdle rate, horizon, and parameter risk without automatic investment-approval language. Official municipal tariffs audited and validated on 27/08/2026 (confirming recent regulatory updates is recommended)."}
        </p>
    </div>

</section>
{economic_charts}

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 6: ACV / LCA — PÁGINA 8
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('environmental')}</h2>
    <p style='margin-bottom: 6px; font-size: 8pt; color: #475569;'>
        {"Análise do Ciclo de Vida (ACV) simplificada calculando as emissões de carbono incorporado no sistema versus o abatedouro de emissões operacionais de abastecimento público." if not is_en else "Simplified Life Cycle Assessment (LCA) calculating embodied carbon emissions vs. operational avoided emissions from municipal water supply."}
    </p>
    {env_status}
    <h3>{"8.1 Comparação do saldo climático entre sistemas" if not is_en else "8.1 Climate-balance comparison across systems"}</h3>
    {environmental_table}
    <h3>{"8.2 Inventário detalhado da alternativa usada como referência no relatório" if not is_en else "8.2 Detailed inventory for the report reference alternative"}</h3>
    <table>
        <thead>
            <tr>
                <th style='width: 55%;'>Dado / Parâmetro</th>
                <th style='width: 45%;'>Valor</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><b>{t('embodied')}</b></td>
                <td class='val-red'><b>+{num(lca_result.total_embodied_co2_kg, 1)} kg CO2e</b></td>
            </tr>
            <tr>
                <td><b>{t('pump')}</b></td>
                <td class='val-red'><b>+{num(lca_result.annual_pumping_co2_kg, 1)} kg CO2e/{"ano" if not is_en else "yr"}</b></td>
            </tr>
            <tr>
                <td><b>{"Cloração calculada" if not is_en else "Calculated chlorination"}</b></td>
                <td><b>{num(lca_result.annual_chlorine_kg, 3)} kg Cl2/{"ano" if not is_en else "yr"} ({num(lca_result.chlorine_dose_mg_l, 2)} mg/L)</b></td>
            </tr>
            <tr>
                <td><b>{"Emissão da cloração" if not is_en else "Chlorination emissions"}</b></td>
                <td class='val-red'><b>+{num(lca_result.annual_treatment_co2_kg, 2)} kg CO2e/{"ano" if not is_en else "yr"} ({num(lca_result.treatment_co2_kg_per_m3, 3)} kg CO2e/m³)</b></td>
            </tr>
            <tr>
                <td><b>{t('avoided')}</b></td>
                <td class='val-green'><b>-{num(lca_result.annual_avoided_co2_kg, 1)} kg CO2e/{"ano" if not is_en else "yr"}</b></td>
            </tr>
            <tr>
                <td><b>{t('net')}</b></td>
                <td class='{"val-green" if lca_result.net_annual_avoided_co2_kg >= 0 else "val-red"}'><b>{("-" if lca_result.net_annual_avoided_co2_kg >= 0 else "+") + num(abs(lca_result.net_annual_avoided_co2_kg), 1)} kg CO2e/{"ano" if not is_en else "yr"}</b></td>
            </tr>
            <tr>
                <td><b>{t('life')}</b></td>
                <td class='{"val-green" if lca_result.lifetime_net_co2_saved_kg >= 0 else "val-red"}'><b>{("-" if lca_result.lifetime_net_co2_saved_kg >= 0 else "+") + num(abs(lca_result.lifetime_net_co2_saved_kg), 1)} kg CO2e</b></td>
            </tr>
            <tr>
                <td><b>{t('env_payback')}</b></td>
                <td><b>{num(lca_result.environmental_payback_years, 1)} {"anos" if not is_en else "years"}</b></td>
            </tr>
        </tbody>
    </table>

    <div class='disc-box green'>
        <h4>🌱 {"Discussão Técnica de Análise do Ciclo de Vida (ACV)" if not is_en else "Technical Discussion on Life Cycle Assessment (LCA)"}</h4>
        <p>
            {"A ACV simplificada é uma triagem comparativa. Na convenção oficial do Netuno 5, emissões à atmosfera são positivas (+) e associadas ao vermelho (impacto ambiental), enquanto emissões evitadas ou carbono retirado da atmosfera são negativos (-) e associados ao verde (benefício ecológico). "
             f"Para a alternativa detalhada, o carbono incorporado inicial é <b>+{num(lca_result.total_embodied_co2_kg, 1)} kg CO2e</b> e o payback calculado é <b>{num(lca_result.environmental_payback_years, 1)} anos</b>. "
             "Esses números não atestam sustentabilidade; dependem de quantitativos, fatores, fronteiras, vida útil e crédito atribuído à água substituída."
             if not is_en else
             f"The simplified LCA is a comparative screening assessment. Under Netuno 5's official convention, atmospheric emissions are positive (+) in red (environmental impact), whereas avoided emissions or removed carbon are negative (-) in green (ecological benefit). For the detailed alternative, initial embodied carbon is <b>+{num(lca_result.total_embodied_co2_kg, 1)} kg CO2e</b> and calculated payback is <b>{num(lca_result.environmental_payback_years, 1)} years</b>. These figures do not certify sustainability; they depend on quantities, factors, boundaries, service life, and the credit assigned to displaced water."}
        </p>
    </div>

</section>
{environmental_charts}

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 9: INCERTEZAS E LIMITAÇÕES
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('uncertainty')}</h2>
    <p class='chapter-intro'>
        {"As diferenças numéricas deste relatório são condicionais, não previsões determinísticas. A robustez da escolha depende de quanto o ranking e os sinais de VPL/CO2e resistem a variações plausíveis nas entradas." if not is_en else "The numerical differences in this report are conditional, not deterministic forecasts. Selection robustness depends on whether the ranking and the signs of NPV/CO2e persist under plausible input changes."}
    </p>
    <ul class='limitations'>
        <li><b>{"Clima e série histórica:" if not is_en else "Climate and historical series:"}</b> {"cobertura temporal, falhas, representatividade e mudanças climáticas podem alterar regularidade e extravasamento." if not is_en else "record length, gaps, representativeness, and climate change may alter reliability and overflow."}</li>
        <li><b>{"Demanda e comportamento:" if not is_en else "Demand and behavior:"}</b> {"ocupação, usos não potáveis e sazonalidade devem ser testados em cenários baixo, central e alto." if not is_en else "occupancy, non-potable uses, and seasonality should be tested under low, central, and high scenarios."}</li>
        <li><b>{"Economia:" if not is_en else "Economics:"}</b> {"CAPEX, manutenção, tarifa, reajuste e taxa de desconto podem inverter VPL, TIR e payback." if not is_en else "CAPEX, maintenance, tariffs, escalation, and discount rate may reverse NPV, IRR, and payback."}</li>
        <li><b>{"ACV:" if not is_en else "LCA:"}</b> {"massa de materiais, origem da eletricidade, eficiência de bombeamento, tratamento evitado e vida útil controlam o saldo climático." if not is_en else "material mass, electricity source, pump efficiency, displaced treatment, and service life control the climate balance."}</li>
        <li><b>{"Decisão multicritério:" if not is_en else "Multi-criteria decision:"}</b> {(f"a aceitabilidade resulta de {mcdm_samples:,} amostras de pesos; registre a semente, o total de simulações e a estabilidade dos postos.".replace(",", ".") if not is_en else f"acceptability is based on {mcdm_samples:,} weight samples; record the seed, simulation count, and rank stability.") if is_smaa_vikor else ("pesos são preferências declaradas; recomenda-se repetir o TOPSIS com pesos alternativos e registrar mudanças no primeiro colocado." if not is_en else "weights express stated preferences; rerun TOPSIS with alternative weights and record changes in the first-ranked option.")}</li>
    </ul>
    <div class='decision-note'>
        {"Critério mínimo de robustez sugerido: a alternativa escolhida deve permanecer tecnicamente aceitável nos cenários adversos, manter indicadores econômicos compatíveis com a política do decisor e não depender de um único fator ambiental sem fonte rastreável." if not is_en else "Suggested minimum robustness criterion: the selected alternative should remain technically acceptable under adverse scenarios, maintain economic indicators compatible with the decision maker's policy, and not depend on a single environmental factor without a traceable source."}
    </div>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 10: CONCLUSÕES E PROTOCOLO
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('conclusion')}</h2>
    <div class='disc-box green'><p>{comparison_conclusion[1] if is_en else comparison_conclusion[0]}</p></div>
    <h3>{"10.1 Protocolo recomendado para registrar a decisão" if not is_en else "10.1 Recommended protocol for documenting the decision"}</h3>
    <table>
        <thead><tr><th style='width:12%;'>{"Etapa" if not is_en else "Step"}</th><th style='width:35%;'>{"Pergunta" if not is_en else "Question"}</th><th>{"Registro esperado" if not is_en else "Expected record"}</th></tr></thead>
        <tbody>
            <tr><td><b>1</b></td><td>{"Quais restrições são inegociáveis?" if not is_en else "Which constraints are non-negotiable?"}</td><td>{"Espaço, volume comercial, orçamento, atendimento mínimo e requisitos normativos." if not is_en else "Space, commercial size, budget, minimum service, and regulatory requirements."}</td></tr>
            <tr><td><b>2</b></td><td>{"Qual objetivo tem prioridade e por quê?" if not is_en else "Which objective has priority and why?"}</td><td>{((f"Justificativa técnica, econômica, ambiental ou de compromisso; perfil SMAA-VIKOR com {mcdm_samples:,} simulações.".replace(",", ".")) if is_smaa_vikor else "Justificativa técnica, econômica, ambiental ou de compromisso; pesos TOPSIS aprovados.") if not is_en else ((f"Technical, economic, environmental, or compromise rationale; SMAA-VIKOR profile with {mcdm_samples:,} simulations.") if is_smaa_vikor else "Technical, economic, environmental, or compromise rationale; approved TOPSIS weights.")}</td></tr>
            <tr><td><b>3</b></td><td>{"Quanto custa migrar para outra referência?" if not is_en else "What is the cost of moving to another reference?"}</td><td>{"Diferenças de cisterna, economia hídrica, CAPEX, VPL e CO2e extraídas das tabelas comparativas." if not is_en else "Differences in tank size, water savings, CAPEX, NPV, and CO2e from the comparison tables."}</td></tr>
            <tr><td><b>4</b></td><td>{"A escolha resiste às incertezas?" if not is_en else "Is the choice robust to uncertainty?"}</td><td>{"Cenários testados, parâmetros críticos, mudanças de ranking e margens de segurança." if not is_en else "Scenarios tested, critical parameters, ranking changes, and safety margins."}</td></tr>
            <tr><td><b>5</b></td><td>{"Qual configuração será adotada?" if not is_en else "Which configuration will be adopted?"}</td><td>{"Volume final, componentes, premissas, responsável, data e justificativa assinada." if not is_en else "Final capacity, components, assumptions, responsible party, date, and signed rationale."}</td></tr>
        </tbody>
    </table>
    <p class='chapter-intro'>
        {"O Netuno apoia essa decisão, mas não substitui o projeto executivo, a verificação normativa, a análise de riscos nem a responsabilidade técnica." if not is_en else "Netuno supports this decision but does not replace detailed design, regulatory verification, risk analysis, or professional responsibility."}
    </p>
</section>

<!-- ══════════════════════════════════════════════════════════
     CAPÍTULO 11: REFERÊNCIAS E ASSINATURA
     ══════════════════════════════════════════════════════════ -->
<div style='page-break-before: always;'></div>
<section class='section'>
    <h2>{t('references')}</h2>
    <ul>
        <li><b>ABNT NBR 15527:2019</b> — Aproveitamento de água de chuva de coberturas para fins não potáveis — Requisitos.</li>
        <li><b>ISO 14040/14044</b> — Gestão Ambiental — Avaliação do Ciclo de Vida — Princípios, estrutura e requisitos.</li>
        <li><b>MCTI/SIRENE</b> — Série oficial de fatores médios de emissão do SIN; selecionar o arquivo correspondente ao período do estudo.</li>
        <li><b>Fatores de materiais/equipamentos</b> — Premissas editáveis de triagem; registrar EPD/inventário, versão, geografia, fronteira e transformação adotados.</li>
        <li><b>Hwang & Yoon (1981)</b> — <i>Multiple Attribute Decision Making</i>; fundamento do TOPSIS.</li>
    </ul>

    <div class='disc-box' style='margin-top: 15px; border-left-color: #0284c7; background-color: #f0f9ff;'>
        <h4>ℹ️ {"Responsabilidade de Verificação das Equações Implementadas" if not is_en else "User Responsibility for Equation Verification"}</h4>
        <p>
            {"O relatório registra as equações e premissas implementadas para permitir auditoria. A equipe do estudo deve confirmar dados locais, fontes, fronteiras, normas e resultados antes da decisão; testes internos não equivalem a validação externa." if not is_en else "The report records implemented equations and assumptions to support audit. The study team must confirm local data, sources, boundaries, standards and results before making a decision; internal tests are not external validation."}
        </p>
    </div>

    <div class='footer-sig'>
        <div>
            <b>Grupo de Pesquisa Gestão do Espaço Sustentável (UFSC)</b><br/>
            {APP_VERSION_LABEL} Engine — {t('prepared')}
        </div>
        <div style='text-align: right;'>
            <br/><br/><br/><br/>
            ___________________________________________________<br/>
            <b>{"Pesquisador(a) / Engenheiro(a) Responsável" if not is_en else "Responsible Researcher / Engineer"}</b><br/>
            CREA / Matrícula Acadêmica / Registro Profissional
        </div>
    </div>
</section>

</main>
</body>
</html>"""
    return _localize_report_markup(html)


def _save_pdf_report_with_webengine(file_path: str, html_content: str) -> bool:
    """Renderiza o CSS completo em Chromium; retorna False para permitir fallback."""
    if os.environ.get("QT_QPA_PLATFORM", "").lower() in {"offscreen", "minimal"}:
        return False
    if os.environ.get("NETUNO_LIGHTWEIGHT_REPORT_PDF") == "1":
        return False

    from pathlib import Path
    from PySide6.QtCore import QEventLoop, QMarginsF, QTimer
    from PySide6.QtGui import QPageLayout, QPageSize
    from PySide6.QtWidgets import QApplication
    from PySide6.QtWebEngineCore import QWebEnginePage, QWebEngineSettings

    if QApplication.instance() is None:
        return False

    page = QWebEnginePage()
    page.settings().setAttribute(QWebEngineSettings.JavascriptEnabled, False)
    page.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessRemoteUrls, False)
    page.settings().setAttribute(QWebEngineSettings.LocalContentCanAccessFileUrls, False)
    is_landscape = "landscape" in html_content.lower()[:2000]
    orientation = QPageLayout.Landscape if is_landscape else QPageLayout.Portrait
    page_layout = QPageLayout(
        QPageSize(QPageSize.A4),
        orientation,
        QMarginsF(5, 5, 5, 5) if is_landscape else QMarginsF(6, 6, 6, 6),
        QPageLayout.Millimeter,
    )
    loop = QEventLoop()
    state = {"ok": False}

    def pdf_ready(pdf_data):
        raw = bytes(pdf_data)
        if raw.startswith(b"%PDF"):
            Path(file_path).write_bytes(raw)
            state["ok"] = True
        loop.quit()

    def html_ready(ok):
        if not ok:
            loop.quit()
            return
        page.printToPdf(pdf_ready, page_layout)

    page.loadFinished.connect(html_ready)
    timeout = QTimer()
    timeout.setSingleShot(True)
    timeout.timeout.connect(loop.quit)
    timeout.start(30000)
    page.setHtml(html_content)
    loop.exec()
    timeout.stop()
    page.deleteLater()
    return bool(state["ok"])


def save_pdf_report(file_path: str, html_content: str):
    """
    Salva o relatório em PDF nativo de altíssima qualidade utilizando PySide6.QtPrintSupport.
    Suporta formato A4 retrato ou A4 paisagem (detectado automaticamente do cabeçalho HTML).
    """
    try:
        if _save_pdf_report_with_webengine(file_path, html_content):
            return
    except Exception:
        # Instalações sem QtWebEngine continuam exportando por QTextDocument.
        pass

    from PySide6.QtGui import QTextDocument, QPageLayout, QPageSize, QFont, QPdfWriter
    from PySide6.QtCore import QMarginsF

    is_landscape = "landscape" in html_content.lower()[:2000]
    orientation = QPageLayout.Landscape if is_landscape else QPageLayout.Portrait

    doc = QTextDocument()
    if get_current_lang() == "zh":
        # Garante que o motor Qt de PDF escolha uma família com glifos CJK.
        doc.setDefaultFont(QFont("Microsoft YaHei", 9))
    doc.setHtml(html_content)

    try:
        writer = QPdfWriter(file_path)
        page_layout = QPageLayout(
            QPageSize(QPageSize.A4),
            orientation,
            QMarginsF(5, 5, 5, 5) if is_landscape else QMarginsF(6, 6, 6, 6),
            QPageLayout.Millimeter
        )
        writer.setPageLayout(page_layout)
        doc.print_(writer)
    except Exception as exc:
        raise RuntimeError(f"Não foi possível gerar o PDF: {exc}") from exc
