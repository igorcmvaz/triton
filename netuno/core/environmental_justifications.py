"""
Módulo de Justificativas e Tooltips para Análise Ambiental (ACV).
Fornece justificativas detalhadas, referências bibliográficas e explicações
para cada definição de parâmetro ambiental, integrado com o sistema de tooltips da UI.
"""

from dataclasses import dataclass, replace
from typing import Dict, Optional

from netuno.core.environmental import (
    MATERIAL_PRESETS,
    PIPE_EMISSION_FACTORS_PER_METER,
    PUMP_EMBEDDED_CO2,
)
from netuno.core.parser import format_ptbr


@dataclass
class ParameterJustification:
    """
    Encapsula uma justificativa completa e estruturada para um parâmetro ambiental.
    """
    title: str                          # Título curto do parâmetro
    short_description: str              # Descrição breve (1-2 linhas)
    detailed_explanation: str           # Explicação detalhada do cálculo/escolha
    source_reference: str               # Referência bibliográfica completa
    calculation_basis: str              # Base do cálculo ou inferência
    notes: Optional[str] = None         # Notas adicionais relevantes


# ── JUSTIFICATIVAS PARA PRESETS DE MATERIAIS ──
MATERIAL_JUSTIFICATIONS: Dict[str, Dict[str, ParameterJustification]] = {
    "PEAD": {
        "density": ParameterJustification(
            title="Densidade do PEAD para Cisterna",
            short_description="Polietileno de Alta Densidade rotomoldado",
            detailed_explanation=(
                "Cisternas pré-fabricadas em PEAD requerem ~22 kg de material por m³ útil.\n"
                "Essa densidade considera a espessura otimizada das paredes (8-12 mm) para "
                "resistência mecânica e testes de pressão interna, sem excesso de material."
            ),
            source_reference="Cenário interno: substituir pela massa da ficha técnica do reservatório",
            calculation_basis="Peso médio de cisternas comerciais 5000L ÷ 5m³ = 22 kg/m³",
            notes="Valores podem variar de 18-25 kg/m³ conforme especificação do fabricante."
        ),
        "co2_factor": ParameterJustification(
            title="Fator de Emissão de CO2e do PEAD",
            short_description="3,0 kg CO2e por kg de material processado",
            detailed_explanation=(
                "O fator de 3,0 kg CO2e/kg reflete toda a pegada de carbono da produção do PEAD:\n"
                "• Extração e refino de petróleo bruto (~1,5 kg CO2e/kg)\n"
                "• Polimerização e processamento químico (~1,0 kg CO2e/kg)\n"
                "• Transporte industrial (~0,5 kg CO2e/kg)\n\n"
                "A decomposição é apenas o racional histórico do cenário interno. O fator não foi "
                "auditado contra uma EPD ou processo versionado nesta distribuição."
            ),
            source_reference="Cenário interno: selecionar EPD/inventário versionado do PEAD adotado",
            calculation_basis="Life Cycle Assessment (LCA) de produção PEAD virgin",
            notes=(
                "Valores com reciclagem podem ser 30-50% menores (~1,5-2,1 kg CO2e/kg).\n"
                "Este projeto usa material virgin por conservadorismo."
            )
        )
    },
    "CONCRETO": {
        "density": ParameterJustification(
            title="Densidade do Concreto Armado C-30",
            short_description="~0,50 m³ de concreto armado por m³ útil de reservatório",
            detailed_explanation=(
                "Um reservatório de 5 m³ não é cheio de concreto: ele é um casco estrutural vazado.\n"
                "Para uma cisterna de 5 m³, as paredes de concreto armado de 120-150 mm e a laje de base "
                "de 120 mm consomem apenas cerca de 0,45-0,55 m³ de concreto, ou ~10-11% do volume útil.\n"
                "Este cálculo considera uma geometria típica de cisterna retangular com parede perimetral, "
                "fundação e revestimento interno impermeável, mas não o volume de água armazenada.\n"
                "Usando densidade do concreto C-30 (~2400 kg/m³) e armadura de 50-80 kg por m³ útil, "
                "obtém-se ~1200 kg de material por m³ útil de reservatório."
            ),
            source_reference="Cenário geométrico interno: dimensionar a estrutura e quantificar concreto/aço",
            calculation_basis="Cálculo de volume de parede + laje de base + armadura para cisterna de 5 m³.",
            notes=(
                "O reservatório é basicamente um invólucro vazado. As paredes finas e a laje de base são "
                "que efetivamente formam a estrutura, não o preenchimento com concreto maciço."
            )
        ),
        "co2_factor": ParameterJustification(
            title="Fator de Emissão de CO2e do Concreto Armado",
            short_description="0,14 kg CO2e por kg de concreto (incluindo armadura)",
            detailed_explanation=(
                "A emissão de CO2e do concreto armado é dominada pelo cimento Portland (CP-II):\n"
                "• Cimento (80% da pegada): ~0,126 kg CO2e/kg\n"
                "• Aço de armadura (20%): ~0,014 kg CO2e/kg\n"
                "• Agregados e água: negligenciáveis\n\n"
                "Concreto com CP-II (pozolânico, menos intenso em carbono que CP-I) é escolhido.\n"
                "Valor final integrado: 0,14 kg CO2e/kg da mistura total."
            ),
            source_reference="Cenário interno: aplicar EPDs do concreto e do aço com quantitativos do projeto",
            calculation_basis="Pegada de cimento CP-II + Aço ABNT NBR 6152",
            notes=(
                "Concreto com cinza volante reduz a 0,09-0,11 kg CO2e/kg (30-40% menos).\n"
                "Este projeto usa CP-II por disponibilidade regional."
            )
        )
    },
    "FIBRA": {
        "density": ParameterJustification(
            title="Densidade do PRFV (Poliéster + Fibra de Vidro)",
            short_description="~20 kg de material composto por m³ útil",
            detailed_explanation=(
                "Cisternas em PRFV (Poliéster Reforçado com Fibra de Vidro) são mais leves que "
                "concreto mas mais densas que PEAD puro, devido à fibra de vidro estrutural.\n"
                "Composição típica: 70% resina poliéster (~15 kg) + 30% fibra vidro (~5 kg) = ~20 kg/m³"
            ),
            source_reference="Cenário interno: substituir pela massa da ficha técnica do reservatório PRFV",
            calculation_basis="Razão fibra:resina em projetos de cisternas comerciais",
            notes="Varia de 18-24 kg/m³ conforme processo de fabricação (hand-lay-up vs infusão)."
        ),
        "co2_factor": ParameterJustification(
            title="Fator de Emissão de CO2e do PRFV",
            short_description="4,25 kg CO2e por kg de composto",
            detailed_explanation=(
                "A pegada do PRFV é dominada pela resina poliéster + solventes de fabricação:\n"
                "• Resina poliéster insaturada: ~4,5 kg CO2e/kg\n"
                "• Fibra de vidro: ~2,5 kg CO2e/kg\n"
                "• Solventes e processamento: ~1,2 kg CO2e/kg\n\n"
                "Média ponderada: 0,70 × 4,5 + 0,30 × 2,5 = ~4,0 kg CO2e/kg (ajustado para 4,25 kg CO2e/kg"
                " considerando desperdícios de processamento)."
            ),
            source_reference="Cenário interno: selecionar EPD/inventário versionado do compósito adotado",
            calculation_basis="LCA de composição típica PRFV hand-lay-up",
            notes="PRFV com resina epóxi ecológica pode reduzir a ~2,8-3,2 kg CO2e/kg."
        )
    },
    "ACO_INOX": {
        "density": ParameterJustification(
            title="Densidade do Aço Inoxidável AISI 304/316",
            short_description="~38 kg de aço por m³ útil de reservatório",
            detailed_explanation=(
                "Cisternas em aço inox usam chapas de 2-3 mm soldadas, gerando ~38 kg por m³ útil.\n"
                "Composição típica AISI 304: Fe 70%, Cr 18%, Ni 10%, Mo 2% = densidade específica ~7,8 kg/dm³\n"
                "Volume de aço necessário: 38 kg ÷ 7,8 kg/dm³ ≈ 4,8 dm³/m³ (aprovisionamento ~5%)."
            ),
            source_reference="Cenário geométrico interno: substituir pela massa da ficha técnica do tanque",
            calculation_basis="Massa de chapas + soldas em projeto típico de cisterna inox",
            notes="Pode variar de 32-45 kg/m³ conforme espessura de parede e design (cilíndrico, quadrado)."
        ),
        "co2_factor": ParameterJustification(
            title="Fator de Emissão de CO2e do Aço Inoxidável",
            short_description="2,89 kg CO2e por kg de aço inox AISI 304",
            detailed_explanation=(
                "A pegada do aço inox é alta comparada ao aço carbono (0,7-0,9 kg CO2e/kg) "
                "devido ao alto teor de Cromo e Níquel:\n"
                "• Minério e sinterização: ~1,0 kg CO2e/kg\n"
                "• Fusão em forno elétrico de arco (EAF): ~1,2 kg CO2e/kg\n"
                "• Redução de Cr/Ni e refino: ~0,6 kg CO2e/kg\n"
                "• Laminação e acabamento: ~0,09 kg CO2e/kg\n\n"
                "Total: ~2,89 kg CO2e/kg (AISI 304 primary route)."
            ),
            source_reference="Cenário interno: selecionar EPD do aço com teor reciclado e rota declarados",
            calculation_basis="Life Cycle Inventory de produção aço inox AISI 304 (EAF)",
            notes=(
                "Uso de aço inox reciclado reduz para ~1,5-1,8 kg CO2e/kg.\n"
                "Este projeto assume produção primária (95% reciclabilidade ao final de vida)."
            )
        )
    }
}


