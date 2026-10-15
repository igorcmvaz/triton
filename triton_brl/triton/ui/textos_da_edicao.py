# -*- coding: utf-8 -*-
"""Textos que dependem da edição: normas, entidades e referências de cada país.

O pacote `triton/` é o mesmo nas três edições. O que é do Brasil (normas ABNT, SINAPI, MCTI,
CREA, perfis IPCA/Selic, fabricantes brasileiros) só aparece na Edição Brasil (BRL); a
Internacional (INT) não cita país nem norma nacional; a Portugal (PRT) cita só o que é de
Portugal ou da União Europeia. Este módulo reúne as variantes num só lugar, para que as
telas e os laudos perguntem «qual é o texto desta edição?» em vez de espalhar ``if``.

Os textos-fonte estão em português (a língua do catálogo de ``tr``); as variantes neutras têm
tradução no catálogo (``translation.py``) e, na Portugal, passam pelo glossário de português
de Portugal.

Regra de redação: **nenhum número de norma nem artigo de lei é inventado**. Onde a edição não
tem uma referência segura, o texto é genérico («normas e regulamentos aplicáveis no local do
projeto»).
"""

from __future__ import annotations

import re

from triton.core.edition import (
    is_prt_edition, usa_dados_do_brasil,
    sem_norma_do_brasil, sem_marcas_do_brasil,
    TERMOS_DO_BRASIL, PADRAO_DO_BRASIL, _AUTORIA, cita_o_brasil, _MARCAS_DO_BRASIL,
)

#: Sinal genérico de moeda (U+00A4): a Internacional não tem moeda predefinida.
SINAL_DE_MOEDA = "¤"


def por_edicao(brl, internacional, portugal=None):
    """O valor da edição ativa; sem ``portugal``, a Portugal usa o da Internacional."""
    if usa_dados_do_brasil():
        return brl
    if is_prt_edition():
        return internacional if portugal is None else portugal
    return internacional


# ── Normas ────────────────────────────────────────────────────────────────────────────────

def norma_pluvial(com_ano: bool = False) -> str:
    """A norma de aproveitamento de água de chuva da edição; vazia onde não há referência segura."""
    if usa_dados_do_brasil():
        return "ABNT NBR 15527:2019" if com_ano else "ABNT NBR 15527"
    if is_prt_edition():
        return "EN 16941-1"
    return ""


def norma_curta() -> str:
    """«NBR 15527» na Brasil, «EN 16941-1» na Portugal; vazia na Internacional."""
    if usa_dados_do_brasil():
        return "NBR 15527"
    return "EN 16941-1" if is_prt_edition() else ""


def normas_do_laudo(ingles: bool = False) -> str:
    """O campo «Conformidade Normativa» dos laudos."""
    if usa_dados_do_brasil():
        return "ABNT NBR 15527:2019 & NBR 5626"
    if is_prt_edition():
        return "EN 16941-1 e regulamentação nacional aplicável" if not ingles else "EN 16941-1 and applicable national regulations"
    return "Normas e regulamentos aplicáveis no local do projeto" if not ingles else "Standards and regulations applicable at the project site"


def registro_profissional(ingles: bool = False, tipo: str = "executivo") -> str:
    """O campo de registro do responsável técnico, ao pé dos laudos."""
    if usa_dados_do_brasil():
        return {
            "executivo": "CREA / Registro Profissional",
            "ambiental": "CREA / CRQ / Registro Profissional" if not ingles
            else "Professional Engineering / Environmental Board Registration",
            "pesquisa": "CREA / Matrícula Acadêmica / Registro Profissional",
        }.get(tipo, "CREA / Registro Profissional")
    if is_prt_edition():
        return "Ordem profissional / Número de membro" if not ingles else "Professional order / Membership number"
    return "Professional registration / Licence number" if ingles else "Registro profissional / Número de licença"


# ── Rótulos de tela ──────────────────────────────────────────────────────────────────────

def titulo_tipologia() -> str:
    return por_edicao("🎯 Tipologia & Padrão de Referência da Edificação (NBR 5626 / ANA)",
                      "🎯 Tipologia & Padrão de Referência da Edificação")


