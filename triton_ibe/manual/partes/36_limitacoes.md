# Limitações conhecidas

> Onde o programa não serve, e porquê. Um programa que declara os próprios limites é mais
> fiável do que um que aparenta servir para tudo, porque o segundo deixa ao utilizador a tarefa de
> os descobrir por conta própria.

Esta secção deriva do registo de pendências que o grupo de investigação mantém, e reflete o estado
da versão beta atual, a 0.2.0. Uma limitação sai desta lista quando é efetivamente resolvida, e
não quando deixa de ser mencionada — distinção que parece óbvia e que a documentação dos programas
científicos muitas vezes não observa.

As limitações estão agrupadas por origem, porque a providência que cada grupo admite é diferente.
As do modelo decorrem de escolhas de representação e só mudam com uma revisão do próprio modelo.
As dos dados dependem de levantamento, e podem ser supridas pelo utilizador. As metodológicas são
desvios declarados em relação a uma formulação de referência. E as de implementação são trabalho
pendente, sem obstáculo conceptual.

---

## Limitações do modelo

**Não há subpasso horário.** Uma chuva de 40 mm concentrada em duas horas e a mesma lâmina
repartida por vinte e quatro horas produzem o mesmo resultado. Para reservatórios muito pequenos
face à área de captação, isto subestima o extravasamento.

**Não há perdas no reservatório.** A evaporação e as fugas não são modeladas.

**A condição inicial é o reservatório vazio.** Em séries de menos de um ano, isto penaliza o
resultado de forma sensível.

**O coeficiente de escoamento é único e constante.** Não varia com a intensidade da chuva nem com o
tempo decorrido desde o último evento, quando na realidade o primeiro evento após uma estiagem tem
um coeficiente menor.

**O descarte é uma lâmina, e não um dispositivo.** O programa calcula o volume e o custo do
dispositivo, `A × d_f`, mas não o seu arranjo hidráulico, que exige um projeto à parte.

---

## Limitações dos dados de chuva e de tarifário

**A chuva por concelho é uma média de grelha.** Em Lisboa e no Porto, a série é a média diária das
células da grelha (Iberia01 ou E-OBS, 0,1°) do município, e não o registo de um posto. O Iberia01 vai só até 2015; Canárias, Madeira e Açores são ERA5 de 0,25° (nível C), que subestima a chuva; Ceuta e Melilla não têm série. Nas tarifas, Espanha só tem a média regional do INE (indicativa) e Portugal, três concelhos transcritos. O Iberia01 cobre 278 dos 308
concelhos de Portugal; os 30 das ilhas (Madeira e Açores) estão fora do seu domínio e usam a reanálise
ERA5. O Funchal usa um nó de 0,25° (cerca de 25 km), com chuva em 42% dos dias, e é a série menos fiável das três. Para um
projeto real, use a série medida.

**O tarifário cobre três cidades e só o utilizador doméstico.** Estão transcritos os tarifários de
Lisboa (EPAL e Câmara Municipal de Lisboa), do Porto (Águas e Energia do Porto) e do Funchal
(Câmara Municipal do Funchal), todos do escalão geral de utilizador doméstico, com contador até
25 mm (no Funchal, até 15 mm). Noutros concelhos, ou noutras categorias, a estrutura tem de ser
introduzida à mão pelo utilizador, e a sua exatidão é dele. Um estudo de escola, comércio ou
indústria calcula a poupança com a estrutura que estiver introduzida; se for a doméstica, o
resultado é em regra **subestimado**: o erro é conservador e tem sentido conhecido, mas precisa de
ser declarado. O programa avisa quando a tipologia não é residencial, e a secção {{n:16}} descreve
como se introduz a estrutura da categoria certa.

**Há hipóteses de transcrição por confirmar.** No Funchal, a taxa de IVA de 4% não foi confirmada
(com 5%, a fatura de 10 m³ passaria de 17,0872 € para 17,2515 €), e o primeiro escalão (até 5 m³)
do saneamento e dos resíduos não tem valor impresso e foi tratado como zero. No Porto, a
disponibilidade de água de 0,1242 € por dia foi lida da página dos utilizadores domésticos, e a
taxa de recursos hídricos das águas residuais não foi incluída. Em Lisboa, o adicional da Câmara
foi tratado sem IVA. As hipóteses estão registadas junto dos exemplos da edição.

**O saneamento é aproximado.** O saneamento faturado por escalões próprios representa-se por uma
percentagem única da fatura da água, por um valor fixo ou por um preço por metro cúbico. É uma
aproximação declarada.

**Não há tarifa social nem sobretaxas sazonais ou de escassez.** Uma classe de baixos rendimentos,
uma sobretaxa de seca ou um preço sazonal não são modelados, a menos que o utilizador os incorpore
na estrutura introduzida. Num estudo de habitação social, a diferença pode inverter a conclusão.