# ── JUSTIFICATIVAS PARA TUBULAÇÕES PVC ──
PIPE_JUSTIFICATIONS: Dict[int, ParameterJustification] = {
    50: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 50 mm (2\")",
        short_description="1,54 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 50 mm contém ~0,55 kg de material PVC por metro.\n"
            "Considerando fator de emissão do PVC = 2,80 kg CO2e/kg:\n"
            "  0,55 kg × 2,80 kg CO2e/kg = 1,54 kg CO2e/m\n\n"
            "Este é o tubo mais fino do padrão, usado para linhas de recirculação e drenos."
        ),
        source_reference="Cenário interno: massa linear × fator do PVC; substituir por ficha técnica/EPD",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Inclui cimento PVC (5-10% das dimensões do tubo) e aditivos estabilizadores."
    ),
    75: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 75 mm (3\")",
        short_description="2,66 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 75 mm contém ~0,95 kg de material PVC por metro.\n"
            "Cálculo: 0,95 kg × 2,80 kg CO2e/kg = 2,66 kg CO2e/m\n\n"
            "Diâmetro intermediário, tipicamente usado para distribuição principal "
            "e interconexões entre cisterna e caixa superior."
        ),
        source_reference="Cenário interno: massa linear × fator do PVC; substituir por ficha técnica/EPD",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Tubo Schedule 40 com pressão nominal 100 psi (padrão sistemas de aproveitamento)."
    ),
    100: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 100 mm (4\")",
        short_description="3,92 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 100 mm contém ~1,40 kg de material PVC por metro.\n"
            "Cálculo: 1,40 kg × 2,80 kg CO2e/kg = 3,92 kg CO2e/m\n\n"
            "Tubo de maior seção, usado para linhas de grande vazão, "
            "captação principal e alimentação de cisterna."
        ),
        source_reference="Cenário interno: massa linear × fator do PVC; substituir por ficha técnica/EPD",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Mais econômico para grandes vazões que múltiplas linhas menores."
    ),
    150: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 150 mm (6\")",
        short_description="7,84 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 150 mm contém ~2,80 kg de material PVC por metro.\n"
            "Cálculo: 2,80 kg × 2,80 kg CO2e/kg = 7,84 kg CO2e/m\n\n"
            "Tubo de maior seção do catálogo padrão, usado em coletas de grande escala "
            "ou quando a velocidade de fluxo deve ser minimizada (reduz perdas)."
        ),
        source_reference="Cenário interno: massa linear × fator do PVC; substituir por ficha técnica/EPD",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Próximo limite de aplicação em sistemas residenciais/comerciais de médio porte."
    )
}


