# Arquivos, pastas e formatos

Tudo o que o programa lê e escreve, e onde cada coisa fica.

---

## O que o programa lê

<!-- tabela: Formatos que o programa lê e onde cada um é carregado -->
| Formato | Extensão | O que é | Onde se carrega |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | um estudo completo, com a chuva dentro | Abrir projeto |
| projeto antigo | `.json` | projeto de versão anterior, mesmo conteúdo | Abrir projeto |
| projeto legado | `.csv` | projeto do Netuno 4 ou da série 5.0 inicial | Abrir projeto |
| série de chuva | `.csv` | uma coluna de milímetros por dia | etapa 1. Projeto e Chuva |
| demanda diária | `.csv` | consumo medido, dia a dia | etapa 2. Edificação e Consumo |
| cenários | `.xlsx` | uma linha por cenário | menu Cenários & Ferramentas |

**A série de chuva em CSV** é o formato mais simples possível: uma linha por dia, com
a lâmina em milímetros. O programa aceita ponto ou vírgula como separador decimal, e
ignora uma linha de cabeçalho se houver. Ano incompleto é descartado na leitura, para
não enviesar os totais anuais.

> **Projeto legado em CSV.** O formato antigo não guarda tudo o que a versão atual
> usa: modulação de demanda, materiais, pesos do multicritério e a série de chuva
> ficam de fora. Ao abrir um arquivo desses, o programa avisa e adota os valores
> padrão para o que falta. A seção {{n:21}} mostra o que conferir depois de importar.

---

## O que o programa escreve

<!-- tabela: Formatos que o programa escreve e onde cada um é gerado -->
| Formato | Extensão | O que leva | Onde se gera |
| :--- | :--- | :--- | :--- |
| projeto | `.triton` | todos os parâmetros e a série de chuva | Salvar projeto |
| relatório | `.pdf` | o estudo completo, pronto para entregar | etapa 9. Relatórios PDF |
| planilha | `.xlsx` | série diária, varredura e indicadores | etapa 10. Exportação |
| tabela | `.csv` | os mesmos dados, em texto delimitado | etapa 10. Exportação |
| dados | `.json` | os resultados, para reprocessar | etapa 10. Exportação |
| desenho | `.dxf` | o esquema hidráulico, para CAD | etapa 10. Exportação |
| desenho | `.svg` | o mesmo esquema, como imagem vetorial | etapa 10. Exportação |

Na exportação em CSV você escolhe o separador: **ponto e vírgula** para abrir no Excel
em português, **vírgula** para o padrão internacional. Escolher errado faz a planilha
abrir tudo numa coluna só.

O desenho sai em três apresentações: **prancha técnica A3**, **esquemático simples** e
**biblioteca de blocos**, esta última acompanhada de um arquivo JSON com as
propriedades dos componentes, para compatibilização BIM. A seção {{n:22}} trata de todos.

---

## O arquivo de projeto, por dentro

O `.triton` é um arquivo de texto no formato JSON. Pode ser aberto em qualquer editor
de texto, e isso é deliberado: um estudo publicado precisa ser inspecionável sem o
programa.

Ele tem sete seções:

<!-- tabela: As sete seções do arquivo de projeto e o que cada uma guarda -->
| Seção | O que guarda |
| :--- | :--- |
| `metadata` | nome do projeto, identificador e datas |
| `rainfall` | a cidade, o período e a **série diária inteira** |
| `building_and_demand` | área, coeficiente, ocupantes, consumo e fração |
| `demand_modulation` | os perfis semanal, mensal e diário, quando houver |
| `reservoirs_and_pumping` | volumes, limiares e a motobomba |
| `water_quality_and_etap` | classe-alvo, desinfecção e tratamento |
| `financial_and_economic` | tarifas, impostos, reajustes e prazo |

O apêndice {{n:A}} lista todos os parâmetros, com o nome exato de cada campo.

> **A série de chuva vai dentro do arquivo.** É o que torna o projeto reproduzível:
> quem receber o arquivo obtém exatamente os seus números, mesmo sem ter a base
> climática instalada. Em compensação, um projeto com trinta anos de série ocupa
> cerca de 160 kB — o que é pouco para um arquivo e muito para um anexo de e-mail com
> vinte deles.

---

## Onde ficam as coisas

<!-- tabela: Localização dos arquivos do programa e dos arquivos do usuário -->
| O que | Onde |
| :--- | :--- |
| o programa | `C:\Program Files\Triton` |
| as séries de chuva que acompanham | na pasta do programa, em `data\rainfall` |
| a base de tarifas dos 652 municípios | dentro do programa |
| os casos do manual | na pasta do programa, em `casos` |
| os três estudos de referência | na pasta do programa, em `exemplos` |
| a base climática nacional, se instalada | onde o instalador dela indicar |
| **os seus projetos e relatórios** | **onde você escolher ao salvar** |

