# -*- coding: utf-8 -*-
"""Compõe o manual em PDF a partir do Markdown montado.

Não depende de pandoc nem de LaTeX: usa `reportlab`, que o programa já traz para
os relatórios. O manual é um documento de impressão — o leitor imprime capítulos
soltos e escreve na margem — e por isso a composição é de página, e não de tela.

Entrada: manual/Manual-Netuno-5.md, produzido por manual/gerar.py.
Saída:   manual/Manual-Netuno-5.pdf

Executar a partir da raiz do programa:
    python manual/gerar_pdf.py
"""

from __future__ import annotations

import os
import re
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, Image, KeepTogether, NextPageTemplate, PageBreak,
    PageTemplate, Paragraph, Preformatted, Spacer, Table, TableStyle,
)

AQUI = os.path.dirname(os.path.abspath(__file__))
ENTRADA = os.path.join(AQUI, "Manual-Netuno-5.md")
SAIDA = os.path.join(AQUI, "Manual-Netuno-5.pdf")

NL = chr(10)

# ── tinta ────────────────────────────────────────────────────────────────────
TINTA = colors.HexColor("#14171a")
TINTA2 = colors.HexColor("#5a5f66")
ACENTO = colors.HexColor("#2a78d6")      # o mesmo azul das figuras
REGUA = colors.HexColor("#d7d9dc")
FUNDO = colors.HexColor("#f2f4f6")
DESTAQUE = colors.HexColor("#c2521f")     # o laranja das figuras, escurecido para texto
FUNDO_APROF = colors.HexColor("#fdf4ef")


# ── tipografia ───────────────────────────────────────────────────────────────
def registrar_fontes():
    """Serifada para o texto, sem serifa para os títulos e as tabelas.

    Se as fontes do sistema não estiverem presentes, cai nas fontes internas do
    reportlab. Elas não têm subscrito nem travessão, e por isso a substituição
    de caracteres em `_sem_unicode` entra junto.
    """
    familias = [
        # (papel, arquivo, índice dentro do .ttc)
        ("Texto", ["cambria.ttc", "georgia.ttf", "times.ttf"], 0),
        ("Texto-B", ["cambriab.ttf", "georgiab.ttf", "timesbd.ttf"], None),
        ("Texto-I", ["cambriai.ttf", "georgiai.ttf", "timesi.ttf"], None),
        ("Texto-BI", ["cambriaz.ttf", "georgiaz.ttf", "timesbi.ttf"], None),
        ("Titulo", ["calibrib.ttf", "arialbd.ttf"], None),
        ("Titulo-R", ["calibri.ttf", "arial.ttf"], None),
        ("Mono", ["consola.ttf", "cour.ttf"], None),
        ("Mono-B", ["consolab.ttf", "courbd.ttf"], None),
    ]
    pastas = [r"C:\Windows\Fonts", "/usr/share/fonts/truetype/msttcorefonts",
              "/usr/share/fonts/truetype/dejavu", "/Library/Fonts"]
    achou_todas = True
    for papel, arquivos, idx in familias:
        registrou = False
        for arquivo in arquivos:
            for pasta in pastas:
                caminho = os.path.join(pasta, arquivo)
                if not os.path.exists(caminho):
                    continue
                try:
                    fonte = (TTFont(papel, caminho) if idx is None
                             else TTFont(papel, caminho, subfontIndex=idx))
                    pdfmetrics.registerFont(fonte)
                    registrou = True
                    break
                except Exception:
                    continue
            if registrou:
                break
        if not registrou:
            achou_todas = False

    if not achou_todas:
        return {
            "texto": "Times-Roman", "texto_b": "Times-Bold",
            "texto_i": "Times-Italic", "texto_bi": "Times-BoldItalic",
            "titulo": "Helvetica-Bold", "titulo_r": "Helvetica",
            "mono": "Courier", "mono_b": "Courier-Bold", "unicode": False,
        }

    pdfmetrics.registerFontFamily(
        "Texto", normal="Texto", bold="Texto-B", italic="Texto-I",
        boldItalic="Texto-BI")
    # Sem esta segunda família, o negrito dentro de célula de tabela e de
    # legenda não aparece: a marcação é aplicada e a fonte não tem para onde ir.
    pdfmetrics.registerFontFamily(
        "Titulo-R", normal="Titulo-R", bold="Titulo", italic="Titulo-R",
        boldItalic="Titulo")
    return {
        "texto": "Texto", "texto_b": "Texto-B", "texto_i": "Texto-I",
        "texto_bi": "Texto-BI", "titulo": "Titulo", "titulo_r": "Titulo-R",
        "mono": "Mono", "mono_b": "Mono-B", "unicode": True,
    }


