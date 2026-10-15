# -*- coding: utf-8 -*-
"""Traduções dos textos neutros das edições INT e PRT (rodada 4 da auditoria).

Cada chave é o texto-fonte em português; o valor traz inglês, espanhol e chinês. Em
``translation.py`` estas entradas **substituem** as do catálogo principal quando a chave é a
mesma (os textos neutros reescrevem frases que citavam normas e índices do Brasil), e preenchem
as lacunas quando não existia tradução. Também reúne as cadeias que a interface em inglês
deixava em português (UI-14).
"""

COMPLEMENTO_NEUTRO = {
    # ── Moeda (decisão U-21: a Internacional não tem moeda predefinida) ──────────────────────
    'Moeda não definida (¤)': ('Currency not set (¤)', 'Moneda no definida (¤)', '未设置货币（¤）'),
    'Na Edição Portugal a moeda é o euro.': ('In the Portugal Edition the currency is the euro.', 'En la Edición Portugal la moneda es el euro.', '葡萄牙版的货币为欧元。'),
    'Escolha a moeda do projeto: todos os valores informados e calculados passam a usá-la. Sem escolha, aparece o sinal genérico de moeda (¤).':
        ('Choose the project currency: every value you enter and every result uses it. Until you choose, the generic currency sign (¤) is shown.',
         'Elija la moneda del proyecto: todos los valores introducidos y calculados la usan. Sin elección, se muestra el signo genérico de moneda (¤).',
         '请选择项目货币：所有输入值与计算结果都将使用该货币。未选择时显示通用货币符号（¤）。'),
    # ── Perfis econômicos da Etapa 4 (genéricos) ────────────────────────────────────────────
    'Valor genérico de referência; substitua pela inflação esperada no local e no período do projeto.':
        ('Generic reference value; replace it with the inflation expected at the site and over the period of the project.',
         'Valor genérico de referencia; sustitúyalo por la inflación esperada en el lugar y en el periodo del proyecto.',
         '通用参考值；请替换为项目所在地及项目期内的预期通胀率。'),
    'Inflação genérica baixa — 2,0% a.a. (O&M)': ('Generic low inflation — 2.0% p.a. (O&M)', 'Inflación genérica baja — 2,0% anual (O&M)', '通用低通胀 — 每年 2.0%（运维）'),
    'Inflação genérica moderada — 3,0% a.a. (O&M)': ('Generic moderate inflation — 3.0% p.a. (O&M)', 'Inflación genérica moderada — 3,0% anual (O&M)', '通用中等通胀 — 每年 3.0%（运维）'),
    'Inflação genérica alta — 4,5% a.a. (O&M)': ('Generic high inflation — 4.5% p.a. (O&M)', 'Inflación genérica alta — 4,5% anual (O&M)', '通用高通胀 — 每年 4.5%（运维）'),
    'Inflação genérica muito alta — 6,0% a.a. (O&M)': ('Generic very high inflation — 6.0% p.a. (O&M)', 'Inflación genérica muy alta — 6,0% anual (O&M)', '通用极高通胀 — 每年 6.0%（运维）'),
    'Taxa de desconto baixa — 6,0% a.a.': ('Low discount rate — 6.0% p.a.', 'Tasa de descuento baja — 6,0% anual', '低贴现率 — 每年 6.0%'),
    'Custo de oportunidade elevado — 14,0% a.a.': ('High opportunity cost — 14.0% p.a.', 'Costo de oportunidad elevado — 14,0% anual', '较高机会成本 — 每年 14.0%'),
    'Reajuste baixo — água 4,5%; energia 3,5% a.a.': ('Low adjustment — water 4.5%; electricity 3.5% p.a.', 'Reajuste bajo — agua 4,5%; energía 3,5% anual', '低调价 — 水费 4.5%；电费 3.5%（每年）'),
    'Reajuste médio — água/saneamento 5,0%; energia 6,0% a.a.': ('Medium adjustment — water/sewerage 5.0%; electricity 6.0% p.a.', 'Reajuste medio — agua/saneamiento 5,0%; energía 6,0% anual', '中等调价 — 水费/污水费 5.0%；电费 6.0%（每年）'),
    # ── Normas e referências por edição ─────────────────────────────────────────────────────
    '🎯 Tipologia & Padrão de Referência da Edificação': ('🎯 Building Typology & Reference Standard', '🎯 Tipología y estándar de referencia de la edificación', '🎯 建筑类型与参考标准'),
    '📋 B. Classe de Uso Final e Parâmetros da Qualidade': ('📋 B. End-Use Class and Quality Parameters', '📋 B. Clase de uso final y parámetros de calidad', '📋 B. 终端用途等级与水质参数'),
    'Análise do impacto físico do descarte de primeira chuva (wash-off), metas de qualidade da água de uso final e dimensionamento paramétrico de filtros mecânicos, desinfecção e polimento.':
        ('Analysis of the physical impact of the first-flush discard (wash-off), end-use water quality targets and parametric sizing of mechanical filters, disinfection and polishing.',
         'Análisis del impacto físico del descarte de la primera lluvia (wash-off), metas de calidad del agua de uso final y dimensionamiento paramétrico de filtros mecánicos, desinfección y pulido.',
         '分析初期雨水弃流（冲刷）的物理影响、终端用水水质目标，并对机械过滤、消毒与精处理进行参数化设计。'),
    'A classe selecionada recomenda filtração fina. A recomendação é do programa, e não de uma norma — as classes 2 a 4 são adaptadas. Sem o filtro, o investimento e o custeio da linha de tratamento não o incluem.':
        ('The selected class recommends fine filtration. The recommendation comes from the program, not from a standard: classes 2 to 4 are adapted. Without the filter, the investment and running cost of the treatment line do not include it.',
         'La clase seleccionada recomienda filtración fina. La recomendación es del programa y no de una norma: las clases 2 a 4 son adaptadas. Sin el filtro, la inversión y el costo de la línea de tratamiento no lo incluyen.',
         '所选等级建议采用精细过滤。该建议来自程序而非标准：2 至 4 级为改编等级。不设该过滤器时，处理线的投资与运行成本不含此项。'),
    "<span style='color: #ea580c;'>⚠️ Dosagem baixa (< 0,5 mg/L). Risco de residual livre insuficiente.</span>":
        ("<span style='color: #ea580c;'>⚠️ Low dose (< 0.5 mg/L). Risk of insufficient free residual.</span>",
         "<span style='color: #ea580c;'>⚠️ Dosis baja (< 0,5 mg/L). Riesgo de residual libre insuficiente.</span>",
         "<span style='color: #ea580c;'>⚠️ 投加量偏低（< 0.5 mg/L）。游离余氯可能不足。</span>"),
    "<span style='color: #16a34a;'>✅ Atende plenamente à faixa de referência (Residual livre esperado: 0,5 a 2,0 mg/L).</span>":
        ("<span style='color: #16a34a;'>✅ Fully within the reference range (expected free residual: 0.5 to 2.0 mg/L).</span>",
         "<span style='color: #16a34a;'>✅ Cumple plenamente el rango de referencia (residual libre esperado: 0,5 a 2,0 mg/L).</span>",
         "<span style='color: #16a34a;'>✅ 完全符合参考范围（预期游离余氯：0.5 至 2.0 mg/L）。</span>"),
    '📐 Prancha Técnica Completa em A3': ('📐 Complete A3 Technical Sheet', '📐 Lámina técnica completa en A3', '📐 完整 A3 技术图纸'),
    'Prancha Técnica A3': ('A3 Technical Sheet', 'Lámina técnica A3', 'A3 技术图纸'),

    # ── ACV: água substituída (fora da Brasil) ─────────────────────────────────────────────
    'Rede pública, com fator informado pelo usuário': ('Mains supply, with a user-supplied factor', 'Red pública, con factor informado por el usuario', '公共供水管网，由用户输入排放因子'),
    'Personalizada (digite o fator acima)': ('Custom (type the factor above)', 'Personalizada (escriba el factor arriba)', '自定义（在上方输入因子）'),
    "<b>Qual água o sistema substitui?</b> O CO₂ evitado por m³ não é uma constante do sistema pluvial: é propriedade da água que ele deixa de consumir. Substituir água dessalinizada vale dezenas de vezes mais do que substituir água de manancial tratada por gravidade.<br><br>O ideal é <b>informar o fator da água de rede do seu local</b> (kg CO₂e/m³ entregue na edificação), obtido da entidade que abastece o projeto ou de um inventário local. Na falta dele, escolha abaixo uma rota publicada que se aproxime do tratamento do seu local, ou digite um valor personalizado. Cada rota declara fonte, tecnologia, matriz elétrica e fronteira do sistema.":
        ("<b>Which water does the system replace?</b> The CO₂ avoided per m³ is not a constant of the rainwater system: it is a property of the water it stops consuming. Replacing desalinated water is worth tens of times more than replacing gravity-fed, treated source water.<br><br>The best option is to <b>enter the mains-water factor of your site</b> (kg CO₂e per m³ delivered to the building), taken from the utility that serves the project or from a local inventory. Failing that, choose below a published route close to the treatment at your site, or type a custom value. Each route states its source, technology, electricity mix and system boundary.",
         "<b>¿Qué agua sustituye el sistema?</b> El CO₂ evitado por m³ no es una constante del sistema pluvial: es una propiedad del agua que deja de consumirse. Sustituir agua desalinizada vale decenas de veces más que sustituir agua de fuente tratada por gravedad.<br><br>Lo ideal es <b>informar el factor del agua de red de su lugar</b> (kg CO₂e por m³ entregado en el edificio), obtenido de la entidad que abastece el proyecto o de un inventario local. A falta de él, elija abajo una ruta publicada cercana al tratamiento de su lugar, o escriba un valor personalizado. Cada ruta declara su fuente, tecnología, matriz eléctrica y frontera del sistema.",
         "<b>系统替代的是哪种水？</b>每立方米避免的 CO₂ 并非雨水系统的常数，而取决于被替代的水。替代海水淡化水的价值比替代重力供水的处理水高出数十倍。<br><br>最佳做法是<b>输入项目所在地的公共供水因子</b>（送到建筑的每立方米 kg CO₂e），数据来自供水机构或本地清单。若没有，请在下方选择与当地处理方式相近的已发表路线，或输入自定义数值。每条路线均注明来源、技术、电力结构与系统边界。"),
    'O fator da água de rede é o que estiver no campo «Abatimento Água Potável» acima. Informe o valor do seu local, em kg CO2e por m³ entregue na edificação (produção, produtos químicos, infraestrutura e distribuição).':
        ('The mains-water factor is whatever is in the «Potable-Water Offset» field above. Enter the value for your site, in kg CO2e per m³ delivered to the building (production, chemicals, infrastructure and distribution).',
         'El factor del agua de red es el que figure en el campo «Abatimiento de agua potable» de arriba. Introduzca el valor de su lugar, en kg CO2e por m³ entregado en el edificio (producción, productos químicos, infraestructura y distribución).',
         '公共供水因子即上方“饮用水替代减排量”字段中的数值。请输入项目所在地的数值，单位为送到建筑的每立方米 kg CO2e（含生产、化学品、基础设施与配水）。'),

    # ── Documentação (fora da Brasil) ───────────────────────────────────────────────────────
    'Certificações Sustentáveis & Critérios ESG (LEED, EDGE, GRI)':
        ('Sustainability Certifications & ESG Criteria (LEED, EDGE, GRI)', 'Certificaciones de sostenibilidad y criterios ESG (LEED, EDGE, GRI)', '可持续认证与 ESG 标准（LEED、EDGE、GRI）'),

    # ── Menu e janela principal ─────────────────────────────────────────────────────────────
    'Descartar o projeto atual e começar um novo? As alterações não salvas serão perdidas.':
        ('Discard the current project and start a new one? Unsaved changes will be lost.', '¿Descartar el proyecto actual y empezar uno nuevo? Los cambios no guardados se perderán.', '放弃当前项目并新建项目？未保存的更改将丢失。'),
    'Software de computador, versão': ('Computer software, version', 'Software, versión', '计算机软件，版本'),
    'Referência recomendada': ('Recommended reference', 'Referencia recomendada', '推荐引用格式'),
    'Versão científica e operacional com modelagem diária YAS, análise de ciclo de vida (ACV) e tomada de decisão multicritério (TOPSIS/SMAA-VIKOR).':
        ('Scientific and operational version with daily YAS modelling, life cycle assessment (LCA) and multi-criteria decision-making (TOPSIS/SMAA-VIKOR).',
         'Versión científica y operativa con modelado diario YAS, análisis de ciclo de vida (ACV) y toma de decisiones multicriterio (TOPSIS/SMAA-VIKOR).',
         '科学与实用版本：逐日 YAS 建模、生命周期评价（ACV）与多准则决策（TOPSIS/SMAA-VIKOR）。'),
    '🇵🇹 Português (Portugal)': ('🇵🇹 Portuguese (Portugal)', '🇵🇹 Portugués (Portugal)', '🇵🇹 葡萄牙语（葡萄牙）'),

    # ── UI-14: cadeias que a interface em inglês deixava em português ───────────────────────
    '🌿 Detalhamento de Custos': ('🌿 Cost Breakdown', '🌿 Desglose de costos', '🌿 成本明细'),
    'PRCPTOT Médio Anual': ('Mean Annual PRCPTOT', 'PRCPTOT medio anual', '年均 PRCPTOT'),
    'R95p Médio Anual': ('Mean Annual R95p', 'R95p medio anual', '年均 R95p'),
    'SDII Médio Anual': ('Mean Annual SDII', 'SDII medio anual', '年均 SDII'),
    'CWD Médio (Chuvosos)': ('Mean CWD (Wet Spells)', 'CWD medio (rachas lluviosas)', '平均 CWD（连续降雨日）'),
    'Máximo de dias secos consecutivos (<1mm) (dias)': ('Maximum consecutive dry days (<1 mm) (days)', 'Máximo de días secos consecutivos (<1 mm) (días)', '最大连续干旱日数（<1 mm）（天）'),
    'Máximo de dias chuvosos consecutivos (≥1mm) (dias)': ('Maximum consecutive wet days (≥1 mm) (days)', 'Máximo de días lluviosos consecutivos (≥1 mm) (días)', '最大连续降雨日数（≥1 mm）（天）'),
    '🏠 Residencial Unifamiliar — Padrão Médio (150 L/hab/dia | 65% Potável | Jardim 15 m²)':
        ('🏠 Single-Family Residential — Medium Standard (150 L/person/day | 65% Potable | 15 m² Garden)', '🏠 Residencial unifamiliar — estándar medio (150 L/hab/día | 65% potable | jardín 15 m²)', '🏠 独户住宅 — 中等标准（150 升/人/天 | 65% 饮用水 | 花园 15 m²）'),
    '🏡 Residencial Unifamiliar — Econômico / Popular (120 L/hab/dia | 68% Potável | Jardim 10 m²)':
        ('🏡 Single-Family Residential — Economy / Affordable (120 L/person/day | 68% Potable | 10 m² Garden)', '🏡 Residencial unifamiliar — económico / popular (120 L/hab/día | 68% potable | jardín 10 m²)', '🏡 独户住宅 — 经济型（120 升/人/天 | 68% 饮用水 | 花园 10 m²）'),
    '🏰 Residencial Unifamiliar — Alto Padrão (220 L/hab/dia | 60% Potável | Jardim 30 m²)':
        ('🏰 Single-Family Residential — High Standard (220 L/person/day | 60% Potable | 30 m² Garden)', '🏰 Residencial unifamiliar — alto estándar (220 L/hab/día | 60% potable | jardín 30 m²)', '🏰 独户住宅 — 高标准（220 升/人/天 | 60% 饮用水 | 花园 30 m²）'),
    '🏢 Edifício Residencial Multifamiliar / Apartamentos (140 L/hab/dia | 65% Potável | Sem rega privativa)':
        ('🏢 Multi-Family Residential Building / Apartments (140 L/person/day | 65% Potable | No private irrigation)', '🏢 Edificio residencial multifamiliar / apartamentos (140 L/hab/día | 65% potable | sin riego privado)', '🏢 多户住宅楼 / 公寓（140 升/人/天 | 65% 饮用水 | 无私人灌溉）'),
    '🏫 Escola / Creche / Educação (40 L/aluno/dia — Foco em Bebedouros, Merenda & Bacias)':
        ('🏫 School / Nursery / Education (40 L/pupil/day — Drinking Fountains, Meals & Toilets)', '🏫 Escuela / guardería / educación (40 L/alumno/día — bebederos, comedor e inodoros)', '🏫 学校 / 幼儿园 / 教育（40 升/学生/天 — 饮水点、餐食与便器）'),
    '🏥 Hospital / Clínica de Saúde (250 L/leito/dia — Esterilização, Higiene & Lavanderia)':
        ('🏥 Hospital / Health Clinic (250 L/bed/day — Sterilisation, Hygiene & Laundry)', '🏥 Hospital / clínica de salud (250 L/cama/día — esterilización, higiene y lavandería)', '🏥 医院 / 诊所（250 升/床/天 — 消毒、卫生与洗衣）'),
    'Classe 1: parâmetros mínimos de referência': ('Class 1: minimum reference parameters', 'Clase 1: parámetros mínimos de referencia', '1 级：最低参考参数'),
    '📊 Gráfico de Decisão Multi-Critério por Volume': ('📊 Multi-Criteria Decision Chart by Volume', '📊 Gráfico de decisión multicriterio por volumen', '📊 按体积的多准则决策图'),

    # ── Assistente de bombas fora da Brasil (modelos de referência, sem marca nem preço) ───────
    'Dimensiona o diâmetro econômico de recalque, adota sucção uma bitola acima e cruza com modelos de motobomba de referência.':
        ('Sizes the economic discharge diameter, adopts a suction pipe one size larger and matches reference pump models.', 'Dimensiona el diámetro económico de impulsión, adopta la succión un diámetro mayor y cruza con modelos de bomba de referencia.', '计算经济出水管径，吸水管取大一级，并与参考水泵型号匹配。'),
    'Modelo de referência A — 0,18 kW — Serviço leve': ('Reference model A — 0.18 kW — Light duty', 'Modelo de referencia A — 0,18 kW — Servicio ligero', '参考型号 A — 0.18 kW — 轻载'),
    'Modelo de referência B — 0,25 kW — Serviço padrão': ('Reference model B — 0.25 kW — Standard duty', 'Modelo de referencia B — 0,25 kW — Servicio estándar', '参考型号 B — 0.25 kW — 标准载荷'),
    'Modelo de referência C — 0,37 kW — Centrífuga de vazão média': ('Reference model C — 0.37 kW — Medium-flow centrifugal', 'Modelo de referencia C — 0,37 kW — Centrífuga de caudal medio', '参考型号 C — 0.37 kW — 中流量离心泵'),
    'Modelo de referência D — 0,55 kW — Média elevação': ('Reference model D — 0.55 kW — Medium head', 'Modelo de referencia D — 0,55 kW — Elevación media', '参考型号 D — 0.55 kW — 中扬程'),
    'Modelo de referência E — 2,20 kW — Multiestágio de alta pressão': ('Reference model E — 2.20 kW — High-pressure multistage', 'Modelo de referencia E — 2,20 kW — Multietapa de alta presión', '参考型号 E — 2.20 kW — 高压多级泵'),
    'Modelo de referência A': ('Reference model A', 'Modelo de referencia A', '参考型号 A'),
    'Modelo de referência B': ('Reference model B', 'Modelo de referencia B', '参考型号 B'),
    'Modelo de referência C': ('Reference model C', 'Modelo de referencia C', '参考型号 C'),
    'Modelo de referência D': ('Reference model D', 'Modelo de referencia D', '参考型号 D'),
    'Modelo de referência E': ('Reference model E', 'Modelo de referencia E', '参考型号 E'),
    'Poliéster Reforçado com Fibra de Vidro (PRFV)': ('Glass-Fibre Reinforced Polyester (GRP)', 'Poliéster reforzado con fibra de vidrio (PRFV)', '玻璃纤维增强聚酯（玻璃钢）'),
    'Tubo PVC DN 20 (Sucção/Recalque) (m):': ('PVC pipe DN 20 (suction/discharge) (m):', 'Tubo PVC DN 20 (succión/impulsión) (m):', 'PVC 管 DN 20（吸水/出水）（m）：'),
    'Tubo PVC DN 25 (Sucção/Recalque) (m):': ('PVC pipe DN 25 (suction/discharge) (m):', 'Tubo PVC DN 25 (succión/impulsión) (m):', 'PVC 管 DN 25（吸水/出水）（m）：'),
    'Tubo PVC DN 32 (Sucção/Recalque) (m):': ('PVC pipe DN 32 (suction/discharge) (m):', 'Tubo PVC DN 32 (succión/impulsión) (m):', 'PVC 管 DN 32（吸水/出水）（m）：'),
    'Tubo PVC DN 40 (Sucção/Recalque) (m):': ('PVC pipe DN 40 (suction/discharge) (m):', 'Tubo PVC DN 40 (succión/impulsión) (m):', 'PVC 管 DN 40（吸水/出水）（m）：'),
    'Tubo PVC DN 100 (Captação/Extrav.) (m):': ('PVC pipe DN 100 (collection/overflow) (m):', 'Tubo PVC DN 100 (captación/rebose) (m):', 'PVC 管 DN 100（集水/溢流）（m）：'),
    'Tubulação PVC DN 60 mm (m):': ('PVC pipe DN 60 mm (m):', 'Tubería PVC DN 60 mm (m):', 'PVC 管 DN 60 mm（m）：'),
    'Tubulação PVC DN 85 mm (m):': ('PVC pipe DN 85 mm (m):', 'Tubería PVC DN 85 mm (m):', 'PVC 管 DN 85 mm（m）：'),
    'Tubulação PVC DN 110 mm (m):': ('PVC pipe DN 110 mm (m):', 'Tubería PVC DN 110 mm (m):', 'PVC 管 DN 110 mm（m）：'),
    '📌 Modelo de Referência: {0}': ('📌 Reference Model: {0}', '📌 Modelo de referencia: {0}', '📌 参考型号：{0}'),

    # ── Motor, tubulação e regime de cobrança (fora da Brasil) ─────────────────────────────
    'Rendimento do motor (%, em branco usa o valor típico da potência):':
        ('Motor efficiency (%, blank uses the typical value for the power):', 'Rendimiento del motor (%, en blanco usa el valor típico de la potencia):', '电机效率（%，留空则采用该功率的典型值）：'),
    'A potência de placa é a potência mecânica no eixo, e o rendimento do motor é uma grandeza separada. Em branco, o programa adota um rendimento típico para a potência escolhida: cerca de 60% em meio CV e 69% em um CV.':
        ('Nameplate power is the mechanical power at the shaft, and motor efficiency is a separate quantity. If left blank, the program adopts a typical efficiency for the selected power: about 60% at half a horsepower and 69% at one horsepower.',
         'La potencia de placa es la potencia mecánica en el eje, y el rendimiento del motor es una magnitud aparte. En blanco, el programa adopta un rendimiento típico para la potencia elegida: cerca de 60% en medio CV y 69% en un CV.',
         '铭牌功率是轴上的机械功率，电机效率是另一项独立的量。留空时，程序按所选功率采用典型效率：半马力约 60%，一马力约 69%。'),
    'Modelos com curva de catálogo publicada pelo fabricante. A energia é o tempo ligado vezes a potência elétrica: a potência de placa dividida pelo rendimento do motor.':
        ('Models with a catalogue curve published by the manufacturer. Energy is the on-time times the electric power: the nameplate power divided by the motor efficiency.',
         'Modelos con curva de catálogo publicada por el fabricante. La energía es el tiempo encendido por la potencia eléctrica: la potencia de placa dividida por el rendimiento del motor.',
         '厂家公布了样本曲线的型号。能耗为运行时间乘以电功率：铭牌功率除以电机效率。'),
    'Potência de placa, que é mecânica, no eixo. O programa a divide pelo rendimento do motor para chegar à potência elétrica.':
        ('Nameplate power, which is mechanical, at the shaft. The program divides it by the motor efficiency to get the electric power.',
         'Potencia de placa, que es mecánica, en el eje. El programa la divide por el rendimiento del motor para obtener la potencia eléctrica.',
         '铭牌功率为轴上的机械功率。程序将其除以电机效率，得到电功率。'),
    '💡 <b>Custos de Referência:</b> Tubulações comerciais de PVC de água fria (DN 20 a 110 mm) e pluviais (DN 100 e 150 mm) com acréscimo de 25% para conexões e registros. Informe os preços unitários do seu fornecedor.<br>Os comprimentos informados aqui são automaticamente sincronizados com o Módulo Ambiental (ACV).':
        ('💡 <b>Reference costs:</b> Commercial cold-water PVC pipes (DN 20 to 110 mm) and rainwater pipes (DN 100 and 150 mm) with a 25% allowance for fittings and valves. Enter the unit prices of your supplier.<br>The lengths entered here are automatically synchronised with the Environmental Module (LCA).',
         '💡 <b>Costos de referencia:</b> Tuberías comerciales de PVC para agua fría (DN 20 a 110 mm) y pluviales (DN 100 y 150 mm) con un 25% adicional para conexiones y válvulas. Introduzca los precios unitarios de su proveedor.<br>Las longitudes introducidas aquí se sincronizan automáticamente con el Módulo Ambiental (ACV).',
         '💡 <b>参考成本：</b>商用冷水 PVC 管（DN 20 至 110 mm）与雨水管（DN 100 和 150 mm），管件与阀门按 25% 附加。请输入您的供应商单价。<br>此处输入的长度会自动同步到环境模块（ACV）。'),
    'Subtotal Calculado de Tubulações (conexões incluídas):': ('Calculated Piping Subtotal (fittings included):', 'Subtotal calculado de tuberías (conexiones incluidas):', '管道计算小计（含管件）：'),
    '💧 <b>Regime de cobrança:</b> defina você mesmo. Se a sua entidade de abastecimento cobra um mínimo que já dá direito a alguns m³, lance-o como faixa de R$ 0,00/m³ até esse volume: abaixo dele economizar água não reduz a conta.':
        ('💧 <b>Billing regime:</b> define it yourself. If your water supplier charges a minimum that already entitles you to some m³, enter it as a band of R$ 0.00/m³ up to that volume: below it, saving water does not reduce the bill.',
         '💧 <b>Régimen de cobro:</b> defínalo usted mismo. Si su proveedor de agua cobra un mínimo que ya da derecho a algunos m³, regístrelo como un tramo de R$ 0,00/m³ hasta ese volumen: por debajo de él, ahorrar agua no reduce la factura.',
         '💧 <b>计费方式：</b>请自行设定。若供水单位收取的最低费用已包含若干 m³，请将其录为至该水量的 R$ 0.00/m³ 档：低于该水量时，节水不会减少账单。'),

    # ── Tooltip das justificativas de ACV ──────────────────────────────────────────────────
    '🔍 Explicação Detalhada:': ('🔍 Detailed Explanation:', '🔍 Explicación detallada:', '🔍 详细说明：'),
    '📐 Base do Cálculo:': ('📐 Calculation Basis:', '📐 Base del cálculo:', '📐 计算依据：'),
    '📚 Referência:': ('📚 Reference:', '📚 Referencia:', '📚 参考文献：'),
    '📌 Notas:': ('📌 Notes:', '📌 Notas:', '📌 说明：'),
}
