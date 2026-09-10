"""
Gera o artigo científico consolidado com as 8 figuras em formato DOCX de padrão internacional.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = ROOT / "figuras_consolidadas_artigo"
MD_FILE = ROOT / "Artigo_Cientifico_Netuno5_Consolidado.md"
DOCX_OUT = ROOT / "Artigo_Cientifico_Netuno5_8Figuras.docx"

NAVY = "0F172A"
BLUE = "1E40AF"
MUTED = "64748B"
INK = RGBColor(15, 23, 42)

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

def configure_doc(doc):
    doc.settings.odd_and_even_pages_header_footer = False
    section = doc.sections[0]
    section.different_first_page_header_footer = False
    section.page_width = Inches(8.2677)  # A4
    section.page_height = Inches(11.6929)
    section.top_margin = section.bottom_margin = Inches(0.9843)
    section.left_margin = section.right_margin = Inches(0.9843)
    section.header_distance = section.footer_distance = Inches(0.492)

    # Numeração de linhas contínua para padrão de submissão
    sect_pr = section._sectPr
    line_numbers = OxmlElement("w:lnNumType")
    line_numbers.set(qn("w:countBy"), "1")
    line_numbers.set(qn("w:restart"), "continuous")
    sect_pr.append(line_numbers)

    normal = doc.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(10.5)
    normal.paragraph_format.space_before = Pt(0)
    normal.paragraph_format.space_after = Pt(5)
    normal.paragraph_format.line_spacing = 1.35
    normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT

    for name, size, color, before, after in [
        ("Heading 1", 13.5, BLUE, 14, 6),
        ("Heading 2", 11.5, NAVY, 10, 4),
        ("Heading 3", 10.5, NAVY, 8, 3),
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
    hrun = header.add_run("NETUNO 5 — CONSOLIDAÇÃO DOS TRÊS ESTUDOS (RESIDENCIAL CMIP6, 11 TIPOLOGIAS BRASIL E 255 METRÓPOLES)")
    set_run(hrun, size=8, color=MUTED)

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    frun = footer.add_run("Página ")
    set_run(frun, size=9, color=MUTED)
    add_page_field(footer)

def add_figure(doc, filename: str, caption: str, width_in: float = 6.30):
    path = FIG_DIR / filename
    if not path.exists():
        print(f"Alerta: Figura não encontrada: {path}")
        return
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    shape = p.add_run().add_picture(str(path), width=Inches(width_in))
    shape._inline.docPr.set("descr", caption)

    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.LEFT
    c.paragraph_format.keep_together = True
    c.paragraph_format.space_before = Pt(2)
    c.paragraph_format.space_after = Pt(8)

    match = re.match(r"(Figura\s+\d+\s*[-—–]\s*)(.*)", caption, re.IGNORECASE)
    if match:
        set_run(c.add_run(match.group(1)), size=9, bold=True, color=NAVY)
        set_run(c.add_run(match.group(2)), size=9, italic=False)
    else:
        set_run(c.add_run(caption), size=9)

def build_article_docx():
    print("Iniciando compilação do artigo consolidado em DOCX...")
    doc = Document()
    configure_doc(doc)

    with open(MD_FILE, 'r', encoding='utf-8') as f:
        md_text = f.read()

    lines = md_text.splitlines()
    i = 0
    in_references = False

    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        # Título principal
        if line.startswith("# "):
            title = line[2:].strip()
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(16)
            p.paragraph_format.space_after = Pt(6)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            set_run(p.add_run(title), size=16, bold=True, color=NAVY)
            i += 1
            continue

        # Autores / Data / Metadados
        if line.startswith("**Autores:**") or line.startswith("**Data:**") or line.startswith("**Documento Técnico"):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            set_run(p.add_run(line.replace("**", "")), size=9.5, italic=True, color=MUTED)
            i += 1
            continue

        if line == "---":
            i += 1
            continue

        # Seções principais H2
        if line.startswith("## "):
            h2 = line[3:].strip()
            doc.add_heading(h2, level=1)
            i += 1
            continue

        # Subseções H3
        if line.startswith("### "):
            h3 = line[4:].strip()
            doc.add_heading(h3, level=2)
            i += 1
            continue

        # Imagens embutidas: ![Caption](caminho)
        img_match = re.match(r"!\[(.*?)\]\((.*?)\)", line)
        if img_match:
            caption = img_match.group(1)
            rel_path = img_match.group(2)
            filename = os.path.basename(rel_path)
            add_figure(doc, filename, caption)
            i += 1
            continue

        # Listas com marcadores ou numéricas
        if line.startswith("- ") or line.startswith("* "):
            p = doc.add_paragraph(style='List Bullet')
            p.paragraph_format.space_after = Pt(3)
            # Tratar negritos simples
            text = line[2:].strip()
            parts = re.split(r"(\*\*.*?\*\*)", text)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    set_run(p.add_run(part[2:-2]), size=10, bold=True)
                else:
                    set_run(p.add_run(part), size=10)
            i += 1
            continue

        if re.match(r"^\d+\.\s+", line):
            p = doc.add_paragraph(style='List Number')
            p.paragraph_format.space_after = Pt(3)
            num_match = re.match(r"^\d+\.\s+(.*)", line)
            text = num_match.group(1) if num_match else line
            parts = re.split(r"(\*\*.*?\*\*)", text)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    set_run(p.add_run(part[2:-2]), size=10, bold=True)
                else:
                    set_run(p.add_run(part), size=10)
            i += 1
            continue

        # Parágrafo comum
        p = doc.add_paragraph()
        parts = re.split(r"(\*\*.*?\*\*)", line)
        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                set_run(p.add_run(part[2:-2]), size=10.5, bold=True)
            else:
                set_run(p.add_run(part), size=10.5)
        i += 1

    doc.save(str(DOCX_OUT))
    print(f"Artigo DOCX gerado com sucesso em: {DOCX_OUT}")

if __name__ == "__main__":
    build_article_docx()
