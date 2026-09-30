# Base tarifária auditada — fontes, escopo e confiança

Data de corte: **24 de agosto de 2026**.

## Arquivos canônicos

- `tarifas_detalhadas_auditadas.csv`: 3.604 registros por município e faixa de consumo. É a entrada canônica para o cálculo das contas.
- `catalogo_tarifas_auditado_652.csv`: uma linha por município, com primeira faixa, parcela fixa, esgoto, energia, fontes e confiança.
- `catalogo_tarifas_auditado_652.xlsx`: versão para inspeção humana, com abas de dados, metodologia, fontes e resumo de qualidade.
- `validated_cidades_50k.json`: coordenadas utilizadas pelos mapas; não contém tarifas.

## Fontes oficiais

1. **Energia elétrica — ANEEL:** base aberta “Tarifas de aplicação das distribuidoras de energia elétrica”, gerada e consultada em 24/08/2026:  
   https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4
2. **Definição do escopo da tarifa ANEEL:** o ranking e a base homologada são expressos em R$/kWh e **não incluem** ICMS, PIS/Pasep, Cofins, COSIP nem bandeiras:  
   https://www.gov.br/aneel/pt-br/centrais-de-conteudos/relatorios-e-indicadores/tarifas-e-informacoes-economico-financeiras
3. **Saneamento — SINISA/Ministério das Cidades:** referência nacional para prestadores e indicadores; as estruturas tarifárias vigentes foram verificadas nas páginas dos prestadores e agências registradas em cada linha:  
   https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa/resultados-sinisa
4. **Tarifa Social — ANA:** verificação cruzada da identidade de prestadores e reguladores aderentes:  
   https://www.gov.br/ana/pt-br/assuntos/saneamento-basico/tarifa-social-de-agua-e-esgoto/lista-positiva/lista-positiva-1
5. **Exemplos de verificação direta de estruturas tarifárias vigentes:**
   - CAESB/ADASA, vigência 01/06/2026–31/05/2027: https://s3.caesb.df.gov.br/www/prod/site1/Tabela-01-06-2026-a-31-05-2027.pdf
   - CASAN, valores desde 01/04/2026: https://www.casan.com.br/menu-conteudo/index/url/tarifas
   - SANEPAR/AGEPAR, tabela 2026: https://www.sanepar.com.br/tarifas
   - Águas de Manaus/AGEMAN: https://www.aguasdemanaus.com.br/legislacao-e-tarifas/
   - CORSAN/AGERGS, tabelas por município em 2026: https://www.corsan.com.br/sistematarifario/
     A CORSAN fatura a água por `PB × Cⁿ + serviço básico`, e não por faixas. No banco, a
     fórmula usa os códigos `2` (preço-base) e `3` (Tabela de Exponenciais, transcrita da
     CORSAN em `tarifas/tabela_exponencial_corsan.json`, aplicada por
     `scripts/aplicar_tarifa_exponencial.py`). O esgoto é cobrado por m³ consumido
     (`esgoto_modo` 2, `esgoto_r_m3`), sem serviço básico nem expoente.
   - SANESUL/AGEMS, repositório de estruturas 2026: https://www.sanesul.ms.gov.br/evolucao-tarifaria
   - AGRESE/DESO, estruturas tarifárias autorizadas: https://agrese.se.gov.br/estrutura-tarifaria-autorizada/
   - MRAE/AGRESPI, identificação da concessionária Águas do Piauí: https://mrae.sead.pi.gov.br/institucional/governanca/concessionaria-aguas-do-piaui/
   - CAGECE/ARCE, tabela residencial vigente desde 05/11/2025: https://www.cagece.com.br/produtos-e-servicos/precos-e-prazos/estrutura-tarifaria/
   - SANEAGO/AGR-AR, Resolução Conjunta nº 1/2026: https://www.saneago.com.br/2026/arquivos/Res_Normativa_Conjunta_AGR_AR_01_2026.pdf
   - COMPESA/ARPE, estrutura homologada pela Resolução nº 289/2025: https://www.arpe.pe.gov.br/images/COORDENADORIAS/TARIFAS/SANEAMENTO/Estrutura-Tarifria-Compesa-2025---Resoluo-ARPE-n-289-2025.pdf
   - COSANPA, tabela aplicada desde 28/11/2023: https://www.cosanpa.pa.gov.br/wp-content/uploads/2018/05/Tarifa_Novembro_2023.pdf
   - Itabirito/SAAE, Resolução ARISB-MG nº 406/2026: https://www.arisb.com.br/imgeditor/file/RES_406_2026_ARISB_MG_Reajuste_Itabirito_assinada.pdf
   - Uberaba/CODAU, Resolução ARISB-MG nº 383/2026: https://www.arisb.com.br/imgeditor/file/Resolu%C3%A7%C3%A3o%20383%20-%20Rev1.pdf
   - Sete Lagoas/SAAE, tabela do Decreto nº 7.702/2026: https://www.saaesetelagoas.com.br/documentos-e-anexos/415-tabela-de-tarifas-03-03-2026/file
   - Lucas do Rio Verde/SAAE, tabela oficial 2026: https://saae.lucasdorioverde.mt.gov.br/site/tarifas
   - Pontes e Lacerda/Norte Saneamento, estrutura tarifária 2026: https://5bffdcd3-acd1-40b3-a6ad-b27e6176bd71.filesusr.com/ugd/4b7c39_6e231a86fe124123986c8a503ce2aa26.pdf
   - Cáceres/Águas do Pantanal, tabela oficial: https://www.aguasdopantanal.eco.br/Informacoes-ao-consumidor/Tabela-tarifaria/
   - Teresópolis/Águas da Imperatriz, Deliberação AGENERSA nº 4.995/2026: https://www.rj.gov.br/agenersa/sites/default/files/arquivos_paginas_basicas/DELIBERACAO_AGENERSA_NA___4995_1.pdf
   - Cuiabá/Águas Cuiabá, histórico tarifário oficial vigente desde 20/03/2025: https://igua.com.br/storage/e3/69/85/historico-das-tarifa-urkqd.pdf

