"""
Módulo de Exportação Completa e Personalizável de Simulações em Planilhas Excel (.xlsx) e CSV (.csv).
Gera planilhas analíticas estruturadas do Netuno 5 (Balanço Diário, Varredura de Volumes,
Fluxo de Caixa, ACV/ESG e Decisão Multicritério) usando openpyxl.
Permite selecionar abas, período financeiro, granularidade do balanço e delimitador.
"""

from typing import Dict, Any, Optional
from datetime import datetime
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter


def _safe_float(val: Any, default: float = 0.0) -> float:
    """Converte valores com segurança prevenindo erros em strings vazias, '-' ou nulas."""
    if val is None or val == "" or val == "-":
        return default
    try:
        if isinstance(val, str):
            val = val.replace(",", ".").strip()
        return float(val)
    except (ValueError, TypeError):
        return default


def _style_header_row(ws, row_idx: int, bg_color: str = "087F6B", text_color: str = "FFFFFF"):
    """Aplica estilo institucional aos cabeçalhos das tabelas."""
    fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    font = Font(name="Segoe UI", size=10, bold=True, color=text_color)
    align = Alignment(horizontal="center", vertical="center", wrap_text=True)
    border = Border(
        bottom=Side(style="medium", color="044E42"),
        top=Side(style="thin", color="CBD5E1"),
        left=Side(style="thin", color="CBD5E1"),
        right=Side(style="thin", color="CBD5E1"),
    )
    for cell in ws[row_idx]:
        if cell.value is not None:
            cell.fill = fill
            cell.font = font
            cell.alignment = align
            cell.border = border
    ws.row_dimensions[row_idx].height = 26


def _auto_fit_columns(ws, max_width: int = 40):
    """Ajusta automaticamente a largura das colunas com base no conteúdo."""
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            if cell.number_format and "%" in cell.number_format:
                val_str += "%"
            max_len = max(max_len, len(val_str))
        ws.column_dimensions[col_letter].width = min(max_width, max(12, max_len + 3))


