# -*- coding: utf-8 -*-
"""Compõe o manual em PDF a partir do Markdown montado.

Não depende de pandoc nem de LaTeX: usa `reportlab`, que o programa já traz para
os relatórios. O manual é um documento de impressão — o leitor imprime capítulos
soltos e escreve na margem — e por isso a composição é de página, e não de tela.

Entrada: manual/Manual-Triton.md, produzido por manual/gerar.py.
Saída:   manual/Manual-Triton.pdf

Executar a partir da raiz do programa:
    python manual/gerar_pdf.py
"""

from __future__ import annotations

import json
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
RAIZ = os.path.dirname(AQUI)
if RAIZ not in sys.path:
    sys.path.insert(0, RAIZ)
from triton import __version__ as VERSAO  # noqa: E402
ENTRADA = os.path.join(AQUI, "Manual-Triton.md")
SAIDA = os.path.join(AQUI, "Manual-Triton.pdf")

NL = chr(10)

# ── tinta ────────────────────────────────────────────────────────────────────
TINTA = colors.HexColor("#14171a")
TINTA2 = colors.HexColor("#5a5f66")
ACENTO = colors.HexColor("#2a78d6")      # o mesmo azul das figuras
REGUA = colors.HexColor("#d7d9dc")
FUNDO = colors.HexColor("#f2f4f6")
DESTAQUE = colors.HexColor("#c2521f")     # o laranja das figuras, escurecido para texto
FUNDO_APROF = colors.HexColor("#fdf4ef")
#: O realce de frase. Amarelo palido, que imprime bem em preto e branco.
REALCE = "#fdf0b5"


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
# Uma figura pode ocupar metade da mancha; passando disso, ela empurra sozinha
# para a página seguinte o parágrafo que a apresenta.
ALTURA_MAX_FIGURA = 0.52 * (ALTURA - MARGEM_S - MARGEM_I)


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
    "equacao": estilo("equacao", fontName=F["mono"], fontSize=10.0,
                      leading=15.0, alignment=TA_CENTER, spaceAfter=0),
    "eq_numero": estilo("eq_numero", fontSize=10.0, leading=15.0,
                        alignment=TA_RIGHT, spaceAfter=0),
    "legenda_tabela": estilo("legenda_tabela", fontName=F["titulo_r"],
                             fontSize=8.6, leading=11.4, textColor=TINTA2,
                             spaceAfter=1),
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
CIRCULO_POR_MARCADOR = {"🟢": "#2e9d55", "🟡": "#d9a400", "🔴": "#d1453b"}