def titulo_classe_de_uso() -> str:
    return por_edicao("📋 B. Classe de Uso Final e Parâmetros da Qualidade (ABNT NBR 15527)",
                      "📋 B. Classe de Uso Final e Parâmetros da Qualidade")


def descricao_da_qualidade() -> str:
    return por_edicao(
        "Análise do impacto físico do descarte de primeira chuva (wash-off), metas normativas da ABNT NBR 15527:2019 / NBR 16783 "
        "e dimensionamento paramétrico de filtros mecânicos, desinfecção e polimento.",
        "Análise do impacto físico do descarte de primeira chuva (wash-off), metas de qualidade da água de uso final "
        "e dimensionamento paramétrico de filtros mecânicos, desinfecção e polimento.")


def recomendacao_de_polimento() -> str:
    return por_edicao(
        "A classe selecionada recomenda filtração fina. A recomendação é do "
        "programa, e não da NBR 15527:2019 — as classes 2 a 4 são adaptadas. "
        "Sem o filtro, o investimento e o custeio da linha de tratamento não o incluem.",
        "A classe selecionada recomenda filtração fina. A recomendação é do "
        "programa, e não de uma norma — as classes 2 a 4 são adaptadas. "
        "Sem o filtro, o investimento e o custeio da linha de tratamento não o incluem.")


def prancha_a3() -> str:
    return por_edicao("📐 Prancha Técnica Completa em A3 (Engenharia NBR 15527)",
                      "📐 Prancha Técnica Completa em A3")


def nome_da_prancha_a3() -> str:
    return por_edicao("Prancha Técnica A3 (ABNT NBR 15527)", "Prancha Técnica A3")


# ── Rede de segurança para textos que vêm do núcleo ─────────────────────────────────────

_NORMA_NBR = re.compile(
    r"(?:ABNT\s+)?NBR\s*\d{3,5}(?::\d{4})?(?:\s*(?:/|e|and|y)\s*(?:ABNT\s+)?NBR\s*\d{3,5}(?::\d{4})?)*",
    re.IGNORECASE)
_NORMA_DE_REFERENCIA = {
    "pt": "norma de referência", "en": "the reference standard",
    "es": "la norma de referencia", "zh": "参考标准",
}


def sem_norma_do_brasil(texto: str, idioma: str | None = None) -> str:
    """Troca «ABNT NBR n» por «norma de referência» em textos que o núcleo escreveu.

    Só fora da Edição Brasil. É a rede de segurança dos textos que não passam pelas variantes
    deste módulo (nomes das classes de qualidade da água, mensagens do descarte da primeira
    chuva): o texto vem do núcleo, que cita a norma brasileira. Não substitui a variante
    própria: onde a frase cabe reescrita, escreva a variante.
    """
    if not texto or usa_dados_do_brasil() or not isinstance(texto, str):
        return texto
    if idioma is None:
        from triton.ui.translation import get_current_lang
        idioma = get_current_lang()
    return _NORMA_NBR.sub(_NORMA_DE_REFERENCIA.get(idioma, _NORMA_DE_REFERENCIA["en"]), texto)


# ── Descritivos do núcleo (equipamentos da ETAP e do descarte) ───────────────────────────
#
# O núcleo escreve os nomes dos equipamentos em português (e alguns levam o volume no meio da
# frase). Para o inglês, as frases abaixo são trocadas de dentro para fora, da mais longa para a
# mais curta; o espanhol e o chinês caem no inglês. O português da Edição Portugal passa pelo
# glossário. Texto sem frase conhecida volta como veio.

