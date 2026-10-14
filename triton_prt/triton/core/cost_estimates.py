"""Premissas transparentes, engenharia detalhada e calibração de custos para dimensionamento econômico.

Os custos são carregados a partir do arquivo estruturado JSON em triton/data/costs_database.json,
permitindo edição fácil e direta pelo usuário conforme novas cotações e dados de mercado estejam disponíveis.
Qualquer capacidade (ex: 450 L, 1.250 L, etc.) é interpolada de forma contínua e suave.

Inclui:
- Detalhamento de 8 subsistemas prediais para as 5 tipologias residenciais (UTI, UTG, MSG, MFH, MFL)
- Redundância de motobombas (1+1 operação e reserva) e painéis elétricos automatizados em edifícios
- Automação com sensores de nível, proteção a seco e reposição potável via Air Gap (NBR 5626 / NBR 15527)
- Fatores regionais SINAPI / CUB por UF (27 Unidades Federativas)
- Cálculo integrado de CAPEX e OPEX calibrados (energia B1 ANEEL, desinfecção com cloro e manutenção modular)
"""

import json
from triton.core.chlorination import Cloracao, DOSE_PADRAO_MG_POR_LITRO, PUREZA_PADRAO
import os
from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import numpy as np


COSTS_FILE_PATH = Path(__file__).resolve().parent.parent / "data" / "costs_database.json"

# Fatores Regionais SINAPI/CUB padrão por UF (Ponderação: 55% Materiais + 30% Mão de Obra + 15% Logística/Frete)
_DEFAULT_REGIONAL_FACTORS: Dict[str, float] = {
    "AC": 1.17, "AL": 0.95, "AM": 1.16, "AP": 1.15, "BA": 0.95, "CE": 0.93,
    "DF": 1.06, "ES": 0.97, "GO": 0.95, "MA": 0.96, "MG": 0.95, "MS": 1.02,
    "MT": 1.08, "PA": 1.11, "PB": 0.93, "PE": 0.94, "PI": 0.94, "PR": 0.98,
    "RJ": 1.05, "RN": 0.94, "RO": 1.09, "RR": 1.21, "RS": 1.01, "SC": 1.02,
    "SE": 0.93, "SP": 1.00, "TO": 1.03
}

# Valores padrão de fallback caso o arquivo JSON não seja encontrado ou contenha erro
# Tabela de recurso, usada quando o banco de custos em JSON nao esta legivel.
# Tem de espelhar `lower_tank_pead_prices` do JSON: antes desta revisao ela guardava a
# versao antiga, com 1.750 L a R$ 1.399 e 2.000 L a R$ 1.299 - um reservatorio
# maior custando menos. Bastava o arquivo faltar para o defeito voltar sem aviso.
#
# Fortlev, menor preco anunciado por capacidade em copafer.com.br, com maximo
# corrente para garantir monotonicidade. Ver `_procedencia_precos_reservatorio`
# no JSON para o criterio completo.
_DEFAULT_LOWER_TANK_PRICES = [
    (310, 246.90), (500, 269.90), (750, 459.90), (1000, 459.90),
    (2000, 1139.90), (3000, 2051.90), (5000, 2999.90), (10000, 5499.90),
    (15000, 6935.00),
]

# O reservatorio superior e o mesmo produto; so as capacidades usuais mudam.
_DEFAULT_UPPER_TANK_PRICES = [
    (310, 246.90), (500, 269.90), (750, 459.90), (1000, 459.90),
    (2000, 1139.90),
]

_DEFAULT_MATERIAL_MULTIPLIERS = {
    "PEAD": 1.00,       # Polietileno de alta densidade rotomoldado (referência base de mercado)
    "PRFV": 1.35,       # Poliéster reforçado com fibra de vidro (~35% superior)
    "FIBRA": 1.35,      # Alias usado pelo módulo ambiental/persistência
    "CONCRETO": 2.10,   # Concreto armado moldado in loco com armadura e forma (~110% superior)
    "ACO_INOX": 3.60,   # Aço inoxidável AISI 304/316 de alta durabilidade (~260% superior)
}

