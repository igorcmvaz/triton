"""Gera o artigo científico e os apêndices em arquivos DOCX separados."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.section import WD_SECTION_START
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from scripts.build_comprehensive_article import (
    CLIMATE_REGIONS,
    NATIONAL_RESULTS,
    SOURCES,
    TYPOLOGIES,
    optimization_table,
)
from netuno.core.cost_estimates import estimate_calibrated_capex_opex

ARTICLE = ROOT / "Artigo_Cientifico_Netuno5.docx"
APPENDICES = ROOT / "Apendices_Artigo_Netuno5.docx"
TARIFFS = ROOT / "tarifas" / "catalogo_tarifas_auditado_652.csv"
TARIFFS_XLSX = ROOT / "tarifas" / "catalogo_tarifas_auditado_652.xlsx"
SWEEP = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "capitais_varredura_completa.csv"
FIG = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "figuras_publicacao"
COST_DB = ROOT / "netuno" / "data" / "costs_database.json"

NAVY = "1F2933"
TEAL = "0F6B78"
BLUE = "1F2933"
MUTED = "5F6B76"
LIGHT = "E9ECEF"
GOLD = "7A5C00"
INK = RGBColor(31, 41, 51)
CONTENT_DXA = 9360


def set_repeat_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tag = OxmlElement("w:tblHeader")
    tag.set(qn("w:val"), "true")
    tr_pr.append(tag)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def set_run(run, size=None, bold=None, italic=None, color=None, font="Arial"):
    run.font.name = font
    run._element.get_or_add_rPr().rFonts.set(qn("w:ascii"), font)
    run._element.get_or_add_rPr().rFonts.set(qn("w:hAnsi"), font)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.bold = bold
    if italic is not None:
        run.italic = italic
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def add_page_field(paragraph):
    run = paragraph.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)


def configure(doc, running_label):
    doc.settings.odd_and_even_pages_header_footer = False
    section = doc.sections[0]
    section.different_first_page_header_footer = False
    section.page_width = Inches(8.2677)
    section.page_height = Inches(11.6929)
    section.top_margin = section.bottom_margin = Inches(0.9843)
    section.left_margin = section.right_margin = Inches(0.9843)
    section.header_distance = section.footer_distance = Inches(0.492)

    sect_pr = section._sectPr
    line_numbers = OxmlElement("w:lnNumType")
    line_numbers.set(qn("w:countBy"), "1")
    line_numbers.set(qn("w:restart"), "continuous")
    sect_pr.append(line_numbers)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.5
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for name, size, color, before, after in [
        ("Heading 1", 14, BLUE, 16, 8),
        ("Heading 2", 12, BLUE, 12, 6),
        ("Heading 3", 11, NAVY, 8, 4),
    ]:
        style = doc.styles[name]
        style.font.name = "Arial"
        style.font.size = Pt(size)
        style.font.bold = True
        style.font.color.rgb = RGBColor.from_string(color)
        style.paragraph_format.space_before = Pt(before)
        style.paragraph_format.space_after = Pt(after)
        style.paragraph_format.keep_with_next = True

    header = section.header.paragraphs[0]
    header.clear()
    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    add_page_field(footer)


def cover(doc, kicker, title, subtitle, note, *, article=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(36)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_run(p.add_run(kicker.upper()), size=10, bold=True, color=MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(8)
    set_run(p.add_run(title), size=18, bold=True, color=NAVY)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(24)
    set_run(p.add_run(subtitle), size=11, italic=True, color=MUTED)
    if article:
        for label, value in [
            ("Autores", "[Inserir nomes completos e ORCID]"),
            ("Afiliações", "[Inserir instituições, cidades e países]"),
            ("Autor correspondente", "[Inserir nome, endereço postal e e-mail]"),
        ]:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(4)
            set_run(p.add_run(f"{label}: "), size=10, bold=True)
            set_run(p.add_run(value), size=10, color=MUTED)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(28)
    set_run(p.add_run(note), size=10, italic=True, color=MUTED)
    doc.add_page_break()


def add_table(doc, headers, rows, widths=None, font_size=8.2):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.style = "Table Grid"
    tbl_pr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    tbl_w = tbl_pr.find(qn("w:tblW"))
    if tbl_w is None:
        tbl_w = OxmlElement("w:tblW")
        tbl_pr.append(tbl_w)
    tbl_w.set(qn("w:w"), str(CONTENT_DXA))
    tbl_w.set(qn("w:type"), "dxa")
    tbl_ind = OxmlElement("w:tblInd")
    tbl_ind.set(qn("w:w"), "120")
    tbl_ind.set(qn("w:type"), "dxa")
    tbl_pr.append(tbl_ind)

    if widths is None:
        widths = [CONTENT_DXA // len(headers)] * len(headers)
        widths[-1] += CONTENT_DXA - sum(widths)
    # python-docx cria tblGrid com colunas iguais; substituí-lo é necessário
    # para que tblGrid, tcW e tblW expressem a mesma geometria fixa.
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        col = OxmlElement("w:gridCol")
        col.set(qn("w:w"), str(width))
        grid.append(col)
    set_repeat_header(table.rows[0])
    for i, text in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = str(text)
        shade(cell, LIGHT)
        cell.width = Inches(widths[i] / 1440)
        cell.paragraphs[0].paragraph_format.keep_with_next = True
        for run in cell.paragraphs[0].runs:
            set_run(run, size=font_size, bold=True, color=NAVY)
    for values in rows:
        row = table.add_row()
        row_pr = row._tr.get_or_add_trPr()
        row_pr.append(OxmlElement("w:cantSplit"))
        cells = row.cells
        for i, value in enumerate(values):
            cells[i].text = "—" if value is None else str(value)
            cells[i].width = Inches(widths[i] / 1440)
            cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for paragraph in cells[i].paragraphs:
                paragraph.paragraph_format.space_after = Pt(1)
                paragraph.paragraph_format.line_spacing = 1.0
                for run in paragraph.runs:
                    set_run(run, size=font_size)
    return table


def add_figure(doc, filename, caption, width=6.35):
    path = FIG / filename
    if not path.exists():
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(path), width=Inches(width))
    shape._inline.docPr.set("descr", caption)
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c.paragraph_format.keep_together = True
    c.paragraph_format.space_after = Pt(9)
    match = re.match(r"(Figura\s+[A-Z]?\.?\d+\.)\s*(.*)", caption)
    if match:
        set_run(c.add_run(match.group(1) + " "), size=9, bold=True)
        set_run(c.add_run(match.group(2)), size=9)
    else:
        set_run(c.add_run(caption), size=9)


def bullet(doc, text):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(4)
    p.add_run(text)


def equation(doc, label, text):
    """Insere equação editável do Word em tabela 1 × 2 sem bordas."""
    number_match = re.search(r"(?:Equação\s+)?([A-Z]\.\d+|\d+)", label)
    if number_match is None:
        raise ValueError(f"Rótulo de equação inválido: {label}")
    number = number_match.group(1)

    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    widths = [8400, 960]
    table.columns[0].width = Inches(widths[0] / 1440)
    table.columns[1].width = Inches(widths[1] / 1440)
    tbl_pr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tbl_pr.append(layout)
    grid = table._tbl.tblGrid
    for child in list(grid):
        grid.remove(child)
    for width in widths:
        grid_col = OxmlElement("w:gridCol")
        grid_col.set(qn("w:w"), str(width))
        grid.append(grid_col)
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        border = OxmlElement(f"w:{edge}")
        border.set(qn("w:val"), "nil")
        borders.append(border)
    tbl_pr.append(borders)
    row_pr = table.rows[0]._tr.get_or_add_trPr()
    row_pr.append(OxmlElement("w:cantSplit"))

    equation_cell, number_cell = table.rows[0].cells
    equation_cell.width = Inches(widths[0] / 1440)
    number_cell.width = Inches(widths[1] / 1440)
    equation_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    number_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    p = equation_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    math = OxmlElement("m:oMath")
    math_run = OxmlElement("m:r")
    run_props = OxmlElement("w:rPr")
    fonts = OxmlElement("w:rFonts")
    fonts.set(qn("w:ascii"), "Cambria Math")
    fonts.set(qn("w:hAnsi"), "Cambria Math")
    run_props.append(fonts)
    size = OxmlElement("w:sz")
    size.set(qn("w:val"), "22")
    run_props.append(size)
    math_run.append(run_props)
    math_text = OxmlElement("m:t")
    math_text.text = text
    math_run.append(math_text)
    math.append(math_run)
    p._p.append(math)

    p = number_cell.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)
    set_run(p.add_run(f"({number})"), size=10)
    return table


def currency(x):
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def data_context():
    tariffs = pd.read_csv(TARIFFS)
    required = {"confianca_global_grau", "energia_aneel_status_vigencia"}
    if tariffs.empty or not required.issubset(tariffs.columns):
        # A planilha auditada é a fonte completa; o CSV pode ser um arquivo de
        # intercâmbio temporário durante atualizações tarifárias.
        tariffs = pd.read_excel(TARIFFS_XLSX, sheet_name="Tarifas 652")
    sweep = pd.read_csv(SWEEP, sep=";")
    opt = optimization_table(sweep)
    best = sweep.loc[sweep.groupby(["city", "building_code"])["topsis_score"].idxmax()].copy()
    capital = best.groupby(["city", "uf", "regiao"], as_index=False).agg(
        economia=("potential_water_savings_pct", "mean"),
        volume=("lower_tank_vol_l", "median"),
        vpl=("vpl_6pct_brl", "mean"),
        co2=("lifetime_net_co2_saved_kg", "mean"),
        payback=("payback_years", "median"),
    )
    costs = json.loads(COST_DB.read_text(encoding="utf-8"))
    return tariffs, sweep, opt, capital, costs


def build_article(tariffs, opt, capital):
    doc = Document()
    configure(doc, "Artigo científico | Sistemas prediais de água de chuva")
    cover(
        doc,
        "Artigo científico",
        "Desempenho técnico, econômico, ambiental e climático de sistemas prediais de aproveitamento de água de chuva no Brasil",
        "Cinco tipologias residenciais, 652 municípios, 19 modelos CMIP6 e otimização multicritério",
        "Versão reorganizada | corte tarifário: 24 de agosto de 2026",
        article=True,
    )

    doc.add_heading("Resumo", level=1)
    doc.add_paragraph(
        "Este estudo avalia sistemas prediais de aproveitamento de água de chuva em cinco tipologias residenciais e 652 municípios brasileiros. "
        "O balanço hídrico diário foi combinado com tarifas progressivas, CAPEX regionalizado, análise financeira em 20 anos, balanço simplificado "
        "de carbono e otimização TOPSIS. A base climática reúne o período histórico (1980–2013) e projeções CMIP6, incluindo SSP2-4.5 e SSP5-8.5. "
        "Os resultados mostram que eficiência percentual, retorno financeiro e benefício ambiental não indicam necessariamente o mesmo volume. "
        "No fim do século sob SSP5-8.5, a redução relativa agregada do potencial varia de 16,0% no Sul a 31,7% no Norte. A auditoria tarifária "
        "distingue valores reconciliados, pendentes e atos ANEEL recém-expirados, permitindo análise de sensibilidade sem ocultar incertezas locais."
    )
    p = doc.add_paragraph()
    set_run(p.add_run("Palavras-chave: "), bold=True)
    p.add_run("aproveitamento de água de chuva; dimensionamento de reservatórios; CMIP6; análise multicritério; viabilidade econômica; adaptação climática.")

    doc.add_heading("1. Introdução", level=1)
    doc.add_paragraph(
        "A urbanização, a variabilidade climática e o custo crescente dos serviços de água tornam relevante a substituição de usos não potáveis por "
        "água de chuva. Entretanto, um reservatório maior não é automaticamente melhor: ele pode elevar CAPEX, ocupar área, incorporar mais carbono e "
        "permanecer subutilizado em regimes de precipitação concentrada. A decisão depende simultaneamente da área de cobertura, demanda, regularidade "
        "da chuva, estrutura tarifária, escala da edificação e critério adotado para definir o ótimo."
    )
    doc.add_paragraph(
        "O objetivo é comparar o desempenho técnico, financeiro e ambiental de cinco tipologias residenciais no território brasileiro, quantificar a "
        "mudança entre clima histórico e futuro, comparar volumes ótimos por diferentes critérios e identificar diferenças entre capitais. O estudo "
        "também explicita como tarifas, custos regionais e incertezas de modelos climáticos condicionam a interpretação dos resultados."
    )

    doc.add_heading("2. Método", level=1)
    doc.add_heading("2.1. Dados de entrada", level=2)
    doc.add_paragraph(
        "A unidade de análise foi a combinação cidade–série climática–tipologia–regra de descarte–demanda–fração não potável–volume. "
        "Foram representados 652 municípios brasileiros e cinco tipologias: casa unifamiliar térrea (UTI: 4 moradores, uma economia, 60,19 m²), "
        "casa unifamiliar geminada (UTG: 8 moradores, duas economias, 115,43 m²), sobrado multifamiliar geminado (MSG: 16 moradores, quatro "
        "economias, 132,53 m²), bloco multifamiliar H (MFH: 64 moradores, 16 economias, 158,70 m²) e bloco multifamiliar retangular (MFL: 128 "
        "moradores, 32 economias, 421,52 m²). Coberturas cerâmicas receberam coeficiente de escoamento 0,80; coberturas de fibrocimento, 0,90."
    )
    doc.add_paragraph(
        "O experimento fatorial avaliou consumos per capita de 120, 150 e 180 L/(hab.dia), frações substituíveis de 30%, 40% e 50%, e 12 "
        "capacidades inferiores discretas: 0,5; 1; 2; 3; 5; 7,5; 10; 15; 20; 30; 40 e 50 m³. O reservatório superior, utilizado na estimativa "
        "de custos, foi definido por Vsup=max(200;0,10Vinf), em litros. O caso-base apresentado nas comparações usa 150 L/(hab.dia) e 40% de "
        "substituição, mas a base de simulações preserva todas as combinações."
    )
    equation(doc, "Equação 1", "Dᵗᵒᵗ = Nhab · dpc;   Dᵖˡ = fpl · Dᵗᵒᵗ")
    equation(doc, "Equação 2", "Vsup = max(200 L; 0,10 · Vinf)")
    doc.add_paragraph(
        "Foram considerados sete tratamentos de first flush: ausência de descarte (0 mm) e descartes de 2 ou 4 mm sob três regras. No modo 1, "
        "o descarte ocorre em todo dia chuvoso; no modo 2, somente quando a precipitação do dia anterior é inferior a 1 mm; no modo 3, somente "
        "quando transcorreram pelo menos sete dias desde o último descarte. Assim, cada série climática gera 5×7×3×3×12=3.780 perfis de "
        "dimensionamento. As 86.716 séries processadas produziram 327.786.480 combinações diárias agregadas na base consolidada."
    )
    doc.add_paragraph(
        "A precipitação histórica abrange 1980–2013. As projeções foram organizadas em Near Future (2015–2040), Mid Future (2041–2070) e "
        "Far Future (2075–2100), para SSP2-4.5 e SSP5-8.5 e até 19 modelos globais CMIP6. Cada GCM foi simulado separadamente. Médias entre "
        "modelos aparecem apenas na etapa estatística e são declaradas nas legendas; portanto, a simulação não usa uma chuva média artificial. "
        "Arquivos ausentes não foram imputados. Cidade, modelo, cenário e horizonte foram extraídos do nome padronizado do arquivo, e os vetores "
        "diários foram carregados na ordem temporal original."
    )
    doc.add_paragraph(
        "A análise nacional das figuras usa amostra estratificada de 350.000 registros quando o volume integral inviabiliza a renderização. A seleção "
        "ótima, os indicadores armazenados e os agregados por capital foram calculados a partir do Parquet consolidado. As estatísticas agrupadas "
        "identificam explicitamente se incluem todos os volumes ou apenas soluções TOPSIS; se separam tipologias; e se agregam GCMs, SSPs e horizontes."
    )

    doc.add_heading("2.2. Tarifas", level=2)
    doc.add_paragraph(
        "A economia monetária foi calculada pela diferença entre duas faturas, evitando a aproximação simplista tarifa×volume. A base "
        "reúne 652 municípios brasileiros auditados, preservando o prestador de saneamento, categoria tarifária residencial, parcelas fixas "
        "ou consumos mínimos, limites e preços de todas as faixas de consumo, percentual oficial de esgoto (variando de 0% a 100%) e número de "
        "economias. Todos os valores de tarifas, custos de investimento (CAPEX) e despesas operacionais (OPEX) são considerados com todos os impostos "
        "e tributos inclusos (premissa de desembolso final do usuário). O consumo mensal do edifício é dividido pelo número de economias antes da "
        "aplicação da progressividade e a fatura unitária é multiplicada novamente por esse número, procedimento decisivo para edifícios multifamiliares."
    )
    equation(doc, "Equação 3", "qᵘ = Qmês / Nunidades")
    equation(doc, "Equação 4", "qᵘₖ = max[0; min(qᵘ,bₖ) − aₖ]")
    equation(doc, "Equação 5", "Fágua(Q) = Nunidades · [Ffixa + Σₖ(qᵘₖ · tₖ)]")
    equation(doc, "Equação 6", "Ftotal(Q) = Fágua(Q) · (1 + αesgoto/100)")
    equation(doc, "Equação 7", "Bágua,ano = 12 · max{0; Ftotal(Qbase) − Ftotal(Qresidual)}")
    doc.add_paragraph(
        "Nas equações, [aₖ,bₖ] é a faixa k, tₖ é sua tarifa volumétrica homologada e Ffixa agrega parcelas fixas aplicáveis. O esgoto foi modelado "
        "como percentual αesgoto da conta de água conforme a regra oficial regulada de cada município. A economia anual é truncada em zero para impedir "
        "que qualquer inconsistência cadastral produza benefício fictício negativo. Para fins de auditoria e reprodutibilidade, cada registro municipal "
        "armazena o link oficial da publicação tarifária e alerta de validação."
    )
    doc.add_paragraph(
        "A tarifa elétrica corresponde à subclasse B1 residencial convencional homologada pela ANEEL para a concessionária da área de concessão do "
        "município, em R$/kWh (corte temporal: 24 de agosto de 2026). No saneamento, autoridade da fonte, atualidade, completude das faixas, identidade "
        "do operador e igualdade entre valor publicado e valor modelado são avaliados separadamente. Grau A exige fonte primária oficial, vigente e com "
        "reconciliação numérica completa."
    )

    doc.add_heading("2.3. Modelo matemático de simulação técnica", level=2)
    doc.add_paragraph(
        "O motor executa balanço de massa diário contínuo, iniciando a cisterna vazia. Seja Pₜ a precipitação (mm), A a área de cobertura (m²), "
        "C o coeficiente de escoamento, FF a lâmina de descarte (mm), Vmax a capacidade inferior (L), Vₜ₋₁ o estoque final anterior (L), "
        "Dpl a demanda pluvial (L/d) e Dtot a demanda total (L/d). Como 1 mm sobre 1 m² equivale a 1 L, não há fator adicional de conversão."
    )
    equation(doc, "Equação 8", "Iₜ = 1 se a regra de descarte for ativada no dia t; 0 em caso contrário")
    equation(doc, "Equação 9", "Pₜ,ef = Iₜ · max(Pₜ − FF,0) + (1 − Iₜ) · Pₜ")
    equation(doc, "Equação 10", "Qₜ = Pₜ,ef · A · C")
    equation(doc, "Equação 11", "Sₜ = Vₜ₋₁ + Qₜ")
    equation(doc, "Equação 12", "Oₜ = max(Sₜ − Vmax,0);   Aₜ = min(Sₜ,Vmax)")
    equation(doc, "Equação 13", "Uₜ = min(Dpl,Aₜ);   Vₜ = Aₜ − Uₜ")
    equation(doc, "Equação 14", "Wₜ = Dtot − Uₜ")
    doc.add_paragraph(
        "Qₜ é o volume captado, Sₜ a disponibilidade antes do limite, Oₜ o extravasamento, Aₜ o estoque disponível após o limite, Uₜ o "
        "consumo pluvial, Vₜ o estoque final e Wₜ o consumo de água potável. Essa ordem é a implementada: primeiro se limita a entrada pela "
        "capacidade e contabiliza-se o extravasamento; depois se atende a demanda. A forma simplificada Vₜ=min[Vmax,Vₜ₋₁+Qₜ−Dₜ] não é "
        "usada porque poderia subestimar o extravasamento em dias de chuva intensa."
    )
    equation(doc, "Equação 15", "E = 100 · ΣₜUₜ / ΣₜDtot")
    equation(doc, "Equação 16", "Rfull = 100 · n(Uₜ≥Dpl−10⁻⁴)/T")
    equation(doc, "Equação 17", "Rpartial = 100 · n(10⁻⁴<Uₜ<Dpl−10⁻⁴)/T")
    equation(doc, "Equação 18", "Rnull = 100 · n(Uₜ≤10⁻⁴)/T")
    equation(doc, "Equação 19", "Vpl,ano = (365,25/1000) · (ΣₜUₜ/T)")
    equation(doc, "Equação 20", "Vpot,ano = (365,25/1000) · (ΣₜWₜ/T)")
    equation(doc, "Equação 21", "Vspill,ano = (365,25/1000) · (ΣₜOₜ/T)")
    doc.add_paragraph(
        "As três classes de atendimento são mutuamente exclusivas e somam 100%, salvo arredondamento. Os volumes anuais são anualizações da média "
        "diária da própria série e não a soma bruta quando o horizonte tem mais de um ano. O ótimo técnico é obtido no pós-processamento. "
        "Para volumes ordenados Vₖ, calcula-se o ganho marginal da economia em pontos percentuais por m³ adicional; seleciona-se o primeiro volume "
        "positivo com Δₖ≤2,5 p.p./m³. O núcleo genérico possui 5,0 p.p./m³ como valor padrão de interface, mas esse padrão não foi o "
        "limiar experimental usado neste artigo."
    )
    equation(doc, "Equação 22", "Δₖ = (Eₖ − Eₖ₋₁)/[(Vₖ − Vₖ₋₁)/1000]")
    equation(doc, "Equação 23", "Vót,téc = min{Vₖ>0 : Δₖ ≤ 2,5 p.p./m³}")

    doc.add_heading("2.4. Análise financeira", level=2)
    doc.add_paragraph(
        "O CAPEX cobre cisterna inferior e reservatório superior, motobombas, painel de comando, sensores de nível, filtração e tratamento, "
        "dispositivo de separação atmosférica (air gap NBR 5626/15527), rede de tubulações prediais e mão de obra de instalação especializada. "
        "Preços de reservatórios são interpolados linearmente a partir de cotações comerciais catalogadas; acima do maior ponto, utiliza-se a "
        "inclinação marginal dos dois últimos volumes. A rede de tubulações em PVC é modelada por trechos nos quatro diâmetros nominais padrão "
        "(DN 50, 75, 100 e 150 mm) com custos unitários baseados no SINAPI/Caixa (R$ 18,50/m para DN 50; R$ 28,00/m para DN 75; R$ 35,00/m para DN 100; "
        "e R$ 68,00/m para DN 150) acrescidos de 25% para conexões, curvas e registros. A mão de obra de instalação civil, hidráulica e elétrica "
        "corresponde ao maior valor entre o piso tipológico e 30% dos materiais. Por fim, todo o CAPEX e a manutenção periódica recebem o Fator Regional "
        "da UF (fUF), calibrado pela composição de 55% materiais, 30% mão de obra local e 15% frete/logística (variando de 0,93 a 1,21 em relação a SP=1,00)."
    )
    equation(doc, "Equação 24", "Ctank(V)=Cₖ+[Cₖ₊₁−Cₖ]·(V−Vₖ)/(Vₖ₊₁−Vₖ)")
    equation(doc, "Equação 25", "Cpipes = 1,25 · Σ_{d} (L_{d} · c_{d})   [d ∈ {50, 75, 100, 150 mm}]")
    equation(doc, "Equação 26", "Cmat = Cinf+Csup+Cpump+Cpipes+Cpanel+Csens+Ctreat+Cairgap")
    equation(doc, "Equação 27", "Clabor = max(Clabor,min; 0,30·Cmat)")
    equation(doc, "Equação 28", "CAPEXUF = fUF · (Cmat+Clabor)")
    doc.add_paragraph(
        "O OPEX anual é composto pela manutenção preventiva regionalizada (Cmaint,UF = Cmaint,base · fUF), eletricidade de bombeamento e "
        "desinfecção com cloro. Na triagem massiva adota-se intensidade específica de bombeamento de 0,45 kWh/m³ multiplicada pela tarifa elétrica B1 "
        "da concessionária local (Telec) e cloração de R$ 0,05/m³ (2,0 mg/L de Cl₂ ativo a R$ 25,00/kg). O núcleo detalhado do programa também "
        "suporta cálculo hidromecânico exato da bomba por altura manométrica, rendimento, potência e partidas elétricas."
    )
    equation(doc, "Equação 29", "Epump,ano = 0,45 · Vpl,ano")
    equation(doc, "Equação 30", "Cpump,ano = Epump,ano · Telec")
    equation(doc, "Equação 31", "CCl2,ano = 0,05 · Vpl,ano")
    equation(doc, "Equação 32", "OPEXano = (Cmaint,base · fUF) + Cpump,ano + CCl2,ano")
    equation(doc, "Equação 33", "tpump = Vpump/q + Nstart·tstart;   Epump = P·tpump/η")
    doc.add_paragraph(
        "Foi adotada vida útil n=20 anos e benefício líquido anual constante L=Bágua,ano−OPEXano. Os fatores de valor presente foram calculados "
        "para 6%, 10% e 14% a.a. O cenário principal é 6% a.a. O VPL usa uma anuidade uniforme, o payback simples é limitado a 99 anos quando "
        "L≤0, e o LCOW divide todos os custos presentes pelo volume pluvial presente. A coluna denominada TIR no runner massivo é, estritamente, "
        "a razão anual L/CAPEX, em porcentagem, e não a raiz da equação de TIR; por isso é tratada como retorno anual simples no texto. O núcleo "
        "econômico completo possui solução iterativa de TIR para fluxos mensais, mas ela não foi usada na base nacional."
    )
    equation(doc, "Equação 34", "FVP(i,n) = [1−(1+i)⁻ⁿ]/i")
    equation(doc, "Equação 35", "VPL(i) = −CAPEXUF + L·FVP(i,20)")
    equation(doc, "Equação 36", "Paybacksimples = CAPEXUF/L, se L>0; 99 caso contrário")
    equation(doc, "Equação 37", "Retorno anual simples (%) = 100·L/CAPEXUF")
    equation(doc, "Equação 38", "LCOW = [CAPEXUF+OPEXano·FVP(0,06;20)]/[Vpl,ano·FVP(0,06;20)]")

    doc.add_heading("2.5. Análise ambiental", level=2)
    doc.add_paragraph(
        "A avaliação ambiental do conjunto nacional é um balanço de carbono de triagem, com fronteira de fabricação simplificada mais operação "
        "por 20 anos. O inventário massivo atribui 0,045 kg de PEAD por litro de cisterna, fator de 1,9 kg CO₂e/kg de PEAD, 45 kg CO₂e ao "
        "conjunto de bombeamento e 35 kg CO₂e às tubulações. O crédito operacional é 0,35 kg CO₂e por m³ de água potável evitada; "
        "o débito elétrico é 0,08 kg CO₂e/kWh. A cloração entra no custo, mas não no balanço de carbono do runner nacional."
    )
    equation(doc, "Equação 39", "mPEAD = 0,045 · Vinf")
    equation(doc, "Equação 40", "CO₂inc = 1,9·mPEAD + 45 + 35")
    equation(doc, "Equação 41", "CO₂op,evitado = 0,35·Vpl,ano − 0,08·Epump,ano")
    equation(doc, "Equação 42", "CO₂líq,20 = 20·CO₂op,evitado − CO₂inc")
    doc.add_paragraph(
        "O ótimo ambiental é o volume com maior CO₂líq,20 dentro das 12 alternativas do mesmo perfil. Valores negativos significam que o crédito "
        "operacional em 20 anos não compensa o impacto inicial representado. Não foram modelados transporte real, substituição de equipamentos, "
        "fim de vida, escassez hídrica, eutrofização ou toxicidade. Portanto, o indicador não constitui ACV multicategoria conforme ISO 14040/14044."
    )
    doc.add_paragraph(
        "Para aplicações locais, o núcleo ACV completo permite substituir o inventário agregado por massas de reservatórios, fatores por material, "
        "comprimentos e diâmetros de tubos, número e potência de bombas, eletricidade calculada pela simulação e dosagem de cloro. Suas relações "
        "gerais, apresentadas no apêndice, não foram confundidas com a formulação efetivamente usada para gerar os resultados nacionais."
    )

    doc.add_heading("2.6. Modelo matemático de otimização TOPSIS", level=2)
    doc.add_paragraph(
        "Foram comparadas quatro regras de escolha: ótimo técnico pelo limiar da Equação 23; ótimo econômico pelo maior VPL a 6% a.a.; "
        "ótimo ambiental pelo maior saldo de carbono em 20 anos; e compromisso TOPSIS. O TOPSIS efetivamente aplicado ao runner nacional possui "
        "cinco critérios: economia potencial (benefício, peso 0,25), VPL a 6% (benefício, 0,25), CO₂ líquido em 20 anos (benefício, 0,20), "
        "percentual de dias com atendimento integral (benefício, 0,15) e CAPEX (custo, 0,15). Esta especificação substitui a descrição anterior, "
        "incorreta, de três critérios equiponderados."
    )
    equation(doc, "Equação 43", "rᵢⱼ = xᵢⱼ / √(Σₖxₖⱼ²);   vᵢⱼ = wⱼ·rᵢⱼ")
    equation(doc, "Equação 44", "Aⱼ⁺=maxᵢ(vᵢⱼ), Aⱼ⁻=minᵢ(vᵢⱼ) para benefício; inverso para CAPEX")
    equation(doc, "Equação 45", "Dᵢ⁺=√[Σⱼ(vᵢⱼ−Aⱼ⁺)²];   Dᵢ⁻=√[Σⱼ(vᵢⱼ−Aⱼ⁻)²]")
    equation(doc, "Equação 46", "Cᵢ = Dᵢ⁻/(Dᵢ⁺ + Dᵢ⁻),  0 ≤ Cᵢ ≤ 1")
    equation(doc, "Equação 47", "Vót,TOPSIS = arg maxᵢ(Cᵢ)")
    doc.add_paragraph(
        "A normalização é vetorial dentro de cada perfil de 12 volumes; normas inferiores a 10⁻⁹ são substituídas por 1. O ideal positivo usa "
        "o máximo nas quatro colunas de benefício e o mínimo no CAPEX; o anti-ideal usa a regra inversa. Se Dᵢ⁺+Dᵢ⁻≤10⁻⁹, atribui-se "
        "Cᵢ=0,5. O ranking ordena Cᵢ de forma decrescente. Como o TOPSIS é compensatório, um mau desempenho pode ser compensado por outro; por "
        "isso o artigo também reporta os ótimos isolados e recomenda sensibilidade de pesos."
    )
    doc.add_paragraph(
        "Reprodutibilidade. O pipeline parte dos CSVs diários e do catálogo tarifário, executa o balanço, calcula faturas, custos, finanças, carbono "
        "e TOPSIS por perfil, grava os resultados em Parquet e gera estatísticas e figuras. As constantes, tabelas de custos, aliases de prestadores, "
        "URLs primárias e regras de confiança permanecem em arquivos versionáveis. O Apêndice J lista entradas e scripts; o Apêndice C inclui as "
        "equações gerais adicionais do núcleo, testes de sanidade e diferenças deliberadas entre o motor genérico e o experimento nacional."
    )

    doc.add_heading("3. Resultados", level=1)
    doc.add_heading("3.1. Variação histórico–futuro", level=2)
    doc.add_paragraph(
        "No SSP5-8.5, a média municipal entre GCMs, cinco tipologias e todos os volumes diminui em todas as macrorregiões entre 1980–2013 e 2075–2100. "
        "O Norte apresenta a maior redução relativa (31,7%) e o Sul a menor (16,0%). Esses valores não pertencem a uma tipologia isolada nem somente "
        "ao ótimo TOPSIS; representam a agregação explicitada na legenda."
    )
    add_table(doc, ["Região", "Histórico (%)", "Far SSP5-8.5 (%)", "Δ relativo"], [(r, f"{h:.2f}", f"{f:.2f}", f"{d:.1f}%") for r,h,f,d in CLIMATE_REGIONS], [2200, 2200, 2700, 2260])
    add_figure(doc, "fig17_climate_potential_degradation_map.png", "Figura 1. Histórico (1980–2013) versus Far Future (2075–2100), SSP5-8.5. Média entre GCMs, cinco tipologias e todos os volumes; o delta não representa uma tipologia isolada.")

    doc.add_heading("3.2. Reservatórios ótimos", level=2)
    doc.add_paragraph(
        "O volume mediano TOPSIS é 7,5 m³ para UTI, UTG, MSG e MFH e 15 m³ para MFL. A coincidência de medianas não implica igualdade de curvas: as "
        "tipologias diferem em demanda, área de cobertura, VPL, carbono e frequência de seleção. O ótimo técnico tende a ser menor; o econômico e o "
        "ambiental podem deslocar-se para volumes maiores quando o uso absoluto compensa o custo incremental."
    )
    add_figure(doc, "fig7_optimal_storage_boxplots_grid_2x5.png", "Figura 2. Frequência relativa dos volumes ótimos TOPSIS. Condições: cinco tipologias separadas, cenários SSP e horizontes indicados em cada painel; resultados entre GCMs agregados por frequência.")

    doc.add_heading("3.3. Resultados financeiros", level=2)
    fin_rows = [(c, f"{s:.2f}%", f"{v/1000:.1f}", currency(vpl), f"{pb:.2f}") for c,s,v,vpl,pb,_ in NATIONAL_RESULTS]
    add_table(doc, ["Tipo", "Economia média", "Volume mediano (m³)", "VPL médio", "Payback mediano (anos)"], fin_rows, [1100, 1900, 2100, 2200, 2060])
    doc.add_paragraph(
        "UTI apresenta VPL médio negativo, enquanto MFL alcança o maior VPL médio. A escala aumenta o uso absoluto e dilui parte dos custos fixos, mas "
        "a eficiência percentual cai porque a demanda cresce mais rapidamente que a área de cobertura. Tarifas de esgoto, número de economias e parcela "
        "fixa alteram substancialmente o benefício e explicam parte da dispersão entre cidades."
    )
    add_figure(doc, "fig10_financial_payback_capex.png", "Figura 3. Viabilidade financeira no volume ótimo TOPSIS. Condições: cinco tipologias, vida útil de 20 anos, payback descontado a 6% a.a. e projeções climáticas agregadas.")

    doc.add_heading("3.4. Resultados ambientais", level=2)
    env_rows = [(c, f"{co2:.0f}", "crédito" if co2 >= 0 else "dívida") for c,_,_,_,_,co2 in NATIONAL_RESULTS]
    add_table(doc, ["Tipo", "CO₂ líquido médio em 20 anos (kg)", "Interpretação"], env_rows, [1800, 4200, 3360])
    doc.add_paragraph(
        "UTI mantém dívida média de carbono em 20 anos; UTG é próxima da neutralidade e as tipologias coletivas apresentam créditos crescentes. A MFL "
        "atinge o maior benefício absoluto. O resultado é sensível à massa real do reservatório, substituições, transporte, matriz elétrica e emissões "
        "do sistema público de água, fatores que devem ser refinados em ACV específica de projeto."
    )
    add_figure(doc, "matriz_multitipologia_co2_otimo_27_capitais.png", "Figura 4. CO₂ líquido no ótimo ambiental das 27 capitais. Condições: tipologias e capitais identificadas na matriz, vida útil de 20 anos e fatores de carbono do inventário simplificado.")

    doc.add_heading("3.5. Comparação entre capitais", level=2)
    top = capital.nlargest(5, "vpl")
    bottom = capital.nsmallest(5, "vpl")
    rows = []
    for label, frame in [("Maiores VPL", top), ("Menores VPL", bottom)]:
        for _, r in frame.iterrows():
            rows.append((label, f"{r.city}/{r.uf}", r.regiao, f"{r.volume/1000:.1f}", currency(r.vpl), f"{r.economia:.2f}%", f"{r.co2:.0f}"))
    add_table(doc, ["Grupo", "Capital", "Região", "Vol. mediano (m³)", "VPL médio", "Economia", "CO₂ (kg)"], rows, [1300, 1600, 1200, 1500, 1500, 1100, 1160], 7.6)
    doc.add_paragraph(
        "A comparação confirma que o ranking não é puramente climático: tarifa de água e esgoto, custo regional, energia e escala interagem com a "
        "disponibilidade de chuva. Uma capital pode ter boa eficiência física e retorno limitado, ou retorno elevado apesar de economia percentual "
        "modesta. A recomendação local deve abrir cada componente e consultar o grau de confiança tarifária."
    )
    add_figure(doc, "matriz_multitipologia_vpl_otimo_27_capitais.png", "Figura 5. VPL no ótimo econômico das 27 capitais. Condições: cinco tipologias, TMA de 6% a.a., vida útil de 20 anos e tarifas/custos locais do banco de entrada.")

    doc.add_heading("4. Discussão", level=1)
    doc.add_heading("4.1. Políticas públicas", level=2)
    doc.add_paragraph(
        "Programas de incentivo devem priorizar situações em que vulnerabilidade hídrica, benefício coletivo e viabilidade convergem. Subsídios uniformes "
        "por volume podem induzir superdimensionamento; instrumentos mais eficientes vinculam apoio ao desempenho verificado, à demanda não potável, à "
        "manutenção e à redução de pressão sobre o sistema público. A tarifa social e a cobrança efetiva de esgoto precisam ser tratadas separadamente "
        "para evitar atribuir benefício financeiro inexistente a famílias ou imóveis não conectados."
    )
    doc.add_heading("4.2. Considerações técnicas e de simulação", level=2)
    doc.add_paragraph(
        "O modelo conserva massa e permite comparação nacional, mas depende da qualidade da precipitação, demanda, first flush, coeficiente de escoamento "
        "e cobertura. A média entre GCMs não representa certeza e pode ocultar extremos. Financeiramente, usar a primeira faixa como tarifa linear é "
        "inadequado; ambientalmente, o balanço de carbono simplificado não substitui inventário de obra. O TOPSIS deve ser acompanhado pelos ótimos "
        "isolados, fronteira de Pareto e sensibilidade dos pesos."
    )
    doc.add_heading("4.3. Sugestões para adaptação às mudanças climáticas", level=2)
    for text in [
        "dimensionar por cidade, tipologia e nível de serviço, testando múltiplos GCMs e não apenas a média;",
        "combinar reservação com redução de demanda, dispositivos eficientes e operação sazonal;",
        "adotar sistemas modulares ou possibilidade de expansão quando a incerteza futura for alta;",
        "preservar extravasamento seguro e integração com drenagem urbana para eventos intensos;",
        "reavaliar tarifas, matriz elétrica e desempenho observado em ciclos regulares de operação.",
    ]:
        bullet(doc, text)

    doc.add_heading("5. Conclusão", level=1)
    doc.add_paragraph(
        "Não existe um único volume ótimo independente do objetivo. A solução técnica privilegia rendimentos marginais, a econômica maximiza VPL, a "
        "ambiental maximiza o saldo de carbono e o TOPSIS busca compromisso. Tipologias coletivas apresentam maior benefício absoluto e melhor desempenho "
        "ambiental, enquanto UTI lidera a economia percentual, mas frequentemente não recupera CAPEX ou carbono em 20 anos. O SSP5-8.5 reduz o potencial "
        "agregado em todas as regiões no fim do século, reforçando a necessidade de dimensionamento adaptativo. A base tarifária deve permanecer viva: "
        "atos vencidos, transições de concessionária e valores não reconciliados precisam entrar como incerteza, não como precisão aparente."
    )

    doc.add_heading("6. Declarações editoriais", level=1)
    for label, value in [
        ("Contribuições dos autores (CRediT)", "[Inserir as contribuições individuais de cada autor.]"),
        ("Financiamento", "[Inserir agência, número do processo e beneficiário; ou declarar ausência de financiamento específico.]"),
        ("Conflitos de interesse", "Os autores declaram que não há conflitos de interesse conhecidos que possam ter influenciado este trabalho. [Confirmar antes da submissão.]"),
        ("Disponibilidade de dados e código", "[Inserir repositório, DOI, licença e eventuais restrições de acesso.]"),
        ("Agradecimentos", "[Inserir agradecimentos, se aplicável.]"),
    ]:
        p = doc.add_paragraph()
        set_run(p.add_run(f"{label}. "), bold=True)
        p.add_run(value)

    doc.add_heading("7. Referências", level=1)
    refs = list(SOURCES) + [
        ("ANA", "Lista positiva da Tarifa Social de Água e Esgoto.", "https://www.gov.br/ana/pt-br/assuntos/saneamento-basico/tarifa-social-de-agua-e-esgoto/lista-positiva/lista-positiva-1"),
        ("EMBASA/AGERSA", "Tabela tarifária residencial de 2026, vigente desde 20/07/2026.", "https://www.embasa.ba.gov.br/w/tarifas-2026"),
        ("CORSAN/AGERGS", "Sistema e tabelas tarifárias de 2026.", "https://www.corsan.com.br/sistematarifario/"),
        ("SANESUL/AGEMS", "Evolução e estrutura tarifária de 2026.", "https://www.sanesul.ms.gov.br/evolucao-tarifaria"),
        ("AGRESE", "Estruturas tarifárias autorizadas de saneamento.", "https://agrese.se.gov.br/estrutura-tarifaria-autorizada/"),
        ("MRAE-PI", "Contrato e identificação da concessionária Águas do Piauí.", "https://mrae.sead.pi.gov.br/institucional/governanca/concessionaria-aguas-do-piaui/"),
    ]
    for i, (org, desc, url) in enumerate(refs, 1):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_after = Pt(4)
        set_run(p.add_run(f"[{i}] {org}. "), bold=True)
        p.add_run(f"{desc} {url}")

    doc.save(ARTICLE)


def build_appendices(tariffs, opt, capital, costs):
    doc = Document()
    configure(doc, "Apêndices técnicos | Netuno 5")
    cover(
        doc,
        "Material suplementar",
        "Apêndices técnicos do estudo Netuno 5",
        "Premissas, tipologias, tarifas, custos, inventários, otimizações e rastreabilidade",
        "Documento complementar ao artigo científico | agosto de 2026",
    )

    doc.add_heading("Apêndice A. Escopo e tipologias", level=1)
    rows = [(c, n, hab, f"{area:.2f}", f"{dem}", f"{npot}") for c,n,hab,area,dem,npot in TYPOLOGIES]
    add_table(doc, ["Código", "Tipologia", "Moradores", "Cobertura (m²)", "Demanda total (L/d)", "Não potável (L/d)"], rows, [900, 2800, 1100, 1400, 1700, 1460])
    doc.add_paragraph(
        "A escala cresce de uma residência térrea a um bloco de 128 moradores. O aumento da demanda é mais rápido que o aumento da área de cobertura, "
        "explicando a queda da eficiência percentual nas tipologias coletivas e, simultaneamente, o aumento do benefício absoluto."
    )

    doc.add_heading("Apêndice B. Matriz completa de premissas", level=1)
    premises = [
        ("Demanda", "Consumo per capita", "150", "L/(hab.dia)", "120 e 180"),
        ("Demanda", "Fração não potável", "40", "%", "30 e 50"),
        ("Clima", "Histórico", "1980–2013", "anos", "—"),
        ("Clima", "Near/Mid/Far", "2015–2040 / 2041–2070 / 2075–2100", "anos", "SSP2-4.5 e SSP5-8.5"),
        ("Clima", "Modelos", "19", "GCMs CMIP6", "avaliar dispersão"),
        ("Armazenamento", "Cisterna inferior", "0,5–50", "m³", "12 volumes"),
        ("Armazenamento", "Reservatório superior", "máx.(200 L; 10%)", "L", "editável"),
        ("Tubulações", "PVC DN 50 mm (recalque/distribuição)", "18,50", "R$/m", "SINAPI 89712 (+25% conexões)"),
        ("Tubulações", "PVC DN 75 mm (distribuição)", "28,00", "R$/m", "SINAPI 89713 (+25% conexões)"),
        ("Tubulações", "PVC DN 100 mm (prumada/captação)", "35,00", "R$/m", "SINAPI 89800 (+25% conexões)"),
        ("Tubulações", "PVC DN 150 mm (subcoletor)", "68,00", "R$/m", "SINAPI 89849 (+25% conexões)"),
        ("Tributação", "Impostos e encargos", "Inclusos", "—", "Todas as tarifas, CAPEX e OPEX consideram tributos"),
        ("Financeiro", "Vida útil", "20", "anos", "—"),
        ("Financeiro", "TMA", "6", "% a.a.", "10 e 14"),
        ("Operação", "Bombeamento", "0,45", "kWh/m³", "curva real da bomba"),
        ("Carbono", "Água evitada", "0,35", "kg CO₂e/m³", "sensibilidade"),
        ("Carbono", "Eletricidade", "0,08", "kg CO₂e/kWh", "série anual"),
        ("TOPSIS", "Pesos", "0,25; 0,25; 0,20; 0,15; 0,15", "economia; VPL; CO₂; atendimento; CAPEX", "análise de pesos"),
    ]
    add_table(doc, ["Grupo", "Parâmetro", "Base", "Unidade", "Sensibilidade"], premises, [1500, 2500, 2200, 1700, 1460])

    doc.add_heading("Apêndice C. Formulação expandida, equações do código e verificações", level=1)
    doc.add_paragraph(
        "As equações C.1–C.18 reproduzem a formulação efetivamente usada no estudo nacional. As equações C.19–C.35 documentam "
        "rotinas gerais disponíveis no núcleo Netuno 5 para projetos detalhados. Estas últimas não substituem silenciosamente as premissas do "
        "runner massivo; a distinção permite replicar tanto o artigo como casos locais executados pela interface."
    )
    for label, text in [
        ("C.1 Demanda total", "Dtot=Nhab·dpc; Dpl=fpl·Dtot"),
        ("C.2 Chuva útil", "Pef=I·max(P−FF,0)+(1−I)·P"),
        ("C.3 Captação", "Qₜ=Pef·A·C"),
        ("C.4 Disponibilidade", "Sₜ=Vₜ₋₁+Qₜ"),
        ("C.5 Extravasamento", "Oₜ=max(Sₜ−Vmax,0); Aₜ=min(Sₜ,Vmax)"),
        ("C.6 Consumo e estoque", "Uₜ=min(Dpl,Aₜ); Vₜ=Aₜ−Uₜ; Wₜ=Dtot−Uₜ"),
        ("C.7 Economia", "E=100·ΣUₜ/ΣDtot"),
        ("C.8 Anualização", "Vano=(365,25/1000)·(ΣₜVdiário,ₜ/T)"),
        ("C.9 Ganho marginal", "Δₖ=(Eₖ−Eₖ₋₁)/[(Vₖ−Vₖ₋₁)/1000]"),
        ("C.10 Fatura por faixas", "Fágua=N·[Ffixa+Σₖ max(0,min(q,bₖ)−aₖ)·tₖ]"),
        ("C.11 Benefício", "Bano=12·max[0,F(base)−F(residual)]"),
        ("C.12 Tubulações SINAPI", "Cpipes=1,25·Σd (Ld·cd)  [d ∈ {50, 75, 100, 150 mm}]"),
        ("C.13 CAPEX regionalizado", "CAPEXUF=fUF·(Cmateriais+max[Clabor,min;0,30·Cmateriais])"),
        ("C.14 OPEX regionalizado", "OPEX=(Cmaint,base·fUF)+0,45·Vpl,ano·Telec+0,05·Vpl,ano"),
        ("C.15 Fator presente", "FVP=[1−(1+i)⁻ⁿ]/i"),
        ("C.16 VPL", "VPL=−CAPEX+(Bano−OPEX)·FVP"),
        ("C.17 LCOW", "LCOW=[CAPEX+OPEX·FVP]/[Vpl,ano·FVP]"),
        ("C.18 Carbono nacional", "CO₂líq,20=20(0,35Vpl,ano−0,08Ebomba)−(0,045Vinf·1,9+45+35)"),
        ("C.19 TOPSIS", "Cᵢ=Dᵢ⁻/(Dᵢ⁺+Dᵢ⁻); w=(0,25;0,25;0,20;0,15;0,15)"),
        ("C.20 Energia detalhada", "trec=Vpump/q; tpart=Nstart·tstart; E=P(trec+tpart)/η"),
        ("C.21 Tarifa efetiva", "Teff=[F(Qbase)−F(Qbase−Qsave)]/Qsave"),
        ("C.22 Escalonamento", "fₘ=(1+g/100)^⌊(m−1)/k⌋"),
        ("C.23 Inflação", "finf,m=(1+πm)^(m−1)"),
        ("C.24 Fluxo mensal", "FCm=Bágua,m−Celec,m−Cmaint,m−CCl2,m"),
        ("C.25 VPL mensal", "VPL=−CAPEX+Σm FCm/(1+im)^m"),
        ("C.26 TIR mensal", "0=Σk FCk(1+r)⁻ᵏ"),
        ("C.27 Newton–Raphson", "rnew=r−f(r)/f′(r); f′(r)=Σk−kFCk(1+r)^(−k−1)"),
        ("C.28 TIR anual", "TIRaa=(1+rm)^12−1"),
        ("C.29 Massa do reservatório", "mtank=(V/1000)·ρmaterial"),
        ("C.30 Carbono do reservatório", "CO₂tank=mtank·EFmaterial"),
        ("C.31 Carbono de tubos", "CO₂pipes=ΣDN LDN·EFDN"),
        ("C.32 Carbono de bombas", "CO₂pump=Npump·EFpump"),
        ("C.33 Cloro anual", "mCl2=Vpl,ano·dose/1000"),
        ("C.34 Carbono do tratamento", "CO₂treat=Vpl,ano·dose·EFCl2/1000"),
        ("C.35 Saldo anual ACV completa", "CO₂net,ano=Vpl,ano·EFágua−Epump·EFrede−CO₂treat"),
        ("C.36 Payback ambiental", "PBenvironmental=CO₂inc/CO₂net,ano, se CO₂net,ano>0"),
    ]:
        equation(doc, label, text)
    doc.add_paragraph(
        "As verificações recomendadas incluem conservação de massa diária, monotonicidade da economia com demanda substituível, limites 0–100% para "
        "indicadores percentuais, VPL igual a −CAPEX quando não há benefício e escore TOPSIS no intervalo [0,1]."
    )

    doc.add_heading("Apêndice D. Comparação completa entre otimizações", level=1)
    opt_rows = []
    for _, r in opt.iterrows():
        opt_rows.append((r["criterio"], r["building_code"], f"{r['volume']/1000:.1f}", currency(r["vpl"]), f"{r['co2']:.0f}", f"{r['savings']:.2f}%"))
    add_table(doc, ["Critério", "Tipo", "Volume (m³)", "VPL", "CO₂ (kg)", "Economia"], opt_rows, [2600, 900, 1300, 1700, 1400, 1460], 7.6)
    add_figure(doc, "fig20_pareto_frontier_vpl_co2_payback.png", "Figura D.1. Síntese multicritério das soluções ótimas TOPSIS. Condições: cinco tipologias; cidades, cenários, horizontes e GCMs agregados.")

    doc.add_heading("Apêndice E. Auditoria tarifária e abordagem de confiança", level=1)
    counts = tariffs["confianca_global_grau"].str[0].value_counts()
    statuses = tariffs["energia_aneel_status_vigencia"].value_counts()
    detailed_count = pd.read_csv(ROOT / "tarifas" / "tarifas_detalhadas_auditadas.csv").shape[0]
    doc.add_paragraph(
        f"A base contém 652 municípios brasileiros e {detailed_count:,} registros detalhados por faixa de consumo. A rodada atual resultou em A={counts.get('A',0)}, B={counts.get('B',0)}, "
        f"C={counts.get('C',0)} e D={counts.get('D',0)}. Há {statuses.get('VIGENTE',0)} referências elétricas vigentes homologadas pela ANEEL. "
        "A seleção de estado e município na interface do usuário carrega automaticamente as faixas de água, a alíquota oficial de esgoto da concessionária "
        "e a tarifa elétrica B1, mantendo hiperlink direto para a publicação regulatória original de onde os dados foram extraídos."
    )
    add_table(doc, ["Componente", "Peso/pontos", "Regra"], [
        ("Saneamento no escore global", "60%", "Rubrica abaixo; penalizações por fallback e transição não reconciliada."),
        ("Autoridade/especificidade", "35", "Tabela/ato específico > página institucional > fonte sem URL."),
        ("Atualidade", "20", "2026/2027 > 2025 > 2023/2024 > sem data."),
        ("Conciliação numérica", "25", "SIM, PENDENTE ou NÃO; página oficial não prova o valor."),
        ("Completude", "15", "Faixas, parcela fixa e esgoto."),
        ("Operador", "5", "Prestador atual e agência reguladora coerentes."),
        ("Energia no escore global", "40%", "ANEEL vigente recebe maior escore; ato expirado é penalizado."),
    ], [2600, 1500, 5260])
    low = tariffs[tariffs["confianca_global_grau"].str.startswith("C")]
    if low.empty:
        doc.add_paragraph("Nenhum município recebeu grau global C na rodada de auditoria atual.")
    else:
        add_table(doc, ["Município", "UF", "Prestador atual", "Escore global", "Pendência"], [(r.municipio, r.uf, r.prestador_saneamento, f"{r.confianca_global_score:.1f}", r.alerta_auditoria_saneamento) for _,r in low.iterrows()], [1500, 600, 1800, 1200, 4260], 7.6)
    doc.add_paragraph(
        "Correções desta rodada: inclusão dos aliases Equatorial Pará, CELESC e Sulgipe; atualização da antiga Energisa Minas Gerais para Energisa Minas "
        "Rio; correção do operador do Piauí para Águas do Piauí; e conciliação faixa a faixa da EMBASA 2026, incluindo a separação das faixas "
        "21–25 e 26–30 m³. Cada registro mantém fonte primária, tipo de evidência, reconciliação, alerta e fontes cruzadas."
    )

    doc.add_heading("Apêndice F. CAPEX, OPEX e diferenças regionais", level=1)
    doc.add_paragraph(
        "Os Fatores Regionais SINAPI/CUB por Unidade Federativa (fUF) expressam a ponderação de 55% materiais da construção civil, 30% mão de obra "
        "local especializada e 15% logística e frete interestadual. Esses coeficientes atuam diretamente sobre o investimento inicial (CAPEX) e "
        "sobre a manutenção periódica anual (OPEX fixo):"
    )
    factors = costs["regional_factors_by_uf"]
    add_table(doc, ["UF", "Fator (SP=1,00)", "Diferença", "Justificativa Regional SINAPI/CUB"], [
        (uf, f"{v:.2f}", f"{(v-1)*100:+.0f}%",
         "Custos logísticos elevados de frete e transporte fluvial/aéreo" if v >= 1.15 else
         "Encargos locais e mão de obra civil qualificada acima da média" if v >= 1.05 else
         "Custo de vida e CUB regional ligeiramente superior" if v > 1.00 else
         "Estado referência base de distribuição fabril nacional" if v == 1.00 else
         "Proximidade de polos fabris e cadeias de suprimento" if v >= 0.97 else
         "Custos médios de mão de obra SINAPI desonerada menores"
        ) for uf,v in sorted(factors.items())
    ], [800, 1500, 1200, 5860], 7.4)

    doc.add_paragraph(
        "Para a rede hidráulica predial, os custos unitários de tubulações em PVC foram pesquisados e calibrados a partir das composições oficiais do SINAPI/Caixa:"
    )
    add_table(doc, ["Diâmetro Nominal", "Aplicação Predial", "Insumo Base SINAPI", "Custo c/ Conexões (+25%)", "Composição SINAPI de Referência"], [
        ("DN 50 mm (2\")", "Recalque, barrilete e distribuição", "R$ 18,50 / m", "R$ 23,12 / m", "Composição 89712 / AF_08/2022"),
        ("DN 75 mm (3\")", "Distribuição secundária e ventilação", "R$ 28,00 / m", "R$ 35,00 / m", "Composição 89713 / AF_08/2022"),
        ("DN 100 mm (4\")", "Captação, prumadas e extravasor", "R$ 35,00 / m", "R$ 43,75 / m", "Composição 89800 / AF_08/2022"),
        ("DN 150 mm (6\")", "Coletores pluviais de grande porte", "R$ 68,00 / m", "R$ 85,00 / m", "Composição 89849 / AF_08/2022"),
    ], [1500, 2600, 1500, 1700, 2060], 7.4)

    econ = opt[opt["criterio"].astype(str).str.startswith("Econômico")]
    capex_rows = []
    for _, r in econ.iterrows():
        result = estimate_calibrated_capex_opex(r["building_code"], r["volume"], "SP", 0.84)
        capex_rows.append((r["building_code"], f"{r['volume']/1000:.1f}", currency(result["c_inf"]), currency(result["c_pump"]), currency(result["c_pipes"]), currency(result["labor_cost"]), currency(result["capex_total_brl"])))
    add_table(doc, ["Tipo", "Vol. (m³)", "Cisterna", "Bombas", "Tubos", "Mão de obra", "CAPEX SP"], capex_rows, [800, 1100, 1500, 1300, 1300, 1600, 1760], 7.4)
    doc.add_paragraph(
        "Os fatores variam de 0,93 a 1,21, diferença aproximada de 30% entre extremos. São fatores de pré-dimensionamento baseados em materiais, mão de "
        "obra e logística; devem ser substituídos por orçamento executivo e referências SINAPI/CUB locais."
    )

    doc.add_heading("Apêndice G. Inventário ambiental e limitações da ACV", level=1)
    add_table(doc, ["Item", "Fator", "Unidade", "Limitação"], [
        ("PEAD", "45 × 1,9", "kg/m³ × kg CO₂e/kg", "Massa genérica por volume"),
        ("Bomba", "45", "kg CO₂e/sistema", "Não varia por potência no runner massivo"),
        ("Tubos", "35", "kg CO₂e/sistema", "Não varia por comprimento/diâmetro no runner massivo"),
        ("Água evitada", "0,35", "kg CO₂e/m³", "Depende do sistema público local"),
        ("Eletricidade", "0,08", "kg CO₂e/kWh", "Matriz varia no tempo"),
        ("Bombeamento", "0,45", "kWh/m³", "Substituir por curva e altura manométrica"),
        ("Vida útil", "20", "anos", "Sem reposição completa e fim de vida"),
    ], [1900, 1600, 2500, 3360])
    doc.add_paragraph(
        "Sincronização Física entre CAPEX e ACV: No núcleo interativo do Netuno 5, os comprimentos de tubulações informados na análise econômica "
        "(DN 50, 75, 100 e 150 mm) são compartilhados bidirecionalmente com o módulo de ACV. Dessa forma, a quantidade física de tubos empregada no "
        "orçamento orçamentário reflete com exatidão a massa e o impacto incorporado de carbono no inventário de ciclo de vida."
    )
    doc.add_paragraph(
        "Categorias não cobertas no runner nacional: escassez hídrica, eutrofização, toxicidade, uso do solo, transporte real, manutenção detalhada, substituições e fim de "
        "vida. O balanço é apropriado para triagem comparativa, não para declaração ambiental de produto ou afirmação multicategoria definitiva."
    )

    doc.add_heading("Apêndice H. Clima, cenários e incerteza inter-GCM", level=1)
    add_table(doc, ["Período", "Anos", "Cenários", "Agregação"], [
        ("Histórico", "1980–2013", "observado/referência", "cidade e tipologia"),
        ("Near Future", "2015–2040", "SSP2-4.5; SSP5-8.5", "19 GCMs"),
        ("Mid Future", "2041–2070", "SSP2-4.5; SSP5-8.5", "19 GCMs"),
        ("Far Future", "2075–2100", "SSP2-4.5; SSP5-8.5", "19 GCMs"),
    ], [2100, 1900, 3000, 2360])
    add_figure(doc, "fig5_gcm_climate_model_uncertainty.png", "Figura H.1. Incerteza inter-GCM entre 19 modelos CMIP6. Condições: cinco tipologias e volumes ótimos TOPSIS agregados; dispersão municipal indicada por desvio-padrão e coeficiente de variação.")

    doc.add_heading("Apêndice I. Resultados nacionais detalhados", level=1)
    add_table(doc, ["Tipo", "Economia média", "Volume mediano", "VPL médio", "Payback", "CO₂ líquido"], [(c, f"{s:.2f}%", f"{v/1000:.1f} m³", currency(n), f"{p:.2f} anos", f"{co2:.0f} kg") for c,s,v,n,p,co2 in NATIONAL_RESULTS], [1100, 1500, 1700, 1900, 1500, 1660])
    add_figure(doc, "fig9_regional_macro_analysis.png", "Figura I.1. Desempenho macrorregional por tipologia. Condições: soluções ótimas TOPSIS e projeções climáticas agregadas.")
    add_figure(doc, "fig11_spatial_tariffs_distribution_brasil.png", "Figura I.2. Tarifas locais em 652 cidades. Pontos repetidos por solução ótima TOPSIS; cenários climáticos agregados; colormaps discretizados em bins.", width=5.25)
    add_figure(doc, "fig13_cost_benefit_breakdown_typologies.png", "Figura I.3. Custos e benefícios anuais por tipologia e macrorregião. Condições: volumes ótimos TOPSIS e projeções climáticas agregadas.", width=5.75)

    doc.add_heading("Apêndice J. Rastreabilidade e reprodução", level=1)
    for path, purpose in [
        ("tarifas/tarifas_detalhadas_auditadas.csv", "entrada canônica por faixa de saneamento"),
        ("tarifas/catalogo_tarifas_auditado_652.csv", "resumo municipal, tarifas de esgoto/energia e confiança"),
        ("scripts/audit_tariffs.py", "auditoria reproduzível de tarifas"),
        ("scripts/analyze_vaz_parquet.py", "figuras e estatísticas"),
        ("scripts/build_article_and_appendices.py", "geração dos documentos do artigo e apêndices"),
        ("netuno/data/costs_database.json", "base editável de custos, tubulações SINAPI e fatores regionais"),
    ]:
        bullet(doc, f"{path}: {purpose}.")
    doc.add_paragraph(
        "Antes de nova simulação, deve-se baixar novamente a base ANEEL, executar a auditoria, revisar linhas NÃO/PENDENTE do saneamento, atualizar custos e "
        "registrar a data de corte. Resultados locais exigem validação do prestador, cobertura de esgoto e número de economias do imóvel."
    )

    doc.save(APPENDICES)


def main():
    tariffs, sweep, opt, capital, costs = data_context()
    build_article(tariffs, opt, capital)
    build_appendices(tariffs, opt, capital, costs)
    print(f"Artigo: {ARTICLE}")
    print(f"Apêndices: {APPENDICES}")


if __name__ == "__main__":
    main()
