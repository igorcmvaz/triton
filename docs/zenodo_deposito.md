# Depósito Científico do Software Triton no Zenodo
# Zenodo Scientific Software Deposit Package

Este documento contém os metadados cadastrais, a descrição científica e as instruções de citação estruturadas para o depósito e atribuição de DOI do software **Triton** no repositório aberto **Zenodo** (CERN / OpenAIRE).

O texto da descrição está apresentado em **Português (pt-BR)** e em **Inglês (en-GB)**, em conformidade com as diretrizes de FAIR Data e preservação digital de software acadêmico.

---

## 1. Metadados Gerais do Depósito / General Deposit Metadata

| Campo / Field | Valor / Value |
| :--- | :--- |
| **Title / Título** | Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings (Editions: Brasil, International, and Ibérica) |
| **Publication Date / Data de Publicação** | 2026-11-11 (versão 0.2.0; a 0.1.0 foi publicada em 2026-11-03) |
| **Resource Type / Tipo de Recurso** | Software |
| **Authors / Autores** | **Vaz, Igor Catão Martins** (UFSC - Universidade Federal de Santa Catarina, Departamento de Engenharia Civil, Grupo de Pesquisa em Ambientes Sustentáveis)<br>**Ghisi, Enedir** (UFSC - Universidade Federal de Santa Catarina, Departamento de Engenharia Civil, Grupo de Pesquisa em Ambientes Sustentáveis) |
| **License / Licença** | Other (Non-Commercial): licença acadêmica de código-fonte disponível, todos os direitos reservados, uso não comercial; texto integral em `LICENSE.md` (cada edição). NÃO é GPL |
| **Access / Acesso** | Open Access (Acesso Aberto) |
| **Digital Object Identifier (DOI)** | Todas as versões: 10.5281/zenodo.23402915. A 0.1.0: 10.5281/zenodo.23402916. A 0.2.0 recebe o DOI de versão ao ser publicada como nova versão do mesmo registro. |
| **Language / Idioma** | Multilingual (pt-BR, en-GB, es, zh) |
| **Related Identifiers / Identificadores Relacionados** | - IsSupplementTo / IsDocumentedBy: Manual do Usuário Triton (UFSC, 2026)<br>- Continues / IsNewVersionOf: Netuno (Software de Aproveitamento de Água de Chuva em Edifícios - Netuno 4, UFSC)<br>- References: NBR 15527 (ABNT); EN 16941-1 (CEN); CLIMBra CMIP6 (UFSC/INPE); Iberia01; E-OBS |
| **Communities / Comunidades Zenodo** | - ufsc: Universidade Federal de Santa Catarina<br>- water-management: Sustainable Water Resource Management & Building Hydrology<br>- `building-sustainability`: Architecture, Civil Engineering & Urban Sustainability |
| **Keywords / Palavras-chave** | rainwater harvesting; building hydrology; yield-after-spill; life-cycle assessment; multi-criteria decision-making; topsis; vikor; smaa-vikor; promethee; engineering economics; climate change; cmip6; water conservation; netuno; aproveitamento de água pluvial |

---

## 2. Descrição para o Zenodo em Português (pt-BR)

### Resumo (Abstract)
O **Triton** é uma plataforma computacional científica de alta precisão desenvolvida pelo Grupo de Pesquisa em Ambientes Sustentáveis da Universidade Federal de Santa Catarina (UFSC), atuando como o sucessor tecnológico do amplamente difundido programa **Netuno** (tendo o Netuno 4 como referência primária de validação de balanço hídrico). O Triton foi concebido para modelar, simular, dimensionar e otimizar sistemas prediais de aproveitamento de água de chuva (pluvial), integrando hidrologia diária contínua, engenharia econômica detalhada, avaliação simplificada do ciclo de vida (ACV) e métodos científicos avançados de apoio à tomada de decisão multicritério (MCDA).

A plataforma é distribuída em três edições compartilhando o mesmo núcleo de cálculo validado (`triton-core`):
1. **Triton Brasil (BRL):** Especializada na realidade técnica, tarifária e climática brasileira. Incorpora malha de dados pluviométricos de alta resolução do CLIMBra (CMIP6: histórico e projeções de cenários de mudanças climáticas SSP2-4.5 e SSP5-8.5), catálogo de estruturas tarifárias auditadas de abastecimento de água e esgotamento sanitário para 652 municípios brasileiros, base de custos prediais de reservatórios em Reais (R$), normas brasileiras (ABNT NBR 15527, NBR 5626) e modelagem de estações de tratamento de água de chuva (ETAP / cloração conforme Portaria GM/MS 888/2021).
2. **Triton Ibérica (IBE):** Voltada para Portugal e a Península Ibérica, com dados de precipitação diária de alta resolução provenientes das bases E-OBS e Iberia01, regulamentação técnica em Português de Portugal (terminologias normalizadas como VAL, VPL, autossuficiência, autoclismos), estruturas tarifárias auditadas de entidades gestoras portuguesas (ERSAR) em Euros (€) e conformidade com a norma europeia EN 16941-1.
3. **Triton Internacional (INT):** Versão neutra geograficamente e totalmente flexível, permitindo importação customizada de séries de precipitação diária globais, parametrização aberta de moedas, taxas de juros, inflação e escalonamentos tarifários, e interface multilíngue (Português, Inglês, Espanhol e Mandarim).

