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

from netuno.core.grid_emission_factors import BASE_PADRAO as BASE_PADRAO_DA_REDE
from netuno.core.grid_emission_factors import fator_co2eq as _fator_co2eq_da_rede
from netuno.core.pump_energy import consumo_especifico_padrao_kwh_por_m3
from netuno.core.chlorination import Cloracao, DOSE_PADRAO_MG_POR_LITRO, FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO, PUREZA_PADRAO
from netuno.core.water_supply_routes import ROTA_PADRAO as ROTA_PADRAO_DA_AGUA
from netuno.core.water_supply_routes import co2_evitado_por_m3 as _co2_evitado_por_m3
from netuno.core.etap_integration import (
    AREA_DE_RECURSO_M2,
    dimensionar_etap_do_projeto,
)


def grid_factor_default() -> float:
    """Fator da rede elétrica em **kg CO₂e/kWh**, para uso em ACV.

    É uma função — e não uma constante — porque `dataclasses` exige
    `default_factory` para valores lidos de arquivo, e porque assim o número
    nunca aparece transcrito no código-fonte.

    **Por que CO₂e e não CO₂.** Uma versão intermediária deste módulo passou a
    ler a série anual do MCTI/SIRENE, que é de **CO₂ apenas** e cobre só a
    geração. Foi um erro de grandeza: uma ACV precisa de CO₂-equivalente e de
    fronteira que inclua transmissão, distribuição, construção das usinas e as
    emissões biogênicas e de uso da terra. Vaz, Scolaro & Ghisi (2025,
    DOI 10.1016/j.scitotenv.2025.179774) mostram que a intensidade sobe de
    ~0,07 kg CO₂/kWh (SIRENE) para até 0,20 kg CO₂e/kWh quando os demais
    processos e gases entram. Usar o número do SIRENE aqui subestimaria o
    bombeamento e inflaria o saldo ambiental do sistema.

    A série do MCTI continua disponível em `grid_emission_factors.fator_anual`,
    corretamente rotulada, para quem precisar dela.
    """
    return _fator_co2eq_da_rede(BASE_PADRAO_DA_REDE)