# ── JUSTIFICATIVAS PARA MOTOBOMBAS ──
PUMP_JUSTIFICATIONS: Dict[float, ParameterJustification] = {
    0.25: ParameterJustification(
        title="Emissão Incorporada - Motobomba 0,25 CV",
        short_description="~12 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 1/4 CV em desenho típico (motor mono/trifásico + corpo ferro fundido + selo mecânico):\n"
            "• Motor elétrico (bobinagem Cu + Alumínio): ~6 kg CO2e\n"
            "• Corpo bomba (ferro fundido): ~4 kg CO2e\n"
            "• Acoplamento, polia e acessórios: ~2 kg CO2e\n"
            "Total: ~12 kg CO2e (cradle-to-gate, fábrica saída)"
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Desassembly-LCA de bomba comercial 0,25 CV",
        notes="Bomba submersível reduz massa (~8 kg CO2e). Valor conservador para bomba superficial."
    ),
    0.50: ParameterJustification(
        title="Emissão Incorporada - Motobomba 0,5 CV (1/2 CV)",
        short_description="~18 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 1/2 CV, conforme ABNT NBR 9881:\n"
            "• Motor elétrico (potência nominal): ~9 kg CO2e\n"
            "• Corpo bomba + Impelidor (ferro fundido + latão): ~6 kg CO2e\n"
            "• Acoplamento, vedações e acessórios: ~3 kg CO2e\n"
            "Total: ~18 kg CO2e\n\n"
            "É a faixa mais comum em sistemas de cisterna de médio porte (5000-8000 L)."
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Desassembly-LCA típica de produto comercial consolidado",
        notes="Maior volume de produção = fator CO2 otimizado por escala de fabricação."
    ),
    0.75: ParameterJustification(
        title="Emissão Incorporada - Motobomba 0,75 CV (3/4 CV)",
        short_description="~24 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 3/4 CV para sistemas de maior circulação:\n"
            "• Motor elétrico (maior potência, mais cobre): ~12 kg CO2e\n"
            "• Corpo bomba + impelidor (maior volume): ~8 kg CO2e\n"
            "• Sistema de selagem mais robusto: ~4 kg CO2e\n"
            "Total: ~24 kg CO2e\n\n"
            "Razão: 3/4 CV = 0,75 ÷ 0,5 = 1,5×, então ~18 × 1,33 ≈ 24 kg CO2e (escala não-linear)"
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Extrapolação linear + fator de investimento estrutural",
        notes="Ainda em faixa de eficiência elevada; próximo limite de motores monofásicos."
    ),
    1.00: ParameterJustification(
        title="Emissão Incorporada - Motobomba 1,0 CV",
        short_description="~30 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 1 CV, fronteira entre trifásica leve e média industrial:\n"
            "• Motor trifásico (cobre + alumínio + ferro): ~15 kg CO2e\n"
            "• Corpo bomba + Rodete (ferro fundido, maior volume): ~10 kg CO2e\n"
            "• Sistema de vedação industrial (duplo): ~5 kg CO2e\n"
            "Total: ~30 kg CO2e\n\n"
            "Usada em sistemas maiores (cisternas > 8000 L) ou múltiplas bombas."
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Padrão consolidado para 1 CV em literatura técnica",
        notes="Produtos de qualidade superior (menor tempo de reposição) podem ter +10% CO2 (maior eficiência)."
    ),
    1.50: ParameterJustification(
        title="Emissão Incorporada - Motobomba 1,5 CV",
        short_description="~42 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 1,5 CV, agora plenamente industrial (trifásica):\n"
            "• Motor trifásico robusto (mais cobre, novo bobinado): ~21 kg CO2e\n"
            "• Corpo bomba + impelidor (ferro nodular, maior rigidez): ~15 kg CO2e\n"
            "• Sistema de lubrificação e vedação industrial: ~6 kg CO2e\n"
            "Total: ~42 kg CO2e\n\n"
            "Proporção: 1,5 ÷ 1,0 = 1,5, então ~30 × 1,4 = 42 kg CO2e (eficiência de escala levemente melhor)"
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Incremento proporcional + ganhos de eficiência produtiva",
        notes="Raramente usada em sistemas residenciais; comum em condomínios/indústria leve."
    ),
    2.00: ParameterJustification(
        title="Emissão Incorporada - Motobomba 2,0 CV",
        short_description="~55 kg CO2e de fabricação por unidade",
        detailed_explanation=(
            "Motobomba de 2 CV, entrada em classe industrial forte:\n"
            "• Motor trifásico de classe energética IE3 mínima: ~27 kg CO2e\n"
            "• Corpo bomba + carcaça ferro nodular (> 10 kg ferro): ~20 kg CO2e\n"
            "• Sistema de lubrificação automática, vedação mecânica dupla: ~8 kg CO2e\n"
            "Total: ~55 kg CO2e\n\n"
            "Proporção: 2,0 ÷ 1,5 = 1,33, então ~42 × 1,31 = 55 kg CO2e (ganhos de escala continuam)"
        ),
        source_reference="Cenário interno: substituir por BOM/massa/EPD do modelo de motobomba",
        calculation_basis="Incremento industrial + padrões de eficiência energética",
        notes=(
            "Já fora da faixa típica de sistemas de aproveitamento residencial;\n"
            "aplicável em estações elevadoras de condomínios ou fazendas."
        )
    )
}


