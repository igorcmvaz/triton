# Fila da base tarifária

Gerado em 2026-10-05 por `tarifas/procedencia.py`. Não edite à mão.

Fluxo: arquivo novo em `tarifas/entrada/` → `python tarifas/processar_entrada.py` (registra e move para `tarifas/fontes/<prestador>/`) → transcrição em `tarifas/transcricoes/<prestador>.json` → `python tarifas/aplicar_transcricoes.py --aplicar`. Por município vale a transcrição de vigência mais recente.

## Situação dos municípios

| Classe | Municípios |
| :--- | ---: |
| documentada, com as 4 categorias | 299 |
| residencial documentada | 161 |
| documentada, vigência com mais de 12 meses | 136 |
| auditada sem documento guardado | 8 |
| a confirmar | 48 |
| dado ruim | 0 |
| **total** | **652** |

## 1. Recebidos, a transcrever

Documentos já guardados em `tarifas/fontes/` que ainda não viraram transcrição. Em ordem de municípios que destravam.

| # | Recebido | Prestador | Arquivo | Vigência | Municípios na base |
| ---: | :--- | :--- | :--- | :--- | ---: |

### Consultados sem transcrição: o que faltou

| # | Prestador | Arquivo | Por que não virou transcrição |
| ---: | :--- | :--- | :--- |
| 16 | CAER | CAER _ Serviços.html | consultado: a CAER publica uma fórmula polinomial (Res. 04/2008) com tarifas mínimas de 01/09/2011; falta a tabela vigente |
| 25 | ARES-PCJ | 1790877131-tarifas_categoria_comercial_01_09_2026.pdf | consultado: quadro da ARES-PCJ só com a conta mínima comercial por município; não traz faixas |
| 26 | ARES-PCJ | 1790877131-tarifas_categoria_industrial_01_09_2026.pdf | consultado: quadro da ARES-PCJ só com a conta mínima industrial por município; não traz faixas |
| 27 | ARES-PCJ | 1790877131-tarifas_categoria_residencial_social_01_09_2026.pdf | consultado: quadro da ARES-PCJ só com a conta mínima residencial social por município; não traz faixas |
| 36 | Águas do Rio | Legislação e Tarifas_AguasdoRio.html | consultado: a página traz Regiões 1 e 4, Áreas A e B e Tarifas 1 e 2, mas não diz quais municípios estão em cada região e área nem quando vale a Tarifa 1; falta a deliberação da AGENERSA com a lista |
| 49 | DAESC Coruripe | Diario_07082025.pdf | consultado: o Diário de Coruripe de 07/08/2025 traz só a portaria de preços de serviços do DAESC, sem as tarifas de água |
| 53 | Águas do Rio | Legislação e Tarifas.html | consultado: a página traz Regiões 1 e 4, Áreas A e B e Tarifas 1 e 2, mas não diz quais municípios estão em cada região e área nem quando vale a Tarifa 1; falta a deliberação da AGENERSA com a lista |
| 73 | SABESP | tabela de tarifas-sabesp-geral.pdf | consultado: tabela antiga e sem data da SABESP (mínimo de R$ 16,82), substituída pela NT ARSESP de 2026 (item 11); confirma a divisão regional usada na transcrição da SABESP: litoral (RS e RN) e Vale do Ribeira (RR) com esgoto a 100%, Bragança Paulista e vizinhos em tabela própria |
| 84 | CAER | CAER _ Serviços (item 84).html | consultado: a mesma página da CAER (item 16), com a fórmula de 2011; falta a tabela vigente |
| 85 | COPASA | COPASA - ARSAE-MG.html | consultado: a página da ARSAE-MG sobre a COPASA só lista os atos; a tabela vigente está na Resolução Arsae-MG nº 217, de 22/12/2025, e no Anexo III dela, que faltam |
| 92 | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste (item 92).html | consultado: a mesma notícia da CAEMA de 2023 (item 40), salva de novo |
| 93 | COMPESA | Tabela-Tarifria-Compesa-Reajuste-Maro-2023-para-Site.pdf | consultado: tabela da COMPESA de março de 2023, anterior à Res. ARPE nº 289/2025 (item 18) já transcrita |
| 95 | COSANPA | Tarifa_Novembro_2023.pdf | consultado: tabela da COSANPA de novembro de 2023, anterior ao Anexo VII de 2024 (item 29); era a fonte da base |
| 96 | Águas do Rio / Iguá / Rio+ Saneamento | conteudos-uwbca.pdf | consultado: tabela de reajustes do Rio de Janeiro (2023 a 2025) com multiplicadores por área, sem dizer a que municípios se aplica; falta a deliberação da AGENERSA |
| 98 | CAEMA | tabela_tarifaria_CAEMA.jpg | consultado: a mesma imagem da tabela da CAEMA já usada (item 40); vigência de 05/01/2024, falta o reajuste posterior |
| 99 | Águas do Rio | Águas do Rio - Legislação e Tarifas.html | consultado: a mesma página da Águas do Rio (item 53); falta a deliberação da AGENERSA que diga a região e a área de cada município |
| 108 | Águas do Rio | AguasDoRio_Bloco1_AGENERSA_Reajuste2025_dez2025.pdf | consultado: decisão cautelar da AGENERSA só com o percentual do reajuste de dez/2025; a tabela em R$ não vem no documento |
| 109 | Águas do Rio | AguasDoRio_Bloco4_AGENERSA_Reajuste2025_dez2025.pdf | consultado: decisão cautelar da AGENERSA só com o percentual do reajuste de dez/2025; a tabela em R$ não vem no documento |
| 110 | Águas do Rio / Iguá / Rio+ Saneamento | Igua_AGENERSA_Reajuste2025_dez2025.pdf | consultado: decisão cautelar da AGENERSA só com o percentual do reajuste de dez/2025; a tabela em R$ não vem no documento |
| 156 | SEMAE Piracicaba | semae_piracicaba_ARESPCJ_resoluo_n_720_2026_-_reviso_extraordinria_-_piracicaba.pdf | consultado: Res. ARES-PCJ 720/2026 é a revisão extraordinária da PPP do SEMAE com a Águas do Mirante, sem tabela tarifária |
| 160 | COSANPA | Tarifas_Cosanpa_Santarém.jpg | consultado: tabela da COSANPA de 23/01/2016, superada pelo Anexo VII de 13/12/2024 (item 29), que tem a mesma estrutura |
| 163 | Iguá Castilho | historico-de-tarifas-70cbv.pdf | consultado: Castilho/SP não está entre os 652 municípios da base |
| 173 | CORSAN | Tabela-Tarifaria-298-municipios_2026-x.pdf | consultado: estrutura da CORSAN de 01/01/2026 (PB 8,65, SB 41,03), substituída pela do Anexo 5 de 01/07/2026 (item 4), que o banco já usa |
| 182 | Águas Pontes e Lacerda / Norte Saneamento | aguas_pontes_e_lacerda_comunicados.html | consultado: a página de comunicados da Águas Pontes e Lacerda não traz a tabela tarifária |
| 185 | SAMAE Blumenau / BRK Ambiental Blumenau | brk_blumenau_estrutura_tarifaria_esgoto.html | consultado: página da BRK Blumenau com o histórico; a estrutura 2026 é a imagem do item 184 |
| 186 | COMUSA Novo Hamburgo | comusa_sistema_tarifario.html | consultado: página «Sistema tarifário» da COMUSA, com os links da tabela (item 187), da resolução (item 196) e dos exponenciais (item 197) |
| 193 | SAMAE São Bento do Sul | samae_sao_bento_do_sul_comercial.html | consultado: página-índice dos posts comerciais do SAMAE São Bento do Sul (itens 198 e 199) |
| 198 | SAMAE São Bento do Sul | samae_sao_bento_do_sul_reajuste_agosto_2026.html | consultado: o post do SAMAE São Bento do Sul anuncia o reajuste de 4,40% a partir de 01/08/2026, mas a tabela está nos anexos «Baixar arquivo» (formulário do site), que precisam ser baixados pelo navegador |
| 199 | SAMAE São Bento do Sul | samae_sao_bento_do_sul_tabela_2025_2026.html | consultado: o post «Tabela Tarifária 2025/2026» do SAMAE São Bento do Sul só tem o anexo pelo botão «Baixar arquivo» (formulário) |

