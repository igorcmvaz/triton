# Triton CLI — guia prático

Use a linha de comando para execuções reproduzíveis, automação e comparação em lote. Ela aceita projetos CSV legados e projetos estruturados `.triton` (JSON).

Execute os exemplos a partir da raiz do repositório, com o mesmo ambiente usado pela aplicação de ambiente de trabalho. Consulte a ajuda efetiva da versão instalada com:

```powershell
python -m triton.cli --help
python -m triton.cli analyze --help
```

## Escolha do formato de projeto

| Formato | Uso recomendado | Rastreabilidade |
| --- | --- | --- |
| `.triton` | novos estudos, intercâmbio e automação | preserva entradas técnicas, económicas, ambientais e TOPSIS; pode incorporar a chuva |
| CSV legado | compatibilidade e casos técnicos existentes | possui estrutura mais limitada; documente externamente as premissas não representadas |

Prefira `.triton` com `--embed-rainfall` quando o estudo precisar ser reproduzido em outro computador. Mesmo autocontido, o ficheiro não substitui o registo da fonte, do período, do tratamento e do controlo de qualidade da série.

## Fluxo recomendado

```powershell
# 1. Crie um projeto portátil, incorporando a chuva diária.
python -m triton.cli init .\projeto.triton --rainfall Funchal.csv --embed-rainfall

# 2. Valide o ficheiro antes de calcular.
python -m triton.cli validate .\projeto.triton

# 3. Execute a análise técnica, a economia, a ACV, o peso do sistema e o TOPSIS, com resultado auditável.
python -m triton.cli analyze .\projeto.triton --analysis all --format json --output .\saida\resultado.json
```

O comando `run` executa o balanço hídrico técnico. `analyze --analysis all` aplica, para cada volume da varredura, o balanço técnico, a análise económica, o balanço ambiental, o peso do sistema e o ranking TOPSIS. Assim, todas as escolhas usam as mesmas alternativas simuladas.

O **peso do sistema** (`--analysis all` ou `--analysis system_weight`) traz a massa a seco, a carga de água e a carga em operação, em kg e kN, no subsolo ou nível inferior, na cobertura ou nível superior e nas prumadas e rede. O HTML, o XLSX (folha `system_weight` com o resumo do volume escolhido; os valores por volume ficam na folha `alternatives`) e o texto do terminal mostram o bloco. Os alertas usam limiares de atenção do **programa**, e não de norma — 500 kg sobre a cobertura com o reservatório cheio, reservatório superior acima de 1 500 L, cisterna acima de 3 000 kg a seco, cisterna de betão — e pedem a confirmação do projeto estrutural ou de fundações.

## Comandos mais usados

| Objetivo | Comando |
| --- | --- |
| Simular um volume específico | `python -m triton.cli run .\projeto.triton --volume 5000 --analysis all` |
| Alterar premissas sem editar o projeto | `python -m triton.cli analyze .\projeto.triton --set area=150 --set rainwater_share=0.5` |
| Ajustar pesos TOPSIS | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weights 0.40,0.30,0.20,0.10` |
| Repartir o peso dentro dos eixos | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weights 0.25,0.25,0.25,0.25 --criterion-shares 1,1,2,1,1,1,1,1` |
| Avaliar robustez dos pesos | `python -m triton.cli analyze .\projeto.triton --analysis topsis --weight-sensitivity 1000 --seed 42 --format json --output .\saida\pesos.json` |
| Propagar incertezas | `python -m triton.cli uncertainty .\projeto.triton --samples 1000 --rainfall-cv 10 --demand-cv 15 --capex-cv 20 --format json --output .\saida\monte-carlo.json` |
| Gerar HTML ou XLSX | Troque `--format json` por `html` ou `xlsx` e informe `--output` |
| Executar folha de cálculo de cenários | `python -m triton.cli batch .\cenarios.xlsx --base .\projeto.triton --analysis all --format xlsx --output .\saida\lote.xlsx` |
| Combinar vários projetos e chuvas | `python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\saida\matriz` |

O multicritério tem oito critérios em quatro eixos: técnico (fiabilidade volumétrica, eficiência de armazenamento), económico (economia financeira líquida, custo nivelado da água, período de recuperação descontado), ambiental (CO₂e de ciclo de vida) e estrutural (massa a seco dos materiais, extravasamento anual). Os valores de `--weights` são, nesta ordem, os pesos dos eixos técnico, económico, ambiental e estrutural (25% cada por omissão), ou oito pesos, um por critério; três valores, de projetos e estudos até à 0.1.0, ainda são aceites, e o eixo estrutural recebe a média dos três. `--criterion-shares` reparte o peso de cada eixo pelos seus critérios, com oito valores pela ordem acima (por omissão, `1,1,1,1,1,1,1,1`, partes iguais). A CLI normaliza a soma automaticamente. Sete valores, do modelo de sete critérios anterior à 0.2.0, são recusados. No ficheiro de projeto, os mesmos dados são `analysis.topsis_weights` (quatro ou oito valores) e `analysis.topsis_criterion_shares` (oito). As saídas gerais aceitam `text`, `json`, `csv`, `html` e `xlsx`; o comando `uncertainty` aceita `text`, `json` e `csv`. Formatos estruturados exigem `--output`. XLSX requer `pandas` e `openpyxl`.

