# Auditoria de convergência — Triton Desktop e Web

## Decisão arquitetural

As duas edições devem permanecer como interfaces diferentes sobre o mesmo núcleo em `triton/core`. A edição web não deve reimplementar fórmulas no React nem manter uma cópia simplificada do motor. O backend web já segue esse princípio ao chamar `triton.cli.run_analysis`, que por sua vez usa o núcleo compartilhado.

O arquivo `.triton` é o contrato de interoperabilidade entre as edições. Campos ainda não representados no schema estável devem continuar no bloco `web_config` até serem promovidos ao schema comum, sem perda silenciosa.

## Cobertura funcional atual

As duas interfaces apresentam as mesmas 11 áreas de trabalho: projeto e chuva, edificação, qualidade da água, reservatórios, resultados técnicos, economia, ambiental/ESG, otimização e cenários, relatórios, documentação e tarifas. Paridade de títulos não significa, por si só, paridade de profundidade; cada nova função deve ter teste de contrato comparando o resultado web ao resultado obtido diretamente no núcleo.

## Correções desta auditoria

- A sazonalidade mensal da web passou a respeitar os meses-calendário a partir da data inicial do projeto. O resultado informa início, fim, quantidade de observações e metodologia.
- LCOW e relação benefício/custo passaram a descontar os fluxos na periodicidade mensal usada pelo núcleo econômico. A resposta expõe a taxa mensal e a taxa anual efetiva equivalente.
- A API rejeita precipitação e pesos com `NaN` ou infinito, evitando resultados JSON inválidos e simulações não auditáveis.
- Calculadora predial, diagrama hidráulico e comparador de cenários passaram a ser carregados sob demanda no navegador.

## Critérios para levar toda a profundidade do desktop à web

Uma função pode ser promovida quando:

1. usa exclusivamente `triton/core` ou um serviço comum, sem fórmula duplicada no frontend;
2. possui teste de paridade com tolerância numérica explícita;
3. informa unidade, fonte, período, premissas e versão do motor no resultado/exportação;
4. respeita os limites públicos de série, fila, tempo, upload e sensibilidade;
5. não aumenta o pacote inicial: telas e bibliotecas pesadas devem ser carregadas sob demanda;
6. operações longas executam na fila, admitem cancelamento e expiram os artefatos;
7. um ensaio de carga no servidor-alvo confirma latência e memória aceitáveis.

## Plano de carga e capacidade

O limite funcional atual é de 40.000 dias por série, 50 tarefas na fila, 10 tarefas por IP/hora e 600 segundos por tarefa. Esses valores são guardrails, não uma medição de capacidade. Antes de liberar paridade total, executar três perfis no hardware de produção:

- leve: 365–3.650 dias, varredura até 20 alternativas;
- típico: 9.125 dias, 50–100 alternativas e análise completa;
- extremo permitido: 40.000 dias, sensibilidade e maior grade aceita.

Registrar p50/p95 de duração, pico de memória por worker, tamanho da resposta e taxa de falhas. Aumentar recursos web apenas se o custo marginal estiver dentro do orçamento; caso contrário, manter o mesmo recurso por processamento assíncrono, paginação, agregação de séries e download de resultados completos.

### Linha de base local (01/09/2026)

Ensaio técnico isolado, em processo único e sem concorrência: 3.650 dias/21 alternativas em 0,122 s; 9.125 dias/26 alternativas em 0,352 s; 40.000 dias/26 alternativas em 1,522 s. Esses números confirmam que a simulação técnica cabe confortavelmente no backend, mas não substituem p50/p95 concorrente nem cobrem análise econômica, ambiental, sensibilidade, serialização e tráfego. Instrumentação Python detalhada de memória alterou o tempo em mais de duas ordens de grandeza e, por isso, não foi usada como estimativa de produção; medir memória no container/host.

## Regra de aceite contínuo

Uma versão é publicável quando a compilação do frontend passa sem erro, os testes do núcleo e da API passam, os testes de invariantes financeiros e de conservação de massa permanecem verdes e nenhum campo é perdido no ciclo desktop → `.triton` → web → `.triton` → desktop.
