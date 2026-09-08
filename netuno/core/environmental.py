"""
Módulo Core de Análise do Ciclo de Vida (ACV/LCA de triagem).
Permite modelar, com inventário explícito e editável, a pegada de carbono de:
- Cisternas e Reservatórios Superiores por material, densidade de massa e emissão específica.
- Redes de Tubulações por Diâmetro Nominal (DN 50, 75, 100, 150 mm).
- Equipamentos de Bombeamento por potência (CV), tipo e consumo elétrico operacional.
- Dosagem de insumos de tratamento químico de água e emissão evitada da rede pública.

Os valores padrão são cenários internos e não foram verificados como fatores
normativos. Para uso científico definitivo, substitua-os por quantitativos do
projeto, EPDs ou inventários versionados compatíveis com a fronteira do estudo.
"""

from dataclasses import dataclass, field, replace
from typing import Dict, List, Any, Optional, Tuple


@dataclass
class MaterialPreset:
    name: str
    material_density_kg_per_m3_tank: float  # Consumo de material por m³ de reservatório (kg material / m³ útil)
    co2_factor_kg_per_kg: float             # Emissão específica do material (kg CO2e / kg material)
    co2_factor_kg_per_m3_tank: float        # Emissão consolidada por m³ de reservatório (kg CO2e / m³ útil)
    source_reference: str                    # Fonte bibliográfica / Inventário de ACV
    description: str


# Cenários genéricos de triagem. Os fatores não substituem uma EPD, inventário
# regional ou quantitativo geométrico do fabricante. As referências indicam as
# famílias de bases usadas na concepção; o valor adotado permanece editável.
MATERIAL_PRESETS: Dict[str, MaterialPreset] = {
    "PEAD": MaterialPreset(
        name="Polietileno de Alta Densidade (PEAD)",
        material_density_kg_per_m3_tank=22.0,  # ~22 kg PEAD por m³ útil
        co2_factor_kg_per_kg=3.00,             # 3,0 kg CO2e / kg PEAD
        co2_factor_kg_per_m3_tank=66.0,        # 22 * 3.0 = 66 kg CO2e / m³ útil
        source_reference="Cenário de triagem; calibrar com EPD/inventário do fornecedor (famílias ICE/Ecoinvent)",
        description="Reservatório plástico rotomoldado pré-fabricado. Leve e de fácil instalação."
    ),
    "CONCRETO": MaterialPreset(
        name="Concreto Armado Moldado in loco",
        material_density_kg_per_m3_tank=1200.0, # ~0.5 m³ concreto armado (~1200 kg) por m³ útil
        co2_factor_kg_per_kg=0.14,              # 0.14 kg CO2e / kg concreto (Cimento CP-II + Armadura)
        co2_factor_kg_per_m3_tank=168.0,        # 1200 * 0.14 = 168 kg CO2e / m³ útil
        source_reference="Cenário de triagem geométrico; calibrar estrutura e EPD do concreto/aço",
        description="Estrutura de concreto armado de alta durabilidade (50+ anos) e maior pegada inicial."
    ),
    "FIBRA": MaterialPreset(
        name="Poliéster Reforçado com Fibra de Vidro (PRFV)",
        material_density_kg_per_m3_tank=20.0,  # ~20 kg PRFV por m³ útil
        co2_factor_kg_per_kg=4.25,             # 4.25 kg CO2e / kg PRFV
        co2_factor_kg_per_m3_tank=85.0,        # 20 * 4.25 = 85 kg CO2e / m³ útil
        source_reference="Cenário de triagem; calibrar massa e EPD do reservatório PRFV",
        description="Reservatório composto leve, altamente anticorrosivo e de médio gasto energético."
    ),
    "ACO_INOX": MaterialPreset(
        name="Aço Inoxidável (AISI 304/316)",
        material_density_kg_per_m3_tank=38.0,  # ~38 kg Aço Inox por m³ útil
        co2_factor_kg_per_kg=2.89,             # 2.89 kg CO2e / kg Aço Inox
        co2_factor_kg_per_m3_tank=109.8,       # 38 * 2.89 = 109,8 kg CO2e / m³ útil
        source_reference="Cenário de triagem; calibrar massa, teor reciclado e EPD do aço inox",
        description="Reservatório industrial metálico de altíssima longevidade e 100% reciclável."
    )
}

