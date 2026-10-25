# Triton, Edição Brasil (BRL): notas de lançamento da versão 0.1.0

Versão 0.1.0 (beta), data de lançamento a definir. É a primeira versão do Triton e a primeira da Edição Brasil. Este documento diz o que a versão traz, o que ela não traz, o que se sabe que não está perfeito e o que não foi verificado. Os dados de cada conjunto estão em [`DADOS.md`](DADOS.md); o histórico completo, em [`../CHANGELOG.md`](../CHANGELOG.md); o manual, em [`../manual/Manual-Triton.pdf`](../manual/Manual-Triton.pdf).

## O que é

O Triton dimensiona sistemas de aproveitamento de água da chuva em edificações. Simula o balanço hídrico diário sobre uma série de precipitação, varre volumes de reservatório e indica o que cada volume rende em água potável poupada, em dinheiro e em carbono do ciclo de vida; depois ordena as alternativas por decisão multicritério (TOPSIS e SMAA-VIKOR). Parte do motor do Netuno 5.0.1, com nome, versão e repositório próprios.

## Instalar

| | |
| :--- | :--- |
| Instalador para Windows | `Triton_Setup_0_1_0.exe`, ainda não publicado (e sem assinatura digital); o repositório é privado nesta fase e o DOI do Zenodo ainda não foi criado. Compilação local de 25/10/2026: 859.3 MiB, SHA-256 `9f04b541aec0f6efcb83fd2adfdfe126a5e3e26bf511d9779f58a98f4b22e89a`. O hash do instalador publicado, como o endereço do registro no Zenodo, será indicado na publicação do release (o instalador não é reprodutível bit a bit: cada compilação grava a data). Não precisa de Python. Até lá, execute a partir do código. |
| A partir do código | Python 3.12 ou superior; `pip install -r requirements.txt`; `python main.py` (interface) ou `python -m triton.cli --help` (linha de comando) |
| Espaço | A base climática embutida tem 785,1 MiB (19 arquivos); o repositório rastreado soma cerca de 872 MiB nesta pasta |

As verificações desta versão foram feitas em Windows. A licença é de código-fonte disponível para fins acadêmicos, uso gratuito não comercial, com citação obrigatória (`LICENSE.md`, `CITATION.cff`).

## O que a Edição Brasil traz

- **Chuva.** A base CLIMBra para 652 municípios, 19 modelos do CMIP6 e três simulações (histórica, SSP2-4.5 e SSP5-8.5): 37.164 séries diárias, em 19 bancos de 39,98 a 43,02 MiB, cada um abaixo do limite de 50 MiB, com o SHA-256 de cada parte. Licença CC0 1.0.
- **Tarifas.** Água e esgoto de 652 municípios, por prestador, com 617 conferências de conta (241 corrigidas); energia B1 da ANEEL por distribuidora. Grau de confiança por município: 584 de grau A, 63 de B e 5 de C.
- **Custos.** CAPEX e OPEX calculados automaticamente de um catálogo de referência em reais, com o digitado pelo usuário prevalecendo (manual, seção 10).
- **Análise.** Balanço diário, volume ideal, economia (VPL, TIR, payback), ACV simplificada, linha de tratamento, enquadramento em certificações (LEED, EDGE, GRI, AQUA-HQE, Selo Casa Azul), decisão multicritério, modulação probabilística.
- **Saídas.** Laudos em PDF (executivo, ambiental/ESG e dossiê técnico), planilha de auditoria, DXF, glTF/HTML e manifesto BIM.
- **Idiomas.** Interface e laudos completos em português e em inglês; espanhol e chinês parciais (ver abaixo).
- **Documentação.** Manual completo em português do Brasil (PDF, site offline e volumes curtos), com as seções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice E.

## O que não há

- **Chuva medida.** As séries da base e as dos exemplos vêm do CLIMBra: são modeladas, com correção de viés, e não registros de pluviômetro. Para um projeto real, use a série medida no local.
- **Energia com tributos e bandeiras.** A tarifa de energia é a B1 sem ICMS, PIS/Pasep, Cofins, COSIP nem bandeira.
- **Preços de referência com fonte para todos os itens.** Só os preços de reservatório têm fonte e data registradas; o resto do catálogo de CAPEX é uma referência sem procedência completa, e o fator regional existe mas não altera o investimento do projeto (manual, seção 10).

