# Regimes tarifários

A base traz **652 municípios** com estrutura tarifária, percentual
de esgoto, regime de mínimo, data de vigência e fonte. Esta lista é extraída
da própria base do programa, e não transcrita.

## Os códigos de faixa

Cada linha da tabela tarifária é uma quádrupla `(mínimo, máximo, valor, código)`.

Os seis códigos e o efeito de cada um sobre a fatura estão desenhados na seção {{n:29}}, e não se repetem aqui.


## Os seis regimes

<!-- tabela: Distribuição dos municípios do catálogo pelos seis regimes tarifários -->
| Regime | Municípios | O que acontece ao economizar |
| :--- | ---: | :--- |
| **Sem mínimo** | 165 | Cada m³ economizado reduz a fatura. |
| **Disponibilidade** | 122 | Valor fixo que **soma** por cima do consumo medido. Cada m³ economizado desconta. |
| **Franquia no mínimo** | 329 | O valor fixo já inclui um volume. Economizar **abaixo** da franquia não desconta nada. |
| **Franquia retroativa** | 2 | Até a franquia paga-se o fixo; passando dela, tarifa-se **tudo desde zero**. |
| **Piso de pagamento** | 0 | A fatura **não fica** abaixo do piso. Não soma: limita. |
| **Fórmula exponencial** | 34 | Serviço básico mais `PB × Cⁿ`, com `n` pelo consumo do mês (CORSAN). Cada m³ economizado desconta. |

> O piso de pagamento está implementado e nenhum município da base foi
> classificado nele até esta versão.

## Distribuição por unidade da federação

A cobertura do catálogo acompanha a população, e não o território: as capitais e as regiões metropolitanas estão quase todas cadastradas, e o interior das regiões Norte e Centro-Oeste concentra os municípios ainda ausentes ({{fig:fig42_uf}}).

![Os municípios do catálogo, por unidade da federação](../figuras/fig42_uf.png)

*Figura 99 — A distribuição dos 652 municípios catalogados pelas unidades da federação, com as cores identificando a macrorregião. São Paulo e Minas Gerais respondem sozinhos por quase um terço do catálogo.*


## Atualização e auditoria da base

A base tarifária é mantida pelo grupo com uma rotina de atualização executada fora da interface, antes de cada versão. A rotina tem três componentes.

**Energia elétrica.** As tarifas residenciais do subgrupo B1 são lidas da base aberta de tarifas homologadas das distribuidoras, publicada pela Agência Nacional de Energia Elétrica (ANEEL), e associadas à distribuidora de cada município do catálogo.

**Água e esgoto.** Um registro de evidências primárias associa cada prestador à agência reguladora, à página oficial de tarifas e ao tipo de ato que as publica. Os prestadores com portal padronizado têm leitura automática; os demais são marcados para conferência manual do decreto ou da resolução, e a estrutura resultante é submetida à mesma validação de regime descrita neste apêndice.

**Detecção de alterações.** Cada página oficial monitorada é registrada com a assinatura SHA-256 do conteúdo e os cabeçalhos `ETag` e `Last-Modified`. Uma nova verificação compara as assinaturas e aponta as páginas alteradas desde a última coleta, que são as candidatas a revisão tarifária.

A rotina pode simular a atualização sem gravar a base, executar apenas a detecção de alterações, restringir-se a uma unidade da federação ou a um município e separar energia de saneamento. Cada execução grava um relatório de auditoria em Markdown e um painel HTML com a situação de cada município.

## Grau de confiança

Cada registro traz o grau de confiança da coleta:

<!-- tabela: Grau de confiança dos registros tarifários do catálogo -->
| Grau | Registros |
| :--- | ---: |
| A — alta | 580 |
| B — boa | 63 |
| C — estrutura a conferir | 5 |
| D — estrutura incompleta | 4 |

> **Confira sempre a data de vigência** do registro do seu município contra a
> resolução da concessionária. Tarifas são reajustadas anualmente, e a seção {{n:16}}
> ensina o teste que identifica estrutura errada.


## As faixas por município e categoria

A tabela abaixo traz o preço da água, em R$/m³, em cada intervalo de consumo mensal,
para cada estrutura do catálogo. As colunas são a maior discretização que o catálogo
pede: a união dos limites de faixa de todos os prestadores, de modo que dentro de cada
coluna nenhum prestador muda o preço. Municípios com a mesma tabela formam uma linha,
identificada pelo número da primeira coluna, que se repete nas partes seguintes.

A categoria residencial está nos 652 municípios; as demais aparecem onde a tabela oficial
do prestador foi coletada. A tabela é gerada da base a cada versão e cresce com ela.
A parcela fixa soma por cima do consumo; um preço zero nas primeiras faixas é o volume
já incluído no valor fixo (franquia no mínimo).

A cor da linha diz quanto o dado merece confiança: **verde** (🟢), auditado contra a
fonte primária, a resolução ou a tabela oficial do prestador; **amarelo** (🟡), coletado
automaticamente ou marcado para revisão, e por isso a confirmar contra a resolução
vigente; **vermelho** (🔴), estrutura incompleta, que não deve ser usada sem correção.