F = registrar_fontes()

# Caracteres que as fontes internas do reportlab não têm. Só entram em jogo
# quando nenhuma fonte do sistema foi encontrada.
SEM_UNICODE = {
    "₂": "2", "₃": "3", "⁻": "-", "≈": "~", "≥": ">=", "≤": "<=",
    "×": "x", "−": "-", "—": "--", "–": "-", "→": "->", "…": "...",
    "“": '"', "”": '"', "‘": "'", "’": "'", "·": ".", "√": "raiz",
    "Δ": "delta", "ρ": "rho", "η": "eta", "Σ": "soma", "≠": "!=",
}


def _sem_unicode(s):
    if F["unicode"]:
        return s
    for de, para in SEM_UNICODE.items():
        s = s.replace(de, para)
    return s


LARGURA, ALTURA = A4
MARGEM_E = 2.3 * cm
MARGEM_D = 2.0 * cm
MARGEM_S = 2.0 * cm
MARGEM_I = 1.8 * cm
UTIL = LARGURA - MARGEM_E - MARGEM_D


def estilo(nome, **kw):
    base = dict(fontName=F["texto"], fontSize=10.2, leading=14.6,
                textColor=TINTA, spaceAfter=6)
    base.update(kw)
    return ParagraphStyle(nome, **base)


E = {
    "corpo": estilo("corpo", alignment=TA_JUSTIFY),
    "parte": estilo("parte", fontName=F["titulo"], fontSize=30, leading=34,
                    textColor=ACENTO, spaceAfter=10, alignment=TA_LEFT),
    "cap": estilo("cap", fontName=F["titulo"], fontSize=19, leading=23,
                  textColor=TINTA, spaceBefore=2, spaceAfter=10),
    "h2": estilo("h2", fontName=F["titulo"], fontSize=12.6, leading=16,
                 textColor=TINTA, spaceBefore=14, spaceAfter=5),
    "h3": estilo("h3", fontName=F["titulo"], fontSize=10.8, leading=14,
                 textColor=TINTA2, spaceBefore=10, spaceAfter=4),
    "cita": estilo("cita", fontSize=9.8, leading=13.8, textColor=TINTA2,
                   alignment=TA_JUSTIFY),
    "aprof": estilo("aprof", fontSize=9.4, leading=13.2, textColor=TINTA2,
                    alignment=TA_JUSTIFY),
    "aprof_etiqueta": estilo("aprof_etiqueta", fontName=F["titulo"],
                             fontSize=7.4, leading=9.5, textColor=DESTAQUE,
                             spaceAfter=3),
    "item": estilo("item", alignment=TA_JUSTIFY, spaceAfter=3),
    "legenda": estilo("legenda", fontName=F["texto_i"], fontSize=8.8,
                      leading=11.5, textColor=TINTA2, alignment=TA_CENTER,
                      spaceBefore=4, spaceAfter=12),
    "celula": estilo("celula", fontName=F["titulo_r"], fontSize=8.6,
                     leading=11.2, spaceAfter=0),
    "celula_d": estilo("celula_d", fontName=F["titulo_r"], fontSize=8.6,
                       leading=11.2, spaceAfter=0, alignment=TA_RIGHT),
    "celula_c": estilo("celula_c", fontName=F["titulo_r"], fontSize=8.6,
                       leading=11.2, spaceAfter=0, alignment=TA_CENTER),
    "cabecalho": estilo("cabecalho", fontName=F["titulo"], fontSize=8.6,
                        leading=11.2, spaceAfter=0, textColor=TINTA),
    "cabecalho_d": estilo("cabecalho_d", fontName=F["titulo"], fontSize=8.6,
                          leading=11.2, spaceAfter=0, alignment=TA_RIGHT),
    "capa_titulo": estilo("capa_titulo", fontName=F["titulo"], fontSize=40,
                          leading=44, textColor=TINTA, spaceAfter=6),
    "capa_sub": estilo("capa_sub", fontName=F["titulo_r"], fontSize=14,
                       leading=19, textColor=TINTA2, spaceAfter=4),
}