def inline(texto):
    """Converte o Markdown de linha para a marcação que o Paragraph entende."""
    t = _sem_unicode(texto)
    t = t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    # Os marcadores de situação viram um círculo na cor deles: a fonte do PDF não tem
    # os emojis, e sem isto eles saíam como um quadrado preto.
    for marcador, cor in CIRCULO_POR_MARCADOR.items():
        t = t.replace(marcador, f'<font color="{cor}">\u25cf</font>')

    # O código entra primeiro e sai do caminho das demais marcações: um trecho
    # como `**` dentro de crase não pode virar negrito.
    guardados = []

    def guardar(m):
        guardados.append(m.group(1))
        return f"\x00{len(guardados) - 1}\x00"

    t = re.sub(r"`([^`]+)`", guardar, t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", t)
    # ==frase== sai com fundo tingido, para a frase que carrega o ponto do
    # paragrafo. O reportlab aceita backColor dentro da marcacao de fonte.
    t = re.sub(r"==([^=]+)==",
               r'<font backColor="' + REALCE + r'">\1</font>', t)
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


FUNDO_POR_MARCADOR = {"🟢": colors.HexColor("#e3f4e8"), "🟡": colors.HexColor("#fff4cc"),
                      "🔴": colors.HexColor("#fbe0dc")}


def montar_tabela(linhas):
    """Compõe uma tabela do Markdown, com a largura repartida pelo conteúdo."""
    if len(linhas) < 2:
        return None
    cabecalho = _celulas(linhas[0])
    alin = alinhamentos(linhas[1])
    corpo = [_celulas(l) for l in linhas[2:]]
    # Uma linha cuja primeira célula abre com 🟢, 🟡 ou 🔴 ganha fundo verde, amarelo ou
    # vermelho claro, e o marcador sai do texto: é a situação do dado (apêndice de tarifas).
    fundos = {}
    for i, l in enumerate(corpo, 1):
        if l and l[0][:1] in FUNDO_POR_MARCADOR:
            fundos[i] = FUNDO_POR_MARCADOR[l[0][:1]]
            l[0] = l[0][1:].strip()
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
        # A celula que e so codigo sai em monoespacada, que e mais larga que a
        # fonte do texto: medir com a fonte errada espreme a coluna e quebra o
        # simbolo no meio.
        # O cabeçalho fica de fora: ele é palavra («Símbolo»), e a coluna é de
        # código quando as **células** são código.
        celulas_col = [t for t in textos[1:] if t.strip()]
        so_codigo = bool(celulas_col) and all(
            t.strip().startswith("`") for t in celulas_col)
        fonte_col = F["mono"] if so_codigo else F["titulo"]
        corpo_col = 8.8 if so_codigo else 8.6
        # Numa coluna de código, a célula inteira é um símbolo só: `V_cap,t`
        # não pode quebrar na vírgula. Fora dela, o mínimo é a maior palavra.
        if so_codigo:
            trechos = [t.strip() for t in limpos]
        else:
            trechos = [p for t in limpos for p in t.split()]
        maior_trecho = max(trechos, key=lambda p: pdfmetrics.stringWidth(
            _sem_unicode(p), fonte_col, corpo_col), default="")
        minimos.append(pdfmetrics.stringWidth(
            _sem_unicode(maior_trecho), fonte_col, corpo_col) + 11.0)

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
    for i, cor in fundos.items():
        estilo_tab.add("BACKGROUND", (0, i), (-1, i), cor)
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
        if isinstance(flowable, Paragraph) and flowable.style.name in ("cap", "parte"):  # noqa: E501
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
                               getattr(doc, "cabecalho", T("cabecalho")))
        canvas.setStrokeColor(REGUA)
        canvas.setLineWidth(0.4)
        canvas.line(MARGEM_E, ALTURA - MARGEM_S + 6 * mm,
                    LARGURA - MARGEM_D, ALTURA - MARGEM_S + 6 * mm)
        canvas.setFont(F["titulo_r"], 8.4)
        canvas.drawCentredString(LARGURA / 2.0, MARGEM_I - 6 * mm,
                                 str(canvas.getPageNumber()))
    canvas.restoreState()


#: O que a composição escreve por conta própria, por idioma. O manual em inglês usa
#: `compor_pdf(..., idioma="en")`; o texto dele já vem traduzido do Markdown.
TEXTOS = {
    "pt": dict(cabecalho=f"Manual do Triton {VERSAO}", capa="MANUAL DO USUÁRIO",
               grupo="Grupo de Pesquisa em Ambientes Sustentáveis",
               universidade="Universidade Federal de Santa Catarina",
               rodape=f"Florianópolis · 2026 · Versão {VERSAO}",
               aprofundamento="Aprofundamento", sumario="sumário", apendice="Apêndice",
               assunto="Aproveitamento de água pluvial em edificações"),
    "en": dict(cabecalho=f"Triton User Manual {VERSAO}", capa="USER MANUAL",
               grupo="Sustainable Environments Research Group",
               universidade="Federal University of Santa Catarina",
               rodape=f"Florianópolis, Brazil · 2026 · Version {VERSAO}",
               aprofundamento="In depth", sumario="contents", apendice="Appendix",
               assunto="Rainwater harvesting in buildings"),
}
IDIOMA_PDF = "pt"


def T(chave):
    return TEXTOS[IDIOMA_PDF][chave]


MARINHO = colors.HexColor("#0b2545")
PAINEL = 0.62            # fração da altura da folha ocupada pelo painel


