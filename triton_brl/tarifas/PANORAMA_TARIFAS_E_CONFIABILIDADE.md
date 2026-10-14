# Panorama nacional das tarifas e da confiabilidade

Data de corte: **24 de agosto de 2026**. Universo: **652 municípios** e **3.604 registros tarifários detalhados**.

## Resultado executivo

| Componente | A — alta | B — boa | C — moderada | D — baixa |
|---|---:|---:|---:|---:|
| Saneamento | 586 (89,9%) | 66 (10,1%) | 0 | 0 |
| Energia elétrica | 578 (88,7%) | 74 (11,3%) | 0 | 0 |
| Confiança global | 620 (95,1%) | 32 (4,9%) | 0 | 0 |

O grau global é a média ponderada de **60% saneamento + 40% energia**. Por isso, um município pode ter um componente B e ainda obter grau global A. O catálogo preserva os três escores para que essa composição seja transparente.

## Significado das classificações

- **A — alta (85 a 100):** conjunto de evidências forte para uso no estudo. Há fonte institucional específica, atualidade, estrutura tarifária e/ou reconciliação numérica suficientes para superar 85 pontos. Como o escore é aditivo, A não significa que todas as dimensões sejam perfeitas; a coluna de reconciliação deve ser consultada junto com o grau.
- **B — boa (70 a 84,9):** dado utilizável em análises agregadas, mas com ressalva material identificada — por exemplo, matriz numérica ainda não reconciliada, página oficial genérica, ato antigo, cobertura/prestador local a confirmar ou referência ANEEL recém-expirada.
- **C — moderada (50 a 69,9):** evidência institucional incompleta, histórica ou derivada; exige validação antes de sustentar conclusão municipal.
- **D — baixa (abaixo de 50):** fallback ou inconsistência relevante; não deve sustentar decisão local sem nova pesquisa.

Não há registros C ou D nesta versão.

## Panorama dos valores

- **Água, primeira faixa volumétrica:** valor disponível em 646 municípios; mediana de **R$ 5,60/m³**, intervalo interquartil de **R$ 3,05 a R$ 6,77/m³**.
- **Parcela fixa/mínima de água:** valor positivo em 483 municípios; mediana condicional de **R$ 40,42/mês**.
- **Água + esgoto na primeira faixa volumétrica:** mediana de **R$ 8,838/m³**. Esse indicador só compara parcelas volumétricas; não é a conta mensal completa.
- **Energia residencial B1 homologada pela ANEEL, sem tributos e bandeiras:** mediana de **R$ 0,842285/kWh**, mínimo de **R$ 0,61757/kWh** e máximo de **R$ 1,06110/kWh**.

| Região | Municípios | Água volumétrica mediana (R$/m³) | Fixa positiva mediana (R$/mês) | Água + esgoto mediana (R$/m³) | Energia mediana (R$/kWh) | Saneamento A |
|---|---:|---:|---:|---:|---:|---:|
| Centro-Oeste | 44 | 5,77 | 17,46 | 5,7700 | 0,8918 | 90,9% |
| Nordeste | 173 | 6,77 | 44,77 | 12,1860 | 0,7989 | 99,4% |
| Norte | 71 | 4,91 | 32,50 | 8,8380 | 0,9783 | 81,7% |
| Sudeste | 255 | 5,11 | 40,42 | 6,8494 | 0,7960 | 82,0% |
| Sul | 109 | 3,08 | 46,34 | 6,1600 | 0,7680 | 98,2% |

As medianas regionais não são uma comparação de contas finais. Prestadores usam combinações diferentes de consumo mínimo, tarifa fixa, faixas progressivas, parcelas a deduzir, número de economias e cobrança de esgoto.

## Reconciliação e ressalvas remanescentes

No saneamento, 389 municípios estão marcados como **SIM** na conciliação numérica, 220 como **PENDENTE** e 43 como **NÃO**. Entre os 66 municípios classificados como B, 43 têm fonte primária localizada mas números não conciliados integralmente e 23 estão pendentes. A distribuição dos B é: RJ 18, SP 14, MG 12, AM 11, MT 4, ES 2, RS 2, AL 1, RO 1 e RR 1.

Na energia, os 74 B decorrem exclusivamente de a base aberta da ANEEL ainda não apresentar um ato vigente na data de corte para três distribuidoras: **42 municípios da Equatorial Pará** (referência 18 dias expirada), **30 da CELESC** (3 dias) e **2 da Sulgipe** (95 dias). O catálogo mantém o valor oficial mais recente, identifica-o como expirado e não aplica percentuais noticiados sem a matriz homologada de TUSD + TE.

## Promoções desta rodada

Oito municípios subiram de B para A no saneamento após conferência e correção numérica em fonte oficial:

| Município | Prestador | Evidência conciliada |
|---|---|---|
| Lucas do Rio Verde/MT | SAAE | seis faixas residenciais de 2026; esgoto a 80% |
| Pontes e Lacerda/MT | Norte Saneamento | cinco faixas residenciais de 2026 |
| Cáceres/MT | Águas do Pantanal | cinco faixas; esgoto a 50% |
| Teresópolis/RJ | Águas da Imperatriz | cinco faixas da Deliberação AGENERSA nº 4.995/2026 |
| Cuiabá/MT | Águas Cuiabá | cinco faixas vigentes desde 20/03/2025; esgoto a 90% |
| Itabirito/MG | SAAE | 12 faixas, tarifa básica operacional e esgoto a 60% na Resolução ARISB-MG nº 406/2026 |
| Uberaba/MG | CODAU | sete faixas e esgoto a 95% na Resolução ARISB-MG nº 383/2026 |
| Sete Lagoas/MG | SAAE | mínimo residencial de 6 m³ e esgoto a 80% na tabela do Decreto nº 7.702/2026 |

## Como usar os arquivos

- `tarifas_detalhadas_auditadas.csv`: base para simulação, com todas as faixas disponíveis.
- `catalogo_tarifas_auditado_652.csv`: panorama completo, uma linha por município, incluindo valores, fontes, alertas e escores.
- `catalogo_tarifas_auditado_652.xlsx`: versão navegável com resumo, metodologia e links.
- `FONTES_E_METODOLOGIA.md`: fontes oficiais e regra de pontuação.

Para cálculo financeiro, usar as faixas detalhadas. A “primeira faixa” do catálogo serve para inspeção e comparação descritiva, não substitui a função tarifária integral. A cobrança de esgoto também depende da disponibilidade efetiva do serviço no imóvel.
