# Como relatar um problema

Programas de simulação têm defeitos, e o Netuno não é exceção. A revisão conduzida antes
desta publicação encontrou uma dúzia de defeitos de cálculo, nenhum deles acompanhado de
mensagem de erro, e a maioria descoberta não por leitura do código mas por comparação
entre dois pontos do próprio programa que deveriam concordar e não concordavam. A lição
prática é que o usuário atento constitui a melhor fonte de detecção de que um programa
científico dispõe, e é por essa razão que esta seção existe.

==Um relato bem feito é aquele que permite reproduzir o problema sem a sua presença.==
Tudo o que se pede abaixo serve a esse único objetivo.

---

## O que enviar

Um relato útil tem quatro componentes, e a ausência de qualquer um deles costuma
transformar a investigação numa troca de mensagens que consome mais tempo de todos do
que o próprio conserto.

**O arquivo do projeto.** É o item mais importante, e sozinho substitui páginas de
descrição. O `.netuno` é autocontido: traz todos os parâmetros e a série de chuva inteira
dentro dele, de modo que quem o receber reproduz exatamente a sua simulação, na mesma
máquina ou em outra qualquer. Sem ele, a investigação começa por tentar adivinhar as
entradas, e adivinhar entradas é a forma mais eficiente de não encontrar um defeito.

**O que você esperava e o que obteve.** Esta é a parte que só você pode fornecer.
Descreva o número que apareceu e o número que deveria ter aparecido, com a justificativa
do segundo — seja ela uma conta feita à mão, um resultado de versão anterior, um valor
da literatura ou simplesmente a ordem de grandeza que a experiência sugere. Um relato
que diz apenas «o resultado está errado» transfere ao destinatário a tarefa de descobrir
qual dos quarenta números da tela é o errado.

**A versão do programa.** Aparece na barra lateral, no rodapé e no menu **Sobre o
Netuno**, e já está gravada dentro do arquivo de projeto e de qualquer relatório
exportado. Informe-a mesmo assim, porque é o primeiro filtro da investigação: metade dos
problemas relatados em programas científicos são defeitos já corrigidos numa versão
posterior à que o usuário tem instalada.

**A mensagem de erro, se houver.** Copie o texto integral, e não um resumo. A seção
{{n:37}} lista as mensagens que o programa emite deliberadamente, com o significado e a
providência de cada uma; se a sua mensagem estiver lá, o problema provavelmente é de
entrada e tem solução imediata.

---

## O que conferir antes de relatar

Uma parte considerável dos resultados que parecem errados são resultados corretos de
entradas erradas, e a conferência abaixo leva poucos minutos. Ela não existe para
desencorajar o relato, e sim para que o seu tempo e o de quem investiga sejam gastos com
o que de fato é defeito.

Comece pela seção {{n:33}}, que reúne os dez enganos de projeto que o programa não tem
como impedir. Três deles respondem pela maioria dos resultados inesperados: a área de
captação informada como área inclinada do telhado em vez da projeção horizontal, a
lâmina de descarte informada em litros em vez de milímetros, e o regime tarifário do
município tratado como consumo mínimo quando é taxa de disponibilidade — ou o inverso.

Confira em seguida se o comportamento observado não é uma limitação declarada. A seção
{{n:36}} relaciona o que o programa reconhecidamente não faz, e algumas dessas limitações
produzem exatamente a impressão de defeito. O caso mais frequente envolve a categoria
tarifária: o catálogo cobre a categoria residencial dos 652 municípios e as demais só
onde a tabela oficial do prestador foi transcrita, de modo que, nos outros municípios, um
estudo de escola ou de comércio sai com a tarifa residencial enquanto o usuário não
lançar a da categoria correta. O programa avisa disso em vez de corrigir por conta
própria, porque a tabela certa é pública e específica de cada concessionária.

---

## Para onde enviar

O Netuno é desenvolvido pelo Grupo de Pesquisa em Ambientes Sustentáveis, no
Departamento de Engenharia Civil da Universidade Federal de Santa Catarina. O contato
do grupo é o canal de relato, e vale tanto para defeitos quanto para sugestões de
funcionalidade e para pedidos de esclarecimento sobre o método.

Relatos que vêm acompanhados do arquivo de projeto entram diretamente na suíte de
verificação descrita na seção {{n:34}}: um caso que reproduz um defeito vira um teste, e
o teste passa a impedir que aquele defeito volte. É a razão pela qual o arquivo importa
tanto, e é também a resposta mais completa que se pode dar a quem relatou — o problema
não apenas foi corrigido, como passou a ser vigiado.

> **Aprofundamento: o que torna um defeito difícil de encontrar.** Os defeitos que
> sobrevivem por anos num programa científico têm todos a mesma assinatura: produzem
> números plausíveis. Um erro que gera um valor negativo, ou mil vezes maior que o
> esperado, é encontrado na primeira execução. Já um fator de rendimento aplicado duas
> vezes, ou uma unidade convertida uma vez a mais que o necessário, produz um número
> que passa em qualquer inspeção visual e atravessa anos de uso. É por isso que a
> verificação do programa se apoia em invariantes — o balanço de massa que precisa
> fechar, a monotonicidade que precisa valer, o teto que a curva não pode cruzar — e não
> apenas em valores esperados. Quando você suspeitar de um número, o caminho mais rápido
> de confirmar a suspeita é procurar uma dessas identidades que ele viola.
