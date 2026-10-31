# O que há de novo em cada versão do Triton

Este ficheiro é **gerado** do capítulo de histórico do manual do utilizador
(`manual/partes/38_historico_de_versoes.md`) por `manual/gerar_changelog.py`.
Não o edite à mão: escreva no manual, regere, e os dois ficam iguais.

Cada versão traz as mesmas secções: o resumo em uma frase, as novidades, **as
correções que alteram resultados de estudos já feitos**, as que não alteram e o
que mudou na documentação. A distinção entre os dois tipos de correção é a que
mais importa para quem publica com o programa: uma correção de cálculo obriga a
declarar a versão usada num trabalho; uma correção de interface, não.

A versão atual é a 0.1.0. O manual completo está em `manual/Manual-Triton.pdf`
e o site de documentação, em `manual/site/index.html`.

---

## Versão 0.1.0 (beta) — 24 de outubro de 2026

> **Numa frase.** Primeira versão beta do Triton, com nome próprio para cada edição, no mesmo repositório e com a mesma numeração.

### Novidades

O Triton simula o aproveitamento de águas pluviais dia a dia e inclui o motor de simulação, a
avaliação de ciclo de vida, a linha de tratamento, a decisão multicritério e a modulação
probabilística. Esta é a primeira versão da Edição Ibérica (IBE, antes Edição Portugal), que tem nome e logótipo próprios e partilha o repositório e a numeração das outras edições, com a chuva do Iberia01 por município (e a E-OBS por concelho como opção), os tarifários de Lisboa, do Porto e do Funchal
e os valores em euros. A regra de operação de Fewkes (φ) está disponível como opção em todos os
módulos.

**O que a Edição Ibérica traz nesta versão.**

- **Chuva.** A precipitação diária de 278 concelhos de Portugal continental, de 1950 a 2025, calculada a partir da grelha E-OBS v33.0e, numa base de 5,74 MiB identificada por `PT-EOBS-v33.0e-37fcba20` e por SHA-256. Cada concelho tem um nível de qualidade, A, B ou C: 45 de nível A, 159 de B e 74 de C.
- **Licença da chuva (E-OBS, opcional).** No primeiro arranque, o aviso da licença da E-OBS (só uso não comercial, em investigação e educação) e a declaração do uso pretendido, que fica registada nos laudos. Por decisão do titular (25/10/2026), o uso comercial da chuva E-OBS é bloqueado e os relatórios avisam, em vermelho e em tamanho grande, que não pode ser usada comercialmente.
- **Tarifários.** Água, saneamento e resíduos de Lisboa, do Porto e do Funchal, transcritos de documentos oficiais com endereço e SHA-256 registados; a entidade gestora de cada serviço em 280 concelhos, a partir da ERSAR; e um estado de confiança por concelho e por serviço.
- **Valores e língua.** Euros, IVA tratado em cada tarifário, português europeu na interface, nos laudos e no manual.
- **Chuva de toda a Península (30/10/2026).** O Iberia01 passa a ser a fonte por defeito da Edição Ibérica: Portugal (308 locais), Espanha (8 131 municípios, incluindo as Baleares) e, com a ERA5 em nível C, Canárias, Madeira e Açores; chave por código INE/DTMN, busca por nome e código na Etapa 1, `--local` na linha de comandos e `clima.iberia` nos estudos em lote. A E-OBS fica opcional. Os exemplos (Lisboa, Porto e Funchal; novos Madrid e Palma), os relatórios de exemplo e o tutorial deste manual foram regerados com o Iberia01 (normal 1986–2015) em 31/10/2026, e já não levam o aviso vermelho da E-OBS; o Funchal usa a ERA5 de ilha (nível C). A tabela de qualidade passa para um ficheiro separado sob ODbL. Tarifas de Espanha: média regional do INE (indicativa).
- **Estudos em lote por JSON.** O subcomando `triton estudo` organiza um estudo num `estudo.json` (projeto base, casos por tipologia, substituições de parâmetros por apelidos, análise e saídas), roda todos os casos em ordem estável, com retomada e execução paralela, e grava tabelas para artigos: CSV tidy, JSON com proveniência (versão, edição, SHA-256, fonte e licença da chuva), Markdown, LaTeX (booktabs) e XLSX. Um modelo de texto com marcadores recebe os números reais e deixa «XX» onde faltar resultado. Há um estudo de exemplo em `examples/estudos/`.
- **Documentação.** O manual completo, o sítio de documentação, volumes curtos e `docs/DADOS.md`, que descreve cada conjunto de dados com fonte, licença e qualidade.

**O que a versão ainda não tem.**

- **Espanha.** As tarifas são a média regional do INE (indicativa) e, em sete municípios, uma tarifa transcrita ainda não conferida (segunda leitura pendente); o exemplo de Madrid mostra a tarifa do Canal de Isabel II com esse aviso.
- **Ilhas.** Canárias, Madeira e Açores usam a reanálise ERA5 de 0,25°, sempre em nível C e com aviso; Ceuta e Melilla não têm série.
- **Tarifários nos restantes concelhos.** Só três estão transcritos; nenhum concelho está em verde, porque falta a verificação independente (42 amarelos e 238 cinzentos na água e no saneamento).
- **Preços e CAPEX.** O programa não calcula preços de Portugal: reservatórios, tubagem, eletrobombas, mão de obra e manutenção partem de zero, e a tarifa de eletricidade e o preço do cloro também. Os resultados económicos dos exemplos não são resultados.
- **Fator de emissão da rede.** Sem valor: é zero até o utilizador indicar o da rede do projeto.
- **Correção de escala da chuva.** A correção calibrada com o Iberia01 não faz parte desta versão.

**Limitações conhecidas.**

- A licença da E-OBS é omissa quanto à redistribuição da base derivada; por decisão do titular (25/10/2026) o uso comercial é bloqueado e avisado, e quem usa a chuva E-OBS assume o uso não comercial. A tabela de qualidade, derivada do Iberia01 (ODbL), vai para um ficheiro separado sob a ODbL, com atribuição. O aviso da licença só existe em português europeu, e o texto ainda precisa de revisão.
- O diálogo do CAPEX não tem campo para o preço da cisterna e repõe-no a zero ao confirmar; a secção 4.7 dá o contorno.
- Em espanhol e em chinês, a interface está traduzida em parte (as traduções do nível de qualidade da chuva não foram revistas por um falante nativo) e os laudos saem com trechos em português; o português e o inglês estão completos.
- Em inglês, alguns textos do catálogo da linha de tratamento e a proveniência do tarifário aparecem em português.
- Os termos de reutilização dos sítios das entidades gestoras não foram verificados (no do Porto não se encontrou nenhum).
- Referências a rever antes de citar: a edição da EN 16941-1 em vigor e a sua transposição, a revisão da ETA 0701 da ANQIP (as secções 1.1 e 4.6 marcam o que falta).

### Correções que alteram resultados

Nenhuma: esta é a primeira versão beta, e não há versão anterior a corrigir.

| O que foi corrigido | Efeito no resultado |
| :--- | :--- |

### Correções que não alteram resultados

Nenhuma.

### Documentação

O manual ganhou as secções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice E.

---
