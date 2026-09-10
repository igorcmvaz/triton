"""
Módulo Core de Avaliação ESG e Pontuação de Certificações Ambientais.
Calcula a elegibilidade de créditos para certificações sustentáveis de edificações:
- LEED v4 / v4.1 (Water Efficiency - WEc1 e WEc2);
- Processo AQUA-HQE (Categoria 4 - Gestão da Água);
- Selo Casa Azul CAIXA (Critérios de Conservação de Água);
- EDGE (IFC / Banco Mundial), barra de água — medida WEM14;
- Indicadores GRI 303 (Água e Efluentes) e Pegada Hídrica Evitada (Water Positive Index).

O EDGE é o único da lista que não pontua: mede percentual de economia contra um
caso-base local e o compara com um limiar. Ver `netuno/core/edge_certification.py`.
"""

from dataclasses import dataclass, field

from netuno.core.edge_certification import (
    AvaliacaoEdge,
    LIMIAR_DE_AGUA_PCT,
    avaliar_agua_edge,
    regra_da_barra_de_agua,
)
from typing import Dict, Any, Optional, List


# Tetos normativos da categoria Water Efficiency do LEED v4 BD+C. Estavam
# repetidos como literais em dez pontos do programa; ficam aqui, uma vez.
LEED_WEC1_MAX_PONTOS = 2   # reducao do uso externo
LEED_WEC2_MAX_PONTOS = 6   # reducao do uso interno
LEED_WE_MAX_PONTOS = LEED_WEC1_MAX_PONTOS + LEED_WEC2_MAX_PONTOS


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


@dataclass
class AquaHqeRating:
    performance_level: str         # "Excelente", "Boas Práticas", "Base", "Insuficiente"
    stars: int                     # 0 a 3 estrelas
    description: str


