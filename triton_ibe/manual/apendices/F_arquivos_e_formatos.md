# Ficheiros, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

## O que o programa lê

<!-- tabela: Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto guardado como tabela por uma versão inicial do programa | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia (a edição traz um exemplo em `data/rainfall`) | etapa 1. Projeto e Chuva |
| procura diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de procura, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um ficheiro desses, o programa avisa e adota os valores
> padrão para o que falta. A secção {{n:21}} mostra o que conferir depois de importar.

---

## O que o programa escreve

<!-- tabela: Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Guardar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| folha de cálculo | `.xlsx` | série diária, varrimento e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV escolhe-se o separador: **ponto e vírgula** para abrir numa folha de cálculo
configurada em português, **vírgula** para o padrão internacional. Escolher mal faz a folha de
cálculo abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um ficheiro JSON com as
propriedades dos componentes, para compatibilização BIM. A secção {{n:22}} trata de todos.

---

## O ficheiro de projeto, por dentro

O `.triton` é um ficheiro de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete secções:

<!-- tabela: As sete secções do ficheiro de projeto e o que cada uma guarda -->
| Secção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a eletrobomba |
| `water_quality_and_etap` | classe-alvo, desinfeção e tratamento |
| `financial_and_economic` | tarifas, impostos, atualizações e prazo |

O apêndice {{n:A}} lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do ficheiro.** É o que torna o projeto reproduzível:
> quem receber o ficheiro obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um ficheiro e muito para um anexo de e-mail com
> vinte deles.

---

## Onde ficam as coisas

<!-- tabela: Localização dos ficheiros do programa e dos ficheiros do utilizador -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| os tarifários transcritos (Lisboa, Porto e Funchal) | dentro do programa, em `triton\data\portugal_tarifarios.json` |
| os casos do manual | na pasta do programa, em `casos` |
| os três projetos de exemplo (Lisboa, Porto e Funchal) | na pasta do programa, em `examples\portugal` |
| a base de precipitação por município (Iberia01) e a E-OBS opcional | na pasta do programa, em `data\chuva_iberia01_p1.db` a `p4.db`, `data\ibe_unidades.db`, `data\chuva_ilhas_era5.db` e `data\portugal_eobs.db` |
| **os seus projetos e relatórios** | **onde escolher ao guardar** |

O programa não cria pasta de trabalho nem guarda ficheiros escondidos. Cada gravação
pergunta o destino, e nada do que se produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada do que é seu.

---

## O ficheiro de estudo em lote (`estudo.json`)

Usado por `triton estudo` (capítulo «Comparar muitos casos de uma vez»). Esquema `triton-estudo`, versão 1.

<!-- tabela: Secções do ficheiro estudo.json (esquema triton-estudo, versão 1) -->
| Secção | Conteúdo |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; outra versão é recusada |
| `estudo` | `id` (letras, números, ponto, hífen e sublinhado), `titulo`, `tipologia` (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario` ou `outra`), `tipologia_rotulo`, `autores`, `nota` |
| `projeto_base` | `arquivo`: um `.triton`, com caminho relativo ao `estudo.json`; ou `modelo`: `"edicao"`, o modelo de projeto da edição (então cada caso informa área, demanda, fração e chuva: nada é presumido) |
| `padroes` | `substituicoes` e `clima` aplicados a todos os casos; o que o caso declara vence o padrão |
| `casos` | lista; cada caso tem `id`, `nome`, `grupo` (por padrão, a tipologia), `projeto` (outro `.triton` para este caso), `clima` e `substituicoes` |
| `clima` | `arquivo` (série diária de chuva, CSV), `data_inicio` (dd/mm/aaaa), `nome` e `fonte` (rótulos que vão para a procedência) |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` ou `all`), `volume` (`otimo_tecnico`, `topsis` ou um volume em litros), `pesos` (TOPSIS) e `semente` |
| `saidas` | `formatos` (`csv`, `json`, `md`, `tex`, `xlsx`), `metricas`, `casas_decimais` (um inteiro ou uma por métrica), `idioma` (`auto`, `pt-BR`, `pt-PT`, `en`, `es`, `zh`), `milhar`, `legenda` e `orientacao` (`casos_nas_linhas` ou `metricas_nas_linhas`) |