def capa(canvas, doc):
    """A capa desenhada: painel com o desenho do volume, título e créditos.

    Sem `doc.capa`, fica a folha de rosto antiga, só com texto.
    """
    info = getattr(doc, "capa", None)
    if not info:
        moldura(canvas, doc, com_furniture=False)
        return
    from reportlab.lib.utils import simpleSplit
    cor = colors.HexColor(info["cor"])
    base = ALTURA * (1 - PAINEL)
    canvas.saveState()

    # o painel, de ponta a ponta
    canvas.setFillColor(MARINHO)
    canvas.rect(0, base, LARGURA, ALTURA - base, stroke=0, fill=1)
    if os.path.exists(info.get("painel", "")):
        canvas.drawImage(info["painel"], 0, base, width=LARGURA, height=ALTURA - base)

    # cabeçalho do painel
    canvas.setFillColor(colors.white)
    canvas.setFont(F["titulo"], 10)
    canvas.drawString(MARGEM_E, ALTURA - 18 * mm, "TRITON")
    canvas.setFont(F["titulo_r"], 10)
    canvas.drawRightString(LARGURA - MARGEM_D, ALTURA - 18 * mm, T("capa"))
    canvas.setStrokeColor(colors.Color(1, 1, 1, alpha=0.35))
    canvas.setLineWidth(0.5)
    canvas.line(MARGEM_E, ALTURA - 21 * mm, LARGURA - MARGEM_D, ALTURA - 21 * mm)

    # o número do volume, grande, no pé do painel
    if info.get("numero"):
        canvas.setFillColor(cor)
        canvas.setFont(F["titulo"], 132)
        canvas.drawString(MARGEM_E - 4, base + 12 * mm, info["numero"])
        largura_num = canvas.stringWidth(info["numero"], F["titulo"], 132)
        canvas.setFillColor(colors.white)
        canvas.setFont(F["titulo_r"], 12)
        canvas.drawString(MARGEM_E + largura_num + 6, base + 16 * mm, info.get("de", ""))

    # faixa na cor do volume, na divisa entre o painel e a folha
    canvas.setFillColor(cor)
    canvas.rect(0, base - 2.2 * mm, LARGURA, 2.2 * mm, stroke=0, fill=1)

    # título, frase e conteúdo
    y = base - 20 * mm
    canvas.setFillColor(MARINHO)
    for linha in simpleSplit(info["titulo"], F["titulo"], 32, UTIL):
        canvas.setFont(F["titulo"], 32)
        canvas.drawString(MARGEM_E, y, linha)
        y -= 36
    y -= 4
    canvas.setFillColor(TINTA2)
    for linha in simpleSplit(info.get("frase", ""), F["texto_i"], 13, UTIL):
        canvas.setFont(F["texto_i"], 13)
        canvas.drawString(MARGEM_E, y, linha)
        y -= 17
    if info.get("conteudo"):
        y -= 8
        canvas.setFont(F["titulo_r"], 9.5)
        for linha in simpleSplit(info["conteudo"].upper(), F["titulo_r"], 9.5, UTIL):
            canvas.drawString(MARGEM_E, y, linha)
            y -= 13

    # créditos no pé da folha
    canvas.setFillColor(TINTA)
    canvas.setFont(F["titulo"], 10.5)
    canvas.drawString(MARGEM_E, 30 * mm, "Igor Catão Martins Vaz & Enedir Ghisi")
    canvas.setFillColor(TINTA2)
    canvas.setFont(F["titulo_r"], 9.5)
    canvas.drawString(MARGEM_E, 25 * mm, T("grupo"))
    canvas.drawString(MARGEM_E, 20.5 * mm, T("universidade"))
    canvas.drawString(MARGEM_E, 16 * mm, T("rodape"))
    if os.path.exists(LOGO):
        from reportlab.lib.utils import ImageReader
        lx, ly = ImageReader(LOGO).getSize()
        largura = 2.4 * cm
        canvas.drawImage(LOGO, LARGURA - MARGEM_D - largura, 15 * mm, width=largura,
                         height=largura * ly / float(lx), mask="auto")
    canvas.restoreState()


# ── a travessia do Markdown ──────────────────────────────────────────────────
def _com_o_proximo(paragrafo):
    """Marca o parágrafo para não se separar do que vem abaixo.

    O reportlab honra `keepWithNext` no estilo, e não no objeto; a cópia do
    estilo evita que a marca vaze para todos os títulos do mesmo nível.
    """
    estilo = ParagraphStyle(paragrafo.style.name + "-junto",
                            parent=paragrafo.style)
    estilo.keepWithNext = 1
    paragrafo.style = estilo
    return paragrafo


