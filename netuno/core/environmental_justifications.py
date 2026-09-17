"""
Módulo de Justificativas e Tooltips para Análise Ambiental (ACV).
Fornece justificativas detalhadas, referências bibliográficas e explicações
para cada definição de parâmetro ambiental, integrado com o sistema de tooltips da UI.
"""

from netuno.core.chlorination import FONTE_DO_FATOR
from dataclasses import dataclass, replace
from typing import Dict, Optional

from netuno.core.environmental import (
    MATERIAL_PRESETS,
    PIPE_EMISSION_FACTORS_PER_METER,
    PUMP_EMBEDDED_CO2,
    PUMP_EMBEDDED_CO2_SOURCE,
    PUMP_KG_CO2E_POR_KG,
    PUMP_MASS_KG,
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
            short_description="1,612 kg CO2e por kg de resina PEAD",
            detailed_explanation=(
                "Valor publicado, berco-ao-portao, para a resina de PEAD virgem:\n"
                "- 1.221 kg CO2e por 1.000 kg vindos dos materiais de entrada (76%)\n"
                "- 390 kg CO2e por 1.000 kg da producao da resina em si (24%)\n"
                "- Total: 1.612 kg CO2e por 1.000 kg, ou seja 1,612 kg CO2e/kg\n\n"
                "Metodo TRACI 2.1 com GWP-100 do IPCC (2013); escopo Estados Unidos.\n\n"
                "Substitui o valor interno anterior de 3,00 kg CO2e/kg, que nao tinha fonte e "
                "cuja decomposicao declarava a MESMA fronteira (extracao e refino, polimerizacao, "
                "transporte). A diferenca, portanto, nao se explica por fronteira: o valor antigo "
                "superestimava a resina em cerca de 86%.\n\n"
                "Ressalva de escopo: a resina consumida no Brasil tem matriz eletrica e cadeia de "
                "materia-prima diferentes das norte-americanas. Para publicacao, prefira a EPD do "
                "fabricante efetivamente empregado."
            ),
            source_reference=(
                "FRANKLIN ASSOCIATES para o American Chemistry Council (out/2020), "
                "Cradle-to-Gate Life Cycle Analysis of High-Density Polyethylene (HDPE) Resin, Tabela 6"
            ),
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
                "O SIDAC, inventário brasileiro da construção, publica para concreto dosado em central "
                "cerca de 310 kg CO2/m³ a 20 MPa e 480 kg CO2/m³ a 40 MPa.\n\n"
                "0,14 kg CO2e/kg x 2.400 kg/m³ = 336 kg/m³, dentro da faixa de um concreto de 25 a 30 MPa.\n\n"
                "A armadura não está separada: para a obra, some a EPD do aço com o quantitativo do projeto."
            ),
            source_reference=(
                "SIDAC (Sistema de Informação do Desempenho Ambiental da Construção): concreto dosado em "
                "central, 310 a 480 kg CO2/m³ entre 20 e 40 MPa"
            ),
            calculation_basis="Faixa do SIDAC por resistência convertida pela massa específica de 2.400 kg/m³",
            notes=(
                "Concretos de maior resistência emitem mais por metro cúbico: a 40 MPa o SIDAC chega a "
                "cerca de 480 kg CO2/m³, 43% acima do valor adotado. Declare a classe do concreto."
            )
        )
    },
    "FIBRA": {
        "density": ParameterJustification(
            title="Densidade do PRFV (Poliéster + Fibra de Vidro)",
            short_description="massa por capacidade do catálogo Fortlev; cerca de 15 kg por m³ útil",
            detailed_explanation=(
                "O cálculo interpola a massa da caixa vazia por capacidade no catálogo técnico da "
                "Fortlev (reservatórios conforme ABNT NBR 13210): 20,3 kg a 1.000 L, 74,9 kg a "
                "5.000 L e 136,7 kg a 10.000 L. Há economia de escala, e a densidade constante de "
                "20 kg/m³ usada antes superestimava a massa em até 46%."
            ),
            source_reference="Catálogo técnico Fortlev, «Caixa d'água em fibra de vidro», peso da caixa vazia por capacidade",
            calculation_basis="Interpolação linear da massa por capacidade na tabela do fabricante; fora da faixa, densidade do extremo mais próximo",
            notes="A densidade cai com o porte: 20 kg/m³ a 1.000 L, 15 kg/m³ a 5.000 L e 13,7 kg/m³ a 10.000 L."
        ),
        "co2_factor": ParameterJustification(
            title="Fator de Emissão de CO2e do PRFV",
            short_description="3,25 kg CO2e por kg de composto",
            detailed_explanation=(
                "A Composites UK publica, para peças de PRFV, faixa típica de 2,5 a 4,0 kg CO2e/kg. "
                "Adota-se o ponto médio, 3,25 kg CO2e/kg.\n\n"
                "O valor de 8,1 kg CO2e/kg que circula na literatura antiga vem da base ICE dos anos "
                "1990 e foi retirado na ICE v4.0: quem o encontrar deve descartá-lo.\n\n"
                "Versões anteriores do programa exibiam aqui 4,25 kg CO2e/kg, com uma decomposição por "
                "componente sem fonte, enquanto o cálculo já usava 3,25."
            ),
            source_reference=(
                "COMPOSITES UK, Embodied carbon data for composites (atual. 22/04/2026): "
                "faixa tipica de 2,5 a 4,0 kg CO2e/kg para pecas de PRFV"
            ),
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
            short_description="3,70 kg CO2e por kg de aço inox, a 50% de sucata",
            detailed_explanation=(
                "A pegada do aço inox é alta comparada à do aço carbono (0,7 a 0,9 kg CO2e/kg) "
                "por causa do teor de cromo e níquel.\n\n"
                "O que domina o resultado, porém, não é a liga: é o teor de sucata da carga. "
                "O relatório worldstainless publica, berço-ao-portão com escopos 1, 2 e 3:\n"
                "\u2022 85% de sucata: 1,95 kg CO2e/kg\n"
                "\u2022 75% de sucata: 2,45 kg CO2e/kg\n"
                "\u2022 50% de sucata: 3,70 kg CO2e/kg  (adotado)\n"
                "\u2022 30% de sucata: 6,80 kg CO2e/kg\n\n"
                "São 3,5 vezes entre os extremos. Um estudo que não declare o teor de sucata "
                "não é comparável, pela mesma razão que um fator de rede sem ano não é."
            ),
            source_reference=(
                "WORLDSTAINLESS (World Steel Association), Stainless steel CO2 emissions "
                "report (24/09/2024): 3,70 kg CO2/kg a 50% de sucata"
            ),
            calculation_basis="worldstainless, berço-ao-portão, escopos 1, 2 e 3, carga com 50% de sucata",
            notes=(
                "Elevar o teor de sucata para 85% levaria o fator a 1,95 kg CO2e/kg, quase metade "
                "do adotado. O aço inox é reciclável ao final da vida, o que não entra "
                "nesta fronteira berço-ao-portão."
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
            "Tubulação PVC rígido DN 50 mm contém 0,668 kg de material PVC por metro.\n"
            "Considerando fator de emissão do PVC = 2,36 kg CO2e/kg:\n"
            "  0,668 kg x 2,36 kg CO2e/kg = 1,58 kg CO2e/m\n\n"
            "Este é o tubo mais fino do padrão, usado para linhas de recirculação e drenos."
        ),
        source_reference="Massa linear: Amanco Wavin FTC000021 (out/2025) ou geometria das ABNT NBR 5648 e 5688. Fator: EPD Australasia S-P-05503, RXP PVC Pipes (25/11/2022), módulos A1-A3, 2,36 kg CO2e por kg de tubo instalado",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Inclui cimento PVC (5-10% das dimensões do tubo) e aditivos estabilizadores."
    ),
    75: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 75 mm (3\")",
        short_description="2,66 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 75 mm contém 1,412 kg de material PVC por metro.\n"
            "Cálculo: 0,95 kg x 2,36 kg CO2e/kg = 2,24 kg CO2e/m\n\n"
            "Diâmetro intermediário, tipicamente usado para distribuição principal "
            "e interconexões entre cisterna e caixa superior."
        ),
        source_reference="Massa linear: Amanco Wavin FTC000021 (out/2025) ou geometria das ABNT NBR 5648 e 5688. Fator: EPD Australasia S-P-05503, RXP PVC Pipes (25/11/2022), módulos A1-A3, 2,36 kg CO2e por kg de tubo instalado",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Tubo Schedule 40 com pressão nominal 100 psi (padrão sistemas de aproveitamento)."
    ),
    100: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 100 mm (4\")",
        short_description="3,92 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 100 mm contém 1,176 kg de material PVC por metro.\n"
            "Cálculo: 1,40 kg x 2,36 kg CO2e/kg = 3,30 kg CO2e/m\n\n"
            "Tubo de maior seção, usado para linhas de grande vazão, "
            "captação principal e alimentação de cisterna."
        ),
        source_reference="Massa linear: Amanco Wavin FTC000021 (out/2025) ou geometria das ABNT NBR 5648 e 5688. Fator: EPD Australasia S-P-05503, RXP PVC Pipes (25/11/2022), módulos A1-A3, 2,36 kg CO2e por kg de tubo instalado",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Mais econômico para grandes vazões que múltiplas linhas menores."
    ),
    150: ParameterJustification(
        title="Fator de CO2 - Tubulação PVC DN 150 mm (6\")",
        short_description="7,84 kg CO2e por metro linear",
        detailed_explanation=(
            "Tubulação PVC rígido DN 150 mm contém 2,502 kg de material PVC por metro.\n"
            "Cálculo: 2,80 kg x 2,36 kg CO2e/kg = 6,61 kg CO2e/m\n\n"
            "Tubo de maior seção do catálogo padrão, usado em coletas de grande escala "
            "ou quando a velocidade de fluxo deve ser minimizada (reduz perdas)."
        ),
        source_reference="Massa linear: Amanco Wavin FTC000021 (out/2025) ou geometria das ABNT NBR 5648 e 5688. Fator: EPD Australasia S-P-05503, RXP PVC Pipes (25/11/2022), módulos A1-A3, 2,36 kg CO2e por kg de tubo instalado",
        calculation_basis="Peso linear de tubo PVC comercial × fator CO2 PVC virgin",
        notes="Próximo limite de aplicação em sistemas residenciais/comerciais de médio porte."
    )
}