Chaves que começam por `_` são comentários e o programa as ignora. Campo vazio, `null` ou «XX» é «a preencher»: a validação o recusa e diz onde está. Uma chave desconhecida é erro, com a sugestão da mais parecida. `triton estudo esquema` imprime o JSON Schema do ficheiro, para completar e conferir no editor.

### Apelidos das substituições

<!-- tabela: Apelidos das substituições e o campo do projeto que cada um altera -->
| Apelido | Campo do projeto | Unidade |
| :--- | :--- | :--- |
| `area_captacao_m2` | `area` | m² |
| `coeficiente_escoamento` | `runoff_coeff` | 0 a 1 |
| `descarte_mm` | `discard` | mm |
| `usuarios` (também `populacao`, `pessoas`, `ocupantes`) | `residents_count` | pessoas |
| `demanda_per_capita_l_dia` | `demand_value` | L/pessoa·dia |
| `demanda_total_l_dia` | `demand_value` (a demanda total dividida pelos utilizadores) | L/dia |
| `fracao_pluvial_pct` ou `fracao_pluvial` | `rainwater_share` | % ou 0 a 1 |
| `volume_reservatorio_l` | `lower_tank_fixed` (e `lower_tank_mode` = volume fixo) | L |
| `volume_maximo_l`, `passo_volume_l` | `lower_tank_max` (varredura), `lower_tank_step` | L |
| `reservatorio_superior_l` | `upper_tank_vol` (e `upper_tank_used`) | L |
| `limiar_bombeamento_l`, `economias`, `irrigacao_l_dia` | `pumping_threshold`, `num_economias`, `irrigation_liters_per_day` | L, unidades, L/dia |
| `data_inicio`, `regra_phi`, `delta_ideal_pct` | `start_date`, `phi_operation_rule`, `delta_ideal` | dd/mm/aaaa, 0 a 1, %/m³ |
| `periodo_analise_anos`, `tma_pct_mes`, `tarifa_energia` | `analysis_period_years`, `tma`, `elec_tariff` | anos, % ao mês, moeda/kWh |

Além dos apelidos, a chave de uma substituição pode ser **qualquer campo que `--set` aceita** (por exemplo `cost_labor`) ou um **caminho pontilhado do próprio `.triton`**, como `inputs.building_and_demand.catchment_area_m2`. O caminho precisa existir no projeto e o valor precisa ter o mesmo tipo do que já está lá; senão o caso termina com erro claro, que lista as chaves disponíveis. Um apelido desconhecido também é recusado, com a sugestão do mais parecido. Dois nomes para o mesmo parâmetro no mesmo caso (`area_captacao_m2` e `area_m2`, ou `fracao_pluvial` e `fracao_pluvial_pct`) são conflito. A fração em 0 a 1 recusa 40 (provável percentual); o percentual recusa fora de 0 a 100.

As substituições passam pela mesma conciliação de frações do `--set`, e o preenchimento preliminar de custos (CAPEX) roda **depois** delas, de modo que o preço da cisterna acompanha o volume do caso. `triton estudo apelidos` lista todos os apelidos e métricas, na língua da edição.

### Saídas do estudo

