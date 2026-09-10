"""Gera a versão completa, organizada por capítulos, do artigo Netuno 5."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from netuno.core.cost_estimates import estimate_calibrated_capex_opex


OUTPUT = ROOT / "Artigo_Cientifico_5_Tipologias_Netuno5.docx"
TARIFFS = ROOT / "tarifas" / "catalogo_tarifas_auditado_652.csv"
SWEEP = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "capitais_varredura_completa.csv"
FIG_DIR = ROOT / "estudo_5_tipologias_residenciais" / "estudo_vaz" / "figuras"
COST_DB = ROOT / "netuno" / "data" / "costs_database.json"

TYPOLOGIES = [
    ("UTI", "Casa unifamiliar térrea", 4, 60.19, 600, 240),
    ("UTG", "Casa unifamiliar geminada", 8, 115.43, 1200, 480),
    ("MSG", "Sobrado multifamiliar geminado", 16, 132.53, 2400, 960),
    ("MFH", "Bloco multifamiliar H", 64, 158.70, 9600, 3840),
    ("MFL", "Bloco multifamiliar retangular", 128, 421.52, 19200, 7680),
]

NATIONAL_RESULTS = [
    ("UTI", 19.13, 7500, -4420.27, 12.09, -148.59),
    ("UTG", 17.13, 7500, 100.52, 10.99, 31.31),
    ("MSG", 12.00, 7500, 2158.86, 9.90, 206.08),
    ("MFH", 4.66, 7500, 305.76, 11.04, 545.00),
    ("MFL", 5.93, 15000, 22183.91, 8.23, 1727.58),
]

CLIMATE_REGIONS = [
    ("Norte", 17.60, 12.03, -31.7),
    ("Nordeste", 9.79, 7.18, -26.6),
    ("Centro-Oeste", 12.69, 9.31, -26.6),
    ("Sudeste", 12.81, 10.14, -20.8),
    ("Sul", 14.66, 12.31, -16.0),
]

SOURCES = [
    ("ANEEL", "Tarifas homologadas das distribuidoras, base vigente em 24/08/2026.", "https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4"),
    ("ANEEL", "Escopo do ranking: não inclui tributos, COSIP nem bandeiras.", "https://www.gov.br/aneel/pt-br/centrais-de-conteudos/relatorios-e-indicadores/tarifas-e-informacoes-economico-financeiras"),
    ("SINISA", "Resultados nacionais de água e esgoto e identificação de prestadores.", "https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa"),
    ("CAIXA/IBGE", "SINAPI: referência oficial para custos de obras e serviços de engenharia.", "https://www.caixa.gov.br/poder-publico/modernizacao-gestao/sinapi/Paginas/default.aspx"),
    ("IBGE", "Índices mensais e diferenças de custo da construção por UF.", "https://www.ibge.gov.br/estatisticas/economicas/precos-e-custos/9270-indice-nacional-da-construcao-civil.html"),
    ("Jesus et al. (2020)", "ACV energética de sistemas pluviais no semiárido brasileiro; construção dominante e ótimo de 1–2,5 m³.", "https://doi.org/10.1111/wej.12464"),
    ("Soares et al. (2023)", "Revisão sobre gestão pluvial e ACV.", "https://doi.org/10.3390/su151612133"),
    ("Modular LCA (2024)", "Comparação de sistema centralizado e híbrido no Brasil com ReCiPe 2016.", "https://www.sciencedirect.com/science/article/pii/S0048969723069085"),
]


def set_repeat_table_header(row):
    tr_pr = row._tr.get_or_add_trPr()
    tbl_header = OxmlElement("w:tblHeader")
    tbl_header.set(qn("w:val"), "true")
    tr_pr.append(tbl_header)


def shade(cell, fill):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def configure_document(doc):
    sec = doc.sections[0]
    sec.top_margin = Cm(2.2)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(2.3)
    sec.right_margin = Cm(2.3)
    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Aptos"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_after = Pt(6)
    normal.paragraph_format.line_spacing = 1.15
    for name, size, color in [("Heading 1", 16, "0F4C5C"), ("Heading 2", 13, "16697A"), ("Heading 3", 11.5, "334155")]:
        st = styles[name]
        st.font.name = "Aptos Display"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = RGBColor.from_string(color)
        st.paragraph_format.space_before = Pt(12)
        st.paragraph_format.space_after = Pt(6)
        st.paragraph_format.keep_with_next = True


def add_title(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(36)
    r = p.add_run("Desempenho técnico, econômico, ambiental e climático de sistemas prediais de aproveitamento de água de chuva no Brasil")
    r.bold = True
    r.font.name = "Aptos Display"
    r.font.size = Pt(21)
    r.font.color.rgb = RGBColor(15, 76, 92)
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r2 = p2.add_run("Cinco tipologias residenciais · 652 municípios · CMIP6 · Netuno 5")
    r2.font.size = Pt(13)
    r2.font.color.rgb = RGBColor(71, 85, 105)
    p3 = doc.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.add_run("Versão integral auditada — corte tarifário em 24 de agosto de 2026").italic = True
    doc.add_page_break()


def add_table(doc, headers, rows, widths=None, font_size=8.5):
    table = doc.add_table(rows=1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.style = "Table Grid"
    table.autofit = False
    hdr = table.rows[0]
    set_repeat_table_header(hdr)
    for i, text in enumerate(headers):
        cell = hdr.cells[i]
        cell.text = str(text)
        shade(cell, "DCEAF0")
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(font_size)
    for values in rows:
        cells = table.add_row().cells
        for i, value in enumerate(values):
            cells[i].text = "—" if value is None else str(value)
            cells[i].vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cells[i].paragraphs:
                p.paragraph_format.space_after = Pt(1)
                for run in p.runs:
                    run.font.size = Pt(font_size)
    if widths:
        for row in table.rows:
            for i, width in enumerate(widths):
                row.cells[i].width = Cm(width)
    return table


def add_bullets(doc, items):
    for item in items:
        p = doc.add_paragraph(style="List Bullet")
        p.add_run(item)


def add_figure(doc, filename, caption):
    path = FIG_DIR / filename
    if not path.exists():
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(path), width=Inches(6.35))
    shape._inline.docPr.set("descr", caption)
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.keep_together = True
    run = c.add_run(caption)
    run.bold = True
    run.font.size = Pt(9)


def optimization_table(sweep):
    keys = ["city", "building_code"]
    sweep = sweep.sort_values(keys + ["lower_tank_vol_l"]).copy()
    sweep["delta_marginal"] = sweep.groupby(keys)["potential_water_savings_pct"].diff() / (sweep.groupby(keys)["lower_tank_vol_l"].diff() / 1000.0)
    selected = []
    tech_pool = sweep[sweep["delta_marginal"] <= 2.5]
    tech_idx = tech_pool.groupby(keys)["lower_tank_vol_l"].idxmin()
    tech = sweep.loc[tech_idx].copy()
    tech["criterio"] = "Técnico Δ≤2,5 p.p./m³"
    selected.append(tech)
    for label, metric in [
        ("Econômico: maior VPL a 6%", "vpl_6pct_brl"),
        ("Ambiental: maior CO₂ líquido", "lifetime_net_co2_saved_kg"),
        ("TOPSIS: compromisso", "topsis_score"),
    ]:
        part = sweep.loc[sweep.groupby(keys)[metric].idxmax()].copy()
        part["criterio"] = label
        selected.append(part)
    out = pd.concat(selected)
    med = out.groupby(["criterio", "building_code"], observed=True).agg(
        volume=("lower_tank_vol_l", "median"), vpl=("vpl_6pct_brl", "median"),
        co2=("lifetime_net_co2_saved_kg", "median"), savings=("potential_water_savings_pct", "median")
    ).reset_index()
    order = ["Técnico Δ≤2,5 p.p./m³", "Econômico: maior VPL a 6%", "Ambiental: maior CO₂ líquido", "TOPSIS: compromisso"]
    med["criterio"] = pd.Categorical(med["criterio"], order, ordered=True)
    med["building_code"] = pd.Categorical(med["building_code"], [x[0] for x in TYPOLOGIES], ordered=True)
    return med.sort_values(["criterio", "building_code"])


def fmt_currency(v):
    return f"R$ {v:,.0f}".replace(",", ".")


def build():
    tariffs = pd.read_csv(TARIFFS, encoding="utf-8-sig")
    sweep = pd.read_csv(SWEEP, sep=";")
    costs = json.loads(COST_DB.read_text(encoding="utf-8"))
    opt = optimization_table(sweep)

    doc = Document()
    configure_document(doc)
    add_title(doc)

    doc.add_heading("Resumo", level=1)
    doc.add_paragraph(
        "Este estudo avalia sistemas prediais de aproveitamento de água de chuva em cinco tipologias residenciais, "
        "652 municípios brasileiros, 19 modelos climáticos globais e quatro horizontes temporais. A análise integra "
        "balanço hídrico diário, descarte inicial, energia de bombeamento, tarifas progressivas, CAPEX/OPEX regionalizados, "
        "VPL, payback, custo nivelado da água e um balanço simplificado de carbono. O banco massivo contém 327.786.480 "
        "simulações; as estatísticas nacionais publicadas derivam de amostra estratificada de 350.000 execuções, enquanto "
        "a comparação entre critérios de otimização usa a varredura completa das 27 capitais (1.620 combinações)."
    )
    doc.add_paragraph(
        "Os resultados mostram que o critério de projeto altera materialmente a capacidade recomendada. O ótimo econômico "
        "favorece volumes menores em UTI/UTG/MSG, o ambiental aproxima-se do econômico em várias tipologias e o TOPSIS "
        "preserva maior segurança hídrica às custas de algum VPL. A heterogeneidade tarifária e de CAPEX é tão importante "
        "quanto a precipitação. Sob SSP5-8.5, a comparação histórico–2075/2100 indica redução agregada do potencial em todas "
        "as macrorregiões. A auditoria tarifária classificou 236 municípios com confiança A, 334 B, 81 C e 1 D."
    )
    doc.add_paragraph("Palavras-chave: água de chuva; dimensionamento; VPL; TOPSIS; ACV; CMIP6; tarifas; resiliência climática.")

    doc.add_heading("Capítulo 1 — Escopo, perguntas e arquitetura do estudo", level=1)
    doc.add_paragraph(
        "A pergunta central é qual capacidade de cisterna oferece o melhor compromisso entre economia de água potável, "
        "retorno financeiro, redução líquida de carbono e confiabilidade, considerando que clima, tarifas e custos construtivos "
        "variam no território. O estudo não pressupõe um único ‘volume ótimo’: define quatro ótimos com funções-objetivo distintas."
    )
    add_table(doc, ["Código", "Tipologia", "Habitantes", "Telhado (m²)", "Demanda total (L/d)", "Demanda pluvial (L/d)"], TYPOLOGIES, [1.3, 4.1, 1.6, 1.8, 2.1, 2.1])
    add_bullets(doc, [
        "Demanda per capita de referência: 150 L/(hab.dia), com sensibilidades de 120 e 180 L/(hab.dia).",
        "Fração não potável de referência: 40%, com sensibilidades de 30% e 50%.",
        "Volumes inferiores avaliados: 0,5; 1; 2; 3; 5; 7,5; 10; 15; 20; 30; 40 e 50 m³.",
        "Reservatório superior: máximo entre 200 L e 10% do volume inferior.",
        "Vida útil econômica e ambiental: 20 anos; taxas de desconto: 6%, 10% e 14% a.a.",
    ])

    doc.add_heading("Capítulo 2 — Balanço hídrico, clima e cenários", level=1)
    doc.add_paragraph(
        "O motor executa balanço diário de massa. A chuva efetiva é o produto da precipitação, área de cobertura e coeficiente "
        "de escoamento, descontado o first flush. O volume disponível é limitado pela cisterna; o atendimento é limitado pela "
        "demanda não potável; excedentes são contabilizados como extravasamento. Essa resolução diária preserva estiagens, "
        "sequência de eventos e saturação, fenômenos perdidos em médias mensais."
    )
    add_table(doc, ["Horizonte", "Período", "Cenário", "Uso"], [
        ("Histórico", "1980–2013", "Observado/CMIP6 histórico", "Referência"),
        ("Near", "2015–2044", "SSP2-4.5 e SSP5-8.5", "Curto prazo"),
        ("Middle", "2045–2074", "SSP2-4.5 e SSP5-8.5", "Meados do século"),
        ("Far", "2075–2100", "SSP2-4.5 e SSP5-8.5", "Fim do século"),
    ], [2.0, 2.2, 4.1, 3.4])
    doc.add_paragraph(
        "First flush foi avaliado sem descarte, com 2 ou 4 mm e três lógicas: em todo evento; após ao menos um dia seco; "
        "e após sete dias secos. A última reduz perdas em eventos consecutivos, mas sua escolha deve respeitar qualidade da água, "
        "uso final e manutenção."
    )

    doc.add_heading("Capítulo 3 — Comparação entre otimizações", level=1)
    doc.add_paragraph(
        "O ótimo técnico é o menor volume cujo ganho marginal cai para até 2,5 pontos percentuais de economia por m³ adicional. "
        "O econômico maximiza o VPL a 6% a.a.; o ambiental maximiza o saldo de CO₂ em 20 anos; e o TOPSIS normaliza economia, "
        "VPL, CO₂, confiabilidade e CAPEX para selecionar um compromisso. Portanto, chamar qualquer um deles simplesmente de "
        "‘volume ótimo’ sem informar o critério é incorreto."
    )
    rows = []
    for _, r in opt.iterrows():
        rows.append((str(r["criterio"]), str(r["building_code"]), f"{r['volume']/1000:.1f}", fmt_currency(r["vpl"]), f"{r['co2']:.0f}", f"{r['savings']:.1f}%"))
    add_table(doc, ["Critério", "Tipo", "Volume mediano (m³)", "VPL mediano", "CO₂ mediano (kg)", "Economia mediana"], rows, [4.0, 1.2, 2.1, 2.2, 2.1, 2.0], 7.8)
    doc.add_paragraph(
        "A tabela usa 27 capitais × cinco tipologias × 12 volumes. O critério técnico pode selecionar volumes pequenos nas "
        "tipologias de alta densidade porque o ganho marginal inicial já é baixo; isso não significa que maximiza economia, "
        "VPL ou carbono. O TOPSIS é preferível quando nenhum indicador pode dominar sozinho, mas seus pesos devem ser publicados."
    )
    add_figure(doc, "fig20_pareto_frontier_vpl_co2_payback.png", "Figura 1 — Soluções TOPSIS e relações entre VPL, CO₂, confiabilidade e parâmetros. Condições: volumes ótimos TOPSIS; cinco tipologias e projeções climáticas agregadas.")

    doc.add_heading("Capítulo 4 — Tarifas de água, esgoto e energia", level=1)
    doc.add_paragraph(
        "A conta de saneamento é não linear. O benefício anual foi calculado pela diferença entre a fatura sem e com substituição "
        "pluvial, aplicando tarifa fixa/TBO/TFDI, blocos progressivos e esgoto. A parcela fixa cancela-se somente quando permanece "
        "inalterada nos dois cenários. Em edifícios, o volume deve ser dividido pelo número regulatório de economias antes do "
        "enquadramento em faixas. Usar apenas a tarifa do primeiro bloco distorce o benefício."
    )
    region_tar = tariffs.groupby("regiao", observed=True).agg(
        cidades=("municipio", "count"), agua_mediana=("tarifa_agua_primeira_faixa_r_m3", "median"),
        fixa_mediana=("tarifa_fixa_agua_r_mes", "median"), esgoto_mediano=("esgoto_pct_sobre_agua", "median"),
        energia_mediana=("energia_modelo_referencia_aneel_sem_tributos_r_kwh", "median"),
        confianca=("confianca_global_score", "mean")
    ).reset_index()
    rows = [(r.regiao, int(r.cidades), f"{r.agua_mediana:.2f}", f"{r.fixa_mediana:.2f}", f"{r.esgoto_mediano:.0f}%", f"{r.energia_mediana:.4f}", f"{r.confianca:.1f}") for _, r in region_tar.iterrows()]
    add_table(doc, ["Região", "Cidades", "Água mediana (R$/m³)", "Fixa mediana (R$/mês)", "Esgoto", "Energia ANEEL (R$/kWh)", "Confiança"], rows, [2.3, 1.2, 2.3, 2.3, 1.4, 2.3, 1.6], 7.4)
    doc.add_paragraph(
        "A tarifa elétrica é a soma TUSD + TE homologada pela ANEEL para B1 residencial convencional e não inclui ICMS, "
        "PIS/Cofins, COSIP nem bandeiras. Em 572 municípios houve conciliação automática exata com a base vigente. A auditoria "
        "classificou 236 municípios A, 334 B, 81 C e Gaspar/SC como D; este último exige validação manual antes de decisão local."
    )
    add_figure(doc, "fig11_spatial_tariffs_distribution_brasil.png", "Figura 2 — Distribuição tarifária. Condições: 652 municípios; pontos vinculados às soluções ótimas TOPSIS, com tarifas locais independentes do GCM.")

    doc.add_heading("Capítulo 5 — CAPEX, OPEX e diferenças de custo entre cidades", level=1)
    doc.add_paragraph(
        "O CAPEX soma reservatórios inferior e superior, bombas, painel, sensores, filtragem, air gap, tubos/prumadas e mão de obra. "
        "Os preços dos reservatórios são interpolados; tubos recebem componente de escala; a mão de obra é 30% dos materiais, "
        "respeitando piso por tipologia. O fator regional combina materiais, mão de obra e logística com SP=1,00. Os parâmetros "
        "são de pré-dimensionamento, não substituem orçamento executivo com três cotações."
    )
    econ_volumes = {str(r.building_code): float(r.volume) for _, r in opt[opt.criterio.astype(str).str.startswith("Econômico")].iterrows()}
    capex_rows = []
    for code, name, *_ in TYPOLOGIES:
        res = estimate_calibrated_capex_opex(code, econ_volumes[code], "SP", 0.84)
        capex_rows.append((code, f"{econ_volumes[code]/1000:.1f}", fmt_currency(res["c_inf"]), fmt_currency(res["c_pump"]), fmt_currency(res["c_pipes"]), fmt_currency(res["c_accessories_total"]), fmt_currency(res["labor_cost"]), fmt_currency(res["capex_total_brl"])))
    add_table(doc, ["Tipo", "Vol. (m³)", "Cisterna", "Bombas", "Tubos", "Comando/filtro", "Mão de obra", "CAPEX SP"], capex_rows, [1.0, 1.3, 1.7, 1.5, 1.5, 2.1, 1.9, 1.8], 7.2)
    factors = costs["regional_factors_by_uf"]
    min_uf = min(factors, key=factors.get)
    max_uf = max(factors, key=factors.get)
    doc.add_paragraph(
        f"Os fatores variam de {factors[min_uf]:.2f} em {min_uf} a {factors[max_uf]:.2f} em {max_uf}. Assim, o mesmo sistema "
        f"pode apresentar diferença de aproximadamente {(factors[max_uf]/factors[min_uf]-1)*100:.1f}% apenas pela regionalização. "
        "O OPEX anual inclui manutenção fixa por tipologia, 0,45 kWh/m³ bombeado multiplicado pela tarifa elétrica e R$ 0,05/m³ "
        "para cloração. Não foram incluídos financiamento, tributos de aquisição, obra extraordinária, troca integral de tubulações "
        "ou custo de área ocupada."
    )
    add_figure(doc, "fig13_cost_benefit_breakdown_typologies.png", "Figura 3 — Custos e benefícios anuais por tipologia. Condições: volumes ótimos TOPSIS; médias entre cidades e projeções climáticas.")

    doc.add_heading("Capítulo 6 — Avaliação do ciclo de vida e balanço de carbono", level=1)
    doc.add_paragraph(
        "A métrica usada no banco massivo é uma ACV simplificada de carbono, do berço à operação por 20 anos. Ela contabiliza "
        "CO₂ incorporado do reservatório PEAD, bomba e tubulação; emissões do bombeamento; e crédito pela água potável evitada. "
        "No runner massivo, o PEAD foi aproximado por massa de 22 kg/m³ e fator de 1,9 kg CO₂e/kg, com 45 kg CO₂e para bomba e "
        "35 kg CO₂e para tubos; o crédito é 0,35 kg CO₂e/m³ e a eletricidade 0,08 kg CO₂e/kWh. O módulo ambiental detalhado usa "
        "3,0 kg CO₂e/kg de PEAD, inventário por diâmetro de tubo, potência/quantidade de bombas e tratamento químico."
    )
    add_table(doc, ["Componente", "Fator no estudo massivo", "Unidade/observação", "Confiança"], [
        ("PEAD", "22 × 1,9", "kg material/m³ × kg CO₂e/kg", "Moderada"),
        ("Bomba", "45", "kg CO₂e por sistema", "Baixa–moderada"),
        ("Tubos", "35", "kg CO₂e por sistema", "Baixa–moderada"),
        ("Água potável evitada", "0,35", "kg CO₂e/m³", "Moderada"),
        ("Eletricidade", "0,08", "kg CO₂e/kWh", "Moderada; depende do ano"),
        ("Bombeamento", "0,45", "kWh/m³", "Parâmetro de projeto"),
        ("Vida útil", "20", "anos", "Premissa"),
    ], [3.0, 3.0, 5.0, 2.5])
    doc.add_paragraph(
        "Essa abordagem permite comparar volumes e tipologias em CO₂, mas não é uma ACV ISO 14040/14044 completa: não "
        "cobre transporte real, substituições, fim de vida, eutrofização, toxicidade, escassez hídrica nem 18 categorias ReCiPe. "
        "A literatura brasileira confirma que a construção — sobretudo o reservatório — pode dominar os impactos, e que aumentar "
        "o volume além do necessário pode piorar o desempenho ambiental. Resultados negativos em UTI e alguns cenários devem ser "
        "interpretados como dívida de carbono não recuperada em 20 anos."
    )

    doc.add_heading("Capítulo 7 — Clima atual versus futuro e queda de desempenho", level=1)
    doc.add_paragraph(
        "A comparação climática deve sempre informar cenário, horizonte, tipologias, volumes e agregação de GCMs. Na Figura 17, "
        "o delta não pertence a uma tipologia isolada: compara Histórico (1980–2013) com Far Future (2075–2100) sob SSP5-8.5, "
        "agregando a média dos GCMs disponíveis, das cinco tipologias e de todos os volumes/configurações da amostra. Portanto, "
        "não representa exclusivamente o ótimo TOPSIS."
    )
    add_table(doc, ["Região", "Histórico (%)", "Far SSP5-8.5 (%)", "Variação relativa"], [(r, f"{h:.2f}", f"{f:.2f}", f"{d:.1f}%") for r,h,f,d in CLIMATE_REGIONS], [3.6, 3.0, 3.4, 3.2])
    doc.add_paragraph(
        "A redução é compatível com estiagens mais longas e chuva mais concentrada: o sistema alterna períodos vazios com eventos "
        "que excedem a capacidade de armazenamento. A resposta de adaptação não é simplesmente aumentar a cisterna; devem ser "
        "comparados CAPEX, carbono incorporado e ganho marginal. O redimensionamento futuro deve ser específico por cidade, GCM, "
        "tipologia e nível de serviço."
    )
    add_figure(doc, "fig17_climate_potential_degradation_map.png", "Figura 4 — Histórico versus Far Future/SSP5-8.5. Média dos GCMs, cinco tipologias e todos os volumes; o delta não é de uma tipologia específica.")

    doc.add_heading("Capítulo 8 — Diferenças nacionais e desempenho por tipologia", level=1)
    doc.add_paragraph(
        "A eficiência percentual diminui com a densidade porque a área de cobertura cresce menos que a demanda, mas o benefício "
        "absoluto e o carbono evitado podem aumentar. Por isso, a UTI lidera em percentual de economia e a MFL em VPL e CO₂. "
        "As estatísticas abaixo referem-se às soluções TOPSIS da amostra nacional estratificada; cenários, horizontes e GCMs estão agregados."
    )
    add_table(doc, ["Tipo", "Economia média", "Volume mediano", "VPL médio", "Payback mediano", "CO₂ médio (kg)"], [(c, f"{s:.2f}%", f"{v/1000:.1f} m³", fmt_currency(n), f"{p:.2f} anos", f"{co2:.0f}") for c,s,v,n,p,co2 in NATIONAL_RESULTS], [1.5, 2.2, 2.2, 2.3, 2.3, 2.0])
    doc.add_paragraph(
        "A variação municipal resulta da combinação de chuva, regularidade temporal, tarifa marginal de água/esgoto, parcela fixa, "
        "energia, número de economias, fator regional de CAPEX e escala. Rankings nacionais não devem ser usados para contratação "
        "sem abrir esses determinantes e o grau de confiança tarifária da cidade."
    )
    add_figure(doc, "fig9_regional_macro_analysis.png", "Figura 5 — Diferenças macrorregionais por tipologia. Condições: soluções ótimas TOPSIS e projeções climáticas agregadas.")

    doc.add_heading("Capítulo 9 — Discussão integrada, incertezas e aplicação", level=1)
    add_bullets(doc, [
        "Decisão técnica: usar curva de ganho marginal e confiabilidade, não apenas volume máximo.",
        "Decisão econômica: recalcular a fatura completa por economia e usar tarifa vigente na data do projeto.",
        "Decisão ambiental: refazer o inventário com massa real, distância de transporte, matriz elétrica do período, manutenção e fim de vida.",
        "Decisão climática: testar SSP2-4.5 e SSP5-8.5, múltiplos GCMs e horizontes; não tratar a média como certeza.",
        "Decisão pública: priorizar locais em que benefício hídrico, tarifa evitada, custo regional e vulnerabilidade climática convergem.",
    ])
    doc.add_paragraph(
        "As principais incertezas são: qualidade e vigência das tarifas locais; simplificação do CAPEX; tarifa elétrica sem tributos; "
        "fatores de carbono genéricos; ausência de falhas e reposições; peso TOPSIS; amostragem nacional; e viés/interdispersão dos GCMs. "
        "A planilha tarifária suplementar torna cada cidade rastreável e impede que um número sintético seja apresentado como verdade uniforme."
    )

    doc.add_heading("Capítulo 10 — Conclusões", level=1)
    add_bullets(doc, [
        "Não existe volume ótimo sem critério declarado; técnico, econômico, ambiental e TOPSIS respondem a perguntas diferentes.",
        "Tarifas progressivas e número de economias mudam o VPL; a primeira faixa isolada não representa a economia real.",
        "CAPEX regionalizado varia cerca de 30% entre os extremos dos fatores adotados e deve ser substituído por orçamento executivo.",
        "O balanço de carbono favorece tipologias de maior uso absoluto, mas a ACV massiva é simplificada e deve ser expandida para decisão ambiental definitiva.",
        "O SSP5-8.5 reduz o potencial agregado no fim do século em todas as regiões, com maior queda relativa no Norte.",
        "A base tarifária auditada possui confiança explícita; registros C/D devem entrar em análise de sensibilidade e validação local.",
    ])

    doc.add_page_break()
    doc.add_heading("Apêndice A — Matriz completa de premissas", level=1)
    add_table(doc, ["Grupo", "Parâmetro", "Valor/base", "Sensibilidade/alternativa", "Unidade"], [
        ("Demanda", "Consumo per capita", "150", "120; 180", "L/(hab.dia)"),
        ("Demanda", "Substituição não potável", "40", "30; 50", "%"),
        ("Hidrologia", "Coeficiente de escoamento", "configurável", "por cobertura", "adimensional"),
        ("First flush", "Lâmina", "0; 2; 4", "modos 1, 2 e 3", "mm"),
        ("Armazenamento", "Cisterna inferior", "0,5–50", "12 volumes", "m³"),
        ("Armazenamento", "Reservatório superior", "máx.(200; 10%)", "editável", "L"),
        ("Financeiro", "Vida útil", "20", "editável", "anos"),
        ("Financeiro", "TMA", "6", "10; 14", "% a.a."),
        ("Operação", "Energia de bombeamento", "0,45", "por curva real", "kWh/m³"),
        ("Operação", "Cloro", "2", "por qualidade/uso", "mg/L"),
        ("Operação", "Custo do cloro", "25", "atualizar cotação", "R$/kg"),
        ("Carbono", "Água potável evitada", "0,35", "sensibilidade", "kg CO₂e/m³"),
        ("Carbono", "Eletricidade", "0,08", "série anual", "kg CO₂e/kWh"),
    ], [2.5, 4.0, 3.0, 3.5, 2.2])

    doc.add_heading("Apêndice B — Fatores regionais de CAPEX", level=1)
    factor_rows = [(uf, f"{factor:.2f}", f"{(factor-1)*100:+.0f}%") for uf, factor in sorted(factors.items())]
    add_table(doc, ["UF", "Fator (SP=1,00)", "Diferença relativa"], factor_rows, [3.0, 4.0, 4.0])

    doc.add_heading("Apêndice C — Inventário de subsistemas por tipologia", level=1)
    configs = costs["typology_subsystems_configs"]
    rows = []
    for code, cfg in configs.items():
        rows.append((code, f"{cfg['pump_count']} × {cfg['pump_power_kw']:.2f} kW", fmt_currency(cfg['pipes_base_cost']), fmt_currency(cfg['maint_base_annual']), cfg['description']))
    add_table(doc, ["Tipo", "Bombas", "Tubos base", "Manutenção anual", "Configuração"], rows, [1.3, 2.4, 2.2, 2.4, 7.0], 7.6)

    doc.add_heading("Apêndice D — Proveniência e interpretação da base tarifária", level=1)
    doc.add_paragraph(
        "O suplemento catalogo_tarifas_auditado_652.xlsx contém uma linha por município, URLs, vigência, ato ANEEL, escore e "
        "justificativa. O arquivo tarifas_detalhadas_auditadas.csv preserva as 3.310 linhas por faixa usadas pelo simulador. "
        "A distribuição global é A=236, B=334, C=81 e D=1. A confiança mede evidência e atualidade; não mede estabilidade futura."
    )

    doc.add_heading("Apêndice E — Fontes e referências verificadas", level=1)
    source_rows = [(org, desc, url) for org, desc, url in SOURCES]
    add_table(doc, ["Instituição/estudo", "Uso no artigo", "URL/DOI"], source_rows, [3.0, 6.0, 6.0], 7.4)
    doc.add_paragraph(
        "Normas técnicas de projeto citadas: ABNT NBR 15527 (água de chuva para fins não potáveis), ABNT NBR 5626 "
        "(sistemas prediais de água) e ISO 14040/14044 (princípios e requisitos de ACV). As normas devem ser consultadas em sua "
        "edição licenciada vigente; o artigo não reproduz seu conteúdo integral."
    )

    # Rodapé simples com identificação do estudo.
    for section in doc.sections:
        footer = section.footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = footer.add_run("Netuno 5 · estudo nacional de aproveitamento de água de chuva · versão auditada 2026")
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(100, 116, 139)

    doc.save(OUTPUT)
    print(f"Artigo completo gerado: {OUTPUT}")


if __name__ == "__main__":
    build()