@dataclass
class CasaAzulRating:
    category: str                  # "Diamante", "Ouro", "Prata", "Não Elegível"
    points_awarded: int
    criterion_met: bool
    description: str


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
    # Determina se há de fato demanda externa cadastrada / ativa
    has_real_outdoor = has_irrigation_demand
    if outdoor_demand_m3 is not None and outdoor_demand_m3 <= 0.001:
        has_real_outdoor = False
    elif not has_irrigation_demand:
        has_real_outdoor = False

    if not has_real_outdoor:
        out_demand = 0.0
        pluv_to_outdoor = 0.0
        calc_out_pct = 0.0
        in_demand = indoor_demand_m3 if (indoor_demand_m3 is not None and indoor_demand_m3 > 0) else tot_demand_m3
        pluv_to_indoor = annual_saved_m3
        calc_in_pct = (pluv_to_indoor / in_demand * 100.0) if in_demand > 0 else savings_pct
    elif is_simplified_mode:
        # Modo Simplificado com uso externo ativo: partição normativa de referência (85% interno / 15% externo)
        out_demand = outdoor_demand_m3 if (outdoor_demand_m3 is not None and outdoor_demand_m3 > 0) else (tot_demand_m3 * 0.15)
        in_demand = indoor_demand_m3 if (indoor_demand_m3 is not None and indoor_demand_m3 > 0) else max(0.0, tot_demand_m3 - out_demand)
        
        pluv_to_outdoor = min(annual_saved_m3 * 0.35, out_demand) if out_demand > 0 else 0.0
        pluv_to_indoor = max(0.0, annual_saved_m3 - pluv_to_outdoor)
        
        calc_out_pct = (pluv_to_outdoor / out_demand * 100.0) if out_demand > 0 else 0.0
        calc_in_pct = (pluv_to_indoor / in_demand * 100.0) if in_demand > 0 else savings_pct
    else:
        # Modo Avançado com demanda externa
        if indoor_savings_pct is not None:
            calc_in_pct = max(0.0, min(100.0, float(indoor_savings_pct)))
        else:
            calc_in_pct = savings_pct

        if outdoor_savings_pct is not None:
            calc_out_pct = max(0.0, min(100.0, float(outdoor_savings_pct)))
        else:
            calc_out_pct = 100.0 if savings_pct >= 25.0 else min(100.0, savings_pct * 4.0)

    # 1. LEED v4 / v4.1 WE (Water Efficiency)
    # WEc1: Redução do uso externo (Outdoor Water Use Reduction)
    # Requer demanda de irrigação/externa para ser atendida pelo sistema pluvial.
    # Sem demanda externa no projeto, não pontua em WEc1 (0 pts) e indica explicitamente como não aplicável.
    if has_real_outdoor and calc_out_pct >= 95.0:
        outdoor_pts = 2
        outdoor_status = "Elegível (Máximo)"
        outdoor_perf = f"Economia externa: {calc_out_pct:.1f}%"
        outdoor_notes = "Dispensa potável em irrigação e torneiras de jardim via água pluvial filtrada."
    elif has_real_outdoor and calc_out_pct >= 50.0:
        outdoor_pts = 1
        outdoor_status = "Elegível (1 pt)"
        outdoor_perf = f"Economia externa: {calc_out_pct:.1f}%"
        outdoor_notes = "Redução mínima de 50% no uso de água potável para irrigação alcançada."
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
    if tot_leed >= 6:
        leed_badge = "Alta Pontuação (Ouro/Platina)"
    elif tot_leed >= 3:
        leed_badge = "Média Pontuação (Prata)"
    elif tot_leed >= 1:
        leed_badge = "Pontuação Inicial (Certificado)"
    else:
        leed_badge = "Abaixo do limiar LEED (Mín. 25%)"

    mode_text = " (estimado via Modo Simplificado)" if (is_simplified_mode and has_real_outdoor) else ""
    if not has_real_outdoor or calc_out_pct <= 0:
        outdoor_desc = "sem demanda externa cadastrada no projeto (0 de 2 pontos no crédito WEc1)"
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

    # 2. Processo AQUA-HQE (Categoria 4 - Gestão da Água do Empreendimento)
    if savings_pct >= 40.0 or (calc_in_pct >= 35.0 and calc_out_pct >= 50.0):
        aqua_level = "Excelente"
        aqua_stars = 3
        aqua_desc = "Perfil Excelente na Categoria 4 (Gestão da Água e fontes alternativas)."
    elif savings_pct >= 25.0 or calc_in_pct >= 25.0:
        aqua_level = "Boas Práticas"
        aqua_stars = 2
        aqua_desc = "Perfil de Boas Práticas (nível intermediário de eficiência hídrica)."
    elif savings_pct >= 10.0 or calc_in_pct >= 15.0:
        aqua_level = "Base"
        aqua_stars = 1
        aqua_desc = "Atendimento ao nível Base normativo AQUA-HQE."
    else:
        aqua_level = "Insuficiente"
        aqua_stars = 0
        aqua_desc = "Economia inferior a 10%, insuficiente para perfil de destaque AQUA."

    aqua_result = AquaHqeRating(
        performance_level=aqua_level,
        stars=aqua_stars,
        description=aqua_desc,
    )

    # 3. Selo Casa Azul CAIXA (Critério 2.1 - Conservação de Água por Fontes Alternativas)
    if savings_pct >= 30.0 or (calc_in_pct >= 30.0 and calc_out_pct >= 50.0):
        casa_cat = "Diamante"
        casa_pts = 5
        casa_met = True
        casa_desc = "Atende com folga ao critério de fontes alternativas em graduação Diamante."
    elif savings_pct >= 20.0 or calc_in_pct >= 20.0:
        casa_cat = "Ouro"
        casa_pts = 3
        casa_met = True
        casa_desc = "Atende ao critério de aproveitamento pluvial em graduação Ouro."
    elif savings_pct >= 10.0 or calc_in_pct >= 10.0:
        casa_cat = "Prata"
        casa_pts = 2
        casa_met = True
        casa_desc = "Atende aos requisitos básicos da graduação Prata."
    else:
        casa_cat = "Não Elegível"
        casa_pts = 0
        casa_met = False
        casa_desc = "Economia insuficiente para pontuação Casa Azul."

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

    summary_text = (
        f"O empreendimento atinge substituição hídrica global de {savings_pct:.1f}% "
        f"(interno: {calc_in_pct:.1f}%, externo: {calc_out_pct:.1f}%), "
        f"poupando {annual_saved_m3:,.0f} m³/ano de água tratada "
        f"({lifetime_saved_m3:,.0f} m³ acumulados em {project_lifetime_years} anos). "
        f"No Selo LEED v4 WE (máximo de {LEED_WE_MAX_PONTOS} pontos possíveis), o projeto tirou "
        f"{tot_leed} de {LEED_WE_MAX_PONTOS} pontos "
        f"e qualificou-se com perfil '{aqua_level}' no Processo AQUA-HQE. "
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
            certification="Processo AQUA-HQE",
            credit_code="Categoria 4",
            credit_name="Gestão da Água",
            focus="Consumo Global do Lote",
            requirement_rule="Base: ≥ 10% (⭐) | Boas Práticas: ≥ 25% (⭐⭐) | Excelente: ≥ 40% (⭐⭐⭐)",
            achieved_performance=f"Substituição global: {savings_pct:.1f}%",
            points_or_level=f"{aqua_level} ({'⭐'*aqua_stars if aqua_stars > 0 else '—'})",
            status=f"Conforme Perfil {aqua_level}",
            notes="Avalia retenção hidrológica no lote, redução da pegada hídrica e NBR 16783."
        ),
        EsgCreditDetail(
            certification="Selo Casa Azul CAIXA",
            credit_code="Critério 2.1",
            credit_name="Fontes Alternativas & Reúso",
            focus="Edificação Habitacional",
            requirement_rule="Prata: ≥ 10% (+2 pts) | Ouro: ≥ 20% (+3 pts) | Diamante: ≥ 30% (+5 pts)",
            achieved_performance=f"Substituição de potável: {savings_pct:.1f}%",
            points_or_level=f"Nível {casa_cat} (+{casa_pts} pts)",
            status="Critério Atingido" if casa_met else "Economia insuficiente (< 10%)",
            notes="Gera bonificação e elegibilidade a juros reduzidos em financiamentos habitacionais CAIXA."
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

    return EsgConsolidatedReport(
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