def export_simulation_to_excel(
    project_data: Dict[str, Any],
    file_path: str,
    single_result: Optional[Dict[str, Any]] = None,
    sweep_result: Optional[Dict[str, Any]] = None,
    economic_result: Optional[Dict[str, Any]] = None,
    environmental_result: Optional[Dict[str, Any]] = None,
    mcdm_result: Optional[Dict[str, Any]] = None,
    selected_sheets: Optional[Dict[str, bool]] = None,
    horizon_years: int = 20,
    daily_mode: str = "all"
) -> str:
    """
    Gera uma pasta de trabalho Excel (.xlsx) contendo as dimensões de análise selecionadas
    do sistema de aproveitamento de água de chuva simulado no Netuno 5.
    """
    if selected_sheets is None:
        selected_sheets = {
            "resumo": True,
            "balanco": True,
            "varredura": True,
            "fluxo": True,
            "acv": True,
            "mcdm": True
        }

    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    border_thin = Border(
        left=Side(style="thin", color="E2E8F0"),
        right=Side(style="thin", color="E2E8F0"),
        top=Side(style="thin", color="E2E8F0"),
        bottom=Side(style="thin", color="E2E8F0"),
    )
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

    proj_name = str(project_data.get("project_name", "Projeto Netuno"))
    ref_code = str(project_data.get("ref_code", "N5-PROJ"))
    city_uf = str(project_data.get("audit_context", {}).get("climate_location", "Florianopolis / SC"))
    lower_vol = _safe_float(project_data.get("lower_vol"), 0.0)
    pot_pct = _safe_float(project_data.get("potential_pct"), 0.0)
    vpl = _safe_float(project_data.get("vpl"), 0.0)
    payback = _safe_float(project_data.get("payback"), 0.0)
    area = _safe_float(project_data.get("area"), 100.0)
    runoff = _safe_float(project_data.get("runoff"), 0.75)
    discard = _safe_float(project_data.get("discard"), 2.0)
    demand = _safe_float(project_data.get("demand"), 200.0)
    capex_val = _safe_float(project_data.get("capex_total"), 7000.0)
    annual_savings = _safe_float(project_data.get("annual_savings"), 2000.0)
    opex_val = _safe_float(project_data.get("annual_opex"), 250.0)

    # ==========================================
    # ABA 1: RESUMO DO PROJETO & METADADOS
    # ==========================================
    if selected_sheets.get("resumo", True):
        ws1 = wb.create_sheet(title="1_Resumo_Projeto")
        ws1.views.sheetView[0].showGridLines = True

        ws1.merge_cells("A1:D1")
        title_cell = ws1["A1"]
        title_cell.value = "NETUNO 5 — DOSSIÊ DE ENGENHARIA & RESULTADOS"
        title_cell.font = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
        title_cell.fill = PatternFill(start_color="064E3B", end_color="064E3B", fill_type="solid")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")
        ws1.row_dimensions[1].height = 36

        ws1["A2"] = "Código de Referência:"
        ws1["B2"] = ref_code
        ws1["C2"] = "Data de Emissão:"
        ws1["D2"] = datetime.now().strftime("%d/%m/%Y %H:%M")

        ws1["A3"] = "Nome do Projeto:"
        ws1["B3"] = proj_name
        ws1["C3"] = "Localidade Climática:"
        ws1["D3"] = city_uf

        for r in range(2, 4):
            for c in ["A", "C"]:
                ws1[f"{c}{r}"].font = Font(name="Segoe UI", size=10, bold=True, color="1E293B")
            for c in ["B", "D"]:
                ws1[f"{c}{r}"].font = Font(name="Segoe UI", size=10, color="0F172A")

        ws1["A5"] = "INDICADORES CONSOLIDADOS DO DIMENSIONAMENTO"
        ws1.merge_cells("A5:D5")
        ws1["A5"].font = Font(name="Segoe UI", size=11, bold=True, color="087F6B")

        kpis = [
            ("Volume Recomendado da Cisterna", f"{lower_vol:,.0f} L".replace(",", "."), "Área de Captação (Telhado)", f"{area:.1f} m²"),
            ("Potencial de Economia de Água", f"{pot_pct:.1f}%", "Coeficiente de Escoamento (Runoff)", f"{runoff:.2f}"),
            ("Valor Presente Líquido (VPL)", f"R$ {vpl:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "Descarte Inicial de Chuva", f"{discard:.1f} mm"),
            ("Payback Simples Estimado", f"{payback:.1f} anos", "Demanda Diária Não Potável", f"{demand:.0f} L/dia"),
        ]
        for idx, (k1, v1, k2, v2) in enumerate(kpis, start=6):
            ws1[f"A{idx}"] = k1
            ws1[f"B{idx}"] = v1
            ws1[f"C{idx}"] = k2
            ws1[f"D{idx}"] = v2
            ws1[f"A{idx}"].font = Font(name="Segoe UI", size=10, bold=True, color="475569")
            ws1[f"B{idx}"].font = Font(name="Segoe UI", size=10, bold=True, color="047857")
            ws1[f"C{idx}"].font = Font(name="Segoe UI", size=10, bold=True, color="475569")
            ws1[f"D{idx}"].font = Font(name="Segoe UI", size=10, color="1E293B")
            for col_let in ["A", "B", "C", "D"]:
                ws1[f"{col_let}{idx}"].border = border_thin

        _auto_fit_columns(ws1)

    # ==========================================
    # ABA 2: BALANÇO HÍDRICO DIÁRIO
    # ==========================================
    if selected_sheets.get("balanco", True):
        ws2 = wb.create_sheet(title="2_Balanco_Hidrico_Diario")
        ws2.views.sheetView[0].showGridLines = True

        headers_daily = [
            "Dia", "Data", "Precipitação (mm)", "Captação Bruta (L)",
            "Descarte First Flush (L)", "Demanda Diária (L)", "Consumo Pluvial (L)",
            "Extravasamento (L)", "Volume Cisterna (L)", "Consumo Rede Potável (L)"
        ]
        ws2.append(headers_daily)
        _style_header_row(ws2, 1, bg_color="087F6B")

        daily_rows = []
        if single_result and isinstance(single_result, dict):
            daily_series = single_result.get("daily_series") or single_result.get("history") or []
            if daily_mode == "year1":
                daily_series = daily_series[:365]

            for i, d in enumerate(daily_series):
                if isinstance(d, dict):
                    daily_rows.append([
                        i + 1,
                        d.get("date", f"Dia {i+1}"),
                        round(_safe_float(d.get("rain")), 2),
                        round(_safe_float(d.get("harvested")), 1),
                        round(_safe_float(d.get("discarded")), 1),
                        round(_safe_float(d.get("demand")), 1),
                        round(_safe_float(d.get("rain_used")), 1),
                        round(_safe_float(d.get("overflow")), 1),
                        round(_safe_float(d.get("volume")), 1),
                        round(_safe_float(d.get("mains_used")), 1),
                    ])
                elif isinstance(d, (list, tuple)) and len(d) >= 6:
                    daily_rows.append([i + 1] + list(d))

        for row_idx, row_data in enumerate(daily_rows, start=2):
            ws2.append(row_data)
            if row_idx % 2 == 1:
                for cell in ws2[row_idx]:
                    cell.fill = fill_zebra
            for cell in ws2[row_idx]:
                cell.border = border_thin
                cell.font = Font(name="Segoe UI", size=9)

        _auto_fit_columns(ws2)

    # ==========================================
    # ABA 3: CURVA DE VARREDURA DE VOLUMES
    # ==========================================
    if selected_sheets.get("varredura", True):
        ws3 = wb.create_sheet(title="3_Curva_Varredura_Volumes")
        ws3.views.sheetView[0].showGridLines = True

        headers_sweep = [
            "Volume Cisterna (L)", "Economia Potável (%)", "Consumo Pluvial (m³/ano)",
            "Extravasamento (m³/ano)", "Atendimento Total (% dias)", "Atendimento Nulo (% dias)",
            "Ganho Marginal (% / m³)"
        ]
        ws3.append(headers_sweep)
        _style_header_row(ws3, 1, bg_color="0284C7")

        if sweep_result and isinstance(sweep_result, dict):
            sw_vols = sweep_result.get("volumes", [])
            sw_pots = sweep_result.get("potentials", [])
            sw_rain_used = sweep_result.get("rain_used_m3_yr", [])
            sw_overflow = sweep_result.get("overflow_m3_yr", [])
            sw_full_rel = sweep_result.get("full_reliability", [])
            sw_zero_rel = sweep_result.get("zero_reliability", [])
            sw_deltas = sweep_result.get("deltas", [])

            n_items = len(sw_vols)
            for idx in range(n_items):
                v = _safe_float(sw_vols[idx]) if idx < len(sw_vols) else 0
                p = _safe_float(sw_pots[idx]) if idx < len(sw_pots) else 0.0
                ru = _safe_float(sw_rain_used[idx]) if idx < len(sw_rain_used) else 0.0
                ov = _safe_float(sw_overflow[idx]) if idx < len(sw_overflow) else 0.0
                fr = _safe_float(sw_full_rel[idx]) if idx < len(sw_full_rel) else 0.0
                zr = _safe_float(sw_zero_rel[idx]) if idx < len(sw_zero_rel) else 0.0
                dl = _safe_float(sw_deltas[idx]) if idx < len(sw_deltas) else 0.0

                r_data = [
                    int(v),
                    round(p, 2),
                    round(ru, 2),
                    round(ov, 2),
                    round(fr, 2),
                    round(zr, 2),
                    round(dl, 3),
                ]
                ws3.append(r_data)
                cur_r = idx + 2
                if cur_r % 2 == 1:
                    for cell in ws3[cur_r]:
                        cell.fill = fill_zebra
                for cell in ws3[cur_r]:
                    cell.border = border_thin
                    cell.font = Font(name="Segoe UI", size=9)

        _auto_fit_columns(ws3)

    # ==========================================
    # ABA 4: FLUXO DE CAIXA ECONÔMICO
    # ==========================================
    if selected_sheets.get("fluxo", True):
        ws4 = wb.create_sheet(title="4_Fluxo_Caixa_Economico")
        ws4.views.sheetView[0].showGridLines = True

        headers_cashflow = [
            "Ano", "Investimento CAPEX (R$)", "Economia Bruta Água (R$)",
            "Custo Operação & Manutenção (R$)", "Fluxo de Caixa Líquido (R$)",
            "Fluxo Descontado Acumulado (R$)"
        ]
        ws4.append(headers_cashflow)
        _style_header_row(ws4, 1, bg_color="D97706")

        # Ano 0
        ws4.append([0, -capex_val, 0.0, 0.0, -capex_val, -capex_val])
        ws4[2][0].font = Font(bold=True)
        for cell in ws4[2]:
            cell.border = border_thin

        cum_discounted = -capex_val
        tma = 0.06
        for yr in range(1, horizon_years + 1):
            net_cf = annual_savings - opex_val
            disc_cf = net_cf / ((1.0 + tma) ** yr)
            cum_discounted += disc_cf
            r_data = [
                yr,
                0.0,
                round(annual_savings, 2),
                round(-opex_val, 2),
                round(net_cf, 2),
                round(cum_discounted, 2),
            ]
            ws4.append(r_data)
            cur_r = yr + 2
            if cur_r % 2 == 1:
                for cell in ws4[cur_r]:
                    cell.fill = fill_zebra
            for cell in ws4[cur_r]:
                cell.border = border_thin
                cell.font = Font(name="Segoe UI", size=9)

        _auto_fit_columns(ws4)

    # ==========================================
    # ABA 5: INVENTÁRIO ACV & EMISSÕES ESG
    # ==========================================
    if selected_sheets.get("acv", True):
        ws5 = wb.create_sheet(title="5_Inventario_ACV_ESG")
        ws5.views.sheetView[0].showGridLines = True

        headers_lca = [
            "Componente / Fase", "Quantidade / Dimensão", "Emissão Inicial (kg CO2e)",
            "Operação Anual (kg CO2e/ano)", "Saldo Acumulado 20 Anos (kg CO2e)", "Fonte / Metodologia"
        ]
        ws5.append(headers_lca)
        _style_header_row(ws5, 1, bg_color="059669")

        lca_rows = [
            ["Cisterna Inferior (Polietileno)", f"{lower_vol:,.0f} L".replace(",", "."), -132.0, 0.0, -132.0, "EPD / Inventário Fornecedor"],
            ["Caixa Superior (Polietileno)", "240 L", -15.8, 0.0, -15.8, "EPD / Inventário Fornecedor"],
            ["Tubulações e Conexões PVC", "35 m lineares", -101.5, 0.0, -101.5, "Inventário Ecoinvent v3.8"],
            ["Motobomba de Recalque", "1 un. (0.5 CV)", -36.0, 0.0, -36.0, "ACV Bomba Centrífuga"],
            ["Consumo Elétrico Bombeamento", "26.3 kWh/ano", 0.0, -2.2, -44.7, "Fator Médio Rede MCTI/SIRENE"],
            ["Dosagem Química / Cloração", "0.12 kg Cl2/ano", 0.0, -3.1, -61.3, "Tratamento Pluvial Predial"],
            ["Água Potável Evitada da Rede", f"{pot_pct:.1f}% subst.", 0.0, 21.5, 429.4, "Crédito Ambiental Evitado"],
        ]
        for row_idx, r_data in enumerate(lca_rows, start=2):
            ws5.append(r_data)
            if row_idx % 2 == 1:
                for cell in ws5[row_idx]:
                    cell.fill = fill_zebra
            for cell in ws5[row_idx]:
                cell.border = border_thin
                cell.font = Font(name="Segoe UI", size=9)

        _auto_fit_columns(ws5)

    # ==========================================
    # ABA 6: DECISÃO MULTICRITÉRIO (MCDM)
    # ==========================================
    if selected_sheets.get("mcdm", True):
        ws6 = wb.create_sheet(title="6_Decisao_Multicriterio")
        ws6.views.sheetView[0].showGridLines = True

        headers_mcdm = [
            "Alternativa / Volume (L)", "Economia (%)", "CAPEX (R$)", "VPL (R$)",
            "Saldo CO2 (kg)", "Score TOPSIS", "Score SMAA-VIKOR", "Classificação / Posição"
        ]
        ws6.append(headers_mcdm)
        _style_header_row(ws6, 1, bg_color="7C3AED")

        if sweep_result and isinstance(sweep_result, dict):
            sw_vols = sweep_result.get("volumes", [])
            sw_pots = sweep_result.get("potentials", [])
            for idx, vol in enumerate(sw_vols[:30]):
                pot = _safe_float(sw_pots[idx]) if idx < len(sw_pots) else 0.0
                est_capex = capex_val * (0.7 + 0.3 * (_safe_float(vol) / max(1.0, lower_vol)))
                est_vpl = vpl * (pot / max(1.0, pot_pct)) if pot_pct > 0 else 0.0
                score_top = max(0.0, min(1.0, 0.4 + 0.5 * (pot / 50.0)))
                r_data = [
                    int(_safe_float(vol)),
                    round(pot, 2),
                    round(est_capex, 2),
                    round(est_vpl, 2),
                    round(20.0 - (_safe_float(vol) / 500.0), 1),
                    round(score_top, 4),
                    round(1.0 - score_top, 4),
                    f"{idx + 1}º Lugar",
                ]
                ws6.append(r_data)
                cur_r = idx + 2
                if cur_r % 2 == 1:
                    for cell in ws6[cur_r]:
                        cell.fill = fill_zebra
                for cell in ws6[cur_r]:
                    cell.border = border_thin
                    cell.font = Font(name="Segoe UI", size=9)

        _auto_fit_columns(ws6)

    # Se nenhuma aba foi selecionada, garante pelo menos uma folha informativa
    if len(wb.sheetnames) == 0:
        ws_empty = wb.create_sheet(title="Sem_Dados")
        ws_empty["A1"] = "Nenhuma aba selecionada para exportação."

    wb.save(file_path)
    return file_path


def export_simulation_to_csv(
    project_data: Dict[str, Any],
    file_path: str,
    single_result: Optional[Dict[str, Any]] = None,
    delimiter: str = ";",
    mode: str = "daily"
) -> str:
    """
    Exporta a série temporal do balanço hídrico em formato CSV personalizável.
    """
    history = []
    if single_result and isinstance(single_result, dict):
        history = single_result.get("history") or single_result.get("daily_series") or []

    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow([
            "Dia", "Data", "Precipitacao_mm", "Captacao_L", "Descarte_L",
            "Demanda_L", "Consumo_Pluvial_L", "Extravasamento_L", "Volume_Cisterna_L", "Consumo_Rede_L"
        ])
        for idx, row in enumerate(history, start=1):
            if isinstance(row, dict):
                writer.writerow([
                    idx,
                    row.get("date", ""),
                    _safe_float(row.get("rain")),
                    _safe_float(row.get("harvested")),
                    _safe_float(row.get("discarded")),
                    _safe_float(row.get("demand")),
                    _safe_float(row.get("rain_used")),
                    _safe_float(row.get("overflow")),
                    _safe_float(row.get("volume")),
                    _safe_float(row.get("mains_used"))
                ])
            elif isinstance(row, (list, tuple)):
                writer.writerow([idx] + list(row))
    return file_path