## 2. Documentados com vigência antiga (a renovar)

Vigência com mais de 12 meses: procurar o reajuste mais recente.

| Município | Prestador | Documento | Vigência |
| :--- | :--- | :--- | :--- |
| AC - Cruzeiro do Sul | SANEACRE | ESTRUTURATARIFÁRIA-2025-CORRIGIDA.pdf | 14/04/2025 |
| AC - Rio Branco | SANEACRE | ESTRUTURATARIFÁRIA-2025-CORRIGIDA.pdf | 14/04/2025 |
| AM - Humaitá | COHASB / Prefeitura de Humaitá – prestação local | publicado_27336_2014-12-29_585ddfcef92d6a007feb8db90d1cd821.pdf | 29/12/2014 |
| AM - Tabatinga | COSAMA | Estrutura Tarifária – COSAMA – Companhia de Saneamento do Amazonas.html | 2025 |
| ES - Cachoeiro de Itapemirim | BRK Ambiental Cachoeiro | 01-estrutura-tarifaria-cachoeiro-2024.pdf | 01/02/2024 |
| MA - Açailândia | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Bacabal | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Balsas | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Barra do Corda | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Barreirinhas | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Buriticupu | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Caxias | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Chapadinha | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Codó | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Coroatá | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Grajaú | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Imperatriz | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Itapecuru-Mirim | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Paço do Lumiar | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Pinheiro | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Santa Inês | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Santa Luzia | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - São José de Ribamar | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - São Luís | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Timon | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Tutóia | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MA - Viana | CAEMA | Tabela de tarifas de água tem novo valor após três anos sem reajuste.html | 05/01/2024 |
| MT - Cuiabá | Águas Cuiabá (Iguá) | AguasCuiaba_comunicado_reajuste_2025.pdf | 20/03/2025 |
| PA - Abaetetuba | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Acará | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Alenquer | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Altamira | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Ananindeua | Águas do Pará | AguasDoPara_legislacao-e-tarifas.html | 2025 |
| PA - Baião | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Barcarena | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Belém | Águas do Pará | AguasDoPara_legislacao-e-tarifas.html | 2025 |
| PA - Benevides | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Bragança | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Breves | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Cametá | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Canaã dos Carajás | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Capanema | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Capitão Poço | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Castanhal | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Dom Eliseu | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Igarapé-Miri | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Itaituba | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Juruti | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Marabá | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Marituba | Águas do Pará | AguasDoPara_legislacao-e-tarifas.html | 2025 |
| PA - Moju | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Monte Alegre | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Novo Repartimento | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Oriximiná | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Paragominas | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Parauapebas | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Portel | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Redenção | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Rondon do Pará | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Santa Izabel do Pará | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Santarém | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - São Félix do Xingu | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - São Miguel do Guamá | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Tailândia | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Tomé-Açu | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Tucuruí | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Vigia | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Viseu | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Xinguara | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PA - Óbidos | COSANPA | Anexo_VII_Estrutura_Tarifaria_A-B-C-D_13_12_2024.pdf | 13/12/2024 |
| PB - Bayeux | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Cabedelo | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Cajazeiras | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Campina Grande | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Guarabira | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - João Pessoa | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Patos | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Santa Rita | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Sapé | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PB - Sousa | CAGEPA | RESOLUÇÃO-ARPB-004-2025.pdf | 30/06/2025 |
| PE - Abreu e Lima | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Araripina | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Arcoverde | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Belo Jardim | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Bezerros | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Buíque | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Cabo de Santo Agostinho | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Camaragibe | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Carpina | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Caruaru | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Escada | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Garanhuns | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Goiana | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Gravatá | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Igarassu | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Ipojuca | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Jaboatão dos Guararapes | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Limoeiro | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Moreno | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Olinda | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Ouricuri | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Palmares | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Paudalho | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Paulista | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Pesqueira | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Petrolina | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Recife | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Salgueiro | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Santa Cruz do Capibaribe | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Serra Talhada | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Surubim | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - São Lourenço da Mata | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| PE - Vitória de Santo Antão | COMPESA | Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf | 26/03/2025 |
| RO - Ariquemes | CAERD | Resolucao_n._082_2025.pdf | 19/06/2025 |
| RO - Jaru | CAERD | Resolucao_n._082_2025.pdf | 19/06/2025 |
| RO - Ji-Paraná | CAERD | Resolucao_n._082_2025.pdf | 19/06/2025 |
| RO - Porto Velho | CAERD | Resolucao_n._082_2025.pdf | 19/06/2025 |
| RO - Rolim de Moura | CAERD | Resolucao_n._082_2025.pdf | 19/06/2025 |
| RS - Pelotas | SANEP Pelotas | e4ec53825f3073f59ac90291977bea60.pdf | 2022 |
| RS - Uruguaiana | BRK Ambiental Uruguaiana | tabelas-de-tarifas-brk-2025.pdf | 30/08/2025 |
| SC - Itajaí | SEMASA Itajaí | SEMASA _ Tabela tarifária.html | 02/09/2025 |
| SC - São Bento do Sul | SAMAE São Bento do Sul | Tabela Tarifária - 2025_2026 - SAMAE SBS.html | 01/08/2025 |
| SE - Aracaju | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - Estância | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - Itabaiana | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - Lagarto | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - Nossa Senhora do Socorro | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - São Cristóvão | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SE - Tobias Barreto | Iguá Sergipe | estrutura-tarifaria-nfvjp (1).pdf | 01/09/2025 |
| SP - Americana | DAE Americana | Serviços – DAE Americana.html | 12/05/2025 |
| SP - Cosmópolis | Prefeitura de Cosmópolis | prefeitura_de_cosmopolis_ARESPCJ_resoluo_n_623_2025_-_reviso_tarifria_-_cosmpolis.pdf | 01/06/2025 |
| SP - Marília | RIC Ambiental | Taxas de Consumo - RIC Ambiental.html | 01/05/2024 |
| SP - Nova Odessa | CODEN Nova Odessa | coden_nova_odessa_ARESPCJ_resolucao_n_612_2025_-_reajuste_tarifrio_-_nova_odessa.pdf | 27/02/2025 |
| SP - Porto Feliz | SAAE Porto Feliz | saae_porto_feliz_ARESPCJ_resoluo_n_631_2025_-_reviso_tarifria_-_porto_feliz.pdf | 26/05/2025 |
| SP - Santa Bárbara d'Oeste | DAE Santa Bárbara d'Oeste | dae_santa_barbara_d_oeste_ARESPCJ_resoluo_arespcj_655_-_reviso_sbo.pdf | 17/09/2025 |
| SP - Valinhos | DAE Valinhos | 1678301025-resolucao_n_483_2023_-_revisao_tarifaria_-_daev_valinhos.pdf | 27/02/2023 |

