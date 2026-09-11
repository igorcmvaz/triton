# -*- coding: utf-8 -*-
"""Monta o manual inteiro num arquivo só, com a numeração da ABNT NBR 6024.

A estrutura do manual está declarada **uma única vez**, em `ESTRUTURA`, e tudo o
mais é derivado dela: a numeração dos capítulos e das seções, o sumário, as
referências cruzadas do texto e a numeração das figuras e das equações.

Foi assim que a numeração parou de poder divergir. Antes, cada arquivo trazia o
próprio número no título e as referências cruzadas eram escritas à mão; bastava
reordenar o manual para que 160 referências apontassem para o lugar errado, e
nada avisava. Agora o arquivo guarda só o título, o texto refere as seções por
marca, e a montagem resolve as marcas contra a estrutura declarada.

As marcas que o texto usa:

    {{n:23}}    o número da seção que veio do antigo capítulo 23
    {{n:D}}     o número da seção que veio do antigo apêndice D
    {{c:2}}     o número do capítulo que veio da antiga Parte 2
    {{eq:nome}} o número de uma equação, resolvido na ordem de leitura

Uso:
    python manual/gerar_tabelas.py
    python manual/gerar_apendices.py
    python manual/gerar.py
"""

from __future__ import annotations

import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
NL = chr(10)
INCLUI = re.compile(r"^<!--\s*inclui:\s*(\S+)\s*-->\s*$")

#: A estrutura do manual: os capítulos, e as seções de cada um, na ordem de
#: leitura. A chave de cada seção é o nome do arquivo sem extensão, e é por ela
#: que as marcas do texto se referem à seção.
ESTRUTURA = [
    ("Comece aqui", "partes", [
        "01_o_que_o_netuno_faz",
        "02_instalacao",
        "03_por_onde_comecar",
    ]),
    ("O método", "partes", [
        "23_balanco_diario",
        "24_volume_ideal",
        "25_indicadores",
        "26_indices_pluviometricos",
        "27_etap",
        "28_energia_de_bombeamento",
        "29_analise_economica",
        "30_acv",
        "31_certificacoes",
        "32_multicriterio",
    ]),
    ("Guias disponíveis no programa", "partes", [
        "14_comparar_cidades",
        "15_cenario_climatico",
        "16_ajustar_a_tarifa",
        "17_modular_a_demanda",
        "18_escola_hospital_comercio",
        "19_rodar_em_lote",
        "20_sensibilidade",
        "21_importar_do_netuno4",
        "22_exportar_cad_bim_planilha",
    ]),
    ("Tutorial: um exemplo do começo ao fim", "partes", [
        "04_o_projeto_e_a_chuva",
        "05_a_edificacao_e_a_demanda",
        "06_a_primeira_simulacao",
        "07_escolher_o_volume",
        "08_reservatorio_superior",
        "09_qualidade_que_o_uso_exige",
        "10_quanto_custa",
        "11_quanto_carbono_evita",
        "12_qual_volume_escolher",
        "13_o_relatorio_e_o_artigo",
    ]),
    ("Enganos, limitações e confiabilidade", "partes", [
        "33_dez_enganos",
        "36_limitacoes",
        "34_verificacao",
    ]),
    ("Correções, bugs e versionamento", "partes", [
        "35_comparacao_netuno4",
        "37_mensagens_de_erro",
        "38_historico_de_versoes",
        "39_relatar_um_problema",
    ]),
    ("Apêndices", "apendices", [
        "A_parametros",
        "B_processos",
        "C_fatores_de_emissao",
        "D_regimes_tarifarios",
        "E_base_climatica",
        "F_arquivos_e_formatos",
        "G_glossario",
        "H_referencias",
        "I_fichas",
        "J_arquivos_de_exemplo",
    ]),
]