# Emissões lineares de tubulações de PVC rígido por diâmetro nominal (DN).
# Cenário interno de triagem: calibrar massa linear e EPD/inventário do tubo.
PIPE_EMISSION_FACTORS_PER_METER: Dict[int, float] = {
    20:  0.50,   # DN 20 mm (1/2"): ~0.18 kg PVC/m * 2.80 kg CO2e/kg = 0.50 kg CO2e/m
    25:  0.67,   # DN 25 mm (3/4"): ~0.24 kg PVC/m * 2.80 kg CO2e/kg = 0.67 kg CO2e/m
    32:  0.95,   # DN 32 mm (1"): ~0.34 kg PVC/m * 2.80 kg CO2e/kg = 0.95 kg CO2e/m
    40:  1.23,   # DN 40 mm (1 1/4"): ~0.44 kg PVC/m * 2.80 kg CO2e/kg = 1.23 kg CO2e/m
    50:  1.54,   # DN 50 mm (1 1/2"): ~0.55 kg PVC/m * 2.80 kg CO2e/kg = 1.54 kg CO2e/m
    60:  1.96,   # DN 60 mm (2"): ~0.70 kg PVC/m * 2.80 kg CO2e/kg = 1.96 kg CO2e/m
    75:  2.66,   # DN 75 mm (2 1/2"): ~0.95 kg PVC/m * 2.80 kg CO2e/kg = 2.66 kg CO2e/m
    85:  3.22,   # DN 85 mm (3"): ~1.15 kg PVC/m * 2.80 kg CO2e/kg = 3.22 kg CO2e/m
    100: 3.92,   # DN 100 mm (4"): ~1.40 kg PVC/m * 2.80 kg CO2e/kg = 3.92 kg CO2e/m
    110: 4.48,   # DN 110 mm (4"): ~1.60 kg PVC/m * 2.80 kg CO2e/kg = 4.48 kg CO2e/m
    150: 7.84,   # DN 150 mm (6"): ~2.80 kg PVC/m * 2.80 kg CO2e/kg = 7.84 kg CO2e/m
}

# Emissão incorporada de motobomba por potência (CV).
# Cenário interno de triagem: substituir por massa/BOM/EPD do equipamento.
PUMP_EMBEDDED_CO2: Dict[float, float] = {
    0.25: 12.0,  # 1/4 CV: ~12 kg CO2e
    0.50: 18.0,  # 1/2 CV: ~18 kg CO2e
    0.75: 24.0,  # 3/4 CV: ~24 kg CO2e
    1.00: 30.0,  # 1.0 CV: ~30 kg CO2e
    1.50: 42.0,  # 1.5 CV: ~42 kg CO2e
    2.00: 55.0,  # 2.0 CV: ~55 kg CO2e
}


MATERIAL_KEY_ALIASES: Dict[str, str] = {
    "PEAD": "PEAD",
    "HDPE": "PEAD",
    "CONCRETO": "CONCRETO",
    "CONCRETE": "CONCRETO",
    "FIBRA": "FIBRA",
    "PRFV": "FIBRA",
    "GRP": "FIBRA",
    "FRP": "FIBRA",
    "ACO_INOX": "ACO_INOX",
    "AÇO_INOX": "ACO_INOX",
    "INOX": "ACO_INOX",
}


def normalize_material_key(value: Any, default: str = "PEAD") -> str:
    """Normaliza aliases usados pelos módulos econômico e ambiental.

    Na v5.0.4, ``PRFV`` era aceito no custo mas caía silenciosamente no preset
    PEAD da ACV. A normalização explícita elimina essa divergência.
    """
    key = str(value or default).strip().upper()
    return MATERIAL_KEY_ALIASES.get(key, default)


@dataclass
class PipeInput:
    diameter_mm: int           # 50, 75, 100, 150 mm
    length_m: float            # Metros de tubulação
    custom_co2_per_m: Optional[float] = None  # Sobrescreve o fator linear em kg CO2e/m se fornecido


@dataclass
class PumpInput:
    power_cv: float = 0.50             # 0.25, 0.5, 0.75, 1.0, 1.5, 2.0 CV
    custom_embodied_co2: Optional[float] = None # kg CO2e de fabricação por unidade
    specific_kwh_per_m3: float = 0.40  # Consumo elétrico (kWh/m³)
    material: str = "Ferro Fundido, Cobre & Alumínio"