## 3. Sem documento: o que buscar

Prestadores com municípios ainda sem documento guardado. A pasta é só sugestão: qualquer nome serve, o processamento identifica o prestador.

| Prestador | Sem documento | A confirmar | Ruim | Já recebido, falta transcrever |
| :--- | ---: | ---: | ---: | :---: |
| CAERN | 7 | 0 | 0 |  |
| CEDAE/serviço local – validar área | 0 | 2 | 0 |  |
| BRK Ambiental Porto Ferreira | 0 | 1 | 0 |  |
| CAER | 0 | 1 | 0 |  |
| CAESC – Companhia de Água, Esgoto e Saneamento de Coari | 0 | 1 | 0 |  |
| DAE Sant'Ana do Livramento | 0 | 1 | 0 |  |
| DAE/VG | 0 | 1 | 0 |  |
| DAEPA | 0 | 1 | 0 |  |
| DAESC Coruripe | 0 | 1 | 0 |  |
| DAMAE São João del-Rei | 0 | 1 | 0 |  |
| DEMSUR | 0 | 1 | 0 |  |
| DMAE Uberlândia | 0 | 1 | 0 |  |
| DMAES Ponte Nova | 0 | 1 | 0 |  |
| Prefeitura de Birigui – Diretoria de Água e Esgoto | 0 | 1 | 0 |  |
| Prestador municipal/local – Iranduba | 0 | 1 | 0 |  |
| Prestador municipal/local – Manicoré | 0 | 1 | 0 |  |
| Prestador municipal/local – São Gabriel da Cachoeira | 0 | 1 | 0 |  |
| Prestador municipal/local – Tefé | 0 | 1 | 0 |  |
| SAAE / prestação municipal de Manacapuru – confirmar | 0 | 1 | 0 |  |
| SAAE Angra dos Reis | 0 | 1 | 0 |  |
| SAAE Cruzeiro | 0 | 1 | 0 |  |
| SAAE Ibitinga | 0 | 1 | 0 |  |
| SAAE Itacoatiara | 0 | 1 | 0 |  |
| SAAE Jacareí | 0 | 1 | 0 |  |
| SAAE Lençóis Paulista | 0 | 1 | 0 |  |
| SAAE Manhuaçu | 0 | 1 | 0 |  |
| SAAE Mariana | 0 | 1 | 0 |  |
| SAAE Maués | 0 | 1 | 0 |  |
| SAAE Parintins | 0 | 1 | 0 |  |
| SAAE Três Pontas | 0 | 1 | 0 |  |
| SAAE Três Rios | 0 | 1 | 0 |  |
| SAAE Vilhena | 0 | 1 | 0 |  |
| SAAE Viçosa | 0 | 1 | 0 |  |
| SAAE Volta Redonda | 0 | 1 | 0 |  |
| SAAET | 0 | 1 | 0 |  |
| SAESA | 0 | 1 | 0 |  |
| SAMAE Tangará da Serra | 0 | 1 | 0 |  |
| SANEAR Rondonópolis | 0 | 1 | 0 |  |
| Sanessol | 0 | 1 | 0 |  |
| São Gabriel Saneamento S.A. | 0 | 1 | 0 |  |
| Águas das Agulhas Negras | 0 | 1 | 0 |  |
| Águas de Andradina | 0 | 1 | 0 |  |
| Águas de Jahu | 0 | 1 | 0 |  |
| Águas de Niterói | 0 | 1 | 0 |  |
| Águas de Nova Friburgo | 0 | 1 | 0 |  |
| Águas de Pará de Minas | 0 | 1 | 0 |  |
| Águas do Imperador | 0 | 1 | 0 |  |
| Águas do Paraíba | 0 | 1 | 0 |  |
| Águas Pontes e Lacerda / Norte Saneamento | 1 | 0 | 0 |  |