<!-- tabela: As estruturas tarifárias do catálogo, numeradas para as tabelas de preço por faixa que vêm a seguir -->
| Nº | Prestador: municípios | Categoria | Fixo (R$/mês) | Esgoto |
| ---: | :--- | :--- | :--- | :--- |
| 🟢 1 | BRK Alagoas: Maceió (AL) | Residencial | — | 100% |
| 🟢 2 | BRK Alagoas: Marechal Deodoro (AL) | Residencial | — | 80% |
| 🟢 3 | BRK Alagoas: Rio Largo (AL) | Residencial | — | 80% |
| 🟡 4 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Residencial | 45,00 | 80% |
| 🟢 5 | BRK Ambiental Limeira: Limeira (SP) | Residencial | 37,10 | 100% |
| 🟡 6 | BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Residencial | 42,00 | 90% |
| 🟢 7 | BRK Ambiental Sumaré: Sumaré (SP) | Residencial | 36,35 | 80% |
| 🟢 8 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Residencial | — | 70% |
| 🟡 9 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO) e mais 2 | Residencial | — | 80% |
| 🟢 10 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA) e mais 19 | Residencial | 33,58 | 100% |
| 🟡 11 | CAER: Boa Vista (RR) | Residencial | 39,92 | 80% |
| 🟢 12 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO) e mais 2 | Residencial | 57,51 | 70% |
| 🟢 13 | CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN) e mais 4 | Residencial | 56,96 | 70% |
| 🟢 14 | CAERN: Natal (RN) | Residencial | 51,40 | 70% |
| 🟢 15 | CAESB: Brasília (DF) | Residencial | 11,62 | 100% |
| 🟡 16 | CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Residencial | 32,50 | 80% |
| 🟡 17 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE) e mais 34 | Residencial | — | 80% |
| 🟢 18 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB) e mais 7 | Residencial | 54,82 | 80% |
| 🟢 19 | CASAL: Arapiraca (AL) | Residencial | — | 80% |
| 🟡 20 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC) e mais 19 | Residencial | 46,34 | 100% |
| 🟡 21 | CEDAE/serviço local – validar área: Guapimirim (RJ), Itaperuna (RJ), Macaé (RJ) e mais 1 | Residencial | — | 100% |
| 🟢 22 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Residencial | 15,01 | 80% |
| 🟢 23 | CESAN: Cariacica (ES), Guarapari (ES), Serra (ES) e mais 2 | Residencial | 57,39 | 80% |
| 🟢 24 | CODAU Uberaba: Uberaba (MG) | Residencial | — | 95% |
| 🟡 25 | COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Residencial | 32,50 | 80% |
| 🟢 26 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Residencial | 36,96 | 100% |
| 🟢 27 | Companhia Águas de Joinville: Joinville (SC) | Residencial | 34,93 | 80% |
| 🟢 28 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE) e mais 30 | Residencial | 61,77 | 100% |
| 🟢 29 | COMUSA Novo Hamburgo: Novo Hamburgo (RS) | Residencial | 43,21 | 70% |
| 🟡 30 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG) e mais 44 | Residencial | 25,77 | 74% |
| 🟡 31 | COSAMA: Tabatinga (AM) | Residencial | 32,50 | 80% |
| 🟢 32 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA) e mais 39 | Residencial | — | 80% |
| 🟢 33 | CSA Equatorial: Macapá (AP), Santana (AP) | Residencial | 42,91 | 100% |
| 🟢 34 | DAAE Araraquara: Araraquara (SP) | Residencial | 22,70 | 100% |
| 🟢 35 | DAAE Rio Claro: Rio Claro (SP) | Residencial | 35,36 | 100% |
| 🟢 36 | DAE Americana: Americana (SP) | Residencial | até 6 m³: 14,30 (retroativa) | 100% |
| 🟢 37 | DAE Bauru: Bauru (SP) | Residencial | até 6 m³: 19,37 (retroativa) | 65% |
| 🟢 38 | DAE Jundiaí: Jundiaí (SP) | Residencial | 40,84 | 69% |
| 🟡 39 | DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Residencial | — | 80% |
| 🟢 40 | DAE Valinhos: Valinhos (SP) | Residencial | 23,73 | 100% |
| 🟡 41 | DAE/VG: Várzea Grande (MT) | Residencial | 31,20 | 80% |
| 🟢 42 | DAEB Bagé: Bagé (RS) | Residencial | 53,37 | 50% |
| 🟢 43 | DAEP Penápolis: Penápolis (SP) | Residencial | 7,31 | 70% |
| 🟡 44 | DAEPA: Patrocínio (MG) | Residencial | — | 80% |
| 🟡 45 | DAESC Coruripe: Coruripe (AL) | Residencial | — | 80% |
| 🟡 46 | DAMAE São João del-Rei: São João del-Rei (MG) | Residencial | — | 80% |
| 🟡 47 | DEMSUR: Muriaé (MG) | Residencial | — | 80% |
| 🟢 48 | DMAE Porto Alegre: Porto Alegre (RS) | Residencial | — | 100% |
| 🟢 49 | DMAE Poços de Caldas: Poços de Caldas (MG) | Residencial | — | 85% |
| 🟡 50 | DMAE Uberlândia: Uberlândia (MG) | Residencial | — | 80% |
| 🟡 51 | DMAES Ponte Nova: Ponte Nova (MG) | Residencial | — | 80% |
| 🟢 52 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Residencial | 44,95 | 100% |
| 🟡 53 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA) e mais 38 | Residencial | 44,77 | 80% |
| 🟢 54 | GS Inima SAMAR: Araçatuba (SP) | Residencial | 28,48 | 80% |
| 🟢 55 | Iguá Sergipe: Aracaju (SE), Estância (SE), Itabaiana (SE) e mais 4 | Residencial | 49,26 | 80% |
| 🟢 56 | Ourinhos Saneamento: Ourinhos (SP) | Residencial | — | 50% |
| 🟡 57 | Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Residencial | 23,90 | 100% |
| 🟡 58 | Prestador municipal/local – Iranduba: Iranduba (AM) | Residencial | 32,50 | 80% |
| 🟡 59 | Prestador municipal/local – Manicoré: Manicoré (AM) | Residencial | 32,50 | 80% |
| 🟡 60 | Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Residencial | 32,50 | 80% |
| 🟡 61 | Prestador municipal/local – Tefé: Tefé (AM) | Residencial | 32,50 | 80% |
| 🟢 62 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Residencial | — | 100% |
| 🟢 63 | RIC Ambiental: Marília (SP) | Residencial | 19,71 | 75% |
| 🟡 64 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Residencial | — | 100% |
| 🟡 65 | SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Residencial | 32,50 | 80% |
| 🟡 66 | SAAE Angra dos Reis: Angra dos Reis (RJ) | Residencial | — | 100% |
| 🟡 67 | SAAE Aracruz / CESAN conforme área: Aracruz (ES) | Residencial | 57,39 | 80% |
| 🟡 68 | SAAE Atibaia: Atibaia (SP) | Residencial | 52,97 | 100% |
| 🟡 69 | SAAE Barra Mansa: Barra Mansa (RJ) | Residencial | — | 100% |
| 🟡 70 | SAAE Cacoal: Cacoal (RO) | Residencial | 17,58 | 60% |
| 🟡 71 | SAAE Capivari: Capivari (SP) | Residencial | 33,11 | 90% |
| 🟡 72 | SAAE Cruzeiro: Cruzeiro (SP) | Residencial | 42,00 | 90% |
| 🟡 73 | SAAE Formiga: Formiga (MG) | Residencial | 21,40 | 50% |
| 🟡 74 | SAAE Ibitinga: Ibitinga (SP) | Residencial | — | 100% |
| 🟡 75 | SAAE Indaiatuba: Indaiatuba (SP) | Residencial | 35,10 | 90% |
| 🟡 76 | SAAE Itabira: Itabira (MG) | Residencial | — | 80% |
| 🟡 77 | SAAE Itabirito: Itabirito (MG) | Residencial | 22,73 | 60% |
| 🟡 78 | SAAE Itacoatiara: Itacoatiara (AM) | Residencial | 32,50 | 80% |
| 🟡 79 | SAAE Itapira: Itapira (SP) | Residencial | 22,71 | 100% |
| 🟡 80 | SAAE Jaboticabal: Jaboticabal (SP) | Residencial | 28,91 | 100% |
| 🟡 81 | SAAE Jacareí: Jacareí (SP) | Residencial | 42,00 | 90% |
| 🟡 82 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Residencial | 41,70 | 65% |
| 🟡 83 | SAAE Lençóis Paulista: Lençóis Paulista (SP) | Residencial | 42,00 | 90% |
| 🟡 84 | SAAE Linhares: Linhares (ES) | Residencial | 45,00 | 80% |
| 🟡 85 | SAAE Lucas do Rio Verde: Lucas do Rio Verde (MT) | Residencial | — | 80% |
| 🟡 86 | SAAE Manhuaçu: Manhuaçu (MG) | Residencial | — | 80% |
| 🟡 87 | SAAE Mariana: Mariana (MG) | Residencial | 29,82 | 100% |
| 🟡 88 | SAAE Maués: Maués (AM) | Residencial | 32,50 | 80% |
| 🟡 89 | SAAE Mogi Mirim: Mogi Mirim (SP) | Residencial | 20,25 | 140% |
| 🟡 90 | SAAE Nova Mutum: Nova Mutum (MT) | Residencial | 24,82 | 80% |
| 🟡 91 | SAAE Parintins: Parintins (AM) | Residencial | 32,50 | 80% |
| 🟡 92 | SAAE Passos: Passos (MG) | Residencial | — | 80% |
| 🟡 93 | SAAE Pirapora: Pirapora (MG) | Residencial | 43,06 | 50% |
| 🟡 94 | SAAE Salto: Salto (SP) | Residencial | 32,22 | 100% |
| 🔴 95 | SAAE Sete Lagoas: Sete Lagoas (MG) | Residencial | 30,96 | 80% |
| 🟡 96 | SAAE Sorocaba: Sorocaba (SP) | Residencial | 22,00 | 92% |
| 🟡 97 | SAAE São Carlos: São Carlos (SP) | Residencial | — | 100% |
| 🟡 98 | SAAE São Mateus: São Mateus (ES) | Residencial | — | 80% |
| 🟡 99 | SAAE Três Pontas: Três Pontas (MG) | Residencial | — | 80% |
| 🟡 100 | SAAE Três Rios: Três Rios (RJ) | Residencial | — | 100% |
| 🟡 101 | SAAE Vilhena: Vilhena (RO) | Residencial | 57,51 | 70% |
| 🟡 102 | SAAE Viçosa: Viçosa (MG) | Residencial | — | 50% |
| 🟡 103 | SAAE Volta Redonda: Volta Redonda (RJ) | Residencial | — | 100% |
| 🔴 104 | SAAEB Ambiental: Bebedouro (SP) | Residencial | 34,62 | 80% |
| 🟡 105 | SAAEB Barretos: Barretos (SP) | Residencial | 28,90 | 50% |
| 🟡 106 | SAAEJA: Jaguariúna (SP) | Residencial | 22,81 | 100% |
| 🟡 107 | SAAET: Taquaritinga (SP) | Residencial | 42,00 | 90% |
| 🟢 108 | SABESP: Amparo (SP) | Residencial | 29,47 | 90% |
| 🟢 109 | SABESP: Artur Nogueira (SP), Assis (SP), Avaré (SP) e mais 36 | Residencial | 40,42 | 80% |
| 🟢 110 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP) e mais 26 | Residencial | 40,42 | 100% |
| 🟢 111 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP) e mais 9 | Residencial | 40,42 | 100% |
| 🟢 112 | SABESP: Bragança Paulista (SP) | Residencial | 40,42 | 100% |
| 🟢 113 | SABESP: Olímpia (SP) | Residencial | 25,34 | 80% |
| 🟢 114 | SABESP: Presidente Prudente (SP) | Residencial | 32,27 | 80% |
| 🟢 115 | SAE Araguari: Araguari (MG) | Residencial | 33,89 | 80% |
| 🟢 116 | SAE Ituiutaba: Ituiutaba (MG) | Residencial | 18,12 | 70% |
| 🟢 117 | SAE Louveira: Louveira (SP) | Residencial | 27,93 | 85% |
| 🟢 118 | SAEC Catanduva: Catanduva (SP) | Residencial | 24,79 | 100% |
| 🟢 119 | SAECIL Leme: Leme (SP) | Residencial | 35,33 | 85% |
| 🟢 120 | SAEG: Guaratinguetá (SP) | Residencial | 30,06 | 80% |
| 🟢 121 | SAEMA Araras: Araras (SP) | Residencial | 25,71 | 80% |
| 🟢 122 | SAEMAS Sertãozinho: Sertãozinho (SP) | Residencial | 25,31 | 80% |
| 🔴 123 | SAEP Pirassununga: Pirassununga (SP) | Residencial | 29,91 | 100% |
| 🟢 124 | SAERP Ribeirão Preto: Ribeirão Preto (SP) | Residencial | 14,06 | 128% |
| 🔴 125 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Residencial | 29,99 | 80% |
| 🟡 126 | SAESA: São Caetano do Sul (SP) | Residencial | 42,00 | 90% |
| 🟢 127 | SAEV Ambiental: Votuporanga (SP) | Residencial | 28,22 | 100% |
| 🟢 128 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Residencial | 47,43 | 112% |
| 🟢 129 | SAMAE Brusque: Brusque (SC) | Residencial | 42,38 | 80% |
| 🟢 130 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Residencial | 38,30 | 80% |
| 🟢 131 | SAMAE Gaspar: Gaspar (SC) | Residencial | 50,58 | 80% |
| 🟢 132 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Residencial | 30,16 | 80% |
| 🟢 133 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Residencial | 18,91 | 100% |
| 🟢 134 | SAMAE São Bento do Sul: São Bento do Sul (SC) | Residencial | 31,40 | 80% |
| 🟡 135 | SAMAE Tangará da Serra: Tangará da Serra (MT) | Residencial | — | 80% |
| 🟢 136 | SANASA Campinas: Campinas (SP) | Residencial | 53,65 | 123% |
| 🟢 137 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Residencial | 38,37 | 80% |
| 🟢 138 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO) e mais 21 | Residencial | 17,46 | 100% |
| 🟢 139 | Saneaqua: Mairinque (SP) | Residencial | — | 100% |
| 🟢 140 | SANEAR Colatina: Colatina (ES) | Residencial | — | 80% |
| 🟡 141 | SANEAR Rondonópolis: Rondonópolis (MT) | Residencial | 36,50 | 80% |
| 🟢 142 | SANEBAVI Vinhedo: Vinhedo (SP) | Residencial | 40,20 | 100% |
| 🟢 143 | Saneouro: Ouro Preto (MG) | Residencial | 25,72 | 95% |
| 🟢 144 | SANEP Pelotas: Pelotas (RS) | Residencial | 28,96 | 80% |
| 🟡 145 | SANEPAR – Curitiba: Curitiba (PR) | Residencial | 55,09 | 85% |
| 🟡 146 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR) e mais 30 | Residencial | 55,09 | 80% |
| 🟡 147 | Sanessol: Mirassol (SP) | Residencial | 42,00 | 90% |
| 🟢 148 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS) e mais 2 | Residencial | 16,50 | 70% |
| 🟢 149 | SEMAE Piracicaba: Piracicaba (SP) | Residencial | 31,99 | 100% |
| 🟢 150 | SeMAE Rio Preto: São José do Rio Preto (SP) | Residencial | 26,63 | 100% |
| 🟢 151 | SEMAE São Leopoldo: São Leopoldo (RS) | Residencial | 61,29 | 80% |
| 🟢 152 | SEMASA Itajaí: Itajaí (SC) | Residencial | 41,70 | 80% |
| 🟢 153 | SEMASA Lages: Lages (SC) | Residencial | 44,00 | 80% |
| 🟡 154 | Serviço local – Barra do Piraí: Barra do Piraí (RJ) | Residencial | — | 100% |
| 🟡 155 | São Gabriel Saneamento S.A.: São Gabriel (RS) | Residencial | 33,89 | 80% |
| 🟢 156 | Tubarão Saneamento: Tubarão (SC) | Residencial | — | 100% |
| 🟢 157 | Verde Alagoas: União dos Palmares (AL) | Residencial | — | 80% |
| 🟡 158 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Residencial | — | 80% |
| 🟢 159 | Águas Cuiabá (Iguá): Cuiabá (MT) | Residencial | — | 90% |
| 🟢 160 | Águas da Imperatriz: Teresópolis (RJ) | Residencial | — | 90% |
| 🟡 161 | Águas das Agulhas Negras: Resende (RJ) | Residencial | — | 100% |
| 🟡 162 | Águas de Andradina: Andradina (SP) | Residencial | 42,00 | 90% |
| 🟢 163 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Residencial | — | 80% |
| 🟡 164 | Águas de Jahu: Jaú (SP) | Residencial | 42,00 | 90% |
| 🟢 165 | Águas de Juturnaíba: Araruama (RJ) | Residencial | — | 100% |
| 🟡 166 | Águas de Manaus: Manaus (AM) | Residencial | — | 80% |
| 🟢 167 | Águas de Matão: Matão (SP) | Residencial | 45,32 | 100% |
| 🟡 168 | Águas de Niterói: Niterói (RJ) | Residencial | — | 100% |
| 🟡 169 | Águas de Nova Friburgo: Nova Friburgo (RJ) | Residencial | — | 100% |
| 🟡 170 | Águas de Pará de Minas: Pará de Minas (MG) | Residencial | — | 80% |
| 🟢 171 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Residencial | — | 90% |
| 🟢 172 | Águas de Sinop (Aegea): Sinop (MT) | Residencial | — | 100% |
| 🟢 173 | Águas de Sorriso: Sorriso (MT) | Residencial | — | 80% |
| 🟢 174 | Águas de Teresina: Teresina (PI) | Residencial | 46,83 | 80% |
| 🟢 175 | Águas de Valadares (Aegea): Governador Valadares (MG) | Residencial | 14,67 | 70% |
| 🟡 176 | Águas do Imperador: Petrópolis (RJ) | Residencial | — | 100% |
| 🟢 177 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Residencial | — | 50% |
| 🟡 178 | Águas do Paraíba: Campos dos Goytacazes (RJ) | Residencial | — | 100% |
| 🟢 179 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI) e mais 1 | Residencial | 52,89 | 80% |
| 🟡 180 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ) e mais 5 | Residencial | — | 100% |
| 🟡 181 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ) e mais 4 | Residencial | — | 100% |
| 🟡 182 | Águas do Rio / Iguá / Rio+ Saneamento: Rio de Janeiro (RJ) | Residencial | — | 100% |
| 🟢 183 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL) | Residencial | — | 80% |
| 🟢 184 | Águas do Sertão: Penedo (AL) | Residencial | — | 80% |
| 🟢 185 | Águas do Sertão: São Miguel dos Campos (AL) | Residencial | — | 80% |
| 🟢 186 | Águas Guariroba: Campo Grande (MS) | Residencial | 19,87 | 70% |
| 🟢 187 | Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Residencial | — | 90% |

