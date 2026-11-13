# Histórico de versões e o que mudou

Esta secção regista o que mudou entre as versões do programa e, sobretudo, **que mudanças alteram
resultados já publicados**. A distinção importa mais do que parece: uma correção de interface não
afeta nenhum estudo anterior, ao passo que uma correção de cálculo pode deslocar cada número de um
trabalho já submetido. Quem publicou com o Triton precisa de saber em que categoria cai cada
alteração, e é por isso que o histórico abaixo separa as duas coisas de forma explícita.

==A regra que orienta toda esta secção é simples: uma correção de cálculo obriga a declarar a
versão usada; uma correção de interface, não.==

---

## A versão que está a usar

O número da versão aparece na barra lateral, no rodapé e no menu **Sobre o Triton**. É também
gravado dentro de cada ficheiro de projeto e impresso em cada relatório, de modo que um estudo
antigo leva sempre consigo a identificação do programa que o produziu. Esta redundância é
deliberada: os relatórios circulam separados dos ficheiros, e a pergunta «com que versão foi isto
feito?» costuma surgir meses depois, quando já ninguém se lembra.

O esquema de numeração segue a convenção corrente em engenharia de software. O primeiro número
indica a geração do programa, e a sua mudança significa uma reformulação do modelo conceptual; o
segundo indica um conjunto de funcionalidades novas; e o terceiro indica correções e ajustes que
não alteram a arquitetura. Um primeiro número igual a zero marca uma versão beta: o programa é
utilizável e está verificado como a secção {{n:34}} descreve, mas a interface, o formato de
ficheiro e os valores por omissão ainda podem mudar, e uma mudança pode alterar resultados.

A versão atual é a beta **0.2.0**. A anterior, a 0.1.0, saiu a 5 de novembro de 2026; um estudo
feito com ela declara-a e reproduz-se com ela.

---

## Como este histórico é mantido

A partir daqui, cada versão publicada ganha uma entrada própria nesta secção, com a data de
lançamento e o que mudou, sempre separado em duas listas: ==o que altera os resultados de estudos
já feitos e o que não altera.== A entrada mais recente vem primeiro.

Cada entrada segue o mesmo modelo, para que duas versões se possam comparar sem reler: uma frase
de resumo, as novidades, as correções que alteram resultados, as que não alteram, e o que mudou na
documentação. As secções sem conteúdo nessa versão simplesmente não aparecem.

A mesma lista é distribuída com o código, no ficheiro `CHANGELOG.md` da raiz do repositório, e
alimenta a página de versões do sítio de documentação. Não é escrita três vezes: as três saem
desta secção, e uma verificação automática recusa a montagem se divergirem. Quem acompanha o
programa pelo repositório, pelo sítio ou pelo manual lê o mesmo registo.

<!-- inclui: _tabelas/cap38_versoes.md -->

---

## Versão 0.2.0 (beta) — 11 de novembro de 2026

> **Numa frase.** O multicritério passa de sete critérios em três eixos a oito critérios em quatro eixos — técnico, económico, ambiental e estrutural —, relata uma faixa de volumes semelhantes em vez de um volume só e aceita pesos objetivos pelo CRITIC, e o programa ganha a calculadora do peso do sistema.

### Novidades

