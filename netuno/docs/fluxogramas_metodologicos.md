# Atlas de fluxogramas metodológicos — Netuno 5.0.7

Este atlas representa a sequência efetivamente implementada no motor do Netuno. Os diagramas devem ser lidos em conjunto com as equações e limitações do [README](../../README.md), com as [premissas dependentes do volume](../../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md) e com a [verificação manual dos três casos](../../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md).

Os fluxogramas distinguem quatro tipos de elemento:

| Forma | Significado |
| --- | --- |
| Cilindro | dado de entrada, série ou inventário |
| Retângulo | transformação ou equação |
| Losango | decisão lógica |
| Retângulo arredondado | resultado, indicador ou critério de decisão |

As relações representam o software atual. Valores de custos, tarifas, doses e fatores ambientais continuam sendo premissas editáveis; o diagrama não os transforma em valores normativos.

## 1. Visão integrada da metodologia

Este é o encadeamento principal entre entradas, simulação e decisão. A capacidade inferior `V` é varrida; não se transfere automaticamente a ela a geometria de tubos, a potência da bomba ou o reservatório superior.

```mermaid
flowchart LR
    I[("Série diária de chuva<br/>edificação, demanda e sistema")] --> H["Chuva efetiva e captação<br/>Vcap,t = Pef,t · A · C"]
    H --> S["Balanço diário YAS<br/>para cada capacidade V"]
    S --> T(["Indicadores técnicos<br/>água, falhas, extravasamento e Δpotencial"])
    S --> B["Recalque e partidas<br/>energia por alternativa"]
    S --> Q["Água efetivamente usada<br/>cloro por alternativa"]

    C[("Preços, tarifas, O&M<br/>energia, horizonte e TMA")] --> E["Fluxo de caixa anual<br/>CAPEX + OPEX − receita evitada"]
    T --> E
    B --> E
    Q --> E
    E --> F(["VPL, TIR e paybacks"])

    L[("Materiais, quantitativos<br/>e fatores de emissão")] --> A["ACV de triagem<br/>incorporado + operação − crédito"]
    T --> A
    B --> A
    Q --> A
    A --> G(["CO2e líquido e<br/>payback ambiental"])

    T --> M["Matriz de decisão<br/>técnico · econômico · ambiental"]
    F --> M
    G --> M
    W[("Pesos TOPSIS")] --> M
    M --> R["Normalização, ideais<br/>D+, D−, score e gaps"]
    R --> O(["Ótimos técnico, econômico,<br/>ambiental e multicritério"])
    O --> VFY["Verificação reprodutível<br/>conta manual × sistema"]
```

Implementação principal: `simulation.py`, `cost_estimates.py`, `economic.py`, `environmental.py` e `topsis.py`.

## 2. Chuva efetiva e captação

O descarte implementado é um limiar legado. Quando a regra está ativa, chuva abaixo do limiar é zerada; ao atingir o limiar, a precipitação diária entra integralmente. Não se calcula `P − df`.

```mermaid
flowchart TB
    P[("Precipitação do dia Pₜ")] --> R{"Pₜ é maior que zero?"}
    R -->|"não"| Z["Pef,t = 0"]
    R -->|"sim"| M{"Modo de descarte"}

    M -->|"1 · todos os eventos"| A["Ativar descarte"]
    M -->|"2 · primeiro após estiagem"| E{"Chuva anterior menor que 1 mm?"}
    M -->|"3 · intervalo"| I{"Dias desde o último descarte<br/>≥ intervalo configurado?"}
    E -->|"sim"| A
    E -->|"não"| N["Não ativar descarte"]
    I -->|"sim"| A
    I -->|"não"| N

    A --> L{"Pₜ ≥ df?"}
    L -->|"não"| Z
    L -->|"sim"| U["Pef,t = Pₜ"]
    N --> U

    Z --> C["Vcap,t = Pef,t · A · C"]
    U --> C
    C --> O(["Volume captado no dia<br/>1 mm · 1 m² = 1 L"])
```

Equações:

```text
Pef,t = 0,  se a regra estiver ativa e Pt < df
Pef,t = Pt, caso contrário
Vcap,t = Pef,t × A × C
```