def potable_water_factor_default() -> float:
    """Emissao evitada por m3, da rota de producao de agua adotada por padrao.

    A emissao evitada nao e propriedade do sistema pluvial: e propriedade da
    agua que se deixa de consumir. Substituir agua dessalinizada, agua tratada
    convencionalmente ou agua engarrafada sao coisas separadas por ordens de
    grandeza. O catalogo de rotas esta em
    :mod:`netuno.core.water_supply_routes`.
    """
    return _co2_evitado_por_m3(ROTA_PADRAO_DA_AGUA)


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
        material_density_kg_per_m3_tank=22.0,   # ~22 kg PEAD por m³ útil (cenário geométrico interno)
        co2_factor_kg_per_kg=1.612,             # kg CO2e / kg resina PEAD — ver source_reference
        co2_factor_kg_per_m3_tank=35.464,       # 22 * 1,612
        source_reference=(
            "Resina: Franklin Associates para o American Chemistry Council (out/2020), "
            "'Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin', "
            "Tabela 6: 1.612 kg CO2e por 1.000 kg de resina (TRACI 2.1 / IPCC 2013 GWP-100, "
            "escopo EUA). Substitui o valor interno anterior de 3,00, que não tinha fonte e "
            "declarava a mesma fronteira. A massa por m³ segue sendo cenário interno."
        ),
        description="Reservatório plástico rotomoldado pré-fabricado. Leve e de fácil instalação."
    ),
    "CONCRETO": MaterialPreset(
        name="Concreto Armado Moldado in loco",
        material_density_kg_per_m3_tank=1200.0, # ~0.5 m³ concreto armado (~1200 kg) por m³ útil
        co2_factor_kg_per_kg=0.14,              # 0.14 kg CO2e / kg concreto (Cimento CP-II + Armadura)
        co2_factor_kg_per_m3_tank=168.0,        # 1200 * 0.14 = 168 kg CO2e / m³ útil
        source_reference=(
            "Fator corroborado pelo SIDAC (inventário brasileiro da construção): concreto "
            "dosado em central de cerca de 310 kg CO2/m³ a 20 MPa a 480 kg CO2/m³ a 40 MPa; "
            "0,14 kg CO2e/kg x 2.400 kg/m³ = 336 kg/m³, dentro da faixa de 25 a 30 MPa. A massa "
            "por m³ útil (1.200 kg) segue sendo cenário geométrico interno; para a obra, use a "
            "EPD do concreto e o quantitativo de aço do projeto."
        ),
        description="Estrutura de concreto armado de alta durabilidade (50+ anos) e maior pegada inicial."
    ),
    "FIBRA": MaterialPreset(
        name="Poliéster Reforçado com Fibra de Vidro (PRFV)",
        # Densidade media da linha Fortlev entre 1.000 e 10.000 L. A massa exata
        # por capacidade esta em MASSA_PRFV_POR_CAPACIDADE_L, e e ela que o
        # calculo usa; este valor serve de referencia e para faixas fora da tabela.
        material_density_kg_per_m3_tank=15.0,
        co2_factor_kg_per_kg=3.25,             # kg CO2e/kg - ver source_reference
        co2_factor_kg_per_m3_tank=48.75,       # 15 * 3,25
        source_reference=(
            "Massa: catalogo tecnico Fortlev, 'Caixa d'agua em fibra de vidro' "
            "(peso da caixa vazia por capacidade), reservatorios conforme ABNT NBR 13210. "
            "Fator de emissao: Composites UK, 'Embodied carbon data for composites' "
            "(atualizado em 22/04/2026), que da faixa tipica de 2,5 a 4,0 kg CO2e/kg para "
            "pecas de PRFV; adota-se o ponto medio de 3,25. O valor de 8,1 kg CO2e/kg que "
            "circula na literatura antiga vem da base ICE dos anos 1990 e foi removido na "
            "ICE v4.0 - quem o encontrar deve descarta-lo."
        ),
        description="Reservatório composto leve, altamente anticorrosivo e de médio gasto energético."
    ),
    "ACO_INOX": MaterialPreset(
        name="Aço Inoxidável (AISI 304/316)",
        material_density_kg_per_m3_tank=38.0,  # kg de aço por m³ útil - cenário geométrico interno
        co2_factor_kg_per_kg=3.70,             # kg CO2e/kg a 50% de sucata - ver source_reference
        co2_factor_kg_per_m3_tank=140.6,       # 38 * 3,70
        source_reference=(
            "Fator: worldstainless (programa de aço inoxidável da World Steel Association), "
            "relatório de emissões de CO2 divulgado em 24/09/2024, berço-ao-portão com escopos "
            "1, 2 e 3. A emissão depende fortemente do teor de sucata da carga: 1,95 kg CO2/kg a "
            "85% de sucata, 2,45 a 75%, 3,70 a 50% e 6,80 a 30%. Adota-se o ponto de 50%, que é "
            "o cenário intermediário do relatório. O valor anterior deste programa, 2,89, "
            "correspondia a cerca de 66% de sucata, sem que isso estivesse declarado. "
            "Massa por m³ útil permanece cenário interno."
        ),
        description="Reservatório industrial metálico de altíssima longevidade e 100% reciclável."
    )
}

# Massa linear de tubo de PVC, por diâmetro nominal, em kg/m.
#
# Três origens, declaradas por linha em PIPE_LINEAR_MASS_SOURCE:
#
# 1. DN 20 a 60 — **peso real de produto**, da ficha técnica FTC000021 da
#    Amanco Wavin (revisão de outubro/2025), linha Soldável Água Fria, tubo
#    ponta-bolsa de 6 m. O peso unitário publicado foi dividido pelo
#    comprimento.
# 2. DN 75, 85 e 110 — geometria da ABNT NBR 5648 (tubo soldável de água fria,
#    diâmetro externo e espessura de parede da mesma ficha técnica, p. 8),
#    multiplicada pela densidade efetiva calibrada nos pesos reais acima.
# 3. DN 100 e 150 — geometria da ABNT NBR 5688:2018, Tabela 1, **série
#    reforçada**, que é a série que a própria norma destina a água pluvial.
#    São linhas de captação e extravasamento, não de pressão.
#
# A densidade efetiva de 1,511 g/cm³ foi obtida dos seis pesos reais e é muito
# consistente entre eles (1,504 a 1,516). Ela é maior que a densidade do PVC-U
# puro porque incorpora a massa da bolsa, que o tubo comercial traz.
#
# Até a versão 5.0.7 estas massas eram cenário interno. O erro não era pequeno
# nem sistemático: o DN 110 estava 47% abaixo do real e o DN 20, 36% acima.
PIPE_LINEAR_MASS_KG_PER_M: Dict[int, float] = {
    20:  0.132,
    25:  0.189,
    32:  0.299,
    40:  0.427,
    50:  0.668,
    60:  0.884,
    75:  1.412,
    85:  1.792,
    100: 1.176,
    110: 3.009,
    150: 2.502,
}