# ── inline ───────────────────────────────────────────────────────────────────
def inline(texto):
    """Converte o Markdown de linha para a marcação que o Paragraph entende."""
    t = _sem_unicode(texto)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # O código entra primeiro e sai do caminho das demais marcações: um trecho
    # como `**` dentro de crase não pode virar negrito.
    guardados = []

    def guardar(m):
        guardados.append(m.group(1))
        return f"\x00{len(guardados) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guardar, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*([^*]+)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", t)      # o PDF não navega

    def devolver(m):
        trecho = guardados[int(m.group(1))]
        return (f'<font face="{F["mono"]}" size="8.8" '
                f'color="#1f4f8f">{trecho}</font>')

    return re.sub(r"\x00(\d+)\x00", devolver, t)


# ── tabelas ──────────────────────────────────────────────────────────────────
def alinhamentos(linha_separadora):
    saida = []
    for celula in _celulas(linha_separadora):
        c = celula.strip()
        if c.startswith(":") and c.endswith(":"):
            saida.append("c")
        elif c.endswith(":"):
            saida.append("d")
        else:
            saida.append("e")
    return saida


def _celulas(linha):
    return [c.strip() for c in linha.strip().strip("|").split("|")]


def montar_tabela(linhas):
    """Compõe uma tabela do Markdown, com a largura repartida pelo conteúdo."""
    if len(linhas) < 2:
        return None
    cabecalho = _celulas(linhas[0])
    alin = alinhamentos(linhas[1])
    corpo = [_celulas(l) for l in linhas[2:]]
    colunas = max([len(cabecalho)] + [len(l) for l in corpo])
    alin += ["e"] * (colunas - len(alin))

    def normaliza(celulas):
        return list(celulas) + [""] * (colunas - len(celulas))

    # A largura de cada coluna acompanha o conteúdo mais longo, com piso e teto
    # para que uma coluna de números não fique tão estreita quanto o número.
    pesos, minimos = [], []
    for c in range(colunas):
        textos = [normaliza(cabecalho)[c]] + [normaliza(l)[c] for l in corpo]
        limpos = [re.sub(r"[*`]", "", t) for t in textos]
        maior = max((len(t) for t in limpos), default=1)
        pesos.append(min(max(maior, 6), 58))
        # Nenhuma coluna pode ficar mais estreita que a maior palavra que ela
        # contem: abaixo disso o reportlab quebra a palavra no meio, e a
        # tabela sai com "Extravasad o" no cabecalho.
        palavra = max((p for t in limpos for p in t.split()),
                      key=lambda p: pdfmetrics.stringWidth(
                          _sem_unicode(p), F["titulo"], 8.6), default="")
        minimos.append(pdfmetrics.stringWidth(
            _sem_unicode(palavra), F["titulo"], 8.6) + 11.0)

    total = float(sum(pesos)) or 1.0
    larguras = [UTIL * p / total for p in pesos]
    if sum(minimos) < UTIL:
        # Quem esta abaixo do minimo sobe; a diferenca sai de quem tem folga,
        # na proporcao da folga de cada um.
        falta = sum(max(0.0, m - l) for m, l in zip(minimos, larguras))
        folga = sum(max(0.0, l - m) for m, l in zip(minimos, larguras))
        if falta > 0 and folga > 0:
            larguras = [
                m if l < m else l - (l - m) * falta / folga
                for m, l in zip(minimos, larguras)
            ]

    def paragrafo(texto, c, cabeca=False):
        if cabeca:
            chave = "cabecalho_d" if alin[c] == "d" else "cabecalho"
        else:
            chave = {"d": "celula_d", "c": "celula_c"}.get(alin[c], "celula")
        return Paragraph(inline(texto), E[chave])

    dados = [[paragrafo(t, c, True) for c, t in enumerate(normaliza(cabecalho))]]
    for linha in corpo:
        dados.append([paragrafo(t, c) for c, t in enumerate(normaliza(linha))])

    estilo_tab = TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("BACKGROUND", (0, 0), (-1, 0), FUNDO),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, REGUA),
        ("LINEBELOW", (0, 1), (-1, -2), 0.35, colors.HexColor("#eceef0")),
        ("LINEBELOW", (0, -1), (-1, -1), 0.8, REGUA),
    ])
    t = Table(dados, colWidths=larguras, repeatRows=1, hAlign="LEFT")
    t.setStyle(estilo_tab)
    return t


