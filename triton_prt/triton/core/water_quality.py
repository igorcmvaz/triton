"""Qualidade da agua pluvial e dimensionamento da linha de tratamento (ETAP).

**Conferido contra o texto da ABNT NBR 15527:2019 em 2026-09-08.** O resultado
dessa conferencia mudou o que este modulo pode afirmar.

A norma de 2019 **nao traz** matriz de classes de uso. A secao 4.6.3, Tabela 1,
estabelece um unico conjunto de parametros minimos, valido para todos os usos
nao potaveis listados em 4.1.7:

    Escherichia coli   < 200 / 100 mL
    Turbidez           < 5,0 uT
    pH                 6,0 a 9,0

E a secao 4.6.5 recomenda cloro residual livre entre 0,5 e 2,0 mg/L, com maximo
permitido de 5 mg/L.

Tres consequencias para este codigo:

1. A **Classe 1** reproduz a Tabela 1 quase exatamente, e por isso e a unica que
   pode invocar a norma. Duas ressalvas: a norma fala em *Escherichia coli*, nao
   em coliformes termotolerantes (E. coli e subconjunto destes, de modo que o
   limite aqui e mais restritivo que o normativo); e a norma **nao tem parametro
   de cor**, que aqui e acrescimo de projeto.
2. As **Classes 2, 3 e 4 nao sao da NBR 15527:2019.** Sao esquema adaptado deste
   programa, coerente com a pratica corrente e com a edicao de 2007 da norma,
   que trazia parametros por uso. Exibi-las como normativas era atribuicao
   incorreta, e foi corrigido.
3. O **descarte de escoamento inicial** recomendado pela norma, na falta de
   dados, e de **2 mm** (secao 4.3.5). Este modulo dizia 1,0 mm.

Outros pontos do texto que o programa passa a poder citar com precisao: a norma
da a disponibilidade por ``Vdisp = P x A x C x eta``, recomendando eta = 0,85 na
falta de dados (4.1.6); lista sete usos nao potaveis admitidos (4.1.7); e exige
monitoramento com frequencia minima semestral (4.6.7).
"""

from triton.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO, LAMINA_DE_DESCARTE_PADRAO_MM
import math
from dataclasses import dataclass, field

from typing import List, Optional

from triton.core.chlorination import (
    Cloracao,
    FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
    PUREZA_PADRAO,
)
from triton.core.grid_emission_factors import BASE_PADRAO, fator_co2eq