# ── JUSTIFICATIVAS PARA FATORES OPERACIONAIS ──
OPERATIONAL_JUSTIFICATIONS: Dict[str, ParameterJustification] = {
    "chlorine_dose": ParameterJustification(
        title="Dosagem de cloro para o inventário de ACV",
        short_description="Massa anual = volume pluvial atendido × dose (mg/L) / 1000",
        detailed_explanation=(
            "O Netuno aplica a dose somente ao volume anual de água de chuva efetivamente atendido pela simulação. "
            "A conversão é direta: 1 mg/L equivale a 0,001 kg/m³; portanto, a massa anual de cloro é exibida em kg Cl2/ano.\n\n"
            "Esta entrada é uma premissa do inventário ambiental. Ela não dimensiona nem valida o tratamento da água."
        ),
        source_reference="Premissa editável do projeto; validar tratamento conforme norma e responsável técnico",
        calculation_basis="m_Cl2 = V_pluvial (m³/ano) × dose (mg/L) / 1000",
        notes="Use a dosagem adotada pelo projeto de tratamento ou uma análise de sensibilidade."
    ),
    "chlorine_co2": ParameterJustification(
        title="Fator de emissão do cloro",
        short_description="CO2e anual = massa anual de cloro × fator (kg CO2e/kg Cl2)",
        detailed_explanation=(
            "O fator converte a massa anual de cloro equivalente em emissão de ciclo de vida. "
            "O Netuno apresenta separadamente dose, massa calculada, fator e CO2e anual para permitir auditoria."
        ),
        source_reference="Fator editável do inventário de ACV do projeto",
        calculation_basis="CO2_cloro = m_Cl2 × f_Cl2",
        notes="Substitua pelo fator da cadeia de fornecimento ou inventário adotado no estudo."
    ),
    "grid_co2": ParameterJustification(
        title="Fator de Emissão da Matriz Elétrica Brasileira",
        short_description="Padrão de triagem: 0,085 kg CO2e/kWh; entrada editável",
        detailed_explanation=(
            "O fator converte a energia de recalque calculada para cada volume em kg CO2e. "
            "Ele varia no tempo e conforme o escopo do inventário. O valor 0,085 é somente "
            "uma hipótese inicial e não é rotulado como fator oficial de um ano específico."
        ),
        source_reference="MCTI/SIRENE — selecionar e arquivar o fator correspondente ao período do estudo",
        calculation_basis="CO2_bomba = energia anual (kWh) × fator da rede (kg CO2e/kWh)",
        notes=(
            "Registre arquivo, versão, período, data de acesso e natureza média/marginal do fator escolhido."
        )
    ),
    "treatment_co2": ParameterJustification(
        title="Fator agregado legado de tratamento",
        short_description="Campo opcional em kg CO2e/m³ para compatibilidade de projetos antigos",
        detailed_explanation=(
            "Projetos antigos podem informar diretamente uma intensidade agregada de tratamento. "
            "Quando o campo não é usado, a versão 5.0.7 deriva a intensidade de dose de cloro × "
            "fator do cloro / 1000, exibindo também a massa anual."
        ),
        source_reference="Premissa do projeto legado; documentar tecnologia e inventário próprios",
        calculation_basis="CO2_tratamento = volume tratado × intensidade agregada",
        notes="Não misture o fator agregado com a parcela de cloro calculada separadamente."
    ),
    "potable_co2": ParameterJustification(
        title="Fator de Emissão de Água Potável Evitada",
        short_description="Padrão de triagem: 0,35 kg CO2e por m³ evitado",
        detailed_explanation=(
            "O fator representa o crédito de cenário por água potável que deixa de ser fornecida. "
            "Sua fronteira deve declarar se inclui apenas abastecimento ou também esgotamento. "
            "O padrão 0,35 é uma hipótese editável, não um valor nacional universal."
        ),
        source_reference="Inventário local da concessionária ou literatura compatível com a fronteira do estudo",
        calculation_basis="CO2_água_evitado = volume pluvial consumido × fator da água",
        notes=(
            "Faça sensibilidade e evite dupla contagem de esgoto ou energia já incluída em outro módulo."
        )
    )
}


