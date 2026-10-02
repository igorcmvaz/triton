# Tariff regimes

> **Brazil Edition.** The tariff catalogue is Brazilian and ships only with the Brazil
> Edition. In the International Edition the tariff is entered by the user, in one of
> the same six regimes, and this appendix serves as a description of them.

The database holds **652 municipalities** with tariff structure, sewage
percentage, minimum-charge regime, effective date and source. This list is extracted
from the program's own database, not transcribed.

## The block codes

Each row of the tariff table is a quadruple `(minimum, maximum, value, code)`.

The six codes and the effect of each on the bill are drawn in section {{n:29}}, and are not repeated here.


## The six regimes

<!-- tabela: Distribution of the catalogue municipalities across the six tariff regimes -->
| Regime | Municipalities | What happens when saving |
| :--- | ---: | :--- |
| **No minimum** | 165 | Each m³ saved reduces the bill. |
| **Availability charge** | 122 | A fixed value that **adds** on top of the metered consumption. Each m³ saved is deducted. |
| **Allowance in the minimum** | 329 | The fixed value already includes a volume. Saving **below** the allowance deducts nothing. |
| **Retroactive allowance** | 2 | Up to the allowance the fixed value is paid; beyond it, **everything from zero** is charged. |
| **Payment floor** | 0 | The bill does **not** go below the floor. It does not add: it bounds. |
| **Exponential formula** | 34 | Basic service plus `PB × Cⁿ`, with `n` set by the month's consumption (CORSAN). Each m³ saved is deducted. |

> The payment floor is implemented, and no municipality in the database had been
> classified under it as of this version.

## Distribution by state

The catalogue coverage follows the population, not the territory: the state capitals and the metropolitan regions are almost all registered, and the interior of the North and Centre-West regions concentrates the municipalities still missing ({{fig:fig42_uf}}).

![The catalogue municipalities, by state](../figuras/fig42_uf.png)

*Figure 99 — The distribution of the 652 catalogued municipalities across the Brazilian states, with colours identifying the macro-region. São Paulo and Minas Gerais alone account for almost a third of the catalogue.*


## Updating and auditing the database

The tariff database is maintained by the group with an update routine run outside the interface, before each version. The routine has three components.

**Electricity.** The residential tariffs of subgroup B1 are read from the open database of approved distributor tariffs published by the Brazilian Electricity Regulatory Agency (ANEEL), and associated with the distributor of each catalogue municipality.

**Water and sewage.** A register of primary evidence associates each provider with the regulatory agency, the official tariff page and the type of act that publishes them. Providers with a standard portal are read automatically; the others are flagged for manual checking of the decree or resolution, and the resulting structure goes through the same regime validation described in this appendix.

**Change detection.** Each monitored official page is recorded with the SHA-256 signature of its content and the `ETag` and `Last-Modified` headers. A new check compares the signatures and points out the pages changed since the last collection, which are the candidates for a tariff revision.

The routine can simulate the update without writing the database, run only the change detection, restrict itself to one state or one municipality, and separate electricity from sanitation. Each run writes an audit report in Markdown and an HTML panel with the status of each municipality.

## Confidence grade

Each record carries the confidence grade of the collection:

<!-- tabela: Confidence grade of the tariff records in the catalogue -->
| Grade | Records |
| :--- | ---: |
| A — high | 580 |
| B — good | 63 |
| C — structure to be checked | 5 |
| D — incomplete structure | 4 |

> **Always check the effective date** of your municipality's record against the
> utility's resolution. Tariffs are adjusted every year, and section {{n:16}}
> teaches the test that identifies a wrong structure.


## The blocks by municipality and category

The table below gives the price of water, in R$/m³, in each monthly consumption
interval, for each structure of the catalogue. The columns are the finest split the
catalogue needs: the union of the block limits of all providers, so that within each
column no provider changes the price. Municipalities with the same table form one row,
identified by the number in the first column, which repeats in the following parts.

The residential category covers the 652 municipalities; the others appear where the
provider's official table has been collected. The table is generated from the database
for each version and grows with it. The fixed part adds on top of consumption; a zero
price in the first blocks is the volume already included in the fixed value (allowance
in the minimum).