@dataclass
class EnvironmentalConfig:
    lower_tank_vol: float = 4000.0
    annual_water_saved_m3: float = 0.0
    annual_pump_kwh: float = 0.0
    pump_count: int = 1                          # 1 = Principal, 2 = Principal + Reserva/Backup
    pump_material: str = "Ferro Fundido, Cobre & Alumínio"
    material_key: Optional[str] = None

    # Cisterna Inferior
    lower_material_key: str = "PEAD"
    custom_lower_density_kg_m3: Optional[float] = None
    custom_lower_co2_per_kg: Optional[float] = None

    # Reservatório Superior (Caixa d'Água)
    upper_tank_used: bool = True
    upper_tank_vol_liters: float = 500.0
    upper_material_key: str = "PEAD"
    custom_upper_density_kg_m3: Optional[float] = None
    custom_upper_co2_per_kg: Optional[float] = None

    # Tubulações por Diâmetro Nominal (Sincronizadas com o projeto / CAPEX)
    pipes: List[PipeInput] = field(default_factory=lambda: [
        PipeInput(diameter_mm=100, length_m=20.0), # Tubo captação/extravasor
        PipeInput(diameter_mm=32, length_m=5.0),   # Tubo de sucção (5m)
        PipeInput(diameter_mm=25, length_m=20.0),  # Tubo de recalque (20m)
    ])

    # Motobomba
    pump: PumpInput = field(default_factory=PumpInput)

    # Operação, Tratamento Químico e Matriz Elétrica
    grid_co2_factor_kg_kwh: float = 0.085        # Hipótese editável; selecionar série MCTI/SIRENE do período
    potable_water_co2_kg_m3: float = 0.35        # Emissão evitada da água potável da rede (kg CO2e/m³)
    # Cloração: a massa anual é calculada a partir do volume pluvial
    # efetivamente utilizado.  A intensidade de CO2e resulta de dose × fator.
    chlorine_dose_mg_l: float = 2.0              # Dose de cloro equivalente (mg Cl2/L)
    chlorine_co2_kg_per_kg: float = 25.0         # Fator de emissão do insumo (kg CO2e/kg Cl2)
    # Campo legado. Projetos antigos podem informar diretamente kg CO2e/m³;
    # quando presente, ele preserva o resultado histórico de emissão.
    chemical_treatment_co2_m3: Optional[float] = None
    system_lifespan_years: float = 20.0          # Vida útil considerada (anos)

    def __post_init__(self):
        if self.material_key is not None:
            self.lower_material_key = self.material_key
        self.lower_material_key = normalize_material_key(self.lower_material_key, "PEAD")
        self.upper_material_key = normalize_material_key(self.upper_material_key, "PEAD")


@dataclass
class LCAItemBreakdown:
    category: str               # Nome do componente do ciclo de vida
    quantity_str: str           # Quantidade / Dimensão
    embodied_co2_kg: float      # CO2 de Fabricação (kg CO2e)
    annual_op_co2_kg: float     # CO2 Operacional Anual (kg CO2e / ano)
    lifetime_net_co2_kg: float  # CO2 Acumulado em N anos (kg CO2e)
    source_reference: str       # Fonte Bibliográfica / Inventário


@dataclass
class EnvironmentalResult:
    tank_vol_liters: float
    annual_pluvial_m3: float
    lower_tank_mass_kg: float            # Massa da cisterna (kg)
    upper_tank_mass_kg: float            # Massa da caixa d'água superior (kg)
    total_pipes_co2_kg: float            # CO2 total das tubulações (kg CO2e)
    pump_embodied_co2_kg: float          # CO2 de fabricação da bomba (kg CO2e)
    total_embodied_co2_kg: float         # CO2 inicial total (kg CO2e)
    annual_pumping_co2_kg: float         # CO2 anual de bombeamento (kg CO2e / ano)
    annual_treatment_co2_kg: float       # CO2 anual de dosagem química (kg CO2e / ano)
    annual_chlorine_kg: float             # Massa anual de cloro equivalente (kg Cl2 / ano)
    chlorine_dose_mg_l: float             # Dose adotada para o inventário (mg Cl2/L)
    chlorine_co2_kg_per_kg: float         # Fator adotado para o insumo (kg CO2e/kg Cl2)
    treatment_co2_kg_per_m3: float        # Intensidade efetiva do tratamento (kg CO2e/m³)
    annual_avoided_co2_kg: float         # CO2 anual evitado da rede pública (kg CO2e / ano)
    net_annual_avoided_co2_kg: float     # Saldo líquido anual de CO2 evitado (kg CO2e / ano)
    lifetime_net_co2_saved_kg: float     # Economia líquida acumulada na vida útil (kg CO2e)
    environmental_payback_years: float   # Tempo de retorno ambiental (anos)
    specific_co2_avoided_g_per_liter: float # CO2 evitado por litro de chuva (g CO2e / L)
    is_environmentally_viable: bool
    inventory_items: List[LCAItemBreakdown] = field(default_factory=list)