# ── JUSTIFICATIVAS PARA MOTOBOMBAS ──
# As versões anteriores decompunham cada valor em motor, corpo e acessórios, com
# números sem fonte e, em quatro potências, por escalonamento aritmético. Agora a
# justificativa é gerada das duas fontes lidas: massa de catálogo e intensidade
# por quilo de uma EPD.
def _justificativa_da_bomba(cv: float) -> ParameterJustification:
    massa = PUMP_MASS_KG[cv]
    co2 = PUMP_EMBEDDED_CO2[cv]
    potencia = format_ptbr(cv, 2)
    return ParameterJustification(
        title=f"Emissão Incorporada - Motobomba {potencia} CV",
        short_description=f"{format_ptbr(co2, 1)} kg CO2e de fabricação por unidade",
        detailed_explanation=(
            f"Massa do produto: {format_ptbr(massa, 1)} kg (catálogo geral 60 Hz da Dancor, séries CAM W-4C "
            f"e CAM W-10, motor monofásico de 2 polos).\n"
            f"Intensidade: {format_ptbr(PUMP_KG_CO2E_POR_KG, 2)} kg CO2e por kg de bomba (EPD Grundfos "
            f"EPD-GRU-20250340-CBA1-EN, módulos A1-A3: 10,4 kg CO2e por unidade de 2,179 kg).\n"
            f"Emissão de fabricação: {format_ptbr(massa, 1)} x {format_ptbr(PUMP_KG_CO2E_POR_KG, 2)} = "
            f"{format_ptbr(co2, 1)} kg CO2e (berço ao portão)."
        ),
        source_reference=PUMP_EMBEDDED_CO2_SOURCE[cv],
        calculation_basis="Massa de catálogo x intensidade por quilo de EPD de bomba elétrica pequena",
        notes=(
            "A EPD é de circulador europeu com eletrônica embarcada, e a massa de referência inclui a "
            "embalagem: trate o valor como ordem de grandeza. Havendo EPD do modelo empregado, ela prevalece."
        ),
    )