## 3. Balanço hídrico YAS — reservatório inferior único

No modelo *Yield After Spillage*, o limite do estoque e o extravasamento são calculados antes da retirada da demanda pluvial.

```mermaid
flowchart TB
    D[("Estado do início do dia<br/>Sₜ₋₁, Vcap,t, Dpluvial,t e capacidade V")] --> A["Água disponível<br/>Aprov,t = Sₜ₋₁ + Vcap,t"]
    A --> L["Limitar estoque<br/>Santes,t = min(V, Aprov,t)"]
    A --> X["Extravasamento<br/>Qextr,t = max(0, Aprov,t − V)"]
    L --> Q["Atendimento pluvial<br/>Qpluvial,t = min(Dpluvial,t, Santes,t)"]
    Q --> S["Estoque final<br/>Sₜ = Santes,t − Qpluvial,t"]
    Q --> P["Complemento potável<br/>Qpotável,t = Dtotal,t − Qpluvial,t"]
    Q --> F{"Demanda pluvial atendida?"}
    F -->|"integral"| FI(["Dia de atendimento pleno"])
    F -->|"parcial"| PA(["Dia de atendimento parcial"])
    F -->|"nula"| NU(["Dia de atendimento nulo"])
    S --> K["Próximo dia"]
    K --> D
```

Identidade de conservação verificada diariamente:

```text
estoque inicial + captação
= estoque final + consumo pluvial + extravasamento
```

## 4. Dois reservatórios e ciclo de recalque

O recalque é uma transferência interna: não cria nem remove água do balanço global. A água de chuva é consumida a partir do reservatório superior; quando ele chega ao limiar, o motor tenta transferir água do inferior.

```mermaid
flowchart TB
    I[("Início do dia<br/>Sinferior, Ssuperior e demanda pluvial")] --> C["Adicionar captação ao inferior<br/>e calcular extravasamento"]
    C --> N{"Ainda existe demanda<br/>pluvial a atender?"}
    N -->|"não"| O(["Fechar o dia e registrar estados"])
    N -->|"sim"| L{"Ssuperior acima<br/>do limiar?"}
    L -->|"sim"| U["Consumir até a demanda<br/>ou até alcançar o limiar"]
    U --> N
    L -->|"não"| B{"Há água no inferior e<br/>espaço no superior?"}
    B -->|"sim"| R["Recalcar<br/>Vrec = min(Sinferior, Vsuperior − Ssuperior)"]
    R --> K["Registrar uma partida<br/>e atualizar os dois estoques"]
    K --> U2["Consumir do superior"]
    U2 --> N
    B -->|"não"| Q{"Ainda há água<br/>no superior?"}
    Q -->|"sim"| U2
    Q -->|"não"| F["Complementar demanda restante<br/>com água potável"]
    F --> O
```

Energia anual associada à alternativa:

```text
trecalque = Vrecalcado,anual / vazão
tpartidas = npartidas,anual × tempo equivalente por partida
Ebomba = potência × (trecalque + tpartidas) / eficiência
```

## 5. Varredura de capacidades e ótimo técnico

Cada capacidade é simulada novamente para toda a série diária. O ótimo técnico não é o maior potencial absoluto: é o primeiro volume positivo cujo ganho marginal fica igual ou abaixo do limiar configurado.

```mermaid
flowchart TB
    I[("Vmax, passo solicitado e limiar gideal")] --> Q["Normalizar passo para cima<br/>ΔV = 250 · teto(passo/250)"]
    Q --> L{"teto(Vmax/ΔV) > 40<br/>capacidades positivas?"}
    L -->|"sim"| X["Dobrar o passo<br/>ΔV = 2 · ΔV"]
    X --> L
    L -->|"não"| G["Construir grade<br/>0, ΔV, 2ΔV, … e Vmax exato"]
    G --> C{"Vmax é múltiplo de ΔV?"}
    C -->|"não"| J["Preservar Vmax<br/>último intervalo menor"]
    C -->|"sim"| N["Selecionar próxima capacidade Vᵢ"]
    J --> N
    N --> S["Executar toda a simulação diária"]
    S --> P["Calcular potencialᵢ<br/>100 · Qpluvial / Dtotal"]
    P --> D{"É a alternativa de 0 L?"}
    D -->|"sim"| Z["g₀ = 0"]
    D -->|"não"| M["gᵢ = (potencialᵢ − potencialᵢ₋₁)<br/>/ ((Vᵢ − Vᵢ₋₁)/1000)"]
    Z --> R["Armazenar resultado"]
    M --> R
    R --> A{"Ainda há capacidades?"}
    A -->|"sim"| N
    A -->|"não"| T{"Existe Vᵢ > 0 com<br/>gᵢ ≤ gideal?"}
    T -->|"sim"| O(["Ótimo técnico = primeiro Vᵢ<br/>que satisfaz o limiar"])
    T -->|"não"| F(["Fallback = maior volume<br/>da grade simulada"])
```