O programa não cria pasta de trabalho nem guarda arquivos escondidos. Cada gravação
pergunta o destino, e nada do que você produz fica dentro da pasta de instalação — o
que significa que reinstalar ou atualizar o programa não apaga nada seu.

---

## O arquivo de estudo em lote (`estudo.json`)

Usado por `triton estudo` (capítulo «Comparar muitos casos de uma vez»). Esquema `triton-estudo`, versão 1.

<!-- tabela: Seções do arquivo estudo.json (esquema triton-estudo, versão 1) -->
| Seção | Conteúdo |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; outra versão é recusada |
| `estudo` | `id` (letras, números, ponto, hífen e sublinhado), `titulo`, `tipologia` (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario` ou `outra`), `tipologia_rotulo`, `autores`, `nota` |
| `projeto_base` | `arquivo`: um `.triton`, com caminho relativo ao `estudo.json`; ou `modelo`: `"edicao"`, o modelo de projeto da edição (então cada caso informa área, demanda, fração e chuva: nada é presumido) |
| `padroes` | `substituicoes`, `clima` e `tarifa` aplicados a todos os casos; o que o caso declara vence o padrão |
| `casos` | lista; cada caso tem `id`, `nome`, `grupo` (por padrão, a tipologia), `projeto` (outro `.triton` para este caso), `clima`, `tarifa`, `substituicoes` e `dimensoes` (rótulos livres que viram colunas do CSV). Pode faltar se houver `expansao` |
| `expansao` | **só na Edição Brasil.** Gera um caso por município × modelo × recorte da CLIMBra: `municipios` (lista de `municipio`, `uf`, `ibge`), `uf` (padrão dos municípios), `modelos` (`"todos"` ou uma lista dos 19) e `recortes` (lista de `id`, `rotulo`, `cenario` `HIST`, `SSP245` ou `SSP585`, `inicio`, `fim`). Os casos expandidos somam-se aos explícitos |
| `clima` | `arquivo` (série diária de chuva, CSV) **ou** `climbra` (só na Edição Brasil, veja abaixo), `data_inicio` (dd/mm/aaaa), `nome` e `fonte` (rótulos que vão para a procedência) |
| `tarifa` | **só na Edição Brasil.** `municipio`, `uf` (por padrão, os de `clima.climbra`), `categoria` (`residencial`, `comercial`, `publica`, `industrial` ou `social`) e `se_ausente` (`erro`, o padrão, ou `residencial`): aplica as tarifas de água, esgoto e energia do catálogo do programa, como a aba Projeto. Não aceita preços |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` ou `all`), `volume` (`otimo_tecnico`, `topsis` ou um volume em litros), `pesos` (TOPSIS) e `semente` |
| `saidas` | `formatos` (`csv`, `json`, `md`, `tex`, `xlsx`), `metricas`, `casas_decimais` (um inteiro ou uma por métrica), `idioma` (`auto`, `pt-BR`, `pt-PT`, `en`, `es`, `zh`), `milhar`, `legenda` `orientacao` (`casos_nas_linhas` ou `metricas_nas_linhas`) e `gravar_analise` (`true` por padrão; `false` não grava `analise.json` por caso, o que poupa disco em estudos com milhares de casos) |

Chaves que começam por `_` são comentários e o programa as ignora. Campo vazio, `null` ou «XX» é «a preencher»: a validação o recusa e diz onde está. Uma chave desconhecida é erro, com a sugestão da mais parecida. `triton estudo esquema` imprime o JSON Schema do arquivo, para completar e conferir no editor.

### Clima da CLIMBra, tarifa e expansão (só na Edição Brasil)

`clima.climbra` busca a série diária na base CLIMBra do programa: `municipio` (nome como na base; obrigatório), `uf` (confere o município com o catálogo de tarifas e afasta nomes repetidos em outras UFs), `ibge` (código de sete dígitos, só informativo), `modelo` (um dos 19; padrão `INM-CM4`), `cenario` (`HIST`, `SSP245`, `SSP585`; padrão `HIST`) e `inicio`/`fim` (dd/mm/aaaa; padrão, a série inteira do cenário). `arquivo` e `climbra` não convivem no mesmo bloco. Nos `padroes`, `climbra` pode trazer só `modelo` e `cenario`, e o caso completa com o município: os campos se somam. Os modelos de calendário de 360 dias têm um dia a menos no fim do século, e o caso avisa quando a série devolvida é mais curta que o recorte pedido. As saídas registram o SHA-256 do banco `climbra_<modelo>.db` e do catálogo de tarifas usados, além do SHA-256 da série (dias, total e hash).