PIPE_LINEAR_MASS_SOURCE: Dict[int, str] = {
    20:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 20 x 6 m: 791,94 g",
    25:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 25 x 6 m: 1.132,24 g",
    32:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 32 x 6 m: 1.793,14 g",
    40:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 40 x 6 m: 2.561,27 g",
    50:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 50 x 6 m: 4.010,80 g",
    60:  "Amanco Wavin FTC000021 (out/2025), tubo soldável 60 x 6 m: 5.305,97 g",
    75:  "ABNT NBR 5648: DE 75,0 mm, parede 4,2 mm; densidade efetiva 1,511 g/cm³",
    85:  "ABNT NBR 5648: DE 85,0 mm, parede 4,7 mm; densidade efetiva 1,511 g/cm³",
    100: "ABNT NBR 5688:2018 Tab. 1, série reforçada: dem 101,6 mm, parede 2,5 mm",
    110: "ABNT NBR 5648: DE 110,0 mm, parede 6,1 mm; densidade efetiva 1,511 g/cm³",
    150: "ABNT NBR 5688:2018 Tab. 1, série reforçada: dem 150,0 mm, parede 3,6 mm",
}

# Emissão por metro = massa linear x fator do tubo instalado. O fator é
# 2,36 kg CO2e/kg, módulos A1-A3 da Declaração Ambiental de Produto EPD
# Australasia S-P-05503 (RXP PVC Pipes, 25/11/2022, EN 15804+A2), cuja unidade
# declarada é 1 kg de tubo instalado.
PVC_PIPE_CO2E_PER_KG = 2.36

PIPE_EMISSION_FACTORS_PER_METER: Dict[int, float] = {
    dn: round(massa * PVC_PIPE_CO2E_PER_KG, 4)
    for dn, massa in PIPE_LINEAR_MASS_KG_PER_M.items()
}

# Emissão incorporada de motobomba, por potência: massa do produto x
# intensidade de carbono por quilo de bomba.
#
# Não há Declaração Ambiental de Produto de motobomba residencial brasileira. O
# valor é composto por duas fontes recuperadas e lidas:
#
# 1. **Intensidade**: EPD da Grundfos para a bomba ALPHA1 GO 25-40 180,
#    EPD-GRU-20250340-CBA1-EN (IBU, emitida em 09/07/2025, válida até 2030,
#    EN 15804+A2). Módulos A1-A3, GWP-total de 10,4 kg CO2e por unidade, com
#    massa de referência de 2,179 kg: 4,77 kg CO2e por kg de bomba. É bomba
#    elétrica pequena de ferro fundido, aço, alumínio, cobre e eletrônica.
# 2. **Massa**: catálogo geral 60 Hz da Dancor, linha monofásica de aplicação
#    múltipla com carcaça em liga de alumínio-silício — CAM W-4C (1/4 a 1/2 CV)
#    e CAM W-10 (3/4 a 2 CV), coluna «Peso (kg)».
#
# Ressalvas que acompanham o número: a EPD é europeia, de um circulador com
# eletrônica embarcada (3% da massa), e a massa de referência inclui a
# embalagem. A intensidade por quilo é, portanto, aproximação de ordem de
# grandeza para uma centrífuga brasileira, e não inventário do produto.
#
# Até a versão 5.0.0 beta os valores eram 12, 18, 24, 30, 42 e 55 kg CO2e, dos
# quais quatro eram extrapolação aritmética do de 1/2 CV. Ficavam de 1,7 a 2,7
# vezes abaixo destes.
PUMP_EPD_KG_CO2E_POR_UNIDADE = 10.4       # EPD-GRU-20250340-CBA1-EN, A1-A3, GWP-total
PUMP_EPD_MASSA_REFERENCIA_KG = 2.179      # mesma EPD, «mass reference», com embalagem
PUMP_KG_CO2E_POR_KG = PUMP_EPD_KG_CO2E_POR_UNIDADE / PUMP_EPD_MASSA_REFERENCIA_KG

