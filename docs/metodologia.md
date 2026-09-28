# Metodologia, equações e fronteiras do modelo — Netuno 5

Este documento descreve o que o motor do Netuno efetivamente calcula: as equações
implementadas, as premissas que as sustentam e os limites além dos quais os resultados
não devem ser lidos.

**Documentos relacionados**

- [`verificacao_e_validacao.md`](verificacao_e_validacao.md) — o que foi verificado destas
  equações, com que método e com que limitações.
- [`../netuno/docs/fluxogramas_metodologicos.md`](../netuno/docs/fluxogramas_metodologicos.md) —
  os mesmos encadeamentos em forma de diagrama.
- [`../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md`](../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md) —
  detalhamento do que depende do volume da cisterna.

> **Premissas, não normas.** Valores de custos, tarifas, doses de cloro e fatores
> ambientais são premissas editáveis pelo usuário. O software não os transforma em
> valores normativos, e nenhum resultado substitui medição, certificação, projeto
> executivo ou revisão profissional das condições locais.

---

O Netuno é um modelo de apoio à decisão com passo diário. Suas saídas são condicionais às entradas; custos automáticos e fatores ambientais são **valores de triagem editáveis**, não cotações, normas de dimensionamento ou constantes universais. O arquivo `.netuno` registra as premissas necessárias à reprodução do cenário.

## 1. Chuva efetiva e captação

O descarte de primeira chuva `df` é uma lâmina **efetivamente subtraída** da precipitação do evento: a água descartada deixa de estar disponível para consumo. Nos dias em que a regra de descarte está ativa:

```text
Pef,t = max(0, Pt − df)     se a regra de descarte se aplica ao dia t
Pef,t = Pt                  caso contrário
Vcap,t = Pef,t × A × C
```

`Pt` e `Pef,t` estão em mm/dia, `A` em m², `C` é adimensional e `Vcap,t` resulta em litros, pois 1 mm sobre 1 m² equivale a 1 L.

### Quando a regra se aplica

O que varia entre os modos não é a fórmula, mas **em quais dias** ela é acionada:

| Modo | Regra | Aplicação |
| :--- | :--- | :--- |
| 1 | Todos os eventos | todo dia com `Pt > 0` |
| 2 | Primeiro evento após estiagem | dias com `Pt > 0` cujo dia anterior teve `Pt < 1 mm` |
| 3 | Periodicidade de manutenção | dias com `Pt > 0`, respeitado o intervalo mínimo configurado desde o último descarte |

Nos modos 2 e 3, os dias em que a regra não é acionada aproveitam a precipitação integral (`Pef,t = Pt`).

> **Diferença deliberada em relação ao Netuno 4.** O Netuno 4 tratava `df` como limiar do evento (aproveitando `Pt` integralmente sempre que `Pt ≥ df`). O Netuno 5 subtrai a lâmina, o que é fisicamente mais fiel: a água desviada para o dispositivo de descarte não chega à cisterna. A consequência é mensurável e está quantificada em [`verificacao_e_validacao.md`](verificacao_e_validacao.md) §5: o Netuno 5 estima, em média, **2,3 a 2,7 pontos percentuais menos** economia de água potável que o Netuno 4 sobre os 4.050 casos de referência. A decomposição de `verificacao_e_validacao.md` §5.4 atribui a esta mudança **1,36 pp, ou 50%**, da divergência do conjunto de Manaus e São Paulo; o critério de escolha do volume ótimo responde por 1,11 pp (41%) e o resíduo do balanço hídrico por 0,25 pp (9%). Estudos que comparem resultados das duas versões devem declarar esta diferença metodológica.

O parâmetro `df` é uma **lâmina** (mm), não o volume hidráulico do dispositivo físico de first flush (`A × df` litros); o dispositivo deve ser dimensionado separadamente.

## 2. Demanda e balanço YAS

A demanda tem duas parcelas. A interna é `Din,t = N × q`, em que `N` é o número de usuários e `q` a demanda per capita; se houver perfil mensal, o multiplicador do mês é aplicado ao respectivo dia. A externa (rega, lavagem de áreas externas) é um volume diário `Qex`, suspenso nos dias em que a chuva atinge o limiar (2 mm por padrão): `Dex,t = Qex` se `Pt < Plim`, e zero nos demais. A demanda total é `Dtot,t = Din,t + Dex,t`.