#: O título de cada seção, para o sumário e para o esqueleto de seção por
#: escrever. A chave é a mesma do arquivo.
TITULOS = {
    "01_o_que_o_netuno_faz": "O que o Netuno faz, e o que ele não faz",
    "02_instalacao": "Instalação e primeira execução",
    "03_por_onde_comecar": "Por onde começar, conforme o seu objetivo",
    "04_o_projeto_e_a_chuva": "O projeto e a chuva",
    "05_a_edificacao_e_a_demanda": "A edificação e a demanda",
    "06_a_primeira_simulacao": "A primeira simulação",
    "07_escolher_o_volume": "Escolher o volume",
    "08_reservatorio_superior": "Precisa de reservatório superior?",
    "09_qualidade_que_o_uso_exige": "Que qualidade o uso exige",
    "10_quanto_custa": "Quanto custa e em quanto se paga",
    "11_quanto_carbono_evita": "Quanto carbono evita",
    "12_qual_volume_escolher": "Qual volume escolher, afinal",
    "13_o_relatorio_e_o_artigo": "O relatório, e o que declarar num artigo",
    "14_comparar_cidades": "Comparar cidades",
    "15_cenario_climatico": "Usar cenário climático futuro",
    "16_ajustar_a_tarifa": "Ajustar a tarifa do seu município",
    "17_modular_a_demanda": "Modular a demanda por calendário",
    "18_escola_hospital_comercio": "Simular escola, hospital e comércio",
    "19_rodar_em_lote": "Comparar muitos casos de uma vez",
    "20_sensibilidade": "Análise de sensibilidade",
    "21_importar_do_netuno4": "Importar um projeto do Netuno 4",
    "22_exportar_cad_bim_planilha": "Exportar para CAD, BIM e planilha",
    "23_balanco_diario": "O balanço hídrico diário",
    "24_volume_ideal": "Volume ideal e a varredura",
    "25_indicadores": "Indicadores de eficiência",
    "26_indices_pluviometricos": "Índices pluviométricos",
    "27_etap": "Dimensionamento da ETAP",
    "28_energia_de_bombeamento": "Energia de bombeamento",
    "29_analise_economica": "Análise econômica e os regimes tarifários",
    "30_acv": "Avaliação de ciclo de vida",
    "31_certificacoes": "Certificações",
    "32_multicriterio": "Decisão multicritério",
    "33_dez_enganos": "Dez enganos que o programa não impede",
    "34_verificacao": "Como o programa é verificado",
    "35_comparacao_netuno4": "Comparação com o Netuno 4",
    "36_limitacoes": "Limitações conhecidas",
    "37_mensagens_de_erro": "Mensagens de erro e o que fazer",
    "38_historico_de_versoes": "Histórico de versões e o que mudou",
    "39_relatar_um_problema": "Como relatar um problema",
    "A_parametros": "Os parâmetros do projeto",
    "B_processos": "Os processos do programa",
    "C_fatores_de_emissao": "Fatores de emissão",
    "D_regimes_tarifarios": "Regimes tarifários",
    "E_base_climatica": "Base climática",
    "F_arquivos_e_formatos": "Arquivos, pastas e formatos",
    "G_glossario": "Glossário",
    "H_referencias": "Referências",
    "I_fichas": "Fichas de uma página",
    "J_arquivos_de_exemplo": "Arquivos de exemplo",
}

#: Da antiga «Parte N» para o capítulo que a sucedeu.
PARTE_PARA_CAPITULO = {"1": 1, "2": 4, "3": 3, "4": 2, "5": 5, "6": 5}


def indice_das_secoes():
    """Devolve {chave da seção: "2.1"}, a partir da estrutura declarada."""
    indice = {}
    for i, (_, _, secoes) in enumerate(ESTRUTURA, start=1):
        for j, chave in enumerate(secoes, start=1):
            indice[chave] = f"{i}.{j}"
    return indice


def indice_das_marcas():
    """Devolve {marca: número}, com a marca como o texto a escreve."""
    marcas = {}
    for chave, numero in indice_das_secoes().items():
        prefixo = chave.split("_")[0]
        marcas[prefixo] = numero                      # "23" ou "A"
        marcas[prefixo.lstrip("0") or "0"] = numero   # "23" sem zero à esquerda
        marcas[chave] = numero                        # a chave inteira também
    return marcas


