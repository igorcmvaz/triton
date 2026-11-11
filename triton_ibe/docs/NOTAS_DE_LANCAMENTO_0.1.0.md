# Triton IBE, Edição Ibérica: notas de lançamento da versão 0.1.0

Versão 0.1.0 (beta), lançada a 5 de novembro de 2026. É a primeira versão do Triton e a primeira da Edição Ibérica (antes Edição Portugal, PRT; os projetos e os scripts que ainda dizem `PRT` ou `POR` abrem como IBE). Este documento diz o que a versão traz, o que não traz, o que se sabe que não está perfeito e o que não foi verificado. Os dados de cada conjunto estão em [`DADOS.md`](DADOS.md); o histórico completo, em [`../CHANGELOG.md`](../CHANGELOG.md); o manual, em [`../manual/Manual-Triton.pdf`](../manual/Manual-Triton.pdf).

**Em resumo: a chuva cobre toda a Península Ibérica e as ilhas.** O Iberia01 serve Portugal continental, Espanha peninsular e as Baleares (8 319 municípios); Canárias, Madeira e Açores usam a reanálise ERA5, sempre com nível C; Ceuta e Melilla ficam sem série. As tarifas de Espanha são a média regional do INE (indicativa), com 7 municípios (12,0 % da população) de tarifa transcrita ainda não conferida; só 3 concelhos de Portugal têm tarifário transcrito.

## O que é

O Triton dimensiona sistemas de aproveitamento de água da chuva em edifícios. Simula o balanço hídrico diário sobre uma série de precipitação, varre volumes de reservatório e indica o que cada volume rende em água potável poupada, em dinheiro e em carbono do ciclo de vida; depois ordena as alternativas por decisão multicritério (TOPSIS e SMAA-VIKOR).

## Instalar

| | |
| :--- | :--- |
| Instalador para Windows | `Triton_Iberica_Setup_v0.1.0.exe`, publicado no registo do Zenodo (DOI 10.5281/zenodo.23402916), sem assinatura digital: o Windows pode mostrar o aviso do SmartScreen. O SHA-256 de cada instalador está no ficheiro `SHA256SUMS.txt` do registo (o instalador não é reprodutível bit a bit: cada compilação grava a data). Não precisa de Python. |
| A partir do código | Python 3.12 ou superior; `pip install -r requirements.txt`; `python main.py` (interface) ou `python -m triton.cli --help` (linha de comandos) |
| Espaço | A chuva embutida (quatro partes do Iberia01, ERA5 das ilhas, municípios e qualidade) soma 59,1 MiB, mais 5,66 MiB da E-OBS opcional; a edição rastreada soma cerca de 126 MiB, dos quais 42,1 MiB são o manual |

As verificações desta versão foram feitas em Windows. A licença é de código-fonte disponível para fins académicos, uso gratuito não comercial, com citação obrigatória (`LICENSE.md`, `CITATION.cff`).

## O que a Edição Ibérica traz