- **Oito critérios em quatro eixos.** Técnico: fiabilidade volumétrica (água de chuva consumida ÷ procura de água de chuva, em %) e eficiência de armazenamento (água de chuva entregue por dia ÷ volume da cisterna inferior, em %). Económico: economia financeira líquida (o VAL contra a linha de base sem cisterna), custo nivelado da água (LCOW, em €/m³) e período de recuperação descontado. Ambiental: CO₂e de ciclo de vida. Estrutural: massa a seco dos materiais e extravasamento anual. A secção {{n:32}} dá as definições e a fórmula do LCOW.
- **Pesos em dois níveis.** Quatro pesos de eixo, 25% cada por omissão, repartidos pelos critérios de cada eixo segundo as partes no eixo, iguais por omissão; ou oito pesos diretos, um por critério. O separador de decisão tem um cartão por eixo, com o peso do eixo em cima e as partes dos seus critérios por baixo, os perfis «Equilibrado: 25% em cada eixo» e «Priorizar …» (70% num eixo e 10% em cada um dos outros, incluindo «Priorizar Leveza e Drenagem») e os botões «Partes iguais» e «Recalcular». Na linha de comandos, `--weights` (quatro ou oito valores) e `--criterion-shares` (oito); no ficheiro de projeto, `analysis.topsis_weights` e `analysis.topsis_criterion_shares`; no estudo declarativo, `analise.pesos` e `analise.partes_no_eixo`. O TOPSIS, o VIKOR, o PROMETHEE II e o SMAA-VIKOR usam a mesma regra; o SMAA-VIKOR sorteia oito pesos, com 25% esperado em cada eixo, e informa o peso central agregado nos quatro eixos.
- **Pesos objetivos pelo CRITIC.** Em vez de declarar os pesos, pode pedi-los aos resultados: o CRITIC (Diakoulaki, D.; Mavrotas, G.; Papayannakis, L., 1995. Determining objective weights in multiple criteria problems: The CRITIC method. *Computers & Operations Research*, 22(7), 763–770. doi:10.1016/0305-0548(94)00059-H) pesa cada critério pelo contraste entre os volumes e pela independência em relação aos outros critérios, calculados dos volumes maiores que zero a cada análise. Vale para o TOPSIS, o VIKOR e o PROMETHEE II; o SMAA continua a sortear os pesos. No separador de decisão, o perfil «Pesos objetivos (CRITIC), calculados dos resultados»; na linha de comandos, `--weights critic`; no ficheiro de projeto, `analysis.topsis_weights: "critic"`; no estudo declarativo, `analise.pesos: "critic"`. É uma escolha de método, e não o padrão.
- **Faixa de escolha.** O multicritério deixa de apontar um volume como «o melhor» quando vários pontuam quase igual: relata os volumes cuja pontuação fica a até 5% da amplitude das pontuações, contados a partir da maior, e o volume de maior pontuação como informação. A regra vale para o TOPSIS, o VIKOR, o PROMETHEE II e o SMAA. A tolerância declara-se com `--score-band`, `analysis.topsis_score_band` ou `analise.tolerancia_faixa`; a faixa sai na conclusão do separador de decisão, no texto do terminal, no HTML, no JSON (`topsis.choice_band`) e, nos estudos, nas métricas `faixa_topsis_min_l` e `faixa_topsis_max_l`.
- **Peso do sistema.** Massa a seco, carga de água e carga em operação, em quilogramas e quilonewtons, no subsolo, na cobertura e nas prumadas e rede: em `triton analyze --analysis all` (ou `--analysis system_weight`), no HTML, no XLSX e no texto do terminal. Um alerta pede confirmação com o projeto estrutural ou de fundações quando a carga passa um limiar de atenção do programa, que não vem de nenhuma norma.

### Correções que alteram resultados

<!-- tabela: Correções que alteram resultados na versão 0.2.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |
| O multicritério tinha sete critérios em três eixos, e três deles — potencial de poupança, extravasamento e consumo de água potável — mediam a mesma água economizada. Passa a ter oito critérios em quatro eixos, e o SMAA-VIKOR passa a sortear os oito pesos com 25% esperado em cada eixo, como o padrão do TOPSIS. | A ordenação do TOPSIS, do VIKOR, do PROMETHEE II e do SMAA-VIKOR muda, e com ela pode mudar o volume escolhido: no tutorial de Lisboa, com pesos iguais, a maior pontuação do TOPSIS passa de 5 000 L para 3 000 L, numa faixa de escolha de 2 000 a 3 000 L. As aceitabilidades do SMAA-VIKOR também mudam: no tutorial, o volume mais aceite é 3 000 L, em 24,1% dos sorteios. Três pesos de eixo, de projetos e estudos até à 0.1.0, continuam aceites, e o eixo estrutural recebe a média dos três; sete pesos ou sete partes são recusados. Para reproduzir um estudo feito com a 0.1.0, use a 0.1.0 (DOI 10.5281/zenodo.23402916). |

### Correções que não alteram resultados

- A faixa de escolha com um volume só não sai mais como «volumes de 1000 a 1000 L»: a linha de comando, o HTML e a interface dizem que só aquele volume fica a até 5% da amplitude; faixa com lacunas lista os volumes, em vez de sugerir que os do meio também estão nela.
- A linha do SMAA-VIKOR na linha de comando traz a faixa quando ela tem mais de um volume.
- Com `--weights critic`, o JSON traz em `topsis.weights` os pesos calculados, somados por eixo.
- A frase de decisão da interface compara com a menor cisterna a diferença de CO2e evitado (antes, o valor absoluto da alternativa), com sinal, e mantém a vírgula decimal no escore e na aceitabilidade.
- O separador Documentação descreve os quatro eixos, os perfis 70/10, o CRITIC, a faixa de escolha e a Dirichlet por eixo do SMAA.
- O relatório de texto da linha de comando diz o critério da melhor alternativa econômica (menor payback ou, sem nenhuma que se pague, maior VPL), escreve o payback em anos na língua da edição, avisa quando os custos de obra não foram informados (CAPEX zero) e diz o que é o número da melhor alternativa ambiental: CO2e líquido evitado na vida útil, negativo quando o sistema emite mais do que evita.