def get_material_justification(material_key: str, param: str) -> Optional[ParameterJustification]:
    """
    Obtém a justificativa de um parâmetro de material.
    
    Args:
        material_key: Chave do material (ex: "PEAD", "CONCRETO")
        param: Parâmetro ("density" ou "co2_factor")
    
    Returns:
        ParameterJustification ou None se não encontrado
    """
    return _mark_as_screening(MATERIAL_JUSTIFICATIONS.get(material_key, {}).get(param))


def get_pipe_justification(diameter_mm: int) -> Optional[ParameterJustification]:
    """Obtém a justificativa para um fator de emissão de tubulação."""
    return _mark_as_screening(PIPE_JUSTIFICATIONS.get(diameter_mm))


def get_pump_justification(power_cv: float) -> Optional[ParameterJustification]:
    """Obtém a justificativa para uma emissão de bomba."""
    return _mark_as_screening(PUMP_JUSTIFICATIONS.get(power_cv))


def get_operational_justification(param_name: str) -> Optional[ParameterJustification]:
    """Obtém a justificativa para um fator operacional (matriz elétrica, tratamento, etc.)."""
    return _mark_as_screening(OPERATIONAL_JUSTIFICATIONS.get(param_name))


def _mark_as_screening(justification: Optional[ParameterJustification]) -> Optional[ParameterJustification]:
    """Impede que o racional histórico seja apresentado como dado primário auditado.

    As notas antigas são preservadas como memória de construção do cenário, mas
    a interface deixa explícito que o usuário precisa fornecer uma fonte
    rastreável para uso científico.
    """
    if justification is None:
        return None
    return replace(
        justification,
        detailed_explanation=(
            "HIPÓTESE INTERNA DE TRIAGEM — não trate o número abaixo como valor normativo "
            "ou fator primário verificado. Substitua-o por quantitativo, EPD ou inventário "
            "versionado compatível com o projeto.\n\n" + justification.detailed_explanation
        ),
        source_reference=(
            "Cenário interno não auditado nesta distribuição; registrar fonte primária, "
            "versão, geografia, período, fronteira e transformação aplicada"
        ),
    )