PUMP_MASS_KG: Dict[float, float] = {
    0.25: 6.1,    # Dancor CAM W-4C 1/4 CV monofásica
    0.50: 6.4,    # Dancor CAM W-4C 1/2 CV monofásica
    0.75: 13.5,   # Dancor CAM W-10 3/4 CV monofásica
    1.00: 15.3,   # Dancor CAM W-10 1 CV monofásica
    1.50: 17.5,   # Dancor CAM W-10 1 1/2 CV monofásica
    2.00: 20.7,   # Dancor CAM W-10 2 CV monofásica
}

PUMP_EMBEDDED_CO2: Dict[float, float] = {
    cv: round(massa * PUMP_KG_CO2E_POR_KG, 1) for cv, massa in PUMP_MASS_KG.items()
}

PUMP_EMBEDDED_CO2_SOURCE: Dict[float, str] = {
    cv: (f"massa {str(massa).replace('.', ',')} kg (catálogo Dancor, linha CAM W) x "
         f"{PUMP_KG_CO2E_POR_KG:.2f}".replace(".", ",")
         + " kg CO2e/kg (EPD Grundfos EPD-GRU-20250340-CBA1-EN, A1-A3)")
    for cv, massa in PUMP_MASS_KG.items()
}


def pump_embodied_co2_is_extrapolated(power_cv: float) -> bool:
    """Diz se o valor daquela potência é extrapolado em vez de estimado.

    Exposto para que a interface e os relatórios possam sinalizar, em vez de
    apresentar os seis valores como se tivessem o mesmo estatuto.
    """
    fonte = PUMP_EMBEDDED_CO2_SOURCE.get(power_cv, "")
    return "extrapola" in fonte


# Massa de reservatorio vazio por capacidade, catalogo tecnico Fortlev
# "Caixa d'agua em fibra de vidro" (coluna "Peso em quilos - caixa vazia").
# Fabricados conforme ABNT NBR 13210.
#
# O programa tratava a massa como densidade CONSTANTE de 20 kg por m3 util. Os
# dados do fabricante mostram que nao e: ha economia de escala clara, de
# 20,3 kg/m3 num reservatorio de 1.000 L para 13,7 kg/m3 num de 10.000 L. A
# constante de 20 so vale para o menor reservatorio da linha, e superestima em
# cerca de 25% um reservatorio de 5.000 L, que e o porte tipico destes estudos.
MASSA_PRFV_POR_CAPACIDADE_L: Dict[float, float] = {
    310.0: 9.70,
    500.0: 14.10,
    1000.0: 20.30,
    1500.0: 27.10,
    2000.0: 34.80,
    3000.0: 49.00,
    4000.0: 57.10,
    5000.0: 74.90,
    6000.0: 94.00,
    7500.0: 110.30,
    8000.0: 116.40,
    10000.0: 136.70,
    12000.0: 161.00,
    15000.0: 190.90,
    20000.0: 278.10,
    25000.0: 413.00,
}

FONTE_MASSA_PRFV = (
    "FORTLEV, Catalogo tecnico 'Caixa d'agua em fibra de vidro', tabela de peso "
    "em quilos (caixa vazia). Reservatorios conforme ABNT NBR 13210."
)


def massa_de_reservatorio_prfv_kg(capacidade_litros: float) -> float:
    """Massa do reservatorio vazio em PRFV, interpolada do catalogo.

    Fora da faixa tabelada extrapola-se pela densidade do extremo mais proximo,
    porque uma extrapolacao linear da curva daria massa negativa para volumes
    pequenos.
    """
    if capacidade_litros <= 0:
        return 0.0

    tabela = sorted(MASSA_PRFV_POR_CAPACIDADE_L.items())
    menor_v, menor_m = tabela[0]
    maior_v, maior_m = tabela[-1]

    if capacidade_litros <= menor_v:
        return capacidade_litros * (menor_m / menor_v)
    if capacidade_litros >= maior_v:
        return capacidade_litros * (maior_m / maior_v)

    for (v0, m0), (v1, m1) in zip(tabela, tabela[1:]):
        if v0 <= capacidade_litros <= v1:
            fracao = (capacidade_litros - v0) / (v1 - v0)
            return m0 + fracao * (m1 - m0)

    return capacidade_litros * (maior_m / maior_v)


