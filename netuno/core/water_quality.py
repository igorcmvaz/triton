"""
Módulo Core de Qualidade da Água e Dimensionamento da ETAP (Estação de Tratamento de Água Pluvial).
Baseado nas diretrizes da ABNT NBR 15527:2019 e NBR 16783 (Usos não potáveis de fontes alternativas).
Inclui modelo de remoção por descarte de primeira chuva (wash-off), matriz de usos finais,
dimensionamento paramétrico de filtros mecânicos, desinfecção (cloração e radiação UV) e filtros de polimento.
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class WaterQualityClass:
    """Classe de qualidade de água não potável conforme NBR 15527 e NBR 16783."""
    id: str
    nome: str
    descricao: str
    turbidez_max_ntu: float
    cor_aparente_max_uh: float
    ph_min: float
    ph_max: float
    cloro_residual_min_mg_l: float
    cloro_residual_max_mg_l: float
    coliformes_termo_max_ufc_100ml: float
    exige_desinfeccao: bool
    exige_filtracao_fina: bool


WATER_QUALITY_CLASSES: Dict[str, WaterQualityClass] = {
    "classe_1": WaterQualityClass(
        id="classe_1",
        nome="Classe 1: Bacias Sanitárias e Mictórios",
        descricao="Descargas em bacias sanitárias e mictórios sem contato dérmico direto.",
        turbidez_max_ntu=5.0,
        cor_aparente_max_uh=15.0,
        ph_min=6.0,
        ph_max=9.0,
        cloro_residual_min_mg_l=0.5,
        cloro_residual_max_mg_l=2.0,
        coliformes_termo_max_ufc_100ml=200.0,
        exige_desinfeccao=True,
        exige_filtracao_fina=False,
    ),
    "classe_2": WaterQualityClass(
        id="classe_2",
        nome="Classe 2: Irrigação de Jardins e Lavagem de Pisos/Veículos",
        descricao="Contato dérmico eventual e geração moderada de aerossóis.",
        turbidez_max_ntu=5.0,
        cor_aparente_max_uh=15.0,
        ph_min=6.0,
        ph_max=9.0,
        cloro_residual_min_mg_l=1.0,
        cloro_residual_max_mg_l=3.0,
        coliformes_termo_max_ufc_100ml=0.0,  # Ausência
        exige_desinfeccao=True,
        exige_filtracao_fina=True,
    ),
    "classe_3": WaterQualityClass(
        id="classe_3",
        nome="Classe 3: Torres de Resfriamento e Caldeiras Industriais",
        descricao="Usos industriais e climatização com controle severo de biofilme e incrustação.",
        turbidez_max_ntu=2.0,
        cor_aparente_max_uh=10.0,
        ph_min=6.5,
        ph_max=8.5,
        cloro_residual_min_mg_l=1.0,
        cloro_residual_max_mg_l=2.5,
        coliformes_termo_max_ufc_100ml=0.0,
        exige_desinfeccao=True,
        exige_filtracao_fina=True,
    ),
    "classe_4": WaterQualityClass(
        id="classe_4",
        nome="Classe 4: Lavagem de Roupas e Usos Nobres Não Potáveis",
        descricao="Usos que exigem água translúcida e isenta de odores para não manchar tecidos.",
        turbidez_max_ntu=2.0,
        cor_aparente_max_uh=5.0,
        ph_min=6.5,
        ph_max=8.5,
        cloro_residual_min_mg_l=0.5,
        cloro_residual_max_mg_l=1.5,
        coliformes_termo_max_ufc_100ml=0.0,
        exige_desinfeccao=True,
        exige_filtracao_fina=True,
    ),
}


@dataclass
class FirstFlushAnalysis:
    """Resultado do modelo de lavagem (wash-off) para descarte inicial."""
    discard_mm: float
    removal_coarse_solids_pct: float
    removal_turbidity_pct: float
    removal_bacteria_pct: float
    estimated_raw_turbidity_ntu: float
    estimated_post_discard_turbidity_ntu: float
    annual_discard_volume_m3: float
    cleanliness_classification: str
    recommendation_text: str


def calculate_first_flush_washoff(
    discard_mm: float,
    roof_area_m2: float = 100.0,
    annual_precipitation_mm: float = 1500.0,
    roof_runoff_coeff: float = 0.85,
    events_per_year: int = 80
) -> FirstFlushAnalysis:
    """
    Calcula a eficiência do descarte de primeira chuva através do modelo exponencial de lavagem:
    E(d) = 100 * (1 - exp(-k * d))
    onde k varia por tipo de contaminante.
    """
    d = max(0.0, float(discard_mm))

    # Coeficientes de lavagem empíricos calibrados da literatura hidrológica urbana
    k_solids = 1.6   # Sólidos grosseiros lavam rapidamente
    k_turbidity = 1.3 # Partículas finas/turbidez
    k_bacteria = 1.1  # Bactérias e biofilme aderido lavam mais lentamente

    rem_solids = 100.0 * (1.0 - math.exp(-k_solids * d)) if d > 0 else 0.0
    rem_turb = 100.0 * (1.0 - math.exp(-k_turbidity * d)) if d > 0 else 0.0
    rem_bact = 100.0 * (1.0 - math.exp(-k_bacteria * d)) if d > 0 else 0.0

    raw_turbidity = 45.0  # NTU médio de escoamento superficial de telhado sem descarte
    post_turbidity = max(1.5, raw_turbidity * (1.0 - rem_turb / 100.0))

    # Volume anual descartado em m³ (aproximado por eventos de chuva distintos)
    discard_vol_per_event_m3 = (d / 1000.0) * roof_area_m2 * roof_runoff_coeff
    annual_discard_m3 = discard_vol_per_event_m3 * events_per_year

    if d < 0.5:
        classification = "Descarte Mínimo / Insuficiente"
        recom = (
            "Descarte abaixo do recomendado pela NBR 15527. Risco elevado de carrear fuligem, "
            "poeiras e matéria orgânica pesada para o reservatório, exigindo trocas frequentes de filtros."
        )
    elif d < 1.5:
        classification = "Descarte Padrão NBR 15527 (1,0 mm)"
        recom = (
            "Atende plenamente aos requisitos da NBR 15527. Remove entre 75% e 85% dos sólidos iniciais, "
            "garantindo excelente proteção à bomba e redução expressiva no consumo de desinfetante."
        )
    else:
        classification = "Descarte Rigoroso / Alta Eficiência (> 1,5 mm)"
        recom = (
            "Excelente eficiência de retenção (>90% de remoção de contaminantes iniciais). "
            "Recomendado para centros urbanos de tráfego intenso ou aplicações industriais e lavagem de roupas."
        )

    return FirstFlushAnalysis(
        discard_mm=d,
        removal_coarse_solids_pct=rem_solids,
        removal_turbidity_pct=rem_turb,
        removal_bacteria_pct=rem_bact,
        estimated_raw_turbidity_ntu=raw_turbidity,
        estimated_post_discard_turbidity_ntu=post_turbidity,
        annual_discard_volume_m3=annual_discard_m3,
        cleanliness_classification=classification,
        recommendation_text=recom,
    )


@dataclass
class EtapSizingResult:
    """Resultado do dimensionamento da linha de tratamento da água pluvial."""
    # Filtro mecânico de entrada
    pre_filter_type: str
    pre_filter_mesh_microns: int
    pre_filter_capex: float
    
    # Desinfecção
    disinfection_method: str  # "cloro", "uv", "ozonio", "nenhum"
    chlorine_dose_mg_l: float
    annual_chlorine_kg: float
    annual_chlorine_cost_brl: float
    uv_power_watts: float
    uv_annual_kwh: float
    uv_annual_lamp_cost_brl: float
    disinfection_capex: float
    disinfection_opex_yr: float
    
    # Filtro de polimento
    polishing_filter_type: str
    polishing_capex: float
    polishing_annual_opex: float
    
    # Totais ETAP
    total_etap_capex: float
    total_etap_annual_opex: float
    total_etap_co2e_kg_yr: float
    target_quality_class: str


def size_etap(
    target_class_id: str = "classe_1",
    annual_pluvial_consumed_m3: float = 120.0,
    roof_area_m2: float = 100.0,
    disinfection_choice: str = "cloro",
    include_polishing_filter: bool = False,
    chlorine_dose_mg_l: float = 1.5,
    chlorine_kg_price_brl: float = 38.0,
    regional_factor: float = 1.0,
) -> EtapSizingResult:
    """
    Dimensiona os equipamentos e insumos químicos da ETAP.
    """
    target_class = WATER_QUALITY_CLASSES.get(target_class_id, WATER_QUALITY_CLASSES["classe_1"])

    # 1. Filtro mecânico de entrada (Vórtex ou Cesto autolimpante)
    if roof_area_m2 <= 150.0:
        pre_filter_type = "Filtro Autolimpante Vórtex DN 100 (Até 200 m²)"
        pre_filter_mesh_microns = 350
        base_pre_filter_capex = 650.0
    elif roof_area_m2 <= 400.0:
        pre_filter_type = "Filtro Autolimpante Vórtex DN 150 (Até 500 m²)"
        pre_filter_mesh_microns = 400
        base_pre_filter_capex = 1250.0
    else:
        pre_filter_type = "Filtro Industrial de Cesto / Ciclônico DN 200 (Grandes Telhados)"
        pre_filter_mesh_microns = 500
        base_pre_filter_capex = 2800.0

    pre_filter_capex = base_pre_filter_capex * regional_factor

    # 2. Desinfecção
    annual_vol = max(1.0, float(annual_pluvial_consumed_m3))
    disinf_capex = 0.0
    disinf_opex = 0.0
    annual_chlorine_kg = 0.0
    annual_chlorine_cost = 0.0
    uv_watts = 0.0
    uv_kwh = 0.0
    uv_lamp_cost = 0.0
    co2e_chemicals_kg = 0.0

    method = disinfection_choice.lower()
    if method == "cloro":
        # Dosador de pastilhas de hipoclorito de cálcio (65% cloro ativo)
        base_dosador_capex = 280.0
        disinf_capex = base_dosador_capex * regional_factor
        
        dose = max(0.5, float(chlorine_dose_mg_l))
        # Massa de cloro necessária = V (m³) * dose (g/m³) / 1000 = kg de cloro ativo
        # Pastilhas têm 65% de pureza ativa:
        active_kg = (annual_vol * dose) / 1000.0
        annual_chlorine_kg = active_kg / 0.65
        annual_chlorine_cost = annual_chlorine_kg * chlorine_kg_price_brl
        disinf_opex = annual_chlorine_cost
        
        # Emissão de fabricação do hipoclorito: ~1.85 kg CO2e / kg
        co2e_chemicals_kg = annual_chlorine_kg * 1.85

    elif method == "uv":
        # Reator Ultravioleta germicida (dose > 30 mJ/cm²)
        if annual_vol <= 200.0:
            uv_watts = 25.0
            base_uv_capex = 1200.0
            uv_lamp_cost = 180.0
        else:
            uv_watts = 55.0
            base_uv_capex = 2200.0
            uv_lamp_cost = 320.0
            
        disinf_capex = base_uv_capex * regional_factor
        # Estimativa de operação anual UV: ligada junto ao bombeamento (~1.500 horas/ano)
        uv_kwh = (uv_watts * 1500.0) / 1000.0
        # Substituição anual da lâmpada germicida (9.000 h úteis):
        disinf_opex = uv_lamp_cost * regional_factor
        co2e_chemicals_kg = (uv_watts * 0.12)  # Emissão incorporada amortizada da lâmpada

    elif method == "ozonio":
        disinf_capex = 3500.0 * regional_factor
        disinf_opex = 200.0 * regional_factor
        co2e_chemicals_kg = 15.0
    else:
        # Sem desinfecção
        disinf_capex = 0.0
        disinf_opex = 0.0

    # 3. Filtro de Polimento (Carvão Ativado ou Areia)
    polishing_capex = 0.0
    polishing_opex = 0.0
    polishing_type = "Nenhum (Qualidade padrão atendida)"

    if include_polishing_filter or target_class.exige_filtracao_fina:
        if target_class_id == "classe_4":
            polishing_type = "Filtro de Carvão Ativado em Bloco (Remoção de Cor e Odor)"
            polishing_capex = 550.0 * regional_factor
            polishing_opex = 150.0 * regional_factor  # Troca anual do refil
            co2e_chemicals_kg += 8.0
        else:
            polishing_type = "Filtro de Areia Multicamada / Cartucho Plissado 20 µm"
            polishing_capex = 380.0 * regional_factor
            polishing_opex = 90.0 * regional_factor
            co2e_chemicals_kg += 4.0

    tot_capex = pre_filter_capex + disinf_capex + polishing_capex
    tot_opex = disinf_opex + polishing_opex

    return EtapSizingResult(
        pre_filter_type=pre_filter_type,
        pre_filter_mesh_microns=pre_filter_mesh_microns,
        pre_filter_capex=tot_capex - (disinf_capex + polishing_capex),
        disinfection_method=method,
        chlorine_dose_mg_l=chlorine_dose_mg_l if method == "cloro" else 0.0,
        annual_chlorine_kg=annual_chlorine_kg,
        annual_chlorine_cost_brl=annual_chlorine_cost,
        uv_power_watts=uv_watts,
        uv_annual_kwh=uv_kwh,
        uv_annual_lamp_cost_brl=uv_lamp_cost,
        disinfection_capex=disinf_capex,
        disinfection_opex_yr=disinf_opex,
        polishing_filter_type=polishing_type,
        polishing_capex=polishing_capex,
        polishing_annual_opex=polishing_opex,
        total_etap_capex=tot_capex,
        total_etap_annual_opex=tot_opex,
        total_etap_co2e_kg_yr=co2e_chemicals_kg,
        target_quality_class=target_class.nome,
    )