**A eletricidade só tem tarifa registada no Funchal**, e de fonte secundária (a confirmar na
entidade). Em Lisboa e no Porto, o custo da bombagem depende do preço do quilowatt-hora que o
utilizador introduzir; os casos do manual usam um valor ilustrativo, que não é preço de mercado.

---

## Limitações da avaliação de ciclo de vida

**É uma avaliação de triagem**, e não um inventário conforme a ISO 14040.

**Uma única categoria de impacto.** Só carbono. Não há eutrofização, acidificação, uso do solo nem
toxicidade.

**A emissão de fabrico da eletrobomba é uma aproximação por massa.** O programa multiplica a massa
de catálogo de cada potência pela intensidade por quilograma de uma declaração ambiental de produto
de uma bomba de outra classe. A ordem de grandeza é defensável; o valor de cada potência não é uma
medição.

**A pressurização direta é modelada por valores médios.** A energia usa uma pressão de trabalho
única, a média da gama do pressostato, e não o ciclo de ligar e desligar de cada uso; e não se
soma energia de arranque nem consumo em vazio, que um sobrepressor com variador de frequência
teria. Os projetos antigos sem reservatório superior abrem com o arranjo «não informado» e não
recebem energia até que um seja escolhido.

**Não há fim de vida.** Nem crédito por reciclagem, nem encargo por deposição.

**Não há manutenção.** As substituições de componentes ao longo da vida útil não entram.

---

## Limitações da qualidade da água

**As classes 2 a 4 são adaptações do programa**, e não classes de uma norma. A matriz de
parâmetros por uso é uma convenção interna; declare-a como tal.

**As constantes do modelo de lavagem da cobertura não estão calibradas.** A qualidade da água que
daí resulta é uma **premissa**, e não uma medição. O programa não substitui o ensaio laboratorial.

---

## Limitações metodológicas declaradas

**O percentil do R95p é calculado sobre a série inteira**, e não sobre o período-base fixo
1961–1990 do ETCCDI. As séries de comprimentos diferentes não são diretamente comparáveis neste
índice.

**As condições C1 e C2 de Opricovic não estão implementadas** no VIKOR. A solução de compromisso
deve ser lida com a análise de sensibilidade aos pesos ao lado.

**A normalização do TOPSIS é uma variante**, com translação por `x − min(x)`, para admitir um
valor atual líquido negativo.

**O resultado do TOPSIS depende do conjunto de candidatos.** O ideal e o anti-ideal saem dos
volumes avaliados: no tutorial, sete candidatos dão a faixa de escolha de 2 000 a 3 000 L, e a
varredura de 1 a 20 m³ só 1 000 L (secção {{n:32}}). Declare os candidatos junto com os pesos.

**A faixa de escolha depende da tolerância e da grade.** Não é um intervalo de confiança: a
tolerância, 5% da amplitude das pontuações por omissão, é uma declaração do estudo, e a faixa só
contém volumes avaliados.

**Os pesos do CRITIC dependem dos resultados.** Medem o contraste e a independência dos critérios
no conjunto avaliado, e não a preferência de ninguém: mudam quando os candidatos mudam.

**Os limiares do peso do sistema são do programa**, e não de norma: 500 kg na cobertura com o
reservatório cheio, 1 500 L de reservatório superior e 3 000 kg de cisterna a seco servem para
pedir a confirmação do projeto estrutural ou de fundações, e não para a dispensar.

**A atualização das tarifas é uma percentagem única** ao longo de todo o período de análise, o que
torna frágil a projeção a vinte anos. É a premissa que mais move o resultado económico.

---

## Limitações de implementação

**Seis campos são gravados no ficheiro e nunca lidos.** Entre eles o **mês de instalação**, pelo
que o fluxo de caixa começa sempre no mês 1.

**O tempo de arranque da eletrobomba, de 108 s por acionamento**, representa o tempo de
escorvamento de uma bomba cuja linha de aspiração se esvaziou, e é aplicado a **todo** o arranque.
É conservador.

**Não há opção para tratar o descarte como limiar do evento**, como fazem algumas outras
ferramentas. Para comparar com uma delas, use um descarte igual a zero, em que as duas regras
coincidem, ou a transformação da série da secção {{n:35}}.

---

## O que fazer com esta lista

Num trabalho publicado, cite as limitações que afetam o seu caso — não todas, o que transformaria a
secção de método numa lista defensiva, mas as que incidem de facto sobre as conclusões
apresentadas. ==Uma limitação declarada é uma ressalva; uma limitação omitida, quando descoberta,
é um erro.==

Três exemplos orientam a seleção. Um estudo conduzido numa escola precisa de citar a questão da
categoria tarifária, porque ela desloca todo o resultado económico. Um estudo de desempenho
ambiental precisa de citar a categoria única de impacto e a aproximação por massa do fator de
emissão da eletrobomba. E um estudo em habitação social precisa de citar a ausência de tarifa
social, que nesse contexto pode inverter a conclusão.

Um parecerista que encontre uma destas limitações silenciada tem toda a razão em cobrá-la, e a
cobrança costuma custar mais tempo do que a declaração teria custado.