# Preco medio da energia eletrica residencial usado para o custo operacional
# do reator UV. Permanece premissa interna, editavel.
ENERGY_PRICE_BRL_PER_KWH = 0.95
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
        nome="Classe 1: parâmetros mínimos da NBR 15527:2019",
        descricao=("Conjunto normativo da NBR 15527:2019 (Tabela 1 e item 4.6.5), válido para todos os usos não potáveis previstos em 4.1.7: bacias sanitárias, mictórios, lavagem de pisos e veículos, reserva de incêndio, uso ornamental, irrigação paisagística e sistemas de resfriamento. A norma trata de E. coli, não de coliformes termotolerantes, e não define parâmetro de cor. Para sistemas de resfriamento, o item 4.6.2 não fixa parâmetros: eles vêm do fabricante do equipamento ou de profissional habilitado."),
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
        nome="Classe 2 (adaptada, não normativa): Irrigação de Jardins e Lavagem de Pisos/Veículos",
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
        nome="Classe 3 (adaptada, não normativa): Torres de Resfriamento e Caldeiras Industriais",
        descricao="Usos industriais e climatização com controle severo de biofilme e incrustação. A ABNT NBR 15527:2019 (item 4.6.2) não fixa parâmetros para resfriamento: confira os limites com o fabricante do equipamento.",
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
        nome="Classe 4 (adaptada, não normativa): Lavagem de Roupas e Usos Nobres Não Potáveis",
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
    roof_runoff_coeff: float = COEFICIENTE_DE_ESCOAMENTO_PADRAO,
    events_per_year: int = 80
) -> FirstFlushAnalysis:
    """
    Calcula a eficiência do descarte de primeira chuva através do modelo exponencial de lavagem:
    E(d) = 100 * (1 - exp(-k * d))
    onde k varia por tipo de contaminante.
    """
    d = max(0.0, float(discard_mm))

    # Coeficientes de decaimento da curva de lavagem, por fração de sujeira.
    #
    # A finalidade desta função é **correlacionar** a lâmina descartada com a
    # melhoria esperada de qualidade, para que o usuário veja o efeito da escolha
    # do descarte. Não é modelo preditivo: os coeficientes são parâmetros de
    # projeto, situados na faixa relatada pela literatura de first flush, e não
    # resultam de ajuste a dados medidos.
    #
    # A referência de apoio é MAYKOT, MARTINS VAZ & GHISI (2025), Water 17(12),
    # art. 1772, DOI 10.3390/w17121772, que caracteriza experimentalmente o
    # descarte de primeira chuva em edificações.
    #
    # A ordem entre eles tem base física: partícula pesada sai no primeiro
    # impacto das gotas, e biofilme aderido à telha resiste mais. Daí o menor
    # coeficiente ser o das bactérias.
    k_solids = 1.6    # sólidos grosseiros e sedimentáveis
    k_turbidity = 1.3 # partículas finas e fuligem
    k_bacteria = 1.1  # carga bacteriológica e biofilme

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
        classification = "Descarte recomendado pela NBR 15527:2019 (2 mm)"
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
class FirstFlushSizingResult:
    """Dimensionamento físico e orçamentário do sistema de descarte de primeiras águas.

    Composto por:
    1. Filtro de folhas e gradeamento preliminar autolimpante em tela inox 304;
    2. Reservatório de descarte com volume igual a descarte (mm) * área (m²) em Litros;
    3. Dispositivo de purga lenta / dreno calibrado automático para esvaziamento em tempo seco.
    """
    discard_mm: float
    roof_area_m2: float
    diverter_volume_liters: float
    leaf_filter_type: str
    diverter_tank_type: str
    leaf_filter_capex: float
    diverter_tank_capex: float
    first_flush_total_capex: float
    first_flush_annual_opex: float
    first_flush_embodied_co2_kg: float
    purge_drain_description: str
    material_description: str
    diverter_mass_kg: float
    leaf_filter_mass_kg: float


def _interp_pead_tank_price(volume_l: float) -> float:
    """Interpolação contínua de preços de reservatórios PEAD Fortlev de mercado."""
    pts = [
        (310.0, 246.90), (500.0, 269.90), (750.0, 459.90), (1000.0, 459.90),
        (2000.0, 1139.90), (3000.0, 2051.90), (5000.0, 2999.90), (10000.0, 5499.90)
    ]
    v = max(0.0, float(volume_l))
    if v <= pts[0][0]:
        return pts[0][1]
    if v >= pts[-1][0]:
        slope = (pts[-1][1] - pts[-2][1]) / (pts[-1][0] - pts[-2][0])
        return pts[-1][1] + slope * (v - pts[-1][0])
    for i in range(len(pts) - 1):
        if pts[i][0] <= v <= pts[i + 1][0]:
            frac = (v - pts[i][0]) / max(1e-6, pts[i + 1][0] - pts[i][0])
            return pts[i][1] + frac * (pts[i + 1][1] - pts[i][1])
    return pts[-1][1]