_DEFAULT_PIPE_COST_PER_METER = {
    20: 8.20,   # DN 20 mm (1/2"): R$ 8,20/m (SINAPI água fria soldável)
    25: 11.50,  # DN 25 mm (3/4"): R$ 11,50/m (SINAPI 89356 - água fria soldável)
    32: 14.80,  # DN 32 mm (1"): R$ 14,80/m (SINAPI 89357 - água fria soldável)
    40: 16.90,  # DN 40 mm (1 1/4"): R$ 16,90/m (SINAPI 89358 - água fria soldável)
    50: 18.50,  # DN 50 mm (1 1/2"): R$ 18,50/m (SINAPI 89359 - esgoto/água predial)
    60: 22.80,  # DN 60 mm (2"): R$ 22,80/m (SINAPI água fria soldável)
    75: 28.00,  # DN 75 mm (2 1/2"): R$ 28,00/m (SINAPI 89713 - esgoto/água predial)
    85: 32.50,  # DN 85 mm (3"): R$ 32,50/m (SINAPI água fria soldável)
    100: 35.00, # DN 100 mm (4"): R$ 35,00/m (SINAPI 89800 - esgoto/pluvial predial)
    110: 42.00, # DN 110 mm (4"): R$ 42,00/m (SINAPI água fria soldável classe 15)
    150: 68.00, # DN 150 mm (6"): R$ 68,00/m (SINAPI 89849 - subcoletor/pluvial predial)
}

COMMERCIAL_PIPES_CAPEX = [
    {"dn": 20, "pol": '1/2"',   "category": "soldavel", "label": 'DN 20 mm (1/2")'},
    {"dn": 25, "pol": '3/4"',   "category": "soldavel", "label": 'DN 25 mm (3/4")'},
    {"dn": 32, "pol": '1"',     "category": "soldavel", "label": 'DN 32 mm (1")'},
    {"dn": 40, "pol": '1 1/4"', "category": "soldavel", "label": 'DN 40 mm (1 1/4")'},
    {"dn": 50, "pol": '1 1/2"', "category": "soldavel", "label": 'DN 50 mm (1 1/2")'},
    {"dn": 60, "pol": '2"',     "category": "soldavel", "label": 'DN 60 mm (2")'},
    {"dn": 75, "pol": '2 1/2"', "category": "soldavel", "label": 'DN 75 mm (2 1/2")'},
    {"dn": 85, "pol": '3"',     "category": "soldavel", "label": 'DN 85 mm (3")'},
    {"dn": 100, "pol": '4"',    "category": "pluvial",  "label": 'DN 100 mm (4" Pluvial)'},
    {"dn": 110, "pol": '4"',    "category": "soldavel", "label": 'DN 110 mm (4" Soldável)'},
    {"dn": 150, "pol": '6"',    "category": "pluvial",  "label": 'DN 150 mm (6" Pluvial)'},
]

_DEFAULT_CHLORINE_COST_PER_KG = 25.0

_DEFAULT_TYPOLOGY_CONFIGS: Dict[str, Dict[str, Any]] = {
    "UTI": {
        "name": "Casa Unifamiliar Térrea (4 hab)",
        "pump_power_kw": 0.37,
        "pump_count": 1,
        "pump_unit_cost": 301.70,
        "pump_cost_total": 301.70,
        "electrical_panel_cost": 180.00,
        "sensors_automation_cost": 120.00,
        "treatment_filtration_cost": 350.00,
        "air_gap_supplement_cost": 150.00,
        "pipes_base_cost": 950.00,
        "maint_base_annual": 250.00,
        "min_labor_cost": 1400.00,
        "description": "Bomba periférica 0.5 CV, chave contatora e disjuntor, 2 boias de nível, filtro residencial autolimpante, ramal PVC 25 mm."
    },
    "UTG": {
        "name": "Casa Geminada (8 hab)",
        "pump_power_kw": 0.37,
        "pump_count": 1,
        "pump_unit_cost": 301.70,
        "pump_cost_total": 301.70,
        "electrical_panel_cost": 220.00,
        "sensors_automation_cost": 150.00,
        "treatment_filtration_cost": 400.00,
        "air_gap_supplement_cost": 180.00,
        "pipes_base_cost": 1100.00,
        "maint_base_annual": 300.00,
        "min_labor_cost": 1550.00,
        "description": "Bomba 0.5 CV, quadro compacto, 2 boias elétricas, filtro autolimpante, tubulação recalque DN 32 mm."
    },
    "MSG": {
        "name": "Sobrado Multifamiliar Geminado (16 hab, 2 pavimentos)",
        "pump_power_kw": 0.55,
        "pump_count": 1,
        "pump_unit_cost": 450.00,
        "pump_cost_total": 450.00,
        "electrical_panel_cost": 380.00,
        "sensors_automation_cost": 240.00,
        "treatment_filtration_cost": 550.00,
        "air_gap_supplement_cost": 230.00,
        "pipes_base_cost": 1600.00,
        "maint_base_annual": 450.00,
        "min_labor_cost": 1900.00,
        "description": "Bomba centrífuga 0.75 CV, quadro com relé térmico, 3 sensores de nível, dosador de pastilhas de cloro, prumada vertical 2 pavimentos DN 32/40 mm."
    },
    "MFH": {
        "name": "Bloco Multifamiliar H (64 hab, 16 aptos, 4 pavimentos)",
        "pump_power_kw": 0.75,
        "pump_count": 2,
        "pump_unit_cost": 600.00,
        "pump_cost_total": 1200.00,
        "electrical_panel_cost": 950.00,
        "sensors_automation_cost": 550.00,
        "treatment_filtration_cost": 1200.00,
        "air_gap_supplement_cost": 450.00,
        "pipes_base_cost": 3800.00,
        "maint_base_annual": 950.00,
        "min_labor_cost": 3200.00,
        "description": "Sistema de recalque duplo 1+1 (2x 1.0 CV), quadro com alternador automático de bombas e falta de fase, 4 sensores de nível, filtro vortex inox alta vazão, barrilete DN 50 mm, 2 a 4 prumadas de reuso em shaft."
    },
    "MFL": {
        "name": "Bloco Multifamiliar Retangular L (128 hab, 32-48 aptos, 4-8 pavimentos)",
        "pump_power_kw": 1.50,
        "pump_count": 2,
        "pump_unit_cost": 1200.00,
        "pump_cost_total": 2400.00,
        "electrical_panel_cost": 1600.00,
        "sensors_automation_cost": 900.00,
        "treatment_filtration_cost": 2100.00,
        "air_gap_supplement_cost": 750.00,
        "pipes_base_cost": 6500.00,
        "maint_base_annual": 1600.00,
        "min_labor_cost": 4800.00,
        "description": "Sistema de pressurização/recalque duplo 1+1 multiestágio (2x 2.0 CV), painel de comando predial automatizado com alternador e alarme, automação multinível com solenoide para reposição potável via air gap NBR 5626, estação de filtragem dupla inox, barrilete DN 60/75 mm, 4 a 8 prumadas verticais dedicadas em shafts para todos os blocos."
    }
}


