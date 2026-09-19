# -*- coding: utf-8 -*-
"""Monta os mini manuais: um volume por capítulo, para mandar só o que interessa.

Cada mini manual é recortado da mesma estrutura do manual completo, em
`gerar.ESTRUTURA`, e não tem texto próprio além da folha de rosto. Duas regras
mantêm os volumes coerentes com o manual inteiro:

- a numeração das seções e das equações é a do manual completo: «seção 2.6» e
  «Equação 12» apontam para o mesmo lugar em qualquer volume;
- uma remissão a seção ou equação que ficou em outro volume diz em qual:
  «seção 4.5 (volume Tutorial)».

As figuras e as tabelas são numeradas dentro de cada volume, como pede a ABNT,
porque nenhuma é chamada de outro capítulo.

Uso:
    python manual/gerar.py
    python manual/gerar_mini_manuais.py            # Markdown e PDF
    python manual/gerar_mini_manuais.py --sem-pdf  # só o Markdown
"""

from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import gerar as g  # noqa: E402

NL = chr(10)
PASTA = os.path.join(AQUI, "mini")

#: Os volumes: (arquivo, título, capítulos do manual completo, apêndices a mais).
#: O glossário acompanha quase todos, porque o vocabulário é o mesmo.
VOLUMES = [
    ("1-comece-aqui", "Comece aqui", [1], ["G_glossario"]),
    ("2-metodo", "O método", [2],
     ["A_parametros", "B_processos", "C_fatores_de_emissao", "E_base_climatica",
      "G_glossario", "H_referencias"]),
    ("3-guias", "Guias de uso", [3],
     ["D_regimes_tarifarios", "F_arquivos_e_formatos", "G_glossario"]),
    ("4-tutorial", "Tutorial", [4],
     ["G_glossario", "I_fichas", "J_arquivos_de_exemplo"]),
    ("5-confiabilidade", "Enganos, limitações e confiabilidade", [5],
     ["G_glossario", "H_referencias"]),
    ("6-versoes", "Correções, bugs e versionamento", [6], []),
    ("7-apendices", "Apêndices", [7], []),
]


#: A frase de capa de cada volume: o que o leitor encontra nele.
FRASES = {
    "1-comece-aqui": "O que o programa faz, como instalá-lo e por onde entrar conforme o "
                     "seu objetivo.",
    "2-metodo": "As equações, os critérios e as fontes por trás de cada número que o "
                "programa publica.",
    "3-guias": "Casos de uso: outras cidades, clima futuro, tarifas, demanda variável, "
               "lote, sensibilidade e exportação.",
    "4-tutorial": "Um projeto de residência em Florianópolis, do primeiro dado ao volume "
                  "recomendado.",
    "5-confiabilidade": "Os enganos mais comuns, os limites do modelo e como o programa é "
                        "verificado.",
    "6-versoes": "O que mudou desde o Netuno 4, as mensagens de erro e como relatar um "
                 "problema.",
    "7-apendices": "Parâmetros, processos, fatores de emissão, tarifas, base climática, "
                   "formatos, glossário e referências.",
}


def _linha_de_conteudo(capitulos, apendices):
    """«Capítulo 2 · apêndices A, B e H», curta, para a capa."""
    partes = ["Todos os apêndices" if g.ESTRUTURA[c - 1][1] == "apendices" else f"Capítulo {c}"
              for c in capitulos]
    letras = [a.split("_")[0] for a in apendices]
    if letras:
        lista = letras[0] if len(letras) == 1 else ", ".join(letras[:-1]) + " e " + letras[-1]
        partes.append(("apêndice " if len(letras) == 1 else "apêndices ") + lista)
    return " · ".join(partes)


def capa_do_volume(arquivo, titulo, capitulos, apendices):
    from gerar_capas import CORES
    numero = VOLUMES.index(next(v for v in VOLUMES if v[0] == arquivo)) + 1
    return dict(
        painel=os.path.join(AQUI, "figuras", "capas", f"capa_{arquivo}.png"),
        cor=CORES[arquivo], numero=f"{numero:02d}", de=f"de {len(VOLUMES):02d}",
        titulo=titulo, frase=FRASES[arquivo],
        conteudo=_linha_de_conteudo(capitulos, apendices),
    )


def _chaves_do_volume(capitulos, apendices):
    chaves = []
    for i, (_, _, secoes) in enumerate(g.ESTRUTURA, start=1):
        for chave in secoes:
            if i in capitulos or chave in apendices:
                chaves.append(chave)
    return chaves