_DESCRITIVOS_EN = {
    "Separador de Folhas e Gradeamento Autolimpante DN 100": "Self-cleaning Leaf Separator and Screen DN 100",
    "Separador de Folhas Duplo / Gradeamento DN 150": "Double Leaf Separator / Screen DN 150",
    "Sistema de Gradeamento Multicâmaras nas Prumadas": "Multi-chamber Screening System on the Downpipes",
    "un. Separadores Inox 304": "stainless-steel 304 separators",
    "Tela Inox 304, malha": "stainless-steel 304 mesh, aperture",
    "Coluna Vertical de Desvio em PVC Rígido DN 150/200": "Vertical Diverter Column in Rigid PVC DN 150/200",
    "com Conexões, Cap Roscado de Inspeção e Válvula de Purga Lenta": "with fittings, threaded inspection cap and slow-purge valve",
    "Reservatório Estanque de Descarte em PEAD Rotomoldado": "Sealed Rotomoulded HDPE Discard Tank",
    "com Extravasor Superior, Boia Flutuante de Vedação e Purga Lenta Calibrada": "with top overflow, floating sealing ball and calibrated slow purge",
    "PVC Rígido Classe Pluvial e Válvula de Purga/Retenção": "Rainwater-grade Rigid PVC and Purge/Check Valve",
    "Polietileno de Alta Densidade (PEAD) Rotomoldado e Dispositivo de Vedação/Purga": "Rotomoulded High-Density Polyethylene (HDPE) and Sealing/Purge Device",
    "Válvula de micro-drenagem calibrada / orifício com tela de retenção de sedimentos para esvaziamento automático lento em 24-48 horas de tempo seco.":
        "Calibrated micro-drain valve / orifice with a sediment-retention screen for slow automatic emptying within 24-48 dry hours.",
    "Filtro Autolimpante Vórtex DN 100 (Até 200 m²)": "Self-cleaning Vortex Filter DN 100 (up to 200 m²)",
    "Filtro Autolimpante Vórtex DN 150 (Até 500 m²)": "Self-cleaning Vortex Filter DN 150 (up to 500 m²)",
    "Filtro Industrial de Cesto / Ciclônico DN 200 (Grandes Telhados)": "Industrial Basket / Cyclonic Filter DN 200 (Large Roofs)",
    "Cloração (dosador de pastilhas de hipoclorito de cálcio)": "Chlorination (calcium hypochlorite tablet feeder)",
    "Reator ultravioleta (barreira adicional, sem residual)": "Ultraviolet reactor (additional barrier, no residual)",
    "Ozonização (barreira adicional, sem residual)": "Ozonation (additional barrier, no residual)",
    "Nenhum (Qualidade padrão atendida)": "None (standard quality met)",
    "Nenhum (Descarte não configurado)": "None (discard not configured)",
    "Filtro de Carvão Ativado em Bloco (Remoção de Cor e Odor)": "Activated-Carbon Block Filter (Colour and Odour Removal)",
    "Filtro de Areia Multicamada / Cartucho Plissado 20 µm": "Multi-layer Sand Filter / 20 µm Pleated Cartridge",
    "Descarte Mínimo / Insuficiente": "Minimum / Insufficient Discard",
    "Descarte Rigoroso / Alta Eficiência (> 1,5 mm)": "Strict / High-Efficiency Discard (> 1.5 mm)",
    "Descarte abaixo do recomendado. Risco elevado de carrear fuligem, poeiras e matéria orgânica pesada para o reservatório, exigindo trocas frequentes de filtros.":
        "Discard below the recommended value. High risk of carrying soot, dust and heavy organic matter into the tank, requiring frequent filter changes.",
    "Excelente eficiência de retenção (>90% de remoção de contaminantes iniciais). Recomendado para centros urbanos de tráfego intenso ou aplicações industriais e lavagem de roupas.":
        "Excellent retention efficiency (>90% removal of initial contaminants). Recommended for urban centres with heavy traffic or for industrial uses and laundry.",
    "Descarte recomendado (2 mm)": "Recommended discard (2 mm)",
    "Atende plenamente aos requisitos de referência. Remove entre 75% e 85% dos sólidos iniciais, garantindo excelente proteção à bomba e redução expressiva no consumo de desinfetante.":
        "Fully meets the reference requirements. Removes 75% to 85% of the initial solids, giving excellent pump protection and a marked cut in disinfectant use.",
    "Classe 1: parâmetros mínimos de referência": "Class 1: minimum reference parameters",
    "Classe 2 (adaptada, não normativa): Irrigação de Jardins e Lavagem de Pisos/Veículos": "Class 2 (adapted, non-normative): Garden Irrigation and Floor/Vehicle Washing",
    "Classe 3 (adaptada, não normativa): Torres de Resfriamento e Caldeiras Industriais": "Class 3 (adapted, non-normative): Cooling Towers and Industrial Boilers",
    "Classe 4 (adaptada, não normativa): Lavagem de Roupas e Usos Nobres Não Potáveis": "Class 4 (adapted, non-normative): Laundry and Higher-Grade Non-Potable Uses",
    "Malha": "Mesh",
    "Ficha técnica de fabricante (2025), tubo soldável": "Manufacturer's data sheet (2025), solvent-weld pipe",
    "Geometria normalizada do tubo, série reforçada: dem": "Standardised pipe geometry, reinforced series: OD",
    "parede": "wall",
    "Massa de catálogo de fabricante (60 Hz)": "Manufacturer catalogue mass (60 Hz)",
    "da EPD Grundfos": "from the Grundfos EPD",
    "aproximação de ordem de grandeza": "order-of-magnitude approximation",
    "a EPD do fabricante empregado prevalece": "the EPD of the manufacturer actually used prevails",
    "Descarte inicial / Inventário de Polímeros & Inox": "First-flush discard / Polymer & Stainless-steel inventory",
    "Fator de rede editável; usar o fator do local e do período do estudo": "Editable grid factor; use the factor of the site and of the study period",
    "Fator de água potável editável; substituir pelo inventário da entidade que abastece o local": "Editable potable-water factor; replace with the inventory of the entity that supplies the site",
    "sem data de vigência: a tabela entra como está, e o reajuste conta do início do estudo": "no effective date: the table is used as is, and the escalation counts from the start of the study",
    "sem data-base do estudo: a tabela entra como está": "no study base date: the table is used as is",
    "tabela vigente desde": "table in force since",
    "; estudo em": "; study on",
    ": nenhum reajuste a aplicar": ": no adjustment to apply",
    "reajuste(s) aplicado(s), tarifa ×": "adjustment(s) applied, tariff ×",
}
_DESCRITIVOS_ORDENADOS = sorted(_DESCRITIVOS_EN.items(), key=lambda kv: len(kv[0]), reverse=True)