#: As imagens das equações, compostas por manual/gerar_equacoes.py.
EQUACOES = {}

#: Quantas tabelas já receberam número. Fica fora da função porque a legenda é
#: emitida num ponto e a lista inicial é montada noutro.
contador_tabelas = [0]


def _titulo_amarrado(elemento):
    estilo = getattr(elemento, "style", None)
    return isinstance(elemento, Paragraph) and bool(getattr(estilo, "keepWithNext", 0))


def amarrar_titulos(fluxo):
    """Nenhum título termina a página sem o conteúdo que ele abre.

    O `keepWithNext` do reportlab liga o título ao elemento seguinte, e esse
    elemento costuma ser um espaçador: o título ficava no pé da página e a
    tabela descia sozinha (o professor apontou a subseção «A curva» isolada
    assim). Agrupar título e conteúdo num bloco indivisível resolvia, mas
    empurrava blocos grandes inteiros e abria páginas quase vazias. Aqui, antes
    de cada título, uma quebra condicional mede o título e o primeiro conteúdo
    real, e só muda de página quando essa altura não cabe no espaço restante.
    Uma equação é medida junto com a tabela de variáveis que a segue.
    """
    import io
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import CondPageBreak
    from reportlab.platypus import Spacer as _Spacer
    # Os blocos só se medem sobre uma tela; sem ela a medida falhava em
    # silêncio e valia zero.
    tela = Canvas(io.BytesIO())
    altura_util = ALTURA - MARGEM_S - MARGEM_I

    def medir(elemento):
        if isinstance(elemento, KeepTogether):
            # O KeepTogether devolve altura infinita quando o conteúdo passa do
            # espaço oferecido; a soma das partes é a medida real.
            return sum(medir(c) for c in elemento._content)
        try:
            return elemento.wrapOn(tela, UTIL, altura_util)[1]
        except Exception:
            return 0.0

    def inicio_divisivel(elemento):
        """A menor parte de um bloco grande que desce para a página: até a primeira linha da tabela."""
        if isinstance(elemento, KeepTogether):
            soma = 0.0
            for parte in elemento._content:
                if isinstance(parte, Table):
                    return soma + inicio_divisivel(parte)
                soma += medir(parte)
            return soma
        if isinstance(elemento, Table):
            try:
                elemento.wrapOn(tela, UTIL, altura_util)
                repetidas = elemento.repeatRows
                n = (repetidas if isinstance(repetidas, int) else len(repetidas)) + 1
                return float(sum(elemento._rowHeights[:n]))
            except Exception:
                return 0.25 * altura_util
        return 0.25 * altura_util

    saida = []
    i = 0
    while i < len(fluxo):
        elemento = fluxo[i]
        if not _titulo_amarrado(elemento) or (saida and _titulo_amarrado(saida[-1])):
            saida.append(elemento)
            i += 1
            continue
        necessario = 0.0
        k = i
        while k < len(fluxo) and (_titulo_amarrado(fluxo[k]) or isinstance(fluxo[k], _Spacer)):
            necessario += medir(fluxo[k])
            k += 1
        if k < len(fluxo) and not isinstance(fluxo[k], PageBreak):
            primeiro = fluxo[k]
            if isinstance(primeiro, Paragraph):
                # O parágrafo se divide: basta caber o começo dele.
                h = min(medir(primeiro), 3.2 * primeiro.style.leading)
            else:
                h = medir(primeiro)
                # A equação desce com a tabela de variáveis logo abaixo dela.
                if isinstance(primeiro, Table):
                    m = k + 1
                    while m < len(fluxo) and isinstance(fluxo[m], _Spacer):
                        h += medir(fluxo[m])
                        m += 1
                    if m < len(fluxo) and isinstance(fluxo[m], KeepTogether):
                        h += medir(fluxo[m])
                if h > altura_util:
                    # Bloco maior que a página se divide de qualquer modo, e a tabela
                    # só se divide depois do cabeçalho e da primeira linha: é isso,
                    # com a legenda, que tem de caber junto do título.
                    h = min(inicio_divisivel(primeiro), altura_util)
                    if isinstance(primeiro, KeepTogether):
                        # O reportlab leva para a página seguinte, inteiro, o bloco
                        # indivisível maior que o espaço que resta, mesmo quando ele
                        # é maior que a página, e o título ficava sozinho no pé da
                        # página («A cadeia de cálculo», seção 10, na montagem da
                        # 0.2.0). Maior que a página, a legenda e a tabela seguem
                        # soltas, e a quebra condicional acima as mantém juntas.
                        fluxo[k:k + 1] = list(primeiro._content)
            necessario += h
        # Folga para o espaçamento que o reportlab acrescenta entre os blocos.
        saida.append(CondPageBreak(necessario * 1.08 + 14))
        saida.append(elemento)
        i += 1
    return saida


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
    legenda_pendente = []
    while i < len(linhas):
        linha = linhas[i]
        cru = linha.rstrip()

        # equação numerada: o número sai entre parênteses, à direita
        m_eq = re.match(r"^```equacao:([^:`]+):(\d+)\s*$", cru)
        if m_eq:
            fecha_paragrafo(acumulado)
            i += 1
            linhas_eq = []
            while i < len(linhas) and not linhas[i].startswith("```"):
                linhas_eq.append(linhas[i].rstrip())
                i += 1
            i += 1
            nome_eq = m_eq.group(1).strip()
            imagem_eq = EQUACOES.get(nome_eq)
            if imagem_eq and os.path.exists(imagem_eq):
                from reportlab.lib.utils import ImageReader
                lx, ly = ImageReader(imagem_eq).getSize()
                # A imagem e composta a 320 dpi; 72 pontos por polegada dao a
                # medida em pontos, e o teto evita que uma equacao longa
                # invada a margem.
                largura_eq = min(lx * 72.0 / 320.0, UTIL - 2.6 * cm)
                corpo_eq = Image(imagem_eq, width=largura_eq,
                                 height=largura_eq * ly / float(lx),
                                 hAlign="CENTER")
            else:
                corpo_eq = Paragraph(
                    inline(NL.join(linhas_eq)).replace(NL, "<br/>"), E["equacao"])
            numero_eq = Paragraph("(" + m_eq.group(2) + ")", E["eq_numero"])
            tabela_eq = Table([[corpo_eq, numero_eq]],
                              colWidths=[UTIL - 2.2 * cm, 2.2 * cm])
            tabela_eq.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]))
            fluxo += [Spacer(1, 6), tabela_eq, Spacer(1, 6)]
            continue

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

        # legenda de tabela, que vem antes dela
        m_leg = re.match(r"^<!--\s*tabela:\s*(.+?)\s*-->\s*$", cru)
        if m_leg:
            fecha_paragrafo(acumulado)
            legenda_pendente.append(m_leg.group(1))
            i += 1
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
                if legenda_pendente:
                    # A legenda ja vem numerada da montagem, que e quem conhece
                    # a ordem de leitura do manual inteiro. Ela viaja junto com
                    # a tabela: legenda no pe de uma pagina e tabela na
                    # seguinte nao identifica coisa nenhuma.
                    legenda = Paragraph(inline(legenda_pendente.pop(0)),
                                        E["legenda_tabela"])
                    fluxo += [Spacer(1, 6),
                              KeepTogether([legenda, Spacer(1, 2), tabela]),
                              Spacer(1, 10)]
                else:
                    fluxo += [Spacer(1, 2), tabela, Spacer(1, 10)]
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
            if bruto and bruto[0].startswith("**" + T("aprofundamento")):
                aprof = True
                m_et = re.match(r"^\*\*" + T("aprofundamento") + r":?\s*([^*]*)\.?\*\*\s*(.*)$",
                                bruto[0])
                if m_et:
                    etiqueta = (m_et.group(1) or "").strip().rstrip(".")
                    bruto[0] = m_et.group(2).strip()

            estilo_texto = "aprof" if aprof else "cita"
            dentro = []
            if aprof:
                rotulo = T("aprofundamento").upper()
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
                # A figura ocupa toda a largura útil: reduzi-la a 15 cm
                # encolhia junto os rótulos, que já são pequenos no desenho.
                # A altura é limitada para que uma figura alta não expulse da
                # página o texto que a explica.
                largura = UTIL
                altura = largura * ly / float(lx)
                if altura > ALTURA_MAX_FIGURA:
                    largura *= ALTURA_MAX_FIGURA / altura
                    altura = ALTURA_MAX_FIGURA
                fluxo.append(Image(caminho, width=largura, height=altura))
            i += 1
            continue

        # títulos
        # O capítulo abre em folha própria; a seção, em página nova. A folha
        # de abertura não leva a quebra de baixo: a da seção seguinte é a
        # mesma, e duas produziriam uma folha em branco no meio.
        if cru.startswith("# ") and not cru.startswith("## "):
            fecha_paragrafo(acumulado)
            titulo = cru[2:].strip()
            primeira_parte = False
            fluxo += [PageBreak(), Spacer(1, 3.2 * cm),
                      Paragraph(inline(titulo), E["parte"])]
            i += 1
            continue
        if cru.startswith("## ") and not cru.startswith("### "):
            fecha_paragrafo(acumulado)
            titulo = cru[3:].strip()
            if titulo.lower().startswith(T("sumario")):
                fluxo += [PageBreak(), Paragraph(inline(titulo), E["h2"])]
            else:
                if fluxo:
                    fluxo.append(PageBreak())
                fluxo.append(Paragraph(inline(titulo), E["cap"]))
            i += 1
            continue
        # O titulo de subsecao nao fica sozinho no pe da pagina: ele e
        # marcado para descer junto com o que vier abaixo dele.
        if cru.startswith("### ") and not cru.startswith("#### "):
            fecha_paragrafo(acumulado)
            fluxo.append(_com_o_proximo(Paragraph(inline(cru[4:].strip()),
                                                  E["h2"])))
            i += 1
            continue
        if cru.startswith("#### "):
            fecha_paragrafo(acumulado)
            fluxo.append(_com_o_proximo(Paragraph(inline(cru[5:].strip()),
                                                  E["h3"])))
            i += 1
            continue

        # legenda de figura: linha só de itálico logo após a imagem
        if re.match(r"^\*[^*].*\*$", cru) and fluxo and isinstance(
                fluxo[-1], Image):
            fecha_paragrafo(acumulado)
            # A legenda não se separa da figura: imagem no pé de uma página e
            # legenda no alto da seguinte obriga o leitor a folhear para saber
            # o que acabou de ver.
            imagem = fluxo.pop()
            fluxo.append(KeepTogether([
                imagem, Spacer(1, 2),
                Paragraph(inline(cru.strip("*")), E["legenda"])]))
            i += 1
            continue

        # régua
        if cru.strip() in ("---", "***", "___"):
            fecha_paragrafo(acumulado)
            fluxo.append(Spacer(1, 6))
            i += 1
            continue

        # listas. Um paragrafo aberto tem prioridade: a linha que comeca com
        # «2.» depois de «conforme a Equacao» e continuacao do paragrafo, e nao
        # o segundo item de uma lista.
        m = re.match(r"^(\s*)([-*]|\d+\.|[A-J]\.)\s+(.*)$", cru)
        if m and acumulado and m.group(2) not in ("-", "*"):
            m = None
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
        if isinstance(elemento, PageBreak):
            # O espaçador que fecha uma seção não serve antes da quebra, e, se não
            # cabe no pé da página, abre sozinho uma folha que a quebra deixa em
            # branco (três folhas assim na montagem da 0.2.0).
            while enxuto and type(enxuto[-1]) is Spacer:
                enxuto.pop()
        enxuto.append(elemento)
    return enxuto