- **Chuva.** A precipitação diária de 8 319 municípios (Portugal continental, Espanha peninsular e Baleares), de 1971 a 2015 (16 436 dias), calculada a partir das 6 523 células de 0,1° do Iberia01 v1.0 (ODbL), em quatro partes de 13 a 15 MiB e ficheiros separados do programa; período padrão 1986–2015; chave por código INE/DTMN; pacote `iberia01-v1.0-b214eb601c3d`. Canárias, Madeira e Açores (118 locais): ERA5 de 0,25°, nível C. A E-OBS (1950–2025, só uso não comercial) é uma fonte opcional.
- **Nível de qualidade da chuva.** Cada município tem um nível A, B ou C pela representação espacial na grelha (A: 3 ou mais células; B: 1 ou 2, ou contido numa célula; C: célula emprestada ou ERA5): A 461, B 7 857 e C 119; as ilhas são todas C. Não é uma validação com pluviómetros.
- **Aviso de licença.** No primeiro arranque, o programa mostra a licença da E-OBS (só uso não comercial, em investigação e educação) e regista nos laudos o uso declarado. Por decisão do titular (25/10/2026), o uso comercial da chuva E-OBS é bloqueado e os relatórios que usam a E-OBS avisam, em vermelho e em tamanho grande, que não pode ser usada comercialmente; quem a usa assume o uso não comercial. O Iberia01 (ODbL) não tem esse bloqueio: pede só a atribuição, que o rodapé dos laudos leva.
- **Tarifários.** Água, saneamento e resíduos de Lisboa, do Porto e do Funchal, transcritos de documentos oficiais com endereço e SHA-256; a entidade gestora de cada serviço em 280 concelhos (índice da ERSAR); um estado de confiança por concelho e por serviço. Espanha: 7 municípios com tarifário transcrito, ainda não conferido (camada 1); os outros 8 124 usam a média regional do INE (2024), rotulada como indicativa (camada 3).
- **Valores e língua.** Euros; português europeu na interface, nos laudos e no manual.
- **Análise.** Balanço diário, volume ideal, economia, ACV simplificada, linha de tratamento, certificações (LEED, EDGE, GRI), decisão multicritério, modulação probabilística.
- **Saídas.** Laudos em PDF (executivo, ambiental/ESG e dossiê técnico), folha de auditoria, DXF, glTF/HTML e manifesto BIM; exemplos completos para Lisboa, Porto, Funchal, Madrid e Palma (31/10/2026: regerados com o Iberia01, normal 1986–2015, por código do município; o Funchal usa a ERA5 de ilha, nível C; Madrid mostra a tarifa de Espanha ainda não conferida e Palma a média regional do INE). Os exemplos, os 15 relatórios de exemplo e o tutorial do manual não usam a E-OBS e não levam o aviso vermelho de uso não comercial.
- **Documentação.** Manual completo (PDF, sítio offline e volumes curtos), com as secções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice E.

## O que não há

- **Tarifas de Espanha por município, quase todas.** Não existe conjunto aberto nacional. A camada 1 (tarifário transcrito de documento oficial) tem 7 municípios (Madrid, Sevilla, Murcia, A Coruña, Las Palmas, Gijón e Valladolid), ainda sem a segunda leitura humana: o programa avisa «Tarifa transcrita, ainda não conferida (segunda leitura pendente)». Onde o documento não indica o IVA, o cálculo não aplica taxa e o programa avisa «IVA do saneamento não consta da fonte». A camada 2 (herdada da entidade) está vazia; os outros 8 124 municípios usam a média regional do INE.
- **Ceuta e Melilla.** Sem série de chuva (fora do Iberia01); o programa diz porquê e pede série própria.
- **Ilhas.** A ERA5 de 0,25° subestima a chuva (de 8% a 47% nas estações testadas): use a série da estação para um projeto real. A ERA5-Land de 0,1° não estava acessível.
- **Tarifários dos restantes concelhos.** Só três estão transcritos. Nenhum concelho está em verde: não existe verificação independente registada (42 amarelos e 238 cinzentos na água e no saneamento).
- **Preços.** O programa não calcula preços de Portugal. Custos de obra, eletrobomba, tratamento e manutenção, a tarifa de eletricidade e o preço do cloro partem de zero; os resultados económicos dos exemplos não são resultados. O manual (secção 10) diz como introduzir os seus valores.
- **Fator de emissão da rede elétrica.** Sem valor (zero até o utilizador o indicar).
- **Correção de escala da chuva** calibrada com o Iberia01: não faz parte desta versão.

## Limitações conhecidas

- A licença da E-OBS é omissa quanto à redistribuição da base derivada e nenhum pedido foi feito ao KNMI. Decisão do titular (25/10/2026): bloquear o uso comercial e avisar nos relatórios; o titular não responde por uso comercial. A tabela de qualidade (derivada do Iberia01, ODbL) está num ficheiro separado sob a ODbL, com atribuição (`data/qualidade_eobs_odbl.db`).
- O aviso de licença só existe em português europeu, e o texto ainda precisa de revisão.
- O diálogo do CAPEX não tem campo para o preço da cisterna e repõe-no a zero ao confirmar; a secção 10 do manual dá o contorno.
- A E-OBS dá, em média, 13% menos chuva que o Iberia01 (8% em Portugal): os totais e as sobras das versões que usavam a E-OBS não se comparam com os de agora. Nos exemplos, a mudança medida na chuva anual é +3,7% em Lisboa (719 mm da E-OBS 1991–2020 contra 746 mm do Iberia01 1986–2015; no mesmo período de 1986–2015 a diferença é de 0,4%) e −0,1% no Porto (1 199 mm contra 1 197 mm; no mesmo período, 2,4%); o Funchal não tem E-OBS (a série de exemplo, ERA5 1991–2020, dava 538 mm e a ERA5 de ilha 1986–2015 dá 531 mm). Os números do tutorial do manual foram refeitos com o Iberia01. O Iberia01 vai só até 2015 e não tem a normal 1991–2020.
- Em espanhol e em chinês, a interface está traduzida em parte (as traduções do nível de qualidade não foram revistas por um falante nativo) e os laudos saem com trechos em português.
- Em inglês, alguns textos do catálogo da linha de tratamento e a proveniência do tarifário aparecem em português.
- Tarifários: o IVA do Funchal não está confirmado; a disponibilidade de água do Porto foi lida por inferência do layout; Beja, Évora, Ponta Delgada e Bragança têm vigência de mais de 12 meses. A tarifa de eletricidade do Funchal (0,1673 €/kWh) vem de uma fonte secundária.
- Os termos de reutilização dos sítios das entidades gestoras não foram verificados (no do Porto não se encontrou nenhum).
- A EN 16941-1 (edição em vigor e transposição portuguesa) e a ETA 0701 da ANQIP (revisão em vigor) ficam no manual como «não verificado nesta versão».