def traduz_descritivo(texto: str) -> str:
    """Um descritivo escrito pelo núcleo, no idioma da interface e no vocabulário da edição.

    Fora da Brasil, as marcas e normas do Brasil saem antes (``sem_marcas_do_brasil``).
    """
    if not texto or not isinstance(texto, str):
        return texto
    from triton.ui.translation import get_current_lang, tr, em_portugues_da_edicao
    lang = get_current_lang()
    if not usa_dados_do_brasil():
        texto = _norma_neutra_em_portugues(texto)
        texto = sem_marcas_do_brasil(texto, "pt")
    if lang == "pt":
        return em_portugues_da_edicao(texto)
    traduzido = tr(texto)
    if traduzido != texto or usa_dados_do_brasil():
        return sem_norma_do_brasil(traduzido, lang)
    saida = texto
    for fonte, alvo in _DESCRITIVOS_ORDENADOS:
        if fonte in saida:
            saida = saida.replace(fonte, alvo)
    return sem_norma_do_brasil(saida, lang)


#: Frases do núcleo que citam a norma brasileira, na versão sem norma (português).
_NORMA_EM_PORTUGUES = {
    "Classe 1: parâmetros mínimos da NBR 15527:2019": "Classe 1: parâmetros mínimos de referência",
    "Descarte recomendado pela NBR 15527:2019 (2 mm)": "Descarte recomendado (2 mm)",
    "Descarte abaixo do recomendado pela NBR 15527.": "Descarte abaixo do recomendado.",
    "Atende plenamente aos requisitos da NBR 15527.": "Atende plenamente aos requisitos de referência.",
}


def _norma_neutra_em_portugues(texto: str) -> str:
    for fonte, alvo in _NORMA_EM_PORTUGUES.items():
        texto = texto.replace(fonte, alvo)
    return texto


# ── Nomes de arquivo sugeridos ────────────────────────────────────────────────────────────
# Os nomes sugeridos nos seletores de arquivo estavam em português do Brasil em qualquer idioma.
# Fora da Brasil, e fora do português, saem em inglês. Na Brasil nada muda.