#: A marca do programa, na folha de rosto.
LOGO = os.path.join(os.path.dirname(AQUI), "icons", "Triton2.png")


def folha_de_rosto(titulo="Manual do Triton", volume=None):
    capa = [Spacer(1, 3.0 * cm)]
    if os.path.exists(LOGO):
        from reportlab.lib.utils import ImageReader
        lx, ly = ImageReader(LOGO).getSize()
        largura = 4.6 * cm
        capa += [Image(LOGO, width=largura, height=largura * ly / float(lx),
                       hAlign="LEFT"),
                 Spacer(1, 1.2 * cm)]
    else:
        capa += [Spacer(1, 2.0 * cm)]
    return capa + [
        Paragraph(titulo, E["capa_titulo"]),
    ] + ([Paragraph(volume, E["capa_sub"])] if volume else []) + [
        Paragraph(f"Versão {VERSAO}", E["capa_sub"]),
        Spacer(1, 0.8 * cm),
        Paragraph("Simulação de sistemas de aproveitamento de água pluvial "
                  "em edificações", E["capa_sub"]),
        Spacer(1, 4.2 * cm),
        Paragraph("Igor Catão Martins Vaz &amp; Enedir Ghisi", E["capa_sub"]),
        Spacer(1, 0.5 * cm),
        Paragraph("Grupo de Pesquisa em Ambientes Sustentáveis",
                  E["capa_sub"]),
        Paragraph("Universidade Federal de Santa Catarina", E["capa_sub"]),
        Spacer(1, 1.2 * cm),
        Paragraph("Florianópolis, 2026", E["capa_sub"]),
        PageBreak(),
    ]