def _volume_de_cada_secao():
    """A seção mora no volume do seu capítulo; os apêndices, no volume Apêndices."""
    casa = {}
    for _, titulo, capitulos, _ in VOLUMES:
        for i, (_, _, secoes) in enumerate(g.ESTRUTURA, start=1):
            if i in capitulos:
                for chave in secoes:
                    casa[chave] = titulo
    return casa


def _marca_para_chave():
    marcas = {}
    for _, _, secoes in g.ESTRUTURA:
        for chave in secoes:
            prefixo = chave.split("_")[0]
            marcas[prefixo] = chave
            marcas[prefixo.lstrip("0") or "0"] = chave
            marcas[chave] = chave
    return marcas


def _equacoes_do_manual():
    """{nome: (número no manual completo, chave da seção)}, na ordem de leitura."""
    ordem = []
    for _, pasta, secoes in g.ESTRUTURA:
        for chave in secoes:
            caminho = os.path.join(AQUI, pasta, chave + ".md")
            if not os.path.exists(caminho):
                continue
            texto = open(caminho, encoding="utf-8").read()
            for m in re.finditer(r"^```equacao:([^\s`:]+)\s*$", texto, flags=re.M):
                if m.group(1) not in [n for n, _ in ordem]:
                    ordem.append((m.group(1), chave))
    return {nome: (i, chave) for i, (nome, chave) in enumerate(ordem, start=1)}


def resolver_marcas_do_volume(corpo, incluidas):
    numeros = g.indice_das_secoes()
    marcas = _marca_para_chave()
    casa = _volume_de_cada_secao()
    faltando = []

    def fora(chave):
        return "" if chave in incluidas else f" (volume {casa.get(chave, 'Apêndices')})"

    def secao(m):
        alvo = m.group(1).strip()
        base, _, sufixo = alvo.partition(".") if alvo not in marcas else (alvo, "", "")
        if base not in marcas:
            faltando.append(alvo)
            return "??"
        chave = marcas[base]
        return numeros[chave] + ("." + sufixo if sufixo else "") + fora(chave)

    corpo = re.sub(r"\{\{n:([^}]+)\}\}", secao, corpo)

    def capitulo(m):
        chave = m.group(1).strip()
        if chave not in g.PARTE_PARA_CAPITULO:
            faltando.append("c:" + chave)
            return "??"
        return str(g.PARTE_PARA_CAPITULO[chave])

    corpo = re.sub(r"\{\{c:([^}]+)\}\}", capitulo, corpo)
    if faltando:
        raise KeyError("marcas sem destino: " + ", ".join(sorted(set(faltando))))
    return corpo


def numerar_equacoes_do_volume(corpo, incluidas):
    """Equações com o número do manual completo; citação de fora diz o volume."""
    equacoes = _equacoes_do_manual()
    casa = _volume_de_cada_secao()

    def rotular(m):
        nome = m.group(1).strip()
        return "```equacao:" + nome + ":" + str(equacoes[nome][0])

    corpo = re.sub(r"^```equacao:([^\s`:]+)\s*$", rotular, corpo, flags=re.M)

    def citar(m):
        nome = m.group(1).strip()
        if nome not in equacoes:
            raise KeyError(f"equação citada e não escrita: {nome}")
        numero, chave = equacoes[nome]
        if chave in incluidas:
            return str(numero)
        return f"{numero} (volume {casa.get(chave, 'Apêndices')})"

    return re.sub(r"\{\{eq:([^}]+)\}\}", citar, corpo)


def _conteudo(capitulos, apendices):
    """«capítulo 2 e apêndices A, B e H», para a folha de rosto."""
    partes = []
    for c in capitulos:
        partes.append("os apêndices" if g.ESTRUTURA[c - 1][1] == "apendices"
                      else f"o capítulo {c} ({g.ESTRUTURA[c - 1][0]})")
    letras = [a.split("_")[0] for a in apendices]
    if letras:
        lista = letras[0] if len(letras) == 1 else ", ".join(letras[:-1]) + " e " + letras[-1]
        partes.append(("o apêndice " if len(letras) == 1 else "os apêndices ") + lista)
    return " e ".join(partes)