def resolver(texto, origem):
    """Troca as linhas de inclusão pelo conteúdo do arquivo referido."""
    saida = []
    for linha in texto.split(NL):
        m = INCLUI.match(linha)
        if not m:
            saida.append(linha)
            continue
        alvo = os.path.join(os.path.dirname(origem), m.group(1))
        if not os.path.exists(alvo):
            raise FileNotFoundError(
                f"{os.path.basename(origem)} pede {m.group(1)}, que não existe. "
                "Rode manual/gerar_tabelas.py antes."
            )
        saida.append(open(alvo, encoding="utf-8").read().rstrip(NL))
    return NL.join(saida)


def numerar_titulos(texto, capitulo, secao):
    """Numera os títulos da seção conforme a NBR 6024.

    O arquivo traz `# Título` para a seção, `## Título` para a subseção e
    `### Título` para o item. Sai `## 2.1. Título`, `### 2.1.1. Título` e
    `#### 2.1.1.1. Título`: o nível desce um degrau porque o capítulo passou a
    ocupar o primeiro.
    """
    saida = []
    sub = item = 0
    for linha in texto.split(NL):
        if linha.startswith("### ") and not linha.startswith("#### "):
            item += 1
            saida.append(f"#### {capitulo}.{secao}.{sub}.{item}. {linha[4:].strip()}")
        elif linha.startswith("## ") and not linha.startswith("### "):
            sub += 1
            item = 0
            saida.append(f"### {capitulo}.{secao}.{sub}. {linha[3:].strip()}")
        elif linha.startswith("# ") and not linha.startswith("## "):
            saida.append(f"## {capitulo}.{secao}. {linha[2:].strip()}")
        else:
            saida.append(linha)
    return NL.join(saida)


def numerar_figuras(corpo):
    """Renumera as legendas na ordem em que o leitor as encontra."""
    contador = [0]

    def proxima(m):
        contador[0] += 1
        return "*Figura " + str(contador[0]) + " —"

    return re.sub(r"\*Figura\s+\d+\s+—", proxima, corpo)


def numerar_equacoes(corpo):
    """Numera as equações na ordem de leitura e resolve as citações.

    A seção escreve a equação num bloco ```equacao:nome``` e a cita no texto por
    `{{eq:nome}}`. A numeração é sequencial no manual inteiro, como a ABNT pede,
    e o número sai entre parênteses à direita da equação.
    """
    nomes = []

    def registrar(m):
        nome = m.group(1).strip()
        if nome not in nomes:
            nomes.append(nome)
        return m.group(0)

    re.sub(r"^```equacao:([^\s`:]+)\s*$", registrar, corpo, flags=re.M)
    numeros = {nome: i for i, nome in enumerate(nomes, start=1)}

    def rotular(m):
        return "```equacao:" + m.group(1) + ":" + str(numeros[m.group(1).strip()])

    corpo = re.sub(r"^```equacao:([^\s`:]+)\s*$", rotular, corpo, flags=re.M)

    def citar(m):
        nome = m.group(1).strip()
        if nome not in numeros:
            raise KeyError(f"equação citada e não escrita: {nome}")
        return str(numeros[nome])

    return re.sub(r"\{\{eq:([^}]+)\}\}", citar, corpo)


def resolver_marcas(corpo):
    """Troca as marcas de referência cruzada pelos números desta montagem."""
    marcas = indice_das_marcas()
    faltando = []

    def secao(m):
        chave = m.group(1).strip()
        if chave in marcas:
            return marcas[chave]
        # «{{n:33.3}}» aponta para a subseção 3 da antiga seção 33: o número
        # da seção resolve normalmente e o sufixo vai atrás.
        if "." in chave:
            base, _, sufixo = chave.partition(".")
            if base in marcas:
                return marcas[base] + "." + sufixo
        faltando.append(chave)
        return "??"

    corpo = re.sub(r"\{\{n:([^}]+)\}\}", secao, corpo)

    def capitulo(m):
        chave = m.group(1).strip()
        if chave not in PARTE_PARA_CAPITULO:
            faltando.append("c:" + chave)
            return "??"
        return str(PARTE_PARA_CAPITULO[chave])

    corpo = re.sub(r"\{\{c:([^}]+)\}\}", capitulo, corpo)
    if faltando:
        raise KeyError("marcas sem destino: " + ", ".join(sorted(set(faltando))))
    return corpo


