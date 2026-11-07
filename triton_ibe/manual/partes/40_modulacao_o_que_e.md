# O que é a modulação probabilística

> **Pergunta a que este capítulo responde:** o volume que o estudo escolheu continua a ser uma boa
> escolha quando as premissas não são exatamente as que declarei?

O estudo do Triton responde com um número por volume. Esse número vale para as premissas
declaradas: um consumo per capita, um número de pessoas, uma fração não potável, uma área de
captação, uma tarifa, uma taxa de atualização. Nenhuma delas é conhecida com exatidão na fase de
projeto. O consumo per capita de uma casa que ainda não existe é estimado; a ocupação muda ao longo
da vida útil; a chuva dos próximos vinte anos não repete a dos últimos trinta; os tarifários são
revistos.

A ferramenta **13. Modulação Probabilística** mede quanto dessas incertezas chega ao resultado.
Refaz o estudo pronto muitas vezes — mil, por omissão —, de cada vez com as premissas escolhidas
sorteadas a partir de distribuições declaradas pelo utilizador, e devolve a **distribuição** do
resultado em vez de um valor único: gamas de poupança e de valor atual líquido por volume, a
probabilidade de o investimento se pagar e a frequência com que cada volume seria o escolhido.

==O estudo determinístico não muda.== As etapas 5 a 9, os relatórios e a linha de comandos
continuam com ele. A modulação é uma camada de robustez por cima do estudo: não escolhe outro
volume, diz até que ponto a escolha resiste.

---

## Quando usar

A modulação responde a três perguntas a que o estudo determinístico não responde:

1. **Quão largo é o resultado?** Com que margem vale a poupança do estudo? A gama entre os
   percentis 5 e 95 das realizações é o número que deve acompanhar o resultado publicado.
2. **Com que probabilidade se paga o investimento?** Um valor atual líquido positivo no caso-base
   pode esconder uma probabilidade considerável de prejuízo; a modulação dá essa probabilidade e o
   respetivo intervalo de confiança. No tutorial de Lisboa, com os custos ilustrativos (não são
   preços de mercado) e a tarifa de Lisboa, o valor atual líquido do caso-base já é negativo, e a
   pergunta passa a ser outra: haverá alguma gama de premissas plausível em que o sistema se pague?
3. **A decisão de projeto é estável?** Se o volume escolhido vence numa minoria das realizações,
   ao lado de vizinhos com frequências parecidas, a escolha é frágil e o texto tem de o dizer.

No exemplo do tutorial, na secção {{n:43}}, mostra-se como se leem as três respostas.

É a continuação natural da análise de sensibilidade da secção {{n:20}}. A sensibilidade varia uma
premissa de cada vez; a modulação varia em simultâneo todas as escolhidas, com pesos que vêm das
distribuições, e permite ver combinações que um gráfico de tornado não mostra.

## O que ela não faz

A modulação não substitui um dado medido. Uma distribuição larga em torno de um valor errado
continua centrada no valor errado: quando houver medição de consumo, ela vale mais do que qualquer
sorteio. As distribuições iniciais que o ecrã propõe são **de triagem** — centradas no projeto,
com larguras genéricas — e têm de ser ajustadas ao que se sabe do edifício. A secção {{n:44}}
discute os limites do método.