def folha(titulo, chaves, sumario_linhas, capitulos, apendices):
    return NL.join([
        "# Netuno 5",
        "",
        f"## Manual do Usuário — {titulo}",
        "",
        "Igor Catão Martins Vaz e Enedir Ghisi",
        "",
        "Grupo de Pesquisa Gestão do Espaço Sustentável",
        "Universidade Federal de Santa Catarina",
        "",
        "Florianópolis, 2026",
        "",
        "---",
        "",
        "### Sobre este volume",
        "",
        "Este é um dos sete volumes em que o manual do Netuno 5 pode ser distribuído, e",
        f"reúne {_conteudo(capitulos, apendices)} do manual completo. Serve para mandar",
        "só a parte que interessa: o método a um revisor, o tutorial a uma turma, os guias",
        "a quem já usa o programa.",
        "",
        "A numeração das seções e das equações é a mesma do manual completo, de modo que",
        "uma remissão vale nos dois. Quando o texto remete a uma seção que está em outro",
        "volume, o nome do volume vem entre parênteses.",
        "",
        "| Volume | Conteúdo |",
        "| :--- | :--- |",
    ] + [f"| {'**' + t + '**' if t == titulo else t} | {_conteudo(caps, aps)} |"
         for _, t, caps, aps in VOLUMES] + [
        "",
        "### Como citar",
        "",
        "> VAZ, Igor Catão Martins; GHISI, Enedir. **Netuno 5: manual do usuário**.",
        f"> {titulo}. Versão 5.0.0. Florianópolis: Universidade Federal de Santa",
        "> Catarina, 2026.",
        "",
        "---",
        "",
        "## Sumário",
        "",
    ] + sumario_linhas + ["", "---", ""])


def montar(arquivo, titulo, capitulos, apendices):
    chaves = _chaves_do_volume(capitulos, apendices)
    incluidas = set(chaves)
    numeros = g.indice_das_secoes()
    partes, sumario = [], []
    for i, (titulo_cap, pasta, secoes) in enumerate(g.ESTRUTURA, start=1):
        desta = [c for c in secoes if c in incluidas]
        if not desta:
            continue
        sumario.append(f"**{i} {titulo_cap}**" + NL)
        partes.append(f"# {i}. {titulo_cap}" + NL)
        for chave in desta:
            _, j = numeros[chave].split(".")
            sumario.append(f"{numeros[chave]} {g.TITULOS.get(chave, chave)}" + NL)
            caminho = os.path.join(AQUI, pasta, f"{chave}.md")
            texto = g.resolver(open(caminho, encoding="utf-8").read(), caminho)
            partes.append(g.numerar_titulos(texto, i, int(j)).rstrip(NL) + NL)
        sumario.append("")

    corpo = (NL + "---" + NL + NL).join(partes)
    corpo = resolver_marcas_do_volume(corpo, incluidas)
    corpo = g.numerar_figuras(corpo)
    corpo = numerar_equacoes_do_volume(corpo, incluidas)
    corpo, tabelas = g.legendar_tabelas(corpo)
    listas = []
    listas += g.bloco_de_lista("Lista de figuras", g.listar_figuras(corpo), "Figura")
    listas += g.bloco_de_lista("Lista de tabelas", tabelas, "Tabela")
    listas += g.bloco_de_lista("Lista de equações", g.listar_equacoes(corpo), "Equação")
    texto = resolver_marcas_do_volume(folha(titulo, chaves, sumario + [""] + listas,
                                            capitulos, apendices),
                                      incluidas) + corpo
    os.makedirs(PASTA, exist_ok=True)
    destino = os.path.join(PASTA, f"Manual-Netuno-5-{arquivo}.md")
    open(destino, "w", encoding="utf-8").write(texto)
    return destino, len(texto.split())


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    com_pdf = "--sem-pdf" not in argv
    if com_pdf:
        from gerar_pdf import compor_pdf
    for arquivo, titulo, capitulos, apendices in VOLUMES:
        destino, palavras = montar(arquivo, titulo, capitulos, apendices)
        print(f"  {os.path.basename(destino)}: {palavras:,} palavras".replace(",", "."))
        if com_pdf:
            compor_pdf(destino, destino[:-3] + ".pdf", titulo="Manual do Netuno",
                       volume=titulo, cabecalho=f"Manual do Netuno 5.0.0 — {titulo}",
                       capa_info=capa_do_volume(arquivo, titulo, capitulos, apendices))
    return 0


if __name__ == "__main__":
    print("mini manuais:")
    sys.exit(main())
