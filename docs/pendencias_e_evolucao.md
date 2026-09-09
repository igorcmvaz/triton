# Pendências, melhorias e evolução — Netuno 5.0.8

Levantamento de **toda a estrutura** do projeto: 47.212 linhas em `netuno/`,
12.682 em `tests/`, 687 testes verdes. O que segue é o que **não** está resolvido,
ordenado por consequência sobre o resultado de um estudo, e não por esforço.

Cada item traz o que se sabe, o que falta e por que importa. Onde a decisão é
sua, está dito.

---

## Sumário

| # | Pendência | Consequência | Quem decide |
| :-- | :--- | :--- | :--- |
| 1 | Quatro municípios sem tarifa de excedente | payback nulo por defeito de cadastro | dado externo |
| 2 | Cinco municípios da BRK Tocantins com tarifa decrescente | conta subestimada no primeiro bloco | dado externo |
| 3 | Categoria tarifária fixa em Residencial | comercial e público fora do alcance | você |
| 4 | Esgoto tratado como percentual único | superestima onde há faixa própria | você |
| 5 | Emissão de fabricação da motobomba extrapolada | único fator sem fonte primária na ACV | dado externo |
| 6 | Reajuste tarifário como percentual único | projeção de 20 anos frágil | você |
| 7 | Sem tarifa social nem bandeiras de água | classe de baixa renda mal representada | você |
| 8 | Wash-off com constantes não calibradas | qualidade da água é premissa, não medida | você |
| 9 | `tariff_updater` com cobertura mínima | raspagem quebra em silêncio | eu |
| 10 | Percentil do P95 sobre a série toda | diverge do ETCCDI | você |
| 11 | Constantes de domínio repetidas | divergência futura | eu |
| 12 | Módulos de 2.000+ linhas | manutenção | eu |

---

## 1. Quatro municípios sem tarifa de excedente

**Situação.** Sete Lagoas (MG), Bebedouro, Pirassununga e São José do Rio Pardo
(SP) têm apenas o bloco mínimo cadastrado: até 6 ou 10 m³ o valor é conhecido, e
acima disso não há tarifa nenhuma na base.

**Efeito.** A conta não cresce com o consumo. Economizar água não a reduz, e o
aproveitamento pluvial aparece **sem retorno nenhum** — não porque seja inviável,
mas porque falta dado.

**O que foi feito.** Os quatro estão marcados com `estrutura_incompleta`,
rebaixados para confiança D, e a tela de tarifas avisa ao selecioná-los. Um teste
impede que um quinto apareça sem ser notado.

**O que falta.** A tarifa de excedente, das resoluções dos respectivos SAAEs.
Não a reconstruí porque qualquer número seria invenção.

---

## 2. Cinco municípios da BRK Tocantins com tarifa decrescente

**Situação.** Araguaína, Gurupi, Palmas, Paraíso do Tocantins e Porto Nacional
têm a primeira faixa a R$ 8,76/m³ e a segunda a R$ 3,05/m³.

**Efeito.** Tarifa decrescente não é usual e tem a assinatura de um mínimo mensal
diluído em tarifa unitária — o mesmo defeito corrigido em seis outros municípios.
Se for isso, R$ 8,76 × 5 m³ = R$ 43,80 seria o mínimo mensal, e consumir 2 m³
custaria R$ 43,80 e não R$ 17,52.

**Por que não corrigi.** Nos seis casos corrigidos a prova estava no próprio
registro: `tarifa_fixa_mensal` batia exatamente com tarifa × volume. Aqui o
registro não declara mínimo algum, então falta a prova. Corrigir por semelhança
seria adivinhar.

**O que falta.** A estrutura publicada pela BRK Tocantins. Marcados com
`estrutura_suspeita` e confiança C.

---

## 3. Categoria tarifária fixa em Residencial

**Situação.** As 652 estruturas são da categoria **Residencial**. Os catálogos
das concessionárias trazem também Comercial, Industrial, Público e Público
Especial, com tarifas bem diferentes — na CASAN, a faixa de 0 a 10 m³ custa
R$ 3,08/m³ no residencial e R$ 6,81/m³ no comercial, mais que o dobro.