### Principais Módulos Científicos

1. **Balanço Hídrico Diário (Algoritmo Yield-After-Spill - YAS):**
   - Simulação contínua dia a dia do reservatório inferior e superior de água pluvial.
   - Modelagem de descarte de primeiro escoamento (*first-flush*) com parametrização em volume ou lâmina (mm), desvio percentual e coeficientes de escoamento superficial (*runoff*) específicos por tipo de cobertura (NBR 15527).
   - Simulação de demandas não potáveis (bacias sanitárias, mictórios, irrigação de jardins, lavagem de pisos e veículos), incluindo modulação estocástica de demanda por Monte Carlo e supressão de irrigação em dias de chuva.
   - Determinação do volume ótimo de reservatório por varredura paramétrica técnica (critério de rendimento marginal decrescente $\Delta P \le \Delta_{ideal}$).

2. **Engenharia Econômica e Viabilidade Financeira:**
   - Cálculo rigoroso de fluxo de caixa em regime discreto anual e mensal.
   - Indicadores financeiros completos: Valor Presente Líquido (VPL / VAL), Taxa Interna de Retorno (TIR), *Payback* Simples, *Payback* Descontado, Custo Nivelado da Água (*Levelized Cost of Water* - LCOW) e Relação Benefício-Custo (B/C).
   - Tarifação escalonada em cascata (estruturas não lineares por blocos de consumo de água e esgoto), contemplando inflação setorial e taxas mínimas de disponibilidade.
   - Estimativa orçamentária detalhada: CAPEX (cisternas em PEAD, fibra de vidro ou concreto armado, caixa superior, bombas centrífugas/pressurizadores, tubulações, filtros e mão de obra) e OPEX (custos de bombeamento elétrico kwh/m³, manutenções preventivas, desinfecção e reposição periódica).

3. **Avaliação do Ciclo de Vida (ACV Simplificada):**
   - Quantificação de impactos ambientais associados ao sistema predial ao longo do ciclo de vida (berço ao túmulo / *cradle-to-grave*).
   - Indicadores de Potencial de Aquecimento Global (GWP em kg CO₂ eq), Energia Embutida Primária (MJ), emissões evitadas de água tratada da rede pública e consumo elétrico de bombeamento (fatores de emissão da matriz elétrica SIN/Brasil e REN/Portugal).

4. **Apoio à Decisão Multicritério (quatro métodos):**
   - Desde a 0.2.0, oito critérios em quatro eixos, escolhidos para não medir duas vezes a mesma água economizada: técnico (confiabilidade volumétrica; eficiência de armazenamento, a renovação diária do volume da cisterna), econômico (economia financeira líquida, custo nivelado da água — LCOW — e payback descontado), ambiental (CO₂e de ciclo de vida) e estrutural (massa a seco dos materiais, da calculadora de peso do sistema, e extravasamento anual). Pesos por eixo (padrão 25% cada), repartidos em partes iguais dentro do eixo, ou oito pesos diretos.
     - **TOPSIS (*Technique for Order of Preference by Similarity to Ideal Solution*):** proximidade relativa às soluções ideal e anti-ideal, com os pesos declarados; a normalização é uma variante da de Hwang e Yoon (translada cada critério pelo mínimo antes da normalização vetorial, para admitir VPL negativo).
     - **VIKOR (*VlseKriterijumska Optimizacija I Kompromisno Resenje*):** ordena pelo índice de compromisso *Q*, que combina a utilidade do grupo (*S*) e o arrependimento individual (*R*); as condições C1 e C2 de Opricovic e Tzeng não são avaliadas, de modo que a saída é uma ordenação.
     - **SMAA-VIKOR (*Stochastic Multicriteria Acceptability Analysis - VIKOR*):** 20.000 vetores de pesos sorteados no simplex (padrão), com a aceitabilidade de primeiro lugar de cada volume e os pesos centrais agregados nos quatro eixos.
     - **PROMETHEE II (*Preference Ranking Organization METHod for Enrichment Evaluations*):** superação por funções de preferência usual, linear ou gaussiana, com os fluxos positivo (Φ⁺), negativo (Φ⁻) e líquido (Φ = Φ⁺ − Φ⁻).