def titulos_no_pe_da_pagina(caminho):
    """Páginas cujo último bloco de texto é um título numerado.

    Um título sozinho no pé da página, com o conteúdo na folha seguinte, é o
    defeito que o professor pediu para nunca aparecer. A conferência lê o PDF
    pronto, porque só a paginação final mostra onde cada título caiu.
    """
    try:
        import fitz
    except ImportError:
        return []
    achados = []
    with fitz.open(caminho) as pdf:
        for numero, pagina in enumerate(pdf, 1):
            altura = pagina.rect.height
            blocos = [b for b in pagina.get_text("blocks")
                      if b[6] == 0 and b[4].strip() and 60 < b[1] < altura - 60]
            if not blocos:
                continue
            bloco = max(blocos, key=lambda b: b[3])
            ultimo = " ".join(bloco[4].split())
            # Só é título o que tem corpo de título: as entradas do sumário, como
            # «Apêndice J — Arquivos de exemplo», saem no corpo do texto.
            tamanhos = [sp["size"] for b in pagina.get_text("dict")["blocks"]
                        if b.get("type") == 0 and abs(b["bbox"][3] - bloco[3]) < 1
                        for ln in b["lines"] for sp in ln["spans"]]
            if tamanhos and max(tamanhos) < 10.5:
                continue
            if (re.match(r"^(\d+|[A-J])(\.\d+)+\.\s+\S", ultimo)
                    or re.match(r"^" + T("apendice") + r" [A-J] —", ultimo)) and len(ultimo) < 120:
                achados.append((numero, ultimo))
    return achados