**Efeito.** Um estudo em escola, hospital ou indústria — que é onde o
aproveitamento pluvial costuma ter melhor retorno, pela escala — usa a tarifa
errada, e subestima a economia em mais de 100%.

**Caminho.** A estrutura de dados já suporta: bastaria uma chave `categorias`
dentro de cada município e um seletor na tela. O trabalho é de coleta, não de
código.

**Decisão sua.** Se o alvo do programa é residencial, isto vira apenas uma
ressalva de escopo a declarar. Se não é, é a maior lacuna de dado do projeto.

---

## 4. Esgoto tratado como percentual único

**Situação.** O esgoto entra como percentual da conta de água (`esgoto_pct`),
100% na CASAN e 80% em várias outras.

**O que isso não cobre.** Algumas concessionárias têm **estrutura de faixas
própria** para esgoto, e não um percentual. Outras cobram esgoto só sobre o
volume medido acima do mínimo. Outras aplicam percentuais diferentes por faixa.

**Efeito.** Onde o esgoto tem estrutura própria, o percentual único erra a conta,
e o erro é grande: o esgoto costuma ser a metade da fatura.

**Caminho.** O motor já aceita `sewage_mode` 0 (fixo) e 1 (percentual). Faltaria
um modo 2, com faixas próprias, e a coleta correspondente.

---

## 5. Emissão de fabricação da motobomba

**Situação.** É o **único** fator da avaliação de ciclo de vida que continua sem
fonte primária. Quatro dos seis valores são escalonamento aritmético do valor de
0,5 CV.

**O que foi feito.** A interface passou a marcá-los como VALOR EXTRAPOLADO na
justificativa do campo, de modo que o usuário vê o estatuto do número.

**O que falta.** Uma declaração ambiental de produto de fabricante de motobomba,
ou um inventário publicado por potência. Procurei e não encontrei na
granularidade necessária.

**Consequência prática.** É pequena: a bomba responde por parcela menor do
carbono incorporado que os reservatórios e a tubulação. Mas é a única lacuna
declarada do módulo, e num artigo ela será perguntada.

---

## 6. Reajuste tarifário como percentual único

**Situação.** A projeção de 20 anos usa um percentual anual fixo para água,
esgoto e energia, informado pelo usuário.

**Efeito.** O valor presente líquido a 20 anos é muito sensível a esse número, e
ele é o parâmetro menos fundamentado do módulo econômico. Reajustes reais variam
com IPCA, com revisões tarifárias quadrienais e com decisões das agências.

**Caminho.** Duas melhorias independentes: (a) alimentar o padrão com a série
histórica de reajustes da própria concessionária, que as agências publicam; (b)
oferecer análise de sensibilidade sobre esse parâmetro, mostrando a faixa de VPL
em vez de um número.

**A segunda é a mais valiosa** e não depende de coleta.

---

## 7. Sem tarifa social nem estrutura de bandeiras

**Situação.** A base traz a categoria Residencial comum. A **Residencial Social**
existe e é bem diferente — na CASAN, TFDI de R$ 8,63 contra R$ 46,34, e
R$ 0,58/m³ contra R$ 3,08 na primeira faixa.

**Efeito.** Habitação de interesse social é justamente onde o aproveitamento
pluvial tem apelo de política pública, e é onde o programa erra mais: com tarifa
social, a economia monetária é uma fração da calculada, e o payback estoura.

**Observação.** O valor da tarifa social já aparece na tabela da CASAN que
conferi. A coleta é viável para as concessionárias maiores.

---

## 8. Wash-off com constantes não calibradas

**Situação.** O modelo de lavagem do telhado usa constantes k de 1,6, 1,3 e
1,1 mm⁻¹. A documentação afirmava que foram «calibradas a partir de dados
experimentais» sem mostrar o ajuste.

**O que falta.** Ou mostrar a calibração, ou declarar que são premissa. A segunda
é honesta e barata; a primeira exige dados que talvez não existam.

**Efeito.** A eficiência de descarte alimenta a classe de qualidade alvo, que
agora move investimento e emissão pela ligação da linha de tratamento. Deixou de
ser um número decorativo.

---

## 9. `tariff_updater` com cobertura mínima