_NOMES_EM_INGLES = {
    "_Dados_Simulados": "_Simulated_Data",
    "_Auditoria_Completa": "_Full_Audit",
    "Simulacao_Triton": "Triton_Simulation",
    "projeto_triton": "triton_project",
    "fluxo_de_caixa_triton": "triton_cash_flow",
    "triton-modelo-cenarios": "triton-scenarios-template",
    "triton-resultados-cenarios": "triton-scenario-results",
    "triton-modulacao-estocastica": "triton-probabilistic-modulation",
    "triton-grafico": "triton-chart",
    "relatorio-cliente": "client-report",
    "relatorio-ambiental": "environmental-report",
    "relatorio-pesquisa": "research-report",
    "Projeto Triton": "Triton Project",
    "Novo projeto Triton": "New Triton project",
}


def nome_sugerido(nome: str) -> str:
    """O pedaço de nome de arquivo no idioma da interface (inglês fora da Brasil e do português)."""
    if usa_dados_do_brasil() or not nome:
        return nome
    from triton.ui.translation import get_current_lang
    if get_current_lang() == "pt":
        return nome
    for fonte, alvo in _NOMES_EM_INGLES.items():
        nome = nome.replace(fonte, alvo)
    return nome


def artefato_de_projeto() -> str:
    """«projeto» no nome auditável do arquivo de projeto (inglês fora da Brasil e do português)."""
    return "project" if nome_sugerido("projeto_triton") != "projeto_triton" else "projeto"


def artefato_de_laudo(tipo: str) -> str:
    """O tipo de laudo na construção do nome auditável (``relatorio-cliente`` etc.)."""
    chave = {"economic": "relatorio-cliente", "environmental": "relatorio-ambiental"}.get(tipo, "relatorio-pesquisa")
    return nome_sugerido(chave)


# ── Motor, tubulação e custos de referência ───────────────────────────────────────────────

def rotulo_rendimento_do_motor() -> str:
    return por_edicao("Rendimento do motor (%, em branco usa a NBR 17094-2):",
                      "Rendimento do motor (%, em branco usa o valor típico da potência):")


def dica_rendimento_do_motor() -> str:
    return por_edicao(
        "A potência de placa é a potência mecânica no eixo, e a ABNT NBR 17094-2 manda marcar o rendimento na placa como grandeza separada. Em branco, o programa adota a Tabela 13 da norma para a potência escolhida: 60,5% em meio CV, 69,3% em um CV.",
        "A potência de placa é a potência mecânica no eixo, e o rendimento do motor é uma grandeza separada. Em branco, o programa adota um rendimento típico para a potência escolhida: cerca de 60% em meio CV e 69% em um CV.")


def dica_modelos_de_pressurizador() -> str:
    return por_edicao(
        "Modelos com curva de catálogo publicada pelo fabricante. A energia é o tempo ligado vezes a potência elétrica: a potência de placa dividida pelo rendimento do motor da ABNT NBR 17094-2.",
        "Modelos com curva de catálogo publicada pelo fabricante. A energia é o tempo ligado vezes a potência elétrica: a potência de placa dividida pelo rendimento do motor.")


def dica_potencia_de_placa() -> str:
    return por_edicao(
        "Potência de placa, que é mecânica, no eixo. O programa a divide pelo rendimento do motor da ABNT NBR 17094-2 para chegar à potência elétrica.",
        "Potência de placa, que é mecânica, no eixo. O programa a divide pelo rendimento do motor para chegar à potência elétrica.")


def guia_de_custos_de_tubulacao() -> str:
    return por_edicao(
        "💡 <b>Custos de Referência SINAPI:</b> Tubulações comerciais de PVC Soldável Água Fria (DN 20 a 110 mm) e Pluvial (DN 100 e 150 mm) com acréscimo normativo de 25% para conexões e registros.<br>Os comprimentos informados aqui são automaticamente sincronizados com o Módulo Ambiental (ACV).",
        "💡 <b>Custos de Referência:</b> Tubulações comerciais de PVC de água fria (DN 20 a 110 mm) e pluviais (DN 100 e 150 mm) com acréscimo de 25% para conexões e registros. Informe os preços unitários do seu fornecedor.<br>Os comprimentos informados aqui são automaticamente sincronizados com o Módulo Ambiental (ACV).")


def subtotal_de_tubulacoes() -> str:
    return por_edicao("Subtotal Calculado de Tubulações (SINAPI + conexões):", "Subtotal Calculado de Tubulações (conexões incluídas):")


