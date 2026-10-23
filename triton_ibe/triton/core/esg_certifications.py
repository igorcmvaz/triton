"""
Módulo Core de Avaliação ESG e Pontuação de Certificações Ambientais.
Calcula a elegibilidade de créditos para certificações sustentáveis de edificações:
- LEED v4 / v4.1 (Water Efficiency - WEc1 e WEc2), com registro aberto até 30/06/2027;
- LEED v5 BD+C (WEc2 Enhanced Water Efficiency e o ponto de reúso do SSc3);
- Processo AQUA-HQE (Categoria 4 - Gestão da Água);
- Selo Casa Azul CAIXA (Critérios de Conservação de Água);
- EDGE (IFC / Banco Mundial), barra de água — medida WEM14;
- Indicadores GRI 303 (Água e Efluentes) e Pegada Hídrica Evitada (Water Positive Index).

O EDGE é o único da lista que não pontua: mede percentual de economia contra um
caso-base local e o compara com um limiar. Ver `triton/core/edge_certification.py`.
"""

from dataclasses import dataclass, field

from triton.core.edge_certification import (
    AvaliacaoEdge,
    LIMIAR_DE_AGUA_PCT,
    avaliar_agua_edge,
    regra_da_barra_de_agua,
)
from typing import Optional, List


# Tetos normativos da categoria Water Efficiency do LEED v4 BD+C. Estavam
# repetidos como literais em dez pontos do programa; ficam aqui, uma vez.
LEED_WEC1_MAX_PONTOS = 2   # reducao do uso externo
LEED_WEC2_MAX_PONTOS = 6   # reducao do uso interno
LEED_WE_MAX_PONTOS = LEED_WEC1_MAX_PONTOS + LEED_WEC2_MAX_PONTOS

#: LEED v5 BD+C, conferido contra o «LEED v5 BD+C Rating System», edição de
#: novembro de 2025 (USGBC). O v4 e o v4.1 aceitam registro de projetos
#: comerciais até 30/06/2027, com certificação até 30/06/2033.
LEED_V5_REFERENCIAL = "LEED v5 BD+C Rating System, edição de novembro de 2025 (USGBC)"
LEED_V4_REGISTRO_ATE = "30/06/2027"
#: WEc2 Enhanced Water Efficiency, New Construction: até 8 pontos, pela Opção 1
#: (projeto inteiro) ou pela soma das Opções 2 a 6 (Rating System, p. 62-68). O
#: Core and Shell tem teto de 7 e faixas próprias, que o programa não avalia.
LEED_V5_WEC2_MAX_PONTOS = 8
#: Opção 1: redução do uso de água do projeto inteiro contra a linha de base
#: (Tabela 1). Com fonte alternativa, cada faixa vale 1 ponto a mais, até 8; a 65%
#: com fonte alternativa, o referencial fala em desempenho exemplar, que não é
#: ponto deste crédito.
LEED_V5_OPCAO1_FAIXAS = ((65.0, 8), (60.0, 7), (55.0, 6), (50.0, 5), (45.0, 4),
                         (40.0, 3), (35.0, 2), (30.0, 1))
#: Opção 2: redução calculada em louças e metais, além do pré-requisito WEp2.
LEED_V5_OPCAO2_FAIXAS = ((40.0, 3), (35.0, 2), (30.0, 1))
#: Opção 4, caminho 2: redução do requisito teórico de irrigação.
LEED_V5_OPCAO4_FAIXAS = ((100.0, 2), (50.0, 1))
#: Opção 6, caminho 2: sistema de reúso no próprio lote que atenda a um ou mais
#: usos finais (irrigação, descargas, reposição ou processo). O programa trata o
#: aproveitamento de água de chuva como esse sistema.
LEED_V5_OPCAO6_PONTOS = 2


def _pontos_por_faixa(pct: float, faixas) -> int:
    for limiar, pontos in faixas:
        if pct >= limiar - 1e-9:
            return pontos
    return 0


def irrigacao_atendida_m3(resultado) -> Optional[float]:
    """Água de chuva que o balanço diário destinou ao uso externo, em m³/ano.

    O balanço atende primeiro o uso interno e só depois a irrigação. As telas de
    certificação faziam o contrário — atribuíam a chuva primeiro ao uso externo —
    e o crédito WEc1 saía de uma repartição que o motor não calculou. Devolve
    None quando não há resultado de simulação de onde tirar a parcela.
    """
    if resultado is None or not hasattr(resultado, "avg_pluvial_irrigation_consumed_l_day"):
        return None
    return float(resultado.avg_pluvial_irrigation_consumed_l_day) * 365.25 / 1000.0