### Requisitos do Sistema e Instalação
- **Sistemas Operacionais Suportados:** Microsoft Windows 10 / 11 (64-bit).
- **Ambiente de Execução:** Python 3.10+ (ou executáveis compilados autônomos *standalone* sem necessidade de pré-instalação de dependências).
- **Dependências Principais:** PySide6 (Qt 6), NumPy, SciPy, Matplotlib.
- **Instalação:**
  - Usuários finais: Baixar o instalador executável correspondente (`Triton_Brasil_Setup_v0.2.0.exe`, `Triton_Iberica_Setup_v0.2.0.exe` ou `Triton_Internacional_Setup_v0.2.0.exe`) e executar o assistente passo a passo.
  - Desenvolvedores e pesquisadores: Clonar o repositório, criar ambiente virtual Python (python -m venv .venv) e instalar os pacotes via pip install -e triton_brl (ou `triton_int` / `triton_ibe`).

---

## 3. Zenodo Description in English (en-GB)

### Abstract
**Triton** is a state-of-the-art scientific computational platform developed by the Sustainable Environments Research Group at the Federal University of Santa Catarina (UFSC), Brazil. Serving as the next-generation successor to the widely recognised **Netuno** software (with Netuno 4 serving as the benchmark for water-balance validation), Triton is designed for the comprehensive design, daily continuous simulation, techno-economic feasibility analysis, life-cycle impact evaluation, and multi-criteria decision support of rainwater harvesting (RWH) systems in residential, commercial, and public buildings.

The platform is distributed across three specialized editions sharing a unified, mathematically verified calculation kernel (`triton-core`):
1. **Triton Brasil (BRL):** Tailored to Brazilian engineering practice, regulations (ABNT NBR 15527, NBR 5626), and environmental context. It incorporates high-resolution synthetic and observed rainfall records from the CLIMBra database (CMIP6: historical baseline and climate projection scenarios SSP2-4.5 and SSP5-8.5), audited water and sewerage progressive block tariffs for 652 Brazilian municipalities, cost estimation bases in Brazilian Reais (BRL / R$), and models for on-site rainwater treatment plants (ETAP / chlorination according to Ministry of Health Ordinance GM/MS 888/2021).
2. **Triton Ibérica (IBE):** Geared towards Portugal and the Iberian Peninsula, featuring daily gridded precipitation datasets from E-OBS and Iberia01, technical terminology in European Portuguese (e.g., VAL, autossuficiência, autoclismos), audited multi-tier utility tariffs from Portuguese regulatory authorities (ERSAR) in Euros (€), and alignment with European Standard EN 16941-1.
3. **Triton International (INT):** Region-neutral and globally configurable edition, supporting the import of user-defined daily rainfall time series, arbitrary currencies and financial parameters, and a multi-language graphical interface (English, Portuguese, Spanish, and Simplified Chinese).

### Key Scientific Capabilities

1. **Daily Continuous Water Balance (Yield-After-Spill Algorithm):**
   - Daily time-step tracking of rainwater storage dynamics across lower and upper cisterns.
   - Comprehensive first-flush diversion modelling (fixed depth in millimetres, proportional volume, or user-defined diversion rules) with catchment-specific runoff coefficients.
   - Detailed non-potable end-use demand allocation (toilet flushing, urinal flushing, landscape irrigation, vehicle washing, and general cleaning), supported by Monte Carlo stochastic daily demand perturbation and automated rain-triggered irrigation suppression.
   - Optimal storage capacity sizing through parametric marginal efficiency analysis ($\Delta P \le \Delta_{target}$).

2. **Engineering Economics & Life-Cycle Costing:**
   - Rigorous annual and monthly discounted cash flow analysis over custom building life spans.
   - Full suite of investment appraisal metrics: Net Present Value (NPV / VAL), Internal Rate of Return (IRR), Simple Payback Period, Discounted Payback Period, Levelized Cost of Water (LCOW), and Benefit-Cost Ratio (B/C).
   - Multi-tier, non-linear cascading tariff billing structures, incorporating differential inflation escalation rates for water, sewage, and grid electricity.
   - Granular Capital Expenditure (CAPEX) synthesis (HDPE, fibreglass, or reinforced concrete cisterns; booster pump sets; piping and filtration manifolds; installation labor) and Operational Expenditure (OPEX) accounting (pumping electricity kWh/m³, preventive maintenance, chemical disinfection).

3. **Simplified Life-Cycle Assessment (LCA):**
   - Cradle-to-grave environmental impact evaluation of RWH infrastructure.
   - Quantitative determination of Global Warming Potential (GWP in kg CO₂ eq) and Embodied Energy (MJ) across material extraction, component manufacturing, operation phase electricity consumption, and avoided mains potable water treatment burdens.

