# Como relatar um problema

Os programas de simulação têm defeitos, e o Triton não é exceção. A revisão conduzida antes desta
versão beta encontrou uma dúzia de defeitos de cálculo, nenhum acompanhado de mensagem de erro, e a
maioria descoberta não pela leitura do código mas pela comparação entre dois pontos do próprio
programa que deviam concordar e não concordavam. A lição prática é que o utilizador atento é a
melhor fonte de deteção de que um programa científico dispõe, e é por essa razão que esta secção
existe.

==Um bom relato é aquele que permite reproduzir o problema sem a sua presença.== Tudo o que se pede
abaixo serve esse único objetivo.

---

## O que enviar

Um relato útil tem quatro componentes, e a ausência de qualquer um deles costuma transformar a
investigação numa troca de mensagens que consome mais tempo a todos do que a própria correção.

**O ficheiro do projeto.** É o item mais importante, e por si só substitui páginas de descrição. O
`.triton` é autocontido: traz todos os parâmetros e a série de chuva inteira dentro dele — ou,
com a chuva E-OBS por concelho, a referência exata da série e a sua impressão digital, que o
programa recompõe a partir da base —, de modo que quem o receber reproduz exatamente a sua
simulação, no mesmo computador ou noutro qualquer. Sem ele, a investigação começa por tentar
adivinhar as entradas, e adivinhar entradas é a maneira mais eficiente de não encontrar um defeito.

**O que esperava e o que obteve.** Esta é a parte que só o utilizador pode fornecer. Descreva o
número que apareceu e o número que devia ter aparecido, com a justificação do segundo — seja um
cálculo à mão, um resultado de uma versão anterior, um valor da literatura ou simplesmente a ordem
de grandeza que a experiência sugere. Um relato que diz apenas «o resultado está errado» deixa ao
destinatário a tarefa de descobrir qual dos quarenta números do ecrã é o errado.

**A versão do programa.** Aparece na barra lateral, no rodapé e no menu **Sobre o Triton**, e já
está gravada dentro do ficheiro de projeto e de qualquer relatório exportado. Indique-a mesmo
assim, porque é o primeiro filtro da investigação: metade dos problemas relatados em programas
científicos são defeitos já corrigidos numa versão posterior à que o utilizador tem instalada.
Indique também a edição.

**A mensagem de erro, se a houver.** Copie o texto integral, e não um resumo. A secção {{n:37}}
lista as mensagens que o programa emite deliberadamente, com o significado e a providência de cada
uma; se a sua mensagem lá estiver, o problema é provavelmente de entrada e tem solução imediata.

---

## O que conferir antes de relatar

Uma parte considerável dos resultados que parecem errados são resultados corretos de entradas
erradas, e a conferência abaixo leva poucos minutos. Não existe para desencorajar o relato, mas
para que o seu tempo e o de quem investiga sejam gastos no que é, de facto, um defeito.

Comece pela secção {{n:33}}, que reúne os dez enganos de projeto que o programa não tem como
impedir. Três deles respondem pela maioria dos resultados inesperados: a área de captação
introduzida como a área inclinada da cobertura em vez da projeção horizontal, a lâmina de descarte
introduzida em litros em vez de milímetros, e a estrutura do tarifário tratada como um preço único
por metro cúbico quando tem parte fixa e escalões.

Confira em seguida se o comportamento observado não é uma limitação declarada. A secção {{n:36}}
relaciona o que o programa reconhecidamente não faz, e algumas dessas limitações dão exatamente a
impressão de defeito. O caso mais frequente envolve a categoria tarifária: os tarifários que a
edição traz transcritos são os de utilizador doméstico de Lisboa, do Porto e do Funchal, pelo que
um estudo de escola ou de comércio sai com a tarifa doméstica enquanto o utilizador não introduzir
a da categoria correta. O programa avisa disso em vez de corrigir por conta própria, porque a
tabela certa é pública e específica de cada entidade gestora.

---

## Para onde enviar

O Triton é desenvolvido por um grupo de investigação universitário. O contacto indicado no menu do
programa e no repositório é o canal de relato, e serve tanto para defeitos como para sugestões de
funcionalidades e pedidos de esclarecimento sobre o método. Os relatos podem ser escritos em
português ou em inglês.

Os relatos que vêm acompanhados do ficheiro de projeto entram diretamente na suíte de verificação
descrita na secção {{n:34}}: um caso que reproduz um defeito transforma-se num teste, e o teste
passa a impedir que o defeito volte. É a razão pela qual o ficheiro importa tanto, e é também a
resposta mais completa que se pode dar a quem relatou — o problema não só foi corrigido, como
passou a ser vigiado.

> **Aprofundamento: o que torna um defeito difícil de encontrar.** Os defeitos que sobrevivem anos
> num programa científico têm todos a mesma assinatura: produzem números plausíveis. Um erro que
> gera um valor negativo, ou mil vezes maior do que o esperado, encontra-se à primeira execução. Já
> um fator de rendimento aplicado duas vezes, ou uma unidade convertida uma vez a mais do que o
> necessário, produz um número que passa em qualquer inspeção visual e atravessa anos de uso. É por
> isso que a verificação do programa se apoia em invariantes — o balanço de massa que tem de
> fechar, a monotonia que tem de valer, o teto que a curva não pode cruzar — e não apenas em
> valores esperados. Quando suspeitar de um número, a maneira mais rápida de confirmar a suspeita é
> procurar uma dessas identidades que ele viola.