def empty_environmental_result() -> EnvironmentalResult:
    """Resultado neutro usado enquanto a ACV ainda não foi configurada."""
    return EnvironmentalResult(
        tank_vol_liters=0.0,
        annual_pluvial_m3=0.0,
        lower_tank_mass_kg=0.0,
        upper_tank_mass_kg=0.0,
        total_pipes_co2_kg=0.0,
        pump_embodied_co2_kg=0.0,
        total_embodied_co2_kg=0.0,
        annual_pumping_co2_kg=0.0,
        annual_treatment_co2_kg=0.0,
        annual_chlorine_kg=0.0,
        chlorine_dose_mg_l=0.0,
        chlorine_co2_kg_per_kg=0.0,
        treatment_co2_kg_per_m3=0.0,
        annual_avoided_co2_kg=0.0,
        net_annual_avoided_co2_kg=0.0,
        lifetime_net_co2_saved_kg=0.0,
        environmental_payback_years=0.0,
        specific_co2_avoided_g_per_liter=0.0,
        is_environmentally_viable=False,
        inventory_items=[],
    )


def calculate_lca(
    tank_vol_liters: Any = 4000.0,
    annual_pluvial_m3: Any = 0.0,
    config: Optional[EnvironmentalConfig] = None
) -> EnvironmentalResult:
    """
    Executa o cálculo completo e granular da Análise do Ciclo de Vida (ACV Simplificada),
    computando cisternas, caixas superiores, tubulações por diâmetro, motobombas e dosagem química.
    """
    if isinstance(tank_vol_liters, EnvironmentalConfig):
        config = tank_vol_liters
        tank_vol_liters = getattr(config, 'lower_tank_vol', 4000.0)
        annual_pluvial_m3 = getattr(config, 'annual_water_saved_m3', 0.0)
    elif config is None:
        if isinstance(annual_pluvial_m3, EnvironmentalConfig):
            config = annual_pluvial_m3
            annual_pluvial_m3 = getattr(config, 'annual_water_saved_m3', 0.0)
        else:
            config = EnvironmentalConfig()

    tank_vol_liters = float(tank_vol_liters)
    annual_pluvial_m3 = float(annual_pluvial_m3)

    # V=0 é a referência "sem sistema" da varredura, portanto não recebe
    # impactos fixos de caixa superior, tubos ou bomba.
    if tank_vol_liters <= 0 and annual_pluvial_m3 <= 0:
        return empty_environmental_result()

    vol_m3 = tank_vol_liters / 1000.0
    items: List[LCAItemBreakdown] = []

    # 1. Cisterna Inferior
    preset_lower = MATERIAL_PRESETS.get(config.lower_material_key, MATERIAL_PRESETS["PEAD"])
    den_lower = config.custom_lower_density_kg_m3 if (config.custom_lower_density_kg_m3 and config.custom_lower_density_kg_m3 > 0) else preset_lower.material_density_kg_per_m3_tank
    co2_lower = config.custom_lower_co2_per_kg if (config.custom_lower_co2_per_kg and config.custom_lower_co2_per_kg > 0) else preset_lower.co2_factor_kg_per_kg

    lower_mass = vol_m3 * den_lower
    lower_embodied = lower_mass * co2_lower

    items.append(LCAItemBreakdown(
        category=f"Cisterna Inferior ({preset_lower.name.split()[0]})",
        quantity_str=f"{tank_vol_liters:,.0f} L ({lower_mass:.1f} kg)".replace(',', '.'),
        embodied_co2_kg=lower_embodied,
        annual_op_co2_kg=0.0,
        lifetime_net_co2_kg=lower_embodied,
        source_reference=preset_lower.source_reference
    ))

    # 2. Reservatório Superior (Caixa d'Água)
    upper_mass = 0.0
    upper_embodied = 0.0
    if config.upper_tank_used and config.upper_tank_vol_liters > 0:
        vol_up_m3 = config.upper_tank_vol_liters / 1000.0
        preset_upper = MATERIAL_PRESETS.get(config.upper_material_key, MATERIAL_PRESETS["PEAD"])
        den_upper = config.custom_upper_density_kg_m3 if (config.custom_upper_density_kg_m3 and config.custom_upper_density_kg_m3 > 0) else preset_upper.material_density_kg_per_m3_tank
        co2_upper = config.custom_upper_co2_per_kg if (config.custom_upper_co2_per_kg and config.custom_upper_co2_per_kg > 0) else preset_upper.co2_factor_kg_per_kg

        upper_mass = vol_up_m3 * den_upper
        upper_embodied = upper_mass * co2_upper

        items.append(LCAItemBreakdown(
            category=f"Caixa d'Água Superior ({preset_upper.name.split()[0]})",
            quantity_str=f"{config.upper_tank_vol_liters:,.0f} L ({upper_mass:.1f} kg)".replace(',', '.'),
            embodied_co2_kg=upper_embodied,
            annual_op_co2_kg=0.0,
            lifetime_net_co2_kg=upper_embodied,
            source_reference=preset_upper.source_reference
        ))

    # 3. Tubulações por Diâmetro Nominal (DN)
    total_pipes_embodied = 0.0
    for pipe in config.pipes:
        if pipe.length_m <= 0:
            continue
        dn = pipe.diameter_mm
        factor = pipe.custom_co2_per_m if (pipe.custom_co2_per_m and pipe.custom_co2_per_m > 0) else PIPE_EMISSION_FACTORS_PER_METER.get(dn, 3.92)
        pipe_co2 = pipe.length_m * factor
        total_pipes_embodied += pipe_co2

        items.append(LCAItemBreakdown(
            category=f"Tubulação PVC Rígido (DN {dn} mm)",
            quantity_str=f"{pipe.length_m:.1f} m ({factor:.2f} kg CO2/m)",
            embodied_co2_kg=pipe_co2,
            annual_op_co2_kg=0.0,
            lifetime_net_co2_kg=pipe_co2,
            source_reference="Cenário de triagem; substituir pela massa linear e EPD/inventário do tubo"
        ))

    # 4. Motobomba de Recalque (Fabricação e Reserva/Backup)
    pump = config.pump
    pump_count = getattr(config, 'pump_count', 1)
    pump_unit_emb = pump.custom_embodied_co2 if (pump.custom_embodied_co2 and pump.custom_embodied_co2 > 0) else PUMP_EMBEDDED_CO2.get(pump.power_cv, 18.0)
    pump_emb = pump_unit_emb * pump_count
    mat_desc = getattr(config, 'pump_material', getattr(pump, 'material', "Ferro Fundido, Cobre & Alumínio"))

    count_str = f"{pump_count} un. (1 Principal + 1 Reserva/Backup)" if pump_count > 1 else "1 un. (Principal)"
    items.append(LCAItemBreakdown(
        category=f"Motobomba de Recalque ({pump.power_cv:.2f} CV - {mat_desc})",
        quantity_str=f"{count_str} — {pump.power_cv:.2f} CV",
        embodied_co2_kg=pump_emb,
        annual_op_co2_kg=0.0,
        lifetime_net_co2_kg=pump_emb,
        source_reference="Cenário de triagem; substituir por EPD/inventário da motobomba"
    ))

    total_embodied = lower_embodied + upper_embodied + total_pipes_embodied + pump_emb

    # 5. Operação Anual (Bombeamento Elétrico — Sincronizado 100% com a simulação técnica)
    if config.annual_pump_kwh > 0:
        annual_pumping_kwh = config.annual_pump_kwh
    else:
        annual_pumping_kwh = annual_pluvial_m3 * pump.specific_kwh_per_m3

    annual_pumping_co2 = annual_pumping_kwh * config.grid_co2_factor_kg_kwh
    items.append(LCAItemBreakdown(
        category="Consumo Elétrico do Bombeamento",
        quantity_str=f"{annual_pumping_kwh:.1f} kWh/ano ({annual_pumping_kwh / max(1.0, annual_pluvial_m3):.2f} kWh/m³)",
        embodied_co2_kg=0.0,
        annual_op_co2_kg=annual_pumping_co2,
        lifetime_net_co2_kg=annual_pumping_co2 * config.system_lifespan_years,
        source_reference="Fator de rede editável; usar a série MCTI/SIRENE do período do estudo"
    ))

    # 6. Operação Anual (Tratamento Químico / Cloração no Reservatório Superior)
    if config.upper_tank_used:
        chlorine_dose_mg_l = max(0.0, float(config.chlorine_dose_mg_l))
        chlorine_co2_kg_per_kg = max(0.0, float(config.chlorine_co2_kg_per_kg))
        ref_saved_m3 = float(getattr(config, 'annual_water_saved_m3', 0.0))
        pluvial_cl2_base = ref_saved_m3 if ref_saved_m3 > 0 else annual_pluvial_m3
        annual_chlorine_kg = pluvial_cl2_base * chlorine_dose_mg_l / 1000.0
        calculated_treatment_factor = chlorine_dose_mg_l * chlorine_co2_kg_per_kg / 1000.0
        treatment_co2_factor = (
            max(0.0, float(config.chemical_treatment_co2_m3))
            if config.chemical_treatment_co2_m3 is not None
            else calculated_treatment_factor
        )
        annual_treatment_co2 = pluvial_cl2_base * treatment_co2_factor
    else:
        chlorine_dose_mg_l = 0.0
        chlorine_co2_kg_per_kg = 0.0
        annual_chlorine_kg = 0.0
        treatment_co2_factor = 0.0
        annual_treatment_co2 = 0.0

    if annual_treatment_co2 > 0:
        items.append(LCAItemBreakdown(
            category="Dosagem Química / Desinfecção (Caixa Superior)",
            quantity_str=(f"{pluvial_cl2_base:.1f} m³/ano; {annual_chlorine_kg:.3f} kg Cl2/ano "
                          f"({chlorine_dose_mg_l:.2f} mg/L; {treatment_co2_factor:.3f} kg CO2e/m³)"),
            embodied_co2_kg=0.0,
            annual_op_co2_kg=annual_treatment_co2,
            lifetime_net_co2_kg=annual_treatment_co2 * config.system_lifespan_years,
            source_reference="Dosagem no reservatório superior configurada pelo usuário"
        ))

    # 7. Operação Anual Evitada (Água Potável da Rede Pública)
    annual_avoided_co2 = annual_pluvial_m3 * config.potable_water_co2_kg_m3
    items.append(LCAItemBreakdown(
        category="Água Potável Evitada da Rede Pública",
        quantity_str=f"{annual_pluvial_m3:.1f} m³/ano ({config.potable_water_co2_kg_m3:.2f} kg CO2/m³)",
        embodied_co2_kg=0.0,
        annual_op_co2_kg=-annual_avoided_co2,  # Evitada (crédito)
        lifetime_net_co2_kg=-(annual_avoided_co2 * config.system_lifespan_years),
        source_reference="Fator de água potável editável; substituir pelo inventário da concessionária"
    ))

    # Balanços Líquidos Consolidados
    net_annual_avoided_co2 = annual_avoided_co2 - annual_pumping_co2 - annual_treatment_co2
    lifetime_net_co2_saved = (net_annual_avoided_co2 * config.system_lifespan_years) - total_embodied

    if net_annual_avoided_co2 > 0:
        env_payback = total_embodied / net_annual_avoided_co2
    else:
        env_payback = 999.0

    total_lifetime_liters = (annual_pluvial_m3 * 1000.0) * config.system_lifespan_years
    if total_lifetime_liters > 0:
        specific_co2_avoided_g_l = (lifetime_net_co2_saved * 1000.0) / total_lifetime_liters
    else:
        specific_co2_avoided_g_l = 0.0

    is_viable = net_annual_avoided_co2 > 0 and env_payback <= config.system_lifespan_years

    return EnvironmentalResult(
        tank_vol_liters=tank_vol_liters,
        annual_pluvial_m3=annual_pluvial_m3,
        lower_tank_mass_kg=lower_mass,
        upper_tank_mass_kg=upper_mass,
        total_pipes_co2_kg=total_pipes_embodied,
        pump_embodied_co2_kg=pump_emb,
        total_embodied_co2_kg=total_embodied,
        annual_pumping_co2_kg=annual_pumping_co2,
        annual_treatment_co2_kg=annual_treatment_co2,
        annual_chlorine_kg=annual_chlorine_kg,
        chlorine_dose_mg_l=chlorine_dose_mg_l,
        chlorine_co2_kg_per_kg=chlorine_co2_kg_per_kg,
        treatment_co2_kg_per_m3=treatment_co2_factor,
        annual_avoided_co2_kg=annual_avoided_co2,
        net_annual_avoided_co2_kg=net_annual_avoided_co2,
        lifetime_net_co2_saved_kg=lifetime_net_co2_saved,
        environmental_payback_years=env_payback,
        specific_co2_avoided_g_per_liter=specific_co2_avoided_g_l,
        is_environmentally_viable=is_viable,
        inventory_items=items
    )