<!-- tabela: Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 1 de 3: 0–5 a 20–25 m³) -->
| Nº | 0–5 | 5–6 | 6–7 | 7–10 | 10–12 | 12–13 | 13–15 | 15–17 | 17–20 | 20–25 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 7,64 | 7,64 | 7,64 | 7,64 | 14,61 | 14,61 | 14,61 | 16,89 | 16,89 | 18,04 |
| 🟢 2 | 6,82 | 6,82 | 6,82 | 6,82 | 12,70 | 12,70 | 12,70 | 14,27 | 14,27 | 15,46 |
| 🟢 3 | 7,64 | 7,64 | 7,64 | 7,64 | 14,61 | 14,61 | 14,61 | 16,89 | 16,89 | 18,04 |
| 🟡 4 | 0,00 | 0,00 | 0,00 | 0,00 | 6,10 | 6,10 | 6,10 | 6,10 | 6,10 | 9,80 |
| 🟢 5 | 0,00 | 0,00 | 0,00 | 0,00 | 5,11 | 5,11 | 5,11 | 10,14 | 10,14 | 10,14 |
| 🟡 6 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 7 | 0,00 | 0,00 | 0,00 | 0,00 | 3,64 | 3,64 | 3,64 | 3,64 | 3,64 | 4,01 |
| 🟢 8 | 10,20 | 10,20 | 10,20 | 10,20 | 10,70 | 10,70 | 10,70 | 10,70 | 10,70 | 15,34 |
| 🟡 9 | 8,76 | 3,05 | 3,05 | 3,05 | 8,66 | 8,66 | 8,66 | 11,07 | 11,07 | 13,53 |
| 🟢 10 | 0,00 | 0,00 | 0,00 | 0,00 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 10,77 |
| 🟡 11 | 0,00 | 0,00 | 0,00 | 0,00 | 5,40 | 5,40 | 5,40 | 5,40 | 5,40 | 8,90 |
| 🟢 12 | 0,00 | 0,00 | 0,00 | 0,00 | 6,52 | 6,52 | 6,52 | 7,17 | 7,17 | 8,61 |
| 🟢 13 | 0,00 | 0,00 | 0,00 | 0,00 | 6,34 | 6,34 | 6,34 | 7,51 | 7,51 | 8,45 |
| 🟢 14 | 0,00 | 0,00 | 0,00 | 0,00 | 5,73 | 5,73 | 5,73 | 6,77 | 6,77 | 7,64 |
| 🟢 15 | 4,30 | 4,30 | 4,30 | 5,15 | 5,15 | 5,15 | 10,21 | 10,21 | 10,21 | 14,81 |
| 🟡 16 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 17 | 6,77 | 6,77 | 6,77 | 6,77 | 8,78 | 8,78 | 8,78 | 9,49 | 9,49 | 16,29 |
| 🟢 18 | 0,00 | 0,00 | 0,00 | 0,00 | 7,08 | 7,08 | 7,08 | 7,08 | 7,08 | 9,32 |
| 🟢 19 | 7,28 | 7,28 | 7,28 | 7,28 | 13,90 | 13,90 | 13,90 | 16,07 | 16,07 | 17,17 |
| 🟡 20 | 3,08 | 3,08 | 3,08 | 3,08 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟡 21 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟢 22 | 1,65 | 4,46 | 4,46 | 4,46 | 5,58 | 5,58 | 5,58 | 6,32 | 6,32 | 8,55 |
| 🟢 23 | 2,26 | 2,26 | 2,26 | 2,26 | 4,52 | 4,52 | 4,52 | 8,14 | 8,14 | 9,77 |
| 🟢 24 | 3,91 | 3,91 | 3,91 | 3,91 | 5,20 | 5,20 | 5,20 | 5,20 | 5,20 | 5,74 |
| 🟡 25 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 26 | 0,00 | 0,00 | 0,00 | 0,00 | 4,34 | 4,34 | 4,34 | 4,34 | 4,34 | 6,63 |
| 🟢 27 | 1,49 | 1,49 | 1,49 | 1,49 | 9,89 | 9,89 | 9,89 | 9,95 | 9,95 | 9,95 |
| 🟢 28 | 0,00 | 0,00 | 0,00 | 0,00 | 7,09 | 7,09 | 7,09 | 7,09 | 7,09 | 8,42 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 2,69 | 5,33 | 5,33 | 5,33 | 8,06 | 8,06 | 8,06 | 10,83 | 10,83 | 13,66 |
| 🟡 31 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 32 | 4,91 | 4,91 | 4,91 | 4,91 | 7,00 | 7,00 | 7,00 | 7,00 | 7,00 | 9,38 |
| 🟢 33 | 0,00 | 0,00 | 0,00 | 0,00 | 4,49 | 4,49 | 4,49 | 4,49 | 4,49 | 5,06 |
| 🟢 34 | 0,00 | 0,00 | 0,00 | 0,00 | 4,09 | 4,09 | 4,09 | 4,09 | 4,09 | 5,83 |
| 🟢 35 | 0,00 | 0,00 | 0,00 | 0,00 | 7,19 | 7,19 | 7,19 | 7,19 | 7,19 | 10,77 |
| 🟢 36 | — | — | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | — | — | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 0,00 | 0,00 | 0,00 | 0,00 | 5,18 | 5,18 | 5,18 | 7,65 | 7,65 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 0,00 | 0,00 | 0,00 | 0,00 | 4,40 | 4,40 | 4,40 | 4,40 | 5,69 | 5,69 |
| 🟡 41 | 0,00 | 0,00 | 0,00 | 0,00 | 4,20 | 4,20 | 4,20 | 4,20 | 4,20 | 6,80 |
| 🟢 42 | 4,26 | 4,26 | 4,26 | 4,26 | 5,11 | 5,11 | 5,11 | 5,11 | 5,11 | 6,84 |
| 🟢 43 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 3,76 | 4,89 |
| 🟡 44 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 45 | 7,28 | 7,28 | 7,28 | 7,28 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 |
| 🟡 46 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 47 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 3,70 | 3,70 | 3,70 | 3,70 | 4,44 | 4,44 | 4,44 | 5,22 | 5,22 | 6,74 |
| 🟡 50 | 3,85 | 3,85 | 3,85 | 3,85 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 8,20 |
| 🟡 51 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 52 | 0,66 | 0,66 | 0,66 | 0,66 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 |
| 🟡 53 | 0,00 | 0,00 | 1,77 | 1,77 | 12,53 | 12,53 | 12,53 | 13,41 | 13,41 | 15,08 |
| 🟢 54 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,50 | 3,50 | 3,50 | 3,50 | 6,46 |
| 🟢 55 | 0,00 | 0,00 | 0,00 | 0,00 | 11,02 | 11,02 | 11,02 | 11,02 | 11,02 | 16,75 |
| 🟢 56 | 3,11 | 3,11 | 3,11 | 3,11 | 6,17 | 6,17 | 6,17 | 6,17 | 6,17 | 7,77 |
| 🟡 57 | 0,00 | 0,00 | 0,00 | 0,00 | 2,90 | 2,90 | 2,90 | 2,90 | 2,90 | 3,34 |
| 🟡 58 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 59 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 60 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 61 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟢 62 | 17,04 | 17,04 | 17,04 | 17,04 | 22,32 | 22,32 | 22,32 | 35,74 | 35,74 | 35,74 |
| 🟢 63 | 0,00 | 2,31 | 2,31 | 2,31 | 2,31 | 2,31 | 2,31 | 6,24 | 6,24 | 6,24 |
| 🟡 64 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 15,37 | 15,37 | 15,37 |
| 🟡 65 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 66 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 67 | 0,00 | 0,00 | 0,00 | 0,00 | 4,52 | 4,52 | 4,52 | 8,14 | 8,14 | 9,77 |
| 🟡 68 | 0,00 | 0,00 | 0,00 | 0,00 | 7,97 | 7,97 | 7,97 | 7,97 | 7,97 | 13,13 |
| 🟡 69 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 70 | 0,00 | 0,00 | 0,00 | 0,00 | 2,11 | 2,11 | 2,11 | 2,43 | 2,43 | 2,79 |
| 🟡 71 | 0,00 | 0,00 | 0,00 | 0,00 | 5,33 | 5,33 | 5,33 | 5,33 | 5,33 | 6,65 |
| 🟡 72 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 73 | 0,60 | 0,85 | 0,85 | 0,85 | 2,82 | 2,82 | 2,82 | 4,29 | 4,29 | 6,26 |
| 🟡 74 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,41 | 2,99 | 2,99 | 3,59 |
| 🟡 75 | 0,00 | 0,52 | 0,52 | 0,52 | 4,70 | 4,70 | 4,70 | 4,70 | 4,70 | 6,16 |
| 🟡 76 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 77 | 1,66 | 1,95 | 1,95 | 1,95 | 3,84 | 3,84 | 3,84 | 5,64 | 5,64 | 6,19 |
| 🟡 78 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 79 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 7,29 | 7,29 | 8,27 |
| 🟡 80 | 0,00 | 0,00 | 0,00 | 0,00 | 3,48 | 3,48 | 3,48 | 3,48 | 3,48 | 4,38 |
| 🟡 81 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 82 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,58 | 3,58 | 3,76 |
| 🟡 83 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟡 84 | 0,00 | 0,00 | 0,00 | 0,00 | 6,10 | 6,10 | 6,10 | 6,10 | 6,10 | 9,80 |
| 🟡 85 | 2,43 | 2,43 | 2,43 | 2,43 | 3,12 | 3,12 | 3,12 | 3,12 | 3,12 | 4,15 |
| 🟡 86 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 89 | 0,00 | 0,00 | 0,00 | 0,00 | 2,22 | 2,22 | 2,22 | 9,09 | 9,09 | 9,17 |
| 🟡 90 | 0,00 | 0,00 | 0,00 | 0,00 | 5,22 | 5,22 | 5,22 | 5,22 | 5,22 | 7,54 |
| 🟡 91 | 0,00 | 0,00 | 0,00 | 0,00 | 4,50 | 4,50 | 4,50 | 4,50 | 4,50 | 7,20 |
| 🟡 92 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 93 | 1,01 | 1,30 | 1,30 | 1,30 | 2,44 | 2,44 | 2,44 | 4,16 | 4,16 | 6,45 |
| 🟡 94 | 0,00 | 0,00 | 0,00 | 0,00 | 3,60 | 3,60 | 3,60 | 3,92 | 3,92 | 4,31 |
| 🔴 95 | 0,00 | 0,00 | — | — | — | — | — | — | — | — |
| 🟡 96 | 0,00 | 0,00 | 0,00 | 0,00 | 3,30 | 3,30 | 3,30 | 4,81 | 4,81 | 6,98 |
| 🟡 97 | 2,41 | 2,41 | 2,41 | 2,41 | 6,05 | 6,05 | 6,05 | 6,05 | 6,05 | 7,77 |
| 🟡 98 | 3,87 | 3,87 | 3,87 | 3,87 | 6,11 | 6,11 | 6,11 | 7,44 | 7,44 | 8,21 |
| 🟡 99 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟡 100 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 101 | 0,00 | 0,00 | 0,00 | 0,00 | 7,85 | 7,85 | 7,85 | 7,85 | 7,85 | 11,90 |
| 🟡 102 | 2,82 | 2,93 | 2,93 | 2,93 | 3,14 | 3,14 | 3,14 | 7,03 | 7,03 | 7,03 |
| 🟡 103 | 4,05 | 4,05 | 4,05 | 4,05 | 4,85 | 4,85 | 4,85 | 4,85 | 4,85 | 8,20 |
| 🔴 104 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟡 105 | 0,00 | 0,00 | 0,00 | 0,00 | 5,99 | 5,99 | 5,99 | 6,71 | 6,71 | 7,58 |
| 🟡 106 | 0,00 | 0,00 | 0,00 | 0,00 | 2,76 | 2,76 | 2,76 | 3,22 | 3,22 | 3,96 |
| 🟡 107 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 108 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 4,17 | 4,17 | 4,17 | 4,17 | 13,78 |
| 🟢 109 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 8,74 |
| 🟢 110 | 0,00 | 0,00 | 0,00 | 0,00 | 6,40 | 6,40 | 6,40 | 6,40 | 6,40 | 15,95 |
| 🟢 111 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 8,74 |
| 🟢 112 | 0,00 | 0,00 | 0,00 | 0,00 | 5,69 | 5,69 | 5,69 | 5,69 | 5,69 | 7,53 |
| 🟢 113 | 0,00 | 0,00 | 0,00 | 0,00 | 5,09 | 5,09 | 5,09 | 5,09 | 5,09 | 5,16 |
| 🟢 114 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 | 6,95 |
| 🟢 115 | 0,00 | 0,00 | 0,00 | 0,00 | 2,34 | 2,34 | 2,34 | 2,34 | 2,34 | 2,57 |
| 🟢 116 | 1,67 | 2,88 | 2,88 | 2,88 | 4,08 | 4,08 | 4,08 | 5,04 | 5,04 | 5,77 |
| 🟢 117 | 0,00 | 0,00 | 0,00 | 0,00 | 3,78 | 3,78 | 3,78 | 3,78 | 3,78 | 4,68 |
| 🟢 118 | 0,00 | 0,00 | 0,00 | 0,00 | 3,25 | 3,25 | 3,25 | 3,25 | 3,25 | 7,75 |
| 🟢 119 | 0,00 | 0,00 | 0,00 | 0,00 | 4,03 | 4,03 | 4,03 | 4,03 | 4,03 | 5,15 |
| 🟢 120 | 0,00 | 0,00 | 0,00 | 0,00 | 4,12 | 4,12 | 4,12 | 4,12 | 4,12 | 6,91 |
| 🟢 121 | 0,00 | 0,00 | 0,00 | 0,00 | 3,21 | 3,21 | 3,21 | 3,21 | 3,21 | 4,13 |
| 🟢 122 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 2,05 | 2,05 | 4,81 |
| 🔴 123 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟢 124 | 0,00 | 0,00 | 0,00 | 0,00 | 2,48 | 2,48 | 2,48 | 3,93 | 3,93 | 5,39 |
| 🔴 125 | 0,00 | 0,00 | 0,00 | 0,00 | — | — | — | — | — | — |
| 🟡 126 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 127 | 0,00 | 0,00 | 0,00 | 0,00 | 4,87 | 4,87 | 4,87 | 4,87 | 4,87 | 8,31 |
| 🟢 128 | 0,00 | 0,00 | 0,00 | 0,00 | 8,63 | 8,63 | 8,63 | 8,63 | 8,63 | 8,63 |
| 🟢 129 | 0,00 | 0,00 | 0,00 | 0,00 | 7,80 | 7,80 | 7,80 | 10,01 | 10,01 | 11,37 |
| 🟢 130 | 0,00 | 8,77 | 8,77 | 8,77 | 10,54 | 10,54 | 10,54 | 16,56 | 16,56 | 21,75 |
| 🟢 131 | 0,00 | 0,00 | 0,00 | 0,00 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 | 7,81 |
| 🟢 132 | 1,59 | 1,80 | 1,80 | 1,80 | 8,05 | 8,05 | 8,05 | 10,23 | 10,23 | 11,37 |
| 🟢 133 | 0,00 | 0,00 | 0,00 | 0,00 | 2,29 | 2,29 | 2,29 | 2,82 | 2,82 | 7,52 |
| 🟢 134 | 2,36 | 2,55 | 2,55 | 2,55 | 8,83 | 8,83 | 8,83 | 9,40 | 9,40 | 10,02 |
| 🟡 135 | 5,85 | 5,85 | 5,85 | 5,85 | 7,90 | 7,90 | 7,90 | 7,90 | 7,90 | 10,80 |
| 🟢 136 | 0,00 | 0,00 | 0,00 | 0,00 | 9,96 | 9,96 | 9,96 | 10,18 | 10,18 | 10,43 |
| 🟢 137 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 3,68 | 3,68 | 4,57 |
| 🟢 138 | 5,77 | 5,77 | 5,77 | 5,77 | 6,51 | 6,51 | 6,51 | 7,45 | 7,45 | 8,45 |
| 🟢 139 | 4,71 | 4,71 | 4,71 | 4,71 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,04 |
| 🟢 140 | 2,85 | 2,85 | 2,85 | 2,85 | 5,92 | 5,92 | 5,92 | 8,50 | 8,50 | 9,36 |
| 🟡 141 | 0,00 | 0,00 | 0,00 | 0,00 | 5,10 | 5,10 | 5,10 | 5,10 | 5,10 | 8,20 |
| 🟢 142 | 0,00 | 0,00 | 0,00 | 0,00 | 4,56 | 4,56 | 4,56 | 5,73 | 5,73 | 8,00 |
| 🟢 143 | 3,67 | 3,67 | 3,67 | 3,67 | 10,06 | 10,06 | 10,06 | 12,46 | 12,46 | 14,30 |
| 🟢 144 | 6,13 | 6,13 | 6,13 | 6,13 | 7,05 | 7,05 | 7,05 | 7,05 | 7,05 | 9,32 |
| 🟡 145 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,54 | 9,54 | 9,62 |
| 🟡 146 | 0,00 | 1,70 | 1,70 | 1,70 | 9,49 | 9,49 | 9,49 | 9,54 | 9,54 | 9,62 |
| 🟡 147 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 148 | 5,92 | 5,92 | 5,92 | 5,92 | 7,45 | 7,45 | 7,45 | 9,15 | 9,15 | 11,80 |
| 🟢 149 | 0,00 | 0,00 | 0,00 | 0,00 | 5,49 | 5,49 | 5,49 | 7,88 | 7,88 | 11,28 |
| 🟢 150 | 0,00 | 0,00 | 0,00 | 0,00 | 3,84 | 3,84 | 3,84 | 3,84 | 3,84 | 5,25 |
| 🟢 151 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 5,15 | 11,45 | 11,45 | 11,45 |
| 🟢 152 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟢 153 | 0,00 | 0,00 | 0,00 | 0,00 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 | 7,48 |
| 🟡 154 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 5,25 | 5,25 | 5,25 | 5,25 | 9,68 | 9,68 | 9,68 | 9,68 | 9,68 | 11,11 |
| 🟢 157 | 5,58 | 5,58 | 5,58 | 5,58 | 10,25 | 10,25 | 10,25 | 11,14 | 11,14 | 12,22 |
| 🟡 158 | 5,85 | 5,85 | 5,85 | 5,85 | 7,90 | 7,90 | 7,90 | 7,90 | 7,90 | 10,80 |
| 🟢 159 | 4,92 | 4,92 | 4,92 | 4,92 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 | 10,06 |
| 🟢 160 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 5,28 | 11,62 | 11,62 | 11,62 |
| 🟡 161 | 4,50 | 4,50 | 4,50 | 4,50 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,50 |
| 🟡 162 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 163 | 4,33 | 4,33 | 4,33 | 4,33 | 6,50 | 6,50 | 6,50 | 6,50 | 6,50 | 10,83 |
| 🟡 164 | 0,00 | 0,00 | 0,00 | 0,00 | 5,60 | 5,60 | 5,60 | 5,60 | 5,60 | 9,80 |
| 🟢 165 | 13,79 | 13,79 | 13,79 | 13,79 | 17,71 | 17,71 | 17,71 | 26,45 | 26,45 | 26,45 |
| 🟡 166 | 6,42 | 6,42 | 6,42 | 6,42 | 12,43 | 12,43 | 12,43 | 12,43 | 12,43 | 18,98 |
| 🟢 167 | 0,00 | 0,00 | 0,00 | 0,00 | 4,53 | 4,53 | 4,53 | 4,53 | 4,53 | 6,04 |
| 🟡 168 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 5,65 | 14,13 | 14,13 | 14,13 |
| 🟡 169 | 4,25 | 4,25 | 4,25 | 4,25 | 7,10 | 7,10 | 7,10 | 7,10 | 7,10 | 7,10 |
| 🟡 170 | 4,10 | 4,10 | 4,10 | 4,10 | 5,95 | 5,95 | 5,95 | 5,95 | 5,95 | 8,60 |
| 🟢 171 | 5,76 | 5,76 | 5,76 | 5,76 | 8,64 | 8,64 | 8,64 | 8,64 | 8,64 | 14,40 |
| 🟢 172 | 6,01 | 6,01 | 6,01 | 6,01 | 8,54 | 8,54 | 8,54 | 8,54 | 8,54 | 14,32 |
| 🟢 173 | 3,06 | 3,06 | 3,06 | 3,06 | 4,59 | 4,59 | 4,59 | 4,59 | 4,59 | 7,66 |
| 🟢 174 | 0,00 | 0,00 | 0,00 | 0,00 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 | 8,72 |
| 🟢 175 | 1,79 | 1,83 | 1,83 | 1,83 | 5,24 | 5,24 | 5,24 | 5,57 | 5,57 | 5,62 |
| 🟡 176 | 4,80 | 4,80 | 4,80 | 4,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 11,50 |
| 🟢 177 | 3,27 | 3,27 | 3,27 | 3,27 | 5,72 | 5,72 | 5,72 | 5,72 | 5,72 | 8,87 |
| 🟡 178 | 4,85 | 4,85 | 4,85 | 4,85 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 11,50 |
| 🟢 179 | 0,00 | 0,00 | 0,00 | 0,00 | 9,81 | 9,81 | 9,81 | 10,92 | 10,92 | 12,80 |
| 🟡 180 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 7,52 | 16,54 | 16,54 | 16,54 |
| 🟡 181 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 7,44 | 16,36 | 16,36 | 16,36 |
| 🟡 182 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 6,98 | 15,37 | 15,37 | 15,37 |
| 🟢 183 | 7,39 | 7,39 | 7,39 | 7,39 | 14,10 | 14,10 | 14,10 | 16,30 | 16,30 | 17,41 |
| 🟢 184 | 6,14 | 6,14 | 6,14 | 6,14 | 10,68 | 10,68 | 10,68 | 12,17 | 12,17 | 13,72 |
| 🟢 185 | 5,49 | 5,49 | 5,49 | 5,49 | 10,48 | 10,48 | 10,48 | 12,11 | 12,11 | 12,94 |
| 🟢 186 | 8,03 | 8,03 | 8,03 | 8,03 | 10,28 | 10,28 | 10,28 | 10,46 | 10,46 | 11,57 |
| 🟢 187 | 3,03 | 3,03 | 3,03 | 3,03 | 4,55 | 4,55 | 4,55 | 4,55 | 4,55 | 7,57 |