PUMP_JUSTIFICATIONS: Dict[float, ParameterJustification] = {
    cv: _justificativa_da_bomba(cv) for cv in PUMP_MASS_KG
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
        source_reference="ABNT NBR 15527:2019, item 4.6.5: cloro residual livre de 0,5 a 2,0 mg/L; o programa adota 1,5 mg/L",
        calculation_basis="m_Cl2 = V_pluvial (m³/ano) × dose (mg/L) / 1000",
        notes="Use a dosagem adotada pelo projeto de tratamento ou uma análise de sensibilidade."
    ),
    "chlorine_purity": ParameterJustification(
        title="Pureza do produto clorado",
        short_description="Massa de produto = massa de cloro ativo / pureza",
        detailed_explanation=(
            "A dose e prescrita em cloro ATIVO, e e o cloro ativo que desinfeta. "
            "O que se compra, porem, e o PRODUTO comercial, e tanto o preco quanto "
            "o fator de emissao sao por quilo de produto. A pureza faz a ponte "
            "entre os dois.\n\n"
            "Hipoclorito de calcio em pastilha: 0,65 kg de cloro ativo por kg de "
            "produto. Hipoclorito de sodio liquido (agua sanitaria): cerca de 0,10. "
            "Dicloroisocianurato de sodio: cerca de 0,56.\n\n"
            "O efeito e de 1/pureza, e nao e pequeno: a mesma dose, a agua "
            "sanitaria exige seis vezes mais produto que a pastilha."
        ),
        source_reference=(
            "Teor declarado em rotulo dos produtos comerciais; "
            "cadeia de conversao em netuno/core/chlorination.py"
        ),
        calculation_basis="m_produto = m_Cl2_ativo / pureza",
        notes="Confira o teor no rotulo do produto adotado antes de editar."
    ),
    "chlorine_co2": ParameterJustification(
        title="Fator de emissão do produto clorado",
        short_description="CO2e anual = massa anual de produto × fator (kg CO2e/kg de produto)",
        detailed_explanation=(
            "O fator é por quilo de PRODUTO comercial, e não de cloro ativo: a pureza converte "
            "a dose em massa de produto antes da multiplicação.\n\n"
            "O padrão de 1,72 kg CO2e/kg vem do Ecoinvent 3.8 (cutoff), processo «sodium "
            "hypochlorite production, product in 15% solution state», método EF 3.1, "
            "Climate change: 2,52 kg CO2e/kg de NaOCl puro. Como o Ecoinvent 3.8 não tem "
            "hipoclorito de cálcio, o valor foi levado à base de cloro ativo (0,9525 kg de Cl2 "
            "por kg de NaOCl, logo 2,65 kg CO2e/kg de cloro ativo) e multiplicado pela pureza "
            "da pastilha, 0,65."
        ),
        source_reference=FONTE_DO_FATOR,
        calculation_basis="CO2_cloro = V_pluvial × dose / 1000 / pureza × f_produto",
        notes="Aproximação: declare-a no estudo. Um fator digitado pelo usuário substitui este."
    ),
    "grid_co2": ParameterJustification(
        title="Fator de Emissão da Matriz Elétrica Brasileira",
        short_description="Padrão adotado: 0,085 kg CO2e/kWh; cinco bases selecionáveis",
        detailed_explanation=(
            "O fator converte a energia de bombeamento em kg CO2e, e precisa ser de "
            "CO2-equivalente: a série anual do MCTI/SIRENE é de CO2 apenas e cobre só a geração.\n\n"
            "O padrão de 0,085 é uma escolha declarada, e não a transcrição de uma fonte única: "
            "fica entre o SIDAC (0,070), o CaDI (0,074) e o percentil 5 do indicador fóssil da "
            "matriz de 2022 em Vaz, Scolaro e Ghisi (2025), 0,075. O mesmo artigo dá 0,104 "
            "(fóssil) e 0,151 (total) como valores centrais, que o programa oferece como bases "
            "alternativas para a análise de sensibilidade."
        ),
        source_reference=(
            "Vaz, Scolaro & Ghisi (2025), doi:10.1016/j.scitotenv.2025.179774; SIDAC; CaDI (2025). "
            "Base registrada no relatório"
        ),
        calculation_basis="CO2_bomba = energia anual (kWh) × fator da rede (kg CO2e/kWh)",
        notes="Declare a base escolhida e o ano da matriz a que ela se refere."
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
        short_description="Padrão: 0,35 kg CO2e por m³ entregue; 19 rotas por macrorregião e manancial",
        detailed_explanation=(
            "O fator é por metro cúbico ENTREGUE na edificação, e não produzido na estação: as "
            "perdas de distribuição do SNIS, de 33,9% no Sudeste a 46,9% no Norte, fazem cada m³ "
            "entregue exigir de 1,5 a 1,9 m³ produzidos.\n\n"
            "O padrão de 0,35 fica logo abaixo das faixas publicadas para tratamento convencional "
            "(corroborado por Garfí et al., 2016), o que subestima o benefício do sistema pluvial: "
            "é o erro conservador. As 19 rotas do programa trazem fonte e fronteira próprias."
        ),
        source_reference=(
            "Rotas de abastecimento do programa, com procedência por rota; Garfí et al. (2016), "
            "doi:10.1016/j.jclepro.2016.07.218; SNIS, perdas na distribuição"
        ),
        calculation_basis="CO2_água_evitado = volume pluvial consumido × fator por m³ entregue",
        notes="Prefira o inventário da concessionária, quando existir, e declare a rota adotada."
    ),
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
    # Com fonte declarada, a justificativa não recebe o carimbo de triagem, que
    # sobrescreveria a referência pela frase genérica de cenário interno.
    return PUMP_JUSTIFICATIONS.get(power_cv)