def format_justification_as_tooltip(justification: ParameterJustification) -> str:
    """
    Formata uma justificativa como HTML rico para exibição em tooltip.
    
    Args:
        justification: Objeto ParameterJustification
    
    Returns:
        String HTML formatada para tooltip rico
    """
    html = f"""
    <html style="font-family: 'Segoe UI', Arial, sans-serif; max-width: 450px;">
    <head><style>
        body {{ margin: 0; padding: 8px; font-size: 11px; color: #333; }}
        .title {{ font-weight: bold; color: #0369a1; font-size: 12px; margin-bottom: 4px; }}
        .short {{ color: #666; font-style: italic; margin-bottom: 6px; font-size: 10px; }}
        .section {{ margin-top: 8px; }}
        .section-title {{ font-weight: bold; color: #1e293b; font-size: 10.5px; margin-bottom: 2px; }}
        .section-content {{ line-height: 1.4; color: #475569; margin-left: 8px; }}
        .source {{ color: #0369a1; margin-top: 6px; font-weight: bold; font-size: 10px; }}
        .notes {{ color: #d97706; background-color: #fffbeb; padding: 4px 6px; 
                 border-radius: 3px; margin-top: 6px; font-size: 10px; }}
        code {{ background-color: #f1f5f9; padding: 1px 4px; border-radius: 2px; 
               font-family: 'Consolas', monospace; font-size: 9px; }}
    </style></head>
    <body>
        <div class="title">📊 {justification.title}</div>
        <div class="short">{justification.short_description}</div>
        
        <div class="section">
            <div class="section-title">🔍 Explicação Detalhada:</div>
            <div class="section-content">{justification.detailed_explanation.replace(chr(10), '<br>')}</div>
        </div>
        
        <div class="section">
            <div class="section-title">📐 Base do Cálculo:</div>
            <div class="section-content">{justification.calculation_basis}</div>
        </div>
        
        <div class="source">📚 Referência: {justification.source_reference}</div>
    """
    
    if justification.notes:
        html += f'<div class="notes"><strong>📌 Notas:</strong> {justification.notes.replace(chr(10), "<br>")}</div>'
    
    html += "</body></html>"
    return html


def generate_html_justifications_materials() -> str:
    """Gera HTML com tabela de justificativas de materiais para documentação."""
    html = """
    <h2 style='color: #b45309; margin-top: 0px;'>🏗️ Justificativas de Materiais de Reservatório (ACV)</h2>
    <p style='font-size: 13px; line-height: 1.5;'>
        Cenários internos de triagem para cisternas e caixas d'água. Os números não são fatores normativos
        nem dados primários auditados nesta distribuição. Substitua massa e fator por ficha técnica, EPD ou
        inventário versionado, registrando geografia, período, fronteira e incerteza.
    </p>
    
    <table border='1' cellspacing='0' cellpadding='10' style='border-collapse: collapse; border-color: #f59e0b; width: 100%; margin-top: 15px; font-size: 12px;'>
        <tr style='background-color: #f97316; color: #ffffff; font-weight: bold;'>
            <th align='left'>Material</th>
            <th align='center'>Densidade (kg/m³)</th>
            <th align='center'>CO2e Específico (kg/kg)</th>
            <th align='center'>CO2e Total/m³ (kg)</th>
            <th align='left'>Características e Referências</th>
        </tr>
    """
    
    for key, preset in MATERIAL_PRESETS.items():
        html += f"""
        <tr style='background-color: #fffbeb;'>
            <td><b>{preset.name}</b></td>
            <td align='center'>{format_ptbr(preset.material_density_kg_per_m3_tank, 1)}</td>
            <td align='center'>{format_ptbr(preset.co2_factor_kg_per_kg, 2)}</td>
            <td align='center'><b>{format_ptbr(preset.co2_factor_kg_per_m3_tank, 1)}</b></td>
            <td>
                <b>Descrição:</b> {preset.description}<br/>
                <b>Fonte:</b> {preset.source_reference}
            </td>
        </tr>
        """
    
    html += """
    </table>
    
    <div style='background-color: #fff7ed; border-left: 4px solid #f97316; padding: 14px; margin-top: 20px; border-radius: 4px;'>
        <h4 style='color: #b45309; margin: 0px 0px 8px 0px; font-size: 13px;'>💡 Interpretação:</h4>
        <ul style='font-size: 12px; line-height: 1.6; margin: 8px 0px; padding-left: 20px;'>
            <li><b>PEAD:</b> Material com menor impacto inicial (66 kg CO2e/m³), leve e prático para instalação.</li>
            <li><b>CONCRETO:</b> Material com maior volume de estrutura (168 kg CO2e/m³), mas altíssima durabilidade (50+ anos).</li>
            <li><b>FIBRA:</b> Meio termo (85 kg CO2e/m³), resistente à corrosão, vida útil moderada.</li>
            <li><b>AÇO INOX:</b> Maior pegada inicial (110 kg CO2e/m³), totalmente reciclável, durabilidade excepcional.</li>
        </ul>
    </div>
    """
    
    return html