def aviso_de_regime_de_cobranca() -> str:
    return por_edicao(
        "💧 <b>Regime de cobrança:</b> defina você mesmo. Se a sua concessionária cobra um mínimo que já dá direito a alguns m³, lance-o como faixa de R$ 0,00/m³ até esse volume: abaixo dele economizar água não reduz a conta.",
        "💧 <b>Regime de cobrança:</b> defina você mesmo. Se a sua entidade de abastecimento cobra um mínimo que já dá direito a alguns m³, lance-o como faixa de R$ 0,00/m³ até esse volume: abaixo dele economizar água não reduz a conta.")


# ── Fontes e marcas brasileiras nos textos de ACV (fora da Edição Brasil) ───────────────────
#
# As justificativas e as fontes dos fatores de emissão citam fabricantes, normas e inventários do
# Brasil. Fora da Brasil, cada citação vira a descrição genérica da mesma fonte («ficha técnica de
# fabricante», «inventário público da construção»); os números são os mesmos e continuam sujeitos
# à substituição pelo usuário. A ordem importa: as frases longas vêm antes das curtas.

# (_MARCAS_DO_BRASIL, sem_marcas_do_brasil, TERMOS_DO_BRASIL, PADRAO_DO_BRASIL, _AUTORIA, cita_o_brasil
# são importados de triton.core.edition para manter isolamento arquitetural com o núcleo)

_TAGS = re.compile(r"<[^>]+>")


def texto_do_html(html: str) -> str:
    """O texto visível de um trecho de HTML (sem marcas, entidades resolvidas, espaços normalizados)."""
    import html as _h
    return " ".join(_h.unescape(_TAGS.sub(" ", html)).split())


_CABECALHO = re.compile(r"(<h([2-4])\b[^>]*>.*?</h\2>)", re.IGNORECASE | re.DOTALL)
_SEPARADOR_DE_FRASE = re.compile(r"(<br\s*/?>|(?<=[.;!?])\s+(?=[A-ZÀ-Ý<0-9«\"]))", re.IGNORECASE)
_MARCAS_DE_PAR = ("b", "i", "em", "strong", "a", "code", "span", "sub", "sup", "u", "p", "li", "ul", "ol",
                  "div", "table", "tr", "td", "th", "pre", "h2", "h3", "h4")


def _equilibrado(trecho: str) -> bool:
    for marca in _MARCAS_DE_PAR:
        abre = len(re.findall(rf"<{marca}\b", trecho, re.IGNORECASE))
        fecha = len(re.findall(rf"</{marca}\s*>", trecho, re.IGNORECASE))
        if abre != fecha:
            return False
    return True


def _podar(interior: str) -> str | None:
    """O interior de um parágrafo ou item sem as frases do Brasil; ``None`` se nada sobra."""
    pedacos = _SEPARADOR_DE_FRASE.split(interior)
    frases, separadores = pedacos[0::2], pedacos[1::2]
    mantidas, houve_corte = [], False
    for i, frase in enumerate(frases):
        if cita_o_brasil(texto_do_html(frase)):
            if not _equilibrado(frase):
                return None
            houve_corte = True
            continue
        mantidas.append((frase, separadores[i - 1] if i > 0 and i - 1 < len(separadores) else ""))
    if not houve_corte:
        return interior
    if not mantidas or not texto_do_html("".join(f for f, _ in mantidas)):
        return None
    saida = mantidas[0][0]
    for frase, sep in mantidas[1:]:
        saida += (sep if sep.strip() or "<br" in sep.lower() else " ") + frase
    return saida


def _poda_elemento(marca: str):
    padrao = re.compile(rf"(<{marca}\b[^>]*>)(.*?)(</{marca}\s*>)", re.IGNORECASE | re.DOTALL)

    def troca(m):
        if not cita_o_brasil(texto_do_html(m.group(2))):
            return m.group(0)
        podado = _podar(m.group(2))
        return "" if podado is None else f"{m.group(1)}{podado}{m.group(3)}"
    return padrao, troca


_CELULA = re.compile(r"(<t[dh]\b[^>]*>)(.*?)(</t[dh]\s*>)", re.IGNORECASE | re.DOTALL)