def get_operational_justification(param_name: str) -> Optional[ParameterJustification]:
    """Obtém a justificativa para um fator operacional (matriz elétrica, tratamento, etc.)."""
    return _mark_as_screening(OPERATIONAL_JUSTIFICATIONS.get(param_name))


#: Começos de referência que indicam cenário interno ou orientação, e não fonte.
_SEM_FONTE = ("cenário", "premissa", "fator editável", "inventário local")


def tem_fonte_declarada(justification: Optional[ParameterJustification]) -> bool:
    """Diz se a justificativa cita uma fonte, em vez de um cenário interno."""
    if justification is None:
        return False
    referencia = (justification.source_reference or "").strip().lower()
    return bool(referencia) and not referencia.startswith(_SEM_FONTE)


def _mark_as_screening(justification: Optional[ParameterJustification]) -> Optional[ParameterJustification]:
    """Impede que o racional histórico seja apresentado como dado primário auditado.

    As notas antigas são preservadas como memória de construção do cenário, mas
    a interface deixa explícito que o usuário precisa fornecer uma fonte
    rastreável para uso científico.
    """
    # Só o que não tem fonte recebe o carimbo. Antes ele era aplicado a tudo, e
    # sobrescrevia com «cenário interno» até a referência de uma EPD.
    if justification is None or tem_fonte_declarada(justification):
        return justification
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
        weight_per_m = co2_per_m / 2.36  # Reverso: 2.80 é fator PVC
        html += f"""
        <tr style='background-color: #fff7ed;'>
            <td><b>DN {dn} mm ({format_ptbr(dn / 25.4, 1)}")</b></td>
            <td align='center'>{format_ptbr(weight_per_m, 2)}</td>
            <td align='center'><b>{format_ptbr(co2_per_m, 2)}</b></td>
            <td>
                Hipótese de massa linear × 2,36 kg CO2e/kg. Verifique classe, fabricante, massa e EPD do tubo.
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
        Massa do produto (catálogo geral 60 Hz da Dancor, séries CAM W-4C e CAM W-10) multiplicada pela
        intensidade de carbono por quilo de bomba da EPD Grundfos EPD-GRU-20250340-CBA1-EN (IBU, 2025,
        módulos A1-A3). Havendo EPD do modelo empregado, ela prevalece.
    </p>

    <table border='1' cellspacing='0' cellpadding='10' style='border-collapse: collapse; border-color: #fb923c; width: 100%; margin-top: 15px; font-size: 12px;'>
        <tr style='background-color: #fb923c; color: #ffffff; font-weight: bold;'>
            <th align='center'>Potência (CV)</th>
            <th align='center'>Massa (kg)</th>
            <th align='center'>Emissão Incorporada (kg CO2e)</th>
        </tr>
    """

    for cv, co2 in PUMP_EMBEDDED_CO2.items():
        html += f"""
        <tr style='background-color: #fff7ed;'>
            <td align='center'><b>{format_ptbr(cv, 2)}</b></td>
            <td align='center'>{format_ptbr(PUMP_MASS_KG.get(cv, 0.0), 1)}</td>
            <td align='center'><b>{format_ptbr(co2, 1)}</b></td>
        </tr>
        """

    html += f"""
    </table>

    <div style='background-color: #fff7ed; border-left: 4px solid #f97316; padding: 14px; margin-top: 20px; border-radius: 4px;'>
        <h4 style='color: #b45309; margin: 0px 0px 8px 0px; font-size: 13px;'>💡 Interpretação:</h4>
        <p style='font-size: 12px; line-height: 1.6; margin: 0px;'>
            Intensidade adotada: {format_ptbr(PUMP_KG_CO2E_POR_KG, 2)} kg CO2e por kg de bomba (10,4 kg CO2e por
            unidade de 2,179 kg, com embalagem). É um circulador europeu com eletrônica embarcada, e não uma
            centrífuga brasileira: trate o valor como ordem de grandeza. Os valores cobrem a fabricação (berço ao
            portão); a energia de operação é contabilizada à parte, com o fator da rede elétrica escolhido.
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
