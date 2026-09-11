# 36. Limitações conhecidas

> Onde o programa não serve, e por quê. Um programa que declara seus limites é mais
> confiável que um que finge servir para tudo.

Este capítulo é derivado do registro de pendências do repositório, mantido em
`docs/pendencias_e_evolucao.md`, e reflete o estado da versão 5.0.8.

---

## 36.1. Limitações do modelo

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

**O descarte é uma lâmina, não um dispositivo.** O volume hidráulico do reservatório
de autolimpeza exige dimensionamento à parte.

---

## 36.2. Limitações dos dados tarifários

**A categoria tarifária é residencial, e só ela.** Os 652 municípios da base trazem
a estrutura residencial. Escola, hospital, comércio e indústria são faturados em
categorias mais caras, e o programa avisa que o resultado econômico está
**subestimado** quando a tipologia não é residencial. É a maior lacuna de dado do
programa.

**Quatro municípios sem tarifa de excedente.** Sete Lagoas, Bebedouro, Pirassununga e
São José do Rio Pardo têm a tabela truncada na base, o que produz conta que não se
move acima de certo consumo. Aguardam as resoluções dos respectivos serviços
autônomos.

**Cinco municípios da BRK Tocantins com tarifa decrescente** na primeira faixa, o que
subestima a conta no primeiro bloco.

**Quatorze municípios com esgoto por faixas próprias**, representados por percentual
único. É aproximação declarada.

**Sem tarifa social nem bandeiras de água.** A classe de baixa renda é mal
representada. Na CASAN, a tarifa social é de R$ 8,63 contra R$ 46,34 da
disponibilidade comum — diferença que inverteria a conclusão de um estudo em
habitação de interesse social.

---

## 36.3. Limitações da avaliação de ciclo de vida

**É uma avaliação de triagem**, e não um inventário conforme a ISO 14040.

**Uma única categoria de impacto.** Só carbono. Não há eutrofização, acidificação,
uso do solo nem toxicidade.

**A emissão de fabricação da motobomba é extrapolada.** Quatro dos seis valores são
extrapolação aritmética a partir do valor de meio CV. É o único fator do inventário
sem fonte primária, e carrega rótulo de triagem.

**Não há fim de vida.** Nem crédito por reciclagem, nem ônus por disposição.

**Não há manutenção.** Trocas de componente ao longo da vida útil não entram.

---

## 36.4. Limitações da qualidade da água

**As classes 2 a 4 são adaptações do programa**, não da NBR 15527. A matriz de
parâmetros por uso é característica da versão de 2007 da norma e não sobreviveu à
revisão de 2019.

**As constantes do modelo de lavagem da cobertura não são calibradas.** A qualidade
da água resultante é **premissa**, e não medição. O programa não substitui ensaio
laboratorial.

---

## 36.5. Limitações metodológicas declaradas

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

## 36.6. Limitações de implementação

**Seis campos são gravados no arquivo e nunca lidos.** Entre eles o **mês de
instalação**, de modo que o fluxo de caixa começa sempre no mês 1.

**A importação de projeto do Netuno 4 não reconhece demanda variável**, e a degrada
para constante em silêncio. O guia 21 ensina a conferir.

**O tempo de partida da motobomba, de 108 s por acionamento**, representa o tempo de
escorva de uma bomba cuja linha de sucção drenou, e é aplicado a **toda** partida. No
caso de referência responde por 19% do consumo anual da bomba. É conservador.

**A opção `--descarte-como-limiar`, citada no protocolo de verificação, não
existe.**

---

## 36.7. O que fazer com esta lista

Num estudo publicado, **cite as limitações que afetam o seu caso**. Não todas: as
que afetam.

Um estudo em escola precisa citar a categoria tarifária. Um estudo ambiental precisa
citar a categoria única de impacto e o fator da motobomba. Um estudo em habitação de
interesse social precisa citar a ausência de tarifa social.

Um revisor que encontre uma dessas limitações não declarada tem razão em cobrá-la.
