# Revisão de desconexões

Varredura sistemática atrás de uma classe específica de defeito: **valor
calculado corretamente que não chega a quem deveria consumi-lo**. É o defeito do
assistente de motobomba, que computava a altura manométrica e a descartava no
retorno, e não aparece em teste nem em revisão de fórmula, porque cada parte
isolada está certa.

Método: cruzamento entre campos de configuração declarados e lidos, funções do
núcleo e seus chamadores, e variáveis atribuídas e não usadas.

**Situação: todos os pontos resolvidos.** O que segue registra o que se achou, o
que se fez e por que, e o que ficou para decisão. 602 testes verdes, 57 deles
escritos para esta revisão.

---

## 1. A ETAP era uma ilha

Era a maior desconexão do programa.

`size_etap` e `calculate_first_flush_washoff` eram chamadas **somente** pela aba
de Qualidade da Água. O módulo econômico e o de ACV não as conheciam. A aba
dimensionava a linha de tratamento, calculava investimento, custo operacional e
emissão, exibia os três, e nenhum deles atravessava para o resto do programa.

Para uma cisterna de 5.000 L com reservatório superior, aproveitando 120 m³/ano:

| Configuração | CAPEX da ETAP | Fração do sistema | OPEX/ano | CO₂/ano |
| :--- | ---: | ---: | ---: | ---: |
| Cloração | R$ 930 | 14,5% | R$ 10,52 | 0,51 kg |
| Cloração + ultravioleta | R$ 2.130 | 33,2% | R$ 226,15 | 6,70 kg |
| Cloração + ozônio | R$ 4.430 | 69,0% | R$ 210,52 | 15,51 kg |

Três campos existiam para isso, eram escritos pela interface e não eram lidos
por ninguém: `water_quality_target_class`, `water_quality_disinfection` e
`water_quality_polishing` — este último nem escrito era.

### O que se fez

`netuno/core/etap_integration.py` é o ponto único onde a ETAP é dimensionada a
partir da configuração do projeto. O econômico e a ACV o chamam.

O acoplamento **não é uma soma simples**, e é aí que estava o risco:

| Regra | Motivo |
| :--- | :--- |
| A ETAP **substitui** o termo de cloração da ACV | O total da ETAP já contém o hipoclorito. Somar contaria o cloro duas vezes. |
| Só a parcela **sem cloro** entra no custeio | O econômico já custeava o hipoclorito pela linha de cloração. |
| O CAPEX da ETAP é **incremental** sobre «Acessórios» | O estimador já embute uma verba de filtração e tratamento — R$ 350 na casa unifamiliar térrea, R$ 2.100 na tipologia industrial. |
| `etap_enabled=False` devolve o resultado anterior | Estudos já rodados usaram só a cloração, e têm de continuar reproduzíveis. |

Efeito medido, para o mesmo sistema: escolher ultravioleta multiplica por treze a
emissão anual de tratamento, aumenta o investimento e reduz o valor presente
líquido. Antes, não mudava nada.

### Quatro defeitos encontrados de passagem na mesma aba

- A **dose de cloro** digitada não chegava à configuração: o econômico e a ACV
  seguiam com a dose padrão enquanto a tela mostrava outra.
- O **filtro de polimento** não chegava à configuração.
- O **volume pluvial anual** era pedido a `annual_pluvial_consumed_m3` na
  configuração, e esse atributo não existe em `NetunoConfig` — é propriedade do
  *resultado* da simulação. O `getattr` devolvia sempre 120 m³/ano, e a ETAP era
  dimensionada para esse número qualquer que fosse o projeto.
- A **precipitação anual** estava fixa em 1.500 mm no cálculo de wash-off, de
  modo que o volume anual de descarte era o mesmo em Manaus e em Caxias do Sul.

---

## 2. O cloro tinha cinco convenções, não três

Já havia corrigido três. Esta revisão achou a quarta e a quinta:

- `estimate_annual_chlorination_cost`, em `cost_estimates.py`, calculava a massa
  de cloro **ativo** e a multiplicava pelo preço do **produto**, subestimando o
  custo em cerca de 35%.
- A aba de Qualidade da Água usava **R$ 38,00/kg**, fixo no código, enquanto o
  econômico usava `chlorine_cost_per_kg`, de **R$ 25,00**. A mesma cloração
  custava dois valores diferentes no mesmo projeto.

Ambas corrigidas. `size_etap` passou a receber pureza e fator de emissão do
projeto, em vez de assumi-los, e é essa identidade que permite descontar a
parcela do cloro sem contar duas vezes.

