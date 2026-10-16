# -*- coding: utf-8 -*-
"""Monta o site de documentação a partir do manual da edição.

O site não tem texto próprio além da página inicial: as seções saem do manual,
que `gerar.py` monta das mesmas partes do PDF. Por isso a numeração, as figuras,
as tabelas e as equações são as mesmas nos dois, e uma correção no manual chega
ao site na próxima montagem.

O idioma do site é escolhido por `--idioma`, como em `gerar.py` e `gerar_pdf.py`:

- ``en``    (padrão na edição INT): o manual vem de `manual/en/partes` e
  `manual/en/apendices`, montado em memória (num arquivo temporário: o manual
  publicado em `manual/en` não é tocado), e a página usa `site_modelo.html` e
  `site_interativas.js`, escritos em inglês britânico.
- ``pt-pt`` (edição PRT, ainda não implementado): o mecanismo já está aqui. Falta
  preencher a entrada ``pt-pt`` de ``IDIOMAS`` (rótulos, volumes, pastas, locale,
  moeda), escrever `site_modelo.pt-pt.html` e `site_interativas.pt-pt.js` (os
  textos da página e dos painéis ficam nesses dois arquivos, um par por idioma,
  e não em chaves espalhadas) e fazer `gerar.usar_idioma` e
  `gerar_figuras_interativas.py` (que emite alguns textos em inglês) conhecerem
  o idioma. Até lá, ``--idioma pt-pt`` para com uma mensagem clara.

O resultado é uma página só (`site/index.html`), com as seções embutidas e
navegação por âncora (`#/2.6`), que abre direto do disco, sem servidor, e ao
lado as figuras, o PDF e as miniaturas das capas.

Uso:
    python manual/gerar_site.py --idioma en
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)

import gerar as g  # noqa: E402
from triton import __version__ as VERSAO  # noqa: E402

#: O que muda de um idioma para outro e que vive no gerador (a página e os painéis têm o
#: texto no par modelo/JS do idioma). Para acrescentar um idioma, acrescente uma entrada.
IDIOMAS = {
    "en": dict(
        html_lang="en", locale="en-GB", moeda="US$", pronto=True,
        # como `gerar.usar_idioma` chama o idioma
        idioma_do_manual="en",
        pasta_do_manual="en", arquivo_pdf="Triton-User-Manual.pdf",
        modelo="site_modelo.html", interativas="site_interativas.js",
        saida="site",
        # rótulos que o manual montado escreve (os mesmos de en/textos_en.py)
        figura="Figure", tabela="Table", equacao="Equation", apendice="Appendix",
        secao_sg="section", aprofundamento="In depth",
        # o que as remissões em texto corrido dizem
        re_secao=r"(\b[Ss]ections? |\band |, )(\d+\.\d+(?:\.\d+)*)\b",
        re_apendice=r"\b[Aa]ppendi(?:x|ces) [A-J](?:(?:, | and | or )[A-J])*\b(?![.\w])",
        data_fmt="%d %B %Y",
        # a página de versões: como o capítulo de histórico escreve cada entrada
        historico=dict(
            arquivo="38_historico_de_versoes.md", pasta="partes",
            cabecalho=r"^## Version (\S+(?: \([^)]*\))?) — (.+)$", comeco=r"^## (?=Version \d)",
            fora=r"^## (?!Version \d)", resumo=r"^> \*\*In one sentence\.\*\*\s*(.+?)(?=\n\s*\n|\Z)",
            secoes=("What is new", "Fixes that change results", "Fixes that do not change results",
                    "Documentation"),
            altera="Fixes that change results", nao_altera="Fixes that do not change results"),
        # os volumes (um por capítulo): arquivo da capa, título, capítulo, frase
        volumes=[
            ("1-comece-aqui", "Start here", 1,
             "What the program does, how to install it and where to enter, depending on your goal."),
            ("2-metodo", "The method", 2,
             "The equations, criteria and sources behind every number the program publishes."),
            ("3-guias", "Guides", 3,
             "Use cases: other cities, a future climate, tariffs, variable demand, batches, "
             "sensitivity and export."),
            ("4-tutorial", "Tutorial", 4,
             "A house in New York, from the first datum to the recommended volume."),
            ("5-confiabilidade", "Mistakes, limits and reliability", 5,
             "The commonest mistakes, the limits of the model and how the program is verified."),
            ("6-versoes", "Fixes, bugs and versioning", 6,
             "Verification, error messages, version history and how to report a problem."),
            ("7-modulacao", "Probabilistic modulation", 7,
             "The study redone with sampled assumptions: variables, distributions, reading the "
             "results and the limits of the method."),
            ("8-apendices", "Appendices", 8,
             "Parameters, processes, emission factors, tariffs, climate data, formats, glossary "
             "and references."),
        ],
    ),
    "pt-pt": dict(
        html_lang="pt-PT", locale="pt-PT", moeda="€", pronto=False,
        idioma_do_manual="pt-pt", pasta_do_manual=None, arquivo_pdf=None,
        modelo="site_modelo.pt-pt.html", interativas="site_interativas.pt-pt.js",
        saida="site_pt-pt",
        figura="Figura", tabela="Tabela", equacao="Equação", apendice="Apêndice",
        secao_sg="secção", aprofundamento="Aprofundamento",
        re_secao=r"(\b[Ss]ec(?:ção|ções) |\be |, )(\d+\.\d+(?:\.\d+)*)\b",
        re_apendice=r"\b[Aa]pêndices? [A-J](?:(?:, | e | ou )[A-J])*\b(?![.\w])",
        data_fmt="%d/%m/%Y",
        historico=None,   # por escrever com o manual PRT
        volumes=[],       # idem
    ),
}
L = dict(IDIOMAS["en"])          # o idioma ativo; trocado por usar_idioma_do_site()

SITE = os.path.join(AQUI, L["saida"])
MANUAL = None                    # o manual montado (arquivo temporário)
PASTA_TEMP = None

#: O volume de cada capítulo, para a cor.
VOLUME_DO_CAPITULO = {
    1: "1-comece-aqui", 2: "2-metodo", 3: "3-guias", 4: "4-tutorial",
    5: "5-confiabilidade", 6: "6-versoes", 7: "7-modulacao", 8: "8-apendices",
}


def usar_idioma_do_site(idioma):
    """Escolhe o idioma do site; pára com mensagem clara se ele ainda não está pronto."""
    global L, SITE
    if idioma not in IDIOMAS:
        raise SystemExit(f"idioma desconhecido: {idioma} (disponíveis: {', '.join(IDIOMAS)})")
    cfg = IDIOMAS[idioma]
    if not cfg["pronto"]:
        raise SystemExit(
            f"o site em «{idioma}» ainda não foi implementado: faltam o manual montado nesse idioma, "
            f"{cfg['modelo']}, {cfg['interativas']} e os volumes/histórico em IDIOMAS['{idioma}'] "
            "(veja o cabeçalho de gerar_site.py).")
    L = dict(cfg)
    SITE = os.path.join(AQUI, L["saida"])
    return cfg


def montar_manual():
    """Monta o manual do idioma ativo num arquivo temporário e devolve o caminho.

    Usa a mesma montagem de `gerar.py --idioma …`, mas escreve fora de `manual/`,
    para que o site reflita o texto-fonte de agora sem alterar o manual publicado.
    """
    global PASTA_TEMP
    g.usar_idioma(L["idioma_do_manual"])
    PASTA_TEMP = tempfile.mkdtemp(prefix=".triton_site_", dir=AQUI)
    destino = os.path.join(PASTA_TEMP, "manual.md")
    g.DESTINO = destino
    saida_padrao, sys.stdout = sys.stdout, open(os.devnull, "w")
    try:
        g.main()
    finally:
        sys.stdout.close()
        sys.stdout = saida_padrao
    return destino


# ── o texto do manual, seção por seção ────────────────────────────────────────

def _secoes_do_manual(texto):
    """Divide o manual montado em capítulos e seções, a partir do capítulo 1."""
    corpo = texto[texto.index("\n# 1. "):]
    capitulos = []
    atual = None
    secao = None
    ap = re.escape(L["apendice"])
    for linha in corpo.split("\n"):
        m_cap = re.match(r"^# (?:(\d+)\. )?(.+)$", linha)
        m_sec = re.match(rf"^## (?:(\d+\.\d+)\. |{ap} ([A-J]) — )(.+)$", linha)
        if m_cap and not linha.startswith("## "):
            numero = int(m_cap.group(1)) if m_cap.group(1) else len(capitulos) + 1
            atual = {"n": numero, "titulo": m_cap.group(2).strip(), "secoes": [],
                     "apendice": m_cap.group(1) is None}
            capitulos.append(atual)
            secao = None
            continue
        if m_sec and atual is not None:
            ident = m_sec.group(1) or m_sec.group(2)
            rotulo = m_sec.group(1) or f"{L['apendice']} {m_sec.group(2)}"
            secao = {"id": ident, "rotulo": rotulo, "titulo": m_sec.group(3).strip(),
                     "md": []}
            atual["secoes"].append(secao)
            continue
        if secao is not None:
            secao["md"].append(linha)
    for cap in capitulos:
        for s in cap["secoes"]:
            s["md"] = "\n".join(s["md"]).strip().strip("-").strip()
    return capitulos


def _markdown():
    from markdown_it import MarkdownIt
    return MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")


def _equacoes():
    """{número: arquivo da imagem}, compostas pelo mesmo gerador do PDF."""
    from gerar_equacoes import compor_do_manual
    imagens = compor_do_manual(MANUAL)
    numeros = dict(re.findall(r"^```equacao:([^:\n]+):(\d+)\s*$",
                              open(MANUAL, encoding="utf-8").read(), flags=re.M))
    return {int(numeros[n]): os.path.basename(p) for n, p in imagens.items() if n in numeros}


def _preparar(md, equacoes):
    """Troca as convenções do manual por HTML antes do Markdown."""
    # equações compostas: bloco ```equacao:nome:N ... ```
    def eq(m):
        numero = int(m.group(1))
        arquivo = equacoes.get(numero)
        img = (f'<img src="figuras/equacoes/{arquivo}" alt="{L["equacao"]} {numero}" loading="lazy">'
               if arquivo else f"<pre>{html.escape(m.group(2).strip())}</pre>")
        return (f'\n<figure class="eq" id="eq-{numero}">{img}'
                f'<span class="eqn">({numero})</span></figure>\n')
    md = re.sub(r"^```equacao:[^:\n]+:(\d+)\s*\n(.*?)^```\s*$", eq, md, flags=re.M | re.S)

    # legenda de tabela, que o gerar.py escreve num comentário
    def tab(m):
        numero, resto = m.group(1), m.group(2)
        return f'<p class="tab-cap" id="tab-{numero}"><b>{L["tabela"]} {numero}</b>{resto}</p>\n'
    md = re.sub(rf"^<!-- tabela: \*\*{L['tabela']} (\d+)\*\*(.*?) -->\s*$", tab, md, flags=re.M)

    # destaque ==assim==
    md = re.sub(r"==(.+?)==", r"<mark>\1</mark>", md, flags=re.S)

    # figuras: imagem seguida da legenda em itálico
    def fig(m):
        arquivo, numero, legenda = m.group(1), m.group(2), m.group(3)
        return (f'\n<figure class="fig" id="fig-{numero}" data-arquivo="{arquivo}"><a href="figuras/{arquivo}" '
                f'target="_blank" rel="noopener"><img src="figuras/{arquivo}" alt="{L["figura"]} {numero}" '
                f'loading="lazy"></a><figcaption><b>{L["figura"]} {numero}</b> — '
                f'{_inline(legenda)}</figcaption></figure>\n')
    md = re.sub(rf"^!\[[^\]]*\]\((?:\.\./)?figuras/([^)]+)\)\s*\n+\*{L['figura']} (\d+) — (.+?)\*\s*$",
                fig, md, flags=re.M)

    # o bloco de aprofundamento vira recolhível
    apro = L["aprofundamento"]
    linhas, saida, i = md.split("\n"), [], 0
    while i < len(linhas):
        if linhas[i].startswith(f"> **{apro}"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i][1:].lstrip() if linhas[i] != ">" else "")
                i += 1
            m = re.match(rf"\*\*({apro}[^*]*)\*\*\s*(.*)", bloco[0])
            titulo = m.group(1).rstrip(".") if m else apro
            bloco[0] = m.group(2) if m else bloco[0]
            corpo = _markdown().render("\n".join(bloco))
            saida.append(f'\n<details class="aprof"><summary>{_inline(titulo)}</summary>'
                         f'{corpo}</details>\n')
            continue
        saida.append(linhas[i])
        i += 1
    return "\n".join(saida)


def _inline(texto):
    return _markdown().renderInline(texto)


def _ancoras(html_secao, ident):
    """Dá id e âncora aos títulos internos e devolve o quadro «nesta página»."""
    toc = []

    def titulo(m):
        nivel, conteudo = m.group(1), m.group(2)
        limpo = re.sub(r"<[^>]+>", "", conteudo)
        num = re.match(r"^([0-9A-J]+(?:\.\d+)+)\.\s*(.*)$", limpo)
        alvo = "t-" + (num.group(1) if num else re.sub(r"\W+", "-", limpo.lower()).strip("-"))
        alvo = alvo.replace(".", "-")
        if nivel == "3":
            toc.append({"id": alvo, "titulo": limpo})
        return (f'<h{nivel} id="{alvo}">{conteudo}'
                f'<a class="ancora" href="#/{ident}/{alvo}" aria-label="Link">¶</a></h{nivel}>')
    corpo = re.sub(r"<h([34])>(.*?)</h\1>", titulo, html_secao)
    return corpo, toc


def _ligar_remissoes(conteudo, onde_esta):
    """Transforma «section 2.6», «Appendix C», «Equation 12» em links."""
    partes = re.split(r"(<[^>]+>)", conteudo)
    dentro = 0
    saida = []
    for parte in partes:
        if parte.startswith("<"):
            if re.match(r"<(a|code|h[1-6]|pre)\b", parte):
                dentro += 1
            elif re.match(r"</(a|code|h[1-6]|pre)>", parte):
                dentro = max(0, dentro - 1)
            saida.append(parte)
            continue
        if dentro:
            saida.append(parte)
            continue

        def secao(m):
            alvo = m.group(2)
            base = ".".join(alvo.split(".")[:2])
            if base not in onde_esta["secao"]:
                return m.group(0)
            ancora = "" if alvo == base else "/t-" + alvo.replace(".", "-")
            return f'{m.group(1)}<a href="#/{base}{ancora}">{alvo}</a>'
        parte = re.sub(L["re_secao"], secao, parte)

        def apendice(m):
            def letra(x):
                return (f'<a href="#/{x.group(0)}">{x.group(0)}</a>'
                        if x.group(0) in onde_esta["secao"] else x.group(0))
            cabeca, _, resto = m.group(0).partition(" ")
            return cabeca + " " + re.sub(r"[A-J]", letra, resto)
        parte = re.sub(L["re_apendice"], apendice, parte)

        def objeto(m):
            tipo, n = m.group(1), m.group(2)
            chave = {L["figura"]: "fig", L["tabela"]: "tab", L["equacao"]: "eq"}[tipo]
            sec = onde_esta[chave].get(int(n))
            if not sec:
                return m.group(0)
            return f'<a href="#/{sec}/{chave}-{n}">{tipo} {n}</a>'
        parte = re.sub(rf"\b({L['figura']}|{L['tabela']}|{L['equacao']}) (\d+)\b", objeto, parte)
        saida.append(parte)
    return "".join(saida)


def montar_conteudo():
    texto = open(MANUAL, encoding="utf-8").read()
    capitulos = _secoes_do_manual(texto)
    equacoes = _equacoes()
    md = _markdown()
    onde_esta = {"secao": set(), "fig": {}, "tab": {}, "eq": {}}
    for cap in capitulos:
        for s in cap["secoes"]:
            onde_esta["secao"].add(s["id"])
            corpo = md.render(_preparar(s["md"], equacoes))
            s["html"], s["toc"] = _ancoras(corpo, s["id"])
            for chave in ("fig", "tab", "eq"):
                for n in re.findall(rf'id="{chave}-(\d+)"', s["html"]):
                    onde_esta[chave][int(n)] = s["id"]
    for cap in capitulos:
        cap["volume"] = VOLUME_DO_CAPITULO.get(cap["n"])
        for s in cap["secoes"]:
            s["html"] = _ligar_remissoes(s["html"], onde_esta)
            texto_puro = re.sub(r"<[^>]+>", " ", s["html"])
            s["texto"] = re.sub(r"\s+", " ", html.unescape(texto_puro)).strip()
            del s["md"]
    return capitulos


# ── a curva interativa ────────────────────────────────────────────────────────

def dados_da_curva():
    """Potencial, dias plenos e extravasamento do projeto do tutorial, em grade."""
    from gerar_tabelas import _config_tutorial, _serie
    from triton.core.simulation import run_single_simulation
    serie = _serie()
    cfg = dict(_config_tutorial())
    fracoes = [round(0.10 + 0.02 * i, 2) for i in range(26)]
    volumes = list(range(0, 20001, 500))
    grade = {}
    for f in fracoes:
        cfg["rainwater_share"] = f
        linhas = []
        for v in volumes:
            r = run_single_simulation(precip_data=serie, lower_tank_vol=float(v), **cfg)
            linhas.append([round(r.potential_potable_savings_pct, 2),
                           round(r.pct_days_full_satisfaction, 1),
                           round(r.avg_spilled_l_day, 0)])
        grade[f"{f:.2f}"] = linhas
    return {"volumes": volumes, "fracoes": fracoes, "grade": grade}


# ── arquivos ao lado da página ────────────────────────────────────────────────

#: Arquivos de figuras que a edição não publica no site (dados e mapas de outra edição).
IGNORAR_NO_SITE = ("CLIMBra*", "fig42_*", "fig43_*")


def _copiar_arquivos():
    destino = os.path.join(SITE, "figuras")
    if os.path.exists(destino):
        shutil.rmtree(destino)
    shutil.copytree(os.path.join(AQUI, "figuras"), destino,
                    ignore=shutil.ignore_patterns("capas", *IGNORAR_NO_SITE))
    img = os.path.join(SITE, "img")
    os.makedirs(img, exist_ok=True)
    from PIL import Image
    for nome in os.listdir(os.path.join(AQUI, "figuras", "capas")):
        with Image.open(os.path.join(AQUI, "figuras", "capas", nome)) as im:
            im = im.convert("RGB")
            im.thumbnail((900, 900))
            im.save(os.path.join(img, nome.replace(".png", ".jpg")), quality=82)
    logo = os.path.join(RAIZ, "icons", "Triton2.png")
    if os.path.exists(logo):
        with Image.open(logo) as im:
            im.thumbnail((160, 160))
            im.save(os.path.join(img, "logo.png"))
    pdf = os.path.join(SITE, "pdf")
    os.makedirs(pdf, exist_ok=True)
    # Só o manual completo do idioma: os volumes avulsos em PDF não existem neste idioma.
    origem = os.path.join(AQUI, L["pasta_do_manual"], L["arquivo_pdf"])
    if os.path.exists(origem):
        shutil.copy2(origem, pdf)


def historico_de_versoes():
    """As versões publicadas, como dado, para a página de versões do site.

    A fonte é o capítulo de histórico do manual do idioma, a mesma do CHANGELOG.md:
    escrever num lugar e publicar em vários.
    """
    cfg = L["historico"]
    caminho = os.path.join(AQUI, L["pasta_do_manual"], cfg["pasta"], cfg["arquivo"])
    texto = open(caminho, encoding="utf-8").read()
    md = _markdown()
    versoes = []
    partes = re.split(cfg["comeco"], texto, flags=re.M)[1:]
    for parte in partes:
        corte = re.search(cfg["fora"], parte, flags=re.M)
        bloco = ("## " + (parte[: corte.start()] if corte else parte)).rstrip()
        linhas = [x for x in bloco.split("\n") if not re.match(r"^<!--\s*tabela:", x.strip())]
        limpo = g.resolver_marcas("\n".join(linhas)).replace("==", "")
        limpo = re.sub(r"\n{3,}", "\n\n", limpo).strip()
        cab = limpo.splitlines()[0]
        m = re.match(cfg["cabecalho"], cab)
        if not m:
            raise SystemExit(f"entrada de versão fora do modelo: {cab}")
        corpo = limpo[len(cab):].strip()
        r = re.search(cfg["resumo"], corpo, flags=re.M | re.S)
        resumo = re.sub(r"\s*\n>\s*", " ", r.group(1)).strip() if r else ""
        secoes = {}
        for nome in cfg["secoes"]:
            a = re.search(rf"^### {re.escape(nome)}\s*\n(.*?)(?=^### |\Z)", corpo, flags=re.M | re.S)
            if a and a.group(1).strip():
                secoes[nome] = a.group(1).strip()

        def linhas_de_tabela(c):
            ls = [x for x in c.split("\n") if x.strip().startswith("|")]
            uteis = [x for x in ls if not re.match(r"^\|[\s:\-|]+\|$", x.strip())]
            return max(0, len(uteis) - 1)
        versoes.append({
            "versao": m.group(1), "data": m.group(2).strip(), "resumo": resumo,
            "secoes": [{"titulo": t, "html": md.render(c)} for t, c in secoes.items()],
            "altera_resultados": linhas_de_tabela(secoes.get(cfg["altera"], "")),
            "nao_altera_resultados": linhas_de_tabela(secoes.get(cfg["nao_altera"], "")),
        })
    return versoes


def indice_de_busca(capitulos, onde_interativas):
    """O que a busca encontra: seções, subseções, figuras, tabelas e equações.

    Quem procura raramente sabe em que seção a resposta está; sabe o nome da
    coisa. Por isso o índice não se limita ao texto das seções.
    """
    interativas = {o["numero"] for o in onde_interativas.values()}
    itens = []
    fg, tb = L["figura"], L["tabela"]
    for c in capitulos:
        for s in c["secoes"]:
            # O texto da seção não se repete aqui: a página o lê de POR_ID.
            itens.append({"t": "secao", "id": s["id"], "a": "",
                          "r": s["rotulo"], "n": s["titulo"]})
            for entrada in s["toc"]:
                itens.append({"t": "sub", "id": s["id"], "a": entrada["id"],
                              "r": s["rotulo"], "n": entrada["titulo"], "x": ""})
            # A legenda pode ter virado link pelas remissões, e por isso o
            # rótulo não é casado literalmente.
            for m in re.finditer(
                    rf'<figure class="fig" id="fig-(\d+)"[^>]*>.*?<figcaption>.*?'
                    rf'{fg} \d+.*?— (.*?)</figcaption>', s["html"], flags=re.S):
                numero = int(m.group(1))
                itens.append({"t": "interativa" if numero in interativas else "figura",
                              "id": s["id"], "a": f"fig-{numero}",
                              "r": f"{fg} {numero}",
                              "n": re.sub(r"<[^>]+>", "", m.group(2)).strip(), "x": ""})
            for m in re.finditer(rf'<p class="tab-cap" id="tab-(\d+)">.*?{tb} \d+.*?</b>(.*?)</p>',
                                 s["html"], flags=re.S):
                itens.append({"t": "tabela", "id": s["id"], "a": f"tab-{m.group(1)}",
                              "r": f"{tb} {m.group(1)}",
                              "n": re.sub(r"<[^>]+>", "", m.group(2)).strip(" —"), "x": ""})
    return itens


def _quantos_testes():
    try:
        saida = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"],
                               cwd=RAIZ, capture_output=True, text=True, timeout=300).stdout
        # Com -q, o pytest lista «arquivo: n» por arquivo; o total é a soma.
        por_arquivo = re.findall(r"^\S+\.py: (\d+)$", saida, re.M)
        if por_arquivo:
            return sum(int(n) for n in por_arquivo)
        m = re.search(r"(\d+) tests? collected", saida)
        return int(m.group(1)) if m else None
    except Exception:
        return None


def main(idioma="en"):
    global MANUAL
    usar_idioma_do_site(idioma)
    os.makedirs(SITE, exist_ok=True)
    MANUAL = montar_manual()
    try:
        capitulos = montar_conteudo()
        from gerar_capas import CORES
        volumes = [{"arquivo": a, "titulo": t, "frase": f, "cor": CORES[a], "capitulo": c}
                   for a, t, c, f in L["volumes"]]
        dados = {
            "i18n": {"lang": L["html_lang"], "locale": L["locale"], "moeda": L["moeda"]},
            "capitulos": capitulos,
            "volumes": volumes,
            "curva": dados_da_curva(),
            "revisao": date.today().strftime(L["data_fmt"]).lstrip("0"),
            "versao": VERSAO,
            "testes": _quantos_testes(),
            "secoes": sum(len(c["secoes"]) for c in capitulos),
            "figuras": sum(len(re.findall(r'<figure class="fig"', s["html"]))
                           for c in capitulos for s in c["secoes"]),
            "pdf_completo": L["arquivo_pdf"],
        }
        # As figuras interativas: os dados, e a seção e o número de cada uma.
        from gerar_figuras_interativas import dados as dados_interativos
        dados["interativas"] = dados_interativos()
        # A curva de retorno reaproveita a grade da página inicial.
        dados["interativas"]["fig02_curva_de_retorno.png"] = {"usa": "curva"}
        dados["onde_interativas"] = {}
        for c in capitulos:
            for s in c["secoes"]:
                for m in re.finditer(r'id="fig-(\d+)" data-arquivo="([^"]+)"', s["html"]):
                    if m.group(2) in dados["interativas"]:
                        dados["onde_interativas"][m.group(2)] = {
                            "secao": s["id"], "titulo": s["titulo"], "numero": int(m.group(1))}
        dados["versoes"] = historico_de_versoes()
        dados["busca"] = indice_de_busca(capitulos, dados["onde_interativas"])
    finally:
        shutil.rmtree(PASTA_TEMP, ignore_errors=True)
    modelo = open(os.path.join(AQUI, L["modelo"]), encoding="utf-8").read()
    modelo = modelo.replace("/*__INTERATIVAS__*/",
                            open(os.path.join(AQUI, L["interativas"]), encoding="utf-8").read())
    pagina = modelo.replace("/*__DADOS__*/null",
                            json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    # A página publicada como Artifact recebe o esqueleto do próprio publicador;
    # a que abre do disco precisa do seu, com doctype, para não cair no modo quirks.
    open(os.path.join(SITE, "artefato.html"), "w", encoding="utf-8").write(pagina)
    cabeca = (f"<!doctype html>\n<html lang=\"{L['html_lang']}\">\n<head>\n<meta charset=\"utf-8\">\n"
              "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, "
              "viewport-fit=cover\">\n")
    corpo = pagina.replace("<header", "</head>\n<body>\n<header", 1)
    open(os.path.join(SITE, "index.html"), "w", encoding="utf-8").write(
        cabeca + corpo + "\n</body>\n</html>\n")
    _copiar_arquivos()
    tamanho = os.path.getsize(os.path.join(SITE, "index.html")) / 1024 / 1024
    print(f"site: {os.path.relpath(SITE, AQUI)}/index.html  {dados['secoes']} seções, "
          f"{tamanho:.1f} MB")
    return 0


if __name__ == "__main__":
    import argparse
    _args = argparse.ArgumentParser(description="Monta o site de documentação.")
    _args.add_argument("--idioma", choices=tuple(IDIOMAS), default="en")
    sys.exit(main(_args.parse_args().idioma))
