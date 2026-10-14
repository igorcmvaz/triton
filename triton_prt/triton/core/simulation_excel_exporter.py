"""
Exportação das simulações em planilha Excel (.xlsx) e CSV (.csv).

Cada aba lê o resultado que o programa calculou: o balanço diário da simulação, a varredura
de volumes, o fluxo de caixa da análise econômica, o inventário da ACV e a decisão
multicritério. Resultado não calculado vira uma linha que diz isso, e nunca um número
estimado. Até outubro de 2026 estas abas esperavam dicionários, recebiam os objetos de
resultado e saíam vazias; o fluxo de caixa era refeito com TMA fixa de 6% e valores padrão
(R$ 7.000 de investimento), a ACV era uma tabela fixa e o multicritério, pontuações
inventadas.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
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


def _v(obj: Any, nome: str, padrao: Any = None) -> Any:
    """Campo de um resultado, seja objeto (dataclass) ou dicionário."""
    if obj is None:
        return padrao
    if isinstance(obj, dict):
        return obj.get(nome, padrao)
    return getattr(obj, nome, padrao)


def _lista(valor: Any) -> list:
    """Uma sequência como lista; None vira lista vazia (vetores do numpy não têm valor-verdade)."""
    return [] if valor is None else list(valor)


def _inicio(project_data: Dict[str, Any]) -> Optional[datetime]:
    texto = str(project_data.get("start_date") or "").strip()
    for formato in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato)
        except ValueError:
            continue
    return None


CABECALHO_DIARIO = [
    "Dia", "Data", "Precipitação (mm)", "Precipitação após descarte (mm)", "Captação (L)",
    "Demanda total (L)", "Demanda não potável (L)", "Consumo pluvial (L)", "Consumo da rede (L)",
    "Extravasamento (L)", "Volume na cisterna ao fim do dia (L)", "Volume na caixa superior (L)",
    "Bombeado (L)", "Atendimento (2 pleno, 1 parcial, 0 nulo)",
]

NAO_CALCULADO = "Não calculado neste estudo: rode a etapa correspondente antes de exportar."


def linhas_do_balanco(single_result: Any, project_data: Dict[str, Any], daily_mode: str = "all") -> List[list]:
    """O balanço diário da simulação, uma linha por dia, como o programa o calculou."""
    dias = _lista(_v(single_result, "daily_results", None)) or _lista(_v(single_result, "history", None))
    if daily_mode == "year1":
        dias = dias[:365]
    inicio = _inicio(project_data)
    linhas = []
    for i, d in enumerate(dias):
        if isinstance(d, (list, tuple)):
            linhas.append([i + 1] + list(d))
            continue
        data = (inicio + timedelta(days=i)).strftime("%d/%m/%Y") if inicio else ""
        linhas.append([
            i + 1, data,
            round(_safe_float(_v(d, "precip_mm")), 2),
            round(_safe_float(_v(d, "eff_precip_mm")), 2),
            round(_safe_float(_v(d, "harvested_liters")), 1),
            round(_safe_float(_v(d, "total_demand_liters")), 1),
            round(_safe_float(_v(d, "pluvial_demand_liters")), 1),
            round(_safe_float(_v(d, "pluvial_consumed_liters")), 1),
            round(_safe_float(_v(d, "potable_consumed_liters")), 1),
            round(_safe_float(_v(d, "spilled_liters")), 1),
            round(_safe_float(_v(d, "lower_tank_end_liters")), 1),
            round(_safe_float(_v(d, "upper_tank_end_liters")), 1),
            round(_safe_float(_v(d, "pumped_liters")), 1),
            _v(d, "satisfaction_type", ""),
        ])
    return linhas


def _tabela(ws, cabecalho: List[str], linhas: List[list], cor: str, borda, zebra, vazio: str) -> None:
    ws.views.sheetView[0].showGridLines = True
    ws.append(cabecalho)
    _style_header_row(ws, 1, bg_color=cor)
    if not linhas:
        ws.append([vazio])
        ws.cell(row=2, column=1).font = Font(name="Segoe UI", size=10, italic=True, color="64748B")
    for r, linha in enumerate(linhas, start=2):
        ws.append(linha)
        for cell in ws[r]:
            cell.border = borda
            cell.font = Font(name="Segoe UI", size=9)
            if r % 2 == 1:
                cell.fill = zebra
    _auto_fit_columns(ws)


def export_simulation_to_excel(
    project_data: Dict[str, Any],
    file_path: str,
    single_result: Any = None,
    sweep_result: Any = None,
    economic_result: Any = None,
    environmental_result: Any = None,
    mcdm_result: Any = None,
    selected_sheets: Optional[Dict[str, bool]] = None,
    horizon_years: int = 20,
    daily_mode: str = "all"
) -> str:
    """Grava a planilha com as abas selecionadas, lidas dos resultados calculados."""
    if selected_sheets is None:
        selected_sheets = dict.fromkeys(("resumo", "balanco", "varredura", "fluxo", "acv", "mcdm"), True)

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    lado = Side(style="thin", color="E2E8F0")
    borda = Border(left=lado, right=lado, top=lado, bottom=lado)
    zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    moeda = str(project_data.get("moeda") or "R$")

    # 1. Resumo
    if selected_sheets.get("resumo", True):
        ws = wb.create_sheet(title="1_Resumo_Projeto")
        ws.merge_cells("A1:D1")
        ws["A1"] = "TRITON 5 — RESUMO DO ESTUDO"
        ws["A1"].font = Font(name="Segoe UI", size=14, bold=True, color="FFFFFF")
        ws["A1"].fill = PatternFill(start_color="064E3B", end_color="064E3B", fill_type="solid")
        ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
        ws.row_dimensions[1].height = 36
        vol = _v(single_result, "lower_tank_vol", project_data.get("lower_vol"))
        pot = _v(single_result, "potential_potable_savings_pct", project_data.get("potential_pct"))
        eco, amb = economic_result, environmental_result
        linhas = [
            ("Projeto", project_data.get("project_name", "—")),
            ("Localidade da chuva", (project_data.get("audit_context") or {}).get("climate_location", "—")),
            ("Emitido em", datetime.now().strftime("%d/%m/%Y %H:%M")),
            ("Volume da cisterna simulado (L)", round(_safe_float(vol), 0) if vol is not None else "—"),
            ("Potencial de economia de água potável (%)", round(_safe_float(pot), 2) if pot is not None else "—"),
            ("Área de captação (m²)", project_data.get("area", "—")),
            ("Coeficiente de escoamento", project_data.get("runoff", "—")),
            ("Descarte inicial (mm)", project_data.get("discard", "—")),
            (f"Investimento ({moeda})",
             round(_safe_float(_v(eco, "total_investment", _v(eco, "capex_total"))), 2) if eco else NAO_CALCULADO),
            (f"VPL ({moeda})", round(_safe_float(_v(eco, "vpl")), 2) if eco else NAO_CALCULADO),
            ("Payback descontado (anos)",
             _v(eco, "payback_discounted_years", _v(eco, "payback_years", "—")) if eco else NAO_CALCULADO),
            ("Saldo de CO₂ na vida útil (kg CO₂e)",
             round(_safe_float(_v(amb, "lifetime_net_co2_saved_kg")), 1) if amb else NAO_CALCULADO),
        ]
        for r, (k, v) in enumerate(linhas, start=3):
            ws.cell(row=r, column=1, value=k).font = Font(name="Segoe UI", size=10, bold=True, color="475569")
            ws.cell(row=r, column=2, value=v).font = Font(name="Segoe UI", size=10, color="0F172A")
        _auto_fit_columns(ws, max_width=60)

    # 2. Balanço diário
    if selected_sheets.get("balanco", True):
        _tabela(wb.create_sheet(title="2_Balanco_Hidrico_Diario"), CABECALHO_DIARIO,
                linhas_do_balanco(single_result, project_data, daily_mode), "087F6B", borda, zebra, NAO_CALCULADO)

    # 3. Varredura de volumes
    if selected_sheets.get("varredura", True):
        linhas = [[
            round(_safe_float(_v(r, "lower_tank_vol")), 0),
            round(_safe_float(_v(r, "potential_potable_savings_pct")), 2),
            round(_safe_float(_v(r, "avg_pluvial_consumed_l_day")) * 365.25 / 1000.0, 2),
            round(_safe_float(_v(r, "avg_spilled_l_day")) * 365.25 / 1000.0, 2),
            round(_safe_float(_v(r, "pct_days_full_satisfaction")), 2),
            round(_safe_float(_v(r, "pct_days_null_satisfaction")), 2),
            round(_safe_float(_v(r, "delta_potential_per_m3")), 4),
        ] for r in _lista(_v(sweep_result, "results_by_volume", None))]
        _tabela(wb.create_sheet(title="3_Curva_Varredura_Volumes"),
                ["Volume da cisterna (L)", "Economia de água potável (%)", "Consumo pluvial (m³/ano)",
                 "Extravasamento (m³/ano)", "Atendimento pleno (% dos dias)", "Atendimento nulo (% dos dias)",
                 "Ganho marginal (% por m³)"],
                linhas, "0284C7", borda, zebra,
                "Sem varredura: o estudo foi simulado num volume fixo." if single_result is not None else NAO_CALCULADO)

    # 4. Fluxo de caixa
    mensais = _lista(_v(economic_result, "monthly_cash_flows", None))
    if selected_sheets.get("fluxo", True) and mensais and not _lista(_v(economic_result, "annual_cash_flows", None)):
        # Análise mensal (run_economic_analysis): o fluxo mês a mês, como foi calculado.
        linhas = [[
            int(_safe_float(_v(m, "year"))), int(_safe_float(_v(m, "month"))),
            round(_safe_float(_v(m, "water_bill_without_pluvial")), 2),
            round(_safe_float(_v(m, "water_bill_with_pluvial")), 2),
            round(_safe_float(_v(m, "water_savings")), 2),
            round(_safe_float(_v(m, "pump_energy_kwh")), 3),
            round(_safe_float(_v(m, "pump_cost")), 2), round(_safe_float(_v(m, "om_cost")), 2),
            round(_safe_float(_v(m, "chlorine_cost")), 2), round(_safe_float(_v(m, "iptu_savings")), 2),
            round(_safe_float(_v(m, "net_savings")), 2), round(_safe_float(_v(m, "discounted_net_savings")), 2),
            round(_safe_float(_v(m, "cumulative_discounted")), 2),
        ] for m in mensais if int(_safe_float(_v(m, "year"))) <= int(horizon_years)]
        _tabela(wb.create_sheet(title="4_Fluxo_Caixa_Economico"),
                ["Ano", "Mês", f"Conta sem aproveitamento ({moeda})", f"Conta com aproveitamento ({moeda})",
                 f"Economia na conta ({moeda})", "Energia de bombeamento (kWh)", f"Energia ({moeda})",
                 f"Operação e manutenção ({moeda})", f"Cloração ({moeda})", f"Desconto de IPTU ({moeda})",
                 f"Economia líquida ({moeda})", f"Economia descontada ({moeda})", f"Acumulado descontado ({moeda})"],
                linhas, "D97706", borda, zebra, NAO_CALCULADO)
    elif selected_sheets.get("fluxo", True):
        linhas = [[
            int(_safe_float(_v(f, "year"))),
            round(_safe_float(_v(f, "initial_investment")), 2),
            round(_safe_float(_v(f, "water_saved_m3")), 2),
            round(_safe_float(_v(f, "gross_water_savings_brl")), 2),
            round(_safe_float(_v(f, "gross_sewage_savings_brl")), 2),
            round(_safe_float(_v(f, "iptu_green_savings_brl")), 2),
            round(_safe_float(_v(f, "pump_energy_cost_brl")), 2),
            round(_safe_float(_v(f, "om_cost_brl")), 2),
            round(_safe_float(_v(f, "chlorine_cost_brl")), 2),
            round(_safe_float(_v(f, "net_cash_flow_nominal_brl")), 2),
            round(_safe_float(_v(f, "discounted_cash_flow_brl")), 2),
            round(_safe_float(_v(f, "cumulative_discounted_cash_flow_brl")), 2),
        ] for f in _lista(_v(economic_result, "annual_cash_flows", None))
            if int(_safe_float(_v(f, "year"))) <= int(horizon_years)]
        _tabela(wb.create_sheet(title="4_Fluxo_Caixa_Economico"),
                ["Ano", f"Investimento ({moeda})", "Água economizada (m³)", f"Economia de água ({moeda})",
                 f"Economia de esgoto ({moeda})", f"Desconto de IPTU ({moeda})", f"Energia de bombeamento ({moeda})",
                 f"Operação e manutenção ({moeda})", f"Cloração ({moeda})", f"Fluxo líquido nominal ({moeda})",
                 f"Fluxo descontado ({moeda})", f"Fluxo descontado acumulado ({moeda})"],
                linhas, "D97706", borda, zebra, NAO_CALCULADO)

    # 5. ACV
    if selected_sheets.get("acv", True):
        linhas = [[
            _v(it, "category", ""), _v(it, "quantity_str", ""),
            round(_safe_float(_v(it, "embodied_co2_kg")), 3),
            round(_safe_float(_v(it, "annual_op_co2_kg")), 3),
            round(_safe_float(_v(it, "lifetime_net_co2_kg")), 3),
            _v(it, "source_reference", ""),
        ] for it in _lista(_v(environmental_result, "inventory_items", None))]
        _tabela(wb.create_sheet(title="5_Inventario_ACV_ESG"),
                ["Componente / fase", "Quantidade", "Emissão incorporada (kg CO₂e)", "Operação anual (kg CO₂e/ano)",
                 "Saldo na vida útil (kg CO₂e)", "Fonte"],
                linhas, "059669", borda, zebra, NAO_CALCULADO)

    # 6. Multicritério
    if selected_sheets.get("mcdm", True):
        candidatos = _lista(_v(mcdm_result, "candidates", None))
        pontos = _lista(_v(mcdm_result, "scores", None))
        ordem = _lista(_v(mcdm_result, "rankings", None))
        linhas = [[
            round(_safe_float(_v(c, "lower_tank_vol")), 0),
            round(_safe_float(_v(c, "potential_savings_pct")), 2),
            round(_safe_float(_v(c, "capex_brl")), 2),
            round(_safe_float(_v(c, "vpl_brl")), 2),
            _v(c, "discounted_payback_years", ""),
            round(_safe_float(_v(c, "co2_saved_kg_lifetime")), 1),
            round(_safe_float(pontos[i]), 4) if i < len(pontos) else "",
            ordem[i] if i < len(ordem) else "",
        ] for i, c in enumerate(candidatos)]
        _tabela(wb.create_sheet(title="6_Decisao_Multicriterio"),
                ["Volume (L)", "Economia (%)", f"Investimento ({moeda})", f"VPL ({moeda})",
                 "Payback descontado (anos)", "Saldo de CO₂ (kg CO₂e)", "Pontuação", "Posição"],
                linhas, "7C3AED", borda, zebra, NAO_CALCULADO)

    if not wb.sheetnames:
        wb.create_sheet(title="Sem_Dados")["A1"] = "Nenhuma aba selecionada para exportação."
    wb.save(file_path)
    return file_path


def export_simulation_to_csv(
    project_data: Dict[str, Any],
    file_path: str,
    single_result: Any = None,
    delimiter: str = ";",
    mode: str = "daily"
) -> str:
    """O balanço hídrico diário em CSV, com o delimitador escolhido."""
    with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(CABECALHO_DIARIO)
        for linha in linhas_do_balanco(single_result, project_data, "year1" if mode == "year1" else "all"):
            writer.writerow(linha)
    return file_path
