import os
import re
from netuno.core.hydrology_defaults import COEFICIENTE_DE_ESCOAMENTO_PADRAO
from netuno.core.pump_hydraulics import ALTURA_MANOMETRICA_PADRAO_M
from netuno.core.chlorination import (
    DOSE_PADRAO_MG_POR_LITRO,
    FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
    PUREZA_PADRAO,
)
import csv
import hashlib
import socket
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union, Tuple
import numpy as np
from netuno import __version__


def generate_project_id() -> str:
    """Gera uma referência legível e praticamente única para um projeto."""
    import time
    import os as _os
    import uuid

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    raw = f"{time.time_ns()}-{socket.gethostname()}-{_os.getpid()}-{uuid.uuid4().hex}"
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:8].upper()
    return f"N5-{timestamp}-{digest}"

def parse_float(val: Any, default: float = 0.0) -> float:
    """Safely parse float supporting pt-BR (1.234,56 or 1234,56) and en-US (1,234.56 or 1234.56)."""
    import math
    if val is None:
        return default
    s = str(val).strip()
    if not s or s.lower() in ("-", "none", "nan", "inf", "-inf", "+inf"):
        return default
    try:
        if '.' in s and ',' in s:
            if s.rfind(',') > s.rfind('.'):
                # pt-BR: 1.234,56 -> 1234.56
                s = s.replace('.', '').replace(',', '.')
            else:
                # en-US: 1,234.56 -> 1234.56
                s = s.replace(',', '')
        elif ',' in s:
            # 1234,56 -> 1234.56
            s = s.replace(',', '.')
        parsed = float(s)
        return parsed if math.isfinite(parsed) else default
    except (ValueError, TypeError):
        return default

def parse_int(val: Any, default: int = 0) -> int:
    """Safely parse integer supporting pt-BR thousands separators."""
    if val is None:
        return default
    s = str(val).strip()
    if not s or s in ("-", "None", "nan", "NaN"):
        return default
    try:
        parsed_f = parse_float(s, float(default))
        return int(round(parsed_f))
    except (ValueError, TypeError):
        return default

def format_ptbr(val: Union[float, int], decimals: int = 2, thousands: bool = True) -> str:
    """Formats a number in Brazilian style: dot for thousands, comma for decimals (ex: 1.234,56)."""
    if val is None:
        return "-"
    try:
        val_f = float(val)
        if thousands:
            s = f"{val_f:,.{decimals}f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            s = f"{val_f:.{decimals}f}".replace('.', ',')
        return s
    except Exception:
        return str(val)