---

## 3. Justificativas que existiam e nunca apareciam

`get_pipe_justification` e `get_pump_justification` estavam implementadas e não
eram chamadas em lugar nenhum. Tubulação e motobomba eram os únicos parâmetros
do módulo ambiental sem procedência visível — justamente os dois que mais
mudaram nesta versão.

Pior: `_update_pump_co2_justification` era um `pass`, um método que existia só
para não quebrar os signals.

**Feito.** As duas aparecem no diálogo de parâmetros. A da motobomba marca como
**VALOR EXTRAPOLADO** os quatro valores que são escalonamento aritmético do de
0,5 CV, o que dá consumidor a `pump_embodied_co2_is_extrapolated`.

---

## 4. Funções sem nenhum chamador

| Função | Destino |
| :--- | :--- |
| `procedencia_da_base` | **ligada** ao seletor de base do fator da rede |
| `pump_embodied_co2_is_extrapolated` | **ligada** ao aviso de extrapolação da motobomba |
| `get_available_climate_cities` | **ligada** ao combo de cidade da Etapa 1 |
| `search_cities` | **ligada** à busca de município do diálogo de tarifas |
| `save_costs_database` | sem editor de custos na interface — **verificada por teste** |
| `get_tank_linear_regression` | diagnóstico sem superfície de exibição — **verificada por teste** |

Sobre as duas ligadas na Etapa 1 e nas tarifas:

- O combo de cidade escolhe ao mesmo tempo a série de precipitação e a tarifa, e
  era povoado apenas pela base de **tarifas**. As duas bases coincidem hoje — 652
  municípios de cada lado, sem diferença — mas nada garantia isso: acrescentar um
  município à base tarifária o faria aparecer na lista climática sem série para
  carregar, e o usuário só descobriria ao tentar simular. Agora a coincidência é
  verificada, e há teste que falha se as bases divergirem.
- A seleção de tarifa exigia saber a UF de antemão, entre 652 municípios de 27
  estados, e quem procurava pela prestadora — CASAN, SABESP — não tinha caminho
  nenhum. A busca varre nome, estado e prestadora, e posiciona os dois combos.

As duas últimas ficam **verificadas, não ligadas**: não têm consumidor plausível
sem construir uma tela que ninguém pediu. Uma função órfã que ninguém testa é a
que quebra em silêncio quando alguém finalmente a chama, e é por isso que têm
teste. Removê-las é decisão sua.

---

## 5. Campos sem caminho de interface

| Campo | Situação |
| :--- | :--- |
| `chlorine_product_purity` | **campo próprio**, com justificativa. O efeito é de 1/pureza: à mesma dose, água sanitária exige seis vezes mais produto que a pastilha. |
| `grid_co2_factor_basis` | **seletor de base**, com fonte, gás e fronteira à vista. |
| `water_supply_route` | já tinha seletor no diálogo de parâmetros da ACV. |

Sobre a base do fator da rede: as bases **não são intercambiáveis**. A série do
MCTI contabiliza CO₂ apenas, e apenas da geração; as demais são CO₂-equivalente
com fronteira mais larga. Trocar uma pela outra sem dizer qual é qual foi o que
produziu a divergência entre módulos na versão anterior. A procedência aparece
desde a abertura do diálogo, e não só depois de mexer no seletor.

---

## 6. Informação preparada e não exibida

Eram **dois**, não três. A varredura anterior listou `specific_g_l_str` por
engano: ele está no cartão de payback ambiental do laudo.

- `sat_null_str`, no laudo executivo — percentual de dias em que a demanda
  pluvial **não** foi atendida. Dizer que 62% dos dias tiveram atendimento
  integral não diz se os outros 38% foram parciais ou nulos. **Inserido.**
- `cl2_dose_str`, no laudo ambiental — a tabela mostrava a massa anual de produto
  sem a dose que a origina, de modo que não havia como conferir a conta.
  **Inserido.**

Acrescentado também: o laudo ambiental **nomeia os estágios de desinfecção**.
Sem isso, dois laudos com valores de tratamento muito diferentes ficariam
indistinguíveis, e o leitor não saberia que a diferença está na escolha, e não em
erro de cálculo.

---

## 7. O que a varredura confirmou estar ligado

Vale registrar o que **não** é desconexão, para não gerar retrabalho.

A maior parte das funções do núcleo chamadas apenas pela interface é assim por
desenho — exportadores, formatadores, geradores de relatório e diálogos. Elas
produzem saída para o usuário, não entrada para outro cálculo.

