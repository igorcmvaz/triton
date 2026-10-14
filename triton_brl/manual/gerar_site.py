# -*- coding: utf-8 -*-
"""Monta o site de documentação a partir do manual já montado.

O site não tem texto próprio além da página inicial: as seções saem de
`Manual-Triton.md`, que `gerar.py` monta das mesmas partes do PDF. Por isso a
numeração, as figuras, as tabelas e as equações são as mesmas nos dois, e uma
correção no manual chega ao site na próxima montagem.

O resultado é uma página só (`site/index.html`), com as seções embutidas e
navegação por âncora (`#/2.6`), que abre direto do disco, sem servidor, e ao
lado as figuras, os PDFs e as miniaturas das capas.

Uso:
    python manual/gerar.py
    python manual/gerar_mini_manuais.py
    python manual/gerar_site.py
"""

from __future__ import annotations

import html
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
sys.path.insert(0, RAIZ)

import gerar as g  # noqa: E402
from triton import __version__ as VERSAO  # noqa: E402

SITE = os.path.join(AQUI, "site")
MANUAL = os.path.join(AQUI, "Manual-Triton.md")

#: O volume de cada capítulo, para a cor e para o PDF avulso.
VOLUME_DO_CAPITULO = {
    1: "1-comece-aqui", 2: "2-metodo", 3: "3-guias", 4: "4-tutorial",
    5: "5-confiabilidade", 6: "6-versoes", 7: "7-modulacao", 8: "8-apendices",
}


# ── o texto do manual, seção por seção ────────────────────────────────────────

def _secoes_do_manual(texto):
    """Divide o manual montado em capítulos e seções, a partir do capítulo 1."""
    corpo = texto[texto.index("\n# 1. "):]
    capitulos = []
    atual = None
    secao = None
    for linha in corpo.split("\n"):
        m_cap = re.match(r"^# (?:(\d+)\. )?(.+)$", linha)
        m_sec = re.match(r"^## (?:(\d+\.\d+)\. |Apêndice ([A-J]) — )(.+)$", linha)
        if m_cap and not linha.startswith("## "):
            numero = int(m_cap.group(1)) if m_cap.group(1) else len(capitulos) + 1
            atual = {"n": numero, "titulo": m_cap.group(2).strip(), "secoes": [],
                     "apendice": m_cap.group(1) is None}
            capitulos.append(atual)
            secao = None
            continue
        if m_sec and atual is not None:
            ident = m_sec.group(1) or m_sec.group(2)
            rotulo = m_sec.group(1) or f"Apêndice {m_sec.group(2)}"
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
        img = (f'<img src="figuras/equacoes/{arquivo}" alt="Equação {numero}" loading="lazy">'
               if arquivo else f"<pre>{html.escape(m.group(2).strip())}</pre>")
        return (f'\n<figure class="eq" id="eq-{numero}">{img}'
                f'<span class="eqn">({numero})</span></figure>\n')
    md = re.sub(r"^```equacao:[^:\n]+:(\d+)\s*\n(.*?)^```\s*$", eq, md, flags=re.M | re.S)

    # legenda de tabela, que o gerar.py escreve num comentário
    def tab(m):
        numero, resto = m.group(1), m.group(2)
        return f'<p class="tab-cap" id="tab-{numero}"><b>Tabela {numero}</b>{resto}</p>\n'
    md = re.sub(r"^<!-- tabela: \*\*Tabela (\d+)\*\*(.*?) -->\s*$", tab, md, flags=re.M)

    # destaque ==assim==
    md = re.sub(r"==(.+?)==", r"<mark>\1</mark>", md, flags=re.S)

    # figuras: imagem seguida da legenda em itálico
    def fig(m):
        arquivo, numero, legenda = m.group(1), m.group(2), m.group(3)
        return (f'\n<figure class="fig" id="fig-{numero}" data-arquivo="{arquivo}"><a href="figuras/{arquivo}" '
                f'target="_blank" rel="noopener"><img src="figuras/{arquivo}" alt="Figura {numero}" '
                f'loading="lazy"></a><figcaption><b>Figura {numero}</b> — '
                f'{_inline(legenda)}</figcaption></figure>\n')
    md = re.sub(r"^!\[[^\]]*\]\((?:\.\./)?figuras/([^)]+)\)\s*\n+\*Figura (\d+) — (.+?)\*\s*$",
                fig, md, flags=re.M)

    # «Aprofundamento» vira bloco recolhível
    linhas, saida, i = md.split("\n"), [], 0
    while i < len(linhas):
        if linhas[i].startswith("> **Aprofundamento"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(linhas[i][1:].lstrip() if linhas[i] != ">" else "")
                i += 1
            m = re.match(r"\*\*(Aprofundamento[^*]*)\*\*\s*(.*)", bloco[0])
            titulo = m.group(1).rstrip(".") if m else "Aprofundamento"
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
                f'<a class="ancora" href="#/{ident}/{alvo}" aria-label="Link para esta parte">¶</a></h{nivel}>')
    corpo = re.sub(r"<h([34])>(.*?)</h\1>", titulo, html_secao)
    return corpo, toc