## Dados e licenças numa linha

E-OBS: só uso não comercial em investigação e educação (citar Cornes et al., 2018). CAOP 2025: cc-by. Iberia01: ODbL (fonte primária da chuva; os dados derivados vão em ficheiros separados do programa, com atribuição). Limites de Espanha: Eurostat/GISCO LAU 2023. INE: média regional das tarifas, com citação. Tarifas dos 7 municípios de Espanha: documentos oficiais de cada operador, citados com URL e SHA-256 (não redistribuídos). ERA5 via Open-Meteo: CC BY 4.0. ERSAR: avisos legais, citar a fonte, sem licença aberta. Os documentos dos tarifários não se redistribuem. Detalhe em [`DADOS.md`](DADOS.md).

## O que foi verificado e o que não foi

Verificado: os exemplos de Lisboa, Porto, Funchal, Madrid e Palma abrem, percorrem as 13 etapas, recalculam a economia e a decisão, geram os três laudos e a folha de auditoria, gravam o `.triton` e reabrem-no com o mesmo resultado; a linha de comandos funciona; os quatro idiomas abrem sem erro; o nível de qualidade da chuva e o aviso da licença da E-OBS aparecem na etapa 1 e nos laudos.

Verificado em 25/10/2026, no instalador e no programa congelado desta compilação: o instalador (nome definitivo) foi executado em modo silencioso numa pasta temporária, instalou, o programa instalado correu `--diagnostico` e `cli validate`/`cli run` com resultados numéricos iguais aos do código-fonte, e desinstalou-se sem deixar a pasta. O congelado correu também com o PATH reduzido, fora do repositório. SHA-256 dos ficheiros testados: instalador `0add5c5993db7f2d97d2aa6a5267647f6dbcdfde62f5a4c7f91ca0b74d6ecace`; programa `34b7fdba2bd6c6dc38ebd77a6221c4dd0ebac23c549b5a391e74f89fd9564152`. Os instaladores **não são reprodutíveis bit a bit** (cada compilação grava a data e a revisão): o hash vale para estes ficheiros, e o instalador a publicar tem de ser medido de novo.

Não verificado: a janela com ecrã real (a verificação foi em modo sem ecrã); a janela abriu e parou no diálogo da licença da E-OBS, sem chegar à janela principal, a volumetria 3D em WebGL, a impressão dos PDFs, uma máquina limpa real (máquina virtual sem Python), o Windows Defender/SmartScreen, a assinatura de código, a instalação para todos os utilizadores, a associação dos ficheiros `.triton` e os atalhos do menu Iniciar.

## Comunicar um problema

Indique a versão (0.1.0), a edição, os passos e anexe o ficheiro `.triton`. Contacto: igor.catao@posgrad.ufsc.br.

## Como citar

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações.* Universidade Federal de Santa Catarina (UFSC). Para a chuva, cite também a fonte usada: Herrera et al. (2019), doi:10.5194/essd-11-1947-2019, com a atribuição ODbL do Iberia01; Hersbach et al. (2020), doi:10.1002/qj.3803, para a ERA5 das ilhas; ou Cornes et al. (2018), doi:10.1029/2017JD028200, com o reconhecimento exigido pela E-OBS (`DADOS.md`, secção 7).
