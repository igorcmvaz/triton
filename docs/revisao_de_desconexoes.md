# Revisão de desconexões

Varredura sistemática atrás de uma classe específica de defeito: **valor
calculado corretamente que não chega a quem deveria consumi-lo**. É o defeito do
assistente de motobomba, que computava a altura manométrica e a descartava no
retorno, e não aparece em teste nem em revisão de fórmula, porque cada parte
isolada está certa.

Método: cruzamento entre campos de configuração declarados e lidos, funções do
núcleo e seus chamadores, e variáveis atribuídas e não usadas.

---

## 1. A ETAP é uma ilha

**É a maior desconexão do programa.**

`size_etap` e `calculate_first_flush_washoff` são chamadas **somente** pela aba
de Qualidade da Água. O módulo econômico e o de ACV não as conhecem — a busca
por `size_etap` neles não devolve nada.

A aba dimensiona a linha de tratamento, calcula investimento, custo operacional
e emissão, exibe os três, e nenhum deles atravessa para o resto do programa.

Para uma cisterna de 5.000 L com reservatório superior, aproveitando 120 m³/ano:

| Configuração | CAPEX da ETAP | Fração do sistema | OPEX/ano | CO₂/ano |
| :--- | ---: | ---: | ---: | ---: |
| Cloração | R$ 930 | 14,5% | R$ 10,52 | 0,51 kg |
| Cloração + ultravioleta | R$ 2.130 | 33,2% | R$ 226,15 | 6,70 kg |
| Cloração + ozônio | R$ 4.430 | 69,0% | R$ 210,52 | 15,51 kg |

O sistema que o econômico enxerga custa R$ 6.420,76 e emite 1,63 kg CO₂/ano de
operação. Com ultravioleta, a ETAP sozinha emitiria **quatro vezes** isso, e não
entra em lugar nenhum.

Três campos de configuração existem para isso e **nunca são lidos**:

| Campo | Situação |
| :--- | :--- |
| `water_quality_target_class` | escrito pela interface, lido por ninguém |
| `water_quality_disinfection` | escrito pela interface, lido por ninguém |
| `water_quality_polishing` | nem escrito nem lido |

Ou seja: escolher ultravioleta na interface não altera resultado ambiental nem
econômico nenhum. A escolha fica guardada e é ignorada.

**Não liguei.** Fazê-lo muda o investimento em até 69% e a emissão operacional em
até cinco vezes, e isso inverte conclusões de estudos já feitos. É decisão sua,
como a da rota de água.

---

## 2. O cloro tinha quatro convenções, não três

Já havia corrigido três. A varredura achou a quarta:
`estimate_annual_chlorination_cost`, em `cost_estimates.py`, calculava a massa de
cloro **ativo** e a multiplicava pelo preço do **produto**, subestimando o custo
em cerca de 35%.

Ela alimenta a interface, enquanto o módulo econômico já usava a corrigida. Os
dois exibiam custos diferentes para a mesma cloração, na mesma tela. **Corrigido.**

---

## 3. Justificativas que existem e nunca aparecem

`get_pipe_justification` e `get_pump_justification` estão implementadas e não são
chamadas em lugar nenhum. As equivalentes de materiais e de parâmetros
operacionais são chamadas cinco e duas vezes pela interface.

Consequência: os parâmetros de tubulação e de motobomba são os únicos do módulo
ambiental sem justificativa visível ao usuário — justamente os dois que mais
mudaram nesta versão, e o de motobomba é o que continua sem fonte.

---

## 4. Funções sem nenhum chamador

| Função | Módulo | Observação |
| :--- | :--- | :--- |
| `get_available_climate_cities` | `climate_database.py` | lista cidades da base climática, e nada a chama |
| `search_cities` | `tariffs_database.py` | busca de município implementada e não ligada |
| `save_costs_database` | `cost_estimates.py` | escrita do banco de custos sem caminho de uso |
| `get_tank_linear_regression` | `cost_estimates.py` | regressão de preço por volume, órfã |
| `procedencia_da_base` | `grid_emission_factors.py` | minha, ainda sem consumidor |
| `pump_embodied_co2_is_extrapolated` | `environmental.py` | minha, ainda sem consumidor |

As duas últimas são minhas, e ficam anotadas como pontas soltas: existem para
que a interface possa sinalizar procedência, e a interface ainda não sinaliza.

---

## 5. Campos sem caminho de interface

Estes o núcleo lê e nenhuma tela escreve, de modo que ficam presos no padrão:

| Campo | Efeito de não ter controle |
| :--- | :--- |
| `chlorine_product_purity` | a pureza da pastilha não é editável, embora mude a massa e o custo em 1/pureza |
| `grid_co2_factor_basis` | as bases nomeadas de CO₂e não são selecionáveis; só o número é editável |
| `water_supply_route` | a rota tem seletor, mas só no diálogo de parâmetros da ACV |

---

## 6. Informação preparada e não exibida

No gerador de relatórios, alguns valores são formatados e não inseridos no
documento:

- `sat_null_str`, no relatório executivo — percentual de dias em que a demanda
  pluvial **não** foi atendida. É indicador de confiabilidade, e some.
- `cl2_dose_str`, no relatório ambiental — a dose de cloro adotada.
- `specific_g_l_str`, no mesmo relatório — emissão por litro.

Não são números errados; são números calculados e omitidos.

---

## 7. O que a varredura confirmou estar ligado

Vale registrar o que **não** é desconexão, para não gerar retrabalho:

A maior parte das funções do núcleo chamadas apenas pela interface é assim por
desenho — exportadores, formatadores, geradores de relatório e diálogos. Elas
produzem saída para o usuário, não entrada para outro cálculo.

Os campos de configuração, 99 ao todo, estão quase todos ligados: só os três de
qualidade da água aparecem como escritos e nunca lidos.

E a cadeia hidráulica, depois das correções desta versão, vai de ponta a ponta:
altura geométrica informada no assistente, perda de carga estimada, altura
manométrica, seleção no catálogo comercial, potência, vazão, rendimento, energia
específica, consumo anual, custo e emissão.

---

## Ordem sugerida

1. **Ligar a ETAP** ao econômico e à ACV. É a única desconexão que muda
   resultado de forma material, e depende de decisão sua.
2. **Exibir as justificativas** de tubulação e motobomba, que já existem.
3. **Inserir no relatório** os três valores calculados e omitidos.
4. Decidir o destino das funções órfãs: ligar ou remover.