def _linha_sem_brasil(m) -> str:
    linha = m.group(0)
    if not cita_o_brasil(texto_do_html(linha)):
        return linha
    celulas = _CELULA.findall(linha)
    if not celulas or cita_o_brasil(texto_do_html(celulas[0][1])):
        return ""

    def celula(c):
        if not cita_o_brasil(texto_do_html(c.group(2))):
            return c.group(0)
        podado = _podar(c.group(2))
        return f"{c.group(1)}{'—' if podado is None else podado}{c.group(3)}"
    nova = _CELULA.sub(celula, linha)
    return "" if cita_o_brasil(texto_do_html(nova)) else nova


def sem_brasil_no_html(html: str) -> str:
    """O HTML sem seções, linhas de tabela, itens e frases que citam o Brasil (só fora da Edição Brasil)."""
    if not html or usa_dados_do_brasil():
        return html
    # 1. seções cujo título é do Brasil: vão com o corpo, até o próximo título do mesmo nível ou acima
    partes = _CABECALHO.split(html)
    # partes: [texto, cab, nivel, texto, cab, nivel, texto, ...]
    saida, i, corte_nivel = [partes[0]], 1, None
    while i < len(partes):
        cab, nivel, corpo = partes[i], int(partes[i + 1]), partes[i + 2]
        i += 3
        if corte_nivel is not None:
            if nivel > corte_nivel:
                continue
            corte_nivel = None
        if cita_o_brasil(texto_do_html(cab)):
            corte_nivel = nivel
            continue
        saida += [cab, corpo]
    html = "".join(saida)
    # 2. linhas de tabela: sai a linha cujo primeiro campo (o nome do item) cita o Brasil; nas demais,
    #    só o campo que cita perde a frase (ou fica «—»), e a linha, com os seus números, permanece
    html = re.sub(r"<tr\b[^>]*>.*?</tr\s*>", _linha_sem_brasil, html, flags=re.IGNORECASE | re.DOTALL)
    # 3. itens, parágrafos e blocos: poda por frase
    for marca in ("li", "p", "div"):
        padrao, troca = _poda_elemento(marca)
        html = padrao.sub(troca, html)
    # 4. o que ficou vazio
    for _ in range(2):
        html = re.sub(r"<(ul|ol)\b[^>]*>\s*</\1\s*>", "", html, flags=re.IGNORECASE)
    html = re.sub(r"<table\b[^>]*>.*?</table\s*>",
                  lambda m: m.group(0) if re.search(r"<td\b", m.group(0), re.IGNORECASE) else "",
                  html, flags=re.IGNORECASE | re.DOTALL)
    # título seguido de outro título ou do fim: sem corpo
    antes = None
    while antes != html:
        antes = html
        html = re.sub(r"<h([3-4])\b[^>]*>(?:(?!</h\1>).)*?</h\1>\s*(?=<h[2-4]\b|<hr\b|$)", "", html,
                      flags=re.IGNORECASE | re.DOTALL)
    return html


_MARCA_HTML = re.compile(r"(<[a-zA-Z/!][^>]*>)")


def html_da_edicao(html: str, idioma: str | None = None) -> str:
    """O HTML da documentação na edição ativa: sem o Brasil e, na Portugal em português, no glossário."""
    if not html or usa_dados_do_brasil():
        return html
    html = sem_brasil_no_html(html)
    if is_prt_edition():
        if idioma is None:
            from triton.ui.translation import get_current_lang
            idioma = get_current_lang()
        if idioma == "pt":
            from triton.ui.portugues_de_portugal import para_portugal
            # <pre> (comandos): só as linhas de comentário; <style>: nada; o resto, o texto entre as marcas
            partes = re.split(r"(<pre\b.*?</pre\s*>|<style\b.*?</style\s*>)", html,
                              flags=re.IGNORECASE | re.DOTALL)
            for k, parte in enumerate(partes):
                if k % 2 == 0:
                    # separa as marcas do texto (que pode ter um «>» solto, como em «TIR > TMA»)
                    pedacos = _MARCA_HTML.split(parte)
                    for j in range(0, len(pedacos), 2):
                        pedacos[j] = para_portugal(pedacos[j])
                    partes[k] = "".join(pedacos)
                elif parte.lower().startswith("<pre"):
                    partes[k] = re.sub(r"(?m)^(#.*)$", lambda m: para_portugal(m.group(1)), parte)
            html = "".join(partes)
    return html