def esqueleto(titulo):
    return NL.join([f"# {titulo}", "", "> **Seção por escrever.**", ""])


def frontmatter(sumario_linhas, palavras):
    """Folha de rosto e sumário, gerados da própria estrutura do manual."""
    from datetime import date
    return NL.join([
        "# Netuno 5",
        "",
        "## Manual do Usuário",
        "",
        "Igor Catão Martins Vaz e Enedir Ghisi",
        "",
        "Grupo de Pesquisa Gestão do Espaço Sustentável",
        "Universidade Federal de Santa Catarina",
        "",
        f"Versão 5.0.0 (beta) · Florianópolis, {date.today().strftime('%d/%m/%Y')}",
        "",
        "---",
        "",
        "### Como usar este manual",
        "",
        "Ele não foi feito para ser lido do começo ao fim. A seção 1.3 diz por onde",
        "entrar conforme o que você quer fazer.",
        "",
        "| Você quer | Leia |",
        "| :--- | :--- |",
        "| aprender a usar | o capítulo 4, o tutorial |",
        "| resolver um caso | o capítulo 3, os guias |",
        "| publicar um estudo | o capítulo 2, o método; e a seção 4.10 |",
        "| revisar um estudo | o capítulo 5, e as seções 7.1 e 7.2 |",
        "| não errar | a seção 5.1 |",
        "",
        "O manual supõe um leitor de engenharia que ainda não conhece o assunto: os",
        "conceitos são apresentados antes de serem usados, e o vocabulário está na",
        "seção 7.7. Duas caixas aparecem ao longo do texto, e elas se distinguem:",
        "",
        "| A caixa | Quando aparece |",
        "| :--- | :--- |",
        "| de régua **azul** | aviso ou observação que muda o que você faz |",
        "| de régua **laranja**, marcada *Aprofundamento* | o detalhe técnico por trás; pode ser pulada numa primeira leitura |",
        "",
        "> **Todo número impresso neste manual é calculado pelo programa.** As tabelas",
        "> e as figuras não foram digitadas: são produzidas rodando o Netuno com os",
        "> dados de entrada que cada seção declara. Cada valor publicado tem uma",
        "> verificação automática correspondente, de modo que uma correção no programa",
        "> não possa deixar o manual mentindo. A seção 5.3 explica como isso é feito.",
        "",
        "---",
        "",
        "## Sumário",
        "",
    ] + sumario_linhas + [
        "",
        "---",
        "",
    ])


def legendar_tabelas(corpo):
    """Numera as tabelas, escreve a legenda de cada uma e devolve a lista.

    A legenda declarada na seção prevalece. Na falta dela, a montagem compõe
    uma a partir do contexto: o título da subseção em que a tabela está, e,
    quando a tabela declara as variáveis de uma equação, a equação que ela
    acompanha.
    """
    linhas = corpo.split(NL)
    saida, lista = [], []
    numero = 0
    titulo_corrente = ""
    secao_corrente = ""
    equacao_corrente = ""
    legenda_declarada = None

    for i, linha in enumerate(linhas):
        m_sec = re.match(r"^##\s+[\d.]+\.\s+(.*)$", linha)
        if m_sec:
            secao_corrente = m_sec.group(1).strip()
            titulo_corrente = secao_corrente
            # A equação corrente não atravessa a fronteira da seção: uma tabela
            # de variáveis no começo de uma seção não pertence à última equação
            # da seção anterior.
            equacao_corrente = ""
        m_tit = re.match(r"^#{3,4}\s+[\d.]+\.\s+(.*)$", linha)
        if m_tit:
            titulo_corrente = m_tit.group(1).strip()

        m_eq = re.match(r"^```equacao:[^:]+:(\d+)\s*$", linha)
        if m_eq:
            equacao_corrente = m_eq.group(1)

        m_leg = re.match(r"^<!--\s*tabela:\s*(.+?)\s*-->\s*$", linha)
        if m_leg:
            legenda_declarada = m_leg.group(1)
            continue

        cabecalho_de_tabela = (
            linha.startswith("|")
            and i + 1 < len(linhas)
            and re.match(r"^\|[\s:\-|]+\|$", linhas[i + 1].rstrip())
        )
        if cabecalho_de_tabela:
            numero += 1
            if legenda_declarada:
                texto = legenda_declarada
            elif linha.startswith("| Símbolo | Significado | Unidade |"):
                texto = ("Variáveis da Equação " + equacao_corrente
                         if equacao_corrente else "Variáveis da equação")
            else:
                cabecas = [c.strip(" *") for c in linha.strip("|").split("|")]
                cabecas = [c for c in cabecas if c]
                # Cabeçalho genérico não descreve tabela nenhuma: nesse caso a
                # legenda se apoia na seção e na subseção em que a tabela está.
                genericos = {"valor", "valores", "parâmetro", "padrão",
                             "unidade", "o que significa", "o que é",
                             "descrição", "item", "quanto"}
                uteis = [c for c in cabecas if c.lower() not in genericos]
                if len(uteis) >= 2 and titulo_corrente:
                    texto = titulo_corrente + ": " + ", ".join(uteis[:3])
                elif titulo_corrente and secao_corrente:
                    texto = secao_corrente + ": " + titulo_corrente.lower()
                elif titulo_corrente:
                    texto = titulo_corrente
                else:
                    texto = ", ".join(cabecas[:3])
            legenda_declarada = None
            lista.append((numero, texto))
            saida.append("<!-- tabela: **Tabela " + str(numero) + "** — "
                         + texto + " -->")
        saida.append(linha)

    return NL.join(saida), lista


