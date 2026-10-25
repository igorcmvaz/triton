# Triton IBE, Edição Ibérica: notas de lançamento da versão 0.1.0

Versão 0.1.0 (beta), 24 de outubro de 2026. É a primeira versão do Triton e a primeira da Edição Ibérica (antes Edição Portugal, PRT; os projetos e os scripts que ainda dizem `PRT` ou `POR` abrem como IBE). Este documento diz o que a versão traz, o que não traz, o que se sabe que não está perfeito e o que não foi verificado. Os dados de cada conjunto estão em [`DADOS.md`](DADOS.md); o histórico completo, em [`../CHANGELOG.md`](../CHANGELOG.md); o manual, em [`../manual/Manual-Triton.pdf`](../manual/Manual-Triton.pdf).

**Em resumo: esta versão só tem dados de Portugal.** A edição chama-se Ibérica porque foi desenhada para a Península Ibérica, mas a Espanha tem 0 locais no programa.

## O que é

O Triton dimensiona sistemas de aproveitamento de água da chuva em edifícios. Simula o balanço hídrico diário sobre uma série de precipitação, varre volumes de reservatório e indica o que cada volume rende em água potável poupada, em dinheiro e em carbono do ciclo de vida; depois ordena as alternativas por decisão multicritério (TOPSIS e SMAA-VIKOR).

## Instalar

| | |
| :--- | :--- |
| Instalador para Windows | `Triton_IBE_Setup_0_1_0.exe`, ainda não publicado (e sem assinatura digital). Compilação local de 25/10/2026: 278.2 MiB, SHA-256 `0add5c5993db7f2d97d2aa6a5267647f6dbcdfde62f5a4c7f91ca0b74d6ecace`. O hash do instalador publicado, como o endereço do registo no Zenodo, será indicado na publicação do release (o instalador não é reprodutível bit a bit: cada compilação grava a data). Não precisa de Python. Até lá, execute a partir do código. |
| A partir do código | Python 3.12 ou superior; `pip install -r requirements.txt`; `python main.py` (interface) ou `python -m triton.cli --help` (linha de comandos) |
| Espaço | A base de chuva embutida tem 5,74 MiB; a edição rastreada soma cerca de 62 MiB, dos quais 41,6 MiB são o manual |

As verificações desta versão foram feitas em Windows. A licença é de código-fonte disponível para fins académicos, uso gratuito não comercial, com citação obrigatória (`LICENSE.md`, `CITATION.cff`).

## O que a Edição Ibérica traz

- **Chuva.** A precipitação diária de 278 concelhos de Portugal continental, de 1950 a 2025 (27 759 dias), calculada a partir da grelha E-OBS v33.0e (0,1°, cerca de 10 km) e dos limites da CAOP 2025; pacote `PT-EOBS-v33.0e-37fcba20`, com SHA-256.
- **Nível de qualidade da chuva.** Cada concelho tem um nível A, B ou C, pela diferença para o Iberia01 em 1971–2000 e pela geometria da série: 45 de nível A, 159 de B e 74 de C. Os C concentram-se no Algarve (15 dos 16 concelhos).
- **Aviso de licença.** No primeiro arranque, o programa mostra a licença da E-OBS (só uso não comercial, em investigação e educação) e regista nos laudos o uso declarado.
- **Tarifários.** Água, saneamento e resíduos de Lisboa, do Porto e do Funchal, transcritos de documentos oficiais com endereço e SHA-256; a entidade gestora de cada serviço em 280 concelhos (índice da ERSAR); um estado de confiança por concelho e por serviço.
- **Valores e língua.** Euros; português europeu na interface, nos laudos e no manual.
- **Análise.** Balanço diário, volume ideal, economia, ACV simplificada, linha de tratamento, certificações (LEED, EDGE, GRI), decisão multicritério, modulação probabilística.
- **Saídas.** Laudos em PDF (executivo, ambiental/ESG e dossiê técnico), folha de auditoria, DXF, glTF/HTML e manifesto BIM; exemplos completos para Lisboa, Porto e Funchal.
- **Documentação.** Manual completo (PDF, sítio offline e volumes curtos), com as secções «Particularidades de região e país» e «Descrição dos dados e sua qualidade» no apêndice E.

## O que não há