O limite de 40 se refere às capacidades positivas; 0 L é a referência adicional sem cisterna. Como a grade é discreta, mudar o passo pode mudar o volume selecionado. Quando o intervalo terminal é menor, o ganho marginal usa a diferença real `Vᵢ − Vᵢ₋₁`.

## 6. Modelo econômico-financeiro

O modelo calcula custos e receitas para cada capacidade da varredura. A economia na fatura é calculada pela diferença real entre a fatura sem e com o aproveitamento pluvial, considerando as faixas de progressividade tarifária, alíquota de esgoto e parcela fixa homologadas para os 652 municípios brasileiros cadastrados. Todos os valores de tarifas, CAPEX e OPEX consideram tributos e impostos inclusos.

```mermaid
flowchart LR
    subgraph CAP["Investimento inicial (CAPEX)"]
        V[("Capacidade e material")] --> CI["Cisterna inferior<br/>interpolação da tabela × μmaterial"]
        U[("Reservatório superior")] --> CS["Custo superior"]
        B[("Potência e quantidade")] --> CB["Custo das bombas"]
        T[("DN 50, 75, 100, 150 mm<br/>e comprimentos reais")] --> CT["Rede de tubos SINAPI<br/>1,25 · Σ (Ld · cd)"]
        CI --> CA["Acessórios e automação<br/>painel, sensores e air gap"]
        CS --> CA
        CI --> MO["Mão de obra especializada<br/>max(piso; 30% materiais)"]
        CS --> MO
        CB --> MO
        CT --> MO
        CA --> MO
        UF[("Fator Regional UF<br/>55% mat + 30% MO + 15% frete")] --> REG["CAPEX_UF = f_UF · (Cmat + Clabor)"]
        CI --> REG
        CS --> REG
        CB --> REG
        CT --> REG
        CA --> REG
        MO --> REG
    end

    subgraph OP["Operação anual (OPEX)"]
        Q[("Água pluvial usada")] --> OM["Manutenção anual =<br/>Cmaint,base · f_UF"]
        Q --> CL["Cloração =<br/>m³ · dose / 1000 · preço_kg"]
        E[("Energia por alternativa<br/>0,45 kWh/m³ ou curva")] --> CE["Custo elétrico =<br/>kWh · Tarifa B1 ANEEL da UF"]
    end

    subgraph REV["Economia tarifária evitada (652 cidades)"]
        DT[("Demanda total e tabela<br/>progressiva da cidade/UF")] --> FS["Fatura sem aproveitamento<br/>água + αesgoto"]
        Q --> FC["Fatura com aproveitamento<br/>água + αesgoto"]
        DT --> FC
        FS --> DF["Economia anual = 12 · (Fbase − Fresidual)"]
        FC --> DF
    end

    REG --> CF["FC₀ = −CAPEX_UF"]
    OM --> FY["FCₜ = Economia anual<br/>− energia − manutenção − cloro"]
    CL --> FY
    CE --> FY
    DF --> FY
    CF --> IND["VPL = −CAPEX + Σ FCₜ/(1+TMA)ᵗ"]
    FY --> IND
    IND --> O(["VPL, TIR,<br/>payback simples, descontado e LCOW"])
```

O custo de tubulações é computado diretamente pelas composições oficiais SINAPI para PVC esgoto/água predial (DN 50: R$ 18,50/m; DN 75: R$ 28,00/m; DN 100: R$ 35,00/m; DN 150: R$ 68,00/m + 25% conexões/registros). Os comprimentos informados são automaticamente sincronizados com o módulo de Análise de Ciclo de Vida (ACV/CO2e). Na alternativa de `0 L`, o programa adota a referência sem sistema: CAPEX e OPEX associados são nulos.