<!-- tabela: The tariff structures of the catalogue, numbered for the price-by-block tables that follow -->
| No. | Provider: municipalities | Category | Fixed (R$/month) | Sewage |
| ---: | :--- | :--- | :--- | :--- |
| 1 | BRK Alagoas: Maceió (AL) | Residential | — | 100% |
| 2 | BRK Alagoas: Marechal Deodoro (AL) | Residential | — | 80% |
| 3 | BRK Alagoas: Rio Largo (AL) | Residential | — | 80% |
| 4 | BRK Ambiental Cachoeiro: Cachoeiro de Itapemirim (ES) | Residential | 45.00 | 80% |
| 5 | BRK Ambiental Limeira: Limeira (SP) | Residential | 37.10 | 100% |
| 6 | BRK Ambiental Porto Ferreira: Porto Ferreira (SP) | Residential | 42.00 | 90% |
| 7 | BRK Ambiental Sumaré: Sumaré (SP) | Residential | 36.35 | 80% |
| 8 | BRK Ambiental Uruguaiana: Uruguaiana (RS) | Residential | — | 70% |
| 9 | BRK Tocantins: Araguaína (TO), Gurupi (TO), Palmas (TO) and 2 more | Residential | — | 80% |
| 10 | CAEMA: Açailândia (MA), Bacabal (MA), Balsas (MA) and 19 more | Residential | 33.58 | 100% |
| 11 | CAER: Boa Vista (RR) | Residential | 39.92 | 80% |
| 12 | CAERD: Ariquemes (RO), Jaru (RO), Ji-Paraná (RO) and 2 more | Residential | 57.51 | 70% |
| 13 | CAERN: Assu (RN), Caicó (RN), Ceará-Mirim (RN) and 4 more | Residential | 56.96 | 70% |
| 14 | CAERN: Natal (RN) | Residential | 51.40 | 70% |
| 15 | CAESB: Brasília (DF) | Residential | 11.62 | 100% |
| 16 | CAESC – Companhia de Água, Esgoto e Saneamento de Coari: Coari (AM) | Residential | 32.50 | 80% |
| 17 | CAGECE: Acaraú (CE), Aquiraz (CE), Aracati (CE) and 34 more | Residential | — | 80% |
| 18 | CAGEPA: Bayeux (PB), Cabedelo (PB), Cajazeiras (PB) and 7 more | Residential | 54.82 | 80% |
| 19 | CASAL: Arapiraca (AL) | Residential | — | 80% |
| 20 | CASAN: Araranguá (SC), Biguaçu (SC), Camboriú (SC) and 19 more | Residential | 46.34 | 100% |
| 21 | CEDAE/serviço local – validar área: Guapimirim (RJ), Itaperuna (RJ), Macaé (RJ) and 1 more | Residential | — | 100% |
| 22 | CESAMA Juiz de Fora: Juiz de Fora (MG) | Residential | 15.01 | 80% |
| 23 | CESAN: Cariacica (ES), Guarapari (ES), Serra (ES) and 2 more | Residential | 57.39 | 80% |
| 24 | CODAU Uberaba: Uberaba (MG) | Residential | — | 95% |
| 25 | COHASB / Prefeitura de Humaitá – prestação local: Humaitá (AM) | Residential | 32.50 | 80% |
| 26 | Companhia Ituana de Saneamento (CIS): Itu (SP) | Residential | 36.96 | 100% |
| 27 | Companhia Águas de Joinville: Joinville (SC) | Residential | 34.93 | 80% |
| 28 | COMPESA: Abreu e Lima (PE), Araripina (PE), Arcoverde (PE) and 30 more | Residential | 61.77 | 100% |
| 29 | COMUSA Novo Hamburgo: Novo Hamburgo (RS) | Residential | 43.21 | 70% |
| 30 | COPASA: Alfenas (MG), Araxá (MG), Barbacena (MG) and 44 more | Residential | 25.77 | 74% |
| 31 | COSAMA: Tabatinga (AM) | Residential | 32.50 | 80% |
| 32 | COSANPA: Abaetetuba (PA), Acará (PA), Alenquer (PA) and 39 more | Residential | — | 80% |
| 33 | CSA Equatorial: Macapá (AP), Santana (AP) | Residential | 42.91 | 100% |
| 34 | DAAE Araraquara: Araraquara (SP) | Residential | 22.70 | 100% |
| 35 | DAAE Rio Claro: Rio Claro (SP) | Residential | 35.36 | 100% |
| 36 | DAE Americana: Americana (SP) | Residential | up to 6 m³: 14.30 (retroactive) | 100% |
| 37 | DAE Bauru: Bauru (SP) | Residential | up to 6 m³: 19.37 (retroactive) | 65% |
| 38 | DAE Jundiaí: Jundiaí (SP) | Residential | 40.84 | 69% |
| 39 | DAE Sant'Ana do Livramento: Santana do Livramento (RS) | Residential | — | 80% |
| 40 | DAE Valinhos: Valinhos (SP) | Residential | 23.73 | 100% |
| 41 | DAE/VG: Várzea Grande (MT) | Residential | 31.20 | 80% |
| 42 | DAEB Bagé: Bagé (RS) | Residential | 53.37 | 50% |
| 43 | DAEP Penápolis: Penápolis (SP) | Residential | 7.31 | 70% |
| 44 | DAEPA: Patrocínio (MG) | Residential | — | 80% |
| 45 | DAESC Coruripe: Coruripe (AL) | Residential | — | 80% |
| 46 | DAMAE São João del-Rei: São João del-Rei (MG) | Residential | — | 80% |
| 47 | DEMSUR: Muriaé (MG) | Residential | — | 80% |
| 48 | DMAE Porto Alegre: Porto Alegre (RS) | Residential | — | 100% |
| 49 | DMAE Poços de Caldas: Poços de Caldas (MG) | Residential | — | 85% |
| 50 | DMAE Uberlândia: Uberlândia (MG) | Residential | — | 80% |
| 51 | DMAES Ponte Nova: Ponte Nova (MG) | Residential | — | 80% |
| 52 | EMASA Balneário Camboriú: Balneário Camboriú (SC) | Residential | 44.95 | 100% |
| 53 | EMBASA: Alagoinhas (BA), Barra (BA), Barreiras (BA) and 38 more | Residential | 44.77 | 80% |
| 54 | GS Inima SAMAR: Araçatuba (SP) | Residential | 28.48 | 80% |
| 55 | Iguá Sergipe: Aracaju (SE), Estância (SE), Itabaiana (SE) and 4 more | Residential | 49.26 | 80% |
| 56 | Ourinhos Saneamento: Ourinhos (SP) | Residential | — | 50% |
| 57 | Prefeitura de Birigui – Diretoria de Água e Esgoto: Birigui (SP) | Residential | 23.90 | 100% |
| 58 | Prestador municipal/local – Iranduba: Iranduba (AM) | Residential | 32.50 | 80% |
| 59 | Prestador municipal/local – Manicoré: Manicoré (AM) | Residential | 32.50 | 80% |
| 60 | Prestador municipal/local – São Gabriel da Cachoeira: São Gabriel da Cachoeira (AM) | Residential | 32.50 | 80% |
| 61 | Prestador municipal/local – Tefé: Tefé (AM) | Residential | 32.50 | 80% |
| 62 | Prolagos: Cabo Frio (RJ), São Pedro da Aldeia (RJ) | Residential | — | 100% |
| 63 | RIC Ambiental: Marília (SP) | Residential | 19.71 | 75% |
| 64 | Rio+ Saneamento: Itaguaí (RJ), Rio das Ostras (RJ), Seropédica (RJ) | Residential | — | 100% |
| 65 | SAAE / prestação municipal de Manacapuru – confirmar: Manacapuru (AM) | Residential | 32.50 | 80% |
| 66 | SAAE Angra dos Reis: Angra dos Reis (RJ) | Residential | — | 100% |
| 67 | SAAE Aracruz / CESAN conforme área: Aracruz (ES) | Residential | 57.39 | 80% |
| 68 | SAAE Atibaia: Atibaia (SP) | Residential | 52.97 | 100% |
| 69 | SAAE Barra Mansa: Barra Mansa (RJ) | Residential | — | 100% |
| 70 | SAAE Cacoal: Cacoal (RO) | Residential | 17.58 | 60% |
| 71 | SAAE Capivari: Capivari (SP) | Residential | 33.11 | 90% |
| 72 | SAAE Cruzeiro: Cruzeiro (SP) | Residential | 42.00 | 90% |
| 73 | SAAE Formiga: Formiga (MG) | Residential | 21.40 | 50% |
| 74 | SAAE Ibitinga: Ibitinga (SP) | Residential | — | 100% |
| 75 | SAAE Indaiatuba: Indaiatuba (SP) | Residential | 35.10 | 90% |
| 76 | SAAE Itabira: Itabira (MG) | Residential | — | 80% |
| 77 | SAAE Itabirito: Itabirito (MG) | Residential | 22.73 | 60% |
| 78 | SAAE Itacoatiara: Itacoatiara (AM) | Residential | 32.50 | 80% |
| 79 | SAAE Itapira: Itapira (SP) | Residential | 22.71 | 100% |
| 80 | SAAE Jaboticabal: Jaboticabal (SP) | Residential | 28.91 | 100% |
| 81 | SAAE Jacareí: Jacareí (SP) | Residential | 42.00 | 90% |
| 82 | SAAE Lagoa da Prata: Lagoa da Prata (MG) | Residential | 41.70 | 65% |
| 83 | SAAE Lençóis Paulista: Lençóis Paulista (SP) | Residential | 42.00 | 90% |
| 84 | SAAE Linhares: Linhares (ES) | Residential | 45.00 | 80% |
| 85 | SAAE Lucas do Rio Verde: Lucas do Rio Verde (MT) | Residential | — | 80% |
| 86 | SAAE Manhuaçu: Manhuaçu (MG) | Residential | — | 80% |
| 87 | SAAE Mariana: Mariana (MG) | Residential | 29.82 | 100% |
| 88 | SAAE Maués: Maués (AM) | Residential | 32.50 | 80% |
| 89 | SAAE Mogi Mirim: Mogi Mirim (SP) | Residential | 20.25 | 140% |
| 90 | SAAE Nova Mutum: Nova Mutum (MT) | Residential | 24.82 | 80% |
| 91 | SAAE Parintins: Parintins (AM) | Residential | 32.50 | 80% |
| 92 | SAAE Passos: Passos (MG) | Residential | — | 80% |
| 93 | SAAE Pirapora: Pirapora (MG) | Residential | 43.06 | 50% |
| 94 | SAAE Salto: Salto (SP) | Residential | 32.22 | 100% |
| 95 | SAAE Sete Lagoas: Sete Lagoas (MG) | Residential | 30.96 | 80% |
| 96 | SAAE Sorocaba: Sorocaba (SP) | Residential | 22.00 | 92% |
| 97 | SAAE São Carlos: São Carlos (SP) | Residential | — | 100% |
| 98 | SAAE São Mateus: São Mateus (ES) | Residential | — | 80% |
| 99 | SAAE Três Pontas: Três Pontas (MG) | Residential | — | 80% |
| 100 | SAAE Três Rios: Três Rios (RJ) | Residential | — | 100% |
| 101 | SAAE Vilhena: Vilhena (RO) | Residential | 57.51 | 70% |
| 102 | SAAE Viçosa: Viçosa (MG) | Residential | — | 50% |
| 103 | SAAE Volta Redonda: Volta Redonda (RJ) | Residential | — | 100% |
| 104 | SAAEB Ambiental: Bebedouro (SP) | Residential | 34.62 | 80% |
| 105 | SAAEB Barretos: Barretos (SP) | Residential | 28.90 | 50% |
| 106 | SAAEJA: Jaguariúna (SP) | Residential | 22.81 | 100% |
| 107 | SAAET: Taquaritinga (SP) | Residential | 42.00 | 90% |
| 108 | SABESP: Amparo (SP) | Residential | 29.47 | 90% |
| 109 | SABESP: Artur Nogueira (SP), Assis (SP), Avaré (SP) and 36 more | Residential | 40.42 | 80% |
| 110 | SABESP: Arujá (SP), Barueri (SP), Caieiras (SP) and 26 more | Residential | 40.42 | 100% |
| 111 | SABESP: Bertioga (SP), Caraguatatuba (SP), Cubatão (SP) and 9 more | Residential | 40.42 | 100% |
| 112 | SABESP: Bragança Paulista (SP) | Residential | 40.42 | 100% |
| 113 | SABESP: Olímpia (SP) | Residential | 25.34 | 80% |
| 114 | SABESP: Presidente Prudente (SP) | Residential | 32.27 | 80% |
| 115 | SAE Araguari: Araguari (MG) | Residential | 33.89 | 80% |
| 116 | SAE Ituiutaba: Ituiutaba (MG) | Residential | 18.12 | 70% |
| 117 | SAE Louveira: Louveira (SP) | Residential | 27.93 | 85% |
| 118 | SAEC Catanduva: Catanduva (SP) | Residential | 24.79 | 100% |
| 119 | SAECIL Leme: Leme (SP) | Residential | 35.33 | 85% |
| 120 | SAEG: Guaratinguetá (SP) | Residential | 30.06 | 80% |
| 121 | SAEMA Araras: Araras (SP) | Residential | 25.71 | 80% |
| 122 | SAEMAS Sertãozinho: Sertãozinho (SP) | Residential | 25.31 | 80% |
| 123 | SAEP Pirassununga: Pirassununga (SP) | Residential | 29.91 | 100% |
| 124 | SAERP Ribeirão Preto: Ribeirão Preto (SP) | Residential | 14.06 | 128% |
| 125 | SAERP São José do Rio Pardo: São José do Rio Pardo (SP) | Residential | 29.99 | 80% |
| 126 | SAESA: São Caetano do Sul (SP) | Residential | 42.00 | 90% |
| 127 | SAEV Ambiental: Votuporanga (SP) | Residential | 28.22 | 100% |
| 128 | SAMAE Blumenau / BRK Ambiental Blumenau: Blumenau (SC) | Residential | 47.43 | 112% |
| 129 | SAMAE Brusque: Brusque (SC) | Residential | 42.38 | 80% |
| 130 | SAMAE Caxias do Sul: Caxias do Sul (RS) | Residential | 38.30 | 80% |
| 131 | SAMAE Gaspar: Gaspar (SC) | Residential | 50.58 | 80% |
| 132 | SAMAE Jaraguá do Sul: Jaraguá do Sul (SC) | Residential | 30.16 | 80% |
| 133 | SAMAE Mogi Guaçu: Mogi Guaçu (SP) | Residential | 18.91 | 100% |
| 134 | SAMAE São Bento do Sul: São Bento do Sul (SC) | Residential | 31.40 | 80% |
| 135 | SAMAE Tangará da Serra: Tangará da Serra (MT) | Residential | — | 80% |
| 136 | SANASA Campinas: Campinas (SP) | Residential | 53.65 | 123% |
| 137 | SANEACRE: Cruzeiro do Sul (AC), Rio Branco (AC) | Residential | 38.37 | 80% |
| 138 | SANEAGO: Anápolis (GO), Aparecida de Goiânia (GO), Caldas Novas (GO) and 21 more | Residential | 17.46 | 100% |
| 139 | Saneaqua: Mairinque (SP) | Residential | — | 100% |
| 140 | SANEAR Colatina: Colatina (ES) | Residential | — | 80% |
| 141 | SANEAR Rondonópolis: Rondonópolis (MT) | Residential | 36.50 | 80% |
| 142 | SANEBAVI Vinhedo: Vinhedo (SP) | Residential | 40.20 | 100% |
| 143 | Saneouro: Ouro Preto (MG) | Residential | 25.72 | 95% |
| 144 | SANEP Pelotas: Pelotas (RS) | Residential | 28.96 | 80% |
| 145 | SANEPAR – Curitiba: Curitiba (PR) | Residential | 55.09 | 85% |
| 146 | SANEPAR – Demais localidades: Almirante Tamandaré (PR), Apucarana (PR), Arapongas (PR) and 30 more | Residential | 55.09 | 80% |
| 147 | Sanessol: Mirassol (SP) | Residential | 42.00 | 90% |
| 148 | SANESUL: Corumbá (MS), Dourados (MS), Naviraí (MS) and 2 more | Residential | 16.50 | 70% |
| 149 | SEMAE Piracicaba: Piracicaba (SP) | Residential | 31.99 | 100% |
| 150 | SeMAE Rio Preto: São José do Rio Preto (SP) | Residential | 26.63 | 100% |
| 151 | SEMAE São Leopoldo: São Leopoldo (RS) | Residential | 61.29 | 80% |
| 152 | SEMASA Itajaí: Itajaí (SC) | Residential | 41.70 | 80% |
| 153 | SEMASA Lages: Lages (SC) | Residential | 44.00 | 80% |
| 154 | Serviço local – Barra do Piraí: Barra do Piraí (RJ) | Residential | — | 100% |
| 155 | São Gabriel Saneamento S.A.: São Gabriel (RS) | Residential | 33.89 | 80% |
| 156 | Tubarão Saneamento: Tubarão (SC) | Residential | — | 100% |
| 157 | Verde Alagoas: União dos Palmares (AL) | Residential | — | 80% |
| 158 | Águas Alta Floresta / Norte Saneamento: Alta Floresta (MT) | Residential | — | 80% |
| 159 | Águas Cuiabá (Iguá): Cuiabá (MT) | Residential | — | 90% |
| 160 | Águas da Imperatriz: Teresópolis (RJ) | Residential | — | 90% |
| 161 | Águas das Agulhas Negras: Resende (RJ) | Residential | — | 100% |
| 162 | Águas de Andradina: Andradina (SP) | Residential | 42.00 | 90% |
| 163 | Águas de Barra do Garças (Aegea): Barra do Garças (MT) | Residential | — | 80% |
| 164 | Águas de Jahu: Jaú (SP) | Residential | 42.00 | 90% |
| 165 | Águas de Juturnaíba: Araruama (RJ) | Residential | — | 100% |
| 166 | Águas de Manaus: Manaus (AM) | Residential | — | 80% |
| 167 | Águas de Matão: Matão (SP) | Residential | 45.32 | 100% |
| 168 | Águas de Niterói: Niterói (RJ) | Residential | — | 100% |
| 169 | Águas de Nova Friburgo: Nova Friburgo (RJ) | Residential | — | 100% |
| 170 | Águas de Pará de Minas: Pará de Minas (MG) | Residential | — | 80% |
| 171 | Águas de Primavera (Aegea): Primavera do Leste (MT) | Residential | — | 90% |
| 172 | Águas de Sinop (Aegea): Sinop (MT) | Residential | — | 100% |
| 173 | Águas de Sorriso: Sorriso (MT) | Residential | — | 80% |
| 174 | Águas de Teresina: Teresina (PI) | Residential | 46.83 | 80% |
| 175 | Águas de Valadares (Aegea): Governador Valadares (MG) | Residential | 14.67 | 70% |
| 176 | Águas do Imperador: Petrópolis (RJ) | Residential | — | 100% |
| 177 | Águas do Pantanal (autarquia municipal): Cáceres (MT) | Residential | — | 50% |
| 178 | Águas do Paraíba: Campos dos Goytacazes (RJ) | Residential | — | 100% |
| 179 | Águas do Piauí: Floriano (PI), Parnaíba (PI), Picos (PI) and 1 more | Residential | 52.89 | 80% |
| 180 | Águas do Rio: Belford Roxo (RJ), Duque de Caxias (RJ), Japeri (RJ) and 5 more | Residential | — | 100% |
| 181 | Águas do Rio: Cachoeiras de Macacu (RJ), Itaboraí (RJ), Magé (RJ) and 4 more | Residential | — | 100% |
| 182 | Águas do Rio / Iguá / Rio+ Saneamento: Rio de Janeiro (RJ) | Residential | — | 100% |
| 183 | Águas do Sertão: Delmiro Gouveia (AL), Palmeira dos Índios (AL) | Residential | — | 80% |
| 184 | Águas do Sertão: Penedo (AL) | Residential | — | 80% |
| 185 | Águas do Sertão: São Miguel dos Campos (AL) | Residential | — | 80% |
| 186 | Águas Guariroba: Campo Grande (MS) | Residential | 19.87 | 70% |
| 187 | Águas Pontes e Lacerda / Norte Saneamento: Pontes e Lacerda (MT) | Residential | — | 90% |