## Limitações conhecidas

- 140 municípios têm a referência de energia expirada (a distribuidora não tem ato vigente na base aberta); guardam o último valor oficial, marcado como tal.
- Os 5 municípios do Tocantins estão em grau C: a estrutura tarifária ficou «a conferir». O Amazonas e o Rio de Janeiro concentram os de grau B.
- O custo anual do resumo da análise não soma as rotinas de manutenção, que entram no fluxo de caixa à parte e podem mudar o resultado (manual, seção 10).
- Em espanhol e chinês, a interface está traduzida em parte e os laudos saem com trechos em português.
- Em janelas estreitas (cerca de 1.500 px), alguns cabeçalhos de tabela aparecem cortados.
- O metadado `source_article` dentro das 19 partes do CLIMBra ainda diz «art. 48»; o artigo é Scientific Data 10, art. 47 (Crossref, 24/10/2026). O programa e a documentação já dizem 47.
- O catálogo `tarifas/catalogo_tarifas_auditado_652.csv` traz só o cabeçalho; a versão completa é o `.xlsx`. O `PANORAMA_TARIFAS_E_CONFIABILIDADE.md` é a fotografia de 24/08/2026 e difere do banco de 05/10/2026 em alguns números (explicado em `DADOS.md`).

## Dados e licenças em uma linha

CLIMBra: CC0 1.0. Tarifas: valores públicos transcritos, com a fonte de cada um; os documentos dos prestadores não se redistribuem. Base aberta da ANEEL: ODbL; o titular aprovou, em 25/10/2026, o uso do JSON extraído, com a atribuição à ANEEL. Fator de emissão do MCTI/SIRENE: o site declara CC BY-ND 3.0; uso do JSON extraído aprovado pelo titular na mesma data, com atribuição. Resultados do Netuno 4 e logotipo do CLIMBra: mantidos, com «autorização dos criadores, registrada pelo titular em 25/10/2026» (sem documento anexo). Detalhes em [`DADOS.md`](DADOS.md), seção 9.

## O que foi verificado e o que não foi

Verificado: os projetos de exemplo da edição abrem, percorrem as 13 etapas, recalculam a economia e a decisão, geram os três laudos e a planilha de auditoria, gravam o `.triton` e o reabrem com o mesmo resultado; a linha de comando (`validate`, `run`, `analyze`, `init`, `matrix`) funciona; os quatro idiomas abrem sem erro; os números impressos no manual são conferidos por testes automáticos contra o programa.

Verificado em 25/10/2026, no instalador e no programa congelado desta compilação: o instalador (nome definitivo) foi executado em modo silencioso numa pasta temporária, instalou, o programa instalado correu `--diagnostico` e `cli validate`/`cli run` com resultados numéricos iguais aos do código-fonte, e desinstalou-se sem deixar a pasta. O congelado correu também com o PATH reduzido, fora do repositório. SHA-256 dos arquivos testados: instalador `9f04b541aec0f6efcb83fd2adfdfe126a5e3e26bf511d9779f58a98f4b22e89a`; programa `6a66e7a34f8ccecb7ece94801831685512df780a39803be7b9bb17e756c1f35f`. Os instaladores **não são reprodutíveis bit a bit** (cada compilação grava a data e a revisão): o hash vale para estes arquivos, e o instalador a publicar tem de ser medido de novo.

Não verificado: a janela com tela real (a verificação foi em modo sem tela); a janela do programa BRL instalado não chegou a ser aberta, a volumetria 3D em WebGL, a impressão dos PDFs, uma máquina limpa real (máquina virtual sem Python), o Windows Defender/SmartScreen, a assinatura de código, a instalação para todos os utilizadores, a associação dos arquivos `.triton` e os atalhos do menu Iniciar.

## Relatar um problema

Descreva a versão (0.1.0), a edição, os passos e anexe o arquivo `.triton`. Contato: igor.catao@posgrad.ufsc.br. O manual, na seção «Relatar um problema», diz o que anexar.

## Como citar

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações.* Universidade Federal de Santa Catarina (UFSC). Para a base climática, cite também Ballarin et al. (2023), *Scientific Data* 10, 47, doi:10.1038/s41597-023-01956-z.