def massa_do_reservatorio_kg(capacidade_litros: float, material_key: str, densidade_kg_m3: float) -> float:
    """Massa do reservatorio vazio.

    Para o PRFV usa-se a tabela do catalogo Fortlev, porque a massa nao e
    proporcional ao volume: ha economia de escala, e tratar a densidade como
    constante superestimava um reservatorio de 10.000 L em 46%. Para os demais
    materiais, na falta de tabela de fabricante, mantem-se a densidade constante,
    que segue sendo cenario interno.
    """
    if normalize_material_key(material_key) == "FIBRA":
        return massa_de_reservatorio_prfv_kg(capacidade_litros)
    return (capacidade_litros / 1000.0) * densidade_kg_m3


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
    # Derivado da mesma física do módulo econômico, em pump_energy.py. Era
    # 0,40 fixo, sem origem e 36% acima do que aquela física dá.
    specific_kwh_per_m3: float = field(default_factory=consumo_especifico_padrao_kwh_por_m3)
    material: str = "Ferro Fundido, Cobre & Alumínio"


@dataclass
class EnvironmentalConfig:
    lower_tank_vol: float = 4000.0
    annual_water_saved_m3: float = 0.0
    annual_pump_kwh: float = 0.0
    # Principal mais reserva, como em `NetunoConfig.pump_count`. Os dois padroes
    # divergiam - 2 no projeto, 1 aqui - de modo que o economico cobrava duas
    # bombas e a ACV contava o carbono de uma so, 18 kg CO2e a menos.
    pump_count: int = 2                          # 1 = Principal, 2 = Principal + Reserva/Backup
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
    # Fator da rede elétrica em kg CO2e/kWh. As bases documentadas — SIDAC,
    # CaDI, e os indicadores de Vaz, Scolaro & Ghisi (2025) — estão em
    # `netuno.core.grid_emission_factors.bases_disponiveis()`, cada uma com
    # fonte, gás e fronteira declarados.
    grid_co2_factor_kg_kwh: float = field(default_factory=grid_factor_default)
    grid_co2_factor_basis: str = BASE_PADRAO_DA_REDE  # base do fator acima, para o relatório
    # Rota de producao da agua substituida. Define a emissao evitada por m3.
    water_supply_route: str = ROTA_PADRAO_DA_AGUA
    potable_water_co2_kg_m3: float = field(default_factory=potable_water_factor_default)
    # Cloração: a massa anual é calculada a partir do volume pluvial
    # efetivamente utilizado.  A intensidade de CO2e resulta de dose × fator.
    # Cadeia unica em netuno/core/chlorination.py. A dose e de cloro ATIVO;
    # o fator e por kg de PRODUTO comercial, e a pureza faz a ponte.
    chlorine_dose_mg_l: float = DOSE_PADRAO_MG_POR_LITRO   # mg de Cl2 ativo por litro
    chlorine_product_purity: float = PUREZA_PADRAO         # kg Cl2 ativo por kg de produto
    # Ate a 5.0.7 este campo valia 25,0 e era descrito como kg CO2e/kg de Cl2.
    # O numero nao tinha fonte e era identico ao custo (25,00 R$/kg) no
    # costs_database.json. Substituido pelo fator do hipoclorito de calcio,
    # por kg de PRODUTO, que o modulo de qualidade ja usava.
    chlorine_co2_kg_per_kg: float = FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    # Campo legado. Projetos antigos podem informar diretamente kg CO2e/m³;
    # quando presente, ele preserva o resultado histórico de emissão.
    chemical_treatment_co2_m3: Optional[float] = None
    system_lifespan_years: float = 20.0          # Vida útil considerada (anos)

    # Linha de tratamento (ETAP). Estes três campos são a escolha feita na aba
    # de Qualidade da Água. Até a versão 5.0.7 eles existiam apenas em
    # `NetunoConfig`, eram escritos pela interface e não eram lidos por ninguém:
    # optar por ultravioleta não alterava emissão nem custo. Ver
    # `netuno/core/etap_integration.py`.
    water_quality_target_class: str = "classe_1"
    water_quality_disinfection: str = "cloro"    # "cloro", "uv", "ozonio"
    water_quality_polishing: bool = False
    roof_area_m2: float = AREA_DE_RECURSO_M2     # dimensiona o filtro de entrada
    # Dimensionamento do subsistema físico de descarte de primeiras águas
    first_flush_system_enabled: bool = False
    discard: float = 1.0                         # lâmina de descarte em mm
    # Desligar devolve o comportamento da 5.0.7, em que o tratamento era só a
    # cloração. Serve para reproduzir estudos anteriores, não para uso corrente.
    etap_enabled: bool = True

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
    annual_treatment_co2_kg: float       # CO2 anual da linha de tratamento (kg CO2e / ano),
                                          # inclui a cloração e, quando houver,
                                          # ultravioleta, ozônio e polimento
    annual_chlorine_kg: float             # Massa anual de PRODUTO comercial (kg/ano),
                                          # ja corrigida pela pureza - e o que se compra
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
    # Parcela da linha de tratamento que NAO e a cloracao: reator ultravioleta,
    # ozonizador e filtro de polimento. Zero quando so ha cloracao.
    etap_extra_co2_kg_yr: float = 0.0
    etap_capex_brl: float = 0.0
    etap_disinfection_stages: List[str] = field(default_factory=list)


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

    lower_mass = massa_do_reservatorio_kg(tank_vol_liters, config.lower_material_key, den_lower)
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

        upper_mass = massa_do_reservatorio_kg(config.upper_tank_vol_liters, config.upper_material_key, den_upper)
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
            # A massa linear e o fator do tubo têm fonte declarada; só o diâmetro
            # fora da tabela, ou o fator digitado pelo usuário, fica sem ela.
            source_reference=(
                "Fator informado pelo usuário" if (pipe.custom_co2_per_m and pipe.custom_co2_per_m > 0)
                else f"{PIPE_LINEAR_MASS_SOURCE[dn]} × 2,36 kg CO2e/kg (EPD S-P-05503, RXP PVC Pipes, A1-A3)"
                if dn in PIPE_LINEAR_MASS_SOURCE
                else "Cenário de triagem: diâmetro fora da tabela de massas lineares"
            )
        ))

    # 4. Motobomba de Recalque (Fabricação e Reserva/Backup)
    pump = config.pump
    pump_count = getattr(config, 'pump_count', 1)
    pump_unit_emb = pump.custom_embodied_co2 if (pump.custom_embodied_co2 and pump.custom_embodied_co2 > 0) else PUMP_EMBEDDED_CO2.get(pump.power_cv, PUMP_EMBEDDED_CO2[min(PUMP_EMBEDDED_CO2, key=lambda cv: abs(cv - pump.power_cv))])
    pump_emb = pump_unit_emb * pump_count
    mat_desc = getattr(config, 'pump_material', getattr(pump, 'material', "Ferro Fundido, Cobre & Alumínio"))

    count_str = f"{pump_count} un. (1 Principal + 1 Reserva/Backup)" if pump_count > 1 else "1 un. (Principal)"
    items.append(LCAItemBreakdown(
        category=f"Motobomba de Recalque ({pump.power_cv:.2f} CV - {mat_desc})",
        quantity_str=f"{count_str} — {pump.power_cv:.2f} CV",
        embodied_co2_kg=pump_emb,
        annual_op_co2_kg=0.0,
        lifetime_net_co2_kg=pump_emb,
        source_reference=("Massa de catálogo Dancor (60 Hz) × 4,77 kg CO2e/kg da EPD Grundfos "
                          "EPD-GRU-20250340-CBA1-EN (A1-A3): aproximação de ordem de grandeza; "
                          "a EPD do fabricante empregado prevalece")
    ))

    # 4.1 Subsistema de Descarte de Primeiras Águas (Filtro de Folhas e Reservatório de Descarte)
    ff_embodied = 0.0
    if getattr(config, 'first_flush_system_enabled', False) and getattr(config, 'discard', 0.0) > 0:
        from netuno.core.water_quality import size_first_flush_system
        ff_res = size_first_flush_system(
            discard_mm=float(getattr(config, 'discard', 1.0)),
            roof_area_m2=float(getattr(config, 'roof_area_m2', AREA_DE_RECURSO_M2)),
            regional_factor=1.0,
        )
        if ff_res.diverter_volume_liters > 0:
            ff_embodied = ff_res.first_flush_embodied_co2_kg
            items.append(LCAItemBreakdown(
                category=f"Sistema de Descarte de 1ª Água (Filtro Folhas + Res. {ff_res.diverter_volume_liters:.0f} L)",
                quantity_str=f"{ff_res.diverter_volume_liters:.0f} L ({ff_res.diverter_mass_kg + ff_res.leaf_filter_mass_kg:.1f} kg material)",
                embodied_co2_kg=ff_embodied,
                annual_op_co2_kg=0.0,
                lifetime_net_co2_kg=ff_embodied,
                source_reference="ABNT NBR 15527:2019 (Descarte inicial) / Inventário de Polímeros & Inox"
            ))

    total_embodied = lower_embodied + upper_embodied + total_pipes_embodied + pump_emb + ff_embodied

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

    # 6. Operação Anual (linha de tratamento: cloração e, quando houver, as
    #    barreiras adicionais dimensionadas pela ETAP)
    etap_extra_co2 = 0.0
    etap_capex = 0.0
    etap_stages: List[str] = []
    pluvial_cl2_base = 0.0
    if config.upper_tank_used:
        chlorine_dose_mg_l = max(0.0, float(config.chlorine_dose_mg_l))
        chlorine_co2_kg_per_kg = max(0.0, float(config.chlorine_co2_kg_per_kg))
        ref_saved_m3 = float(getattr(config, 'annual_water_saved_m3', 0.0))
        pluvial_cl2_base = ref_saved_m3 if ref_saved_m3 > 0 else annual_pluvial_m3

        # A conta passa pela cadeia unica: a pureza converte dose de cloro ativo
        # em massa de produto, que e a base do fator de emissao. Somar os dois
        # sem essa conversao era metade do erro de 11,7x entre os modulos.
        cloracao = Cloracao(
            dose_mg_por_litro=chlorine_dose_mg_l,
            pureza=max(1e-6, float(getattr(config, 'chlorine_product_purity', PUREZA_PADRAO))),
            fator_kg_co2e_por_kg_produto=chlorine_co2_kg_per_kg,
        )
        annual_chlorine_kg = cloracao.massa_anual_de_produto_kg(pluvial_cl2_base)
        calculated_treatment_factor = cloracao.co2e_kg_por_m3
        treatment_co2_factor = (
            max(0.0, float(config.chemical_treatment_co2_m3))
            if config.chemical_treatment_co2_m3 is not None
            else calculated_treatment_factor
        )
        annual_treatment_co2 = pluvial_cl2_base * treatment_co2_factor

        # A ETAP substitui este termo, e nao se soma a ele. O total dela ja
        # contem o hipoclorito; somar contaria o cloro duas vezes.
        #
        # O campo legado `chemical_treatment_co2_m3` continua tendo precedencia,
        # porque projetos antigos informavam a intensidade diretamente e trocar
        # o numero por baixo mudaria resultados ja publicados.
        if getattr(config, 'etap_enabled', True) and config.chemical_treatment_co2_m3 is None:
            etap = dimensionar_etap_do_projeto(config, annual_pluvial_m3=pluvial_cl2_base)
            annual_treatment_co2 = etap.co2e_anual
            etap_extra_co2 = etap.co2e_anual_sem_cloro
            etap_capex = etap.capex
            etap_stages = etap.estagios
            treatment_co2_factor = annual_treatment_co2 / max(1e-9, pluvial_cl2_base)
            annual_chlorine_kg = etap.resultado.annual_chlorine_kg
    else:
        chlorine_dose_mg_l = 0.0
        chlorine_co2_kg_per_kg = 0.0
        annual_chlorine_kg = 0.0
        treatment_co2_factor = 0.0
        annual_treatment_co2 = 0.0

    if annual_treatment_co2 > 0:
        if etap_stages:
            categoria = "Linha de Tratamento (ETAP)"
            fonte = ("Estágios: " + "; ".join(etap_stages) +
                     ". Dimensionamento em netuno/core/water_quality.py")
        else:
            categoria = "Dosagem Química / Desinfecção (Caixa Superior)"
            fonte = "Dosagem no reservatório superior configurada pelo usuário"
        items.append(LCAItemBreakdown(
            category=categoria,
            quantity_str=(f"{pluvial_cl2_base:.1f} m³/ano; {annual_chlorine_kg:.3f} kg produto/ano "
                          f"({chlorine_dose_mg_l:.2f} mg Cl2/L; {treatment_co2_factor:.3f} kg CO2e/m³)"),
            embodied_co2_kg=0.0,
            annual_op_co2_kg=annual_treatment_co2,
            lifetime_net_co2_kg=annual_treatment_co2 * config.system_lifespan_years,
            source_reference=fonte
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
        inventory_items=items,
        etap_extra_co2_kg_yr=etap_extra_co2,
        etap_capex_brl=etap_capex,
        etap_disinfection_stages=etap_stages,
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