#: A capa do manual completo; a de cada volume está em gerar_mini_manuais.py.
CAPA_COMPLETA = dict(
    painel=os.path.join(AQUI, "figuras", "capas", "capa_completo.png"),
    cor="#8ecae6", numero=None, titulo="Manual do Triton",
    frase="Simulação de sistemas de aproveitamento de água pluvial em edificações: "
          "o método, o tutorial, os guias e as referências, num volume só.",
    conteudo="Edição completa · sete capítulos e dez apêndices",
)


#: A capa do manual em inglês, em manual/en.
CAPA_EN = dict(CAPA_COMPLETA, titulo="Triton User Manual",
               frase="Simulation of rainwater harvesting systems in buildings: the method, "
                     "the tutorial, the guides and the references, in one volume.",
               conteudo="Complete edition · six chapters and ten appendices")


def main(idioma="pt"):
    if idioma == "en":
        pasta = os.path.join(AQUI, "en")
        sys.path.insert(0, pasta)
        import textos_en
        return compor_pdf(os.path.join(pasta, textos_en.ARQUIVO_MONTADO),
                          os.path.join(pasta, textos_en.ARQUIVO_PDF),
                          titulo="Triton User Manual", cabecalho=TEXTOS["en"]["cabecalho"],
                          capa_info=CAPA_EN, idioma="en")
    return compor_pdf(ENTRADA, SAIDA, capa_info=CAPA_COMPLETA)