@dataclass
class EsgCreditDetail:
    certification: str             # "LEED v4 / v4.1", "Processo AQUA-HQE", "Selo Casa Azul CAIXA", "GRI 303"
    credit_code: str               # "WEc1", "WEc2", "Categoria 4", "Critério 2.1", "GRI 303-3/5"
    credit_name: str               # Nome do crédito / indicador
    requirement_rule: str          # Regra de pontuação e faixas de corte
    achieved_performance: str      # Desempenho calculado no projeto
    points_or_level: str           # Pontuação obtida
    status: str                    # Status de elegibilidade
    notes: str                     # Detalhes técnicos e normativos
    focus: str = ""                # "Uso Externo", "Uso Interno", "Gestão Global", etc.


@dataclass
class LeedV5WaterCredits:
    """Enquadramento indicativo no WEc2 do LEED v5 BD+C (New Construction)."""
    opcao1_pts: int                # projeto inteiro, com o ponto da fonte alternativa
    opcao2_pts: int                # louças e metais
    opcao4_pts: int                # uso externo
    opcao6_pts: int                # reúso: fonte alternativa no lote
    total_pts: int                 # máximo entre a Opção 1 e a soma das Opções 2, 4 e 6
    caminho: str                   # "Opção 1" ou "Opções 2 a 6"
    max_possible_points: int = LEED_V5_WEC2_MAX_PONTOS
    description: str = ""
    referencial: str = LEED_V5_REFERENCIAL


@dataclass
class LeedWaterCredits:
    outdoor_water_points: int      # WEc1 (0 a 2 pts)
    indoor_water_points: int       # WEc2 (0 a 6 pts)
    total_leed_we_points: int      # Total (0 a 8 pts)
    savings_pct: float
    indoor_savings_pct: float = 0.0
    outdoor_savings_pct: float = 0.0
    max_possible_points: int = LEED_WE_MAX_PONTOS
    badge_label: str = ""
    description: str = ""


#: Referenciais conferidos contra os documentos originais em 2026-09-16.
AQUA_REFERENCIAL = "Referencial AQUA-HQE Residencial, versão 00 de 22/11/2024 (Fundação Vanzolini / CERQUAL)"
CASA_AZUL_REFERENCIAL = "Guia Selo Casa Azul + CAIXA, V023 de 29/04/2026"
CASA_AZUL_UNI_REFERENCIAL = "Guia Selo Casa Azul Uni, V001 de dezembro de 2025"

#: Critério 3.6 do Selo Casa Azul + CAIXA: pontos conforme a abrangência do uso.
CASA_AZUL_PONTOS_POR_ABRANGENCIA = {
    "areas_comuns": 2,               # uso da água nas áreas comuns do empreendimento
    "loteamento": 2,                 # casas em loteamento com a preparação exigida
    "unidades": 4,                   # uso da água nas unidades habitacionais
    "unidades_e_areas_comuns": 5,    # nas unidades e nas áreas comuns
}

#: Limiares de economia de água potável dos itens do tema «Consumo de água».
AQUA_EAU_1_2_PCT = 20.0   # nível HQE
AQUA_EAU_1_3_PCT = 40.0   # nível HQE 3


@dataclass
class AquaHqeRating:
    performance_level: str         # "HQE 3 (EAU.1.3)", "HQE (EAU.1.2)", "Abaixo de EAU.1.2"
    stars: int                     # 3 para HQE 3, 1 para HQE, 0 abaixo
    description: str
    itens_atendidos: List[str] = field(default_factory=list)
    referencial: str = AQUA_REFERENCIAL


@dataclass
class CasaAzulRating:
    category: str                  # "Critério 3.6 atendido" ou "Critério 3.6 não atendido"
    points_awarded: int            # 0 quando a abrangência não foi informada
    criterion_met: bool
    description: str
    pontuacao_faixa: str = "2 a 5 pontos"
    referencial: str = CASA_AZUL_REFERENCIAL