<!-- tabela: Price of water by monthly consumption interval, in R$/m³, by municipality and category (part 1 of 3: 0–5 to 20–25 m³) -->
| No. | 0–5 | 5–6 | 6–7 | 7–10 | 10–12 | 12–13 | 13–15 | 15–17 | 17–20 | 20–25 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 7.64 | 7.64 | 7.64 | 7.64 | 14.61 | 14.61 | 14.61 | 16.89 | 16.89 | 18.04 |
| 2 | 6.82 | 6.82 | 6.82 | 6.82 | 12.70 | 12.70 | 12.70 | 14.27 | 14.27 | 15.46 |
| 3 | 7.64 | 7.64 | 7.64 | 7.64 | 14.61 | 14.61 | 14.61 | 16.89 | 16.89 | 18.04 |
| 4 | 0.00 | 0.00 | 0.00 | 0.00 | 6.10 | 6.10 | 6.10 | 6.10 | 6.10 | 9.80 |
| 5 | 0.00 | 0.00 | 0.00 | 0.00 | 5.11 | 5.11 | 5.11 | 10.14 | 10.14 | 10.14 |
| 6 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 7 | 0.00 | 0.00 | 0.00 | 0.00 | 3.64 | 3.64 | 3.64 | 3.64 | 3.64 | 4.01 |
| 8 | 10.20 | 10.20 | 10.20 | 10.20 | 10.70 | 10.70 | 10.70 | 10.70 | 10.70 | 15.34 |
| 9 | 8.76 | 3.05 | 3.05 | 3.05 | 8.66 | 8.66 | 8.66 | 11.07 | 11.07 | 13.53 |
| 10 | 0.00 | 0.00 | 0.00 | 0.00 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 10.77 |
| 11 | 0.00 | 0.00 | 0.00 | 0.00 | 5.40 | 5.40 | 5.40 | 5.40 | 5.40 | 8.90 |
| 12 | 0.00 | 0.00 | 0.00 | 0.00 | 6.52 | 6.52 | 6.52 | 7.17 | 7.17 | 8.61 |
| 13 | 0.00 | 0.00 | 0.00 | 0.00 | 6.34 | 6.34 | 6.34 | 7.51 | 7.51 | 8.45 |
| 14 | 0.00 | 0.00 | 0.00 | 0.00 | 5.73 | 5.73 | 5.73 | 6.77 | 6.77 | 7.64 |
| 15 | 4.30 | 4.30 | 4.30 | 5.15 | 5.15 | 5.15 | 10.21 | 10.21 | 10.21 | 14.81 |
| 16 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 17 | 6.77 | 6.77 | 6.77 | 6.77 | 8.78 | 8.78 | 8.78 | 9.49 | 9.49 | 16.29 |
| 18 | 0.00 | 0.00 | 0.00 | 0.00 | 7.08 | 7.08 | 7.08 | 7.08 | 7.08 | 9.32 |
| 19 | 7.28 | 7.28 | 7.28 | 7.28 | 13.90 | 13.90 | 13.90 | 16.07 | 16.07 | 17.17 |
| 20 | 3.08 | 3.08 | 3.08 | 3.08 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 |
| 21 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 22 | 1.65 | 4.46 | 4.46 | 4.46 | 5.58 | 5.58 | 5.58 | 6.32 | 6.32 | 8.55 |
| 23 | 2.26 | 2.26 | 2.26 | 2.26 | 4.52 | 4.52 | 4.52 | 8.14 | 8.14 | 9.77 |
| 24 | 3.91 | 3.91 | 3.91 | 3.91 | 5.20 | 5.20 | 5.20 | 5.20 | 5.20 | 5.74 |
| 25 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 26 | 0.00 | 0.00 | 0.00 | 0.00 | 4.34 | 4.34 | 4.34 | 4.34 | 4.34 | 6.63 |
| 27 | 1.49 | 1.49 | 1.49 | 1.49 | 9.89 | 9.89 | 9.89 | 9.95 | 9.95 | 9.95 |
| 28 | 0.00 | 0.00 | 0.00 | 0.00 | 7.09 | 7.09 | 7.09 | 7.09 | 7.09 | 8.42 |
| 29 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 |
| 30 | 2.69 | 5.33 | 5.33 | 5.33 | 8.06 | 8.06 | 8.06 | 10.83 | 10.83 | 13.66 |
| 31 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 32 | 4.91 | 4.91 | 4.91 | 4.91 | 7.00 | 7.00 | 7.00 | 7.00 | 7.00 | 9.38 |
| 33 | 0.00 | 0.00 | 0.00 | 0.00 | 4.49 | 4.49 | 4.49 | 4.49 | 4.49 | 5.06 |
| 34 | 0.00 | 0.00 | 0.00 | 0.00 | 4.09 | 4.09 | 4.09 | 4.09 | 4.09 | 5.83 |
| 35 | 0.00 | 0.00 | 0.00 | 0.00 | 7.19 | 7.19 | 7.19 | 7.19 | 7.19 | 10.77 |
| 36 | — | — | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 |
| 37 | — | — | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 |
| 38 | 0.00 | 0.00 | 0.00 | 0.00 | 5.18 | 5.18 | 5.18 | 7.65 | 7.65 | 11.01 |
| 39 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 |
| 40 | 0.00 | 0.00 | 0.00 | 0.00 | 4.40 | 4.40 | 4.40 | 4.40 | 5.69 | 5.69 |
| 41 | 0.00 | 0.00 | 0.00 | 0.00 | 4.20 | 4.20 | 4.20 | 4.20 | 4.20 | 6.80 |
| 42 | 4.26 | 4.26 | 4.26 | 4.26 | 5.11 | 5.11 | 5.11 | 5.11 | 5.11 | 6.84 |
| 43 | 3.76 | 3.76 | 3.76 | 3.76 | 3.76 | 3.76 | 3.76 | 3.76 | 3.76 | 4.89 |
| 44 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 45 | 7.28 | 7.28 | 7.28 | 7.28 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 |
| 46 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 47 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 48 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 |
| 49 | 3.70 | 3.70 | 3.70 | 3.70 | 4.44 | 4.44 | 4.44 | 5.22 | 5.22 | 6.74 |
| 50 | 3.85 | 3.85 | 3.85 | 3.85 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 8.20 |
| 51 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 52 | 0.66 | 0.66 | 0.66 | 0.66 | 4.70 | 4.70 | 4.70 | 4.70 | 4.70 | 4.70 |
| 53 | 0.00 | 0.00 | 1.77 | 1.77 | 12.53 | 12.53 | 12.53 | 13.41 | 13.41 | 15.08 |
| 54 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.50 | 3.50 | 3.50 | 3.50 | 6.46 |
| 55 | 0.00 | 0.00 | 0.00 | 0.00 | 11.02 | 11.02 | 11.02 | 11.02 | 11.02 | 16.75 |
| 56 | 3.11 | 3.11 | 3.11 | 3.11 | 6.17 | 6.17 | 6.17 | 6.17 | 6.17 | 7.77 |
| 57 | 0.00 | 0.00 | 0.00 | 0.00 | 2.90 | 2.90 | 2.90 | 2.90 | 2.90 | 3.34 |
| 58 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 59 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 60 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 61 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 62 | 17.04 | 17.04 | 17.04 | 17.04 | 22.32 | 22.32 | 22.32 | 35.74 | 35.74 | 35.74 |
| 63 | 0.00 | 2.31 | 2.31 | 2.31 | 2.31 | 2.31 | 2.31 | 6.24 | 6.24 | 6.24 |
| 64 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 15.37 | 15.37 | 15.37 |
| 65 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 66 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 67 | 0.00 | 0.00 | 0.00 | 0.00 | 4.52 | 4.52 | 4.52 | 8.14 | 8.14 | 9.77 |
| 68 | 0.00 | 0.00 | 0.00 | 0.00 | 7.97 | 7.97 | 7.97 | 7.97 | 7.97 | 13.13 |
| 69 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 70 | 0.00 | 0.00 | 0.00 | 0.00 | 2.11 | 2.11 | 2.11 | 2.43 | 2.43 | 2.79 |
| 71 | 0.00 | 0.00 | 0.00 | 0.00 | 5.33 | 5.33 | 5.33 | 5.33 | 5.33 | 6.65 |
| 72 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 73 | 0.60 | 0.85 | 0.85 | 0.85 | 2.82 | 2.82 | 2.82 | 4.29 | 4.29 | 6.26 |
| 74 | 2.41 | 2.41 | 2.41 | 2.41 | 2.41 | 2.41 | 2.41 | 2.99 | 2.99 | 3.59 |
| 75 | 0.00 | 0.52 | 0.52 | 0.52 | 4.70 | 4.70 | 4.70 | 4.70 | 4.70 | 6.16 |
| 76 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 77 | 1.66 | 1.95 | 1.95 | 1.95 | 3.84 | 3.84 | 3.84 | 5.64 | 5.64 | 6.19 |
| 78 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 79 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 7.29 | 7.29 | 8.27 |
| 80 | 0.00 | 0.00 | 0.00 | 0.00 | 3.48 | 3.48 | 3.48 | 3.48 | 3.48 | 4.38 |
| 81 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 82 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.58 | 3.58 | 3.76 |
| 83 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 84 | 0.00 | 0.00 | 0.00 | 0.00 | 6.10 | 6.10 | 6.10 | 6.10 | 6.10 | 9.80 |
| 85 | 2.43 | 2.43 | 2.43 | 2.43 | 3.12 | 3.12 | 3.12 | 3.12 | 3.12 | 4.15 |
| 86 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 87 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 88 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 89 | 0.00 | 0.00 | 0.00 | 0.00 | 2.22 | 2.22 | 2.22 | 9.09 | 9.09 | 9.17 |
| 90 | 0.00 | 0.00 | 0.00 | 0.00 | 5.22 | 5.22 | 5.22 | 5.22 | 5.22 | 7.54 |
| 91 | 0.00 | 0.00 | 0.00 | 0.00 | 4.50 | 4.50 | 4.50 | 4.50 | 4.50 | 7.20 |
| 92 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 93 | 1.01 | 1.30 | 1.30 | 1.30 | 2.44 | 2.44 | 2.44 | 4.16 | 4.16 | 6.45 |
| 94 | 0.00 | 0.00 | 0.00 | 0.00 | 3.60 | 3.60 | 3.60 | 3.92 | 3.92 | 4.31 |
| 95 | 0.00 | 0.00 | — | — | — | — | — | — | — | — |
| 96 | 0.00 | 0.00 | 0.00 | 0.00 | 3.30 | 3.30 | 3.30 | 4.81 | 4.81 | 6.98 |
| 97 | 2.41 | 2.41 | 2.41 | 2.41 | 6.05 | 6.05 | 6.05 | 6.05 | 6.05 | 7.77 |
| 98 | 3.87 | 3.87 | 3.87 | 3.87 | 6.11 | 6.11 | 6.11 | 7.44 | 7.44 | 8.21 |
| 99 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 100 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 101 | 0.00 | 0.00 | 0.00 | 0.00 | 7.85 | 7.85 | 7.85 | 7.85 | 7.85 | 11.90 |
| 102 | 2.82 | 2.93 | 2.93 | 2.93 | 3.14 | 3.14 | 3.14 | 7.03 | 7.03 | 7.03 |
| 103 | 4.05 | 4.05 | 4.05 | 4.05 | 4.85 | 4.85 | 4.85 | 4.85 | 4.85 | 8.20 |
| 104 | 0.00 | 0.00 | 0.00 | 0.00 | — | — | — | — | — | — |
| 105 | 0.00 | 0.00 | 0.00 | 0.00 | 5.99 | 5.99 | 5.99 | 6.71 | 6.71 | 7.58 |
| 106 | 0.00 | 0.00 | 0.00 | 0.00 | 2.76 | 2.76 | 2.76 | 3.22 | 3.22 | 3.96 |
| 107 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 108 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 4.17 | 4.17 | 4.17 | 4.17 | 13.78 |
| 109 | 0.00 | 0.00 | 0.00 | 0.00 | 5.69 | 5.69 | 5.69 | 5.69 | 5.69 | 8.74 |
| 110 | 0.00 | 0.00 | 0.00 | 0.00 | 6.40 | 6.40 | 6.40 | 6.40 | 6.40 | 15.95 |
| 111 | 0.00 | 0.00 | 0.00 | 0.00 | 5.69 | 5.69 | 5.69 | 5.69 | 5.69 | 8.74 |
| 112 | 0.00 | 0.00 | 0.00 | 0.00 | 5.69 | 5.69 | 5.69 | 5.69 | 5.69 | 7.53 |
| 113 | 0.00 | 0.00 | 0.00 | 0.00 | 5.09 | 5.09 | 5.09 | 5.09 | 5.09 | 5.16 |
| 114 | 0.00 | 0.00 | 0.00 | 0.00 | 4.53 | 4.53 | 4.53 | 4.53 | 4.53 | 6.95 |
| 115 | 0.00 | 0.00 | 0.00 | 0.00 | 2.34 | 2.34 | 2.34 | 2.34 | 2.34 | 2.57 |
| 116 | 1.67 | 2.88 | 2.88 | 2.88 | 4.08 | 4.08 | 4.08 | 5.04 | 5.04 | 5.77 |
| 117 | 0.00 | 0.00 | 0.00 | 0.00 | 3.78 | 3.78 | 3.78 | 3.78 | 3.78 | 4.68 |
| 118 | 0.00 | 0.00 | 0.00 | 0.00 | 3.25 | 3.25 | 3.25 | 3.25 | 3.25 | 7.75 |
| 119 | 0.00 | 0.00 | 0.00 | 0.00 | 4.03 | 4.03 | 4.03 | 4.03 | 4.03 | 5.15 |
| 120 | 0.00 | 0.00 | 0.00 | 0.00 | 4.12 | 4.12 | 4.12 | 4.12 | 4.12 | 6.91 |
| 121 | 0.00 | 0.00 | 0.00 | 0.00 | 3.21 | 3.21 | 3.21 | 3.21 | 3.21 | 4.13 |
| 122 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2.05 | 2.05 | 4.81 |
| 123 | 0.00 | 0.00 | 0.00 | 0.00 | — | — | — | — | — | — |
| 124 | 0.00 | 0.00 | 0.00 | 0.00 | 2.48 | 2.48 | 2.48 | 3.93 | 3.93 | 5.39 |
| 125 | 0.00 | 0.00 | 0.00 | 0.00 | — | — | — | — | — | — |
| 126 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 127 | 0.00 | 0.00 | 0.00 | 0.00 | 4.87 | 4.87 | 4.87 | 4.87 | 4.87 | 8.31 |
| 128 | 0.00 | 0.00 | 0.00 | 0.00 | 8.63 | 8.63 | 8.63 | 8.63 | 8.63 | 8.63 |
| 129 | 0.00 | 0.00 | 0.00 | 0.00 | 7.80 | 7.80 | 7.80 | 10.01 | 10.01 | 11.37 |
| 130 | 0.00 | 8.77 | 8.77 | 8.77 | 10.54 | 10.54 | 10.54 | 16.56 | 16.56 | 21.75 |
| 131 | 0.00 | 0.00 | 0.00 | 0.00 | 7.81 | 7.81 | 7.81 | 7.81 | 7.81 | 7.81 |
| 132 | 1.59 | 1.80 | 1.80 | 1.80 | 8.05 | 8.05 | 8.05 | 10.23 | 10.23 | 11.37 |
| 133 | 0.00 | 0.00 | 0.00 | 0.00 | 2.29 | 2.29 | 2.29 | 2.82 | 2.82 | 7.52 |
| 134 | 2.36 | 2.55 | 2.55 | 2.55 | 8.83 | 8.83 | 8.83 | 9.40 | 9.40 | 10.02 |
| 135 | 5.85 | 5.85 | 5.85 | 5.85 | 7.90 | 7.90 | 7.90 | 7.90 | 7.90 | 10.80 |
| 136 | 0.00 | 0.00 | 0.00 | 0.00 | 9.96 | 9.96 | 9.96 | 10.18 | 10.18 | 10.43 |
| 137 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 3.68 | 3.68 | 4.57 |
| 138 | 5.77 | 5.77 | 5.77 | 5.77 | 6.51 | 6.51 | 6.51 | 7.45 | 7.45 | 8.45 |
| 139 | 4.71 | 4.71 | 4.71 | 4.71 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.04 |
| 140 | 2.85 | 2.85 | 2.85 | 2.85 | 5.92 | 5.92 | 5.92 | 8.50 | 8.50 | 9.36 |
| 141 | 0.00 | 0.00 | 0.00 | 0.00 | 5.10 | 5.10 | 5.10 | 5.10 | 5.10 | 8.20 |
| 142 | 0.00 | 0.00 | 0.00 | 0.00 | 4.56 | 4.56 | 4.56 | 5.73 | 5.73 | 8.00 |
| 143 | 3.67 | 3.67 | 3.67 | 3.67 | 10.06 | 10.06 | 10.06 | 12.46 | 12.46 | 14.30 |
| 144 | 6.13 | 6.13 | 6.13 | 6.13 | 7.05 | 7.05 | 7.05 | 7.05 | 7.05 | 9.32 |
| 145 | 0.00 | 1.70 | 1.70 | 1.70 | 9.49 | 9.49 | 9.49 | 9.54 | 9.54 | 9.62 |
| 146 | 0.00 | 1.70 | 1.70 | 1.70 | 9.49 | 9.49 | 9.49 | 9.54 | 9.54 | 9.62 |
| 147 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 148 | 5.92 | 5.92 | 5.92 | 5.92 | 7.45 | 7.45 | 7.45 | 9.15 | 9.15 | 11.80 |
| 149 | 0.00 | 0.00 | 0.00 | 0.00 | 5.49 | 5.49 | 5.49 | 7.88 | 7.88 | 11.28 |
| 150 | 0.00 | 0.00 | 0.00 | 0.00 | 3.84 | 3.84 | 3.84 | 3.84 | 3.84 | 5.25 |
| 151 | 5.15 | 5.15 | 5.15 | 5.15 | 5.15 | 5.15 | 5.15 | 11.45 | 11.45 | 11.45 |
| 152 | 0.00 | 0.00 | 0.00 | 0.00 | 7.48 | 7.48 | 7.48 | 7.48 | 7.48 | 7.48 |
| 153 | 0.00 | 0.00 | 0.00 | 0.00 | 7.48 | 7.48 | 7.48 | 7.48 | 7.48 | 7.48 |
| 154 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 155 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 |
| 156 | 5.25 | 5.25 | 5.25 | 5.25 | 9.68 | 9.68 | 9.68 | 9.68 | 9.68 | 11.11 |
| 157 | 5.58 | 5.58 | 5.58 | 5.58 | 10.25 | 10.25 | 10.25 | 11.14 | 11.14 | 12.22 |
| 158 | 5.85 | 5.85 | 5.85 | 5.85 | 7.90 | 7.90 | 7.90 | 7.90 | 7.90 | 10.80 |
| 159 | 4.92 | 4.92 | 4.92 | 4.92 | 6.01 | 6.01 | 6.01 | 6.01 | 6.01 | 10.06 |
| 160 | 5.28 | 5.28 | 5.28 | 5.28 | 5.28 | 5.28 | 5.28 | 11.62 | 11.62 | 11.62 |
| 161 | 4.50 | 4.50 | 4.50 | 4.50 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.50 |
| 162 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 163 | 4.33 | 4.33 | 4.33 | 4.33 | 6.50 | 6.50 | 6.50 | 6.50 | 6.50 | 10.83 |
| 164 | 0.00 | 0.00 | 0.00 | 0.00 | 5.60 | 5.60 | 5.60 | 5.60 | 5.60 | 9.80 |
| 165 | 13.79 | 13.79 | 13.79 | 13.79 | 17.71 | 17.71 | 17.71 | 26.45 | 26.45 | 26.45 |
| 166 | 6.42 | 6.42 | 6.42 | 6.42 | 12.43 | 12.43 | 12.43 | 12.43 | 12.43 | 18.98 |
| 167 | 0.00 | 0.00 | 0.00 | 0.00 | 4.53 | 4.53 | 4.53 | 4.53 | 4.53 | 6.04 |
| 168 | 5.65 | 5.65 | 5.65 | 5.65 | 5.65 | 5.65 | 5.65 | 14.13 | 14.13 | 14.13 |
| 169 | 4.25 | 4.25 | 4.25 | 4.25 | 7.10 | 7.10 | 7.10 | 7.10 | 7.10 | 7.10 |
| 170 | 4.10 | 4.10 | 4.10 | 4.10 | 5.95 | 5.95 | 5.95 | 5.95 | 5.95 | 8.60 |
| 171 | 5.76 | 5.76 | 5.76 | 5.76 | 8.64 | 8.64 | 8.64 | 8.64 | 8.64 | 14.40 |
| 172 | 6.01 | 6.01 | 6.01 | 6.01 | 8.54 | 8.54 | 8.54 | 8.54 | 8.54 | 14.32 |
| 173 | 3.06 | 3.06 | 3.06 | 3.06 | 4.59 | 4.59 | 4.59 | 4.59 | 4.59 | 7.66 |
| 174 | 0.00 | 0.00 | 0.00 | 0.00 | 8.72 | 8.72 | 8.72 | 8.72 | 8.72 | 8.72 |
| 175 | 1.79 | 1.83 | 1.83 | 1.83 | 5.24 | 5.24 | 5.24 | 5.57 | 5.57 | 5.62 |
| 176 | 4.80 | 4.80 | 4.80 | 4.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 11.50 |
| 177 | 3.27 | 3.27 | 3.27 | 3.27 | 5.72 | 5.72 | 5.72 | 5.72 | 5.72 | 8.87 |
| 178 | 4.85 | 4.85 | 4.85 | 4.85 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 11.50 |
| 179 | 0.00 | 0.00 | 0.00 | 0.00 | 9.81 | 9.81 | 9.81 | 10.92 | 10.92 | 12.80 |
| 180 | 7.52 | 7.52 | 7.52 | 7.52 | 7.52 | 7.52 | 7.52 | 16.54 | 16.54 | 16.54 |
| 181 | 7.44 | 7.44 | 7.44 | 7.44 | 7.44 | 7.44 | 7.44 | 16.36 | 16.36 | 16.36 |
| 182 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 6.98 | 15.37 | 15.37 | 15.37 |
| 183 | 7.39 | 7.39 | 7.39 | 7.39 | 14.10 | 14.10 | 14.10 | 16.30 | 16.30 | 17.41 |
| 184 | 6.14 | 6.14 | 6.14 | 6.14 | 10.68 | 10.68 | 10.68 | 12.17 | 12.17 | 13.72 |
| 185 | 5.49 | 5.49 | 5.49 | 5.49 | 10.48 | 10.48 | 10.48 | 12.11 | 12.11 | 12.94 |
| 186 | 8.03 | 8.03 | 8.03 | 8.03 | 10.28 | 10.28 | 10.28 | 10.46 | 10.46 | 11.57 |
| 187 | 3.03 | 3.03 | 3.03 | 3.03 | 4.55 | 4.55 | 4.55 | 4.55 | 4.55 | 7.57 |