## 7. Cloração: cálculo implementado e limite sanitário

O motor calcula a massa aplicada equivalente a Cl2 para custos e inventário ambiental. Ele não estima a demanda química real da água, que requer ensaio e residual medido após tempo de contato.

```mermaid
flowchart LR
    Q[("Água pluvial efetivamente<br/>consumida Qanual em m³")] --> H{"Tratamento por<br/>cloro habilitado?"}
    H -->|"não"| Z(["Massa, custo e CO2e<br/>de cloro iguais a zero"])
    H -->|"sim"| M["Massa aplicada<br/>mCl2 = Qanual · dose / 1000"]
    D[("Dose configurada<br/>mg Cl2/L")] --> M
    M --> C["Custo anual<br/>mCl2 · preço por kg"]
    P[("Preço do insumo<br/>R$/kg Cl2 equivalente")] --> C
    M --> E["Impacto anual<br/>mCl2 · fator do insumo"]
    F[("Fator do insumo<br/>kg CO2e/kg Cl2")] --> E
    M --> O(["Massa aplicada equivalente<br/>para cenário econômico e ambiental"])
    C --> O
    E --> O

    subgraph EXT["Fora do cálculo automático"]
        A[("Amostra de água, pH, turbidez,<br/>matéria orgânica e temperatura")] --> J["Ensaio com dose e<br/>tempo de contato definidos"]
        J --> R[("Residual de cloro medido")]
        R --> DR["Demanda real =<br/>dose aplicada − residual"]
    end
    DR -. "não inferida pela vazão ou pela cisterna" .-> O
```

Conversão dimensional:

```text
1 mg/L = 1 g/m³ = 0,001 kg/m³
mCl2 [kg/ano] = Qanual [m³/ano] × dose [mg/L] / 1000
```

## 8. ACV simplificada e fronteira ambiental

A ACV é uma triagem de carbono. Quantitativos e fatores devem ser substituídos por dados locais ou EPDs quando o estudo exigir representatividade de projeto.

```mermaid
flowchart LR
    subgraph EMB["Impactos incorporados · uma vez"]
        V[("Volume e material inferior")] --> MI["Massa inferior<br/>V · kg material/m³"]
        U[("Volume e material superior")] --> MS["Massa superior"]
        P[("Tubos por DN e comprimento")] --> TP["Σ comprimento · fatorDN"]
        B[("Bombas e quantidade")] --> PB["Fator unitário · quantidade"]
        MI --> EI["CO2e incorporado total"]
        MS --> EI
        TP --> EI
        PB --> EI
    end

    subgraph ANN["Operação · por ano"]
        K[("kWh da simulação")] --> EB["CO2e bomba = kWh · fator da rede"]
        Q[("m³ pluvial usado")] --> MQ["kg Cl2 = m³ · dose / 1000"]
        MQ --> EQ["CO2e tratamento = kg Cl2 · fator do insumo"]
        Q --> CR["CO2e evitado = m³ · fator da água potável"]
        EB --> SL["Saldo anual = evitado − bomba − tratamento"]
        EQ --> SL
        CR --> SL
    end

    EI --> LT["Saldo de vida = saldo anual · vida útil<br/>− CO2e incorporado"]
    SL --> LT
    EI --> PBENV["Payback ambiental = incorporado / saldo anual"]
    SL --> PBENV
    LT --> O(["CO2e líquido acumulado<br/>e viabilidade de triagem"])
    PBENV --> O
```

Condição de viabilidade usada: saldo anual positivo e payback ambiental menor ou igual à vida útil configurada. A alternativa de `0 L` é a referência sem sistema e recebe impactos nulos.

## 9. TOPSIS e diagnóstico da concessão

Os três critérios atuais são de benefício: água pluvial usada, VPL e CO2e líquido evitado. A translação de todas as colunas torna o cálculo invariável à origem da escala e permite valores negativos.