Na International e na Ibérica, `clima.climbra`, `tarifa` e `expansao` são recusados na validação com a mensagem de que só existem na Edição Brasil; `clima.arquivo` continua valendo.

Com `expansao`, o `resultados.csv` ganha as colunas `municipio`, `ibge`, `modelo`, `recorte`, `cenario`, `inicio` e `fim` entre `grupo` e `metrica`: uma linha por município, modelo, recorte e métrica.

### Apelidos das substituições

<!-- tabela: Apelidos das substituições e o campo do projeto que cada um altera -->
| Apelido | Campo do projeto | Unidade |
| :--- | :--- | :--- |
| `area_captacao_m2` | `area` | m² |
| `coeficiente_escoamento` | `runoff_coeff` | 0 a 1 |
| `descarte_mm` | `discard` | mm |
| `usuarios` (também `populacao`, `pessoas`, `ocupantes`) | `residents_count` | pessoas |
| `demanda_per_capita_l_dia` | `demand_value` | L/pessoa·dia |
| `demanda_total_l_dia` | `demand_value` (a demanda total dividida pelos usuários) | L/dia |
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

<!-- tabela: Arquivos que triton estudo run grava na pasta de saída -->
| Arquivo | Conteúdo |
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

As saídas não levam caminho absoluto: os projetos aparecem com caminho relativo ao `estudo.json` (ou só o nome). Duas execuções do mesmo estudo dão arquivos idênticos; a data de execução é a única diferença, e a variável de ambiente `SOURCE_DATE_EPOCH` a fixa. O `xlsx` guarda a data de criação nas propriedades do arquivo e não é idêntico byte a byte, só no conteúdo.

**Retomada e códigos de saída.** Numa pasta de saída que já tem resultados, `run` exige `--retomar` (pula os casos prontos e inalterados: a impressão digital do caso inclui o estudo, os arquivos, a versão e a edição) ou `--sobrescrever` (refaz tudo). O código de saída é 0 se todos os casos foram calculados, 1 se algum caso terminou com erro (as saídas dos demais são gravadas e o caso com erro aparece com `status` `erro`) e 2 se o estudo ou os argumentos são inválidos.

**Métricas.** O volume de cada caso é, por padrão, o ótimo técnico da varredura (`volume: "otimo_tecnico"`); com `"topsis"`, o primeiro do ranking; com um número, o volume fixo. As métricas disponíveis incluem `volume_l`, `economia_agua_potavel_pct`, `agua_pluvial_m3_ano`, `agua_potavel_m3_ano`, `extravasamento_m3_ano`, os dias com atendimento total, parcial e nulo, `capex`, `vpl`, `economia_anual_agua`, `opex_anual`, `tir_anual_pct`, `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` e `aceitabilidade_smaa_pct`, além das entradas do caso (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). As métricas econômicas pedem `analise.tipo` `economic` ou `all`; as ambientais, `environmental` ou `all`. Os nomes crus do relatório (`potable_savings_pct`) também valem. Valores monetários saem na moeda de cada projeto; se os casos têm moedas diferentes, o resumo avisa que não são comparáveis e o comparativo não os agrega. Com CAPEX igual a zero (custos não informados), o resumo avisa que VPL, TIR e payback não são resultados.

**Texto com os números.** `triton estudo texto` substitui no seu modelo `.md` os marcadores cercados por chaves duplas (duas de cada lado; os exemplos abaixo vêm sem elas): `economia_agua_potavel_pct:caso-01` (o valor de um caso), `economia_agua_potavel_pct:@min`, `@max`, `@media`, `@mediana` (sobre os casos calculados; `@media(escolar)` restringe a um grupo), `n_casos` e, depois de uma barra vertical, as casas decimais (`vpl:caso-01|0`). Onde falta resultado o marcador vira «XX» e o comando lista as pendências (com `--estrito`, termina com código 1). Métrica desconhecida é erro.

## Compatibilidade entre versões

<!-- tabela: Compatibilidade entre versões do arquivo de projeto -->
| Situação | O que acontece |
| :--- | :--- |
| projeto de versão anterior | abre; campos novos assumem o padrão |
| projeto desta versão em versão anterior | pode não abrir, ou perder campos |
| projeto do Netuno 4 em CSV | abre com aviso; confira o que a seção {{n:21}} lista |
| arquivo JSON de outro programa | **recusado**, com mensagem própria |

A última linha merece explicação. Um arquivo JSON que não seja um projeto do Triton
poderia, em princípio, ser aceito e preenchido com valores padrão — e o usuário
simularia 100 m² acreditando simular os 180 m² que o arquivo descreve. O programa
prefere interromper a abertura com mensagem própria, o que é incômodo e é correto: um
projeto aberto errado produz um estudo inteiro errado.
