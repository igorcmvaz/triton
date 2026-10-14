# Método, estatística e limites

> **Pergunta que esta seção responde:** como a modulação calcula, e até onde se pode
> confiar nela?

## O procedimento

A modulação é uma simulação de Monte Carlo sobre a cadeia completa do programa. Para N
realizações com semente s:

1. o programa roda o caso-base, com as premissas do estudo;
2. sorteia, de uma vez, N valores de cada variável marcada, com o gerador pseudoaleatório
   iniciado pela semente, e, por último, o modelo climático de cada realização, se houver
   modelos marcados — de modo que marcar modelos não muda os demais sorteios da mesma
   semente;
3. para cada realização, copia o projeto, troca as premissas pelos valores sorteados — e a
   série de chuva pela do modelo sorteado — e refaz a cadeia técnica, econômica, ambiental
   e TOPSIS para **todos** os volumes da varredura;
4. reúne as N realizações em estatísticas por volume e no volume escolhido.

A comparação entre volumes é **pareada**: numa realização, todos os volumes enfrentam as
mesmas premissas sorteadas, e a diferença entre dois deles é efeito do volume, e não do
sorteio. É o que permite contar com que frequência cada volume vence. A grade de volumes é
a do estudo, e o programa interrompe a análise se ela mudar entre realizações.

## As estatísticas

Os percentis são empíricos, calculados sobre as realizações; o desvio-padrão é o amostral,
e o coeficiente de variação, a razão entre ele e o módulo da média. As probabilidades vêm
com o intervalo de 95% de Wilson (1927). A sensibilidade é o ρ de Spearman (1904), com empates no posto médio.
A parte da variância explicada é a razão de correlação η², a variância entre as médias de
classe dividida pela variância total; as classes são os decis da variável sorteada, ou os
seus próprios valores quando ela tem até dez valores distintos, como o número de pessoas e o
modelo climático. É o estimador por classes do índice de primeira ordem (Saltelli et al.,
2008), calculado com as mesmas realizações, sem custo adicional.

A convergência é acompanhada pela média acumulada do valor presente líquido no volume
escolhido e pelo seu intervalo de 95%, de meia largura igual a 1,96 vezes o desvio-padrão
dividido pela raiz do número de realizações. A faixa estreita com o inverso da raiz de N:
quadruplicar as realizações reduz pela metade a incerteza do sorteio. Se a faixa ainda
oscila no fim da curva, aumente N antes de publicar.

## Limites

- **As variáveis são independentes.** O programa não impõe correlação entre elas. Em
  muitos projetos isso é razoável; quando duas premissas andam juntas — mais pessoas e
  mais demanda externa, por exemplo —, sortear de forma independente alarga a faixa além
  do real em algumas combinações e a estreita em outras.
- **A incerteza é a declarada.** A faixa de saída nunca é mais confiável que as
  distribuições de entrada. Os valores de triagem são genéricos; ajuste-os com dados da
  edificação, de medição ou de literatura, e declare a fonte.
- **A chuva varia por fator ou por modelo.** O fator da chuva escala a série inteira e
  preserva a sua estrutura temporal — a sequência de dias secos e chuvosos. O sorteio entre
  modelos climáticos troca essa estrutura, mas só entre os dezenove modelos da base, com
  pesos iguais, para o cenário e o período do projeto. A incerteza de cenário — SSP2-4.5
  ou SSP5-8.5 — não é sorteada: compare os cenários rodando a modulação uma vez em cada. O
  efeito do comprimento da série tem estudo próprio (seção {{n:24}}).
- **O que não está no catálogo fica fixo.** O preço de cada material em separado, os
  parâmetros da motobomba, a dose de cloro, o IPTU Verde e as demais premissas seguem o
  estudo. A análise de sensibilidade da seção {{n:20}} cobre as que faltam, uma de cada
  vez.
- **O η² por classes tem viés.** Com k classes e N realizações, ele superestima a parte
  explicada em cerca de (k − 1)/N — 0,009 com dez classes e mil realizações. Valores dessa
  ordem não distinguem uma variável sem efeito.

A modulação probabilística dá a incerteza do resultado a partir da incerteza das premissas; ela
não é uma validação do modelo, que a seção {{n:34}} discute. Para uma introdução ao método
e às suas variantes — amostragem estratificada, índices de sensibilidade baseados em
variância —, ver Saltelli et al. (2008).