def size_first_flush_system(
    discard_mm: float = LAMINA_DE_DESCARTE_PADRAO_MM,
    roof_area_m2: float = 100.0,
    regional_factor: float = 1.0,
) -> FirstFlushSizingResult:
    """Dimensiona o subsistema de descarte de primeiras águas e gradeamento preliminar.

    Calcula o volume do reservatório de descarte V = descarte (mm) * área (m²) [L],
    orça o filtro de folhas com tela em inox 304 e o reservatório com válvula de purga lenta.
    """
    d = max(0.0, float(discard_mm))
    area = max(0.0, float(roof_area_m2))
    diverter_vol = d * area  # Litros (1 mm * 1 m² = 1 L)

    if diverter_vol <= 0.0 or d <= 0.0 or area <= 0.0:
        return FirstFlushSizingResult(
            discard_mm=d,
            roof_area_m2=area,
            diverter_volume_liters=0.0,
            leaf_filter_type="Nenhum (Descarte não configurado)",
            diverter_tank_type="Nenhum",
            leaf_filter_capex=0.0,
            diverter_tank_capex=0.0,
            first_flush_total_capex=0.0,
            first_flush_annual_opex=0.0,
            first_flush_embodied_co2_kg=0.0,
            purge_drain_description="Nenhum",
            material_description="Nenhum",
            diverter_mass_kg=0.0,
            leaf_filter_mass_kg=0.0,
        )

    # 1. Filtro de Folhas e Gradeamento Preliminar
    if area <= 200.0:
        leaf_filter_type = "Separador de Folhas e Gradeamento Autolimpante DN 100 (Tela Inox 304, malha 1,0 mm)"
        base_leaf_capex = 220.0
        leaf_mass = 1.8
    elif area <= 500.0:
        leaf_filter_type = "Separador de Folhas Duplo / Gradeamento DN 150 (Tela Inox 304, malha 1,2 mm)"
        base_leaf_capex = 440.0
        leaf_mass = 3.6
    else:
        unidades = int(math.ceil(area / 250.0))
        leaf_filter_type = f"Sistema de Gradeamento Multicâmaras nas Prumadas ({unidades} un. Separadores Inox 304)"
        base_leaf_capex = unidades * 220.0
        leaf_mass = unidades * 1.8

    leaf_capex = base_leaf_capex * regional_factor

    # 2. Reservatório de Descarte Inicial
    if diverter_vol <= 250.0:
        diverter_tank_type = (
            f"Coluna Vertical de Desvio em PVC Rígido DN 150/200 ({diverter_vol:.0f} L) "
            "com Conexões, Cap Roscado de Inspeção e Válvula de Purga Lenta"
        )
        mat_desc = "PVC Rígido Classe Pluvial e Válvula de Purga/Retenção"
        base_tank_capex = (diverter_vol * 2.20) + 120.0
        diverter_mass = (diverter_vol * 0.084) + 1.2
    else:
        diverter_tank_type = (
            f"Reservatório Estanque de Descarte em PEAD Rotomoldado ({diverter_vol:.0f} L) "
            "com Extravasor Superior, Boia Flutuante de Vedação e Purga Lenta Calibrada"
        )
        mat_desc = "Polietileno de Alta Densidade (PEAD) Rotomoldado e Dispositivo de Vedação/Purga"
        pead_price = _interp_pead_tank_price(diverter_vol)
        base_tank_capex = pead_price + 150.0
        diverter_mass = (diverter_vol / 1000.0) * 25.0

    tank_capex = base_tank_capex * regional_factor

    purge_desc = (
        "Válvula de micro-drenagem calibrada / orifício com tela de retenção de sedimentos "
        "para esvaziamento automático lento em 24-48 horas de tempo seco."
    )
    opex_yr = 40.0 * regional_factor

    # Pegada de carbono incorporada: ~2.10 kg CO2e / kg plástico e ~3.00 kg CO2e / kg inox
    embodied_co2 = (diverter_mass * 2.10) + (leaf_mass * 3.00)

    return FirstFlushSizingResult(
        discard_mm=d,
        roof_area_m2=area,
        diverter_volume_liters=diverter_vol,
        leaf_filter_type=leaf_filter_type,
        diverter_tank_type=diverter_tank_type,
        leaf_filter_capex=round(leaf_capex, 2),
        diverter_tank_capex=round(tank_capex, 2),
        first_flush_total_capex=round(leaf_capex + tank_capex, 2),
        first_flush_annual_opex=round(opex_yr, 2),
        first_flush_embodied_co2_kg=round(embodied_co2, 2),
        purge_drain_description=purge_desc,
        material_description=mat_desc,
        diverter_mass_kg=round(diverter_mass, 2),
        leaf_filter_mass_kg=round(leaf_mass, 2),
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
    disinfection_stages: List[str] = field(default_factory=list)
    # A classe alvo recomenda filtracao fina e o usuario dispensou. Nao e erro:
    # as classes 2 a 4 sao adaptadas e nao normativas, de modo que a recomendacao
    # e do programa. Fica registrado para o relatorio poder declarar a escolha.
    polishing_recommended_but_declined: bool = False

    # Sistema de Descarte de Primeiras Águas (First Flush) e Gradeamento
    first_flush: Optional[FirstFlushSizingResult] = None
    first_flush_diverter_vol_l: float = 0.0
    first_flush_capex: float = 0.0
    first_flush_embodied_co2_kg: float = 0.0


def size_etap(
    target_class_id: str = "classe_1",
    annual_pluvial_consumed_m3: float = 120.0,
    roof_area_m2: float = 100.0,
    disinfection_choice: str = "cloro",
    include_polishing_filter: bool = False,
    chlorine_dose_mg_l: float = 1.5,
    # O mesmo padrão de TritonConfig.chlorine_cost_per_kg: com 38, a linha de
    # tratamento chamada sem o preço cobrava a pastilha mais caro que o fluxo de caixa.
    chlorine_kg_price_brl: float = 25.0,
    regional_factor: float = 1.0,
    grid_co2_factor_kg_kwh: Optional[float] = None,
    chlorine_product_purity: float = PUREZA_PADRAO,
    chlorine_co2_kg_per_kg: float = FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
    discard_mm: float = 0.0,
    include_first_flush: bool = False,
) -> EtapSizingResult:
    """
    Dimensiona os equipamentos e insumos químicos da ETAP.
    """
    target_class = WATER_QUALITY_CLASSES.get(target_class_id, WATER_QUALITY_CLASSES["classe_1"])

    if grid_co2_factor_kg_kwh is None:
        grid_co2_factor_kg_kwh = fator_co2eq(BASE_PADRAO)

    # 0. Sistema de Descarte de Primeiras Águas (First Flush) e Gradeamento
    ff_res: Optional[FirstFlushSizingResult] = None
    ff_capex = 0.0
    ff_opex = 0.0
    ff_vol = 0.0
    ff_co2 = 0.0
    if include_first_flush and discard_mm > 0.0:
        ff_res = size_first_flush_system(
            discard_mm=discard_mm,
            roof_area_m2=roof_area_m2,
            regional_factor=regional_factor,
        )
        ff_capex = ff_res.first_flush_total_capex
        ff_opex = ff_res.first_flush_annual_opex
        ff_vol = ff_res.diverter_volume_liters
        ff_co2 = ff_res.first_flush_embodied_co2_kg

    # 1. Filtro mecânico de entrada (vórtex ou cesto autolimpante)
    #
    # Os limites de faixa acompanham a área que o próprio produto declara
    # atender. Antes desta revisão eles eram 150 e 400 m², contra rótulos de
    # "até 200 m²" e "até 500 m²": um telhado de 180 m² recebia o filtro da
    # faixa seguinte, mais caro em R$ 600, embora o da primeira faixa fosse
    # declarado suficiente. O separador de folhas da Bakof Tec, por exemplo,
    # é indicado para coberturas de até 200 m².
    if roof_area_m2 <= 200.0:
        pre_filter_type = "Filtro Autolimpante Vórtex DN 100 (Até 200 m²)"
        pre_filter_mesh_microns = 350
        base_pre_filter_capex = 650.0
    elif roof_area_m2 <= 500.0:
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

    # A cloracao e obrigatoria: e a unica barreira que deixa residual livre, e a
    # NBR 15527:2019 (4.6.5) trabalha justamente com residual entre 0,5 e 2,0 mg/L.
    # UV e ozonio desinfetam na passagem e nao deixam residual, de modo que sao
    # estagios ADICIONAIS, nao alternativas.
    method = disinfection_choice.lower()

    base_dosador_capex = 280.0
    disinf_capex = base_dosador_capex * regional_factor

    dose = max(0.5, float(chlorine_dose_mg_l))
    # A pureza e o fator vem do projeto, nao de valores fixos: sao os mesmos que
    # o modulo economico e a ACV usam, e e essa identidade que permite descontar
    # a parcela do cloro sem contar duas vezes.
    cloracao = Cloracao(
        dose_mg_por_litro=dose,
        pureza=max(1e-6, float(chlorine_product_purity)),
        fator_kg_co2e_por_kg_produto=max(0.0, float(chlorine_co2_kg_per_kg)),
    )
    annual_chlorine_kg = cloracao.massa_anual_de_produto_kg(annual_vol)
    annual_chlorine_cost = annual_chlorine_kg * chlorine_kg_price_brl
    disinf_opex = annual_chlorine_cost
    co2e_chemicals_kg = cloracao.co2e_anual_kg(annual_vol)

    disinfection_stages = ["Cloração (dosador de pastilhas de hipoclorito de cálcio)"]

    if method == "uv":
        # Reator ultravioleta germicida, dose > 30 mJ/cm2 (NSF/ANSI 55).
        if annual_vol <= 200.0:
            uv_watts = 25.0
            base_uv_capex = 1200.0
            uv_lamp_cost = 180.0
        else:
            uv_watts = 55.0
            base_uv_capex = 2200.0
            uv_lamp_cost = 320.0

        disinf_capex += base_uv_capex * regional_factor
        # Operacao estimada em 1.500 h/ano, junto ao bombeamento.
        uv_kwh = (uv_watts * 1500.0) / 1000.0
        # A energia do reator entrava em lugar nenhum: nem no custo, nem na
        # emissao. Agora entra nos dois.
        disinf_opex += uv_lamp_cost * regional_factor + uv_kwh * ENERGY_PRICE_BRL_PER_KWH
        co2e_chemicals_kg += (uv_watts * 0.12) + uv_kwh * grid_co2_factor_kg_kwh
        disinfection_stages.append("Reator ultravioleta (barreira adicional, sem residual)")

    elif method == "ozonio":
        disinf_capex += 3500.0 * regional_factor
        disinf_opex += 200.0 * regional_factor
        co2e_chemicals_kg += 15.0
        disinfection_stages.append("Ozonização (barreira adicional, sem residual)")

    # 3. Filtro de Polimento (Carvão Ativado ou Areia)
    polishing_capex = 0.0
    polishing_opex = 0.0
    polishing_type = "Nenhum (Qualidade padrão atendida)"

    # A escolha do usuario manda. Antes desta revisao a condicao era
    # `include_polishing_filter or target_class.exige_filtracao_fina`, e a classe
    # sobrepunha a escolha em silencio: desmarcar a caixa nao surtia efeito
    # nenhum nas classes 2 a 4.
    polimento_recomendado = bool(target_class.exige_filtracao_fina)
    polimento_recusado = polimento_recomendado and not include_polishing_filter

    if include_polishing_filter:
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

    if polimento_recusado:
        polishing_type = (
            "Nenhum — a classe alvo recomenda filtração fina, e ela foi dispensada. "
            "As classes 2 a 4 são adaptadas e não normativas: a recomendação é do "
            "programa, e a escolha é do projetista."
        )

    tot_capex = pre_filter_capex + disinf_capex + polishing_capex + ff_capex
    tot_opex = disinf_opex + polishing_opex + ff_opex

    return EtapSizingResult(
        pre_filter_type=pre_filter_type,
        pre_filter_mesh_microns=pre_filter_mesh_microns,
        pre_filter_capex=pre_filter_capex,
        disinfection_method=method,
        # A cloracao e sempre aplicada (4.6.5 da NBR 15527:2019 exige residual
        # livre), de modo que a dose adotada vale para qualquer metodo escolhido.
        chlorine_dose_mg_l=dose,
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
        polishing_recommended_but_declined=polimento_recusado,
        total_etap_capex=tot_capex,
        total_etap_annual_opex=tot_opex,
        total_etap_co2e_kg_yr=co2e_chemicals_kg,
        target_quality_class=target_class.nome,
        disinfection_stages=disinfection_stages,
        first_flush=ff_res,
        first_flush_diverter_vol_l=ff_vol,
        first_flush_capex=ff_capex,
        first_flush_embodied_co2_kg=ff_co2,
    )