A solicitação pluvial é `Dpl,t = fin × Din,t + Dex,t`, em que `fin` é a fração não potável do consumo **interno**. A fração atendível **total**,

```text
f = (fin × Din + Qex) / (Din + Qex)
```

é derivada das duas e não é dado de entrada: a interface a mostra num campo que não se edita, e o arquivo a grava para leitura. Sem demanda externa, `f = fin`. Alterar `f` pela linha de comando (`--share`, `--set rainwater_share=…`) recalcula `fin`, mantida a externa; alterar `fin` ou `Qex` recalcula `f`; alterar as duas de forma incoerente é recusado. A regra fica em `netuno/core/fracao_atendivel.py`.

No reservatório inferior, o modelo *Yield After Spillage* (YAS) limita o estoque e calcula o extravasamento **antes** de retirar a demanda:

```text
Aprov,t = St−1 + Vcap,t
Santes,t = min(V, Aprov,t)
Extravasamento,t = max(0, Aprov,t − V)
Atendimento,t = min(Dpl,t, Santes,t)
St = Santes,t − Atendimento,t
```

Quando há reservatório superior, o recalque é uma transferência interna adicional, limitada pelos estoques, pelo volume superior e pelo limiar de acionamento. O balanço auditável dos dois reservatórios é `estoque inicial + captação = estoque final + consumo pluvial + extravasamento`.

O ótimo técnico é o primeiro ponto discreto, após ordenar os volumes, cujo ganho marginal `Δpotencial/ΔV` é menor ou igual ao limiar configurado. Ele é uma referência dependente do passo da varredura, não um ótimo contínuo.

#### Política da grade de volumes

O passo digitado é uma referência editável. Para evitar bloqueios e limitar o tempo de cálculo, o motor constrói a grade por uma regra única e reproduzível:

```text
ΔV0 = 250 × teto(ΔVsolicitado / 250)
enquanto teto(Vmáx / ΔV) > 40: ΔV = 2 × ΔV
grade = {0, ΔV, 2ΔV, ...} ∪ {Vmáx}
```

Assim, o passo efetivo é sempre múltiplo de 250 L e há no máximo 40 capacidades positivas; 0 L é uma referência adicional sem cisterna. O volume máximo informado pelo usuário nunca é descartado. Se ele não for múltiplo do passo efetivo, é incluído como último candidato e somente o intervalo terminal fica menor. O ganho marginal desse ponto usa o `ΔV` real entre as duas capacidades, não o passo nominal. A interface informa qualquer ajuste e grava o passo efetivo; o resultado interno e a CLI também devolvem `requested_step_l`, `effective_step_l` e `step_adjusted`.

Na sugestão climática, `Vmáx,bruto = 8 × SDII × A × C` é arredondado para baixo ao múltiplo de 250 L, de modo que a sugestão não ultrapasse essa referência de triagem. Essa sugestão não é uma norma de dimensionamento e pode ser substituída pelo intervalo definido pelo pesquisador.

## 3. O que realmente depende do volume da cisterna

| Relação | Variáveis | Tratamento no modelo |
| --- | --- | --- |
| Dependência direta da capacidade | preço e impacto incorporado do reservatório inferior | interpolação da tabela de preço e massa/fator do material |
| Dependência endógena | água atendida, falhas, extravasamento, volume recalcado, partidas, energia, cloro, receita evitada e O&M variável | cada capacidade é novamente simulada dia a dia |
| Entrada independente, salvo cenário explícito | reservatório superior, comprimentos/diâmetros de tubos, potência/quantidade de bombas e acessórios | permanecem constantes na varredura; o programa não inventa quantitativos geométricos a partir da capacidade |

Assim, não se multiplica indiscriminadamente todo custo ou impacto pelo volume. Se o pesquisador quiser alterar tubulação, bomba ou outro componente entre capacidades, deve cadastrar cenários físicos distintos e registrar a regra de dimensionamento adotada.

## 4. CAPEX e manutenção

O preço automático da cisterna é obtido por interpolação linear por trechos entre os pontos explícitos de `netuno/core/cost_estimates.py`; abaixo do primeiro ponto usa-se proporcionalidade e 0 L representa a alternativa sem sistema. A expressão linear antiga `0,5577 × V + 7,47` não é usada, pois não reproduzia a própria tabela. Os valores são uma base de triagem e devem ser substituídos por cotações locais, datadas e comparáveis.

Cada item de O&M segue a semântica do formato Netuno 4:

