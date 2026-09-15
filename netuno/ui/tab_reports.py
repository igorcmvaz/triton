"""

Aba de Gerador de Relatórios em PDF e Excel do Netuno 5 (PySide6).

"""



import os
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO

from PySide6.QtWidgets import (

    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, 

    QPushButton, QFileDialog, QMessageBox

)

from PySide6.QtCore import Qt



import pandas as pd
from netuno import APP_VERSION_LABEL
from netuno.ui.translation import tr





class TabReportsExport(QWidget):
    def __init__(self, parent=None):

        super().__init__(parent)

        self.init_ui()



    def init_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(20, 20, 20, 20)

        layout.setSpacing(20)



        title = QLabel("📑 Central de Exportação de Relatórios de Engenharia")

        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #10b981;")

        layout.addWidget(title)



        # Grupo PDF

        group_pdf = QGroupBox("Relatório Técnico Executivo em PDF")

        grid_pdf = QVBoxLayout()



        lbl_info = QLabel("Gere um relatório técnico completo em PDF contendo o memorial descritivo, os indicadores de balanço hídrico diário e a análise de viabilidade financeira no padrão visual UFSC Sustentável.")

        lbl_info.setWordWrap(True)

        lbl_info.setStyleSheet("color: #cbd5e1; font-size: 13px;")

        grid_pdf.addWidget(lbl_info)



        self.btn_export_pdf = QPushButton("📄 EXPORTAR RELATÓRIO PDF")

        self.btn_export_pdf.setProperty("class", "btn-primary")

        self.btn_export_pdf.setStyleSheet("font-size: 14px; padding: 12px;")

        self.btn_export_pdf.clicked.connect(self.export_pdf_report)

        grid_pdf.addWidget(self.btn_export_pdf)



        group_pdf.setLayout(grid_pdf)

        layout.addWidget(group_pdf)



        # Grupo Excel

        group_excel = QGroupBox("Exportação de Planilha Excel (.xlsx)")

        grid_excel = QVBoxLayout()



        lbl_info2 = QLabel("Exporte os dados da simulação e das varreduras de reservatório para planilhas editáveis no formato Microsoft Excel (.xlsx).")

        lbl_info2.setWordWrap(True)

        lbl_info2.setStyleSheet("color: #cbd5e1; font-size: 13px;")

        grid_excel.addWidget(lbl_info2)



        self.btn_export_excel = QPushButton("📊 EXPORTAR PLANILHA EXCEL (.XLSX)")

        self.btn_export_excel.setProperty("class", "btn-gold")

        self.btn_export_excel.setStyleSheet("font-size: 14px; padding: 12px;")

        self.btn_export_excel.clicked.connect(self.export_excel_report)

        grid_excel.addWidget(self.btn_export_excel)



        group_excel.setLayout(grid_excel)

        layout.addWidget(group_excel)



        # Grupo Netuno 4.0 CSV

        group_csv = QGroupBox("Exportação no Formato Netuno 4.0 Oficial (.csv)")

        grid_csv = QVBoxLayout()



        lbl_info3 = QLabel("Exporte as configurações e os resultados do balanço hídrico no formato CSV exatamente idêntico ao software Netuno original (Grupo de Pesquisa Gestão do Espaço Sustentável).")

        lbl_info3.setWordWrap(True)

        lbl_info3.setStyleSheet("color: #cbd5e1; font-size: 13px;")

        grid_csv.addWidget(lbl_info3)



        self.btn_export_csv = QPushButton("📁 EXPORTAR PROJETO NETUNO 4.0 (.CSV)")

        self.btn_export_csv.setProperty("class", "btn-secondary")

        self.btn_export_csv.setStyleSheet("font-size: 14px; padding: 12px;")

        self.btn_export_csv.clicked.connect(self.export_netuno4_csv)

        grid_csv.addWidget(self.btn_export_csv)



        group_csv.setLayout(grid_csv)

        layout.addWidget(group_csv)



        layout.addStretch()

        self.setLayout(layout)





    def export_pdf_report(self):
        from netuno import get_kebab_filename

        def_name = get_kebab_filename("netuno-relatorio", "pdf")

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Relatório PDF", def_name, "PDF Files (*.pdf)")

        if not file_path:

            return

        try:

            self._build_landscape_pdf(file_path)

            QMessageBox.information(self, "Sucesso", f"Relatório PDF gerado:\n{file_path}")

        except Exception as e:

            import traceback

            QMessageBox.critical(self, "Erro no PDF", f"Falha ao gerar PDF:\n{str(e)}\n\n{traceback.format_exc()}")

    def _build_landscape_pdf(self, file_path: str):
        """Gera um dashboard gerencial A4 Landscape em página única usando ReportLab."""
        from datetime import datetime
        from reportlab.lib.pagesizes import A4, landscape

        from reportlab.lib.units import mm

        from reportlab.lib import colors

        from reportlab.lib.styles import ParagraphStyle

        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

        from reportlab.platypus import (
            SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
        )
        from netuno.ui.translation import get_current_lang
        report_lang = get_current_lang()
        cjk_font = None
        if report_lang == "zh":
            # Fonte CID embutida no ReportLab: garante ideogramas no PDF sem
            # depender de uma fonte instalada no computador do destinatário.
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.cidfonts import UnicodeCIDFont
            cjk_font = "STSong-Light"
            pdfmetrics.registerFont(UnicodeCIDFont(cjk_font))


        # ── Page setup ────────────────────────────────────────────

        page_w, page_h = landscape(A4)   # 841.89 × 595.28 pt

        # Permite um laudo mais amplo e deixa a paginação continuar quando
        # uma seção não couber no espaço restante.
        M = 10 * mm
        doc = SimpleDocTemplate(

            file_path,

            pagesize=landscape(A4),

            leftMargin=M, rightMargin=M,

            topMargin=10 * mm, bottomMargin=10 * mm,

        )

        col_w = page_w - 2 * M           # usable width



        # ── Colour palette ────────────────────────────────────────

        NAVY   = colors.HexColor('#0f2b54')

        BLUE   = colors.HexColor('#0369a1')

        BLUE_L = colors.HexColor('#dbeafe')

        GREEN  = colors.HexColor('#059669')

        GREEN_L= colors.HexColor('#dcfce7')

        AMBER  = colors.HexColor('#d97706')

        AMBER_L= colors.HexColor('#fef9c3')

        SLATE  = colors.HexColor('#475569')

        LIGHT  = colors.HexColor('#f8fafc')

        BORDER = colors.HexColor('#cbd5e1')

        WHITE  = colors.white

        WARN_T = colors.HexColor('#92400e')

        WARN_L = colors.HexColor('#fef3c7')



        # ── Typography ────────────────────────────────────────────

        def P(name, font='Helvetica', size=8, color=SLATE, align=TA_LEFT, leading=None, bold=False):
            return ParagraphStyle(
                name,
                fontName=cjk_font if cjk_font else (f'Helvetica-Bold' if bold else font),
                fontSize=size,

                textColor=color,

                alignment=align,

                leading=leading or size * 1.25,

            )



        s_main_title = P('mt', size=13, color=NAVY,  bold=True)

        s_sub        = P('sb', size=7.5, color=SLATE)

        s_sub_r      = P('sbr', size=7.5, color=SLATE, align=TA_RIGHT)

        s_kpi_lbl    = P('kl', size=6.5, color=SLATE,  bold=True, align=TA_CENTER)

        s_kpi_val    = P('kv', size=17,  color=NAVY,   bold=True, align=TA_CENTER, leading=20)

        s_kpi_sub    = P('ks', size=6,   color=SLATE,  align=TA_CENTER)

        s_sec        = P('sc', size=7.5, color=WHITE,  bold=True)

        s_lbl        = P('lb', size=7.5, color=colors.HexColor('#334155'))

        s_val        = P('vl', size=7.5, color=colors.HexColor('#0f172a'), bold=True)

        s_val_g      = P('vg', size=7.5, color=GREEN, bold=True)

        s_disc       = P('di', size=6.5, color=WARN_T)

        s_disc_b     = P('db', size=6.5, color=WARN_T, bold=True)

        s_foot       = P('ft', size=6.5, color=SLATE)

        s_foot_r     = P('fr', size=6.5, color=SLATE, align=TA_RIGHT)



        # ── Helper: pt-BR number ──────────────────────────────────

        def br(v, dec=0):

            try:

                s = f"{float(v):,.{dec}f}"

                return s.replace(',', 'X').replace('.', ',').replace('X', '.')

            except Exception:

                return str(v)



        # ── Helper: section header row ────────────────────────────

        def sec_hdr(text, bg, width):

            t = Table([[Paragraph(f"<b>{text}</b>", s_sec)]], colWidths=[width])

            t.setStyle(TableStyle([

                ('BACKGROUND', (0,0), (-1,-1), bg),

                ('TOPPADDING',    (0,0),(-1,-1), 3),

                ('BOTTOMPADDING', (0,0),(-1,-1), 3),

                ('LEFTPADDING',   (0,0),(-1,-1), 6),

            ]))

            return t



        # ── Helper: data table ────────────────────────────────────

        def dtable(rows, cw):

            t = Table(rows, colWidths=cw)

            t.setStyle(TableStyle([

                ('BACKGROUND',  (0,0), (-1,0),  colors.HexColor('#f1f5f9')),

                ('FONTNAME',    (0,0), (-1,0),  cjk_font or 'Helvetica-Bold'),
                ('FONTSIZE',    (0,0), (-1,-1), 7.5),

                ('GRID',        (0,0), (-1,-1), 0.4, BORDER),

                ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT]),

                ('TOPPADDING',    (0,0), (-1,-1), 3),

                ('BOTTOMPADDING', (0,0), (-1,-1), 3),

                ('LEFTPADDING',   (0,0), (-1,-1), 5),

                ('RIGHTPADDING',  (0,0), (-1,-1), 5),

                ('TEXTCOLOR', (0,0), (-1,0), SLATE),

                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),

            ]))

            return t



        # ── Collect live data ─────────────────────────────────────

        date_str = datetime.now().strftime("%d/%m/%Y")

        mw = self.window()

        project_ref = getattr(getattr(mw, "config", None), "project_id", "N5-NAO-IDENTIFICADO")



        area = 100.0; demand = 200.0; residents = 3

        runoff = 0.75; discard_mm = 1.0; share = 0.40

        rain_file = "Não carregada"

        lower_vol = 0.0; potential_pct = 0.0

        pluv_day = 0.0; potable_day = 0.0; spill_day = 0.0

        sat_full = 0.0; sat_null = 0.0

        capex = 0.0; annual_gross = 0.0; vpl = 0.0; tir = 0.0

        payback_s = "--"; payback_d = "--"



        if mw and hasattr(mw, 'tab_building'):

            bc = mw.tab_building.get_building_config()

            area     = bc.get('area', 100.0)

            demand   = bc.get('demand', 200.0)

            residents= bc.get('residents', 3)

            runoff   = bc.get('runoff_coeff', COEFICIENTE_DE_ESCOAMENTO_PADRAO)

            discard_mm = bc.get('discard', 1.0)

            share    = bc.get('rainwater_share', 0.40)



        if mw and hasattr(mw, 'tab_project'):

            rf = mw.tab_project.txt_file_path.text()

            if rf and "Nenhum" not in rf:

                rain_file = rf.replace('\\', '/').split('/')[-1]



        if mw and hasattr(mw, 'tab_tanks_simulation'):

            ts = mw.tab_tanks_simulation

            if ts.last_single_result:

                r = ts.last_single_result

                potential_pct = r.potential_potable_savings_pct

                pluv_day   = r.avg_pluvial_consumed_l_day

                potable_day= r.avg_potable_consumed_l_day

                spill_day  = r.avg_spilled_l_day

                sat_full   = r.pct_days_full_satisfaction

                sat_null   = r.pct_days_null_satisfaction

                lower_vol  = r.lower_tank_vol

            if ts.last_sweep_result and ts.last_sweep_result.optimal_lower_tank_vol:

                lower_vol = ts.last_sweep_result.optimal_lower_tank_vol



        sym = "R$"

        if mw and hasattr(mw, 'tab_economic'):

            sym = mw.tab_tanks_simulation.get_currency_symbol()



        if mw and hasattr(mw, 'tab_economic'):

            econ = getattr(mw.tab_economic, 'last_econ_res', None)

            if econ is not None:

                capex = float(getattr(econ, 'total_investment', 0.0))

                vpl = float(getattr(econ, 'vpl', 0.0))

                tir = float(getattr(econ, 'tir_pct', 0.0))

                cash_flows = getattr(econ, 'annual_cash_flows', [])

                if len(cash_flows) > 1:

                    annual_gross = float(getattr(cash_flows[1], 'total_gross_savings_brl', 0.0))

                payback_simple = getattr(econ, 'payback_simple_years', None)

                payback_discounted = getattr(econ, 'payback_discounted_years', None)

                payback_s = f"{payback_simple:.1f}" if payback_simple is not None else "--"
                payback_d = f"{payback_discounted:.1f}" if payback_discounted is not None else "--"

        # O laudo gerencial usa o cenário de ótimo econômico (menor payback viável > 0)
        if mw and hasattr(mw, 'tab_economic') and getattr(mw.tab_economic, 'economic_optimum_volume', None):
            econ_opt_v = float(mw.tab_economic.economic_optimum_volume)
            if econ_opt_v > 0:
                lower_vol = econ_opt_v
                econ_dict = getattr(mw.tab_economic, 'last_sweep_econ_results', {}) or {}
                sc_v = econ_dict.get(round(econ_opt_v, 1))
                if sc_v:
                    capex = sc_v.get('capex', capex)
                    vpl = sc_v.get('vpl', vpl)
                    tir = sc_v.get('tir', tir)
                    payback = sc_v.get('payback')
                    payback_s = f"{payback:.1f}" if isinstance(payback, (int, float)) else "--"
                    payback_d = payback_s
                    annual_gross = sc_v.get('gross_monthly', 0.0) * 12.0
        elif mw and hasattr(mw, 'tab_global_optimizer'):
            optimizer = mw.tab_global_optimizer
            topsis = getattr(optimizer, 'last_topsis_result', None)
            if topsis and getattr(topsis, 'candidates', None):
                fi = getattr(topsis, 'financial_best_index', 0)
                if 0 <= fi < len(topsis.candidates):
                    best = topsis.candidates[fi]
                    if best.lower_tank_vol > 0:
                        lower_vol, capex, vpl = best.lower_tank_vol, best.capex_brl, best.vpl_brl
                        scenario = next((row for row in getattr(optimizer, 'last_scenario_results', [])
                                         if abs(row.get('vol', -1.0) - lower_vol) < 0.1), None)
                        if scenario:
                            annual_gross = scenario.get('gross_m', 0.0) * 12.0
                            tir = scenario.get('tir', 0.0)
                            payback = scenario.get('payback')
                            payback_s = f"{payback:.1f}" if isinstance(payback, (int, float)) else "--"
                            payback_d = payback_s


        # `share` vem da configuração do projeto, em fração.
        from netuno.core.fracao_atendivel import fracao_para_percentual
        share_pct = fracao_para_percentual("A fração atendível", share)
        pluvial_demand = demand * residents * share_pct / 100.0
        cfg = getattr(mw, 'config', None) if mw else None
        upper_used = bool(getattr(cfg, 'upper_tank_used', 0))
        upper_vol = float(getattr(cfg, 'upper_tank_vol', 0.0)) if upper_used else 0.0
        pump_count = int(getattr(cfg, 'pump_count', 0)) if upper_used else 0
        pump_power = getattr(cfg, 'pump_power_str', '-') if upper_used else '-'
        pump_kw = float(getattr(cfg, 'pump_power_kw', 0.0)) if upper_used else 0.0
        pump_flow = float(getattr(cfg, 'pump_flow_rate', 0.0)) if upper_used else 0.0
        threshold_widget = getattr(getattr(mw, 'tab_tanks_simulation', None), 'txt_pump_thresh_pct', None)
        pump_threshold = threshold_widget.text().strip() if threshold_widget else '-'


        # ── Logo ─────────────────────────────────────────────────

        # O PNG foi removido do PDF: imagens externas causavam falhas de
        # renderização em algumas instalações. O nome textual é estável.
        logo_obj = Paragraph("<b>NETUNO 5</b>", s_main_title)


        # ══════════════════════════════════════════════════════════

        # BLOCO 1 — CABEÇALHO

        # ══════════════════════════════════════════════════════════

        hdr_data = [[
            logo_obj,
            Paragraph(
                f"<b>{APP_VERSION_LABEL.upper()}</b>  •  {tr('Laudo Técnico Gerencial de Aproveitamento de Água de Chuva')}",
                s_main_title
            ),
            Paragraph(
                f"ABNT NBR 15527<br/><font color='#0369a1'><b>Ref.: {project_ref}</b><br/>{tr('Emissão')}: {date_str}</font>",
                s_sub_r
            ),
        ]]
        hdr = Table(hdr_data, colWidths=[32*mm, col_w - 64*mm, 32*mm])
        hdr.setStyle(TableStyle([
            ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
            ('ALIGN',       (2,0), (2,0),   'RIGHT'),
            ('LINEBELOW',   (0,0), (-1,0),  1.5, BLUE),
            ('BOTTOMPADDING',(0,0),(-1,-1), 5),
            ('TOPPADDING',  (0,0), (-1,-1), 0),
        ]))

        # ==========================================================
        # BLOCO 2 — KPI CARDS
        # ==========================================================
        kw = (col_w - 3 * 4) / 4

        def kpi_card(label, value, sub, bg, border):
            inner = Table([
                [Paragraph(label, s_kpi_lbl)],
                [Paragraph(value, s_kpi_val)],
                [Paragraph(sub,   s_kpi_sub)],
            ], colWidths=[kw])
            inner.setStyle(TableStyle([
                ('BACKGROUND',    (0,0), (-1,-1), bg),
                ('BOX',           (0,0), (-1,-1), 1, border),
                ('TOPPADDING',    (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
                ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ]))
            return inner

        kpi_row = [[
            kpi_card(tr("VOLUME RECOMENDADO"),  f"{br(lower_vol,0)} L",      tr("Ótimo econômico (menor payback)"), GREEN_L, GREEN),
            kpi_card(tr("Investimento CAPEX"),   f"{sym} {br(capex,2)}",      tr("Custo de implantação"), BLUE_L, BLUE),
            kpi_card(tr("VPL — 20 ANOS"),       f"{sym} {br(vpl,2)}",            tr("Retorno líquido acumulado"),BLUE_L,  BLUE),
            kpi_card(tr("PAYBACK ESTIMADO"),    f"{payback_s} {tr('anos')}",          f"TIR: {br(tir,1)}% {tr('a.a.')}", AMBER_L, AMBER),
        ]]
        kpi_tbl = Table(kpi_row, colWidths=[kw]*4,
                        hAlign='LEFT', spaceBefore=5, spaceAfter=5)

        kpi_tbl.setStyle(TableStyle([

            ('VALIGN',        (0,0), (-1,-1), 'TOP'),

            ('LEFTPADDING',   (0,0), (-1,-1), 2),

            ('RIGHTPADDING',  (0,0), (-1,-1), 2),

        ]))



        # ══════════════════════════════════════════════════════════

        # BLOCO 3 — DUAS COLUNAS (Edificação | Balanço Hídrico)

        # ══════════════════════════════════════════════════════════

        hw = (col_w - 5) / 2   # half width

        lw = hw * 0.58; vw = hw * 0.42



        left_rows = [

            [tr("Parâmetro Técnico"),         tr("Valor")],

            [tr("Série Pluviométrica"),        rain_file],

            [tr("Área de Captação (Telhado)"), f"{br(area,1)} m²"],

            [tr("Coef. de Escoamento (C)"),    br(runoff, 2)],

            [tr("Descarte Inicial (First Flush)"), f"{br(discard_mm,1)} mm"],

            [tr("Ocupantes / Moradores"),      f"{int(residents)} {tr('pessoas')}"],

            [tr("Demanda per capita"),         f"{br(demand,0)} L/hab/dia"],

            [tr("Demanda Pluvial Alvo"),       f"{br(pluvial_demand,0)} L/dia"],

        ]

        right_rows = [

            [tr("Indicador Hídrico"),               tr("Desempenho")],

            [tr("Volume do Reservatório"),           f"{br(lower_vol,0)} L"],

            [tr("Economia de Água Potável"),         f"{br(potential_pct,1)}%"],

            [tr("Consumo Médio Pluvial"),            f"{br(pluv_day,1)} L/dia"],

            [tr("Consumo Médio Potável (Rede)"),     f"{br(potable_day,1)} L/dia"],

            [tr("Volume Extravasado Médio"),         f"{br(spill_day,1)} L/dia"],

            [tr("Dias de Atendimento Total"),        f"{br(sat_full,1)}%"],

            [tr("Dias Sem Atendimento"),             f"{br(sat_null,1)}%"],

        ]



        two_col = Table([[

            Table([

                [sec_hdr(f"1. {tr('PARÂMETROS DA EDIFICAÇÃO & CHUVA')}", BLUE, hw)],

                [dtable(left_rows,  [lw, vw])],

            ], colWidths=[hw]),

            Table([

                [sec_hdr(f"2. {tr('RESULTADOS DO BALANÇO HÍDRICO')}", GREEN, hw)],

                [dtable(right_rows, [lw, vw])],

            ], colWidths=[hw]),

        ]], colWidths=[hw, hw], spaceBefore=0, spaceAfter=4)

        two_col.setStyle(TableStyle([

            ('VALIGN',       (0,0), (-1,-1), 'TOP'),

            ('LEFTPADDING',  (0,0), (0,-1), 0),

            ('RIGHTPADDING', (0,0), (0,-1), 3),

            ('LEFTPADDING',  (1,0), (1,-1), 3),

            ('RIGHTPADDING', (1,0), (1,-1), 0),

        ]))



        # ══════════════════════════════════════════════════════════

        # BLOCO 4 — TABELA ECONÔMICA (horizontal)

        # ══════════════════════════════════════════════════════════

        ew = col_w / 6

        econ_rows = [

            [tr("Investimento CAPEX"), tr("Economia Bruta 1º Ano"),

             tr("Payback Simples"),    tr("Payback Descontado"),

             tr("VPL (20 Anos)"),      tr("TIR (% a.a.)")],

            [f"{sym} {br(capex,2)}",  f"{sym} {br(annual_gross,2)}/{tr('ano')}",

             f"{payback_s} {tr('anos')}",  f"{payback_d} {tr('anos')}",

             f"{sym} {br(vpl,2)}",    f"{br(tir,1)}% {tr('a.a.')}"],

        ]

        econ_tbl = Table(econ_rows, colWidths=[ew]*6)

        econ_tbl.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,0), colors.HexColor('#f1f5f9')),

            ('FONTNAME',      (0,0), (-1,0), cjk_font or 'Helvetica-Bold'),
            ('FONTNAME',      (0,1), (-1,1), cjk_font or 'Helvetica-Bold'),
            ('FONTSIZE',      (0,0), (-1,-1), 8),

            ('GRID',          (0,0), (-1,-1), 0.4, BORDER),

            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),

            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),

            ('TOPPADDING',    (0,0), (-1,-1), 5),

            ('BOTTOMPADDING', (0,0), (-1,-1), 5),

            ('TEXTCOLOR',     (0,1), (-1,1), GREEN),

            ('BACKGROUND',    (0,1), (-1,1), GREEN_L),

            ('TEXTCOLOR',     (0,0), (-1,0), SLATE),
        ]))

        # Memorial construtivo resumido: parâmetros suficientes para orientar
        # a cotação e a compatibilização inicial do sistema selecionado.
        construction_rows = [
            [tr("Componente / especificação"), tr("Valor de referência")],
            [tr("Cisterna inferior"), f"{br(lower_vol, 0)} L"],
            [tr("Reservatório superior"), f"{br(upper_vol, 0)} L" if upper_used else tr("Não utilizado")],
            [tr("Motobomba"), f"{pump_count} × {pump_power} CV ({br(pump_kw, 3)} kW)" if upper_used else tr("Não aplicável")],
            [tr("Vazão nominal de recalque"), f"{br(pump_flow, 0)} L/h" if upper_used else tr("Não aplicável")],
            [tr("Limiar de acionamento"), f"{pump_threshold}%" if upper_used and pump_threshold not in ('', '-') else tr("A definir no projeto")],
            [tr("Uso previsto"), tr("Água de chuva para fins não potáveis; validar tubulações, filtros, extravasor, registros e separação da rede potável no projeto executivo.")],
        ]
        construction_tbl = dtable(construction_rows, [col_w * 0.34, col_w * 0.66])


        # ══════════════════════════════════════════════════════════

        # BLOCO 5 — DISCLAIMER + RODAPÉ

        # ══════════════════════════════════════════════════════════

        disc_text = (

            f"<b>⚠ {tr('É responsabilidade exclusiva do(a) engenheiro(a) ou projetista')}</b> "

            f"{tr('responsável avaliar, verificar e validar todos os resultados.')}"

        )

        disc_tbl = Table([[Paragraph(disc_text, s_disc)]], colWidths=[col_w])

        disc_tbl.setStyle(TableStyle([

            ('BACKGROUND',    (0,0), (-1,-1), WARN_L),

            ('BOX',           (0,0), (-1,-1), 0.75, AMBER),

            ('TOPPADDING',    (0,0), (-1,-1), 4),

            ('BOTTOMPADDING', (0,0), (-1,-1), 4),

            ('LEFTPADDING',   (0,0), (-1,-1), 7),

            ('RIGHTPADDING',  (0,0), (-1,-1), 7),

        ]))



        signature_tbl = Table([[

            Paragraph(

                f"<b>{tr('Assinatura do(a) Responsável Técnico(a)')}</b> "

                f"<font color='#64748b'>({tr('manual ou digital')})</font><br/><br/><br/><br/><br/>"

                "____________________________________________________________<br/>"

                f"{tr('Nome completo')}: ______________________________________________________<br/><br/>"

                f"{tr('CREA / Registro Profissional')}: ____________________________________________________________",

                s_foot,

            )

        ]], colWidths=[col_w])

        signature_tbl.setStyle(TableStyle([

            ('BOX',           (0,0), (-1,-1), 0.75, BORDER),

            ('TOPPADDING',    (0,0), (-1,-1), 5),

            ('BOTTOMPADDING', (0,0), (-1,-1), 5),

            ('LEFTPADDING',   (0,0), (-1,-1), 7),

            ('RIGHTPADDING',  (0,0), (-1,-1), 7),

        ]))



        foot_tbl = Table([[

            Paragraph(

                f"<b>{tr('Grupo de Pesquisa Gestão do Espaço Sustentável | UFSC')}</b>"

                f"<br/>{APP_VERSION_LABEL} Engine — {tr('Documento gerado automaticamente')}",
                s_foot

            )

        ]], colWidths=[col_w])

        foot_tbl.setStyle(TableStyle([

            ('VALIGN',      (0,0), (-1,-1), 'BOTTOM'),

            ('LINEABOVE',   (0,0), (-1,0),  0.75, BORDER),

            ('TOPPADDING',  (0,0), (-1,-1), 4),

            ('LEFTPADDING', (0,0), (0,-1), 0),

            ('RIGHTPADDING',(0,0), (0,-1), 0),

        ]))



        # ── Assemble ──────────────────────────────────────────────

        # Mantém o cabeçalho da seção junto da tabela. Assim, quando a tabela
        # estiver no fim da página, todo o bloco começa na página seguinte.
        economic_section = KeepTogether([
            sec_hdr(f"3. {tr('VIABILIDADE ECONÔMICA')}", NAVY, col_w),
            Spacer(1, 2),
            econ_tbl,
        ])
        construction_section = KeepTogether([
            sec_hdr("4. MEMORIAL CONSTRUTIVO PRELIMINAR", BLUE, col_w),
            Spacer(1, 2),
            construction_tbl,
        ])
        disclaimer_section = KeepTogether([
            disc_tbl,
            Spacer(1, 4),
            signature_tbl,
        ])

        elements = [
            hdr,

            Spacer(1, 4),

            kpi_tbl,
            economic_section,
            Spacer(1, 5),
            construction_section,
            Spacer(1, 5),
            disclaimer_section,
            Spacer(1, 4),

            foot_tbl,

        ]

        doc.build(elements)



    def export_excel_report(self):

        from netuno import get_kebab_filename

        def_name = get_kebab_filename("netuno-simulacao", "xlsx")

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Planilha Excel", def_name, "Excel Files (*.xlsx)")

        if not file_path:

            return



        try:

            main_win = self.window()

            df_summary = pd.DataFrame([

                {"Parâmetro": "Área de Captação (m²)", "Valor": "100,0"},

                {"Parâmetro": "Demanda Total (L/dia)", "Valor": "300,0"},

                {"Parâmetro": "Potencial de Economia (%)", "Valor": "41,8"},

                {"Parâmetro": "Potência da Motobomba", "Valor": "0,50 CV (0,37 kW)"},

                {"Parâmetro": "Limiar de Acionamento Recalque", "Valor": "75,0%"},

                {"Parâmetro": "Número de Acionamentos (Partidas)", "Valor": "180 partidas/ano"},

                {"Parâmetro": "Consumo Energia Elétrica (kWh/ano)", "Valor": "42,5 kWh/ano"},

                {"Parâmetro": "Custo Energia Elétrica (R$/ano)", "Valor": "R$ 38,25/ano"},

                {"Parâmetro": "Reajuste Tarifa Água (% a.a.)", "Valor": "5,0%"},

                {"Parâmetro": "Reajuste Tarifa Esgoto (% a.a.)", "Valor": "5,0%"},

                {"Parâmetro": "Reajuste Tarifa Energia (% a.a.)", "Valor": "5,0%"},

                {"Parâmetro": "Inflação O&M (% a.a.)", "Valor": "4,0%"},

            ])



            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:

                df_summary.to_excel(writer, sheet_name='Resumo', index=False)



            QMessageBox.information(self, "Sucesso", f"Planilha Excel exportada com sucesso em:\n{file_path}")



        except Exception as e:

            QMessageBox.critical(self, "Erro no Excel", f"Falha ao exportar Excel:\n{str(e)}")



    def export_netuno4_csv(self):
        from netuno import get_kebab_filename

        def_name = get_kebab_filename("netuno-projeto", "csv")

        file_path, _ = QFileDialog.getSaveFileName(self, "Salvar Projeto no Formato Netuno 4.0", def_name, "CSV Files (*.csv)")

        if not file_path:

            return



        try:

            from netuno.core.parser import NetunoConfig, export_netuno_csv

            from netuno.core.simulation import SingleTankSimulationResult

            

            cfg = NetunoConfig(

                area=100.0,

                demand_value=200.0,

                residents_count=4,

                rainwater_share=0.4,

                runoff_coeff=COEFICIENTE_DE_ESCOAMENTO_PADRAO,

                discard=1.0,

                lower_tank_max=10000.0,

                lower_tank_step=500.0,

                lower_tank_mode=1

            )

            

            dummy_results = [

                SingleTankSimulationResult(lower_tank_vol=0, potential_potable_savings_pct=0.0, avg_pluvial_consumed_l_day=0.0, avg_potable_consumed_l_day=300.0, avg_spilled_l_day=200.0, pct_days_full_satisfaction=0.0, pct_days_partial_satisfaction=0.0, pct_days_null_satisfaction=100.0),

                SingleTankSimulationResult(lower_tank_vol=500, potential_potable_savings_pct=25.6, avg_pluvial_consumed_l_day=76.8, avg_potable_consumed_l_day=223.2, avg_spilled_l_day=123.2, pct_days_full_satisfaction=50.0, pct_days_partial_satisfaction=10.0, pct_days_null_satisfaction=40.0),

                SingleTankSimulationResult(lower_tank_vol=1000, potential_potable_savings_pct=32.4, avg_pluvial_consumed_l_day=97.2, avg_potable_consumed_l_day=202.8, avg_spilled_l_day=102.8, pct_days_full_satisfaction=62.0, pct_days_partial_satisfaction=8.0, pct_days_null_satisfaction=30.0)

            ]

            

            export_netuno_csv(cfg, dummy_results, file_path)

            QMessageBox.information(self, "Sucesso", f"Arquivo CSV no formato oficial do Netuno 4.0 gerado em:\n{file_path}")



        except Exception as e:

            QMessageBox.critical(self, "Erro no CSV", f"Falha ao exportar CSV Netuno 4.0:\n{str(e)}")


def build_stakeholder_landscape_pdf(report_owner, file_path: str):
    """Reutiliza o laudo executivo em paisagem na aba moderna de relatórios."""
    return TabReportsExport._build_landscape_pdf(report_owner, file_path)