```mermaid
flowchart TB
    C[("Alternativas Vᵢ<br/>águaᵢ, VPLᵢ e CO2eᵢ")] --> X["Matriz de decisão X<br/>n alternativas × 3 critérios"]
    W[("Pesos não negativos")] --> WV{"Σ pesos é maior que zero?"}
    WV -->|"não"| ER(["Rejeitar configuração"])
    WV -->|"sim"| WN["Normalizar pesos<br/>wⱼ = pesoⱼ / Σ pesos"]
    X --> SH["Transladar colunas<br/>zᵢⱼ = xᵢⱼ − min(xⱼ)"]
    SH --> NR["Normalização vetorial<br/>rᵢⱼ = zᵢⱼ / √Σ z²"]
    WN --> WP["Matriz ponderada<br/>vᵢⱼ = rᵢⱼ · wⱼ"]
    NR --> WP
    WP --> ID["Ideais<br/>A+ = máximo; A− = mínimo"]
    ID --> DS["Distâncias euclidianas<br/>D+ᵢ e D−ᵢ"]
    DS --> SC["Proximidade relativa<br/>Cᵢ = D−ᵢ / (D+ᵢ + D−ᵢ)"]
    SC --> RK(["Ranking decrescente<br/>maior Cᵢ = melhor TOPSIS"])

    X --> GP["Gap independente dos pesos<br/>gᵢⱼ = (máx xⱼ − xᵢⱼ)/(máx xⱼ − mín xⱼ)"]
    GP --> PR["Converter em proximidade<br/>pᵢⱼ = 1 − gᵢⱼ"]
    PR --> DG(["Gráfico de proximidade ao ótimo<br/>100% = melhor; 0% = pior"])
    RK --> IN(["Interpretar solução agregada"])
    DG --> IN
```

O score responde aos pesos e à geometria normalizada do conjunto. O motor preserva os gaps para auditoria e a interface exibe `1 − gap`, respondendo à pergunta complementar: “quão próxima esta alternativa está do melhor observado em cada eixo, sem aplicar pesos?”.

## 10. Verificação interna e rastreabilidade

O estudo de referência refaz as contas a partir das entradas elementares e compara cada identidade com o campo retornado pelo motor. Isso detecta regressões computacionais, mas não constitui validação externa das premissas.

```mermaid
flowchart TB
    S[("Séries de chuva versionadas<br/>+ projetos .netuno + SHA-256")] --> G["Gerar três estudos de caso"]
    G --> M["Executar motor<br/>técnico, econômico, ACV e TOPSIS"]
    G --> H["Recompor equações manualmente<br/>com as mesmas entradas elementares"]
    M --> C["Comparar item a item<br/>resíduo = |manual − sistema|"]
    H --> C
    C --> T{"Resíduos dentro<br/>da tolerância?"}
    T -->|"não"| R["Investigar fórmula, unidade,<br/>ordem do balanço ou arredondamento"]
    R --> G
    T -->|"sim"| A["Executar testes automatizados<br/>e invariantes de conservação"]
    A --> P(["Relatórios regenerados<br/>e resultados reprodutíveis"])
    P --> L["Etapa externa ainda necessária:<br/>medições, cotações, ensaios e revisão profissional"]
```

## 11. Matriz de leitura dos resultados

```mermaid
flowchart LR
    V[("Todas as capacidades simuladas")] --> T["Ótimo técnico<br/>primeiro ganho marginal ≤ limiar"]
    V --> E["Ótimo econômico<br/>maior VPL"]
    V --> A["Ótimo ambiental<br/>maior CO2e líquido de vida"]
    V --> M["Ótimo TOPSIS<br/>maior proximidade relativa"]
    T --> C["Comparar os quatro volumes<br/>nas mesmas métricas e unidades"]
    E --> C
    A --> C
    M --> C
    C --> G{"Gaps do TOPSIS<br/>são pequenos nos três eixos?"}
    G -->|"sim"| P(["Solução próxima dos ótimos individuais"])
    G -->|"não"| Q(["Concessão relevante:<br/>explicitar eixo sacrificado e pesos"])
```

Uma recomendação publicável deve apresentar os quatro ótimos, os pesos, os três gaps da alternativa TOPSIS e uma análise de sensibilidade; não apenas o volume vencedor.