def generate_html_justifications_pipes() -> str:
    """Gera HTML com tabela de justificativas de tubulações."""
    html = """
    <h2 style='color: #b45309; margin-top: 0px;'>🔧 Justificativas de Tubulações PVC (ACV)</h2>
    <p style='font-size: 13px; line-height: 1.5;'>
        Cenário interno de triagem por diâmetro nominal. Confirme a massa linear e o material/classe do tubo
        real e aplique uma EPD ou inventário compatível; os valores abaixo não substituem esse levantamento.
    </p>
    
    <table border='1' cellspacing='0' cellpadding='10' style='border-collapse: collapse; border-color: #fb923c; width: 100%; margin-top: 15px; font-size: 12px;'>
        <tr style='background-color: #fb923c; color: #ffffff; font-weight: bold;'>
            <th align='left'>Diâmetro Nominal (DN)</th>
            <th align='center'>Peso Linear (kg/m)</th>
            <th align='center'>CO2e por Metro (kg CO2e/m)</th>
            <th align='left'>Aplicações Típicas e Referências</th>
        </tr>
    """
    
    for dn, co2_per_m in PIPE_EMISSION_FACTORS_PER_METER.items():
        weight_per_m = co2_per_m / 2.80  # Reverso: 2.80 é fator PVC
        html += f"""
        <tr style='background-color: #fff7ed;'>
            <td><b>DN {dn} mm ({format_ptbr(dn / 25.4, 1)}")</b></td>
            <td align='center'>{format_ptbr(weight_per_m, 2)}</td>
            <td align='center'><b>{format_ptbr(co2_per_m, 2)}</b></td>
            <td>
                Hipótese de massa linear × 2,80 kg CO2e/kg. Verifique classe, fabricante, massa e EPD do tubo.
            </td>
        </tr>
        """
    
    html += """
    </table>
    
    <div style='background-color: #fff7ed; border-left: 4px solid #f97316; padding: 14px; margin-top: 20px; border-radius: 4px;'>
        <h4 style='color: #b45309; margin: 0px 0px 8px 0px; font-size: 13px;'>💡 Nota Técnica:</h4>
        <p style='font-size: 12px; line-height: 1.6; margin: 0px;'>
            A emissão de CO2e é proporcional ao peso linear de material PVC. Tubos com maiores diâmetros 
            possuem maior massa linear. A escolha de diâmetro deve otimizar entre velocidades de escoamento 
            (minimizar perdas) e volume de material (minimizar CO2).
        </p>
    </div>
    """
    
    return html