<!-- tabela: Price of water by monthly consumption interval, in R$/m³, by municipality and category (part 2 of 3: 25–30 to 70–75 m³) -->
| No. | 25–30 | 30–35 | 35–40 | 40–45 | 45–50 | 50–55 | 55–60 | 60–65 | 65–70 | 70–75 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 18.04 | 18.63 | 18.63 | 18.86 | 18.86 | 18.99 | 18.99 | 18.99 | 18.99 | 18.99 |
| 2 | 15.46 | 15.97 | 15.97 | 15.92 | 15.92 | 15.14 | 15.14 | 15.14 | 15.14 | 15.14 |
| 3 | 18.04 | 18.63 | 18.63 | 18.86 | 18.86 | 18.99 | 18.99 | 18.99 | 18.99 | 18.99 |
| 4 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 |
| 5 | 10.14 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 16.48 | 16.48 | 16.48 |
| 6 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 7 | 4.01 | 5.64 | 5.64 | 5.64 | 5.64 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 |
| 8 | 15.34 | 15.85 | 15.85 | 15.85 | 15.85 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 |
| 9 | 15.67 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 |
| 10 | 10.77 | 13.68 | 13.68 | 13.68 | 13.68 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 |
| 11 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 |
| 12 | 9.87 | 11.82 | 11.82 | 11.82 | 11.82 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 |
| 13 | 8.45 | 9.74 | 9.74 | 9.74 | 9.74 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 14 | 7.64 | 8.79 | 8.79 | 8.79 | 8.79 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 15 | 14.81 | 22.22 | 22.22 | 22.22 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 |
| 16 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 17 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 |
| 18 | 9.32 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 |
| 19 | 17.17 | 17.72 | 17.72 | 17.96 | 17.96 | 18.07 | 18.07 | 18.07 | 18.07 | 18.07 |
| 20 | 19.14 | 19.14 | 19.14 | 19.14 | 19.14 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 |
| 21 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 22 | 8.55 | 8.55 | 8.55 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 |
| 23 | 9.77 | 11.24 | 11.24 | 11.24 | 11.24 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 |
| 24 | 5.74 | 6.13 | 6.13 | 6.13 | 6.13 | 6.88 | 6.88 | 6.88 | 6.88 | 6.88 |
| 25 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 26 | 6.63 | 6.63 | 6.63 | 6.63 | 6.63 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 |
| 27 | 13.18 | 13.18 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 |
| 28 | 8.42 | 11.59 | 11.59 | 11.59 | 11.59 | 13.74 | 13.74 | 13.74 | 13.74 | 13.74 |
| 29 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 |
| 30 | 13.66 | 13.66 | 13.66 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 |
| 31 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 32 | 9.38 | 10.58 | 10.58 | 14.66 | 14.66 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 |
| 33 | 5.06 | 6.58 | 6.58 | 6.58 | 6.58 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 |
| 34 | 5.83 | 7.64 | 7.64 | 9.07 | 9.07 | 10.82 | 10.82 | 10.82 | 10.82 | 10.82 |
| 35 | 10.77 | 10.77 | 10.77 | 10.77 | 10.77 | 15.55 | 15.55 | 15.55 | 15.55 | 15.55 |
| 36 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 |
| 37 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 |
| 38 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 |
| 39 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 |
| 40 | 7.77 | 7.77 | 10.69 | 10.69 | 10.69 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 |
| 41 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 |
| 42 | 6.84 | 8.10 | 8.10 | 8.94 | 8.94 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 |
| 43 | 4.89 | 5.26 | 5.26 | 5.64 | 5.64 | 6.01 | 6.01 | 6.01 | 6.01 | 6.01 |
| 44 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 45 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 |
| 46 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 47 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 48 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 |
| 49 | 6.74 | 8.37 | 8.37 | 9.93 | 9.93 | 11.47 | 11.47 | 13.08 | 13.08 | 14.61 |
| 50 | 8.20 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 |
| 51 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 52 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 |
| 53 | 16.82 | 18.49 | 18.49 | 20.28 | 20.28 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 |
| 54 | 6.46 | 8.82 | 8.82 | 8.82 | 8.82 | 12.69 | 12.69 | 12.69 | 12.69 | 12.69 |
| 55 | 16.75 | 23.49 | 23.49 | 23.49 | 23.49 | 32.67 | 32.67 | 32.67 | 32.67 | 32.67 |
| 56 | 7.77 | 10.04 | 10.04 | 10.04 | 10.04 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 |
| 57 | 3.34 | 3.70 | 3.70 | 5.06 | 5.06 | 6.46 | 6.46 | 6.46 | 6.46 | 6.46 |
| 58 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 59 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 60 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 61 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 62 | 42.88 | 42.88 | 51.46 | 51.46 | 63.18 | 63.18 | 80.25 | 80.25 | 91.26 | 91.26 |
| 63 | 6.24 | 8.41 | 8.41 | 8.41 | 8.41 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 |
| 64 | 15.37 | 20.94 | 20.94 | 20.94 | 41.88 | 41.88 | 41.88 | 55.84 | 55.84 | 55.84 |
| 65 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 66 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 67 | 9.77 | 11.24 | 11.24 | 11.24 | 11.24 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 |
| 68 | 13.13 | 13.13 | 13.13 | 13.13 | 13.13 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 |
| 69 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 70 | 3.21 | 3.69 | 3.69 | 3.69 | 3.69 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 |
| 71 | 6.65 | 9.53 | 9.53 | 14.27 | 14.27 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 |
| 72 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 73 | 8.23 | 9.71 | 9.71 | 9.96 | 9.96 | 10.01 | 10.01 | 10.01 | 10.01 | 10.01 |
| 74 | 4.11 | 4.66 | 5.33 | 6.07 | 6.92 | 7.88 | 7.88 | 7.88 | 7.88 | 8.99 |
| 75 | 6.16 | 6.83 | 6.83 | 9.65 | 9.65 | 9.65 | 9.65 | 11.45 | 11.45 | 11.45 |
| 76 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 77 | 6.83 | 7.49 | 7.49 | 8.29 | 8.29 | 9.09 | 9.09 | 9.09 | 9.09 | 9.09 |
| 78 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 79 | 8.27 | 8.37 | 8.50 | 8.67 | 8.67 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 |
| 80 | 4.38 | 7.21 | 7.21 | 8.37 | 8.37 | 11.88 | 11.88 | 13.03 | 13.03 | 14.36 |
| 81 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 82 | 3.93 | 4.31 | 4.31 | 4.51 | 4.51 | 4.72 | 4.72 | 4.72 | 4.72 | 4.72 |
| 83 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 84 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 |
| 85 | 5.96 | 5.96 | 7.03 | 7.03 | 7.03 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 |
| 86 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 87 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 88 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 89 | 9.17 | 9.56 | 9.56 | 10.05 | 10.05 | 10.66 | 10.66 | 10.66 | 10.66 | 10.66 |
| 90 | 7.54 | 9.28 | 9.28 | 11.59 | 11.59 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 |
| 91 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 92 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 93 | 8.17 | 9.88 | 9.88 | 10.17 | 10.17 | 10.23 | 10.23 | 10.23 | 10.23 | 10.23 |
| 94 | 4.77 | 5.27 | 6.34 | 8.07 | 8.07 | 8.07 | 8.07 | 10.21 | 10.21 | 10.21 |
| 95 | — | — | — | — | — | — | — | — | — | — |
| 96 | 7.69 | 8.05 | 8.05 | 8.47 | 8.47 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 |
| 97 | 7.77 | 9.81 | 9.81 | 11.65 | 11.65 | 12.78 | 12.78 | 14.16 | 14.16 | 14.16 |
| 98 | 8.21 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 |
| 99 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 100 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 101 | 11.90 | 11.90 | 11.90 | 11.90 | 11.90 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 |
| 102 | 7.03 | 7.03 | 7.03 | 9.74 | 9.74 | 9.74 | 9.74 | 10.33 | 10.33 | 10.33 |
| 103 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 |
| 104 | — | — | — | — | — | — | — | — | — | — |
| 105 | 8.64 | 9.94 | 11.54 | 13.50 | 13.50 | 15.91 | 15.91 | 15.91 | 15.91 | 15.91 |
| 106 | 4.73 | 5.65 | 6.85 | 6.85 | 8.21 | 8.21 | 8.21 | 9.78 | 9.78 | 9.78 |
| 107 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 108 | 13.78 | 13.78 | 13.78 | 13.78 | 13.78 | 20.37 | 20.37 | 20.37 | 20.37 | 20.37 |
| 109 | 8.74 | 8.74 | 8.74 | 8.74 | 8.74 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 |
| 110 | 15.95 | 15.95 | 15.95 | 15.95 | 15.95 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 |
| 111 | 8.74 | 8.74 | 8.74 | 8.74 | 8.74 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 |
| 112 | 7.53 | 7.53 | 7.53 | 7.53 | 7.53 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 |
| 113 | 5.16 | 7.09 | 7.09 | 7.09 | 7.09 | 11.82 | 11.82 | 11.93 | 11.93 | 12.03 |
| 114 | 6.95 | 6.95 | 6.95 | 6.95 | 6.95 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 |
| 115 | 2.57 | 2.81 | 2.81 | 3.10 | 3.10 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 |
| 116 | 6.49 | 6.97 | 6.97 | 7.45 | 7.45 | 7.69 | 7.69 | 7.69 | 7.69 | 7.69 |
| 117 | 4.68 | 6.43 | 6.43 | 7.25 | 7.25 | 10.21 | 10.21 | 10.21 | 10.21 | 15.08 |
| 118 | 7.79 | 8.34 | 8.34 | 9.77 | 9.77 | 11.47 | 11.47 | 11.47 | 11.47 | 11.47 |
| 119 | 5.15 | 6.62 | 6.62 | 6.90 | 6.90 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 |
| 120 | 6.91 | 6.91 | 6.91 | 6.91 | 6.91 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 |
| 121 | 4.13 | 5.58 | 5.58 | 5.58 | 5.58 | 7.82 | 7.82 | 7.82 | 7.82 | 7.82 |
| 122 | 5.39 | 5.83 | 5.93 | 6.46 | 6.46 | 7.02 | 7.02 | 7.67 | 7.67 | 9.92 |
| 123 | — | — | — | — | — | — | — | — | — | — |
| 124 | 7.18 | 9.33 | 9.33 | 12.57 | 12.57 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 |
| 125 | — | — | — | — | — | — | — | — | — | — |
| 126 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 127 | 8.31 | 8.25 | 8.25 | 8.25 | 8.25 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 |
| 128 | 8.63 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 |
| 129 | 12.54 | 12.54 | 12.54 | 12.54 | 12.54 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 |
| 130 | 21.75 | 22.66 | 22.66 | 22.66 | 22.66 | 24.36 | 24.36 | 24.36 | 24.36 | 24.36 |
| 131 | 10.30 | 10.30 | 10.30 | 12.49 | 12.49 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 |
| 132 | 12.49 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 |
| 133 | 7.52 | 7.58 | 7.58 | 9.34 | 9.34 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 |
| 134 | 10.34 | 10.34 | 10.34 | 10.34 | 10.34 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 |
| 135 | 10.80 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 |
| 136 | 12.82 | 13.65 | 13.65 | 13.65 | 13.65 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 |
| 137 | 5.46 | 6.35 | 7.24 | 8.12 | 9.01 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 |
| 138 | 9.54 | 10.89 | 10.89 | 12.33 | 12.33 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 |
| 139 | 10.04 | 10.04 | 10.04 | 10.04 | 10.04 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 |
| 140 | 9.36 | 9.98 | 9.98 | 9.98 | 9.98 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 |
| 141 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 |
| 142 | 8.00 | 8.00 | 11.63 | 11.63 | 11.63 | 16.92 | 16.92 | 16.92 | 16.92 | 16.92 |
| 143 | 14.30 | 14.30 | 14.30 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 |
| 144 | 9.32 | 10.74 | 10.74 | 10.74 | 10.74 | 12.33 | 12.33 | 12.33 | 12.33 | 12.33 |
| 145 | 9.62 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 |
| 146 | 9.62 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 |
| 147 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 148 | 11.80 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 |
| 149 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 |
| 150 | 5.25 | 6.99 | 6.99 | 8.64 | 8.64 | 13.14 | 13.14 | 13.14 | 13.14 | 13.14 |
| 151 | 11.45 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 |
| 152 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 |
| 153 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 |
| 154 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 155 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 |
| 156 | 11.11 | 13.59 | 13.59 | 13.59 | 13.59 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 |
| 157 | 12.22 | 12.64 | 12.64 | 13.29 | 13.29 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 |
| 158 | 10.80 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 |
| 159 | 10.06 | 12.31 | 12.31 | 12.31 | 12.31 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 |
| 160 | 11.62 | 15.85 | 15.85 | 15.85 | 31.70 | 31.70 | 31.70 | 42.27 | 42.27 | 42.27 |
| 161 | 10.50 | 10.50 | 10.50 | 10.50 | 10.50 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 162 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 163 | 10.83 | 14.29 | 14.29 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 |
| 164 | 9.80 | 9.80 | 9.80 | 9.80 | 9.80 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 165 | 33.10 | 33.10 | 42.43 | 42.43 | 51.93 | 51.93 | 66.02 | 66.02 | 80.27 | 80.27 |
| 166 | 18.98 | 25.86 | 25.86 | 29.84 | 29.84 | 29.84 | 29.84 | 34.02 | 34.02 | 34.02 |
| 167 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 |
| 168 | 14.13 | 17.53 | 17.53 | 17.53 | 33.92 | 33.92 | 33.92 | 45.23 | 45.23 | 45.23 |
| 169 | 7.10 | 11.80 | 11.80 | 11.80 | 11.80 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 |
| 170 | 8.60 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 171 | 14.40 | 19.01 | 19.01 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 |
| 172 | 14.32 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 |
| 173 | 7.66 | 11.48 | 11.48 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 |
| 174 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 |
| 175 | 5.62 | 5.62 | 5.62 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 |
| 176 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 |
| 177 | 8.87 | 11.37 | 11.37 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 |
| 178 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 179 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 |
| 180 | 16.54 | 22.56 | 22.56 | 22.56 | 45.12 | 45.12 | 45.12 | 60.16 | 60.16 | 60.16 |
| 181 | 16.36 | 22.31 | 22.31 | 22.31 | 44.62 | 44.62 | 44.62 | 59.49 | 59.49 | 59.49 |
| 182 | 15.37 | 20.94 | 20.94 | 20.94 | 41.88 | 41.88 | 41.88 | 55.84 | 55.84 | 55.84 |
| 183 | 17.41 | 17.98 | 17.98 | 18.21 | 18.21 | 18.33 | 18.33 | 18.33 | 18.33 | 18.33 |
| 184 | 13.72 | 14.83 | 14.83 | 15.57 | 15.57 | 15.95 | 15.95 | 15.95 | 15.95 | 15.95 |
| 185 | 12.94 | 13.36 | 13.36 | 13.54 | 13.54 | 13.62 | 13.62 | 13.62 | 13.62 | 13.62 |
| 186 | 14.23 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 |
| 187 | 7.57 | 9.99 | 9.99 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 |