def load_precipitation(file_path: str) -> np.ndarray:
    """
    Reads a daily precipitation CSV file (single column of numbers).
    Handles comma and dot decimals. Returns numpy array of daily rainfall in mm.
    """
    base_name = os.path.basename(file_path)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    candidate_paths = [
        file_path,
        base_name,
        os.path.join(".", base_name),
        os.path.join(base_dir, "data", "rainfall", base_name),
        os.path.join(base_dir, "Additional_Material", "Precipitation_Samples", base_name)
    ]
    
    target_path = None
    for cp in candidate_paths:
        if os.path.exists(cp) and os.path.isfile(cp):
            target_path = cp
            break
            
    if not target_path:
        raise FileNotFoundError(f"Could not find precipitation file: {file_path} (or {base_name})")
            
    import math

    # Falha de registro vira NaN, e nao 0 mm. Antes, linha vazia ou texto no
    # meio da serie viravam dia seco em silencio, o que subestima a chuva sem
    # aviso; e um cabecalho como "Data;Precipitacao" encerrava a leitura na
    # primeira linha e devolvia serie vazia. Agora o cabecalho e pulado, a falha
    # e preservada, e a simulacao recusa NaN e valor negativo dizendo onde estao.
    nan = float("nan")
    lidos = []  # (valor, linha_tinha_conteudo)
    iniciou = False
    with open(target_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line_str = line.strip()
            valor = parse_float(line_str, nan) if line_str else nan
            if not iniciou:
                if math.isnan(valor):
                    continue  # cabecalho ou linhas vazias antes dos dados
                iniciou = True
            elif (';' in line_str or 'Descarte' in line_str or 'Data' in line_str
                  or 'Área' in line_str or 'Demanda' in line_str):
                break  # bloco de configuracao do Netuno 4, depois dos dados
            lidos.append((valor, bool(line_str)))
    # Linhas vazias no fim do arquivo sao formatacao, e nao falha de registro.
    while lidos and math.isnan(lidos[-1][0]) and not lidos[-1][1]:
        lidos.pop()
    return np.array([v for v, _ in lidos], dtype=np.float64)



@dataclass
class NetunoConfig:
    # Identificação única do projeto
    project_name: str = "Novo projeto Netuno"
    project_id: str = field(default_factory=generate_project_id)
    created_at: str = field(default_factory=lambda: datetime.now().strftime("%d/%m/%Y %H:%M"))

    precip_file: str = ""
    climate_source_mode: str = "national_db"  # "national_db" (base nacional) ou "custom_file" (arquivo próprio)
    climate_city_uf: str = "SC"
    climate_city_name: str = "Florianópolis"
    climate_model: str = "INM-CM4"
    climate_scenario: str = "HIST"
    climate_start_date: str = "01/01/1980"
    climate_end_date: str = "31/12/2013"
    tariff_customized: bool = False

    discard: float = 1.0  # mm
    discard_mode: int = 1  # 1 = todos os eventos, 2 = 1º evento após estiagem, 3 = a cada X dias
    discard_days_interval: int = 7  # intervalo para modo 3
    start_date: str = "01/01/1980"
    area: float = 100.0  # m²
    # Total water demand mode: 0 = fixed total demand per capita or total
    demand_type: int = 0
    demand_mode: str = "constant"  # "constant", "weekly", "monthly", "daily"
    demand_value: float = 200.0  # L/dia, por habitante ou total
    demand_monthly: List[float] = field(default_factory=list)
    
    # Resident count mode: 0 = fixed number of residents
    residents_type: int = 0
    residents_count: int = 4
    residents_monthly: List[int] = field(default_factory=list)
    num_economias: int = 1  # Número de economias / apartamentos com micromedição individual
    
    # Discretização dos Usos da Água (Potável Interno, Não-Potável Interno e Irrigação Condicional)
    potable_indoor_share: float = 0.65  # Fração potável do consumo interno (ex: 65% para banho/cozinha/beber)
    non_potable_indoor_share: float = 0.35  # Fração não-potável do consumo interno (ex: 35% para bacias/máquina)
    irrigation_liters_per_day: float = 50.0  # Volume diário fixo de irrigação/usos externos (L/dia)
    irrigation_rain_threshold_mm: float = 2.0  # Limiar diário de precipitação para supressão da irrigação (mm/dia)
    irrigation_potable_backup: bool = True  # Se True, a rede pública atende a irrigação em dias secos se a cisterna secar
    irrigation_garden_area_m2: float = 0.0  # Área de jardim em m² para o assistente de dimensionamento
    irrigation_rate_l_m2_day: float = 3.0  # Taxa diária de rega (L/m²/dia)
    
    rainwater_share: float = 0.4  # fração de 0 a 1 (0,4 = 40%)
    
    # Weekly modulation (7 days: Mon to Sun)
    weekly_demands: List[float] = field(default_factory=list)
    weekly_residents: List[int] = field(default_factory=list)
    weekly_shares: List[float] = field(default_factory=list)
    
    # Monthly modulation (12 months: Jan to Dec)
    monthly_shares: List[float] = field(default_factory=list)
    
    # Daily total series modulation (free-length lists)
    daily_demands: List[float] = field(default_factory=list)
    daily_residents: List[float] = field(default_factory=list)
    daily_shares: List[float] = field(default_factory=list)
    
    runoff_coeff: float = COEFICIENTE_DE_ESCOAMENTO_PADRAO  # ver hydrology_defaults
    
    # Upper Reservoir
    upper_tank_vol: float = 500.0  # L
    upper_tank_used: int = 1  # 0 = sem caixa superior, 1 = com caixa superior
    pumping_threshold: float = 50.0  # L, nível de acionamento do recalque
    
    # Lower Reservoir
    lower_tank_max: float = 10000.0  # L
    lower_tank_step: float = 250.0  # L
    lower_tank_mode: int = 1  # 0 = volume fixo, 1 = varredura
    lower_tank_fixed: float = 2000.0  # usado no modo de volume fixo
    
    delta_ideal: float = 5.0  # limiar de ganho marginal para o volume ideal, em %/m³

    # Economic Parameters
    econ_lower_tank_vol: float = 2000.0
    water_tariffs: List[Tuple[float, float, float, int]] = field(
        # CASAN residencial, vigente a partir de 01/04/2026. A primeira linha é
        # a TFDI mensal; as demais são faixas de consumo em R$/m³.
        default_factory=lambda: [
            (0.0, 0.0, 46.34, -1),
            (0.0, 10.0, 3.08, 1),
            (10.0, 25.0, 14.31, 1),
            (25.0, 50.0, 19.14, 1),
            (50.0, 999999.0, 24.08, 1),
        ]
    )  # (min_m3, max_m3, rate_or_fixed, is_fixed)
    tariff_city_uf: str = "SC"
    tariff_city_name: str = "Florianópolis"
    elec_city_uf: str = "SC"
    elec_city_name: str = "Florianópolis"
    # Percentual da TARIFA DE ÁGUA quando sewage_mode == 1, ou valor fixo em R$
    # quando sewage_mode == 0. O denominador é a parcela de água, não a fatura:
    # a CASAN cobra 100%, o que faz o esgoto igualar a água e responder por
    # metade da fatura total. Confundir os dois denominadores dobra ou divide
    # pela metade a conta de esgoto.
    sewage_rate: float = 100.0
    sewage_mode: int = 1  # 0 = valor fixo em R$, 1 = percentual da parcela de água
    water_tax_fixed: float = 0.0  # R$
    water_tax_var: float = 0.0  # %
    inflation: float = 0.2  # % ao mês; inflação dos custos de O&M
    tariff_escalation: float = 12.0  # meses; comprimento do período de reajuste
    water_tariff_escalation: float = 5.0  # % por período de reajuste; com 12 meses, % ao ano
    sewage_tariff_escalation: float = 5.0  # % por período de reajuste; com 12 meses, % ao ano
    elec_tariff_escalation: float = 5.0  # % por período de reajuste; com 12 meses, % ao ano
    analysis_period_years: int = 20  # anos
    tma: float = 2.0  # % ao mês; taxa mínima de atratividade
    install_month: int = 0
    
    # Materials & Components Selection
    lower_tank_material: str = "PEAD"  # "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"
    upper_tank_material: str = "PEAD"  # "PEAD", "CONCRETO", "FIBRA" (PRFV), "ACO_INOX"
    
    # Incentivos Fiscais (IPTU Verde) & Bandeiras Tarifárias ANEEL
    iptu_green_enabled: bool = False
    # Caso-base de consumo do aplicativo EDGE, em L/pessoa*dia. Zero significa
    # nao declarado: entao vale a demanda modelada do projeto, com ressalva.
    edge_base_case_l_person_day: float = 0.0
    iptu_annual_value: float = 4000.0       # Valor venal do IPTU anual da edificação (R$/ano)
    iptu_discount_pct: float = 5.0          # Desconto municipal do IPTU Verde (%)
    tariff_flag: str = "verde"              # "verde", "amarela", "vermelha_1", "vermelha_2", "branca"

    # Tipologia da edificação, escolhida na Etapa 2.
    #
    # Ficava presa num dicionário local da aba de edificação: a demanda que ela
    # define atravessava o programa, mas a tipologia em si não. Sem ela nenhum
    # módulo sabe que tipo de edificação está sendo estudada, e o econômico não
    # tem como perceber que cobra tarifa residencial de um hospital.
    building_template_id: str = "res_medio"

    # Qualidade da Água & Linha de Tratamento (ETAP)
    water_quality_target_class: str = "classe_1"
    water_quality_disinfection: str = "cloro"   # "cloro", "uv", "ozonio", "nenhum"
    water_quality_polishing: bool = False
    # Dimensionamento físico e orçamentário do subsistema de descarte de primeiras águas
    first_flush_system_enabled: bool = False
    # Desligar devolve o comportamento da 5.0.7, em que a linha de tratamento
    # nao entrava no investimento nem no custeio. Serve para reproduzir estudos
    # anteriores, e para hipoteses de CAPEX nulo.
    etap_enabled: bool = True
    
    # Chlorination / Chemical Disinfection Treatment
    chlorine_treatment_enabled: bool = True
    chlorine_dose_mg_l: float = DOSE_PADRAO_MG_POR_LITRO   # mg de Cl2 ativo por litro
    chlorine_product_purity: float = PUREZA_PADRAO         # kg Cl2 ativo por kg de produto
    chlorine_cost_per_kg: float = 25.0      # R$ por kg de PRODUTO comercial
    # O valor de 25,0 que aqui estava nao tinha fonte e era identico ao custo
    # acima, em R$/kg. Ver netuno/core/chlorination.py.
    chlorine_co2_kg_per_kg: float = FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO

    # Piping Network
    # List of tuples/dicts or PipeInput: (diameter_mm, length_m)
    pipes_list: List[Tuple[int, float]] = field(default_factory=lambda: [
        (32, 20.0),   # DN 32 mm - 20 m (Linha de Recalque padrão da motobomba 0.5 CV)
        (40, 5.0),    # DN 40 mm - 5 m (Linha de Sucção padrão da motobomba 0.5 CV)
        (75, 0.0),    # DN 75 mm - 0 m (Distribuição)
        (100, 20.0),  # DN 100 mm - 20 m (Captação / Extravasor)
        (150, 0.0),   # DN 150 mm - 0 m (Coletores de Grande Porte)
    ])

    def get_pipe_length(self, dn: int) -> float:
        for d, length in self.pipes_list:
            if int(d) == int(dn):
                return float(length)
        return 0.0

    def set_pipe_length(self, dn: int, length: float):
        target_dn = int(dn)
        target_len = max(0.0, float(length))
        found = False
        new_list = []
        for d, l in self.pipes_list:
            if int(d) == target_dn:
                new_list.append((target_dn, target_len))
                found = True
            else:
                new_list.append((int(d), float(l)))
        if not found:
            new_list.append((target_dn, target_len))
        self.pipes_list = new_list

    def update_pump_pipes(self, suction_dn: int, recalque_dn: int, suction_len: float = 5.0, recalque_len: float = 20.0):
        """Sincroniza os comprimentos de sucção e recalque (5m e 20m) a partir dos diâmetros da motobomba."""
        for d in (20, 25, 32, 40, 50, 60, 75, 85, 110):
            if d != 100 and d != 150:
                self.set_pipe_length(d, 0.0)
        self.set_pipe_length(int(suction_dn), max(0.0, float(suction_len)))
        self.set_pipe_length(int(recalque_dn), max(0.0, float(recalque_len)))

    def total_pipe_length(self) -> float:
        return sum(float(l) for _, l in self.pipes_list)

    def get_pipe_lengths_dict(self) -> Dict[int, float]:
        res = {20: 0.0, 25: 0.0, 32: 0.0, 40: 0.0, 50: 0.0, 60: 0.0, 75: 0.0, 85: 0.0, 100: 0.0, 110: 0.0, 150: 0.0}
        for d, l in self.pipes_list:
            res[int(d)] = float(l)
        return res

    # Initial Investment Costs (CAPEX)
    cost_lower_tank: float = 0.0
    cost_upper_tank: float = 0.0
    cost_labor: float = 0.0
    cost_piping: float = 0.0
    cost_accessories: float = 0.0
    
    # Pump Parameters
    pump_count: int = 2  # principal + reserva como configuração inicial recomendada
    pump_power_str: str = "1/2"
    pump_power_kw: float = 0.36775  # kW (1 CV = 0,7355 kW; 1/2 CV = 0,36775 kW)

    # Altura manométrica total: desnível geométrico entre a sucção e a entrada
    # do reservatório superior, mais as perdas de carga. É o parâmetro que mais
    # pesa no consumo de bombeamento, e até a versão 5.0.8 não existia: estava
    # embutido na vazão e no rendimento fixos, que juntos implicavam 67 m —
    # altura de edifício alto, não de casa.
    # Zero significa «não informada»: o assistente de motobomba a calcula a
    # partir da altura geométrica e das perdas, e é ela que rege a energia
    # quando existe. Sem ela, cai-se na vazão informada ou no valor de recurso.
    pump_manometric_head_m: float = 0.0

    # Rendimento do conjunto motobomba. Zero ou negativo faz o programa adotar o
    # típico do porte, que cresce com a potência.
    pump_efficiency: float = 0.0  # %, 0 = deduzir do porte

    # Vazão em L/h. Zero faz o programa deduzi-la da potência e da altura, pela
    # equação da bomba. Antes era 2.280 fixo, e não acompanhava a potência: uma
    # bomba de 2 CV recalcava tão devagar quanto uma de 1/4.
    pump_flow_rate: float = 0.0
    pump_startup_time_h: float = 0.03  # h
    # Rendimento do MOTOR, em %. A potencia de placa e a mecanica no eixo, e o
    # rendimento do motor e o que separa a energia de eixo da energia que o
    # medidor registra. Zero significa nao informado: vale entao a Tabela 13 da
    # ABNT NBR 17094-2:2016 para a potencia escolhida.
    pump_motor_efficiency: float = 0.0  # %
    pump_unit_cost: float = 300.0  # R$, referência de mercado para motobomba periférica 1/2 CV
    elec_tariff: float = 0.6957  # R$/kWh (Tarifa B1 Residencial CELESC/SC Florianópolis)
    elec_tax_fixed: float = 0.0  # R$
    elec_tax_var: float = 0.0  # %
    
    # Operational Costs (OPEX)
    # List of (name, periodicity_months, fixed_cost_R$, var_cost_R$_per_m3)
    op_costs: List[Tuple[str, int, float, float]] = field(default_factory=lambda: [
        ("Inspeção e limpeza de calhas/pré-filtro", 12, 240.0, 0.0),
        ("Limpeza e inspeção do reservatório", 12, 320.0, 0.0),
        ("Manutenção preventiva da motobomba", 12, 180.0, 0.0),
    ])

    @property
    def lower_tank_unit_cost(self) -> float:
        return self.cost_lower_tank if self.cost_lower_tank > 0 else 2000.0

    @lower_tank_unit_cost.setter
    def lower_tank_unit_cost(self, val: float):
        self.cost_lower_tank = float(val)

    @property
    def upper_tank_unit_cost(self) -> float:
        return self.cost_upper_tank if self.cost_upper_tank > 0 else 380.0

    @upper_tank_unit_cost.setter
    def upper_tank_unit_cost(self, val: float):
        self.cost_upper_tank = float(val)

    @property
    def filters_pipes_cost(self) -> float:
        tot = self.cost_piping + self.cost_accessories
        return tot if tot > 0 else 1450.0

    @filters_pipes_cost.setter
    def filters_pipes_cost(self, val: float):
        self.cost_piping = float(val)

    @property
    def labor_installation_cost(self) -> float:
        return self.cost_labor if self.cost_labor > 0 else 1500.0

    @labor_installation_cost.setter
    def labor_installation_cost(self, val: float):
        self.cost_labor = float(val)


def parametros_do_nome_do_arquivo(caminho: str) -> Dict[str, float]:
    """Extrai os parâmetros codificados no nome de uma exportação do Netuno 4.

    O Netuno 4 exporta a varredura como uma tabela de volume contra resultado, e
    **não grava parâmetro nenhum dentro do arquivo**. Toda a configuração fica no
    nome, por convenção:

        Florianopolis2_Descarte2_Area100_Consumo100_Pessoas4_Percentual90_Coefs08_Recalque20_5000_500_2.csv

    Antes desta versão, ``parse_netuno_csv`` ignorava o nome e devolvia a
    configuração padrão inteira — área, demanda, coeficiente, descarte, tudo. O
    retorno parecia uma leitura bem-sucedida, e quem montasse uma comparação com
    o Netuno 4 a partir dele rodava com parâmetros que não eram os do arquivo,
    sem qualquer sinal de que algo estava errado.

    Devolve apenas as chaves efetivamente encontradas, para que quem chama possa
    distinguir «não estava no nome» de «era igual ao padrão».
    """
    nome = os.path.basename(caminho)
    achados: Dict[str, float] = {}

    padroes = {
        "discard": r"Descarte(\d+(?:[.,]\d+)?)",
        "area": r"Area(\d+(?:[.,]\d+)?)",
        "demand_value": r"Consumo(\d+(?:[.,]\d+)?)",
        "residents_count": r"Pessoas(\d+)",
        "rainwater_share_pct": r"Percentual(\d+(?:[.,]\d+)?)",
        "runoff_coeff_raw": r"Coefs?(\d+)",
        "pumping_threshold": r"Recalque(\d+(?:[.,]\d+)?)",
    }
    for chave, padrao in padroes.items():
        m = re.search(padrao, nome, re.IGNORECASE)
        if m:
            achados[chave] = float(m.group(1).replace(",", "."))

    # "Coefs08" designa 0,80; "Coefs095", 0,95. O dígito inicial nunca é a
    # unidade, porque um coeficiente de escoamento não passa de 1.
    if "runoff_coeff_raw" in achados:
        bruto = achados.pop("runoff_coeff_raw")
        achados["runoff_coeff"] = bruto / (10.0 ** len(str(int(bruto))))

    if "rainwater_share_pct" in achados:
        achados["rainwater_share"] = achados.pop("rainwater_share_pct") / 100.0

    return achados


def parse_netuno_csv(file_path: str) -> NetunoConfig:
    """Lê uma exportação .csv do Netuno 4 e devolve a configuração correspondente.

    O Netuno 4 grava a configuração **no nome do arquivo**, não no conteúdo, de
    modo que a leitura começa por ali. O que estiver também no corpo do arquivo
    prevalece sobre o nome, porque é mais específico.
    """
    config = NetunoConfig()

    for chave, valor in parametros_do_nome_do_arquivo(file_path).items():
        if hasattr(config, chave):
            atual = getattr(config, chave)
            setattr(config, chave, int(valor) if isinstance(atual, int) else valor)
    
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        
    in_economic = False
    in_results = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
            
        if line.startswith("ANLISE ECONMICA") or line.startswith("ANÁLISE ECONÔMICA"):
            in_economic = True
            continue
        elif line.startswith("RESULTADO DA SIMULAO") or line.startswith("RESULTADO DA SIMULAÇÃO"):
            in_results = True
            continue
            
        parts = [p.strip() for p in line.split(';')]
        key = parts[0]
        
        if not in_economic and not in_results:
            if key.startswith("Arquivo dados"):
                config.precip_file = parts[1] if len(parts) > 1 else ""
            elif key.startswith("Descarte precipitao") or key.startswith("Descarte precipitação"):
                config.discard = parse_float(parts[1], 1.0)
            elif key.startswith("Modo de descarte"):
                config.discard_mode = parse_int(parts[1], 1)
                config.discard_days_interval = parse_int(parts[2] if len(parts) > 2 else "7", 7)
            elif key.startswith("Data inicial"):
                config.start_date = parts[1] if len(parts) > 1 else "01/01/2002"
            elif key.startswith("rea de captao") or key.startswith("Área de captação"):
                config.area = parse_float(parts[1], 100.0)
            elif key.startswith("Demanda de gua total") or key.startswith("Demanda de água total"):
                # Format: Demanda de gua total;0;1;200;
                config.demand_type = parse_int(parts[1], 0)
                config.demand_value = parse_float(parts[3] if len(parts) > 3 else parts[2], 200.0)
            elif key.startswith("Nmero de moradores") or key.startswith("Número de moradores"):
                # Format: Nmero de moradores;0;1;3;
                config.residents_type = parse_int(parts[1], 0)
                config.residents_count = parse_int(parts[3] if len(parts) > 3 else parts[2], 3)
            elif key.startswith("Percentual de gua potvel") or key.startswith("Percentual de água potável"):
                # A linha é percentual, de 0 a 100, como o rótulo diz. Um valor entre
                # 0 e 1 costuma vir de arquivo gravado por versão anterior, que
                # gravava fração; é lido como percentual e assinalado.
                from netuno.core.fracao_atendivel import aviso_percentual_pequeno, percentual_para_fracao
                _pct = parse_float(parts[1], 40.0)
                config.rainwater_share = percentual_para_fracao("Percentual de água potável a ser substituída", _pct)
                _aviso = aviso_percentual_pequeno(_pct)
                if _aviso:
                    import warnings
                    warnings.warn(f"Arquivo de parâmetros: {_aviso}", stacklevel=2)
            elif key.startswith("Coeficiente de escoamento"):
                config.runoff_coeff = parse_float(parts[1], COEFICIENTE_DE_ESCOAMENTO_PADRAO)
            elif key.startswith("Reservatrio superior") or key.startswith("Reservatório superior"):
                # Format: Reservatório superior (litros);500;0 (0 = used/desejado, 1 = not used)
                config.upper_tank_vol = parse_float(parts[1], 500.0)
                mode_code = parse_int(parts[2] if len(parts) > 2 else "0", 0)
                config.upper_tank_used = 1 if (mode_code == 0 and config.upper_tank_vol > 0) else 0

            elif key.startswith("Limiar recalque"):
                config.pumping_threshold = parse_float(parts[1], 375.0)
            elif key.startswith("Reservatrio inferior") or key.startswith("Reservatório inferior"):
                # Format: Reservatrio inferior (litros);10000;250;1
                if len(parts) >= 4:
                    config.lower_tank_max = parse_float(parts[1], 10000.0)
                    config.lower_tank_step = parse_float(parts[2], 250.0)
                    config.lower_tank_mode = parse_int(parts[3], 1)
                elif len(parts) >= 2:
                    config.lower_tank_fixed = parse_float(parts[1], 2000.0)
                    config.lower_tank_mode = 0
            elif key.startswith("Diferena entre potenciais") or key.startswith("Diferença entre potenciais"):
                config.delta_ideal = parse_float(parts[1], 5.0)
                
        elif in_economic and not in_results:
            if key.startswith("Volume do reservatorio inferior") or key.startswith("Volume do reservatório inferior"):
                config.econ_lower_tank_vol = parse_float(parts[1], 2000.0)
            elif key.startswith("Tarifas de agua") or key.startswith("Tarifas de água"):
                num_tariffs = parse_int(parts[1], 0)
                config.water_tariffs = []
                for _ in range(num_tariffs):
                    if i < len(lines):
                        t_line = lines[i].strip().split(';')
                        i += 1
                        if len(t_line) >= 4:
                            # min, max, rate/cost, is_fixed (-1 = fixed, 0 = variable)
                            min_v = parse_float(t_line[0])
                            max_v = parse_float(t_line[1])
                            cost_v = parse_float(t_line[2])
                            is_fix = parse_int(t_line[3])
                            config.water_tariffs.append((min_v, max_v, cost_v, is_fix))
            elif key.startswith("Tarifa esgoto"):
                config.sewage_rate = parse_float(parts[1], 100.0)
                config.sewage_mode = parse_int(parts[2] if len(parts) > 2 else "1", 1)
            elif key.startswith("Imposto agua fixo"):
                config.water_tax_fixed = parse_float(parts[1], 0.0)
            elif key.startswith("Imposto agua variavel"):
                config.water_tax_var = parse_float(parts[1], 0.0)
            elif key.startswith("Inflacao") or key.startswith("Inflação"):
                config.inflation = parse_float(parts[1], 0.2)
            elif key.startswith("Aumento tarifas"):
                config.tariff_escalation = parse_float(parts[1], 12.0)
            elif key.startswith("Periodo de analise") or key.startswith("Período de análise"):
                config.analysis_period_years = parse_int(parts[1], 20)
            elif key.startswith("TMA"):
                config.tma = parse_float(parts[1], 2.0)
            elif key.startswith("Mes de instalacao") or key.startswith("Mês de instalação"):
                config.install_month = parse_int(parts[1], 0)
            elif key == "Reservatorio inferior" or key == "Reservatório inferior":
                config.cost_lower_tank = parse_float(parts[1], 0.0)
            elif key == "Reservatorio superior" or key == "Reservatório superior":
                config.cost_upper_tank = parse_float(parts[1], 0.0)
            elif key.startswith("Mao-de-obra") or key.startswith("Mão-de-obra"):
                config.cost_labor = parse_float(parts[1], 0.0)
            elif key.startswith("Tubulacoes") or key.startswith("Tubulações"):
                config.cost_piping = parse_float(parts[1], 0.0)
            elif key.startswith("Acessorios") or key.startswith("Acessórios"):
                config.cost_accessories = parse_float(parts[1], 0.0)
            elif key.startswith("Quantidade"):
                config.pump_count = parse_int(parts[1], 2)
            elif key.startswith("Potencia") or key.startswith("Potência"):
                config.pump_power_str = parts[1] if len(parts) > 1 else "1/2"
                # Parse power string e.g. "1/2" or float
                if "/" in config.pump_power_str:
                    num, den = config.pump_power_str.split("/")
                    power_cv = float(num) / float(den)
                else:
                    power_cv = parse_float(config.pump_power_str, 0.5)
                # 1 CV = 0.735499 kW
                config.pump_power_kw = power_cv * 0.7355
            elif key.startswith("Rendimento"):
                config.pump_efficiency = parse_float(parts[1], 55.0)
            elif key.startswith("Vazao") or key.startswith("Vazão"):
                config.pump_flow_rate = parse_float(parts[1], 2280.0)
            elif key.startswith("Tempo de partida"):
                config.pump_startup_time_h = parse_float(parts[1], 0.03)
            elif key.startswith("Custo unitario") or key.startswith("Custo unitário"):
                config.pump_unit_cost = parse_float(parts[1], 300.0)
            elif key.startswith("Tarifa energia eletrica") or key.startswith("Tarifa energia elétrica"):
                config.elec_tariff = parse_float(parts[1], 1.0)
            elif key.startswith("Imposto energia fixo"):
                config.elec_tax_fixed = parse_float(parts[1], 0.0)
            elif key.startswith("Imposto energia variavel"):
                config.elec_tax_var = parse_float(parts[1], 0.0)
            elif key.startswith("Custos operacionais"):
                num_op = parse_int(parts[1], 0)
                config.op_costs = []
                for _ in range(num_op):
                    if i < len(lines):
                        op_line = lines[i].strip().split(';')
                        i += 1
                        if len(op_line) >= 4:
                            name = op_line[0]
                            period = parse_int(op_line[1], 1)
                            is_var = parse_int(op_line[2], 0)
                            cost_val = parse_float(op_line[3], 0.0)
                            fix_cost = 0.0 if is_var == 1 else cost_val
                            var_cost = cost_val if is_var == 1 else 0.0
                            config.op_costs.append((name, period, fix_cost, var_cost))
                            
    return config


def format_netuno_float(val: float, decimals: Optional[int] = None) -> str:
    """Formats float with comma decimal separator for Netuno 4.0 CSV format."""
    if val is None:
        return ""
    if decimals is not None:
        formatted = f"{val:.{decimals}f}"
    else:
        # Strip unnecessary trailing zeroes after decimal point if int-like
        formatted = f"{val:g}"
    return formatted.replace('.', ',')


def export_netuno_csv(
    config: NetunoConfig,
    results_by_volume: list,
    file_path: str,
    precip_data: Optional[np.ndarray] = None
) -> str:
    """
    Exports simulation results to a CSV file in 100% exact Netuno 4.0 format.
    """
    lines = []
    
    # 1. Rainfall series (if provided)
    if precip_data is not None and len(precip_data) > 0:
        for val in precip_data:
            lines.append(format_netuno_float(val, 5))
            
    # 2. Config parameters matching Netuno 4.0 format
    lines.append(f"Descarte precipitação;{format_netuno_float(config.discard)}")
    lines.append(f"Modo de descarte;{config.discard_mode};{config.discard_days_interval}")
    lines.append(f"Data inicial;{config.start_date}")
    lines.append(f"Área de captação (m²);{format_netuno_float(config.area)}")
    lines.append(f"Demanda de água total;{config.demand_type};1;{format_netuno_float(config.demand_value)};")
    lines.append(f"Número de moradores;{config.residents_type};1;{config.residents_count};")
    
    # A linha herdada do Netuno 4 diz «percentual», e grava percentual, de 0 a 100.
    from netuno.core.fracao_atendivel import fracao_para_percentual
    rain_share_pct = fracao_para_percentual("rainwater_share", config.rainwater_share)
    lines.append(f"Percentual de água potável a ser substituída por pluvial;{format_netuno_float(rain_share_pct)}")
    lines.append(f"Coeficiente de escoamento superficial;{format_netuno_float(config.runoff_coeff)}")
    
    upper_mode = 0 if (config.upper_tank_used and config.upper_tank_vol > 0) else 1
    lines.append(f"Reservatório superior (litros);{format_netuno_float(config.upper_tank_vol)};{upper_mode}")
    lines.append(f"Limiar recalque (litros);{format_netuno_float(config.pumping_threshold)}")
    lines.append("Observações (linhas);0")

    
    if config.lower_tank_mode == 1:
        lines.append(f"Reservatório inferior (litros);{format_netuno_float(config.lower_tank_max)};{format_netuno_float(config.lower_tank_step)};1")
    else:
        lines.append(f"Reservatório inferior (litros);{format_netuno_float(config.lower_tank_fixed)}")
        
    lines.append(f"Diferença entre potenciais de atendimento pluvial (%/m³);{format_netuno_float(config.delta_ideal)}")
    
    # === ANÁLISE ECONÔMICA ===
    lines.append("")
    lines.append("ANÁLISE ECONÔMICA")
    lines.append(f"Volume do reservatório inferior (litros);{format_netuno_float(config.econ_lower_tank_vol)}")
    lines.append(f"Tarifas de água;{len(config.water_tariffs)}")
    for t in config.water_tariffs:
        lines.append(f"{format_netuno_float(t[0])};{format_netuno_float(t[1])};{format_netuno_float(t[2])};{t[3]}")
    lines.append(f"Tarifa esgoto;{format_netuno_float(config.sewage_rate)};{config.sewage_mode}")
    lines.append(f"Imposto agua fixo;{format_netuno_float(config.water_tax_fixed)}")
    lines.append(f"Imposto agua variavel;{format_netuno_float(config.water_tax_var)}")
    lines.append(f"Inflação;{format_netuno_float(config.inflation)}")
    lines.append(f"Aumento tarifas;{format_netuno_float(config.tariff_escalation)}")
    lines.append(f"Período de análise;{config.analysis_period_years}")
    lines.append(f"TMA;{format_netuno_float(config.tma)}")
    lines.append(f"Mês de instalação;{config.install_month}")
    lines.append(f"Reservatório inferior;{format_netuno_float(config.cost_lower_tank)}")
    lines.append(f"Reservatório superior;{format_netuno_float(config.cost_upper_tank)}")
    lines.append(f"Mão-de-obra;{format_netuno_float(config.cost_labor)}")
    lines.append(f"Tubulações;{format_netuno_float(config.cost_piping)}")
    lines.append(f"Acessórios;{format_netuno_float(config.cost_accessories)}")
    lines.append(f"Quantidade;{config.pump_count}")
    lines.append(f"Potência;{config.pump_power_str}")
    lines.append(f"Rendimento;{format_netuno_float(config.pump_efficiency)}")
    lines.append(f"Vazão;{format_netuno_float(config.pump_flow_rate)}")
    lines.append(f"Tempo de partida;{format_netuno_float(config.pump_startup_time_h)}")
    lines.append(f"Custo unitário;{format_netuno_float(config.pump_unit_cost)}")
    lines.append(f"Tarifa energia elétrica;{format_netuno_float(config.elec_tariff)}")
    lines.append(f"Imposto energia fixo;{format_netuno_float(config.elec_tax_fixed)}")
    lines.append(f"Imposto energia variavel;{format_netuno_float(config.elec_tax_var)}")
    lines.append(f"Custos operacionais;{len(config.op_costs)}")
    for op in config.op_costs:
        is_var = 1 if op[3] > 0 else 0
        val = op[3] if is_var else op[2]
        lines.append(f"{op[0]};{op[1]};{is_var};{format_netuno_float(val)}")

    lines.append("")
    lines.append("RESULTADO DA SIMULAÇÃO")
    lines.append("Reservatório inferior (litros);Potencial de economia (%);Volume consumido médio de água pluvial (litros/dia);Volume consumido médio de água potável (litros/dia);Volume médio de água pluvial extravasado (litros/dia);Dias em que a demanda de água pluvial é atendida completamente;Dias em que a demanda de água pluvial é atendida parcialmente (%);Dias em que a demanda de água pluvial não é atendida (%);Diferença entre potenciais de atendimento pluvial (%/m³)")
    
    for res in results_by_volume:
        tank_v = format_netuno_float(res.lower_tank_vol, 0)
        pot = format_netuno_float(res.potential_potable_savings_pct, 2)
        v_pluv = format_netuno_float(res.avg_pluvial_consumed_l_day, 4)
        v_pot = format_netuno_float(res.avg_potable_consumed_l_day, 0)
        v_spill = format_netuno_float(res.avg_spilled_l_day, 3)
        d_full = format_netuno_float(res.pct_days_full_satisfaction, 2)
        d_part = format_netuno_float(res.pct_days_partial_satisfaction, 2)
        d_none = format_netuno_float(res.pct_days_null_satisfaction, 2)
        delta_str = format_netuno_float(res.delta_potential_per_m3, 2) if hasattr(res, 'delta_potential_per_m3') and res.delta_potential_per_m3 is not None else ""

        
        row_str = f"{tank_v};{pot};{v_pluv};{v_pot};{v_spill};{d_full};{d_part};{d_none};{delta_str}"
        lines.append(row_str)
        
    with open(file_path, 'w', encoding='latin1', errors='replace') as f:
        f.write("\n".join(lines) + "\n")
        
    return file_path


def export_netuno_json(
    config: NetunoConfig,
    file_path: str,
    precip_data: Optional[np.ndarray] = None,
    building_data: Optional[dict] = None,
    global_scenarios: Optional[list] = None,
    ui_state: Optional[dict] = None,
    analysis: Optional[dict] = None,
) -> str:
    """
    Exporta o projeto completo e autocontido do Netuno em JSON (.netuno / .json).
    A série diária de chuva é incorporada ao arquivo; ``ui_state`` preserva os
    controles das etapas para que a interface possa ser reconstituída fielmente.
    """
    import json
    from datetime import datetime

    b_data = building_data or {}
    
    precip_list = precip_data.tolist() if precip_data is not None else []
    
    data = {
        "schema": {"name": "netuno-project", "version": 2},
        "version": __version__,
        "metadata": {
            "project_id": getattr(config, 'project_id', 'N5-PROJ'),
            "name": getattr(config, 'project_name', 'Projeto Netuno'),
            "created_at": getattr(config, 'created_at', datetime.now().strftime("%d/%m/%Y %H:%M")),
            "saved_at": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        },
        "rainfall": {
            "source_mode": getattr(config, 'climate_source_mode', 'national_db'),
            "climate_city_uf": getattr(config, 'climate_city_uf', 'SC'),
            "climate_city_name": getattr(config, 'climate_city_name', 'Florianópolis'),
            "climate_model": getattr(config, 'climate_model', 'ACCESS-CM2'),
            "climate_scenario": getattr(config, 'climate_scenario', 'HIST'),
            "climate_start_date": getattr(config, 'climate_start_date', '01/01/1980'),
            "climate_end_date": getattr(config, 'climate_end_date', '31/12/2014'),
            "file_name": getattr(config, 'precip_file', ''),
            "start_date": getattr(config, 'start_date', '01/01/1980'),
            "total_days": len(precip_list),
            "precipitation_mm": precip_list
        },
        "inputs": {
            "building_and_demand": {
                "catchment_area_m2": b_data.get("area", config.area),
                "runoff_coeff": b_data.get("runoff", b_data.get("runoff_coeff", config.runoff_coeff)),
                "residents_count": b_data.get("residents", config.residents_count),
                "residents_type": config.residents_type,
                "residents_monthly": b_data.get("monthly_residents", config.residents_monthly),
                "demand_value": b_data.get("demand", config.demand_value),
                "demand_type": config.demand_type,
                "demand_monthly": b_data.get("monthly_demands", config.demand_monthly),
                "use_variable": b_data.get("use_variable", False),
                "rainwater_share": b_data.get("share", config.rainwater_share)
            },
            # A modulacao por calendario. Ate a 5.0.8 estas sete listas
            # existiam na configuracao e nenhuma era gravada: um projeto
            # semanal ou diario reabria como constante, sem aviso. A lista
            # mensal de demanda fica na secao acima, por compatibilidade com
            # os arquivos ja gravados.
            "demand_modulation": {
                "demand_mode": b_data.get("demand_mode", getattr(config, "demand_mode", "constant")),
                "weekly_demands": b_data.get("weekly_demands") or list(getattr(config, "weekly_demands", [])),
                "weekly_residents": b_data.get("weekly_residents") or list(getattr(config, "weekly_residents", [])),
                "weekly_shares": b_data.get("weekly_shares") or list(getattr(config, "weekly_shares", [])),
                "monthly_shares": b_data.get("monthly_shares") or list(getattr(config, "monthly_shares", [])),
                "daily_demands": b_data.get("daily_demands") or list(getattr(config, "daily_demands", [])),
                "daily_residents": b_data.get("daily_residents") or list(getattr(config, "daily_residents", [])),
                "daily_shares": b_data.get("daily_shares") or list(getattr(config, "daily_shares", [])),
            },
            "rainfall_discard": {
                "discard_mm": b_data.get("discard", config.discard),
                "discard_mode": config.discard_mode,
                "discard_days_interval": config.discard_days_interval
            },
            "reservoirs_and_pumping": {
                "lower_tank_fixed_l": config.lower_tank_fixed,
                "lower_tank_max_l": config.lower_tank_max,
                "lower_tank_step_l": config.lower_tank_step,
                "lower_tank_mode": config.lower_tank_mode,
                "delta_ideal_pct": config.delta_ideal,
                "upper_tank_vol_l": config.upper_tank_vol,
                "upper_tank_used": bool(config.upper_tank_used),
                "pumping_threshold_l": config.pumping_threshold,
                "pump": {
                    "count": config.pump_count,
                    "power_str": config.pump_power_str,
                    "power_kw": config.pump_power_kw,
                    "flow_rate_l_h": config.pump_flow_rate,
                    "efficiency_pct": config.pump_efficiency,
                    "startup_time_h": config.pump_startup_time_h,
                    "motor_efficiency": getattr(config, "pump_motor_efficiency", 0.0),
                    "unit_cost": config.pump_unit_cost,
                    # Saida do assistente de motobomba. Zero significa "nao informada",
                    # e sem ela o calculo de energia volta a usar a altura de recurso.
                    "manometric_head_m": getattr(config, "pump_manometric_head_m", 0.0)
                }
            },
            "financial_and_economic": {
                "analysis_period_years": config.analysis_period_years,
                "tma_monthly_pct": config.tma,
                "inflation_monthly_pct": config.inflation,
                "sewage_mode": config.sewage_mode,
                "sewage_rate_pct": config.sewage_rate,
                "water_tax_fixed": config.water_tax_fixed,
                "water_tax_var_pct": config.water_tax_var,
                "water_tariffs": config.water_tariffs,
                "tariff_city_uf": getattr(config, 'tariff_city_uf', 'SC'),
                "tariff_city_name": getattr(config, 'tariff_city_name', 'Florianópolis'),
                "elec_city_uf": getattr(config, 'elec_city_uf', 'SC'),
                "elec_city_name": getattr(config, 'elec_city_name', 'Florianópolis'),
                "tariff_escalation_months": config.tariff_escalation,
                "water_tariff_escalation_pct": getattr(config, 'water_tariff_escalation', 5.0),
                "sewage_tariff_escalation_pct": getattr(config, 'sewage_tariff_escalation', 5.0),
                "elec_tariff": config.elec_tariff,
                "elec_tax_fixed": config.elec_tax_fixed,
                "elec_tax_var_pct": config.elec_tax_var,
                "elec_tariff_escalation_pct": getattr(config, 'elec_tariff_escalation', 5.0)
            },
            # Secoes que faltavam. Ate a 5.0.8 o arquivo gravava seis secoes e
            # trinta campos ficavam de fora, voltando ao padrao em silencio ao
            # reabrir: quem salvasse um estudo com ozonio, 30 m de desnivel e
            # cisterna de concreto reabria outro, com cloracao, altura zero e PEAD.
            "water_quality_and_etap": {
                "target_class": getattr(config, "water_quality_target_class", "classe_1"),
                "disinfection": getattr(config, "water_quality_disinfection", "cloro"),
                "polishing_filter": bool(getattr(config, "water_quality_polishing", False)),
                "first_flush_system_enabled": bool(getattr(config, "first_flush_system_enabled", False)),
                "etap_enabled": bool(getattr(config, "etap_enabled", True)),
                "chlorine_treatment_enabled": bool(getattr(config, "chlorine_treatment_enabled", True)),
                "chlorine_dose_mg_l": getattr(config, "chlorine_dose_mg_l", 1.5),
                "chlorine_product_purity": getattr(config, "chlorine_product_purity", 0.65),
                "chlorine_cost_per_kg": getattr(config, "chlorine_cost_per_kg", 25.0),
                "chlorine_co2_kg_per_kg": getattr(config, "chlorine_co2_kg_per_kg", 1.85),
            },
            "materials_and_typology": {
                "building_template_id": getattr(config, "building_template_id", "res_medio"),
                "lower_tank_material": getattr(config, "lower_tank_material", "PEAD"),
                "upper_tank_material": getattr(config, "upper_tank_material", "PEAD"),
            },
            "irrigation": {
                "garden_area_m2": getattr(config, "irrigation_garden_area_m2", 0.0),
                "rate_l_m2_day": getattr(config, "irrigation_rate_l_m2_day", 3.0),
                "liters_per_day": getattr(config, "irrigation_liters_per_day", 50.0),
                "rain_threshold_mm": getattr(config, "irrigation_rain_threshold_mm", 2.0),
                "potable_backup": bool(getattr(config, "irrigation_potable_backup", True)),
            },
            "incentives_and_shares": {
                "iptu_green_enabled": bool(getattr(config, "iptu_green_enabled", False)),
                "iptu_annual_value": getattr(config, "iptu_annual_value", 4000.0),
                "iptu_discount_pct": getattr(config, "iptu_discount_pct", 5.0),
                "tariff_flag": getattr(config, "tariff_flag", "verde"),
                "tariff_customized": bool(getattr(config, "tariff_customized", False)),
                "num_economias": getattr(config, "num_economias", 1),
                "potable_indoor_share": getattr(config, "potable_indoor_share", 0.65),
                "non_potable_indoor_share": getattr(config, "non_potable_indoor_share", 0.35),
                "install_month": getattr(config, "install_month", 0),
                "econ_lower_tank_vol": getattr(config, "econ_lower_tank_vol", 2000.0),
                "demand_mode": getattr(config, "demand_mode", "constant"),
                "edge_base_case_l_person_day": getattr(
                    config, "edge_base_case_l_person_day", 0.0),
            },
            "capex_and_opex": {
                "cost_lower_tank": config.cost_lower_tank,
                "cost_upper_tank": config.cost_upper_tank,
                "cost_labor": config.cost_labor,
                "cost_piping": config.cost_piping,
                "cost_accessories": config.cost_accessories,
                "operational_costs": config.op_costs
            },
            "global_optimizer_scenarios": global_scenarios or []
        },
        "ui_state": ui_state or {},
        # Bloco aberto para CLI, automações e futuras extensões; a GUI pode
        # ignorá-lo com segurança quando não houver campos reconhecidos.
        "analysis": analysis or {},
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return file_path


class FormatoDeProjetoDesconhecido(ValueError):
    """O arquivo e JSON, mas nao e um projeto do Netuno.

    Existe para que o erro suba com nome proprio, em vez de ser confundido com
    um JSON truncado — que e o outro motivo de falha na abertura.
    """

def load_netuno_project(file_path: str) -> dict:
    """
    Carrega um projeto Netuno a partir de um arquivo JSON (.netuno / .json)
    ou CSV (legado Netuno 4.0/5.0 ou chuva simples).
    Retorna um dicionário estruturado pronto para sincronizar a interface.
    """
    import json
    import os

    res = {
        "config": NetunoConfig(),
        "precip_data": None,
        "precip_filename": os.path.basename(file_path),
        "building_data": {},
        "global_scenarios": [],
        "ui_state": {},
        "analysis": {},
        "is_json": False
    }

    # Tenta ler como JSON primeiro
    if file_path.lower().endswith('.netuno') or file_path.lower().endswith('.json'):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            res["is_json"] = True
            meta = data.get("metadata", {})
            rainfall = data.get("rainfall", {})
            inputs = data.get("inputs", {})

            # Um JSON que nao traz nenhuma das secoes do projeto nao e um
            # projeto do Netuno. Ate a 5.0.8 ele era aceito e devolvia a
            # configuracao padrao inteira, de modo que o estudo aberto nao era
            # o estudo do arquivo — e nada avisava.
            if not inputs and not rainfall and "schema" not in data:
                raise FormatoDeProjetoDesconhecido(
                    f"O arquivo '{os.path.basename(file_path)}' e um JSON valido, "
                    "mas nao tem as secoes de um projeto do Netuno "
                    "('schema', 'rainfall', 'inputs'). Se ele veio de uma versao "
                    "antiga ou de outro programa, converta-o antes de abrir: "
                    "abrir assim carregaria um projeto padrao com o nome deste "
                    "arquivo."
                )

            cfg = NetunoConfig()
            cfg.project_id = meta.get("project_id", "N5-PROJ")
            cfg.project_name = meta.get("name", "Projeto Netuno")
            cfg.created_at = meta.get("created_at", "")
            cfg.precip_file = rainfall.get("file_name", os.path.basename(file_path))
            cfg.start_date = rainfall.get("start_date", "01/01/1980")
            cfg.climate_source_mode = rainfall.get("source_mode", "national_db")
            cfg.climate_city_uf = rainfall.get("climate_city_uf", "SC")
            cfg.climate_city_name = rainfall.get("climate_city_name", "Florianópolis")
            cfg.climate_model = rainfall.get("climate_model", "ACCESS-CM2")
            cfg.climate_scenario = rainfall.get("climate_scenario", "HIST")
            cfg.climate_start_date = rainfall.get("climate_start_date", "01/01/1980")
            cfg.climate_end_date = rainfall.get("climate_end_date", "31/12/2014")

            # Precipitação
            p_list = rainfall.get("precipitation_mm", [])
            if p_list:
                res["precip_data"] = np.array(p_list, dtype=np.float64)

            # Building & Demand
            b = inputs.get("building_and_demand", {})
            cfg.area = b.get("catchment_area_m2", 100.0)
            cfg.runoff_coeff = b.get("runoff_coeff", COEFICIENTE_DE_ESCOAMENTO_PADRAO)
            cfg.residents_count = b.get("residents_count", 3)
            cfg.residents_type = b.get("residents_type", 0)
            cfg.residents_monthly = b.get("residents_monthly", [])
            cfg.demand_value = b.get("demand_value", 200.0)
            cfg.demand_type = b.get("demand_type", 0)
            cfg.demand_monthly = b.get("demand_monthly", [])
            cfg.residents_monthly = b.get("residents_monthly", cfg.residents_monthly)
            cfg.rainwater_share = b.get("rainwater_share", 0.4)
            cfg.potable_indoor_share = b.get("potable_indoor_share", 0.65)
            cfg.non_potable_indoor_share = b.get("non_potable_indoor_share", 0.35)
            cfg.irrigation_liters_per_day = b.get("irrigation_liters_per_day", 50.0)
            cfg.irrigation_rain_threshold_mm = b.get("irrigation_rain_threshold_mm", 2.0)
            cfg.irrigation_potable_backup = b.get("irrigation_potable_backup", True)
            cfg.irrigation_garden_area_m2 = b.get("irrigation_garden_area_m2", 0.0)
            cfg.irrigation_rate_l_m2_day = b.get("irrigation_rate_l_m2_day", 3.0)

            # Rainfall Discard
            rd = inputs.get("rainfall_discard", {})
            cfg.discard = rd.get("discard_mm", 1.0)
            cfg.discard_mode = rd.get("discard_mode", 1)
            cfg.discard_days_interval = rd.get("discard_days_interval", 7)

            # Reservoirs & Pumping
            rp = inputs.get("reservoirs_and_pumping", {})
            cfg.lower_tank_fixed = rp.get("lower_tank_fixed_l", 2000.0)
            cfg.lower_tank_max = rp.get("lower_tank_max_l", 10000.0)
            cfg.lower_tank_step = rp.get("lower_tank_step_l", 250.0)
            cfg.lower_tank_mode = rp.get("lower_tank_mode", 1)
            cfg.delta_ideal = rp.get("delta_ideal_pct", 5.0)
            cfg.upper_tank_vol = rp.get("upper_tank_vol_l", 500.0)
            cfg.upper_tank_used = 1 if rp.get("upper_tank_used", True) else 0
            cfg.pumping_threshold = rp.get("pumping_threshold_l", 375.0)

            pump = rp.get("pump", {})
            cfg.pump_count = pump.get("count", 2)
            cfg.pump_power_str = pump.get("power_str", "1/2 CV")
            cfg.pump_power_kw = pump.get("power_kw", 0.368)
            cfg.pump_flow_rate = pump.get("flow_rate_l_h", 2280.0)
            cfg.pump_efficiency = pump.get("efficiency_pct", 55.0)
            cfg.pump_startup_time_h = pump.get("startup_time_h", 0.03)
            cfg.pump_motor_efficiency = pump.get(
                "motor_efficiency", cfg.pump_motor_efficiency)
            cfg.pump_unit_cost = pump.get("unit_cost", 320.0)
            # Zero significa «não informada»: é o que faz a precedência do
            # cálculo de energia funcionar. Sem persistir, o desnível levantado
            # pelo assistente se perdia ao reabrir o projeto.
            cfg.pump_manometric_head_m = pump.get("manometric_head_m", 0.0)

            # Financial & Economic
            fe = inputs.get("financial_and_economic", {})
            cfg.analysis_period_years = fe.get("analysis_period_years", 20)
            cfg.tma = fe.get("tma_monthly_pct", 0.5)
            cfg.inflation = fe.get("inflation_monthly_pct", 0.2)
            cfg.sewage_mode = fe.get("sewage_mode", 1)
            cfg.sewage_rate = fe.get("sewage_rate_pct", 100.0)
            cfg.water_tax_fixed = fe.get("water_tax_fixed", 0.0)
            cfg.water_tax_var = fe.get("water_tax_var_pct", 0.0)
            cfg.water_tariffs = fe.get("water_tariffs", cfg.water_tariffs)
            cfg.tariff_city_uf = fe.get("tariff_city_uf", getattr(cfg, "tariff_city_uf", "SC"))
            cfg.tariff_city_name = fe.get("tariff_city_name", getattr(cfg, "tariff_city_name", "Florianópolis"))
            cfg.elec_city_uf = fe.get("elec_city_uf", getattr(cfg, "elec_city_uf", "SC"))
            cfg.elec_city_name = fe.get("elec_city_name", getattr(cfg, "elec_city_name", "Florianópolis"))
            cfg.tariff_escalation = fe.get("tariff_escalation_months", 12)
            cfg.water_tariff_escalation = fe.get("water_tariff_escalation_pct", 5.0)
            cfg.sewage_tariff_escalation = fe.get("sewage_tariff_escalation_pct", 5.0)
            cfg.elec_tariff = fe.get("elec_tariff", 1.0)
            cfg.elec_tax_fixed = fe.get("elec_tax_fixed", 0.0)
            cfg.elec_tax_var = fe.get("elec_tax_var_pct", 0.0)
            cfg.elec_tariff_escalation = fe.get("elec_tariff_escalation_pct", 5.0)

            # CAPEX & OPEX
            co = inputs.get("capex_and_opex", {})
            cfg.cost_lower_tank = co.get("cost_lower_tank", 2500.0)
            cfg.cost_upper_tank = co.get("cost_upper_tank", 380.0)
            cfg.cost_labor = co.get("cost_labor", 1500.0)
            cfg.cost_piping = co.get("cost_piping", 950.0)
            cfg.cost_accessories = co.get("cost_accessories", 500.0)

            # Secoes acrescentadas na 5.0.8. `get` com o padrao mantem os arquivos
            # anteriores legiveis: o que nao existir no arquivo cai no padrao, que
            # e o comportamento que eles ja tinham.
            wq = inputs.get("water_quality_and_etap", {})
            cfg.water_quality_target_class = wq.get("target_class", "classe_1")
            cfg.water_quality_disinfection = wq.get("disinfection", "cloro")
            cfg.water_quality_polishing = bool(wq.get("polishing_filter", False))
            cfg.first_flush_system_enabled = bool(wq.get("first_flush_system_enabled", False))
            cfg.etap_enabled = bool(wq.get("etap_enabled", True))
            cfg.chlorine_treatment_enabled = bool(wq.get("chlorine_treatment_enabled", True))
            cfg.chlorine_dose_mg_l = wq.get("chlorine_dose_mg_l", cfg.chlorine_dose_mg_l)
            cfg.chlorine_product_purity = wq.get("chlorine_product_purity", cfg.chlorine_product_purity)
            cfg.chlorine_cost_per_kg = wq.get("chlorine_cost_per_kg", cfg.chlorine_cost_per_kg)
            cfg.chlorine_co2_kg_per_kg = wq.get("chlorine_co2_kg_per_kg", cfg.chlorine_co2_kg_per_kg)

            mt = inputs.get("materials_and_typology", {})
            cfg.building_template_id = mt.get("building_template_id", "res_medio")
            cfg.lower_tank_material = mt.get("lower_tank_material", "PEAD")
            cfg.upper_tank_material = mt.get("upper_tank_material", "PEAD")

            ir = inputs.get("irrigation", {})
            cfg.irrigation_garden_area_m2 = ir.get("garden_area_m2", cfg.irrigation_garden_area_m2)
            cfg.irrigation_rate_l_m2_day = ir.get("rate_l_m2_day", cfg.irrigation_rate_l_m2_day)
            cfg.irrigation_liters_per_day = ir.get("liters_per_day", cfg.irrigation_liters_per_day)
            cfg.irrigation_rain_threshold_mm = ir.get("rain_threshold_mm", cfg.irrigation_rain_threshold_mm)
            cfg.irrigation_potable_backup = bool(ir.get("potable_backup", True))

            inc = inputs.get("incentives_and_shares", {})
            cfg.iptu_green_enabled = bool(inc.get("iptu_green_enabled", False))
            cfg.iptu_annual_value = inc.get("iptu_annual_value", cfg.iptu_annual_value)
            cfg.iptu_discount_pct = inc.get("iptu_discount_pct", cfg.iptu_discount_pct)
            cfg.tariff_flag = inc.get("tariff_flag", "verde")
            cfg.tariff_customized = bool(inc.get("tariff_customized", False))
            cfg.num_economias = inc.get("num_economias", cfg.num_economias)
            cfg.potable_indoor_share = inc.get("potable_indoor_share", cfg.potable_indoor_share)
            cfg.non_potable_indoor_share = inc.get("non_potable_indoor_share", cfg.non_potable_indoor_share)
            cfg.install_month = inc.get("install_month", cfg.install_month)
            cfg.econ_lower_tank_vol = inc.get("econ_lower_tank_vol", cfg.econ_lower_tank_vol)
            cfg.demand_mode = inc.get("demand_mode", cfg.demand_mode)
            cfg.edge_base_case_l_person_day = inc.get(
                "edge_base_case_l_person_day", cfg.edge_base_case_l_person_day)
            if "operational_costs" in co:
                cfg.op_costs = [tuple(item) for item in co["operational_costs"]]

            res["config"] = cfg
            # O projeto JSON já contém a chuva: o nome é apenas referência
            # visual e nunca é tratado como uma dependência externa.
            res["precip_filename"] = cfg.precip_file or os.path.basename(file_path)
            res["building_data"] = {
                "area": cfg.area,
                "demand": cfg.demand_value,
                "residents": cfg.residents_count,
                "share": cfg.rainwater_share,
                "runoff_coeff": cfg.runoff_coeff,
                "discard": cfg.discard,
                "use_variable": b.get("use_variable", False),
                "monthly_demands": cfg.demand_monthly,
                "monthly_residents": cfg.residents_monthly,
                "potable_indoor_share": cfg.potable_indoor_share,
                "non_potable_indoor_share": cfg.non_potable_indoor_share,
                "irrigation_liters_per_day": cfg.irrigation_liters_per_day,
                "irrigation_rain_threshold_mm": cfg.irrigation_rain_threshold_mm,
                "irrigation_potable_backup": cfg.irrigation_potable_backup,
                "irrigation_garden_area_m2": cfg.irrigation_garden_area_m2,
                "irrigation_rate_l_m2_day": cfg.irrigation_rate_l_m2_day,
            }
            mod = inputs.get("demand_modulation", {})
            if mod:
                cfg.demand_mode = mod.get("demand_mode", cfg.demand_mode)
                cfg.weekly_demands = list(mod.get("weekly_demands", []) or [])
                cfg.weekly_residents = list(mod.get("weekly_residents", []) or [])
                cfg.weekly_shares = list(mod.get("weekly_shares", []) or [])
                cfg.monthly_shares = list(mod.get("monthly_shares", []) or [])
                cfg.daily_demands = list(mod.get("daily_demands", []) or [])
                cfg.daily_residents = list(mod.get("daily_residents", []) or [])
                cfg.daily_shares = list(mod.get("daily_shares", []) or [])
            res["building_data"].update({
                "demand_mode": cfg.demand_mode,
                "weekly_demands": cfg.weekly_demands,
                "weekly_residents": cfg.weekly_residents,
                "weekly_shares": cfg.weekly_shares,
                "monthly_shares": cfg.monthly_shares,
                "daily_demands": cfg.daily_demands,
                "daily_residents": cfg.daily_residents,
                "daily_shares": cfg.daily_shares,
            })
            res["global_scenarios"] = inputs.get("global_optimizer_scenarios", [])
            res["ui_state"] = data.get("ui_state", {})
            res["analysis"] = data.get("analysis", {})
            return res
        except FormatoDeProjetoDesconhecido:
            raise
        except Exception:
            pass

    # Fallback para leitor de chuva / CSV tradicional
    try:
        precip = load_precipitation(file_path)
        res["precip_data"] = precip
    except Exception:
        pass

    try:
        cfg = parse_netuno_csv(file_path)
        res["config"] = cfg
        res["building_data"] = {
            "area": cfg.area,
            "demand": cfg.demand_value,
            "residents": cfg.residents_count,
            "share": cfg.rainwater_share,
            "runoff_coeff": cfg.runoff_coeff,
            "discard": cfg.discard
        }
    except Exception:
        pass

    return res