- **Espanha.** Nenhum local. Há um ensaio, feito fora do programa, com as 52 capitais de província (39 em nível B, 9 em C, 4 sem série). Falta o limite municipal (CNIG) e a decisão sobre a licença da E-OBS para redistribuição.
- **Ilhas.** Os 30 concelhos da Madeira (11) e dos Açores (19) não têm série na base. O exemplo do Funchal usa uma reanálise ERA5 (10 958 dias, 1991–2020), sem nível de qualidade.
- **Tarifários dos restantes concelhos.** Só três estão transcritos. Nenhum concelho está em verde: não existe verificação independente registada (42 amarelos e 238 cinzentos na água e no saneamento).
- **Preços.** O programa não calcula preços de Portugal. Custos de obra, eletrobomba, tratamento e manutenção, a tarifa de eletricidade e o preço do cloro partem de zero; os resultados económicos dos exemplos não são resultados. O manual (secção 10) diz como introduzir os seus valores.
- **Fator de emissão da rede elétrica.** Sem valor (zero até o utilizador o indicar).
- **Correção de escala da chuva** calibrada com o Iberia01: não faz parte desta versão.

## Limitações conhecidas

- A licença da E-OBS é omissa quanto à redistribuição da base derivada; a decisão é da UFSC e nenhum pedido foi feito ao KNMI. A tabela `qualidade` guarda diferenças derivadas do Iberia01 (ODbL), e não está decidido se isso exige a ODbL.
- O aviso de licença só existe em português europeu, e o texto ainda precisa de revisão.
- O diálogo do CAPEX não tem campo para o preço da cisterna e repõe-no a zero ao confirmar; a secção 10 do manual dá o contorno.
- A E-OBS dá, em média, 10,1% menos chuva que o Iberia01 nos 278 concelhos (20,7% menos nos de nível C) e alisa os extremos; em C, valide com uma série local.
- Em espanhol e em chinês, a interface está traduzida em parte (as traduções do nível de qualidade não foram revistas por um falante nativo) e os laudos saem com trechos em português.
- Em inglês, alguns textos do catálogo da linha de tratamento e a proveniência do tarifário aparecem em português.
- Tarifários: o IVA do Funchal não está confirmado; a disponibilidade de água do Porto foi lida por inferência do layout; Beja, Évora, Ponta Delgada e Bragança têm vigência de mais de 12 meses. A tarifa de eletricidade do Funchal (0,1673 €/kWh) vem de uma fonte secundária.
- Os termos de reutilização dos sítios das entidades gestoras não foram verificados (no do Porto não se encontrou nenhum).
- A EN 16941-1 (edição em vigor e transposição portuguesa) e a ETA 0701 da ANQIP (revisão em vigor) estão marcadas no manual como «a completar».

## Dados e licenças numa linha

E-OBS: só uso não comercial em investigação e educação (citar Cornes et al., 2018). CAOP 2025: cc-by. Iberia01: ODbL (só referência para o nível de qualidade). ERA5 via Open-Meteo: CC BY 4.0. ERSAR: avisos legais, citar a fonte, sem licença aberta. Os documentos dos tarifários não se redistribuem. Detalhe em [`DADOS.md`](DADOS.md).

## O que foi verificado e o que não foi

Verificado: os exemplos de Lisboa, Porto e Funchal abrem, percorrem as 13 etapas, recalculam a economia e a decisão, geram os três laudos e a folha de auditoria, gravam o `.triton` e reabrem-no com o mesmo resultado; a linha de comandos funciona; os quatro idiomas abrem sem erro; o nível de qualidade da chuva e o aviso da licença da E-OBS aparecem na etapa 1 e nos laudos.

Não verificado: a janela com ecrã real (a verificação foi em modo sem ecrã), a volumetria 3D em WebGL, a regeração dos instaladores com o nome definitivo e a impressão dos PDFs.

## Comunicar um problema

Indique a versão (0.1.0), a edição, os passos e anexe o ficheiro `.triton`. Contacto: igor.catao@posgrad.ufsc.br.

## Como citar

Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações.* Universidade Federal de Santa Catarina (UFSC). Para a chuva, cite também Cornes et al. (2018), doi:10.1029/2017JD028200, e repita o reconhecimento exigido pela E-OBS (`DADOS.md`, secção 7).