<!-- tabela: Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 2 de 3: 25–30 a 70–75 m³) -->
| Nº | 25–30 | 30–35 | 35–40 | 40–45 | 45–50 | 50–55 | 55–60 | 60–65 | 65–70 | 70–75 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 |
| 🟢 2 | 15,46 | 15,97 | 15,97 | 15,92 | 15,92 | 15,14 | 15,14 | 15,14 | 15,14 | 15,14 |
| 🟢 3 | 18,04 | 18,63 | 18,63 | 18,86 | 18,86 | 18,99 | 18,99 | 18,99 | 18,99 | 18,99 |
| 🟡 4 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 5 | 10,14 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 16,48 | 16,48 | 16,48 |
| 🟡 6 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 7 | 4,01 | 5,64 | 5,64 | 5,64 | 5,64 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 8 | 15,34 | 15,85 | 15,85 | 15,85 | 15,85 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟡 9 | 15,67 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 10 | 10,77 | 13,68 | 13,68 | 13,68 | 13,68 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟡 11 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 12 | 9,87 | 11,82 | 11,82 | 11,82 | 11,82 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟢 13 | 8,45 | 9,74 | 9,74 | 9,74 | 9,74 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 14 | 7,64 | 8,79 | 8,79 | 8,79 | 8,79 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 15 | 14,81 | 22,22 | 22,22 | 22,22 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 16 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 17 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 18 | 9,32 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 19 | 17,17 | 17,72 | 17,72 | 17,96 | 17,96 | 18,07 | 18,07 | 18,07 | 18,07 | 18,07 |
| 🟡 20 | 19,14 | 19,14 | 19,14 | 19,14 | 19,14 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟡 21 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 22 | 8,55 | 8,55 | 8,55 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 |
| 🟢 23 | 9,77 | 11,24 | 11,24 | 11,24 | 11,24 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟢 24 | 5,74 | 6,13 | 6,13 | 6,13 | 6,13 | 6,88 | 6,88 | 6,88 | 6,88 | 6,88 |
| 🟡 25 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 26 | 6,63 | 6,63 | 6,63 | 6,63 | 6,63 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 27 | 13,18 | 13,18 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 28 | 8,42 | 11,59 | 11,59 | 11,59 | 11,59 | 13,74 | 13,74 | 13,74 | 13,74 | 13,74 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 13,66 | 13,66 | 13,66 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟡 31 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 32 | 9,38 | 10,58 | 10,58 | 14,66 | 14,66 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 33 | 5,06 | 6,58 | 6,58 | 6,58 | 6,58 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 |
| 🟢 34 | 5,83 | 7,64 | 7,64 | 9,07 | 9,07 | 10,82 | 10,82 | 10,82 | 10,82 | 10,82 |
| 🟢 35 | 10,77 | 10,77 | 10,77 | 10,77 | 10,77 | 15,55 | 15,55 | 15,55 | 15,55 | 15,55 |
| 🟢 36 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 7,77 | 7,77 | 10,69 | 10,69 | 10,69 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 |
| 🟡 41 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 42 | 6,84 | 8,10 | 8,10 | 8,94 | 8,94 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 43 | 4,89 | 5,26 | 5,26 | 5,64 | 5,64 | 6,01 | 6,01 | 6,01 | 6,01 | 6,01 |
| 🟡 44 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 45 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 46 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 47 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 6,74 | 8,37 | 8,37 | 9,93 | 9,93 | 11,47 | 11,47 | 13,08 | 13,08 | 14,61 |
| 🟡 50 | 8,20 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 51 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 52 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟡 53 | 16,82 | 18,49 | 18,49 | 20,28 | 20,28 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 54 | 6,46 | 8,82 | 8,82 | 8,82 | 8,82 | 12,69 | 12,69 | 12,69 | 12,69 | 12,69 |
| 🟢 55 | 16,75 | 23,49 | 23,49 | 23,49 | 23,49 | 32,67 | 32,67 | 32,67 | 32,67 | 32,67 |
| 🟢 56 | 7,77 | 10,04 | 10,04 | 10,04 | 10,04 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 57 | 3,34 | 3,70 | 3,70 | 5,06 | 5,06 | 6,46 | 6,46 | 6,46 | 6,46 | 6,46 |
| 🟡 58 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 59 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 61 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 62 | 42,88 | 42,88 | 51,46 | 51,46 | 63,18 | 63,18 | 80,25 | 80,25 | 91,26 | 91,26 |
| 🟢 63 | 6,24 | 8,41 | 8,41 | 8,41 | 8,41 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 64 | 15,37 | 20,94 | 20,94 | 20,94 | 41,88 | 41,88 | 41,88 | 55,84 | 55,84 | 55,84 |
| 🟡 65 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 66 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 67 | 9,77 | 11,24 | 11,24 | 11,24 | 11,24 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟡 68 | 13,13 | 13,13 | 13,13 | 13,13 | 13,13 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟡 69 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 70 | 3,21 | 3,69 | 3,69 | 3,69 | 3,69 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟡 71 | 6,65 | 9,53 | 9,53 | 14,27 | 14,27 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 72 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 73 | 8,23 | 9,71 | 9,71 | 9,96 | 9,96 | 10,01 | 10,01 | 10,01 | 10,01 | 10,01 |
| 🟡 74 | 4,11 | 4,66 | 5,33 | 6,07 | 6,92 | 7,88 | 7,88 | 7,88 | 7,88 | 8,99 |
| 🟡 75 | 6,16 | 6,83 | 6,83 | 9,65 | 9,65 | 9,65 | 9,65 | 11,45 | 11,45 | 11,45 |
| 🟡 76 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 77 | 6,83 | 7,49 | 7,49 | 8,29 | 8,29 | 9,09 | 9,09 | 9,09 | 9,09 | 9,09 |
| 🟡 78 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 79 | 8,27 | 8,37 | 8,50 | 8,67 | 8,67 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟡 80 | 4,38 | 7,21 | 7,21 | 8,37 | 8,37 | 11,88 | 11,88 | 13,03 | 13,03 | 14,36 |
| 🟡 81 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 82 | 3,93 | 4,31 | 4,31 | 4,51 | 4,51 | 4,72 | 4,72 | 4,72 | 4,72 | 4,72 |
| 🟡 83 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 84 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟡 85 | 5,96 | 5,96 | 7,03 | 7,03 | 7,03 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟡 86 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 89 | 9,17 | 9,56 | 9,56 | 10,05 | 10,05 | 10,66 | 10,66 | 10,66 | 10,66 | 10,66 |
| 🟡 90 | 7,54 | 9,28 | 9,28 | 11,59 | 11,59 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 91 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 92 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 93 | 8,17 | 9,88 | 9,88 | 10,17 | 10,17 | 10,23 | 10,23 | 10,23 | 10,23 | 10,23 |
| 🟡 94 | 4,77 | 5,27 | 6,34 | 8,07 | 8,07 | 8,07 | 8,07 | 10,21 | 10,21 | 10,21 |
| 🔴 95 | — | — | — | — | — | — | — | — | — | — |
| 🟡 96 | 7,69 | 8,05 | 8,05 | 8,47 | 8,47 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟡 97 | 7,77 | 9,81 | 9,81 | 11,65 | 11,65 | 12,78 | 12,78 | 14,16 | 14,16 | 14,16 |
| 🟡 98 | 8,21 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 99 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 100 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 101 | 11,90 | 11,90 | 11,90 | 11,90 | 11,90 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 102 | 7,03 | 7,03 | 7,03 | 9,74 | 9,74 | 9,74 | 9,74 | 10,33 | 10,33 | 10,33 |
| 🟡 103 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🔴 104 | — | — | — | — | — | — | — | — | — | — |
| 🟡 105 | 8,64 | 9,94 | 11,54 | 13,50 | 13,50 | 15,91 | 15,91 | 15,91 | 15,91 | 15,91 |
| 🟡 106 | 4,73 | 5,65 | 6,85 | 6,85 | 8,21 | 8,21 | 8,21 | 9,78 | 9,78 | 9,78 |
| 🟡 107 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 108 | 13,78 | 13,78 | 13,78 | 13,78 | 13,78 | 20,37 | 20,37 | 20,37 | 20,37 | 20,37 |
| 🟢 109 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 110 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 111 | 8,74 | 8,74 | 8,74 | 8,74 | 8,74 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 112 | 7,53 | 7,53 | 7,53 | 7,53 | 7,53 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 113 | 5,16 | 7,09 | 7,09 | 7,09 | 7,09 | 11,82 | 11,82 | 11,93 | 11,93 | 12,03 |
| 🟢 114 | 6,95 | 6,95 | 6,95 | 6,95 | 6,95 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 115 | 2,57 | 2,81 | 2,81 | 3,10 | 3,10 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 116 | 6,49 | 6,97 | 6,97 | 7,45 | 7,45 | 7,69 | 7,69 | 7,69 | 7,69 | 7,69 |
| 🟢 117 | 4,68 | 6,43 | 6,43 | 7,25 | 7,25 | 10,21 | 10,21 | 10,21 | 10,21 | 15,08 |
| 🟢 118 | 7,79 | 8,34 | 8,34 | 9,77 | 9,77 | 11,47 | 11,47 | 11,47 | 11,47 | 11,47 |
| 🟢 119 | 5,15 | 6,62 | 6,62 | 6,90 | 6,90 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟢 120 | 6,91 | 6,91 | 6,91 | 6,91 | 6,91 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 121 | 4,13 | 5,58 | 5,58 | 5,58 | 5,58 | 7,82 | 7,82 | 7,82 | 7,82 | 7,82 |
| 🟢 122 | 5,39 | 5,83 | 5,93 | 6,46 | 6,46 | 7,02 | 7,02 | 7,67 | 7,67 | 9,92 |
| 🔴 123 | — | — | — | — | — | — | — | — | — | — |
| 🟢 124 | 7,18 | 9,33 | 9,33 | 12,57 | 12,57 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🔴 125 | — | — | — | — | — | — | — | — | — | — |
| 🟡 126 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 127 | 8,31 | 8,25 | 8,25 | 8,25 | 8,25 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 |
| 🟢 128 | 8,63 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 129 | 12,54 | 12,54 | 12,54 | 12,54 | 12,54 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 130 | 21,75 | 22,66 | 22,66 | 22,66 | 22,66 | 24,36 | 24,36 | 24,36 | 24,36 | 24,36 |
| 🟢 131 | 10,30 | 10,30 | 10,30 | 12,49 | 12,49 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 132 | 12,49 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 133 | 7,52 | 7,58 | 7,58 | 9,34 | 9,34 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 134 | 10,34 | 10,34 | 10,34 | 10,34 | 10,34 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 |
| 🟡 135 | 10,80 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 136 | 12,82 | 13,65 | 13,65 | 13,65 | 13,65 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 137 | 5,46 | 6,35 | 7,24 | 8,12 | 9,01 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 138 | 9,54 | 10,89 | 10,89 | 12,33 | 12,33 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 139 | 10,04 | 10,04 | 10,04 | 10,04 | 10,04 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 140 | 9,36 | 9,98 | 9,98 | 9,98 | 9,98 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟡 141 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 142 | 8,00 | 8,00 | 11,63 | 11,63 | 11,63 | 16,92 | 16,92 | 16,92 | 16,92 | 16,92 |
| 🟢 143 | 14,30 | 14,30 | 14,30 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 |
| 🟢 144 | 9,32 | 10,74 | 10,74 | 10,74 | 10,74 | 12,33 | 12,33 | 12,33 | 12,33 | 12,33 |
| 🟡 145 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 146 | 9,62 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 147 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 148 | 11,80 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 |
| 🟢 149 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 |
| 🟢 150 | 5,25 | 6,99 | 6,99 | 8,64 | 8,64 | 13,14 | 13,14 | 13,14 | 13,14 | 13,14 |
| 🟢 151 | 11,45 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 152 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 153 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 154 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 11,11 | 13,59 | 13,59 | 13,59 | 13,59 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 157 | 12,22 | 12,64 | 12,64 | 13,29 | 13,29 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 158 | 10,80 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 159 | 10,06 | 12,31 | 12,31 | 12,31 | 12,31 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 160 | 11,62 | 15,85 | 15,85 | 15,85 | 31,70 | 31,70 | 31,70 | 42,27 | 42,27 | 42,27 |
| 🟡 161 | 10,50 | 10,50 | 10,50 | 10,50 | 10,50 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 162 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 163 | 10,83 | 14,29 | 14,29 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟡 164 | 9,80 | 9,80 | 9,80 | 9,80 | 9,80 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 165 | 33,10 | 33,10 | 42,43 | 42,43 | 51,93 | 51,93 | 66,02 | 66,02 | 80,27 | 80,27 |
| 🟡 166 | 18,98 | 25,86 | 25,86 | 29,84 | 29,84 | 29,84 | 29,84 | 34,02 | 34,02 | 34,02 |
| 🟢 167 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 168 | 14,13 | 17,53 | 17,53 | 17,53 | 33,92 | 33,92 | 33,92 | 45,23 | 45,23 | 45,23 |
| 🟡 169 | 7,10 | 11,80 | 11,80 | 11,80 | 11,80 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 170 | 8,60 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 171 | 14,40 | 19,01 | 19,01 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 172 | 14,32 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 173 | 7,66 | 11,48 | 11,48 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 174 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 175 | 5,62 | 5,62 | 5,62 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟡 176 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 177 | 8,87 | 11,37 | 11,37 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 |
| 🟡 178 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 179 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 180 | 16,54 | 22,56 | 22,56 | 22,56 | 45,12 | 45,12 | 45,12 | 60,16 | 60,16 | 60,16 |
| 🟡 181 | 16,36 | 22,31 | 22,31 | 22,31 | 44,62 | 44,62 | 44,62 | 59,49 | 59,49 | 59,49 |
| 🟡 182 | 15,37 | 20,94 | 20,94 | 20,94 | 41,88 | 41,88 | 41,88 | 55,84 | 55,84 | 55,84 |
| 🟢 183 | 17,41 | 17,98 | 17,98 | 18,21 | 18,21 | 18,33 | 18,33 | 18,33 | 18,33 | 18,33 |
| 🟢 184 | 13,72 | 14,83 | 14,83 | 15,57 | 15,57 | 15,95 | 15,95 | 15,95 | 15,95 | 15,95 |
| 🟢 185 | 12,94 | 13,36 | 13,36 | 13,54 | 13,54 | 13,62 | 13,62 | 13,62 | 13,62 | 13,62 |
| 🟢 186 | 14,23 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 187 | 7,57 | 9,99 | 9,99 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