def citacao(paragrafos, aprofundamento=False):
    """Bloco de citação: régua colorida à esquerda e recuo.

    Duas aparências. A comum, de régua azul e sem fundo, é o aviso que o leitor
    precisa ler. A de aprofundamento, laranja e com fundo tingido, é o detalhe
    técnico que ele pode pular na primeira leitura.
    """
    cor = DESTAQUE if aprofundamento else ACENTO
    fundo = FUNDO_APROF if aprofundamento else None

    interna = Table([[p] for p in paragrafos], colWidths=[UTIL - 18])
    interna.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))
    estilo_fora = [
        ("LINEBEFORE", (0, 0), (0, -1), 2.4, cor),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if fundo is not None:
        estilo_fora.append(("BACKGROUND", (0, 0), (-1, -1), fundo))
    fora = Table([[interna]], colWidths=[UTIL])
    fora.setStyle(TableStyle(estilo_fora))
    return fora


# ── o documento ──────────────────────────────────────────────────────────────
class Manual(BaseDocTemplate):
    """Guarda o título corrente para o cabeçalho de página."""

    def __init__(self, *args, **kw):
        BaseDocTemplate.__init__(self, *args, **kw)
        self.corrente = ""

    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name in ("cap", "parte"):
            self.corrente = re.sub(r"<[^>]+>", "", flowable.getPlainText())


def moldura(canvas, doc, com_furniture=True):
    canvas.saveState()
    if com_furniture:
        canvas.setFont(F["titulo_r"], 7.6)
        canvas.setFillColor(TINTA2)
        titulo = getattr(doc, "corrente", "")
        if titulo:
            canvas.drawString(MARGEM_E, ALTURA - MARGEM_S + 8 * mm, titulo[:78])
        canvas.drawRightString(LARGURA - MARGEM_D, ALTURA - MARGEM_S + 8 * mm,
                               "Manual do Netuno 5.0.8")
        canvas.setStrokeColor(REGUA)
        canvas.setLineWidth(0.4)
        canvas.line(MARGEM_E, ALTURA - MARGEM_S + 6 * mm,
                    LARGURA - MARGEM_D, ALTURA - MARGEM_S + 6 * mm)
        canvas.setFont(F["titulo_r"], 8.4)
        canvas.drawCentredString(LARGURA / 2.0, MARGEM_I - 6 * mm,
                                 str(canvas.getPageNumber()))
    canvas.restoreState()


def capa(canvas, doc):
    moldura(canvas, doc, com_furniture=False)


# ── a travessia do Markdown ──────────────────────────────────────────────────
def converter(texto):
    """Percorre o Markdown montado e devolve a lista de elementos do PDF."""
    linhas = texto.split(NL)
    fluxo = []
    i = 0
    primeira_parte = True

    def fecha_paragrafo(acumulado, estilo_chave="corpo"):
        if acumulado:
            fluxo.append(Paragraph(inline(" ".join(acumulado)), E[estilo_chave]))
            acumulado.clear()

    acumulado = []
    while i < len(linhas):
        linha = linhas[i]
        cru = linha.rstrip()

        # bloco de código
        if cru.startswith("```"):
            fecha_paragrafo(acumulado)
            i += 1
            codigo = []
            while i < len(linhas) and not linhas[i].startswith("```"):
                codigo.append(linhas[i])
                i += 1
            i += 1
            bloco = Preformatted(
                _sem_unicode(NL.join(codigo)),
                ParagraphStyle("cod", fontName=F["mono"], fontSize=8.4,
                               leading=11.4, textColor=TINTA,
                               backColor=FUNDO, borderPadding=7,
                               leftIndent=0, spaceBefore=4, spaceAfter=9))
            fluxo.append(bloco)
            continue

        # tabela
        if cru.startswith("|") and i + 1 < len(linhas) and re.match(
                r"^\|[\s:\-|]+\|$", linhas[i + 1].rstrip()):
            fecha_paragrafo(acumulado)
            bloco = [cru]
            i += 1
            while i < len(linhas) and linhas[i].rstrip().startswith("|"):
                bloco.append(linhas[i].rstrip())
                i += 1
            tabela = montar_tabela(bloco)
            if tabela is not None:
                fluxo += [Spacer(1, 3), tabela, Spacer(1, 9)]
            continue

        # citação
        if cru.startswith(">"):
            fecha_paragrafo(acumulado)
            bruto = []
            while i < len(linhas) and linhas[i].rstrip().startswith(">"):
                bruto.append(linhas[i].rstrip()[1:].strip())
                i += 1

            # «> **Aprofundamento: assunto.** texto...» vira caixa própria, com
            # o assunto como etiqueta acima do texto.
            aprof = False
            etiqueta = ""
            if bruto and bruto[0].startswith("**Aprofundamento"):
                aprof = True
                m_et = re.match(r"^\*\*Aprofundamento:?\s*([^*]*)\.?\*\*\s*(.*)$",
                                bruto[0])
                if m_et:
                    etiqueta = (m_et.group(1) or "").strip().rstrip(".")
                    bruto[0] = m_et.group(2).strip()

            estilo_texto = "aprof" if aprof else "cita"
            dentro = []
            if aprof:
                rotulo = "APROFUNDAMENTO"
                if etiqueta:
                    rotulo += "  ·  " + etiqueta
                dentro.append(Paragraph(inline(rotulo.upper()),
                                        E["aprof_etiqueta"]))
            texto_corrido = []
            for conteudo in bruto:
                if not conteudo:
                    if texto_corrido:
                        dentro.append(Paragraph(
                            inline(" ".join(texto_corrido)), E[estilo_texto]))
                        texto_corrido = []
                else:
                    texto_corrido.append(conteudo)
            if texto_corrido:
                dentro.append(Paragraph(inline(" ".join(texto_corrido)),
                                        E[estilo_texto]))
            fluxo += [Spacer(1, 3), citacao(dentro, aprofundamento=aprof),
                      Spacer(1, 9)]
            continue

        # figura
        m = re.match(r"^!\[([^\]]*)\]\(([^)]+)\)\s*$", cru)
        if m:
            fecha_paragrafo(acumulado)
            caminho = os.path.normpath(os.path.join(AQUI, "partes", m.group(2)))
            if os.path.exists(caminho):
                from reportlab.lib.utils import ImageReader
                lx, ly = ImageReader(caminho).getSize()
                largura = min(UTIL, 15.0 * cm)
                fluxo.append(Image(caminho, width=largura,
                                   height=largura * ly / float(lx)))
            i += 1
            continue

        # títulos
        if cru.startswith("# "):
            fecha_paragrafo(acumulado)
            titulo = cru[2:].strip()
            if titulo.lower().startswith("parte "):
                # A folha de abertura de parte fica sozinha: a quebra de baixo
                # e a do capitulo seguinte sao a mesma, e duas produziriam uma
                # folha em branco no meio.
                primeira_parte = False
                fluxo += [PageBreak(), Spacer(1, 3.2 * cm),
                          Paragraph(inline(titulo), E["parte"])]
            else:
                if fluxo:
                    fluxo.append(PageBreak())
                fluxo.append(Paragraph(inline(titulo), E["cap"]))
            i += 1
            continue
        if cru.startswith("## "):
            fecha_paragrafo(acumulado)
            if cru[3:].strip().lower().startswith("sumário"):
                fluxo.append(PageBreak())
            fluxo.append(Paragraph(inline(cru[3:].strip()), E["h2"]))
            i += 1
            continue
        if cru.startswith("### "):
            fecha_paragrafo(acumulado)
            fluxo.append(Paragraph(inline(cru[4:].strip()), E["h3"]))
            i += 1
            continue

        # legenda de figura: linha só de itálico logo após a imagem
        if re.match(r"^\*[^*].*\*$", cru) and fluxo and isinstance(
                fluxo[-1], Image):
            fecha_paragrafo(acumulado)
            fluxo.append(Paragraph(inline(cru.strip("*")), E["legenda"]))
            i += 1
            continue

        # régua
        if cru.strip() in ("---", "***", "___"):
            fecha_paragrafo(acumulado)
            fluxo.append(Spacer(1, 6))
            i += 1
            continue

        # listas
        m = re.match(r"^(\s*)([-*]|\d+\.|[A-J]\.)\s+(.*)$", cru)
        if m:
            fecha_paragrafo(acumulado)
            recuo = len(m.group(1))
            marca = "•" if m.group(2) in ("-", "*") else m.group(2)
            item = [m.group(3)]
            i += 1
            # continuação recuada do mesmo item
            while (i < len(linhas) and linhas[i].strip()
                   and not re.match(r"^(\s*)([-*]|\d+\.)\s+", linhas[i])
                   and linhas[i].startswith("  ")
                   and not linhas[i].lstrip().startswith(("|", ">", "#", "```"))):
                item.append(linhas[i].strip())
                i += 1
            estilo_item = ParagraphStyle(
                "it", parent=E["item"], leftIndent=14 + recuo * 8,
                bulletIndent=2 + recuo * 8)
            fluxo.append(Paragraph(inline(" ".join(item)), estilo_item,
                                   bulletText=_sem_unicode(marca)))
            continue

        if not cru.strip():
            fecha_paragrafo(acumulado)
            i += 1
            continue

        acumulado.append(cru.strip())
        i += 1

    fecha_paragrafo(acumulado)

    # A abertura de parte termina em quebra e o capítulo seguinte começa com
    # outra: sem isto, cada parte é seguida de uma folha em branco.
    enxuto = []
    for elemento in fluxo:
        if (isinstance(elemento, PageBreak) and enxuto
                and isinstance(enxuto[-1], PageBreak)):
            continue
        enxuto.append(elemento)
    return enxuto


def folha_de_rosto():
    return [
        Spacer(1, 5.0 * cm),
        Paragraph("Manual do Netuno", E["capa_titulo"]),
        Paragraph("Versão 5.0.8", E["capa_sub"]),
        Spacer(1, 0.8 * cm),
        Paragraph("Simulação de sistemas de aproveitamento de água pluvial "
                  "em edificações", E["capa_sub"]),
        Spacer(1, 5.5 * cm),
        Paragraph("Universidade Federal de Santa Catarina", E["capa_sub"]),
        Paragraph("Laboratório de Eficiência Energética em Edificações",
                  E["capa_sub"]),
        PageBreak(),
    ]


def main():
    if not os.path.exists(ENTRADA):
        print("manual ainda não montado; rode manual/gerar.py")
        return 1
    texto = open(ENTRADA, encoding="utf-8").read()

    # A folha de rosto do Markdown é substituída pela do PDF, que ocupa a
    # página inteira; o sumário gerado permanece.
    # A folha de rosto do PDF substitui o bloco de título do Markdown, que vai
    # até a primeira régua; o resto do preâmbulo — como usar, e o sumário —
    # permanece.
    corpo = texto
    marca = NL + "---" + NL
    if corpo.lstrip().startswith("# Netuno 5") and marca in corpo:
        corpo = corpo.split(marca, 1)[1].lstrip()

    # O PDF costuma estar aberto num leitor quando se regera o manual, e no
    # Windows o arquivo aberto nao pode ser sobrescrito. Compoe-se ao lado e
    # troca-se no fim, o que tambem evita deixar um PDF truncado se algo falhar.
    provisorio = SAIDA + ".novo"
    doc = Manual(provisorio, pagesize=A4,
                 leftMargin=MARGEM_E, rightMargin=MARGEM_D,
                 topMargin=MARGEM_S, bottomMargin=MARGEM_I,
                 title="Manual do Netuno 5.0.8",
                 author="UFSC — LabEEE", subject="Aproveitamento de água pluvial")
    quadro = Frame(MARGEM_E, MARGEM_I, UTIL,
                   ALTURA - MARGEM_S - MARGEM_I, id="corpo",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="capa", frames=[quadro], onPage=capa),
        PageTemplate(id="miolo", frames=[quadro], onPage=moldura),
    ])

    fluxo = folha_de_rosto() + [NextPageTemplate("miolo")] + converter(corpo)
    doc.build(fluxo)

    try:
        os.replace(provisorio, SAIDA)
    except PermissionError:
        print("o PDF esta aberto noutro programa; feche-o e rode de novo.")
        print("a versao nova ficou em " + os.path.basename(provisorio))
        return 1

    tamanho = os.path.getsize(SAIDA) / 1024.0 / 1024.0
    print(f"PDF: {os.path.basename(SAIDA)}  {doc.page} páginas, "
          f"{tamanho:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
