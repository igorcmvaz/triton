# Limitações conhecidas

> Onde o programa não serve, e por quê. Um programa que declara os próprios limites é
> mais confiável que um que aparenta servir para tudo, porque o segundo transfere ao
> usuário a tarefa de descobri-los por conta própria.

Esta seção deriva do registro de pendências que o grupo de pesquisa mantém, e reflete o
estado da versão 0.1.0 (beta). Uma limitação sai desta lista quando é efetivamente resolvida, e
não quando deixa de ser mencionada — distinção que parece óbvia e que a documentação de
programas científicos frequentemente não observa.

As limitações estão agrupadas por origem, porque a providência que cada grupo admite é
diferente. As do modelo decorrem de escolhas de representação e só mudam com uma revisão
do próprio modelo. As dos dados dependem de levantamento, e podem ser supridas pelo
usuário. As metodológicas são desvios declarados em relação a uma formulação de
referência. E as de implementação são trabalho pendente, sem obstáculo conceitual.

---

## Limitações do modelo

**Não há sub-passo horário.** Uma chuva de 40 mm concentrada em duas horas e a mesma
lâmina distribuída em vinte e quatro horas produzem o mesmo resultado. Para
reservatórios muito pequenos em relação à área de captação, isso subestima o
extravasamento.

**Não há perdas no reservatório.** Evaporação e vazamento não são modelados.

**A condição inicial é reservatório vazio.** Em séries de menos de um ano, isso
penaliza o resultado de forma sensível.

**O coeficiente de escoamento é único e constante.** Não varia com a intensidade da
chuva nem com o tempo desde o último evento, quando na realidade o primeiro evento
após uma estiagem tem coeficiente menor.

**O descarte é uma lâmina, não um dispositivo.** O programa calcula o volume e o custo
do dispositivo, `A × d_f`, mas não o seu arranjo hidráulico, que exige projeto à parte.

---

## Limitações dos dados tarifários

Estas limitações dizem respeito ao catálogo da Edição Brasil. Na International Edition não
há catálogo: a tarifa é digitada, e a exatidão dela é do usuário.

**O catálogo tarifário cobre quase só a categoria residencial.** Os 652 municípios da
base trazem a estrutura residencial; as categorias não residenciais só entram com a
tabela oficial do prestador, e hoje estão transcritas nos municípios da CORSAN — comercial
e pública em 34, industrial em 30. Nos demais, as categorias comercial, industrial e
pública, que existem em toda concessionária e costumam ser mais caras, precisam ser
lançadas à mão pelo usuário, conforme a seção {{n:16}} descreve. Enquanto não forem, um
estudo de escola, comércio ou indústria calcula a economia com a tarifa residencial, e
portanto a **subestima**: o erro é conservador e tem sentido conhecido, mas precisa ser
declarado. O apêndice {{n:D}} mostra, município a município, o que já foi coletado.

**Cinco municípios da BRK Tocantins com tarifa decrescente** na primeira faixa, o que
subestima a fatura no primeiro bloco.

**Quatorze municípios com esgoto por faixas próprias**, representados por percentual
único. É aproximação declarada.

**Sem tarifa social nem bandeiras de água.** A classe de baixa renda é mal
representada. Na CASAN, a tarifa social é de R$ 8,63 contra R$ 46,34 da
disponibilidade comum — diferença que inverteria a conclusão de um estudo em
habitação de interesse social.

---

## Limitações da avaliação de ciclo de vida

**É uma avaliação de triagem**, e não um inventário conforme a ISO 14040.

**Uma única categoria de impacto.** Só carbono. Não há eutrofização, acidificação,
uso do solo nem toxicidade.

**A emissão de fabricação da motobomba é aproximação por massa.** O programa multiplica
a massa de catálogo de cada potência pela intensidade por quilo de uma declaração
ambiental de produto de bomba de outra classe. A ordem de grandeza é defensável; o valor
de cada potência não é medição.

**A pressurização direta é modelada por valores médios.** A energia usa uma pressão de
trabalho única, a média da faixa do pressostato, e não o ciclo liga-desliga de cada uso;
e não se soma energia de partida nem consumo em espera, que um pressurizador com inversor
de frequência teria. Projetos antigos sem caixa superior abrem com o arranjo «não
informado» e não recebem energia até que ele seja escolhido.

**Não há fim de vida.** Nem crédito por reciclagem, nem ônus por disposição.

**Não há manutenção.** Trocas de componente ao longo da vida útil não entram.

---

## Limitações da qualidade da água

**As classes 2 a 4 são adaptações do programa**, não da NBR 15527. A matriz de
parâmetros por uso é característica da versão de 2007 da norma e não sobreviveu à
revisão de 2019.

**As constantes do modelo de lavagem da cobertura não são calibradas.** A qualidade
da água resultante é **premissa**, e não medição. O programa não substitui ensaio
laboratorial.

---

## Limitações metodológicas declaradas

**O percentil do R95p é calculado sobre a série inteira**, e não sobre a base fixa
1961–1990 do ETCCDI. Séries de comprimentos diferentes não são diretamente
comparáveis nesse índice.

**As condições C1 e C2 de Opricovic não estão implementadas** no VIKOR. A solução de
compromisso deve ser lida com a análise de sensibilidade de pesos ao lado.

**A normalização do TOPSIS é uma variante** com translação por `x − min(x)`, para
admitir valor presente líquido negativo.

**O reajuste tarifário é percentual único** ao longo de todo o período de análise, o
que torna frágil a projeção de vinte anos. É a premissa que mais move o resultado
econômico.

---

## Limitações de implementação

**Seis campos são gravados no arquivo e nunca lidos.** Entre eles o **mês de
instalação**, de modo que o fluxo de caixa começa sempre no mês 1.

**A importação de projeto do Netuno 4 não reconhece demanda variável**, e a degrada
para constante em silêncio. A seção {{n:21}} ensina a conferir.

**O tempo de partida da motobomba, de 108 s por acionamento**, representa o tempo de
escorva de uma bomba cuja linha de sucção drenou, e é aplicado a **toda** partida. No
caso de referência responde por 19% do consumo anual da bomba. É conservador.

**Não há opção para tratar o descarte como limiar do evento**, como fazia o Netuno 4,
embora o protocolo de verificação a mencione. Para comparar as duas versões, use
descarte igual a zero, em que as duas regras coincidem.

---

## O que fazer com esta lista

Num trabalho publicado, cite as limitações que afetam o seu caso — não todas, que
transformaria a seção de método numa lista defensiva, mas as que efetivamente incidem
sobre as conclusões apresentadas. ==Uma limitação declarada é uma ressalva; uma limitação
omitida, quando descoberta, é um erro.==

Três exemplos orientam a seleção. Um estudo conduzido em escola precisa citar a questão da
categoria tarifária, porque ela desloca todo o resultado econômico. Um estudo de
desempenho ambiental precisa citar a categoria única de impacto e a aproximação por massa do
fator de emissão da motobomba. E um estudo em habitação de interesse social precisa citar a
ausência de tarifa social, que nesse contexto pode inverter a conclusão.

Um parecerista que encontre uma dessas limitações silenciada tem inteira razão em
cobrá-la, e a cobrança costuma custar mais tempo do que a declaração teria custado.