<!-- tabela: Preço da água por intervalo de consumo mensal, em R$/m³, por município e categoria (parte 3 de 3: 75–80 a 5.000 m³) -->
| Nº | 75–80 | 80–90 | 90–99 | 99–100 | 100–150 | 150–200 | 200–300 | 300–500 | 500–5.000 | > 5.000 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 🟢 1 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟢 2 | 15,14 | 15,14 | 16,96 | 16,96 | 16,96 | 19,88 | 19,88 | 19,88 | 19,88 | 19,88 |
| 🟢 3 | 18,99 | 18,99 | 19,09 | 19,09 | 19,09 | 19,10 | 19,10 | 19,10 | 19,10 | 19,10 |
| 🟡 4 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟢 5 | 16,48 | 16,48 | 16,48 | 16,48 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 | 20,60 |
| 🟡 6 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 7 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 | 7,57 |
| 🟢 8 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 | 16,18 |
| 🟡 9 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 | 17,50 |
| 🟢 10 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 | 21,48 |
| 🟡 11 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 | 8,90 |
| 🟢 12 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟢 13 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 14 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 15 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 | 28,88 |
| 🟡 16 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 17 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 | 28,77 |
| 🟢 18 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 | 12,67 |
| 🟢 19 | 18,07 | 18,07 | 18,18 | 18,18 | 18,18 | 18,19 | 18,19 | 18,19 | 18,19 | 18,19 |
| 🟡 20 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 | 24,08 |
| 🟡 21 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟢 22 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 | 11,16 |
| 🟢 23 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟢 24 | 6,88 | 6,88 | 6,88 | 6,88 | 7,03 | 7,03 | 7,28 | 7,28 | 7,28 | 7,28 |
| 🟡 25 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 26 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 | 7,94 |
| 🟢 27 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 | 13,63 |
| 🟢 28 | 13,74 | 13,74 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 | 26,40 |
| 🟢 29 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 | 9,23 |
| 🟡 30 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 | 16,54 |
| 🟡 31 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 32 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 | 19,04 |
| 🟢 33 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 | 9,31 |
| 🟢 34 | 10,82 | 10,82 | 10,82 | 10,82 | 12,76 | 12,76 | 15,21 | 15,21 | 15,21 | 15,21 |
| 🟢 35 | 15,55 | 15,55 | 15,55 | 15,55 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 | 17,91 |
| 🟢 36 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 | 3,49 |
| 🟢 37 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 | 3,23 |
| 🟢 38 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 | 11,01 |
| 🟡 39 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 | 2,37 |
| 🟢 40 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 | 22,18 |
| 🟡 41 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 | 6,80 |
| 🟢 42 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 | 11,17 |
| 🟢 43 | 6,39 | 6,39 | 6,39 | 6,39 | 6,76 | 6,76 | 6,76 | 6,76 | 6,76 | 6,76 |
| 🟡 44 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 45 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 | 19,80 |
| 🟡 46 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 47 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 48 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 | 5,50 |
| 🟢 49 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 | 14,61 |
| 🟡 50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 | 11,50 |
| 🟡 51 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 52 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 | 7,83 |
| 🟡 53 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 | 24,40 |
| 🟢 54 | 12,69 | 12,69 | 12,69 | 12,69 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 | 16,79 |
| 🟢 55 | 32,67 | 32,67 | 32,67 | 32,67 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 | 42,08 |
| 🟢 56 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 | 15,77 |
| 🟡 57 | 6,46 | 6,46 | 6,46 | 6,46 | 8,12 | 8,12 | 9,62 | 9,62 | 9,62 | 9,62 |
| 🟡 58 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 59 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 60 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 61 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟢 62 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 | 91,26 |
| 🟢 63 | 10,20 | 10,20 | 10,20 | 10,20 | 11,63 | 11,63 | 11,63 | 11,63 | 11,63 | 11,63 |
| 🟡 64 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 |
| 🟡 65 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 66 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 67 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 | 12,36 |
| 🟡 68 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 | 16,09 |
| 🟡 69 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 70 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 | 4,06 |
| 🟡 71 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 | 15,67 |
| 🟡 72 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 73 | 10,06 | 10,06 | 10,06 | 10,06 | 10,11 | 10,11 | 10,16 | 10,16 | 10,16 | 10,16 |
| 🟡 74 | 8,99 | 8,99 | 8,99 | 8,99 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 | 10,22 |
| 🟡 75 | 11,45 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 | 23,32 |
| 🟡 76 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 77 | 9,99 | 9,99 | 9,99 | 9,99 | 10,99 | 10,99 | 12,09 | 12,09 | 12,09 | 12,09 |
| 🟡 78 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 79 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 | 10,44 |
| 🟡 80 | 14,36 | 15,93 | 17,47 | 17,47 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 | 19,22 |
| 🟡 81 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 82 | 5,11 | 5,11 | 5,11 | 5,11 | 5,54 | 5,54 | 5,72 | 5,72 | 5,72 | 5,72 |
| 🟡 83 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟡 84 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 | 14,80 |
| 🟡 85 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟡 86 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 87 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| 🟡 88 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 89 | 11,67 | 11,67 | 11,67 | 11,67 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 | 12,75 |
| 🟡 90 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 | 13,92 |
| 🟡 91 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 | 7,20 |
| 🟡 92 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 93 | 10,29 | 10,29 | 10,29 | 10,29 | 10,34 | 10,34 | 10,40 | 10,40 | 10,40 | 10,40 |
| 🟡 94 | 10,21 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 | 13,58 |
| 🔴 95 | — | — | — | — | — | — | — | — | — | — |
| 🟡 96 | 9,12 | 9,12 | 9,12 | 9,12 | 10,95 | 10,95 | 13,13 | 15,75 | 15,75 | 15,75 |
| 🟡 97 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 | 14,16 |
| 🟡 98 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 | 9,40 |
| 🟡 99 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟡 100 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 101 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 | 16,50 |
| 🟡 102 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,33 | 10,95 | 10,95 | 10,95 |
| 🟡 103 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 | 12,50 |
| 🔴 104 | — | — | — | — | — | — | — | — | — | — |
| 🟡 105 | 15,91 | 15,91 | 15,91 | 15,91 | 17,18 | 17,18 | 17,18 | 17,18 | 17,18 | 17,18 |
| 🟡 106 | 9,78 | 9,78 | 9,78 | 9,78 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 | 11,75 |
| 🟡 107 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 108 | 20,37 | 20,37 | 20,37 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 | 25,49 |
| 🟢 109 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 110 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 | 17,57 |
| 🟢 111 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 | 10,46 |
| 🟢 112 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟢 113 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 | 12,03 |
| 🟢 114 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 | 8,32 |
| 🟢 115 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 | 3,46 |
| 🟢 116 | 7,93 | 7,93 | 7,93 | 7,93 | 8,17 | 8,17 | 8,41 | 8,41 | 8,41 | 8,41 |
| 🟢 117 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 | 15,08 |
| 🟢 118 | 11,47 | 11,47 | 11,47 | 11,47 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 | 13,46 |
| 🟢 119 | 9,23 | 9,23 | 9,23 | 9,23 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 | 10,87 |
| 🟢 120 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 | 11,31 |
| 🟢 121 | 7,82 | 7,82 | 7,82 | 7,82 | 11,34 | 11,34 | 11,34 | 11,34 | 17,02 | 26,39 |
| 🟢 122 | 9,92 | 12,03 | 12,81 | 12,81 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 | 13,20 |
| 🔴 123 | — | — | — | — | — | — | — | — | — | — |
| 🟢 124 | 15,77 | 19,02 | 19,02 | 19,02 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 | 21,87 |
| 🔴 125 | — | — | — | — | — | — | — | — | — | — |
| 🟡 126 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 127 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 | 9,94 |
| 🟢 128 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 | 11,00 |
| 🟢 129 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 | 13,18 |
| 🟢 130 | 24,36 | 24,36 | 24,36 | 24,36 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 | 28,35 |
| 🟢 131 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 | 14,31 |
| 🟢 132 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 | 14,79 |
| 🟢 133 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 | 10,74 |
| 🟢 134 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 | 10,51 |
| 🟡 135 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 136 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 | 20,94 |
| 🟢 137 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 | 9,90 |
| 🟢 138 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 | 14,06 |
| 🟢 139 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 | 11,91 |
| 🟢 140 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 | 10,41 |
| 🟡 141 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 | 8,20 |
| 🟢 142 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 | 22,82 |
| 🟢 143 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 | 22,98 |
| 🟢 144 | 12,33 | 12,33 | 12,33 | 12,33 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 | 14,18 |
| 🟡 145 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 146 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 | 16,28 |
| 🟡 147 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 148 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 | 15,60 |
| 🟢 149 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 | 11,28 |
| 🟢 150 | 13,14 | 13,14 | 13,14 | 13,14 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 | 14,59 |
| 🟢 151 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 | 16,03 |
| 🟢 152 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 | 10,38 |
| 🟢 153 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 | 10,20 |
| 🟡 154 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 155 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 | 6,74 |
| 🟢 156 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 157 | 13,92 | 13,92 | 13,96 | 13,96 | 13,96 | 13,97 | 13,97 | 13,97 | 13,97 | 13,97 |
| 🟡 158 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 | 14,20 |
| 🟢 159 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 | 16,29 |
| 🟢 160 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 | 42,27 |
| 🟡 161 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 | 15,00 |
| 🟡 162 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 163 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 | 22,95 |
| 🟡 164 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 | 14,50 |
| 🟢 165 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 | 80,27 |
| 🟡 166 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 | 34,02 |
| 🟢 167 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 | 6,04 |
| 🟡 168 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 | 45,23 |
| 🟡 169 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 | 15,50 |
| 🟡 170 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 | 12,00 |
| 🟢 171 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 | 26,90 |
| 🟢 172 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 | 17,93 |
| 🟢 173 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 | 18,04 |
| 🟢 174 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 | 15,06 |
| 🟢 175 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 | 10,37 |
| 🟡 176 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 | 17,20 |
| 🟢 177 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 | 15,88 |
| 🟡 178 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 | 16,80 |
| 🟢 179 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 | 12,80 |
| 🟡 180 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 | 60,16 |
| 🟡 181 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 | 59,49 |
| 🟡 182 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 | 55,84 |
| 🟢 183 | 18,33 | 18,33 | 18,44 | 18,44 | 18,44 | 18,45 | 18,45 | 18,45 | 18,45 | 18,45 |
| 🟢 184 | 15,95 | 15,95 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 | 16,01 |
| 🟢 185 | 13,62 | 13,62 | 13,70 | 13,70 | 13,70 | 13,71 | 13,71 | 13,71 | 13,71 | 13,71 |
| 🟢 186 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 | 20,40 |
| 🟢 187 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 | 16,04 |