<!-- tabela: Price of water by monthly consumption interval, in R$/m³, by municipality and category (part 3 of 3: 75–80 to 5,000 m³) -->
| No. | 75–80 | 80–90 | 90–99 | 99–100 | 100–150 | 150–200 | 200–300 | 300–500 | 500–5,000 | > 5,000 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 18.99 | 18.99 | 19.09 | 19.09 | 19.09 | 19.10 | 19.10 | 19.10 | 19.10 | 19.10 |
| 2 | 15.14 | 15.14 | 16.96 | 16.96 | 16.96 | 19.88 | 19.88 | 19.88 | 19.88 | 19.88 |
| 3 | 18.99 | 18.99 | 19.09 | 19.09 | 19.09 | 19.10 | 19.10 | 19.10 | 19.10 | 19.10 |
| 4 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 |
| 5 | 16.48 | 16.48 | 16.48 | 16.48 | 20.60 | 20.60 | 20.60 | 20.60 | 20.60 | 20.60 |
| 6 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 7 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 | 7.57 |
| 8 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 | 16.18 |
| 9 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 | 17.50 |
| 10 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 | 21.48 |
| 11 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 | 8.90 |
| 12 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 |
| 13 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 14 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 15 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 | 28.88 |
| 16 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 17 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 | 28.77 |
| 18 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 | 12.67 |
| 19 | 18.07 | 18.07 | 18.18 | 18.18 | 18.18 | 18.19 | 18.19 | 18.19 | 18.19 | 18.19 |
| 20 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 | 24.08 |
| 21 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 22 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 | 11.16 |
| 23 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 |
| 24 | 6.88 | 6.88 | 6.88 | 6.88 | 7.03 | 7.03 | 7.28 | 7.28 | 7.28 | 7.28 |
| 25 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 26 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 | 7.94 |
| 27 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 | 13.63 |
| 28 | 13.74 | 13.74 | 26.40 | 26.40 | 26.40 | 26.40 | 26.40 | 26.40 | 26.40 | 26.40 |
| 29 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 | 9.23 |
| 30 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 | 16.54 |
| 31 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 32 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 | 19.04 |
| 33 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 | 9.31 |
| 34 | 10.82 | 10.82 | 10.82 | 10.82 | 12.76 | 12.76 | 15.21 | 15.21 | 15.21 | 15.21 |
| 35 | 15.55 | 15.55 | 15.55 | 15.55 | 17.91 | 17.91 | 17.91 | 17.91 | 17.91 | 17.91 |
| 36 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 | 3.49 |
| 37 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 | 3.23 |
| 38 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 | 11.01 |
| 39 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 | 2.37 |
| 40 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 | 22.18 |
| 41 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 | 6.80 |
| 42 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 | 11.17 |
| 43 | 6.39 | 6.39 | 6.39 | 6.39 | 6.76 | 6.76 | 6.76 | 6.76 | 6.76 | 6.76 |
| 44 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 45 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 | 19.80 |
| 46 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 47 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 48 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 | 5.50 |
| 49 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 | 14.61 |
| 50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 | 11.50 |
| 51 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 52 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 | 7.83 |
| 53 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 | 24.40 |
| 54 | 12.69 | 12.69 | 12.69 | 12.69 | 16.79 | 16.79 | 16.79 | 16.79 | 16.79 | 16.79 |
| 55 | 32.67 | 32.67 | 32.67 | 32.67 | 42.08 | 42.08 | 42.08 | 42.08 | 42.08 | 42.08 |
| 56 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 | 15.77 |
| 57 | 6.46 | 6.46 | 6.46 | 6.46 | 8.12 | 8.12 | 9.62 | 9.62 | 9.62 | 9.62 |
| 58 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 59 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 60 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 61 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 62 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 | 91.26 |
| 63 | 10.20 | 10.20 | 10.20 | 10.20 | 11.63 | 11.63 | 11.63 | 11.63 | 11.63 | 11.63 |
| 64 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 |
| 65 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 66 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 67 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 | 12.36 |
| 68 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 | 16.09 |
| 69 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 70 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 | 4.06 |
| 71 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 | 15.67 |
| 72 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 73 | 10.06 | 10.06 | 10.06 | 10.06 | 10.11 | 10.11 | 10.16 | 10.16 | 10.16 | 10.16 |
| 74 | 8.99 | 8.99 | 8.99 | 8.99 | 10.22 | 10.22 | 10.22 | 10.22 | 10.22 | 10.22 |
| 75 | 11.45 | 23.32 | 23.32 | 23.32 | 23.32 | 23.32 | 23.32 | 23.32 | 23.32 | 23.32 |
| 76 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 77 | 9.99 | 9.99 | 9.99 | 9.99 | 10.99 | 10.99 | 12.09 | 12.09 | 12.09 | 12.09 |
| 78 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 79 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 | 10.44 |
| 80 | 14.36 | 15.93 | 17.47 | 17.47 | 19.22 | 19.22 | 19.22 | 19.22 | 19.22 | 19.22 |
| 81 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 82 | 5.11 | 5.11 | 5.11 | 5.11 | 5.54 | 5.54 | 5.72 | 5.72 | 5.72 | 5.72 |
| 83 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 84 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 | 14.80 |
| 85 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 |
| 86 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 87 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 88 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 89 | 11.67 | 11.67 | 11.67 | 11.67 | 12.75 | 12.75 | 12.75 | 12.75 | 12.75 | 12.75 |
| 90 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 | 13.92 |
| 91 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 | 7.20 |
| 92 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 93 | 10.29 | 10.29 | 10.29 | 10.29 | 10.34 | 10.34 | 10.40 | 10.40 | 10.40 | 10.40 |
| 94 | 10.21 | 13.58 | 13.58 | 13.58 | 13.58 | 13.58 | 13.58 | 13.58 | 13.58 | 13.58 |
| 95 | — | — | — | — | — | — | — | — | — | — |
| 96 | 9.12 | 9.12 | 9.12 | 9.12 | 10.95 | 10.95 | 13.13 | 15.75 | 15.75 | 15.75 |
| 97 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 | 14.16 |
| 98 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 | 9.40 |
| 99 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 100 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 101 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 | 16.50 |
| 102 | 10.33 | 10.33 | 10.33 | 10.33 | 10.33 | 10.33 | 10.33 | 10.95 | 10.95 | 10.95 |
| 103 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 | 12.50 |
| 104 | — | — | — | — | — | — | — | — | — | — |
| 105 | 15.91 | 15.91 | 15.91 | 15.91 | 17.18 | 17.18 | 17.18 | 17.18 | 17.18 | 17.18 |
| 106 | 9.78 | 9.78 | 9.78 | 9.78 | 11.75 | 11.75 | 11.75 | 11.75 | 11.75 | 11.75 |
| 107 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 108 | 20.37 | 20.37 | 20.37 | 25.49 | 25.49 | 25.49 | 25.49 | 25.49 | 25.49 | 25.49 |
| 109 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 |
| 110 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 | 17.57 |
| 111 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 | 10.46 |
| 112 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 |
| 113 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 | 12.03 |
| 114 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 | 8.32 |
| 115 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 | 3.46 |
| 116 | 7.93 | 7.93 | 7.93 | 7.93 | 8.17 | 8.17 | 8.41 | 8.41 | 8.41 | 8.41 |
| 117 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 | 15.08 |
| 118 | 11.47 | 11.47 | 11.47 | 11.47 | 13.46 | 13.46 | 13.46 | 13.46 | 13.46 | 13.46 |
| 119 | 9.23 | 9.23 | 9.23 | 9.23 | 10.87 | 10.87 | 10.87 | 10.87 | 10.87 | 10.87 |
| 120 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 | 11.31 |
| 121 | 7.82 | 7.82 | 7.82 | 7.82 | 11.34 | 11.34 | 11.34 | 11.34 | 17.02 | 26.39 |
| 122 | 9.92 | 12.03 | 12.81 | 12.81 | 13.20 | 13.20 | 13.20 | 13.20 | 13.20 | 13.20 |
| 123 | — | — | — | — | — | — | — | — | — | — |
| 124 | 15.77 | 19.02 | 19.02 | 19.02 | 21.87 | 21.87 | 21.87 | 21.87 | 21.87 | 21.87 |
| 125 | — | — | — | — | — | — | — | — | — | — |
| 126 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 127 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 | 9.94 |
| 128 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 | 11.00 |
| 129 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 | 13.18 |
| 130 | 24.36 | 24.36 | 24.36 | 24.36 | 28.35 | 28.35 | 28.35 | 28.35 | 28.35 | 28.35 |
| 131 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 | 14.31 |
| 132 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 | 14.79 |
| 133 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 | 10.74 |
| 134 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 | 10.51 |
| 135 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 |
| 136 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 | 20.94 |
| 137 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 | 9.90 |
| 138 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 | 14.06 |
| 139 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 | 11.91 |
| 140 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 | 10.41 |
| 141 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 | 8.20 |
| 142 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 | 22.82 |
| 143 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 | 22.98 |
| 144 | 12.33 | 12.33 | 12.33 | 12.33 | 14.18 | 14.18 | 14.18 | 14.18 | 14.18 | 14.18 |
| 145 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 |
| 146 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 | 16.28 |
| 147 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 148 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 | 15.60 |
| 149 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 | 11.28 |
| 150 | 13.14 | 13.14 | 13.14 | 13.14 | 14.59 | 14.59 | 14.59 | 14.59 | 14.59 | 14.59 |
| 151 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 | 16.03 |
| 152 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 | 10.38 |
| 153 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 | 10.20 |
| 154 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 155 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 | 6.74 |
| 156 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 |
| 157 | 13.92 | 13.92 | 13.96 | 13.96 | 13.96 | 13.97 | 13.97 | 13.97 | 13.97 | 13.97 |
| 158 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 | 14.20 |
| 159 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 | 16.29 |
| 160 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 | 42.27 |
| 161 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 | 15.00 |
| 162 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 163 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 | 22.95 |
| 164 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 | 14.50 |
| 165 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 | 80.27 |
| 166 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 | 34.02 |
| 167 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 | 6.04 |
| 168 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 | 45.23 |
| 169 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 | 15.50 |
| 170 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 | 12.00 |
| 171 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 | 26.90 |
| 172 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 | 17.93 |
| 173 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 | 18.04 |
| 174 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 | 15.06 |
| 175 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 | 10.37 |
| 176 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 | 17.20 |
| 177 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 | 15.88 |
| 178 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 | 16.80 |
| 179 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 | 12.80 |
| 180 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 | 60.16 |
| 181 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 | 59.49 |
| 182 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 | 55.84 |
| 183 | 18.33 | 18.33 | 18.44 | 18.44 | 18.44 | 18.45 | 18.45 | 18.45 | 18.45 | 18.45 |
| 184 | 15.95 | 15.95 | 16.01 | 16.01 | 16.01 | 16.01 | 16.01 | 16.01 | 16.01 | 16.01 |
| 185 | 13.62 | 13.62 | 13.70 | 13.70 | 13.70 | 13.71 | 13.71 | 13.71 | 13.71 | 13.71 |
| 186 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 | 20.40 |
| 187 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 | 16.04 |