### Documentação

A secção {{n:32}} descreve os oito critérios, a fórmula do LCOW, a regra dos pesos, os pesos objetivos do CRITIC, a faixa de escolha e o peso do sistema; a secção {{n:12}} refaz a decisão do tutorial com o modelo novo, em faixas de volumes, e diz o que a escolha dos 5 000 L cede; a secção {{n:13}} pede a faixa e a tolerância no estudo publicado; as secções {{n:19}} e {{n:37}} trazem as opções e as mensagens novas. Para citar, use o DOI de todas as versões, 10.5281/zenodo.23402915, que aponta sempre para a mais recente: a 0.2.0 ainda não tem DOI próprio.

---

## Versão 0.1.0 (beta) — 5 de novembro de 2026

> **Numa frase.** Primeira versão beta do Triton, com nome próprio para cada edição, no mesmo repositório e com a mesma numeração.

### Novidades

O Triton simula o aproveitamento de águas pluviais dia a dia e inclui o motor de simulação, a
avaliação de ciclo de vida, a linha de tratamento, a decisão multicritério e a modulação
probabilística. Esta é a primeira versão da Edição Ibérica (IBE, antes Edição Portugal), que tem nome e logótipo próprios e partilha o repositório e a numeração das outras edições, com a chuva do Iberia01 por município (e a E-OBS por concelho como opção), os tarifários de Lisboa, do Porto e do Funchal
e os valores em euros. A regra de operação de Fewkes (φ) está disponível como opção em todos os
módulos.

**O que a Edição Ibérica traz nesta versão.**