`--set CAMPO=VALOR` pode ser repetido e altera a premissa somente para aquela execução. Registe o comando completo no protocolo do estudo, pois o ficheiro de origem permanece inalterado.

## Matriz edifícios × climas

Mantenha os dois catálogos independentes: um de premissas do edifício e outro de ficheiros climáticos. Isso permite comparar várias cidades para o mesmo edifício, ou vários edifícios para a mesma cidade, sem duplicar dados.

```powershell
python -m triton.cli init-catalog premises .\premissas.json
python -m triton.cli init-catalog climates .\climas.json
python -m triton.cli matrix .\premissas.json .\climas.json --analysis all --output-dir .\resultado-matriz
```

O terminal informa progresso, combinações concluídas, tempo decorrido e ETA. A pasta de saída contém `triton-matriz-resumo.csv` (uma decisão por combinação), `triton-matriz-alternativas.csv` (todos os volumes), `triton-matriz-detalhado.json` (auditoria) e `triton-matriz-painel.html` (leitura consolidada).

### Matriz de projetos

Use `matrix-projects` quando cada configuração já estiver num ou mais ficheiros `.triton`, ou quando o próprio projeto declarar fatores experimentais em `cli_factorial`:

```powershell
python -m triton.cli matrix-projects --projects .\projetos --output-dir .\resultado-projetos
python -m triton.cli matrix-projects --projects .\projetos --rainfall-dir .\chuvas --recursive --output-dir .\resultado-climas
```

Use `--ignore-project-factors` para desconsiderar temporariamente o bloco fatorial gravado nos projetos. Fixe `--seed` quando houver sensibilidade estocástica dos pesos.

## Cenários em folha de cálculo

`batch` lê CSV ou XLSX. Com `--base`, as linhas herdam do projeto-base as premissas económicas e ambientais que a folha de cálculo não substitui:

```powershell
python -m triton.cli batch .\examples\triton-cli-scenarios.csv --base .\projeto.triton --analysis all --format csv --output .\saida\cenarios.csv
```

Valide primeiro o projeto-base e preserve a folha de cálculo de entrada junto do resultado. Um lote compara cenários declarados; ele não cria automaticamente distribuições de incerteza.

## Procurar um município (só nesta edição)

`locais` procura um concelho ou município pelo nome ou pelo código e mostra a fonte da chuva e o nível de qualidade:

```powershell
python -m triton.cli locais Sevilla --pais ES --limite 3
python -m triton.cli locais PT-1106 --format json
```

A primeira linha da saída resume a cobertura da base (locais de Portugal e de Espanha, Iberia01, ERA5 e sem série).

## Estudos em lote por JSON

Para comparar vários edifícios por tipologia (escolas, comerciais, residências, hospitais, aeroportos) e levar os resultados a um artigo, organize o estudo num ficheiro `estudo.json` e execute tudo com `triton estudo`. O ficheiro reúne o projeto base, os casos, o que muda de um caso para o outro, a análise e as saídas; o programa roda os casos numa ordem estável e grava tabelas prontas para o texto (CSV tidy, JSON com proveniência, Markdown, LaTeX, XLSX).

```powershell
# 1. Esqueleto do estudo, com os rótulos da tipologia e nenhum valor preenchido.
python -m triton.cli estudo init .\escolas --tipologia escolar

# 2. Preencha escolas\estudo.json (os «XX» e null) e coloque os .triton e as séries em escolas\casos.
python -m triton.cli estudo validate .\escolas\estudo.json

# 3. Execute todos os casos (em ordem estável); --paralelo N usa N processos e não muda o resultado.
python -m triton.cli estudo run .\escolas\estudo.json --saida .\saida\escolas --paralelo 4

# 4. Refaça as tabelas sem recalcular (por exemplo, depois de mudar métricas ou casas decimais).
python -m triton.cli estudo resumo .\saida\escolas

# 5. Preencha o texto do resumo do congresso com os números reais.
python -m triton.cli estudo texto .\saida\escolas --modelo .\escolas\modelo_texto.md

# 6. Vários estudos (uma pasta com estudo*.json), com o comparativo entre tipologias.
python -m triton.cli estudo lote .\estudos --saida .\saida\comparativo

# 7. Reúne os resultados.csv de várias execuções numa só tabela (tipologia, caso, métrica: mínimo, média, mediana, máximo).
python -m triton.cli estudo consolidar .\saida --saida .\saida\consolidado
```