def generate_html_justifications_pumps() -> str:
    """Gera HTML com tabela de justificativas de motobombas."""
    html = """
    <h2 style='color: #b45309; margin-top: 0px;'>⚡ Justificativas de Emissão Incorporada em Motobombas (ACV)</h2>
    <p style='font-size: 13px; line-height: 1.5;'>
        Cenário interno de triagem por faixa de potência. Para estudo definitivo, substitua pela massa/BOM e
        EPD ou inventário do modelo escolhido, incluindo reposições coerentes com a vida útil.
    </p>
    
    <table border='1' cellspacing='0' cellpadding='10' style='border-collapse: collapse; border-color: #fb923c; width: 100%; margin-top: 15px; font-size: 12px;'>
        <tr style='background-color: #fb923c; color: #ffffff; font-weight: bold;'>
            <th align='center'>Potência (CV)</th>
            <th align='center'>Emissão Incorporada (kg CO2e)</th>
            <th align='left'>Composição e Aplicações Típicas</th>
        </tr>
    """
    
    for cv, co2 in PUMP_EMBEDDED_CO2.items():
        html += f"""
        <tr style='background-color: #fff7ed;'>
            <td align='center'><b>{format_ptbr(cv, 2)}</b></td>
            <td align='center'><b>{format_ptbr(co2, 1)}</b></td>
            <td>
                Partição ilustrativa: motor ({format_ptbr(co2 * 0.5, 0)} kg CO2e) + corpo ({format_ptbr(co2 * 0.33, 0)} kg CO2e) + acessórios ({format_ptbr(co2 * 0.17, 0)} kg CO2e).
            </td>
        </tr>
        """
    
    html += """
    </table>
    
    <div style='background-color: #fff7ed; border-left: 4px solid #f97316; padding: 14px; margin-top: 20px; border-radius: 4px;'>
        <h4 style='color: #b45309; margin: 0px 0px 8px 0px; font-size: 13px;'>💡 Interpretação:</h4>
        <p style='font-size: 12px; line-height: 1.6; margin: 0px;'>
            A emissão incorporada cresce de forma não-linear com a potência (ganhos de escala produtivo). 
            Valores referem-se à pegada de fabricação (cradle-to-gate), não incluindo a operação (consumo elétrico), 
            que é contabilizado separadamente com base na matriz elétrica local.
        </p>
    </div>
    """
    
    return html


def generate_html_justifications_operational() -> str:
    """Gera HTML com justificativas de fatores operacionais."""
    html = """
    <h2 style='color: #b45309; margin-top: 0px;'>🌍 Fatores Operacionais e Matriz Elétrica (ACV)</h2>
    <p style='font-size: 13px; line-height: 1.5;'>
        Parâmetros que influenciam a emissão de CO2e durante a fase operacional do sistema 
        (20-50 anos de vida útil do projeto).
    </p>
    
    <table border='1' cellspacing='0' cellpadding='10' style='border-collapse: collapse; border-color: #fb923c; width: 100%; margin-top: 15px; font-size: 12px;'>
        <tr style='background-color: #fb923c; color: #ffffff; font-weight: bold;'>
            <th align='left'>Parâmetro</th>
            <th align='center'>Valor Padrão</th>
            <th align='left'>Justificativa e Referência</th>
        </tr>
        <tr style='background-color: #fff7ed;'>
            <td><b>Matriz Elétrica Brasileira</b></td>
            <td align='center'><b>0,085 kg CO2e/kWh</b></td>
            <td>
                Hipótese editável. Selecionar e arquivar o fator MCTI/SIRENE correspondente ao período e escopo do estudo.
            </td>
        </tr>
        <tr style='background-color: #fff7ed;'>
            <td><b>Cloração (massa e fator)</b></td>
            <td align='center'><b>Dose × fator</b></td>
            <td>
                m_Cl2 = volume pluvial atendido × dose (mg/L) / 1000; CO2e = m_Cl2 × fator do cloro.
                Dose e fator são editáveis e a massa anual calculada é exibida no inventário.
            </td>
        </tr>
        <tr style='background-color: #fff7ed;'>
            <td><b>Abatimento: Água Potável Evitada</b></td>
            <td align='center'><b>0,35 kg CO2e/m³</b></td>
            <td>
                Hipótese editável de crédito. Substituir por inventário local e declarar se a fronteira inclui esgotamento.
            </td>
        </tr>
    </table>
    
    <div style='background-color: #fff7ed; border-left: 4px solid #f97316; padding: 14px; margin-top: 20px; border-radius: 4px;'>
        <h4 style='color: #b45309; margin: 0px 0px 8px 0px; font-size: 13px;'>♻️ Balanço de Carbono:</h4>
        <p style='font-size: 12px; line-height: 1.6; margin: 0px;'>
            <b>Pegada Inicial (ACV Incorporada):</b> Materiais + Estrutura + Equipamentos<br/>
            <b>Pegada Operacional (ACV Operacional):</b> Consumo elétrico + Tratamento químico (negativo)<br/>
            <b>Crédito (ACV de Cenário):</b> Água potável urban evitada ao longo de 20 anos<br/>
            <b>Resultado Final:</b> saldo líquido evitado = crédito − operação − incorporado; interpretar sob as fronteiras declaradas.
        </p>
    </div>
    """
    
    return html