def load_costs_database() -> Dict[str, Any]:
    """Carrega os dados de custo do arquivo JSON com fallback seguro."""
    if COSTS_FILE_PATH.is_file():
        try:
            with open(COSTS_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            pass
    return {
        "regional_factors_by_uf": _DEFAULT_REGIONAL_FACTORS,
        "lower_tank_pead_prices": _DEFAULT_LOWER_TANK_PRICES,
        "upper_tank_pead_prices": _DEFAULT_UPPER_TANK_PRICES,
        "material_multipliers": _DEFAULT_MATERIAL_MULTIPLIERS,
        "pipes_cost_per_meter": _DEFAULT_PIPE_COST_PER_METER,
        "chlorine_cost_per_kg": _DEFAULT_CHLORINE_COST_PER_KG,
        "pump_cost_parameters": {
            "base_cost": 300.0, "base_power_kw": 0.36775, "power_exponent": 0.70, "min_cost": 280.0
        },
        "labor_percentage": 0.30,
        "accessories_percentage": 0.08,
        "piping_percentage_fallback": 0.18,
        "typology_subsystems_configs": _DEFAULT_TYPOLOGY_CONFIGS,
    }


def verba_generica_de_tratamento_brl(typology: str = "UTI") -> float:
    """Verba de filtracao e tratamento ja embutida em «Acessorios».

    O estimador consolida painel, sensores, tratamento e desconexao em um unico
    campo de acessorios. Quando a ETAP e dimensionada, ela substitui a parcela de
    tratamento desse pacote, e so a diferenca e investimento novo. Sem este
    desconto o filtro apareceria duas vezes no CAPEX.

    Lê a cópia em memória do banco de custos (refeita a cada gravação), e não o
    arquivo: é chamada a cada linha econômica, centenas de vezes por varredura.
    """
    cfgs = TYPOLOGY_COST_CONFIGS or _DEFAULT_TYPOLOGY_CONFIGS
    cfg = cfgs.get(str(typology).upper(), cfgs.get("UTI", {}))
    try:
        return max(0.0, float(cfg.get("treatment_filtration_cost", 350.0)))
    except (TypeError, ValueError):
        return 350.0


def save_costs_database(data: Dict[str, Any]) -> bool:
    """Salva dados customizados no arquivo JSON de custos."""
    try:
        COSTS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(COSTS_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        _refresh_runtime_constants()
        return True
    except Exception:
        return False


def _refresh_runtime_constants():
    global LOWER_TANK_PRICE_TABLE, UPPER_TANK_PRICE_TABLE, MATERIAL_COST_MULTIPLIERS
    global PIPE_COST_PER_METER, DEFAULT_CHLORINE_COST_PER_KG, PUMP_PARAMS, LABOR_PCT, ACCESSORIES_PCT, PIPING_PCT
    global REGIONAL_FACTORS_BY_UF, TYPOLOGY_COST_CONFIGS
    
    db = load_costs_database()
    
    raw_reg = db.get("regional_factors_by_uf", _DEFAULT_REGIONAL_FACTORS)
    REGIONAL_FACTORS_BY_UF = {str(k).upper(): float(v) for k, v in raw_reg.items()}
    
    raw_typo = db.get("typology_subsystems_configs", _DEFAULT_TYPOLOGY_CONFIGS)
    TYPOLOGY_COST_CONFIGS = raw_typo
    
    raw_lower = db.get("lower_tank_pead_prices", _DEFAULT_LOWER_TANK_PRICES)
    LOWER_TANK_PRICE_TABLE = [(float(r[0]), float(r[1])) for r in raw_lower]
    
    raw_upper = db.get("upper_tank_pead_prices", _DEFAULT_UPPER_TANK_PRICES)
    UPPER_TANK_PRICE_TABLE = [(float(r[0]), float(r[1])) for r in raw_upper]
    
    raw_mats = db.get("material_multipliers", _DEFAULT_MATERIAL_MULTIPLIERS)
    MATERIAL_COST_MULTIPLIERS = {str(k): float(v) for k, v in raw_mats.items()}
    
    raw_pipes = db.get("pipes_cost_per_meter", _DEFAULT_PIPE_COST_PER_METER)
    PIPE_COST_PER_METER = {int(k): float(v) for k, v in raw_pipes.items()}
    
    DEFAULT_CHLORINE_COST_PER_KG = float(db.get("chlorine_cost_per_kg", _DEFAULT_CHLORINE_COST_PER_KG))
    PUMP_PARAMS = db.get("pump_cost_parameters", {"base_cost": 300.0, "base_power_kw": 0.36775, "power_exponent": 0.70, "min_cost": 280.0})
    LABOR_PCT = float(db.get("labor_percentage", 0.30))
    ACCESSORIES_PCT = float(db.get("accessories_percentage", 0.08))
    PIPING_PCT = float(db.get("piping_percentage_fallback", 0.18))


# Inicializa as constantes na importação
_refresh_runtime_constants()


#: Piso da mão de obra estimada (R$), o mesmo do estimador preliminar.
MAO_DE_OBRA_MINIMA = 1400.0


def mao_de_obra_estimada(materiais_brl: float) -> float:
    """Mão de obra de instalação: ``labor_percentage`` dos materiais, com piso."""
    return max(MAO_DE_OBRA_MINIMA, LABOR_PCT * max(0.0, float(materiais_brl)))


def interpolate_price(table: List[Tuple[float, float]], volume_l: float) -> float:
    """Interpolação linear contínua e monótona para qualquer capacidade de reservatório (litros).
    
    Suporta volumes fracionários, pequenos (ex: 450 L, 100 L) ou volumes industriais elevados (>50.000 L).
    """
    v = max(0.0, float(volume_l))
    if v <= 0.0:
        return 0.0
    if not table:
        return 0.0
    sorted_table = sorted(table, key=lambda x: float(x[0]))
    if sorted_table[0][0] > 0.0:
        sorted_table = [(0.0, 0.0)] + sorted_table
    vols = [float(p[0]) for p in sorted_table]
    prices = [float(p[1]) for p in sorted_table]
    
    if v <= vols[-1]:
        return float(np.interp(v, vols, prices))

    # Fora da tabela nao ha ponto observado. A inclinacao dos DOIS ULTIMOS
    # pontos, que era o criterio anterior, e o par mais sensivel a ruido de
    # varejo de toda a serie: uma promocao no maior volume tabelado girava a
    # reta inteira. A regressao ajustada sobre o banco INTEIRO e a referencia
    # estavel, e e o que `regressao_linear_da_tabela` devolve.
    return _extrapolar_pela_regressao(sorted_table, v)


def regressao_linear_da_tabela(table: List[Tuple[float, float]]) -> Dict[str, float]:
    """Ajusta Preco = a x Volume + b sobre uma tabela de precos.

    Devolve inclinacao, intercepto e R2. E a forma generica de
    `get_tank_linear_regression`, que a chama para as tabelas de reservatorio
    inferior e superior com o multiplicador de material aplicado.
    """
    pontos = sorted((float(v), float(p)) for v, p in table if float(v) > 0)
    if len(pontos) < 2:
        return {"slope_r_per_l": 0.0, "intercept_r": 0.0, "r_squared": 0.0}

    vols = np.array([v for v, _ in pontos])
    precos = np.array([p for _, p in pontos])
    slope, intercept = np.polyfit(vols, precos, 1)
    previsto = slope * vols + intercept
    ss_res = float(np.sum((precos - previsto) ** 2))
    ss_tot = float(np.sum((precos - np.mean(precos)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 1.0
    return {
        "slope_r_per_l": float(slope),
        "intercept_r": float(intercept),
        "r_squared": float(r2),
    }


#: R2 minimo para que a regressao seja usada na extrapolacao. Abaixo disso a reta
#: nao descreve a tabela, e a inclinacao local dos ultimos pontos e menos ruim.
R2_MINIMO_PARA_EXTRAPOLAR = 0.90


def _extrapolar_pela_regressao(sorted_table: List[Tuple[float, float]], volume_l: float) -> float:
    """Preco acima do maior volume tabelado."""
    vols = [float(v) for v, _ in sorted_table]
    precos = [float(p) for _, p in sorted_table]
    reg = regressao_linear_da_tabela(sorted_table)

    if reg["r_squared"] >= R2_MINIMO_PARA_EXTRAPOLAR and reg["slope_r_per_l"] > 0:
        estimado = reg["slope_r_per_l"] * volume_l + reg["intercept_r"]
    else:
        # A reta nao descreve a tabela: volta-se a inclinacao dos ultimos pontos.
        v1, p1 = vols[-2], precos[-2]
        v2, p2 = vols[-1], precos[-1]
        inclinacao_local = (p2 - p1) / max(1.0, v2 - v1)
        estimado = p2 + inclinacao_local * (volume_l - v2)

    # Reservatorio maior nao custa menos que o maior tabelado.
    return float(max(estimado, precos[-1]))


def get_tank_linear_regression(material_key: str = "PEAD", is_upper: bool = False) -> Dict[str, float]:
    """Coeficientes de Preco = a x Volume + b para o material, sobre o banco de custos.

    E a referencia linear que `interpolate_price` usa para extrapolar acima do
    maior volume tabelado, e o R2 diz se ela pode ser usada. Dentro da tabela
    vale a interpolacao ponto a ponto, porque cada ponto e um preco observado.
    """
    table = UPPER_TANK_PRICE_TABLE if is_upper else LOWER_TANK_PRICE_TABLE
    mult = MATERIAL_COST_MULTIPLIERS.get(material_key, 1.0)
    reg = regressao_linear_da_tabela([(float(v), float(pr) * mult) for v, pr in table])
    return {
        **reg,
        "material": material_key,
        "is_upper": is_upper,
        "n_pontos": len(table),
        "volume_maximo_tabelado_l": max((float(v) for v, _ in table), default=0.0),
    }


def estimate_tank_price(
    volume_l: float,
    material_key: str = "PEAD",
    price_table: Optional[List[Tuple[float, float]]] = None,
) -> float:
    """Interpola linearmente o cenário de preços e aplica o multiplicador de material."""
    v = max(0.0, float(volume_l))
    table = price_table or LOWER_TANK_PRICE_TABLE
    base_price = interpolate_price(table, v)
    mult = MATERIAL_COST_MULTIPLIERS.get(material_key, 1.0)
    return base_price * mult


def estimate_tank_price_linear(volume_l: float, material_key: str = "PEAD") -> float:
    """Compatibilidade de API: usa a interpolação linear contínua."""
    return estimate_tank_price(volume_l, material_key, LOWER_TANK_PRICE_TABLE)


def compute_pipe_item_cost(diameter_mm: int, length_m: float, include_fittings: bool = True) -> float:
    """Calcula o custo de tubulação para um diâmetro nominal e comprimento com base nas referências SINAPI."""
    unit = PIPE_COST_PER_METER.get(int(diameter_mm), 35.0)
    base = max(0.0, float(length_m)) * unit
    return round(base * (1.25 if include_fittings else 1.0), 2)


def estimate_pipe_network_cost(pipes: Optional[List[Any]] = None) -> float:
    """Calcula o custo total da rede de tubulações a partir dos diâmetros e extensões informados (SINAPI + 25% conexões)."""
    if pipes is None:
        return 950.0
    total = 0.0
    has_any = False
    for p in pipes:
        if isinstance(p, (list, tuple)) and len(p) >= 2:
            dn = int(p[0])
            length = float(p[1])
        elif isinstance(p, dict):
            dn = int(p.get("diameter_mm", 100))
            length = float(p.get("length_m", 0.0))
        else:
            dn = int(getattr(p, "diameter_mm", 100))
            length = float(getattr(p, "length_m", 0.0))
        unit_cost = PIPE_COST_PER_METER.get(dn, 35.0)
        total += max(0.0, length) * unit_cost
        if length > 0:
            has_any = True
    if not has_any:
        return 0.0
    # Conexões, curvas e registros adicionam ~25% ao custo dos tubos lineares
    return round(total * 1.25, 2)


def estimate_annual_chlorination_cost(
    annual_pluvial_m3: float,
    dose_mg_l: float = DOSE_PADRAO_MG_POR_LITRO,
    cost_per_kg: float = DEFAULT_CHLORINE_COST_PER_KG,
    purity: float = PUREZA_PADRAO,
) -> Tuple[float, float]:
    """Massa anual de produto e custo correspondente.

    A massa devolvida e de **produto comercial**, ja corrigida pela pureza, que
    e o que se compra e sobre o que incide o preco em R$/kg.

    Esta funcao ja calculou a massa de cloro ATIVO e a
    multiplicava pelo preco do produto, subestimando o custo em 1/pureza -
    cerca de 35%. Era a quarta convencao de cloro do programa, e alimentava a
    interface enquanto o modulo economico ja usava a corrigida, de modo que os
    dois exibiam custos diferentes para a mesma cloracao.
    """
    cloracao = Cloracao(
        dose_mg_por_litro=max(0.0, dose_mg_l),
        pureza=max(1e-6, purity),
    )
    annual_product_kg = cloracao.massa_anual_de_produto_kg(max(0.0, annual_pluvial_m3))
    annual_cost = annual_product_kg * max(0.0, cost_per_kg)
    return annual_product_kg, annual_cost


def annualize_operational_costs(
    items: Optional[List[Any]],
    annual_pluvial_m3: float = 0.0,
) -> float:
    """Converte custos periódicos em equivalente do primeiro ano."""
    total = 0.0
    monthly_pluvial_m3 = max(0.0, float(annual_pluvial_m3)) / 12.0
    for item in items or []:
        if len(item) < 4:
            continue
        _, period_months, fixed_cost, variable_cost_per_m3 = item
        occurrences_per_year = 12.0 / max(1.0, float(period_months))
        cost_per_occurrence = max(0.0, float(fixed_cost)) + max(0.0, float(variable_cost_per_m3)) * monthly_pluvial_m3
        total += occurrences_per_year * cost_per_occurrence
    return total


def estimate_calibrated_capex_opex(
    typology: str = "UTI",
    volume_l: float = 5000.0,
    uf: str = "SP",
    energy_tariff_kwh: float = 0.841,
    lower_material: str = "PEAD",
    upper_material: str = "PEAD",
    detailed_breakdown: bool = True
) -> Dict[str, Any]:
    """Calcula o CAPEX detalhado e OPEX parametrizado para as 5 tipologias e 27 UFs.
    
    Modelagem de 8 subsistemas de engenharia:
    1. Reservatório Inferior PEAD (interpolado continuamente)
    2. Reservatório Superior de Reuso PEAD (10% do inferior, mín 200 L)
    3. Conjunto Motobomba de Recalque (simples para UTI/UTG/MSG; duplo 1+1 para MFH/MFL)
    4. Painel Elétrico e Quadro de Comando Automatizado (com relés, proteção e alternador)
    5. Sensores de Nível e Automação (proteção a seco, nível máximo e solenoide)
    6. Filtragem, Freio d'Água de Fundo, Sifão Ladrão e Ruptura Atmosférica Air Gap (NBR 5626 / 15527)
    7. Tubulações Prediais e Prumadas Verticais Dedicadas de Reuso em Shafts
    8. Mão de Obra Especializada de Instalação Civil, Elétrica e Hidráulica (30% sobre materiais com piso mínimo)
    
    Aplica o Fator Regional SINAPI/CUB por UF sobre o total do CAPEX e sobre a manutenção periódica.
    """
    typ_code = str(typology).strip().upper()
    if typ_code not in TYPOLOGY_COST_CONFIGS:
        typ_code = "UTI"
    cfg = TYPOLOGY_COST_CONFIGS[typ_code]
    
    uf_clean = str(uf).strip().upper()
    f_reg = REGIONAL_FACTORS_BY_UF.get(uf_clean, 1.00)
    
    # 1. Reservatório Inferior e Superior
    v_inf = max(0.0, float(volume_l))
    c_inf = estimate_tank_price(v_inf, lower_material, LOWER_TANK_PRICE_TABLE)
    
    v_sup = max(200.0, v_inf * 0.10) if v_inf > 0 else 0.0
    c_sup = estimate_tank_price(v_sup, upper_material, UPPER_TANK_PRICE_TABLE) if v_inf > 0 else 0.0
    
    # 2. Subsistemas Eletromecânicos e Hidráulicos por Tipologia
    c_pump = float(cfg.get("pump_cost_total", 301.70))
    c_panel = float(cfg.get("electrical_panel_cost", 180.00))
    c_sensors = float(cfg.get("sensors_automation_cost", 120.00))
    c_treatment = float(cfg.get("treatment_filtration_cost", 350.00))
    c_air_gap = float(cfg.get("air_gap_supplement_cost", 150.00))
    c_pipes_base = float(cfg.get("pipes_base_cost", 950.00))
    
    # Tubulações com componente de escala para volumes industriais elevados
    c_pipes = max(c_pipes_base, c_pipes_base + 0.05 * c_inf)
    
    # Acessórios e complementos consolidados
    c_accessories_total = c_panel + c_sensors + c_treatment + c_air_gap
    
    # 3. Mão de Obra de Instalação Civil, Elétrica e Hidráulica
    mat_sum = c_inf + c_sup + c_pump + c_pipes + c_accessories_total
    min_labor = float(cfg.get("min_labor_cost", 1400.00))
    labor_cost = max(min_labor, LABOR_PCT * mat_sum)
    
    # 4. CAPEX Total Base e Regionalizado
    capex_base = mat_sum + labor_cost
    capex_regional = capex_base * f_reg
    
    # 5. OPEX Parametrizado
    # Consumo específico de recalque = 0.45 kWh/m³
    opex_energy_per_m3 = 0.45 * max(0.0, float(energy_tariff_kwh))
    # Cloração = 2.0 mg/L x R$ 25,00/kg = R$ 0,05/m³
    opex_chlorine_per_m3 = 0.05
    opex_variable_per_m3 = opex_energy_per_m3 + opex_chlorine_per_m3
    
    maint_base = float(cfg.get("maint_base_annual", 250.00))
    opex_fixed_annual = maint_base * f_reg
    
    res = {
        "typology": typ_code,
        "typology_name": cfg.get("name", typ_code),
        "volume_l": v_inf,
        "volume_sup_l": v_sup,
        "uf": uf_clean,
        "f_regional": f_reg,
        "c_inf": round(c_inf, 2),
        "c_sup": round(c_sup, 2),
        "c_pump": round(c_pump, 2),
        "c_pipes": round(c_pipes, 2),
        "c_panel": round(c_panel, 2),
        "c_sensors": round(c_sensors, 2),
        "c_treatment": round(c_treatment, 2),
        "c_air_gap": round(c_air_gap, 2),
        "c_accessories_total": round(c_accessories_total, 2),
        "labor_cost": round(labor_cost, 2),
        "capex_base_brl": round(capex_base, 2),
        "capex_total_brl": round(capex_regional, 2),
        "opex_fixed_annual_brl": round(opex_fixed_annual, 2),
        "opex_energy_per_m3_brl": round(opex_energy_per_m3, 4),
        "opex_chlorine_per_m3_brl": round(opex_chlorine_per_m3, 4),
        "opex_variable_per_m3_brl": round(opex_variable_per_m3, 4),
    }
    
    if not detailed_breakdown:
        return {
            "typology": typ_code,
            "volume_l": v_inf,
            "uf": uf_clean,
            "f_regional": f_reg,
            "capex_total_brl": round(capex_regional, 2),
            "opex_fixed_annual_brl": round(opex_fixed_annual, 2),
            "opex_variable_per_m3_brl": round(opex_variable_per_m3, 4),
        }
        
    return res


def precos_de_catalogo(cfg: Any) -> bool:
    """Os preços de catálogo (em reais) valem para o projeto? Fora da Brasil, não."""
    return bool(getattr(cfg, "precos_de_catalogo", True))


def preco_da_cisterna_do_volume(cfg: Any, volume_l: float) -> float:
    """Preço da cisterna inferior de um volume, a regra única da interface e da CLI.

    Com o catálogo (Edição Brasil), a interpolação da tabela pelo volume e pelo material;
    sem ele (``precos_de_catalogo`` falso), o custo que o projeto informa. Antes, sem o
    catálogo a cisterna entrava a custo zero mesmo com o preço digitado na etapa 5.
    """
    if volume_l <= 0:
        return 0.0
    if not precos_de_catalogo(cfg):
        return float(getattr(cfg, "cost_lower_tank", 0.0) or 0.0)
    return float(estimate_preliminary_capex(
        volume_l, getattr(cfg, "upper_tank_vol", 500.0), bool(getattr(cfg, "upper_tank_used", 1)),
        getattr(cfg, "pump_power_kw", 0.37), getattr(cfg, "pump_count", 1),
        lower_material=getattr(cfg, "lower_tank_material", "PEAD"),
        upper_material=getattr(cfg, "upper_tank_material", "PEAD"),
    )["lower"])


def estimate_preliminary_capex(
    lower_volume_l: float,
    upper_volume_l: float,
    upper_used: bool,
    pump_power_kw: float = 0.37,
    pump_count: int = 1,
    lower_material: str = "PEAD",
    upper_material: str = "PEAD",
    pipes: Optional[List[Any]] = None,
    typology: Optional[str] = None,
    uf: Optional[str] = None,
    catalogo: bool = True,
) -> dict:
    """Estima o CAPEX preliminar com base na interpolação linear dos reservatórios e componentes.

    ``catalogo=False`` (projeto fora da Brasil, ``precos_de_catalogo`` do projeto): os preços
    são de catálogo brasileiro, em reais, e não valem; tudo sai zero, e o custo é o informado.
    
    Mantém total retrocompatibilidade com chamadas existentes do Triton e permite
    especificação de tipologia e UF para aplicação dos custos calibrados de engenharia.
    """
    if lower_volume_l <= 0 or not catalogo:
        return {
            "lower": 0.0, "upper": 0.0, "pump_unit": 0.0, "pump": 0.0,
            "piping": 0.0, "accessories": 0.0, "labor": 0.0,
            "lower_material": lower_material, "upper_material": upper_material,
            "total": 0.0,
        }

    if typology:
        calib = estimate_calibrated_capex_opex(
            typology=typology,
            volume_l=lower_volume_l,
            uf=uf or "SP",
            lower_material=lower_material,
            upper_material=upper_material,
            detailed_breakdown=True
        )
        return {
            "lower": calib["c_inf"],
            "upper": calib["c_sup"],
            "pump_unit": calib["c_pump"] / max(1, pump_count),
            "pump": calib["c_pump"],
            "piping": calib["c_pipes"],
            "accessories": calib["c_accessories_total"],
            "labor": calib["labor_cost"],
            "lower_material": lower_material,
            "upper_material": upper_material,
            "f_regional": calib["f_regional"],
            "total": calib["capex_total_brl"]
        }

    lower = estimate_tank_price(max(0.0, lower_volume_l), lower_material, LOWER_TANK_PRICE_TABLE)
    upper = estimate_tank_price(max(0.0, upper_volume_l), upper_material, UPPER_TANK_PRICE_TABLE) if upper_used else 0.0
    
    base_pump = PUMP_PARAMS.get("base_cost", 300.0)
    base_kw = PUMP_PARAMS.get("base_power_kw", 0.36775)
    exp_p = PUMP_PARAMS.get("power_exponent", 0.70)
    min_p = PUMP_PARAMS.get("min_cost", 280.0)
    
    pump_unit = max(min_p, base_pump * (max(0.1, pump_power_kw) / base_kw) ** exp_p) if upper_used else 0.0
    pump = pump_unit * max(1, pump_count) if upper_used else 0.0
    
    if pipes:
        piping = estimate_pipe_network_cost(pipes)
    else:
        piping = max(950.0, PIPING_PCT * lower + 0.25 * upper)
        
    accessories = max(500.0, 150.0 + ACCESSORIES_PCT * (lower + upper))
    labor = mao_de_obra_estimada(lower + upper + pump + piping + accessories)
    
    f_reg = REGIONAL_FACTORS_BY_UF.get(str(uf).upper(), 1.00) if uf else 1.00
    total_base = lower + upper + pump + piping + accessories + labor
    total = total_base * f_reg
    
    return {
        "lower": lower,
        "upper": upper,
        "pump_unit": pump_unit,
        "pump": pump,
        "piping": piping,
        "accessories": accessories,
        "labor": labor,
        "lower_material": lower_material,
        "upper_material": upper_material,
        "f_regional": f_reg,
        "total": total
    }


def default_maintenance_items(upper_used: bool = True) -> list:
    """Rotinas anuais de referência carregadas a partir da base de custos."""
    db = load_costs_database()
    raw_items = db.get("default_maintenance_items", [])
    if raw_items:
        items = []
        for it in raw_items:
            req_up = it.get("requires_upper_tank", False)
            if req_up and not upper_used:
                continue
            items.append((it["name"], it["period_months"], it["fixed_cost"], it["variable_cost_per_m3"]))
        return items
    
    items = [
        ("Inspeção e limpeza de calhas/pré-filtro", 12, 240.0, 0.0),
        ("Limpeza e higienização do reservatório", 12, 320.0, 0.0),
    ]
    if upper_used:
        items.append(("Manutenção preventiva da motobomba", 12, 180.0, 0.0))
    return items