As tipologias (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario`) são só estrutura e rótulos: `estudo init --tipologia` grava o rótulo, o `grupo` dos casos e, num comentário, o que `usuarios` significa naquela tipologia. Nenhum número vem com a tipologia: área, demanda, utilizadores e fração vêm dos seus casos, com a fonte de cada um.

A ação `consolidar` procura todos os `resultados.csv` sob as pastas indicadas (vários estudos, lotes, execuções repetidas) e grava `consolidado.csv` e `consolidado.md` na pasta de saída: uma linha por tipologia (`grupo`), caso e métrica, com `n`, mínimo, média, mediana e máximo dos valores dos casos concluídos (`status` ok). A unidade faz parte da chave do grupo, pelo que moedas diferentes nunca se misturam. Os números têm o mesmo formato do `resultados.csv` (ponto decimal, dez algarismos significativos); a tabela em Markdown segue `--idioma`. Se o pacote opcional `duckdb` estiver instalado (`pip install "triton-ibe[analise]"`, que não faz parte do instalador), é ele que lê e agrupa os ficheiros; sem ele a biblioteca padrão faz o mesmo, e os dois caminhos dão os mesmos bytes (`--motor csv` força o segundo; `--motor duckdb` exige o pacote).

`estudo run` e `estudo lote` mostram o progresso na saída de erro. `--progresso simples` escreve uma linha por caso (`[i/N] id: ok (t s)`); `--progresso rich` desenha uma barra de progresso e precisa do pacote opcional `rich` (`pip install "triton-ibe[cli]"`; sem ele o programa avisa uma vez e usa `simples`); o padrão `auto` só usa `rich` se este estiver instalado e a saída de erro for um terminal. Os ficheiros de resultado são idênticos em bytes em qualquer modo, e `--quiet` desliga o progresso.

### O ficheiro estudo.json

<!-- tabela: Secções do ficheiro estudo.json (esquema triton-estudo, versão 1) -->
| Secção | Conteúdo |
| :--- | :--- |
| `esquema` | `{"nome": "triton-estudo", "versao": 1}`; outra versão é recusada |
| `estudo` | `id` (letras, números, ponto, hífen e sublinhado), `titulo`, `tipologia` (`escolar`, `comercial`, `residencial-unifamiliar`, `residencial-multifamiliar`, `hospitalar`, `aeroportuario` ou `outra`), `tipologia_rotulo`, `autores`, `nota` |
| `projeto_base` | `arquivo`: um `.triton`, com caminho relativo ao `estudo.json`; ou `modelo`: `"edicao"`, o modelo de projeto da edição (então cada caso informa área, demanda, fração e chuva: nada é presumido) |
| `padroes` | `substituicoes` e `clima` aplicados a todos os casos; o que o caso declara vence o padrão |
| `casos` | lista; cada caso tem `id`, `nome`, `grupo` (por padrão, a tipologia), `projeto` (outro `.triton` para este caso), `clima` e `substituicoes` |
| `clima` | `arquivo` (série diária de chuva, CSV), `data_inicio` (dd/mm/aaaa), `nome` e `fonte` (rótulos que vão para a procedência) |
| `analise` | `tipo` (`technical`, `economic`, `environmental`, `topsis` ou `all`), `volume` (`otimo_tecnico`, `topsis`, `smaa_vikor` ou um volume em litros), `pesos` (quatro de eixo — técnico, económico, ambiental, estrutural — ou oito de critério; três, de estudos anteriores à 0.2.0, ainda aceites), `partes_no_eixo` (oito valores) e `semente` |
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

### Saídas para o artigo

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

As saídas não levam caminho absoluto: os projetos aparecem com caminho relativo ao `estudo.json` (ou só o nome). Duas execuções do mesmo estudo dão ficheiros idênticos; a data de execução é a única diferença, e a variável de ambiente `SOURCE_DATE_EPOCH` a fixa. O `xlsx` guarda a data de criação nas propriedades do ficheiro e não é idêntico byte a byte, só no conteúdo.

**Retomada e códigos de saída.** Numa pasta de saída que já tem resultados, `run` exige `--retomar` (salta os casos prontos e inalterados: a impressão digital do caso inclui o estudo, os ficheiros, a versão e a edição) ou `--sobrescrever` (refaz tudo). O código de saída é 0 se todos os casos foram calculados, 1 se algum caso terminou com erro (as saídas dos demais são gravadas e o caso com erro aparece com `status` `erro`) e 2 se o estudo ou os argumentos são inválidos.

**Métricas.** O volume de cada caso é, por padrão, o ótimo técnico da varredura (`volume: "otimo_tecnico"`); com `"topsis"`, o primeiro do ranking; com um número, o volume fixo. As métricas disponíveis incluem `volume_l`, `economia_agua_potavel_pct`, `agua_pluvial_m3_ano`, `agua_potavel_m3_ano`, `extravasamento_m3_ano`, os dias com atendimento total, parcial e nulo, `capex`, `vpl`, `economia_anual_agua`, `opex_anual`, `tir_anual_pct`, `payback_descontado_meses`, `co2_liquido_vida_kg`, `indice_topsis` e `aceitabilidade_smaa_pct`, além das entradas do caso (`area_captacao_m2`, `usuarios`, `demanda_total_l_dia`, `chuva_media_anual_mm`). As métricas económicas pedem `analise.tipo` `economic` ou `all`; as ambientais, `environmental` ou `all`. Os nomes crus do relatório (`potable_savings_pct`) também valem. Valores monetários saem na moeda de cada projeto; se os casos têm moedas diferentes, o resumo avisa que não são comparáveis e o comparativo não os agrega. Com CAPEX igual a zero (custos não informados), o resumo avisa que VAL, TIR e payback não são resultados.

**Texto com os números.** `triton estudo texto` substitui no seu modelo `.md` os marcadores entre chaves duplas: `{{economia_agua_potavel_pct:caso-01}}` (o valor de um caso), `{{economia_agua_potavel_pct:@min}}`, `@max`, `@media`, `@mediana` (sobre os casos calculados; `@media(escolar)` restringe a um grupo), `{{n_casos}}` e, depois de uma barra vertical, as casas decimais (`{{vpl:caso-01|0}}`). Onde falta resultado o marcador vira «XX» e o comando lista as pendências (com `--estrito`, termina com código 1). Métrica desconhecida é erro.

### Fonte da chuva e licença

Com a chuva do Iberia01 (a fonte principal da edição), o `analyze` regista em `provenance` a fonte, a atribuição ODbL, o nível de qualidade do município e o pacote de dados. Quando a chuva vem da E-OBS (uso restrito a pesquisa e educação não comerciais), as saídas herdam do `analyze` o aviso de licença e a citação que ele regista em `provenance`: o resumo, a `tabela.md`, a `tabela.tex` e o `resultados.json` os repetem, e o aviso sobre o uso não comercial vai primeiro. A chuva ERA5 das ilhas traz o crédito Open-Meteo e Copernicus (CC BY 4.0). Projetos com a chuva de outra origem (série própria) não levam o bloco da E-OBS.

### Exemplo

O exemplo `examples/estudos/residencial-unifamiliar-exemplo/` calcula a moradia do tutorial em Lisboa, no Porto e no Funchal (`portugal/lisboa.triton`, `portugal/porto.triton`, `portugal/funchal.triton`): `python -m triton.cli estudo run examples\estudos\residencial-unifamiliar-exemplo\estudo.json --saida saida\exemplo`.

Os exemplos usam os projetos já distribuídos e não inventam números. Para acrescentar um caso, copie um bloco de `casos` e troque `id`, `nome` e o `projeto` (ou o `clima.arquivo` e as `substituicoes`); registe a fonte de cada valor que preencher.

## Reprodutibilidade e auditoria

Para cada execução usada em relatório ou publicação, preserve:

- ficheiro `.triton`, catálogos ou folha de cálculo de cenários efetivamente usados;
- série de chuva e sua proveniência, salvo quando incorporada ao projeto;
- comando completo, versão do Triton e versão do Python;
- semente de qualquer análise estocástica;
- ficheiros de saída sem edição manual e um registo das interpretações posteriores.

Sensibilidade de pesos e Monte Carlo respondem a perguntas diferentes. A primeira mede estabilidade do ranking diante das preferências; a segunda propaga incerteza das entradas declaradas. Nenhuma delas corrige dados de baixa qualidade ou hipóteses omitidas.

## Boas práticas

- Use `--embed-rainfall` quando o projeto precisar circular entre computadores.
- Execute `validate` antes de processar lotes.
- Use caminhos de saída diferentes para cenários diferentes e não sobrescreva evidências sem revisão.
- Fixe `--seed` em análises de pesos e Monte Carlo para reproduzir exatamente uma execução.
- Comece lotes grandes com uma amostra pequena e confira unidades, colunas e ordem de grandeza.
- Use `python -m triton.cli <comando> --help` quando este guia e a versão instalada divergirem.