@dataclass
class EnvironmentalSweepResult:
    best_lifetime_co2_vol_liters: float
    max_lifetime_co2_saved_kg: float
    best_payback_vol_liters: float
    min_payback_years: float
    sweep_details: List[Dict[str, Any]] = field(default_factory=list)


def run_environmental_sweep(
    volume_pluvial_map: List[Tuple[float, ...]],
    config: Optional[EnvironmentalConfig] = None
) -> EnvironmentalSweepResult:
    """
    Executa a varredura ambiental em uma série de volumes para encontrar o reservatório
    que otimiza o saldo acumulado de CO2 na vida útil.
    """
    if config is None:
        config = EnvironmentalConfig()

    details = []
    best_co2_vol = 0.0
    max_co2_saved = -1e9
    best_payback_vol = 0.0
    min_payback = 999.0

    for point in volume_pluvial_map:
        if len(point) < 2:
            raise ValueError("Cada ponto ambiental deve informar volume da cisterna e consumo pluvial anual.")
        vol_l, annual_m3 = point[0], point[1]
        point_config = config
        if len(point) >= 3:
            # A energia de bombeamento varia com o volume atendido e com as
            # partidas da alternativa; preservá-la por ponto evita aplicar a
            # energia de um único cenário a toda a varredura.
            point_config = replace(config, annual_pump_kwh=max(0.0, float(point[2])))
        lca = calculate_lca(vol_l, annual_m3, point_config)
        op_20yr = (lca.annual_pumping_co2_kg + lca.annual_treatment_co2_kg) * point_config.system_lifespan_years
        avoided_20yr = lca.annual_avoided_co2_kg * point_config.system_lifespan_years

        details.append({
            "volume_l": vol_l,
            "annual_m3": annual_m3,
            "material_mass_kg": lca.lower_tank_mass_kg,
            "embodied_co2_kg": lca.total_embodied_co2_kg,
            "op_co2_lifetime_kg": op_20yr,
            "positive_co2_lifetime_kg": lca.total_embodied_co2_kg + op_20yr,
            "offset_co2_lifetime_kg": -avoided_20yr,
            "net_annual_avoided_co2_kg": lca.net_annual_avoided_co2_kg,
            "lifetime_net_co2_saved_kg": lca.lifetime_net_co2_saved_kg,
            "payback_years": lca.environmental_payback_years,
            "is_viable": lca.is_environmentally_viable,
            "lca_result": lca
        })

        if lca.lifetime_net_co2_saved_kg > max_co2_saved:
            max_co2_saved = lca.lifetime_net_co2_saved_kg
            best_co2_vol = vol_l

        if lca.environmental_payback_years < min_payback:
            min_payback = lca.environmental_payback_years
            best_payback_vol = vol_l

    return EnvironmentalSweepResult(
        best_lifetime_co2_vol_liters=best_co2_vol,
        max_lifetime_co2_saved_kg=max_co2_saved,
        best_payback_vol_liters=best_payback_vol,
        min_payback_years=min_payback,
        sweep_details=details
    )
