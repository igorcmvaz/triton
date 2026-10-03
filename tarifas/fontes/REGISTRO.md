# Registro do material recebido para a base tarifária

Gerado por `tarifas/registro_de_fontes.py` a partir de `registro.json`. Não edite à mão.

Antes de mandar um arquivo, confira aqui se ele já veio: o registro reconhece o arquivo pela impressão digital SHA-256, ainda que o nome mude.

## O que já chegou

| # | Recebido | Arquivo | Prestador | Conteúdo | Vigência | Situação | Onde está / uso |
| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | 2026-09-29 | Manual-Netuno-4_Junho2014.pdf | Netuno (referência) | Manual do Netuno 4, junho de 2014 | — | consultado, sem dado para a base | não guardado: material de terceiros consultado para o manual; não se redistribui; uso: comparação com o Netuno 4 (manual, seção 35) |
| 2 | 2026-09-30 | Sistema_Tarif_rio___CORSAN.html | CORSAN | Página do Sistema Tarifário da CORSAN (corsan.com.br/sistematarifario) | — | consultado, sem dado para a base | não guardado: página salva do sítio; os anexos dela estão guardados à parte; uso: índice dos anexos tarifários |
| 3 | 2026-09-30 | tabela-exponenciais.pdf | CORSAN | Tabela de Exponenciais, seis categorias | anexa às tabelas de 2026 | transcrito para a base | tarifas/fontes/corsan/tabela-exponenciais.pdf; uso: tarifas/tabela_exponencial_corsan.json |
| 4 | 2026-09-30 | ANEXO-5-TABELA-TARIFARIA_AGOSTO-2026.pdf | CORSAN | ANEXO-5: Tabela I por categoria (PB, SB, esgoto) e Tabela IX industrial; municípios do Apêndice I | 01/07/2026 | transcrito para a base | tarifas/fontes/corsan/ANEXO-5-TABELA-TARIFARIA_AGOSTO-2026.pdf; uso: tarifas/categorias/corsan_2026.json; residencial, comercial, pública, industrial |
| 5 | 2026-10-01 | ANEXO-3-CANOAS-E-ESTEIO-TABELA-TARIFARIA_AGOSTO-2026.pdf | CORSAN | ANEXO-3: Tabela I por categoria, Canoas e Esteio | 01/07/2026 | transcrito para a base | tarifas/fontes/corsan/ANEXO-3-CANOAS-E-ESTEIO-TABELA-TARIFARIA_AGOSTO-2026.pdf; uso: tarifas/categorias/corsan_2026.json; residencial, comercial, pública |
| 6 | 2026-09-30 | Tabela-Tarifaria-Erechim_2026.pdf | CORSAN | Tabela tarifária de Erechim, Tabela I por categoria | 01/01/2026 | transcrito para a base | tarifas/fontes/corsan/Tabela-Tarifaria-Erechim_2026.pdf; uso: tarifas/categorias/corsan_2026.json; residencial, comercial, pública |
| 7 | 2026-09-30 | Tabela-Tarifaria-Santa-Cruz-do-Sul_2026.pdf | CORSAN | Tabela tarifária de Santa Cruz do Sul, Tabela I por categoria | 01/01/2026 | transcrito para a base | tarifas/fontes/corsan/Tabela-Tarifaria-Santa-Cruz-do-Sul_2026.pdf; uso: tarifas/categorias/corsan_2026.json; residencial, comercial, pública |
| 8 | 2026-10-02 | nbn_en_16941-1_2024-e-2.pdf | Norma EN 16941-1 | NBN EN 16941-1:2024, sistemas de aproveitamento de água de chuva | — | consultado, sem dado para a base | não guardado: cópia licenciada à Buildwise; proibida a reprodução; uso: docs/normas_nbr_x_en16941.md (só números de item e valores) |

## O que falta coletar