A segunda tabela traz, para as mesmas linhas, a vigência declarada pela fonte e a data em que a página oficial foi verificada pela última vez pela rotina de monitoramento da base. Linha sem data é fonte que a rotina ainda não monitora.

<!-- tabela: Vigência e última verificação da fonte de cada estrutura tarifária, com a situação do dado -->
| Nº | Vigência declarada | Fonte verificada em | Situação |
| ---: | :--- | :--- | :--- |
| 🟢 1 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 2 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 3 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟡 4 | Resoluções ARSP / Concessões ES | 31/08/2026 | a confirmar |
| 🟢 5 | Contas emitidas desde julho de 2026 | 31/08/2026 | auditada |
| 🟡 6 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 7 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 8 | Tabela vigente desde 30/08/2025; ainda vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 9 | Vigente desde 05/12/2025 | 31/08/2026 | a confirmar |
| 🟢 10 | Água vigente desde 05/01/2024; relação esgoto/água confirmada em 19/01/2026 | 31/08/2026 | auditada |
| 🟡 11 | Estrutura Tarifária CAER Oficial | 31/08/2026 | a confirmar |
| 🟢 12 | Vigente em 2025/2026 | 31/08/2026 | auditada |
| 🟢 13 | Vigente desde 01/04/2025 | 31/08/2026 | auditada |
| 🟢 14 | Vigente desde 01/07/2025 | 31/08/2026 | auditada |
| 🟢 15 | Resolução ADASA nº 70 | 31/08/2026 | auditada |
| 🟡 16 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 17 | Vigente desde 05/11/2025 | 31/08/2026 | a confirmar |
| 🟢 18 | Vigente desde 30/06/2025 | 31/08/2026 | auditada |
| 🟢 19 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟡 20 | Vigente desde 01/04/2026 | 31/08/2026 | a confirmar |
| 🟡 21 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟢 22 | Res. ARISB-MG 332/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 23 | Tabela aplicável desde 01/08/2025 e vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 24 | Vigente desde março de 2026 | 31/08/2026 | auditada |
| 🟡 25 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 26 | Vigente desde maio de 2026 | 31/08/2026 | auditada |
| 🟢 27 | 01/03/2026 | 31/08/2026 | auditada |
| 🟢 28 | Resolução ARPE nº 289 | 31/08/2026 | auditada |
| 🟢 29 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 30 | 22/01/2026–21/01/2027 | 31/08/2026 | a confirmar |
| 🟡 31 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟢 32 | Resoluções ARCON-PA 2024-2026 | 31/08/2026 | auditada |
| 🟢 33 | Vigente de 30/08/2025 a 29/08/2026 | 31/08/2026 | auditada |
| 🟢 34 | Vigente desde novembro de 2025 | 31/08/2026 | auditada |
| 🟢 35 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 36 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 37 | Resolução nº 02, de 11/02/2026 | 31/08/2026 | auditada |
| 🟢 38 | Res. 664/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 39 | Referência vigente pesquisada em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 40 | Vigente desde abril de 2023; último ato listado pela ARES-PCJ | 31/08/2026 | auditada |
| 🟡 41 | Estrutura Tarifária DAE/VG | 31/08/2026 | a confirmar |
| 🟢 42 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 43 | Vigente desde 01/03/2026 | 31/08/2026 | auditada |
| 🟡 44 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 45 | Resolução ARSAL Nº 233 | 31/08/2026 | a confirmar |
| 🟡 46 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 47 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 48 | 2026 vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 49 | Vigente desde 01/06/2026 | 31/08/2026 | auditada |
| 🟡 50 | Estrutura Tarifária DMAE / ARESAN | 31/08/2026 | a confirmar |
| 🟡 51 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 52 | Vigente desde 04/05/2026 | 31/08/2026 | auditada |
| 🟡 53 | Vigente desde 20/07/2026 | 31/08/2026 | a confirmar |
| 🟢 54 | Desde 01/03/2026 | 31/08/2026 | auditada |
| 🟢 55 | Vigente desde 01/08/2025 | 31/08/2026 | auditada |
| 🟢 56 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 57 | Desde 03/2026 | 31/08/2026 | a confirmar |
| 🟡 58 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 59 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 60 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 61 | Estrutura Municipal Vigente | — | a confirmar |
| 🟢 62 | Vigente desde 01/12/2025 | 31/08/2026 | auditada |
| 🟢 63 | Vigente desde abril de 2026 | 31/08/2026 | auditada |
| 🟡 64 | Deliberação AGENERSA | — | a confirmar |
| 🟡 65 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 66 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 67 | SAAE: efeitos desde 09/06/2026; Res. ARSP 103/2026 | 31/08/2026 | a confirmar |
| 🟡 68 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 69 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 70 | Vigente desde 28/12/2025 | 31/08/2026 | a confirmar |
| 🟡 71 | Res. 704/2026; desde 07/2026 | 31/08/2026 | a confirmar |
| 🟡 72 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 73 | Res. ARISB-MG 361/2025; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 74 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 75 | Res. ARES-PCJ 699/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 76 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 77 | Vigente desde agosto de 2026 | 31/08/2026 | a confirmar |
| 🟡 78 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 79 | Vigente desde junho de 2026 | 31/08/2026 | a confirmar |
| 🟡 80 | Res. 713/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 81 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 82 | Res. ARISB-MG 373/2025; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 83 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟡 84 | Resoluções ARSP / Concessões ES | 31/08/2026 | a confirmar |
| 🟡 85 | Tabela oficial de 2026 | 31/08/2026 | a confirmar |
| 🟡 86 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 87 | Desde 01/2026 | 31/08/2026 | a confirmar |
| 🟡 88 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 89 | Vigente desde julho de 2026 | 31/08/2026 | a confirmar |
| 🟡 90 | Vigente desde abril de 2025; mantida como vigente pelo SAAE em 24/08/2026 | 31/08/2026 | a confirmar |
| 🟡 91 | Estrutura Municipal Vigente | 31/08/2026 | a confirmar |
| 🟡 92 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 93 | Res. ARISB-MG 367/2025 c/ correção 377/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 94 | Vigente desde novembro de 2025 | — | a confirmar |
| 🔴 95 | Vigente desde 03/03/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 96 | Res. 703/2026; desde 07/2026 | 31/08/2026 | a confirmar |
| 🟡 97 | Vigente desde setembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 98 | 26/02/2026–25/02/2027; Res. ARSP 098/2026 | 31/08/2026 | a confirmar |
| 🟡 99 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟡 100 | Regulação Oficial | — | a confirmar |
| 🟡 101 | Resoluções AGERO / CAERD | 31/08/2026 | a confirmar |
| 🟡 102 | Resolução ARIS-MG nº 227/2026 | 31/08/2026 | a confirmar |
| 🟡 103 | Decreto Municipal | — | a confirmar |
| 🔴 104 | Desde 03/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 105 | Vigente desde setembro de 2025; tabela sucessora ainda não aplicável na data de corte | 31/08/2026 | a confirmar |
| 🟡 106 | Res. 696/2026; vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 107 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 108 | Res. 697/2026; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 109 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 110 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 111 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 112 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 113 | Res. 659/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 114 | Desde 01/01/2026 | 31/08/2026 | auditada |
| 🟢 115 | Res. ARISB-MG 368/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 116 | Res. ARISB-MG 371/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 117 | Resolução ARES-PCJ nº 687/2026 | 31/08/2026 | auditada |
| 🟢 118 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟢 119 | Tabela da Resolução ARES-PCJ nº 680/2025 vigente em 2026 | 31/08/2026 | auditada |
| 🟢 120 | Vigente desde 15/03/2026 | 31/08/2026 | auditada |
| 🟢 121 | Vigente desde dezembro de 2025 | 31/08/2026 | auditada |
| 🟢 122 | Tabela da Resolução ARES-PCJ nº 678/2025 vigente em 2026 | 31/08/2026 | auditada |
| 🔴 123 | Res. 695/2026; vigente em 19/08/2026 | 31/08/2026 | estrutura incompleta |
| 🟢 124 | Vigente desde maio de 2026 | 31/08/2026 | auditada |
| 🔴 125 | Res. 694/2026; vigente em 19/08/2026 | 31/08/2026 | estrutura incompleta |
| 🟡 126 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 127 | Vigente no exercício de 2026 | 31/08/2026 | auditada |
| 🟢 128 | Água desde 01/01/2026; esgoto desde 01/04/2026 | 31/08/2026 | auditada |
| 🟢 129 | Tarifa de água vigente desde 17/05/2026; esgoto ainda não faturado no cenário atual | 31/08/2026 | auditada |
| 🟢 130 | Vigente desde 01/07/2026 | 31/08/2026 | auditada |
| 🟢 131 | Tarifa de água vigente desde 01/07/2026; adicional de esgoto condicionado à unidade atendida | 31/08/2026 | auditada |
| 🟢 132 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟢 133 | Resolução ARES-PCJ nº 686/2026 | 31/08/2026 | auditada |
| 🟢 134 | 01/08/2026 | 31/08/2026 | auditada |
| 🟡 135 | Resoluções AGER-MT / Concessões | 31/08/2026 | a confirmar |
| 🟢 136 | Vigente desde fevereiro de 2026 | 31/08/2026 | auditada |
| 🟢 137 | Vigente desde julho de 2025 | 31/08/2026 | auditada |
| 🟢 138 | Desde 01/04/2026 | 31/08/2026 | auditada |
| 🟢 139 | Res. ARSESP 1787/2026; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟢 140 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 141 | Estrutura Tarifária SANEAR | 31/08/2026 | a confirmar |
| 🟢 142 | Vigente desde agosto de 2026 | 31/08/2026 | auditada |
| 🟢 143 | Tabela jan/2026 - Res. ARISB-MG 369/2025 | 31/08/2026 | auditada |
| 🟢 144 | Vigente de 07/2026 a 06/2027 | — | auditada |
| 🟡 145 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 146 | Vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟡 147 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 148 | Portaria AGEMS 315 / SANESUL | 31/08/2026 | auditada |
| 🟢 149 | Res. 638/2025 adotada no corte 19/08/2026 | 31/08/2026 | auditada |
| 🟢 150 | Vigente em agosto de 2026, após o prazo legal mínimo | 31/08/2026 | auditada |
| 🟢 151 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟢 152 | Vigente para faturas com vencimento desde 05/10/2025 | 31/08/2026 | auditada |
| 🟢 153 | Tabela tarifária do exercício de 2026 | 31/08/2026 | auditada |
| 🟡 154 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 155 | 2026 vigente em 19/08/2026 | 31/08/2026 | a confirmar |
| 🟢 156 | Vigente de 01/05/2026 a 30/04/2027 | 31/08/2026 | auditada |
| 🟢 157 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟡 158 | Resoluções AGER-MT / Concessões | 31/08/2026 | a confirmar |
| 🟢 159 | Vigente desde 20/03/2025 | 31/08/2026 | auditada |
| 🟢 160 | Vigente desde 06/01/2026 | 31/08/2026 | auditada |
| 🟡 161 | Regulação Oficial | 31/08/2026 | a confirmar |
| 🟡 162 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 163 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟡 164 | Resoluções ARES-PCJ / ARSESP | 31/08/2026 | a confirmar |
| 🟢 165 | Vigente desde 01/12/2025 | 31/08/2026 | auditada |
| 🟡 166 | Vigente desde fevereiro de 2026 | 31/08/2026 | a confirmar |
| 🟢 167 | Res. 665/2025; vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 168 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 169 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟡 170 | Resoluções ARISB-MG / Prestadores Locais | 31/08/2026 | a confirmar |
| 🟢 171 | Vigente desde janeiro de 2026 | 31/08/2026 | auditada |
| 🟢 172 | Estrutura vigente após as parcelas/reajustes de junho de 2026 | 31/08/2026 | auditada |
| 🟢 173 | Vigente desde novembro de 2025 | 31/08/2026 | auditada |
| 🟢 174 | Vigente desde 28/06/2026 | 31/08/2026 | auditada |
| 🟢 175 | Vigente em 19/08/2026 | 31/08/2026 | auditada |
| 🟡 176 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 177 | Tabela oficial consultada em 24/08/2026 | 31/08/2026 | auditada |
| 🟡 178 | Decreto Municipal | 31/08/2026 | a confirmar |
| 🟢 179 | Vigente desde 01/03/2026 | — | auditada |
| 🟡 180 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 181 | Vigente desde dezembro de 2025 | 31/08/2026 | a confirmar |
| 🟡 182 | Deliberação AGENERSA | 31/08/2026 | a confirmar |
| 🟢 183 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 184 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 185 | Vigente desde 08/03/2026 | 31/08/2026 | auditada |
| 🟢 186 | Vigente desde 03/01/2026 | 31/08/2026 | auditada |
| 🟢 187 | Estrutura tarifária 2026; aplicação publicada para março de 2026 | 31/08/2026 | auditada |