## Regra de uso

O cálculo econômico deve usar a **estrutura completa por faixas**, incluindo parcela fixa/TBO/TFDI, tarifa marginal de água, tarifa de esgoto e número de economias. A coluna de “primeira faixa” é descritiva; não substitui a função de faturamento progressivo.

A denominação das distribuidoras foi conciliada nos 652 municípios. Em 578, o CSV aberto da ANEEL contém ato vigente na data de corte. Nos 74 restantes, o arquivo gerado em 24/08/2026 ainda apresenta como referência numérica mais recente um ato expirado: 42 linhas da Equatorial Pará há 18 dias, 30 da CELESC há 3 dias e 2 da Sulgipe há 95 dias. A própria ANEEL já noticiou novos processos para essas distribuidoras em 2026, mas a auditoria não converteu percentuais de reajuste em TUSD+TE: aguarda-se a inclusão das tabelas de aplicação no conjunto aberto ou o respectivo anexo homologatório. As referências antigas permanecem identificadas e penalizadas, nunca apresentadas como vigentes.

No Piauí, o operador foi atualizado de AGESPISA para **Águas do Piauí**, conforme o Contrato de Concessão nº 648/2024 e a transferência operacional de 2025. A tabela vigente foi posteriormente conciliada no catálogo; não restam registros C ou D.

## Escala de confiança

- **A — alta (85–100):** evidência primária específica, atual, estrutura completa e conciliação documentada.
- **B — boa (70–84,9):** evidência oficial suficiente, mas URL genérica, vigência sem data completa ou uma dimensão não conciliada.
- **C — moderada (50–69,9):** valor plausível e fonte institucional, porém histórico, derivado ou sem conciliação vigente completa.
- **D — baixa (<50):** fallback, fonte pouco específica ou inconsistência que exige validação manual antes de decisão local.

Resultado em 24/08/2026: **620 municípios A e 32 B na confiança global**, sem C ou D. No componente saneamento são **586 A e 66 B**; no componente energia, **578 A e 74 B**. Nesta rodada final, oito municípios subiram de B para A em saneamento por conciliação numérica com atos/tabelas oficiais: Lucas do Rio Verde, Pontes e Lacerda, Cáceres, Teresópolis, Cuiabá, Itabirito, Uberaba e Sete Lagoas. Os B remanescentes foram mantidos quando faltava a matriz numérica completa, a confirmação da cobertura local ou uma referência ANEEL ainda vigente na data de corte.

O escore global é `60% saneamento + 40% energia`. O saneamento soma autoridade/especificidade da evidência (35 pontos), atualidade (20), conciliação numérica (25), completude da estrutura (15) e consistência do operador (5), com penalizações de fallback e transição não reconciliada. A energia considera conciliação com a ANEEL, diferença relativa e vigência do ato. Uma página oficial localizada não é tratada como prova de que o número foi reconciliado.

## Limitações

- Tarifas mudam por resolução e devem ser reauditadas antes de uma nova rodada de simulações.
- A base ANEEL não inclui tributos nem bandeiras; adicionar esses componentes exige cenário tributário estadual e temporal próprio.
- A cobrança de esgoto pode depender da existência do serviço no imóvel. O estudo modela a alíquota regulatória informada, não a cobertura efetiva de cada ligação.
- Condomínios devem ser faturados pelo número de economias previsto pela prestadora, evitando aplicar o consumo agregado do edifício como se fosse uma única economia.

Reprodução: execute `scripts/audit_tariffs.py` após atualizar a cópia oficial da ANEEL em `tmp/aneel_tarifas_homologadas_2026.csv`.