- **Chuva.** A precipitação diária de 278 concelhos de Portugal continental, de 1950 a 2025, calculada a partir da grelha E-OBS v33.0e, numa base de 5,74 MiB identificada por `PT-EOBS-v33.0e-37fcba20` e por SHA-256. Cada concelho tem um nível de qualidade, A, B ou C: 45 de nível A, 159 de B e 74 de C.
- **Licença da chuva (E-OBS, opcional).** No primeiro arranque, o aviso da licença da E-OBS (só uso não comercial, em investigação e educação) e a declaração do uso pretendido, que fica registada nos laudos. Por decisão do titular (25/10/2026), o uso comercial da chuva E-OBS é bloqueado e os relatórios avisam, em vermelho e em tamanho grande, que não pode ser usada comercialmente.
- **Tarifários.** Água, saneamento e resíduos de Lisboa, do Porto e do Funchal, transcritos de documentos oficiais com endereço e SHA-256 registados; a entidade gestora de cada serviço em 280 concelhos, a partir da ERSAR; e um estado de confiança por concelho e por serviço.
- **Valores e língua.** Euros, IVA tratado em cada tarifário, português europeu na interface, nos laudos e no manual.
- **Chuva de toda a Península (30/10/2026).** O Iberia01 passa a ser a fonte por defeito da Edição Ibérica: Portugal (308 locais), Espanha (8 131 municípios, incluindo as Baleares) e, com a ERA5 em nível C, Canárias, Madeira e Açores; chave por código INE/DTMN, busca por nome e código na Etapa 1, `--local` na linha de comandos e `clima.iberia` nos estudos em lote. A E-OBS fica opcional. Os exemplos (Lisboa, Porto e Funchal; novos Madrid e Palma), os relatórios de exemplo e o tutorial deste manual foram regerados com o Iberia01 (normal 1986–2015) em 31/10/2026, e já não levam o aviso vermelho da E-OBS; o Funchal usa a ERA5 de ilha (nível C). A tabela de qualidade passa para um ficheiro separado sob ODbL. Tarifas de Espanha: média regional do INE (indicativa).
- **Estudos em lote por JSON.** O subcomando `triton estudo` organiza um estudo num `estudo.json` (projeto base, casos por tipologia, substituições de parâmetros por apelidos, análise e saídas), roda todos os casos em ordem estável, com retomada e execução paralela, e grava tabelas para artigos: CSV tidy, JSON com proveniência (versão, edição, SHA-256, fonte e licença da chuva), Markdown, LaTeX (booktabs) e XLSX. Um modelo de texto com marcadores recebe os números reais e deixa «XX» onde faltar resultado. Há um estudo de exemplo em `examples/estudos/`.
- **Documentação.** O manual completo, o sítio de documentação, volumes curtos e `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e qualidade.

**O que a versão ainda não tem.**

- **Espanha.** As tarifas são a média regional do INE (indicativa) e, em sete municípios, uma tarifa transcrita ainda não conferida (segunda leitura pendente); o exemplo de Madrid mostra a tarifa do Canal de Isabel II com esse aviso.
- **Ilhas.** Canárias, Madeira e Açores usam a reanálise ERA5 de 0,25°, sempre em nível C e com aviso; Ceuta e Melilla não têm série.
- **Tarifários nos restantes concelhos.** Só três estão transcritos; nenhum concelho está em verde, porque falta a verificação independente (42 amarelos e 238 cinzentos na água e no saneamento).
- **Preços e CAPEX.** O programa não calcula preços de Portugal: reservatórios, tubagem, eletrobombas, mão de obra e manutenção partem de zero, e a tarifa de eletricidade e o preço do cloro também. Os resultados económicos dos exemplos não são resultados.
- **Fator de emissão da rede.** Sem valor: é zero até o utilizador indicar o da rede do projeto.
- **Correção de escala da chuva.** A correção calibrada com o Iberia01 não faz parte desta versão.

**Limitações conhecidas.**

- A licença da E-OBS é omissa quanto à redistribuição da base derivada; por decisão do titular (25/10/2026) o uso comercial é bloqueado e avisado, e quem usa a chuva E-OBS assume o uso não comercial. A tabela de qualidade, derivada do Iberia01 (ODbL), vai para um ficheiro separado sob a ODbL, com atribuição. O aviso da licença só existe em português europeu, e o texto ainda precisa de revisão.
- O diálogo do CAPEX não tem campo para o preço da cisterna e repõe-no a zero ao confirmar; a secção {{n:10}} dá o contorno.
- Em espanhol e em chinês, a interface está traduzida em parte (as traduções do nível de qualidade da chuva não foram revistas por um falante nativo) e os laudos saem com trechos em português; o português e o inglês estão completos.
- Em inglês, alguns textos do catálogo da linha de tratamento e a proveniência do tarifário aparecem em português.
- Os termos de reutilização dos sítios das entidades gestoras não foram verificados (no do Porto não se encontrou nenhum).
- Referências a rever antes de citar: a edição da EN 16941-1 em vigor e a sua transposição, a revisão da ETA 0701 da ANQIP (as secções {{n:1}} e {{n:9}} marcam o que falta).

### Correções que alteram resultados

Nenhuma: esta é a primeira versão beta, e não há versão anterior a corrigir.

<!-- tabela: Correções que alteram resultados na versão 0.1.0 -->
| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

Nenhuma.

### Documentação

O manual ganhou as secções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice {{n:E}}.

---

## Como saber se a sua versão tem uma correção

O procedimento é direto e não depende de consultar ninguém: abra um dos ficheiros de exemplo que
acompanham o programa, descritos no apêndice {{n:J}}, execute-o e compare o resultado obtido com o
valor impresso neste manual. Cada caso de exemplo foi gerado pela mesma versão do programa que
gerou este manual, e cada número publicado tem a verificação automática correspondente, como a
secção {{n:34}} descreve. Uma divergência, portanto, indica que o programa instalado não é o da
versão deste manual.

==Se os números coincidirem, a sua instalação corresponde exatamente ao manual que tem em mãos.==
Se não coincidirem, a diferença não é um defeito da sua instalação, mas uma diferença de versão que
é preciso identificar antes de qualquer estudo.

---

## O que declarar num trabalho publicado

A boa prática de reprodutibilidade computacional exige que um trabalho identifique de forma
inequívoca o programa que produziu os resultados. No caso do Triton, bastam quatro informações, e
todas estão disponíveis sem esforço: a versão do programa, que aparece no relatório; a origem da
série de precipitação, com o período utilizado; a estrutura tarifária adotada, com a data de
entrada em vigor; e a declaração de quais os parâmetros alterados em relação aos valores por
omissão. A secção {{n:13}} traz a lista completa, com um parágrafo de método pronto a adaptar.

Anexar o ficheiro `.triton` ao material suplementar resolve as quatro de uma só vez, porque o
ficheiro é autocontido: traz a série de chuva dentro dele ou, com a chuva da base (Iberia01 ou E-OBS), a
referência da série e a sua impressão digital, que o programa recompõe a partir da base. É a forma
mais económica de tornar um estudo verificável por terceiros, e custa um pequeno anexo.