Por prestador, em ordem de municípios atendidos. «Categorias faltando» conta municípios sem a tabela oficial da categoria; «residencial a confirmar» conta os registros residenciais que não estão auditados (amarelos ou vermelhos no apêndice D do manual). O material que mais rende é a resolução tarifária vigente do prestador, com todas as categorias.

| Prestador | Municípios | Comercial | Pública | Industrial | Social | Residencial a confirmar |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| SABESP | 84 | 84 | 84 | 84 | 84 | 0 |
| COPASA | 47 | 47 | 47 | 47 | 47 | 47 |
| COSANPA | 42 | 42 | 42 | 42 | 42 | 0 |
| EMBASA | 41 | 41 | 41 | 41 | 41 | 41 |
| CAGECE | 37 | 37 | 37 | 37 | 37 | 37 |
| CORSAN | 34 | 0 | 0 | 4 | 34 | 0 |
| COMPESA | 33 | 33 | 33 | 33 | 33 | 0 |
| SANEPAR – Demais localidades | 33 | 33 | 33 | 33 | 33 | 33 |
| SANEAGO | 24 | 24 | 24 | 24 | 24 | 0 |
| CAEMA | 22 | 22 | 22 | 22 | 22 | 0 |
| CASAN | 22 | 22 | 22 | 22 | 22 | 22 |
| Águas do Rio | 15 | 15 | 15 | 15 | 15 | 15 |
| CAGEPA | 10 | 10 | 10 | 10 | 10 | 0 |
| CAERN | 8 | 8 | 8 | 8 | 8 | 0 |
| Iguá Sergipe | 7 | 7 | 7 | 7 | 7 | 0 |
| BRK Tocantins | 5 | 5 | 5 | 5 | 5 | 5 |
| CAERD | 5 | 5 | 5 | 5 | 5 | 0 |
| CESAN | 5 | 5 | 5 | 5 | 5 | 0 |
| SANESUL | 5 | 5 | 5 | 5 | 5 | 0 |
| CEDAE/serviço local – validar área | 4 | 4 | 4 | 4 | 4 | 4 |
| Águas do Piauí | 4 | 4 | 4 | 4 | 4 | 0 |
| Águas do Sertão | 4 | 4 | 4 | 4 | 4 | 0 |
| BRK Alagoas | 3 | 3 | 3 | 3 | 3 | 0 |
| Rio+ Saneamento | 3 | 3 | 3 | 3 | 3 | 3 |
| CSA Equatorial | 2 | 2 | 2 | 2 | 2 | 0 |
| Prolagos | 2 | 2 | 2 | 2 | 2 | 0 |
| SANEACRE | 2 | 2 | 2 | 2 | 2 | 0 |
| BRK Ambiental Cachoeiro | 1 | 1 | 1 | 1 | 1 | 1 |
| BRK Ambiental Limeira | 1 | 1 | 1 | 1 | 1 | 0 |
| BRK Ambiental Porto Ferreira | 1 | 1 | 1 | 1 | 1 | 1 |
| BRK Ambiental Sumaré | 1 | 1 | 1 | 1 | 1 | 0 |
| BRK Ambiental Uruguaiana | 1 | 1 | 1 | 1 | 1 | 0 |
| CAER | 1 | 1 | 1 | 1 | 1 | 1 |
| CAESB | 1 | 1 | 1 | 1 | 1 | 0 |
| CAESC – Companhia de Água, Esgoto e Saneamento de Coari | 1 | 1 | 1 | 1 | 1 | 1 |
| CASAL | 1 | 1 | 1 | 1 | 1 | 0 |
| CESAMA Juiz de Fora | 1 | 1 | 1 | 1 | 1 | 0 |
| CODAU Uberaba | 1 | 1 | 1 | 1 | 1 | 0 |
| COHASB / Prefeitura de Humaitá – prestação local | 1 | 1 | 1 | 1 | 1 | 1 |
| Companhia Ituana de Saneamento (CIS) | 1 | 1 | 1 | 1 | 1 | 0 |
| Companhia Águas de Joinville | 1 | 1 | 1 | 1 | 1 | 0 |
| COMUSA Novo Hamburgo | 1 | 1 | 1 | 1 | 1 | 0 |
| COSAMA | 1 | 1 | 1 | 1 | 1 | 1 |
| DAAE Araraquara | 1 | 1 | 1 | 1 | 1 | 0 |
| DAAE Rio Claro | 1 | 1 | 1 | 1 | 1 | 0 |
| DAE Americana | 1 | 1 | 1 | 1 | 1 | 0 |
| DAE Bauru | 1 | 1 | 1 | 1 | 1 | 0 |
| DAE Jundiaí | 1 | 1 | 1 | 1 | 1 | 0 |
| DAE Sant'Ana do Livramento | 1 | 1 | 1 | 1 | 1 | 1 |
| DAE Valinhos | 1 | 1 | 1 | 1 | 1 | 0 |
| DAE/VG | 1 | 1 | 1 | 1 | 1 | 1 |
| DAEB Bagé | 1 | 1 | 1 | 1 | 1 | 0 |
| DAEP Penápolis | 1 | 1 | 1 | 1 | 1 | 0 |
| DAEPA | 1 | 1 | 1 | 1 | 1 | 1 |
| DAESC Coruripe | 1 | 1 | 1 | 1 | 1 | 1 |
| DAMAE São João del-Rei | 1 | 1 | 1 | 1 | 1 | 1 |
| DEMSUR | 1 | 1 | 1 | 1 | 1 | 1 |
| DMAE Porto Alegre | 1 | 1 | 1 | 1 | 1 | 0 |
| DMAE Poços de Caldas | 1 | 1 | 1 | 1 | 1 | 0 |
| DMAE Uberlândia | 1 | 1 | 1 | 1 | 1 | 1 |
| DMAES Ponte Nova | 1 | 1 | 1 | 1 | 1 | 1 |
| EMASA Balneário Camboriú | 1 | 1 | 1 | 1 | 1 | 0 |
| GS Inima SAMAR | 1 | 1 | 1 | 1 | 1 | 0 |
| Ourinhos Saneamento | 1 | 1 | 1 | 1 | 1 | 0 |
| Prefeitura de Birigui – Diretoria de Água e Esgoto | 1 | 1 | 1 | 1 | 1 | 1 |
| Prestador municipal/local – Iranduba | 1 | 1 | 1 | 1 | 1 | 1 |
| Prestador municipal/local – Manicoré | 1 | 1 | 1 | 1 | 1 | 1 |
| Prestador municipal/local – São Gabriel da Cachoeira | 1 | 1 | 1 | 1 | 1 | 1 |
| Prestador municipal/local – Tefé | 1 | 1 | 1 | 1 | 1 | 1 |
| RIC Ambiental | 1 | 1 | 1 | 1 | 1 | 0 |
| SAAE / prestação municipal de Manacapuru – confirmar | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Angra dos Reis | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Aracruz / CESAN conforme área | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Atibaia | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Barra Mansa | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Cacoal | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Capivari | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Cruzeiro | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Formiga | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Ibitinga | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Indaiatuba | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Itabira | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Itabirito | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Itacoatiara | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Itapira | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Jaboticabal | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Jacareí | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Lagoa da Prata | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Lençóis Paulista | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Linhares | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Lucas do Rio Verde | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Manhuaçu | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Mariana | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Maués | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Mogi Mirim | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Nova Mutum | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Parintins | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Passos | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Pirapora | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Salto | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Sete Lagoas | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Sorocaba | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE São Carlos | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE São Mateus | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Três Pontas | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Três Rios | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Vilhena | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Viçosa | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAE Volta Redonda | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAEB Ambiental | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAEB Barretos | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAEJA | 1 | 1 | 1 | 1 | 1 | 1 |
| SAAET | 1 | 1 | 1 | 1 | 1 | 1 |
| SAE Araguari | 1 | 1 | 1 | 1 | 1 | 0 |
| SAE Ituiutaba | 1 | 1 | 1 | 1 | 1 | 0 |
| SAE Louveira | 1 | 1 | 1 | 1 | 1 | 0 |
| SAEC Catanduva | 1 | 1 | 1 | 1 | 1 | 0 |
| SAECIL Leme | 1 | 1 | 1 | 1 | 1 | 0 |
| SAEG | 1 | 1 | 1 | 1 | 1 | 0 |
| SAEMA Araras | 1 | 1 | 1 | 1 | 1 | 0 |
| SAEMAS Sertãozinho | 1 | 1 | 1 | 1 | 1 | 0 |
| SAEP Pirassununga | 1 | 1 | 1 | 1 | 1 | 1 |
| SAERP Ribeirão Preto | 1 | 1 | 1 | 1 | 1 | 0 |
| SAERP São José do Rio Pardo | 1 | 1 | 1 | 1 | 1 | 1 |
| SAESA | 1 | 1 | 1 | 1 | 1 | 1 |
| SAEV Ambiental | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Blumenau / BRK Ambiental Blumenau | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Brusque | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Caxias do Sul | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Gaspar | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Jaraguá do Sul | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Mogi Guaçu | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE São Bento do Sul | 1 | 1 | 1 | 1 | 1 | 0 |
| SAMAE Tangará da Serra | 1 | 1 | 1 | 1 | 1 | 1 |
| SANASA Campinas | 1 | 1 | 1 | 1 | 1 | 0 |
| Saneaqua | 1 | 1 | 1 | 1 | 1 | 0 |
| SANEAR Colatina | 1 | 1 | 1 | 1 | 1 | 0 |
| SANEAR Rondonópolis | 1 | 1 | 1 | 1 | 1 | 1 |
| SANEBAVI Vinhedo | 1 | 1 | 1 | 1 | 1 | 0 |
| Saneouro | 1 | 1 | 1 | 1 | 1 | 0 |
| SANEP Pelotas | 1 | 1 | 1 | 1 | 1 | 0 |
| SANEPAR – Curitiba | 1 | 1 | 1 | 1 | 1 | 1 |
| Sanessol | 1 | 1 | 1 | 1 | 1 | 1 |
| SEMAE Piracicaba | 1 | 1 | 1 | 1 | 1 | 0 |
| SeMAE Rio Preto | 1 | 1 | 1 | 1 | 1 | 0 |
| SEMAE São Leopoldo | 1 | 1 | 1 | 1 | 1 | 0 |
| SEMASA Itajaí | 1 | 1 | 1 | 1 | 1 | 0 |
| SEMASA Lages | 1 | 1 | 1 | 1 | 1 | 0 |
| Serviço local – Barra do Piraí | 1 | 1 | 1 | 1 | 1 | 1 |
| São Gabriel Saneamento S.A. | 1 | 1 | 1 | 1 | 1 | 1 |
| Tubarão Saneamento | 1 | 1 | 1 | 1 | 1 | 0 |
| Verde Alagoas | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas Alta Floresta / Norte Saneamento | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas Cuiabá (Iguá) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas da Imperatriz | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas das Agulhas Negras | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Andradina | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Barra do Garças (Aegea) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Jahu | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Juturnaíba | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Manaus | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Matão | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Niterói | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Nova Friburgo | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Pará de Minas | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas de Primavera (Aegea) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Sinop (Aegea) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Sorriso | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Teresina | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas de Valadares (Aegea) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas do Imperador | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas do Pantanal (autarquia municipal) | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas do Paraíba | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas do Rio / Iguá / Rio+ Saneamento | 1 | 1 | 1 | 1 | 1 | 1 |
| Águas Guariroba | 1 | 1 | 1 | 1 | 1 | 0 |
| Águas Pontes e Lacerda / Norte Saneamento | 1 | 1 | 1 | 1 | 1 | 0 |