Dos 99 campos de configuração, os únicos escritos e nunca lidos eram os três de
qualidade da água, agora ligados.

E a cadeia hidráulica vai de ponta a ponta: altura geométrica informada no
assistente, perda de carga estimada, altura manométrica, seleção no catálogo
comercial, potência, vazão, rendimento, energia específica, consumo anual, custo
e emissão.

---

## 8. Como isso fica guardado

O risco desta classe de defeito é voltar sem que ninguém note, porque cada parte
isolada continua certa. `tests/integration/test_fluidez_de_informacoes.py`
verifica o **percurso**, não a fórmula: uma escolha feita numa etapa tem de mover
um resultado nas seguintes, e se deixar de mover, alguma ponte se rompeu.

| Arquivo de teste | O que guarda |
| :--- | :--- |
| `test_etap_integration.py` | a ETAP move os dois módulos, e o cloro é contado uma vez |
| `test_environmental_params_ui.py` | os controles novos chegam ao cálculo |
| `test_funcoes_orfas.py` | as quatro órfãs, ligadas ou verificadas |
| `test_report_omitted_values.py` | os valores omitidos estão no documento |
| `test_fluidez_de_informacoes.py` | os três percursos, de ponta a ponta |

---

## As duas decisões, respondidas e implementadas

### Decisão 1 — a rota de água

**Resposta:** o valor passa a ser escolhido pelo usuário conforme a **tecnologia
de tratamento** do local, com **0,35 kg CO₂e/m³ como base do programa**. A rota
do SNIS não é adotada, porque parte de um indicador de energia e uma avaliação de
ciclo de vida é mais do que energia.

**Feito.** O catálogo foi de 8 para 19 rotas, cada uma declarando fonte, DOI,
tecnologia, matriz elétrica assumida e fronteira do sistema. Entraram as cinco
macrorregiões brasileiras de Vaz, Ghisi, Scolaro & Schaefer (2025), estações
urbanas do Paquistão, matriz limpa escocesa, matriz carvoeira chinesa e a
dessalinização térmica. O seletor passou a explicar a escolha, e não só a
fazê-la. Ver [rotas_de_producao_de_agua.md](rotas_de_producao_de_agua.md).

Duas correções de fundo vieram junto.

**A fronteira.** O sistema pluvial substitui água entregue na edificação, não
água produzida na estação, e entre uma e outra estão as perdas de distribuição:
de 33,9% no sudeste a 46,9% no norte. Os 0,236 kg CO₂e/m³ que o artigo publica
são de porta de estação; por m³ entregue, as macrorregiões vão de 0,336 a 0,461.
Não são valores discordantes, são a mesma água medida em dois pontos. A base de
0,35 fica logo abaixo dessa faixa e da europeia, o que a torna conservadora.

**A rota do SNIS** ganhou `fronteira_incompleta` no registro e aviso visível na
interface, ao lado das outras duas de fronteira parcial. Continua no catálogo
porque o limite inferior é informação; sinalizada porque um limite inferior
apresentado como estimativa central é desinformação.

### Decisão 2 — as duas funções verificadas

**Resposta:** manter as duas, e fazer a interpolação usar o banco de dados como
referência.

**Feito.** A extrapolação acima do maior volume tabelado passa a usar a regressão
ajustada sobre o banco inteiro, o que dá consumidor a
`get_tank_linear_regression`. O critério anterior era a inclinação dos dois
últimos pontos, o par mais sensível a ruído de varejo de toda a série: uma
promoção no maior volume girava a reta inteira. Com R² abaixo de 0,90 cai-se no
método local, e o preço extrapolado nunca fica abaixo do último tabelado.

A pesquisa de preços encontrou um defeito na tabela: ela misturava fabricantes, e
o resultado era 1.750 L a R$ 1.399 contra 2.000 L a R$ 1.299. **Um reservatório
maior custava menos**, na faixa que é justamente a residencial. A tabela nova é
de uma marca num único varejista, coletada no mesmo dia, com máximo corrente para
garantir monotonicidade, e o banco declara de onde veio.

Corrigir o arquivo não bastava: a tabela de recurso embutida no código guardava a
versão defeituosa, de modo que bastava o arquivo faltar — instalação nova,
permissão negada, arquivo corrompido — para o defeito voltar sem aviso. Só
apareceu porque um teste exercitou o caminho de recurso.

`save_costs_database` fica como está, verificada por teste. Sem editor de custos
na interface, construir a tela seria escopo que ninguém pediu.
