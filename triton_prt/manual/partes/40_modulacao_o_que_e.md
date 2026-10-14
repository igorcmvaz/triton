# O que é a modulação probabilística

> **Pergunta que este capítulo responde:** o volume que o estudo escolheu continua
> sendo uma boa escolha quando as premissas não são exatamente as que eu declarei?

O estudo do Triton responde com um número por volume. Esse número vale para as premissas
declaradas: um consumo per capita, um número de pessoas, uma fração não potável, uma
área de captação, uma tarifa, uma taxa de desconto. Nenhuma delas é conhecida com
exatidão no projeto. O consumo per capita de uma casa que ainda não existe é estimado; a
ocupação muda ao longo da vida útil; a chuva dos próximos vinte anos não repete a dos
últimos trinta; a tarifa é revista.

A ferramenta **13. Modulação Probabilística** mede o quanto essas incertezas chegam ao
resultado. Ela refaz o estudo pronto muitas vezes — mil, por padrão —, cada vez com
as premissas escolhidas sorteadas de distribuições declaradas pelo usuário, e devolve a
**distribuição** do resultado em vez de um valor único: faixas de economia e de valor
presente líquido por volume, a probabilidade de o investimento se pagar e a frequência
com que cada volume seria o escolhido.

==O estudo determinístico não muda.== As etapas 5 a 9, os relatórios e a linha de
comando continuam com ele. A modulação é uma camada de robustez por cima do estudo: ela
não escolhe outro volume, ela diz o quanto a escolha resiste.

---

## Quando usar

A modulação responde a três perguntas que o estudo determinístico não responde:

1. **Quão largo é o resultado?** A economia do estudo vale com que margem? A faixa entre
   os percentis 5 e 95 das realizações é o número que deve acompanhar o resultado
   publicado.
2. **O investimento se paga com que probabilidade?** Um valor presente líquido positivo
   no caso-base pode esconder uma chance considerável de prejuízo; a modulação dá essa
   chance e o seu intervalo de confiança.
3. **A decisão de projeto é estável?** Se o volume escolhido vence numa minoria das
   realizações, ao lado de vizinhos com frequências parecidas, a escolha é frágil e o
   texto precisa dizer isso.

No exemplo do tutorial, na seção {{n:43}}, as três respostas aparecem em números.

Ela é a continuação natural da análise de sensibilidade da seção {{n:20}}. A sensibilidade
varia uma premissa de cada vez; a modulação varia todas as escolhidas ao mesmo tempo, com
pesos que vêm das distribuições, e permite ver combinações que um tornado não mostra.

## O que ela não faz

A modulação não substitui um dado medido. Uma distribuição larga em torno de um valor
errado continua centrada no valor errado: quando houver medição de consumo, ela vale mais
que qualquer sorteio. As distribuições iniciais que a tela propõe são **de triagem** —
centradas no projeto, com larguras genéricas — e precisam ser ajustadas ao que se sabe da
edificação. A seção {{n:44}} discute os limites do método.