<!-- tabela: Ficheiros que triton estudo run grava na pasta de saída -->
| Ficheiro | Conteúdo |
| :--- | :--- |
| `resultados.csv` | formato **tidy**: uma linha por caso e métrica (`estudo_id`, `caso_id`, `caso`, `grupo`, `metrica`, `rotulo`, `valor`, `unidade`, `status`); ponto decimal, sem separador de milhar, UTF-8 |
| `resultados.json` | os mesmos valores, mais a **proveniência**: versão do Triton, edição, SHA-256 do `estudo.json` e de cada projeto e série de chuva, fonte, crédito e licença da chuva, avisos e a data de execução |
| `tabela.md` | tabela em Markdown, com os números no formato do idioma (vírgula decimal em português e espanhol, ponto em inglês e chinês) |
| `tabela.tex` | tabela LaTeX com `booktabs` (`\toprule`, `\midrule`, `\bottomrule`), pronta para colar; precisa de `\usepackage{booktabs}` |
| `tabela.xlsx` | opcional (`xlsx` em `formatos`): números de verdade, formatados, mais as abas `tidy` e `proveniencia` |
| `resumo.md` | resumo curto: casos, faixa de cada resultado, avisos, fontes e licenças |
| `casos/<id>/resultado.json` e `analise.json` | todas as métricas do caso e a análise completa do motor (é o que o `resumo` e o `texto` leem) |
| `estudo.json` | cópia do estudo que gerou a pasta |
| `consolidado.csv` e `consolidado.md` | gravados por `triton estudo consolidar` (não pelo `run`): uma linha por tipologia (`grupo`), caso, métrica e unidade, com `n`, mínimo, média, mediana e máximo dos `resultados.csv` encontrados |

As saídas não levam caminho absoluto: os projetos aparecem com caminho relativo ao `estudo.json` (ou só o nome). Duas execuções do mesmo estudo dão ficheiros idênticos; a data de execução é a única diferença, e a variável de ambiente `SOURCE_DATE_EPOCH` a fixa. O `xlsx` guarda a data de criação nas propriedades do ficheiro e não é idêntico byte a byte, só no conteúdo.

**Retomada e códigos de saída.** Numa pasta de saída que já tem resultados, `run` exige `--retomar` (pula os casos prontos e inalterados: a impressão digital do caso inclui o estudo, os ficheiros, a versão e a edição) ou `--sobrescrever` (refaz tudo). O código de saída é 0 se todos os casos foram calculados, 1 se algum caso terminou com erro (as saídas dos demais são gravadas e o caso com erro aparece com `status` `erro`) e 2 se o estudo ou os argumentos são inválidos.

**Métricas.** O volume de cada caso é, por padrão, o ótimo técnico da varredura (`volume: "otimo_tecnico"`); com `"topsis"`, o primeiro do ranking; com um número, o volume fixo. As métricas disponíveis incluem `volume_l`, `economia_agua_potavel_pct`, `agua_pluvial_m3_ano`, `agua_potavel_m3_ano`, `extravasamento_m3_ano`, os dias com atendimento total, parcial e nulo, `capex`, `vpl`, `economia_anual_agua`, `opex_anual`, `tir_anual_pct`, `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` e `aceitabilidade_smaa_pct`, além das entradas do caso (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). As métricas económicas pedem `analise.tipo` `economic` ou `all`; as ambientais, `environmental` ou `all`. Os nomes crus do relatório (`potable_savings_pct`) também valem. Valores monetários saem na moeda de cada projeto; se os casos têm moedas diferentes, o resumo avisa que não são comparáveis e o comparativo não os agrega. Com CAPEX igual a zero (custos não informados), o resumo avisa que VAL, TIR e payback não são resultados.

**Texto com os números.** `triton estudo texto` substitui no seu modelo `.md` os marcadores cercados por chaves duplas (duas de cada lado; os exemplos abaixo vêm sem elas): `economia_agua_potavel_pct:caso-01` (o valor de um caso), `economia_agua_potavel_pct:@min`, `@max`, `@media`, `@mediana` (sobre os casos calculados; `@media(escolar)` restringe a um grupo), `n_casos` e, depois de uma barra vertical, as casas decimais (`vpl:caso-01|0`). Onde falta resultado o marcador vira «XX» e o comando lista as pendências (com `--estrito`, termina com código 1). Métrica desconhecida é erro.

## Compatibilidade entre versões

<!-- tabela: Compatibilidade entre versões do ficheiro de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o valor por defeito |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto legado em CSV | abre com aviso; confira o que a secção {{n:21}} lista |
| ficheiro JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um ficheiro JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores por defeito — e o utilizador
simularia 100 m² acreditando simular os 180 m² que o ficheiro descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.