def listar_figuras(corpo):
    """Devolve [(número, legenda)] das figuras, na ordem de leitura."""
    lista = []
    for m in re.finditer(r"^\*Figura (\d+) — (.+?)\*\s*$", corpo, flags=re.M):
        texto = m.group(2).strip()
        # A legenda da figura é longa por desígnio; a lista inicial leva só a
        # primeira oração, que é o que identifica a figura.
        curta = re.split(r"(?<=[a-z0-9çãé])\. ", texto)[0].rstrip(".")
        lista.append((int(m.group(1)), curta))
    return lista


def listar_equacoes(corpo):
    """Devolve [(número, nome legível)] das equações, na ordem de leitura."""
    nomes = {
        "volume_captado": "Volume captado no dia",
        "disponivel": "Volume disponível antes do consumo",
        "extravasado": "Volume extravasado",
        "armazenado": "Volume armazenado antes do consumo",
        "consumido": "Volume de água pluvial consumido",
        "sobra": "Volume remanescente para o dia seguinte",
        "potavel": "Complemento de água potável da rede",
        "classificacao": "Classificação do dia quanto ao atendimento",
        "fechamento": "Fechamento do balanço de massa",
        "demanda_tres": "As três parcelas da demanda diária",
        "ganho_marginal": "Ganho marginal por metro cúbico acrescentado",
        "volume_ideal": "Volume ideal pelo critério de ganho marginal",
        "potencial": "Potencial de economia de água potável",
        "confiabilidade": "Confiabilidade volumétrica",
        "relacao_indicadores": "Relação entre potencial e confiabilidade",
        "extravasamento_medio": "Extravasamento médio diário",
        "volume_poupado": "Volume anual de água potável poupado",
        "nao_atendida": "Demanda média diária não atendida",
        "prcptot": "Precipitação total anual, PRCPTOT",
        "r95p": "Precipitação em dias muito úmidos, R95p",
        "rx1day": "Máxima precipitação em um dia, RX1day",
        "rx5day": "Máxima precipitação em cinco dias, RX5day",
        "sdii": "Índice simples de intensidade diária, SDII",
        "r20mm": "Dias de precipitação intensa, R20mm",
        "cdd": "Dias secos consecutivos, CDD",
        "cwd": "Dias úmidos consecutivos, CWD",
        "sazonalidade": "Índice de sazonalidade, SI",
        "massa_cloro": "Massa de produto clorado por metro cúbico",
        "capex_etap": "Investimento incremental da linha de tratamento",
        "energia_especifica": "Consumo específico de energia de recalque",
        "energia_por_vazao": "Consumo específico a partir da vazão",
        "vazao_deduzida": "Vazão de recalque deduzida da potência",
        "energia_partida": "Energia consumida nas partidas",
        "energia_anual": "Energia anual da motobomba",
        "economia_mensal": "Economia mensal na fatura",
        "esgoto": "Parcela de esgoto da fatura",
        "capex": "Investimento inicial total",
        "inflacao": "Fator acumulado de inflação",
        "degraus": "Número de reajustes aplicados",
        "reajuste": "Fator acumulado de reajuste tarifário",
        "vpl": "Valor presente líquido",
        "emissao_componente": "Emissão incorporada de um componente",
        "emissao_energia": "Emissão anual da energia de bombeamento",
        "saldo_liquido": "Saldo líquido anual de emissões",
        "payback_carbono": "Tempo de retorno ambiental",
        "saldo_vida": "Saldo de carbono ao fim da vida útil",
        "emissao_especifica": "Emissão específica por litro entregue",
        "topsis": "Coeficiente de proximidade do TOPSIS",
        "emulacao": "Transformação da série para emular o Netuno 4",
    }
    lista = []
    for m in re.finditer(r"^```equacao:([^:\n]+):(\d+)\s*$", corpo, flags=re.M):
        chave = m.group(1).strip()
        lista.append((int(m.group(2)), nomes.get(chave, chave)))
    return lista