@dataclass
class EsgConsolidatedReport:
    leed: LeedWaterCredits
    aqua: AquaHqeRating
    casa_azul: CasaAzulRating
    edge: AvaliacaoEdge
    annual_potable_saved_m3: float
    lifetime_potable_saved_m3: float
    annual_co2e_saved_kg: float
    lifetime_co2e_saved_kg: float
    water_positive_ratio: float
    esg_summary_text: str
    indoor_savings_pct: float = 0.0
    outdoor_savings_pct: float = 0.0
    credit_details: List[EsgCreditDetail] = field(default_factory=list)
    leed_v5: Optional[LeedV5WaterCredits] = None


def calculate_esg_certifications(
    potable_savings_pct: float,
    annual_pluvial_consumed_m3: float,
    annual_potable_consumed_m3: float,
    net_co2e_saved_kg_lifetime: float,
    project_lifetime_years: int = 20,
    has_irrigation_demand: bool = True,
    indoor_savings_pct: Optional[float] = None,
    outdoor_savings_pct: Optional[float] = None,
    is_simplified_mode: bool = False,
    indoor_demand_m3: Optional[float] = None,
    outdoor_demand_m3: Optional[float] = None,
    catchment_area_m2: float = 0.0,
    edge_base_case_annual_m3: Optional[float] = None,
    casa_azul_abrangencia: Optional[str] = None,
) -> EsgConsolidatedReport:
    """
    Consolida as pontuações e relatórios ESG do sistema pluvial.
    Avalia especificamente o desempenho em usos internos (WEc2) e externos (WEc1).
    No modo simplificado (sem medição setorizada de bacias e jardins), realiza
    a partição normativa de referência (85% interno / 15% externo).
    """
    savings_pct = max(0.0, min(100.0, float(potable_savings_pct)))
    annual_saved_m3 = float(annual_pluvial_consumed_m3)
    annual_potable_m3 = float(annual_potable_consumed_m3)
    tot_demand_m3 = annual_saved_m3 + annual_potable_m3

    # ── PARTIÇÃO DE USOS INTERNOS E EXTERNOS ──
    # Só a repartição que o balanço diário calcula entra na conta. Esta função
    # inventava uma quando não a recebia: 85% da demanda como interna e 15% como
    # externa, 35% da chuva para o uso externo, ou economia externa de 100% a
    # partir de 25% de economia total. Nenhum desses números tinha fonte.
    has_real_outdoor = bool(has_irrigation_demand)
    if outdoor_demand_m3 is not None and outdoor_demand_m3 <= 0.001:
        has_real_outdoor = False

    # O crédito externo só é avaliado com a economia externa calculada.
    outdoor_avaliavel = has_real_outdoor and outdoor_savings_pct is not None
    calc_out_pct = max(0.0, min(100.0, float(outdoor_savings_pct))) if outdoor_avaliavel else 0.0

    if indoor_savings_pct is not None:
        calc_in_pct = max(0.0, min(100.0, float(indoor_savings_pct)))
    elif not has_real_outdoor:
        # Sem uso externo, toda a água de chuva vai para o uso interno.
        in_demand = indoor_demand_m3 if (indoor_demand_m3 is not None and indoor_demand_m3 > 0) else tot_demand_m3
        calc_in_pct = (annual_saved_m3 / in_demand * 100.0) if in_demand > 0 else savings_pct
    else:
        # Há uso externo e a repartição não veio: a economia interna é tomada
        # igual à total, que é a leitura conservadora.
        calc_in_pct = savings_pct

    # 1. LEED v4 / v4.1 WE (Water Efficiency)
    # WEc1: Redução do uso externo (Outdoor Water Use Reduction)
    # Requer demanda de irrigação/externa para ser atendida pelo sistema pluvial.
    # Sem demanda externa no projeto, não pontua em WEc1 (0 pts) e indica explicitamente como não aplicável.
    # O LEED concede os dois pontos com 100% de redução do uso externo de água
    # potável; o programa concedia a partir de 95%.
    if outdoor_avaliavel and calc_out_pct >= 100.0 - 1e-6:
        outdoor_pts = 2
        outdoor_status = "Elegível (Máximo)"
        outdoor_perf = f"Economia externa: {calc_out_pct:.1f}%"
        outdoor_notes = "Dispensa potável em irrigação e torneiras de jardim via água pluvial filtrada."
    elif outdoor_avaliavel and calc_out_pct >= 50.0:
        outdoor_pts = 1
        outdoor_status = "Elegível (1 pt)"
        outdoor_perf = f"Economia externa: {calc_out_pct:.1f}%"
        outdoor_notes = "Redução mínima de 50% no uso de água potável para irrigação alcançada."
    elif has_real_outdoor and not outdoor_avaliavel:
        outdoor_pts = 0
        outdoor_status = "Não avaliado (economia externa não calculada)"
        outdoor_perf = "Economia externa não calculada"
        outdoor_notes = ("Há demanda externa, mas a água de chuva destinada a ela não foi "
                         "calculada pelo balanço diário; o crédito WEc1 não é estimado sem essa repartição.")
    elif has_real_outdoor:
        outdoor_pts = 0
        outdoor_status = "Abaixo do limiar (50%)"
        outdoor_perf = f"Economia externa: {calc_out_pct:.1f}%"
        outdoor_notes = "A economia externa atingida está abaixo do limiar mínimo de 50% para pontuação no WEc1."
    else:
        outdoor_pts = 0
        outdoor_status = "Não aplicável (sem rega/área externa)"
        outdoor_perf = "Sem consumo externo (0 m³/ano)"
        outdoor_notes = "O projeto não possui demanda de água externa cadastrada (0 m³/ano); 0 pontos atribuídos no crédito WEc1 conforme regras do LEED."

    # WEc2: Redução do uso interno (Indoor Water Use Reduction)
    # Tabela Oficial LEED v4 BD+C / O+M: 
    # Pré-requisito obrigatório (WEp2): 20% (não pontua)
    # >= 50%: 6 pts | >= 45%: 5 pts | >= 40%: 4 pts | >= 35%: 3 pts | >= 30%: 2 pts | >= 25%: 1 pt
    if calc_in_pct >= 50.0:
        indoor_pts = 6
    elif calc_in_pct >= 45.0:
        indoor_pts = 5
    elif calc_in_pct >= 40.0:
        indoor_pts = 4
    elif calc_in_pct >= 35.0:
        indoor_pts = 3
    elif calc_in_pct >= 30.0:
        indoor_pts = 2
    elif calc_in_pct >= 25.0:
        indoor_pts = 1
    else:
        indoor_pts = 0

    tot_leed = outdoor_pts + indoor_pts
    # O nível do LEED (Certified, Silver, Gold, Platinum) soma todas as
    # categorias; a de água sozinha não o define. O rótulo antigo dizia
    # «Ouro/Platina» a partir de 6 pontos de água, o que o referencial não diz.
    if tot_leed >= 1:
        leed_badge = f"{tot_leed} de {LEED_WE_MAX_PONTOS} pontos na categoria de água"
    else:
        leed_badge = "Abaixo do limiar LEED (Mín. 25%)"

    mode_text = ""
    if not has_real_outdoor:
        outdoor_desc = "sem demanda externa cadastrada no projeto (0 de 2 pontos no crédito WEc1)"
    elif not outdoor_avaliavel:
        outdoor_desc = "sem a economia externa calculada pelo balanço (crédito WEc1 não avaliado)"
    else:
        outdoor_desc = (f"a economia externa de {calc_out_pct:.1f}% garante {outdoor_pts} de "
                        f"{LEED_WEC1_MAX_PONTOS} pontos possíveis no crédito WEc1 (Uso Externo)")

    leed_desc = (
        f"No Selo LEED v4 Water Efficiency, o crédito de água pluvial possui um teto máximo "
        f"normativo de {LEED_WE_MAX_PONTOS} pontos. "
        f"O projeto tirou {tot_leed} de {LEED_WE_MAX_PONTOS} pontos possíveis: "
        f"a economia interna de {calc_in_pct:.1f}% confere {indoor_pts} de {LEED_WEC2_MAX_PONTOS} "
        f"pontos possíveis no crédito WEc2 (Uso Interno) "
        f"e {outdoor_desc}{mode_text}."
    )

    leed_result = LeedWaterCredits(
        outdoor_water_points=outdoor_pts,
        indoor_water_points=indoor_pts,
        total_leed_we_points=tot_leed,
        savings_pct=savings_pct,
        indoor_savings_pct=calc_in_pct,
        outdoor_savings_pct=calc_out_pct,
        badge_label=leed_badge,
        max_possible_points=LEED_WE_MAX_PONTOS,
        description=leed_desc,
    )

    tem_sistema = annual_saved_m3 > 0.0

    # 1b. LEED v5 BD+C, WEc2 «Enhanced Water Efficiency». O projeto escolhe a
    # Opção 1 (projeto inteiro) ou soma as Opções 2 a 6. A água pluvial
    # contribui pela redução do uso interno (Opção 2), do uso externo
    # (Opção 4) e, por existir, pela Opção 6, caminho 2 (fonte alternativa no
    # lote). As reduções do LEED são medidas contra a linha de base de louças,
    # metais e irrigação do referencial, e não contra a demanda modelada: o
    # enquadramento é indicativo.
    v5_op1 = _pontos_por_faixa(savings_pct, LEED_V5_OPCAO1_FAIXAS)
    if v5_op1 and tem_sistema:
        v5_op1 = min(LEED_V5_WEC2_MAX_PONTOS, v5_op1 + 1)
    v5_op2 = _pontos_por_faixa(calc_in_pct, LEED_V5_OPCAO2_FAIXAS)
    v5_op4 = _pontos_por_faixa(calc_out_pct, LEED_V5_OPCAO4_FAIXAS) if outdoor_avaliavel else 0
    v5_op6 = LEED_V5_OPCAO6_PONTOS if tem_sistema else 0
    v5_soma = min(LEED_V5_WEC2_MAX_PONTOS, v5_op2 + v5_op4 + v5_op6)
    if v5_op1 > v5_soma:
        v5_total, v5_caminho = v5_op1, "Opção 1"
    else:
        v5_total, v5_caminho = v5_soma, "Opções 2 a 6"
    leed_v5 = LeedV5WaterCredits(
        opcao1_pts=v5_op1, opcao2_pts=v5_op2, opcao4_pts=v5_op4, opcao6_pts=v5_op6,
        total_pts=v5_total, caminho=v5_caminho,
        description=(
            f"LEED v5 BD+C, WEc2 Enhanced Water Efficiency: {v5_total} de "
            f"{LEED_V5_WEC2_MAX_PONTOS} pontos pelo caminho «{v5_caminho}» "
            f"(Opção 2, louças e metais: {v5_op2}; Opção 4, uso externo: {v5_op4}; "
            f"Opção 6, fonte alternativa: {v5_op6}; Opção 1, projeto inteiro: {v5_op1}). "
            "No SSc3 Rainwater Management, reusar parte do volume retido acrescenta 1 ponto, "
            "até o teto de 3; o programa não avalia esse crédito porque ele depende do "
            "escoamento de todo o terreno."
        ),
    )

    # 2. AQUA-HQE Residencial, tema «Consumo de água» (EAU), conferido contra o
    # referencial de 22/11/2024. Até 2026-09-15 o programa usava perfis «Base,
    # Boas Práticas, Excelente» a 10, 25 e 40%, que o referencial não tem.
    #   EAU.1.2 (HQE):   redução de pelo menos 20% do consumo de água potável;
    #   EAU.1.3 (HQE 3): economia de 40% de água potável;
    #   EAU.1.5 (HQE 3): sistema de recuperação de águas pluviais, conforme as
    #                    NBR 15527 e 16783.
    # O referencial compara com um cenário de referência de vazões da sua planilha
    # auxiliar, e não com a demanda modelada: o percentual aqui é indicativo.
    aqua_itens = []
    if tem_sistema:
        aqua_itens.append("EAU.1.5 (HQE 3): sistema de recuperação de águas pluviais")
    if savings_pct >= AQUA_EAU_1_2_PCT:
        aqua_itens.append("EAU.1.2 (HQE): redução de pelo menos 20% da água potável")
    if savings_pct >= AQUA_EAU_1_3_PCT:
        aqua_itens.append("EAU.1.3 (HQE 3): economia de 40% da água potável")
    if savings_pct >= AQUA_EAU_1_3_PCT:
        aqua_level, aqua_stars = "HQE 3 (EAU.1.3)", 3
    elif savings_pct >= AQUA_EAU_1_2_PCT:
        aqua_level, aqua_stars = "HQE (EAU.1.2)", 1
    else:
        aqua_level, aqua_stars = "Abaixo de EAU.1.2", 0
    aqua_desc = (
        f"Economia de {savings_pct:.1f}% de água potável. "
        + ("O sistema atende ao item EAU.1.5 (HQE 3) se seguir as NBR 15527 e 16783. " if tem_sistema else "")
        + "O referencial mede a economia contra o cenário de referência da planilha auxiliar "
        "da Fundação Vanzolini, que soma também os dispositivos economizadores: confira ali."
    )
    aqua_result = AquaHqeRating(
        performance_level=aqua_level,
        stars=aqua_stars,
        description=aqua_desc,
        itens_atendidos=aqua_itens,
    )

    # 3. Selo Casa Azul + CAIXA, critério 3.6 «Aproveitamento de águas pluviais»,
    # conferido contra o guia V023 de 29/04/2026. O indicador é a EXISTÊNCIA do
    # sistema (captação, tratamento e reservação), e os pontos dependem da
    # abrangência do uso, não do percentual de economia. Até 2026-09-15 o programa
    # usava «Prata, Ouro, Diamante» a 10, 20 e 30%, que o guia não tem.
    casa_pts = CASA_AZUL_PONTOS_POR_ABRANGENCIA.get(casa_azul_abrangencia, 0) if tem_sistema else 0
    if tem_sistema:
        casa_cat = "Critério 3.6 atendido"
        casa_met = True
        casa_desc = (
            "O indicador é a existência de sistema de aproveitamento de águas pluviais, com "
            "captação, tratamento, reservação e pontos de uso indicados. Pontuação pela "
            "abrangência: áreas comuns 2, unidades habitacionais 4, unidades e áreas comuns 5 "
            "(casas em loteamento com preparação, 2). Obrigatório para o nível Diamante. "
            "No Selo Casa Azul Uni, o critério equivalente (7) vale 1 ponto."
        )
        if casa_azul_abrangencia not in CASA_AZUL_PONTOS_POR_ABRANGENCIA:
            casa_desc += " Abrangência não informada: pontuação não atribuída."
    else:
        casa_cat = "Critério 3.6 não atendido"
        casa_met = False
        casa_desc = "Sem água pluvial aproveitada, não há sistema a enquadrar no critério 3.6."
    casa_azul_result = CasaAzulRating(
        category=casa_cat,
        points_awarded=casa_pts,
        criterion_met=casa_met,
        description=casa_desc,
    )

    # 4. EDGE (IFC): barra de água, medida WEM14
    # Não pontua. Mede percentual contra um caso-base local e compara com 20%.
    edge_result = avaliar_agua_edge(
        volume_pluvial_anual_m3=annual_saved_m3,
        demanda_total_anual_m3=tot_demand_m3,
        area_de_captacao_m2=catchment_area_m2,
        consumo_base_anual_m3_declarado=edge_base_case_annual_m3,
    )

    # Indicadores GRI e Pegada Hídrica
    lifetime_saved_m3 = annual_saved_m3 * project_lifetime_years
    annual_co2_kg = float(net_co2e_saved_kg_lifetime) / max(1.0, float(project_lifetime_years))
    water_pos_ratio = (annual_saved_m3 / tot_demand_m3) if tot_demand_m3 > 0 else 0.0

    # AQUA-HQE e Selo Casa Azul são certificações brasileiras: fora da Brasil saem da síntese
    # e da matriz (a aba ambiental já não os mostrava; docs/edicoes.md).
    from triton.core.edition import usa_dados_do_brasil
    selos_brasileiros = usa_dados_do_brasil()
    trecho_aqua = f"e, no AQUA-HQE Residencial, alcança {aqua_level}. " if selos_brasileiros else ""
    summary_text = (
        f"O empreendimento atinge substituição hídrica global de {savings_pct:.1f}% "
        f"(interno: {calc_in_pct:.1f}%, externo: {calc_out_pct:.1f}%), "
        f"poupando {annual_saved_m3:,.0f} m³/ano de água tratada "
        f"({lifetime_saved_m3:,.0f} m³ acumulados em {project_lifetime_years} anos). "
        f"No Selo LEED v4 WE (máximo de {LEED_WE_MAX_PONTOS} pontos possíveis), o projeto tirou "
        f"{tot_leed} de {LEED_WE_MAX_PONTOS} pontos{'' if selos_brasileiros else '. '}"
        f"{' ' if selos_brasileiros else ''}{trecho_aqua}"
        f"Na certificação EDGE, que não pontua e sim mede percentual contra um "
        f"caso-base, a barra de água chega a {edge_result.economia_de_agua_pct:.1f}% — "
        f"{'acima' if edge_result.atende_o_padrao_de_agua else 'abaixo'} do limiar de "
        f"{LIMIAR_DE_AGUA_PCT:.0f}% exigido em cada uma das três barras."
    )

    # Montagem detalhada da matriz de critérios
    credit_details = [
        EsgCreditDetail(
            certification="LEED v4 / v4.1",
            credit_code="WEc1",
            credit_name="Uso Externo de Água",
            focus="Área Externa & Jardim",
            requirement_rule="Máx. 2 pts: ≥ 50% red.: 1 pt | ≥ 100% ou s/ rega potável: 2 pts",
            achieved_performance=outdoor_perf,
            points_or_level=f"{outdoor_pts} / {LEED_WEC1_MAX_PONTOS} pts",
            status=outdoor_status,
            notes=f"Teto máximo de 2 pontos no crédito WEc1. {outdoor_notes}"
        ),
        EsgCreditDetail(
            certification="LEED v4 / v4.1",
            credit_code="WEc2",
            credit_name="Uso Interno de Água",
            focus="Bacias, Mictórios & Lavagem",
            requirement_rule="Máx. 6 pts: ≥ 25%: 1 pt | ≥ 30%: 2 | ≥ 35%: 3 | ≥ 40%: 4 | ≥ 45%: 5 | ≥ 50%: 6 pts",
            achieved_performance=f"Economia interna: {calc_in_pct:.1f}%",
            points_or_level=f"{indoor_pts} / {LEED_WEC2_MAX_PONTOS} pts",
            status="Elegível" if indoor_pts > 0 else "Abaixo do limiar (25%)",
            notes=f"Teto máximo de 6 pontos no crédito WEc2 (tirou {indoor_pts} de 6 pts). Suprimento a bacias sanitárias e lavanderia com água de chuva conforme ABNT NBR 15527."
        ),
        EsgCreditDetail(
            certification="AQUA-HQE Residencial",
            credit_code="EAU.1.2 / EAU.1.3 / EAU.1.5",
            credit_name="Consumo de água",
            focus="Empreendimento (unidades e áreas comuns)",
            requirement_rule="EAU.1.2 (HQE): ≥ 20% | EAU.1.3 (HQE 3): ≥ 40% | EAU.1.5 (HQE 3): sistema pluvial",
            achieved_performance=f"Economia de potável: {savings_pct:.1f}%",
            points_or_level=aqua_level,
            status="; ".join(i.split(":")[0] for i in aqua_itens) or "Nenhum item atendido",
            notes=(
                f"{AQUA_REFERENCIAL}. A economia do referencial é medida contra o cenário de "
                "referência da planilha auxiliar da Fundação Vanzolini; o percentual aqui é indicativo."
            ),
        ),
        EsgCreditDetail(
            certification="Selo Casa Azul + CAIXA",
            credit_code="Critério 3.6",
            credit_name="Aproveitamento de águas pluviais",
            focus="Empreendimento habitacional",
            requirement_rule="Existência do sistema; áreas comuns 2 | unidades 4 | unidades e áreas comuns 5 pts",
            achieved_performance="Sistema de aproveitamento presente" if casa_met else "Sem sistema",
            points_or_level=(f"{casa_pts} pts" if casa_pts else "2 a 5 pts, conforme a abrangência")
            if casa_met else "0 pts",
            status="Critério atendido" if casa_met else "Critério não atendido",
            notes=(
                f"{CASA_AZUL_REFERENCIAL}. Obrigatório para o nível Diamante. {CASA_AZUL_UNI_REFERENCIAL}: "
                "critério 7, 1 ponto, obrigatório para o Selo Ouro."
            ),
        ),
        EsgCreditDetail(
            certification="EDGE (IFC / Banco Mundial)",
            credit_code="WEM14",
            credit_name="Sistema de Aproveitamento de Água Pluvial",
            focus="Barra de Água do Projeto",
            requirement_rule=regra_da_barra_de_agua(),
            achieved_performance=(
                f"Barra de água: {edge_result.economia_de_agua_pct:.1f}% "
                f"(base: {edge_result.consumo_base_anual_m3:,.0f} m³/ano)"
            ),
            points_or_level=(
                "Atende ao padrão de água"
                if edge_result.atende_o_padrao_de_agua
                else f"Faltam {abs(edge_result.margem_pct):.1f} p.p."
            ),
            status=(
                "Padrão de água atendido"
                if edge_result.atende_o_padrao_de_agua
                else "Abaixo do limiar (20%)"
            ),
            notes=(
                f"O EDGE não atribui pontos. Área de captação a declarar no campo "
                f"da WEM14: {edge_result.area_de_captacao_m2:,.0f} m². "
                + edge_result.ressalva
            ),
        ),
        EsgCreditDetail(
            certification="GRI Standard 303",
            credit_code="303-3 / 303-5",
            credit_name="Circularidade Hídrica",
            focus="Balanço Hídrico Corporativo",
            requirement_rule="Reporte padronizado de captação evitada (m³/ano) e taxa de circularidade (%)",
            achieved_performance=f"{annual_saved_m3:,.0f} m³/ano poupados | Circularidade: {water_pos_ratio*100.0:.1f}%",
            points_or_level=f"{annual_saved_m3:,.0f} m³/ano",
            status="Em conformidade GRI",
            notes="Indicador corporativo para relatórios anuais ESG e metas de pegada hídrica positiva."
        ),
    ]

    credit_details[2:2] = [
        EsgCreditDetail(
            certification="LEED v5 BD+C",
            credit_code="WEc2",
            credit_name="Enhanced Water Efficiency",
            focus="Louças, metais, irrigação e reúso",
            requirement_rule=("Máx. 8 pts. Opção 1 (projeto inteiro): 30% 1 pt a 65% 8 pts, +1 com fonte "
                              "alternativa | Opção 2 (louças e metais): 30% 1, 35% 2, 40% 3 | "
                              "Opção 4 (externo): 50% 1, 100% 2 | Opção 6 (fonte alternativa no lote): 2 | "
                              "Opção 1 ou soma das Opções 2 a 6; New Construction (Core and Shell: máx. 7)"),
            achieved_performance=(f"Interno: {calc_in_pct:.1f}% | Externo: {calc_out_pct:.1f}% | "
                                  f"Total: {savings_pct:.1f}%"),
            points_or_level=f"{v5_total} / {LEED_V5_WEC2_MAX_PONTOS} pts ({v5_caminho})",
            status="Elegível" if v5_total > 0 else "Abaixo dos limiares",
            notes=(f"{LEED_V5_REFERENCIAL}. As reduções são medidas contra a linha de base do "
                   "referencial; o enquadramento é indicativo. O LEED v4/v4.1 aceita registro até "
                   f"{LEED_V4_REGISTRO_ATE}."),
        ),
        EsgCreditDetail(
            certification="LEED v5 BD+C",
            credit_code="SSc3",
            credit_name="Rainwater Management",
            focus="Terreno",
            requirement_rule=("Opção 1: reter no lote o volume do percentil 80, 85 ou 90 das chuvas "
                              "(70, 75 ou 80 em lote sem recuo): 1, 2 ou 3 pts; reusar parte desse "
                              "volume dá +1 pt, até 3 | Opção 2: reter o acréscimo de escoamento "
                              "sobre a cobertura natural: 3 pts"),
            achieved_performance="Não avaliado: depende do escoamento de todo o terreno",
            points_or_level="—",
            status="Não avaliado",
            notes="O sistema pluvial pode contribuir com o ponto de reúso, se o volume retido atender ao percentil.",
        ),
    ]

    if not selos_brasileiros:
        credit_details = [d for d in credit_details
                          if d.certification not in ("AQUA-HQE Residencial", "Selo Casa Azul + CAIXA")]

    return EsgConsolidatedReport(
        leed_v5=leed_v5,
        leed=leed_result,
        aqua=aqua_result,
        casa_azul=casa_azul_result,
        edge=edge_result,
        annual_potable_saved_m3=annual_saved_m3,
        lifetime_potable_saved_m3=lifetime_saved_m3,
        annual_co2e_saved_kg=annual_co2_kg,
        lifetime_co2e_saved_kg=net_co2e_saved_kg_lifetime,
        water_positive_ratio=water_pos_ratio,
        esg_summary_text=summary_text,
        indoor_savings_pct=calc_in_pct,
        outdoor_savings_pct=calc_out_pct,
        credit_details=credit_details,
    )
