# Método, estatística e limites

> **Pergunta a que esta secção responde:** como calcula a modulação, e até onde se pode confiar
> nela?

## O procedimento

A modulação é uma simulação de Monte Carlo sobre a cadeia completa do programa. Para N realizações
com a semente s:

1. o programa executa o caso-base, com as premissas do estudo;
2. sorteia, de uma só vez, N valores de cada variável marcada, com o gerador pseudoaleatório
   iniciado pela semente;
3. para cada realização, copia o projeto, troca as premissas pelos valores sorteados e refaz a
   cadeia técnica, económica, ambiental e TOPSIS para **todos** os volumes da varredura;
4. reúne as N realizações em estatísticas por volume e no volume escolhido.

A comparação entre volumes é **emparelhada**: numa realização, todos os volumes enfrentam as mesmas
premissas sorteadas, e a diferença entre dois deles é efeito do volume, e não do sorteio. É o que
permite contar com que frequência cada volume vence. A grelha de volumes é a do estudo, e o
programa interrompe a análise se ela mudar entre realizações.

## As estatísticas

Os percentis são empíricos, calculados sobre as realizações; o desvio-padrão é o amostral, e o
coeficiente de variação a razão entre ele e o módulo da média. As probabilidades vêm com o
intervalo de 95% de Wilson (1927). A sensibilidade é o ρ de Spearman (1904), com os empates no
posto médio. A parte da variância explicada é a razão de correlação η², a variância entre as
médias de classe dividida pela variância total; as classes são os decis da variável sorteada, ou
os seus próprios valores quando ela tem até dez valores distintos, como o número de pessoas. É o
estimador por classes do índice de primeira ordem (Saltelli et al., 2008), calculado com as mesmas
realizações, sem custo adicional.

A convergência acompanha-se pela média acumulada do valor atual líquido no volume escolhido e pelo
respetivo intervalo de 95%, cuja meia largura é igual a 1,96 vezes o desvio-padrão dividido pela
raiz quadrada do número de realizações. A faixa estreita-se com o inverso da raiz de N: quadruplicar
as realizações reduz para metade a incerteza do sorteio. Se a faixa ainda oscilar no fim da curva,
aumente N antes de publicar.

## Limites

- **As variáveis são independentes.** O programa não impõe correlação entre elas. Em muitos
  projetos isso é razoável; quando duas premissas andam juntas — mais pessoas e mais procura
  exterior, por exemplo —, sortear de forma independente alarga a gama para além do real em
  algumas combinações e estreita-a noutras.
- **A incerteza é a declarada.** A gama de saída nunca é mais fiável do que as distribuições de
  entrada. Os valores de triagem são genéricos; ajuste-os com dados do edifício, de medição ou da
  literatura, e declare a fonte.
- **A chuva varia por fator.** O fator da chuva escala a série inteira e preserva a sua estrutura
  temporal — a sequência de dias secos e chuvosos. Uma alteração dessa estrutura, ou um cenário
  climático diferente, não é sorteada: compare-os executando a modulação uma vez para cada série.
  O efeito do comprimento da série tem estudo próprio (secção {{n:24}}).
- **O que não está no catálogo fica fixo.** O preço de cada material em separado, os parâmetros da
  eletrobomba, a dose de cloro e as restantes premissas seguem o estudo. A análise de
  sensibilidade da secção {{n:20}} cobre as que faltam, uma de cada vez.
- **O η² por classes tem viés.** Com k classes e N realizações, sobrestima a parte explicada em
  cerca de (k − 1)/N — 0,009 com dez classes e mil realizações. Valores desta ordem não distinguem
  uma variável sem efeito.

A modulação probabilística dá a incerteza do resultado a partir da incerteza das premissas; não é
uma validação do modelo, que a secção {{n:34}} discute. Para uma introdução ao método e às suas
variantes — amostragem estratificada, índices de sensibilidade baseados na variância —, ver
Saltelli et al. (2008).