**Situação.** O subpacote de atualização automática tem 2.197 linhas em quatro
módulos. Até esta rodada não tinha teste nenhum.

**O que foi feito.** Uma porta de validação estrutural antes de gravar, com os
primeiros sete testes. A porta conserva o registro anterior do município cuja
estrutura nova tem erro e o manda para revisão manual.

**O que falta.** Teste dos raspadores em si, com páginas gravadas como fixture.
Sem isso, uma concessionária que mude o layout do site produz falha silenciosa —
a porta impede que o dado errado entre, mas não avisa que o dado parou de vir.

---

## 10. Percentil do P95 sobre a série inteira

**Situação.** O índice R95p calcula o percentil 95 sobre **toda a série
carregada**. O ETCCDI define período-base fixo de 1961 a 1990.

**Efeito.** Os valores não são diretamente comparáveis com a literatura de
extremos que usa a definição padrão. Com séries de projeção climática, a
diferença cresce.

**Caminho.** Ou implementar o período-base configurável, ou declarar a escolha
na documentação do índice. A segunda já está feita em parte.

**Nota relacionada.** O conjunto é chamado «ETCCDI + Sazonalidade» porque inclui
o índice de Walsh & Lawler, que não é ETCCDI, e omite o R10mm, que é. Está
declarado, mas o R10mm continua ausente e seria barato acrescentar.

---

## 11. Constantes de domínio repetidas

**Situação.** A varredura encontra `365.25` em 14 módulos e `0.85` em 10.
`hydrology_defaults.py` existe e define o coeficiente de escoamento padrão, mas
nem todos os módulos o consomem.

**Efeito.** Nenhum hoje. O risco é de amanhã: alterar um e não os outros produz
divergência entre telas, que foi exatamente como o cloro chegou a ter cinco
convenções nesta versão.

**Caminho.** Um módulo de constantes de domínio, com dias do ano, coeficiente de
escoamento e vida útil, e substituição gradual.

---

## 12. Módulos de 2.000 linhas ou mais

| Módulo | Linhas |
| :--- | ---: |
| `core/report_generator.py` | 2.404 |
| `ui/dialogs/dialog_economic.py` | 2.326 |
| `ui/translation.py` | 2.101 |
| `ui/tab_documentation.py` | 2.056 |
| `cli.py` | 2.021 |

**Efeito.** Nenhum sobre resultado. Sobre manutenção, sim: `dialog_economic.py`
concentra sete diálogos independentes, e `report_generator.py` três geradores de
relatório com HTML literal.

**Caminho.** Separar por diálogo e por relatório, sem mudar comportamento, com a
suíte atual como rede.

---

## O que esta rodada resolveu

Registrado para não gerar retrabalho.

- **Regimes de tarifa mínima** nomeados, declarados nos 652 municípios e
  validados por teste. O motor ganhou o piso de pagamento, que lhe faltava.
- **21 registros tarifários defeituosos**: 12 corrigidos com a reconstrução
  documentada, 9 sinalizados com confiança rebaixada e aviso na tela.
- **Florianópolis conferida** contra a Tabela Tarifária CASAN 04/2026: a TFDI de
  R$ 46,34 e as quatro faixas batem exatamente. É taxa de disponibilidade e não
  consumo mínimo, de modo que na área da CASAN **cada metro cúbico economizado
  gera desconto desde o primeiro**.
- **Porta de validação** antes do gravador automático de tarifas.
- **Duplicação de códigos de faixa** que eu havia introduzido, unificada.

---

## Como eu ordenaria

1. **Item 3, categoria tarifária.** É a maior lacuna de dado, e decide se o
   programa serve para não residencial.
2. **Item 6b, sensibilidade do reajuste.** Não depende de coleta e melhora a
   honestidade do valor presente líquido de imediato.
3. **Itens 1 e 2**, os nove municípios, quando houver acesso às resoluções.
4. **Item 7, tarifa social**, se o uso em habitação de interesse social estiver
   no horizonte.
5. **Item 9**, fixtures dos raspadores, antes que uma concessionária mude o site.

Os itens 11 e 12 são meus e não precisam da sua decisão: entram quando houver
folga, sem alterar comportamento.