def bloco_de_lista(titulo, itens, rotulo):
    if not itens:
        return []
    linhas = ["## " + titulo, ""]
    for numero, texto in itens:
        linhas.append(f"{rotulo} {numero} — {texto}")
        linhas.append("")
    linhas.append("---")
    linhas.append("")
    return linhas


def main():
    corpo_partes, faltando, escritos = [], [], []
    sumario = []

    for i, (titulo_cap, pasta, secoes) in enumerate(ESTRUTURA, start=1):
        sumario.append(f"**{i} {titulo_cap}**" + NL)
        for j, chave in enumerate(secoes, start=1):
            sumario.append(f"{i}.{j} {TITULOS.get(chave, chave)}")
        sumario.append("")

        corpo_partes.append(f"# {i}. {titulo_cap}" + NL)
        for j, chave in enumerate(secoes, start=1):
            caminho = os.path.join(AQUI, pasta, f"{chave}.md")
            if os.path.exists(caminho):
                texto = resolver(open(caminho, encoding="utf-8").read(), caminho)
                escritos.append(chave)
            else:
                texto = esqueleto(TITULOS.get(chave, chave))
                faltando.append(chave)
            corpo_partes.append(numerar_titulos(texto, i, j).rstrip(NL) + NL)

    destino = os.path.join(AQUI, "Manual-Netuno-5.md")
    corpo = (NL + "---" + NL + NL).join(corpo_partes)
    corpo = resolver_marcas(corpo)
    corpo = numerar_figuras(corpo)
    corpo = numerar_equacoes(corpo)
    corpo, tabelas = legendar_tabelas(corpo)
    figuras = listar_figuras(corpo)
    equacoes = listar_equacoes(corpo)

    listas = []
    listas += bloco_de_lista("Lista de figuras", figuras, "Figura")
    listas += bloco_de_lista("Lista de tabelas", tabelas, "Tabela")
    listas += bloco_de_lista("Lista de equações", equacoes, "Equação")

    palavras = len(corpo.split())
    corpo = frontmatter(sumario + [""] + listas, palavras) + corpo
    open(destino, "w", encoding="utf-8").write(corpo)

    print(f"montado: {os.path.relpath(destino, AQUI)}")
    print(f"  {len(escritos)} de {len(faltando) + len(escritos)} seções escritas")
    print(f"  {palavras:,} palavras, cerca de {palavras // 450} páginas".replace(",", "."))
    print(f"  {len(figuras)} figuras, {len(tabelas)} tabelas, "
          f"{len(equacoes)} equações")
    if faltando:
        print(f"  por escrever: {', '.join(str(f) for f in faltando)}")
    return len(escritos), len(faltando)


if __name__ == "__main__":
    sys.exit(0 if main() else 0)