def _ligar_remissoes(conteudo, onde_esta):
    """Transforma «seção 2.6», «apêndice C», «Equação 12» em links."""
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
        parte = re.sub(r"(\b[Ss]eç(?:ão|ões) |\be |, )(\d+\.\d+(?:\.\d+)*)\b", secao, parte)

        def apendice(m):
            letra = m.group(2)
            return f'{m.group(1)}<a href="#/{letra}">{letra}</a>' if letra in onde_esta["secao"] else m.group(0)
        parte = re.sub(r"(\b[Aa]pêndices? |\bapêndices [A-J], |\be )([A-J])\b(?![.\w])", apendice, parte)

        def objeto(m):
            tipo, n = m.group(1), m.group(2)
            chave = {"Figura": "fig", "Tabela": "tab", "Equação": "eq"}[tipo]
            sec = onde_esta[chave].get(int(n))
            if not sec:
                return m.group(0)
            return f'<a href="#/{sec}/{chave}-{n}">{tipo} {n}</a>'
        parte = re.sub(r"\b(Figura|Tabela|Equação) (\d+)\b", objeto, parte)
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

def _copiar_arquivos():
    destino = os.path.join(SITE, "figuras")
    if os.path.exists(destino):
        shutil.rmtree(destino)
    shutil.copytree(os.path.join(AQUI, "figuras"), destino,
                    ignore=shutil.ignore_patterns("capas"))
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
    pasta_mini = os.path.join(AQUI, "mini")
    origens = [os.path.join(AQUI, "Manual-Triton.pdf")]
    if os.path.isdir(pasta_mini):
        origens += [os.path.join(pasta_mini, f) for f in sorted(os.listdir(pasta_mini))
                    if f.endswith(".pdf")]
    for origem in origens:
        if os.path.exists(origem):
            shutil.copy2(origem, pdf)


def historico_de_versoes():
    """As versões publicadas, como dado, para a página de versões do site.

    A fonte é o capítulo de histórico do manual, a mesma do CHANGELOG.md e do
    panorama impresso: escrever num lugar e publicar em três.
    """
    from gerar_changelog import entradas_estruturadas
    md = _markdown()
    versoes = []
    for entrada in entradas_estruturadas():
        secoes = [{"titulo": titulo, "html": md.render(corpo)}
                  for titulo, corpo in entrada["secoes"].items()]
        versoes.append({
            "versao": entrada["versao"], "data": entrada["data"],
            "resumo": entrada["resumo"], "secoes": secoes,
            "altera_resultados": entrada["altera_resultados"],
            "nao_altera_resultados": entrada["nao_altera_resultados"],
        })
    return versoes


def indice_de_busca(capitulos, onde_interativas):
    """O que a busca encontra: seções, subseções, figuras, tabelas e equações.

    Quem procura raramente sabe em que seção a resposta está; sabe o nome da
    coisa — «tornado», «Tabela 83», «coeficiente de escoamento». Por isso o
    índice não se limita ao texto das seções.
    """
    interativas = {o["numero"] for o in onde_interativas.values()}
    itens = []
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
                    r'<figure class="fig" id="fig-(\d+)"[^>]*>.*?<figcaption>.*?'
                    r'Figura \d+.*?— (.*?)</figcaption>', s["html"], flags=re.S):
                numero = int(m.group(1))
                itens.append({"t": "interativa" if numero in interativas else "figura",
                              "id": s["id"], "a": f"fig-{numero}",
                              "r": f"Figura {numero}",
                              "n": re.sub(r"<[^>]+>", "", m.group(2)).strip(), "x": ""})
            for m in re.finditer(r'<p class="tab-cap" id="tab-(\d+)">.*?Tabela \d+.*?</b>(.*?)</p>',
                                 s["html"], flags=re.S):
                itens.append({"t": "tabela", "id": s["id"], "a": f"tab-{m.group(1)}",
                              "r": f"Tabela {m.group(1)}",
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


def main():
    if not os.path.exists(MANUAL):
        print("monte o manual antes: python manual/gerar.py")
        return 1
    os.makedirs(SITE, exist_ok=True)
    capitulos = montar_conteudo()
    from gerar_capas import CORES
    from gerar_mini_manuais import FRASES, VOLUMES
    volumes = [{"arquivo": a, "titulo": t, "frase": FRASES[a], "cor": CORES[a],
                "capitulo": caps[0]} for a, t, caps, _ in VOLUMES]
    dados = {
        "capitulos": capitulos,
        "volumes": volumes,
        "curva": dados_da_curva(),
        "revisao": date.today().strftime("%d/%m/%Y"),
        "versao": VERSAO,
        "testes": _quantos_testes(),
        "secoes": sum(len(c["secoes"]) for c in capitulos),
        "figuras": sum(len(re.findall(r'<figure class="fig"', s["html"]))
                       for c in capitulos for s in c["secoes"]),
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
    modelo = open(os.path.join(AQUI, "site_modelo.html"), encoding="utf-8").read()
    modelo = modelo.replace("/*__INTERATIVAS__*/",
                            open(os.path.join(AQUI, "site_interativas.js"), encoding="utf-8").read())
    pagina = modelo.replace("/*__DADOS__*/null",
                            json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    # A página publicada como Artifact recebe o esqueleto do próprio publicador;
    # a que abre do disco precisa do seu, com doctype, para não cair no modo quirks.
    open(os.path.join(SITE, "artefato.html"), "w", encoding="utf-8").write(pagina)
    cabeca = ("<!doctype html>\n<html lang=\"pt-BR\">\n<head>\n<meta charset=\"utf-8\">\n"
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
    sys.exit(main())