4. **Multi-Criteria Decision Analysis (four methods):**
   - Since 0.2.0, eight criteria in four dimensions, chosen so that the same water saving is not counted twice: technical (volumetric reliability; storage efficiency, the daily turnover of the cistern volume), economic (net financial savings, levelised cost of water — LCOW — and discounted payback), environmental (life-cycle CO₂e) and structural (dry mass of materials, from the system-weight calculator, and annual overflow). Weights per dimension (25% each by default), shared equally within each dimension, or eight direct weights.
     - **TOPSIS (*Technique for Order of Preference by Similarity to Ideal Solution*):** relative closeness to the ideal and anti-ideal solutions under the declared weights; the normalisation is a variant of Hwang and Yoon's (each criterion is shifted by its minimum before vector normalisation, so a negative NPV is admitted).
     - **VIKOR (*VlseKriterijumska Optimizacija I Kompromisno Resenje*):** ranks by the compromise index *Q*, which combines group utility (*S*) and individual regret (*R*); Opricovic and Tzeng's conditions C1 and C2 are not evaluated, so the output is a ranking.
     - **SMAA-VIKOR (*Stochastic Multicriteria Acceptability Analysis - VIKOR*):** 20,000 weight vectors drawn on the simplex (default), giving each volume's first-rank acceptability and the central weights aggregated into the four dimensions.
     - **PROMETHEE II (*Preference Ranking Organization METHod for Enrichment Evaluations*):** outranking with usual, linear or Gaussian preference functions, giving the positive (Φ⁺), negative (Φ⁻) and net (Φ = Φ⁺ − Φ⁻) flows.

### System Requirements & Installation
- **Operating Systems:** Microsoft Windows 10 / 11 (64-bit architecture).
- **Runtime Environment:** Python 3.10+ (or standalone pre-compiled executable installers requiring no prior dependencies).
- **Core Dependencies:** PySide6 (Qt 6), NumPy, SciPy, Matplotlib.
- **Installation Procedure:**
  - End Users: Download and run the appropriate executable installer (`Triton_Brasil_Setup_v0.2.0.exe`, `Triton_Iberica_Setup_v0.2.0.exe`, or `Triton_Internacional_Setup_v0.2.0.exe`).
  - Developers / Researchers: Clone the source repository, establish a Python virtual environment (python -m venv .venv), and perform editable installation via pip install -e triton_brl (or `triton_int` / `triton_ibe`).

---

## 4. Como Citar / How to Cite

### Citação ABNT (Brasil)
VAZ, Igor Catão Martins; GHISI, Enedir. **Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edifícios**. Versão 0.2.0. Florianópolis: Universidade Federal de Santa Catarina (UFSC), 2026. DOI: 10.5281/zenodo.23402916. Disponível em: https://github.com/igorcmvaz/triton.

### APA Citation (7th Edition)
Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings* (Version 0.2.0) [Computer software]. Universidade Federal de Santa Catarina (UFSC). https://doi.org/10.5281/zenodo.23402916

### BibTeX Entry
```bibtex
@software{vaz_ghisi_2026_triton,
  author       = {Vaz, Igor Catão Martins and Ghisi, Enedir},
  title        = {{Triton: Computational Platform for Rainwater Harvesting Simulation in Buildings}},
  month        = nov,
  year         = 2026,
  publisher    = {Zenodo},
  version      = {0.2.0},
  doi          = {10.5281/zenodo.23402915},
  url          = {https://github.com/igorcmvaz/triton},
  institution  = {Universidade Federal de Santa Catarina (UFSC)},
  organization = {Grupo de Pesquisa em Ambientes Sustentáveis, UFSC}
}
```

---

## 5. Arquivos Sugeridos para o Upload no Zenodo / Suggested Release Files

Ao criar o release no Zenodo, recomenda-se anexar:
1. `Triton_Brasil_Setup_v0.2.0.exe`: Instalador compilado da Edição Brasil.
2. `Triton_Iberica_Setup_v0.2.0.exe`: Instalador compilado da Edição Ibérica.
3. `Triton_Internacional_Setup_v0.2.0.exe`: Instalador compilado da Edição Internacional.
4. `triton-0.2.0-source.zip`: Arquivo compactado com o código-fonte integral de todas as edições, documentação técnica e suíte de testes automatizados.
5. CITATION.cff: Arquivo legível por máquina para indexação de citações no GitHub, Zotero e Zenodo.
6. README.md e LICENSE.md: termos da licença acadêmica de código-fonte disponível (uso não comercial, citação obrigatória, cláusula 4) e apresentação técnica do projeto.