```text
n = 12 / periodicidade_em_meses
custo_anual = n × [custo_fixo_por_ocorrência
                   + coeficiente_por_m³ × (consumo_pluvial_anual / 12)]
```

O coeficiente variável, quando informado, remunera o **volume pluvial consumido no mês da ocorrência**, não a capacidade da cisterna. O programa não adota o antigo coeficiente arbitrário de R$ 15 por m³ de capacidade: a manutenção preliminar padrão é fixa. Uma relação com a capacidade só deve ser incluída se houver dados locais — ordens de serviço, contratos ou regressão de custos — com unidade, data-base, amostra e incerteza documentadas.

## 5. Bombeamento e cloração

A energia anual de recalque é calculada com os resultados de cada volume simulado:

```text
E = P × [(Vrecalcado / Q) + (Npartidas × tpartida)] / η
```

`P` está em kW, `Vrecalcado/Q` e `tpartida` em horas e `η` é o rendimento global em fração. Se não houver reservatório superior, a energia de recalque é zero.

A cloração usa uma dose aplicada informada pelo usuário:

```text
mCl2,ativo (kg/ano) = Vtratado (m³/ano) × dose (mg/L) / 1000
mproduto  (kg/ano) = mCl2,ativo / pureza
custoCl2           = mproduto × preço_por_kg_de_produto
CO2Cl2             = mproduto × fator_kgCO2e_por_kg_de_produto
```

A **pureza** está na conta porque a dose é prescrita em cloro ativo e o que se
compra, transporta e fabrica é a pastilha, com 65% de cloro ativo. Somar uma
dose de cloro ativo a um fator por quilo de pastilha subestima em 35%, e foi
metade da divergência que separava o módulo ambiental do de qualidade até a
revisão que precedeu o lançamento. A cadeia está em `netuno/core/chlorination.py`, e os três módulos
— ambiental, econômico e de qualidade — partem dela.

Essa conta estima **massa aplicada em cloro equivalente**, não a demanda de cloro da água. Demanda de cloro é a diferença entre dose aplicada e residual após tempo de contato, e exige ensaio com a água da fonte, definição do residual-alvo, pH, turbidez, matéria orgânica, tempo de contato e protocolo sanitário aplicável. Portanto, a dose padrão serve apenas para cenário econômico/ambiental e não prescreve tratamento.

## 6. Economia

As tarifas efetivas de água e esgoto são diferenças marginais: a conta mensal para a demanda total simulada é comparada à conta após a economia pluvial, preservando blocos, tarifa fixa e modo de cobrança de esgoto. O fluxo nominal de cada ano é:

```text
FCt = economia_água,t + economia_esgoto,t − energia,t − O&Mt − cloro,t
VPL = −CAPEX + Σ FCt / (1 + TMA)^t
```

Tarifas, eletricidade e O&M/cloro recebem os reajustes configurados. A TIR zera o VPL dos fluxos nominais; payback simples e descontado são o primeiro ano em que os acumulados correspondentes se tornam não negativos. Projeções não incluem automaticamente impostos, financiamento, valor residual ou reposições: inclua-os como premissas quando relevantes.

## 7. ACV simplificada

Para cada alternativa, a ACV de triagem soma reservatórios, tubulações e bombas, adiciona operação e subtrai o crédito pela água potável evitada:

```text
CO2líquido,vida = anos × (CO2água_evitado,anual
                         − CO2bomba,anual
                         − CO2tratamento,anual)
                  − CO2incorporado
```

Os fatores têm fonte declarada, e não são mais hipóteses
internas. O detalhe valor a valor está em
[`procedencia_fatores_co2.md`](procedencia_fatores_co2.md):

| Item | Fonte |
| :--- | :--- |
| PEAD | Franklin Associates para o American Chemistry Council (2020) |
| PVC de tubo | EPD Australasia S-P-05503, por kg de tubo instalado |
| PRFV | Composites UK, faixa de 2,5 a 4,0 kg CO₂e/kg |
| Aço inox | worldstainless, por teor de sucata da carga |
| Concreto | Hammond & Jones, corroborado pelo SIDAC |
| Massa linear dos tubos | pesos Amanco Wavin e geometria das NBR 5648 e 5688 |
| Massa do reservatório em PRFV | catálogo Fortlev, por capacidade |
| Rede elétrica | bases de CO₂e nomeadas (SIDAC, CaDI, Vaz et al. 2025) |
| Água substituída | rotas selecionáveis, incluindo a brasileira do SNIS |