def compor_pdf(entrada, saida, titulo="Manual do Triton", volume=None,
               cabecalho=f"Manual do Triton {VERSAO}", capa_info=None, idioma="pt"):
    """Compõe o PDF de um manual montado: o completo, um mini manual ou o em inglês."""
    global IDIOMA_PDF
    IDIOMA_PDF = idioma
    ENTRADA, SAIDA = entrada, saida
    if not os.path.exists(ENTRADA):
        print("manual ainda não montado; rode manual/gerar.py")
        return 1
    texto = open(ENTRADA, encoding="utf-8").read()
    EQUACOES.clear()

    # As equacoes sao compostas em tipografia matematica antes de o documento
    # ser montado; sem elas, o bloco cai no texto monoespacado.
    try:
        import sys as _sys
        _sys.path.insert(0, AQUI)
        from gerar_equacoes import compor_do_manual
        EQUACOES.update(compor_do_manual(ENTRADA))
        print(f"  {len(EQUACOES)} equações compostas")
    except Exception as erro:
        print(f"  equações em texto simples: {erro}")

    # A folha de rosto do Markdown é substituída pela do PDF, que ocupa a
    # página inteira; o sumário gerado permanece.
    # A folha de rosto do PDF substitui o bloco de título do Markdown, que vai
    # até a primeira régua; o resto do preâmbulo — como usar, e o sumário —
    # permanece.
    corpo = texto
    marca = NL + "---" + NL
    if corpo.lstrip().startswith("# Triton") and marca in corpo:
        corpo = corpo.split(marca, 1)[1].lstrip()

    # O PDF costuma estar aberto num leitor quando se regera o manual, e no
    # Windows o arquivo aberto nao pode ser sobrescrito. Compoe-se ao lado e
    # troca-se no fim, o que tambem evita deixar um PDF truncado se algo falhar.
    provisorio = SAIDA + ".novo"
    doc = Manual(provisorio, pagesize=A4,
                 leftMargin=MARGEM_E, rightMargin=MARGEM_D,
                 topMargin=MARGEM_S, bottomMargin=MARGEM_I,
                 title=cabecalho,
                 author="Igor Catão Martins Vaz; Enedir Ghisi",
                 subject=T("assunto"))
    quadro = Frame(MARGEM_E, MARGEM_I, UTIL,
                   ALTURA - MARGEM_S - MARGEM_I, id="corpo",
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([
        PageTemplate(id="capa", frames=[quadro], onPage=capa),
        PageTemplate(id="miolo", frames=[quadro], onPage=moldura),
    ])

    doc.cabecalho = cabecalho
    doc.capa = capa_info
    # A troca de modelo vem antes da quebra: depois dela, só valeria a partir da
    # página 3, e a página 2 redesenhava a capa por baixo do texto.
    rosto = ([Spacer(1, 1), NextPageTemplate("miolo"), PageBreak()] if capa_info
             else folha_de_rosto(titulo, volume)[:-1] + [NextPageTemplate("miolo"), PageBreak()])
    fluxo = rosto + amarrar_titulos(converter(corpo))
    doc.build(fluxo)
    orfaos = titulos_no_pe_da_pagina(provisorio)
    if orfaos:
        print(f"  AVISO: {len(orfaos)} título(s) no pé da página, sem conteúdo abaixo:")
        for pagina, titulo in orfaos:
            print(f"    página {pagina}: {titulo}")

    try:
        os.replace(provisorio, SAIDA)
    except PermissionError:
        print("o PDF esta aberto noutro programa; feche-o e rode de novo.")
        print("a versao nova ficou em " + os.path.basename(provisorio))
        return 1

    tamanho = os.path.getsize(SAIDA) / 1024.0 / 1024.0
    print(f"PDF: {os.path.basename(SAIDA)}  {doc.page} páginas, "
          f"{tamanho:.1f} MB")
    # O programa mostra as páginas de cada volume lendo este arquivo, que vai junto
    # com os PDFs (triton/ui/tab_documentation.py): o número não fica para trás.
    indice = os.path.join(os.path.dirname(SAIDA), "paginas.json")
    try:
        paginas = json.load(open(indice, encoding="utf-8"))
    except (OSError, ValueError):
        paginas = {}
    paginas[os.path.basename(SAIDA)] = doc.page
    with open(indice, "w", encoding="utf-8", newline="\n") as f:
        json.dump(dict(sorted(paginas.items())), f, ensure_ascii=False, indent=1)
    return 0


if __name__ == "__main__":
    import argparse
    _args = argparse.ArgumentParser(description="Compõe o PDF do manual.")
    _args.add_argument("--idioma", choices=("pt", "en"), default="pt")
    sys.exit(main(_args.parse_args().idioma))