The CORSAN municipalities charge by the exponential formula `PB × Cⁿ + SB` (section {{n:16}}), with no price per block; the exponent `n` is that of the category's column in the Exponent Table.

<!-- tabela: The CORSAN exponential formula in each tariff table and collected category -->
| Municipalities | Category | PB (R$/m³) | SB (R$/month) | Sewage (R$/m³) |
| :--- | :--- | ---: | ---: | ---: |
| Erechim (RS) | Residential | 6.95 | 32.95 | 4.86 |
| Erechim (RS) | Commercial | 7.90 | 58.79 | 5.53 |
| Erechim (RS) | Public | 7.90 | 117.40 | 5.53 |
| Santa Cruz do Sul (RS) | Residential | 7.91 | 37.50 | 5.53 |
| Canoas (RS), Esteio (RS) | Residential | 8.68 | 41.20 | 6.07 |
| Santa Cruz do Sul (RS) | Commercial | 8.98 | 66.92 | 6.28 |
| Santa Cruz do Sul (RS) | Public | 8.98 | 133.64 | 6.28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) and 27 more | Residential | 9.15 | 43.39 | 6.40 |
| Canoas (RS), Esteio (RS) | Commercial | 9.88 | 73.48 | 6.91 |
| Canoas (RS), Esteio (RS) | Public | 9.88 | 146.79 | 6.91 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) and 27 more | Commercial | 10.41 | 77.41 | 7.28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) and 27 more | Public | 10.41 | 154.64 | 7.28 |
| Alegrete (RS), Alvorada (RS), Bento Gonçalves (RS) and 27 more | Industrial | 11.83 | 154.64 | 8.28 |