Duas ressalvas permanecem. **O fator da rede é CO₂-equivalente, não CO₂**: a
série do MCTI/SIRENE cobre só o dióxido de carbono e só a geração, e usá-la aqui
subestimaria o bombeamento. E as **motobombas** continuam sem fonte, com quatro
dos seis valores extrapolados aritmeticamente — nenhum catálogo consultado
publica massa por potência.

## 8. TOPSIS e novo diagnóstico da concessão

São **sete** os critérios avaliados, quatro de benefício e três de custo:

| Critério | Sentido |
| :--- | :--- |
| Potencial de economia de água potável | benefício |
| Extravasamento | custo |
| Valor presente líquido | benefício |
| Payback descontado | custo |
| Taxa interna de retorno | benefício |
| CO₂ de ciclo de vida | custo |
| Água potável consumida | custo |

> Esta seção já descreveu **três** critérios — água pluvial consumida,
> VPL e CO₂e líquido evitado. O motor (`netuno/core/topsis.py`) já usava sete; a
> documentação é que estava defasada.

Para permitir valores negativos sem uma correção condicional, cada coluna é transladada pelo pior valor observado, `zij = xij − min(xj)`, e normalizada pelo vetor, `rij = zij / √Σzij²`. Após aplicar pesos não negativos normalizados, calculam-se as distâncias euclidianas `D+` e `D−` e o escore `Ci = D−/(D+ + D−)`.

**Esta é uma variante declarada, não o TOPSIS canônico.** Hwang & Yoon (1981) normalizam pela norma euclidiana dos valores originais. Onde todos os valores de um critério são positivos e o mínimo é zero, as duas formas coincidem; onde há VPL negativo — o caso que motivou a mudança — divergem, e os escores não são comparáveis com os de uma implementação canônica sobre a mesma matriz.

O VIKOR implementado em `netuno/core/mcdm_methods.py` calcula `S`, `R` e `Q` conforme Opricovic & Tzeng (2004), mas **não aplica as condições C1 (vantagem aceitável) e C2 (estabilidade aceitável)**. O ranking é, portanto, uma ordenação por `Q`, e não a afirmação de que o primeiro colocado seja um compromisso estável. O SMAA-VIKOR segue Lahdelma & Salminen (2001), amostrando o simplex por Dirichlet simétrica; é implementação independente sobre NumPy, seguindo o desenho da biblioteca `crispyn` (licença MIT), que serve de base de comparação e não de origem do código.

Além do escore agregado, o programa calcula o afastamento independente dos pesos e o apresenta na interface como proximidade:

```text
gapij = [max(xj) − xij] / [max(xj) − min(xj)]
proximidadeij = 1 − gapij
```

No gráfico, 100% significa o melhor resultado observado naquele critério e 0% o pior. Os valores são invertidos, não o sentido do eixo Y: maior proximidade permanece visualmente mais alta. A segunda sub-aba permite distinguir um vencedor próximo dos três ótimos de uma concessão com perdas relevantes em um ou mais eixos. TOPSIS é sensível aos pesos e ao conjunto de alternativas; use a análise de sensibilidade e não interprete o ranking como verdade física.

## 9. Reprodutibilidade e validação

O [DETALHAMENTO_COMPLETO_TRES_MODELOS.md](../examples/DETALHAMENTO_COMPLETO_TRES_MODELOS.md) preserva o diagrama causal, compara todas as entradas dos três modelos e fornece as varreduras técnica, econômica, ambiental e TOPSIS completas, volume a volume. O estudo [ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md](../examples/ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md) apresenta a conta manual e o resíduo item a item. Ambos são gerados diretamente pelo script [generate_reference_case_studies.py](../scripts/generate_reference_case_studies.py), evitando números copiados que possam divergir após uma alteração do motor. A concordância apenas demonstra verificação interna das mesmas equações; validação externa exige dados medidos e comparação independente.

Premissas e critérios de qualidade dos dados estão detalhados em [PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md](../examples/PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md). A base histórica do algoritmo pode ser consultada no [Manual do Netuno 4](../additional_material/documentation/Manual-Netuno-4_Junho2014.pdf), e a validação acadêmica do algoritmo original na [dissertação de Rocha (2009)](../additional_material/documentation/Dissertacao_Vinicius%20Rocha.pdf).