Os municípios da CORSAN cobram pela fórmula exponencial `PB × Cⁿ + SB` (seção {{n:16}}), sem preço por faixa; o expoente `n` é o da coluna da categoria na Tabela de Exponenciais.

<!-- tabela: A fórmula exponencial da CORSAN em cada tabela tarifária e categoria coletada -->
| Municípios | Categoria | PB (R$/m³) | SB (R$/mês) | Esgoto (R$/m³) |
| :--- | :--- | ---: | ---: | ---: |
| Erechim (RS) | Residencial | 6,95 | 32,95 | 4,86 |
| Erechim (RS) | Comercial | 7,90 | 58,79 | 5,53 |
| Erechim (RS) | Pública | 7,90 | 117,40 | 5,53 |
| Santa Cruz do Sul (RS) | Residencial | 7,91 | 37,50 | 5,53 |
| Canoas (RS), Esteio (RS) | Residencial | 8,68 | 41,20 | 6,07 |
| Santa Cruz do Sul (RS) | Comercial | 8,98 | 66,92 | 6,28 |
| Santa Cruz do Sul (RS) | Pública | 8,98 | 133,64 | 6,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) e mais 27 | Residencial | 9,15 | 43,39 | 6,40 |
| Canoas (RS), Esteio (RS) | Comercial | 9,88 | 73,48 | 6,91 |
| Canoas (RS), Esteio (RS) | Pública | 9,88 | 146,79 | 6,91 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) e mais 27 | Comercial | 10,41 | 77,41 | 7,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) e mais 27 | Pública | 10,41 | 154,64 | 7,28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) e mais 27 | Industrial | 11,83 | 154,64 | 8,28 |

