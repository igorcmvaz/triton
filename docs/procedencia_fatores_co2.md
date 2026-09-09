# Procedência dos fatores de CO₂

**Documento de trabalho — em construção.** Registra, valor a valor, de onde vem
cada fator de emissão usado pelo módulo ambiental. Um valor só sai da condição de
«hipótese de triagem» quando esta tabela lhe der fonte, versão/ano, geografia e
fronteira do sistema.

Regra adotada: **nenhum número recebe fonte que não tenha sido recuperada e
lida**. Citar uma base pelo nome — «ICE», «Ecoinvent» — sem versão nem processo
não é procedência; é a aparência dela.

---

## Situação de partida

Levantamento de 2026-09-08 sobre `netuno/core/environmental.py` e
`netuno/core/environmental_justifications.py`:

- **32 valores** de CO₂ expostos pelo módulo.
- **Nenhum** com fonte primária. As duas únicas referências externas nomeadas
  (SIRENE para a rede elétrica, «famílias ICE/Ecoinvent» para os materiais) são
  *instruções de onde buscar*, não a origem do número usado.
- `environmental_justifications.py:420` (`_mark_as_screening`) sobrescreve em
  tempo de execução **toda** justificativa com «HIPÓTESE INTERNA DE TRIAGEM». O
  próprio programa declara que nada ali é auditado.

---

## Achado que muda a estratégia

A citação natural para coeficientes de carbono incorporado seria a base ICE
(*Inventory of Carbon and Energy*, Universidade de Bath). Ao recuperar o artigo:

> HAMMOND, G. P.; JONES, C. I. Embodied energy and carbon in construction
> materials. *Proceedings of the Institution of Civil Engineers — Energy*,
> v. 161, n. 2, p. 87–98, 2008. DOI 10.1680/ener.2008.161.2.87
> · acesso aberto (Bath PURE) · 997 publicações citantes

**A Tabela 2 do artigo publica seis materiais: tijolo, cimento, concreto, vidro,
aço e madeira.** Não publica plásticos. Portanto:

- **concreto** → o artigo serve como fonte;
- **PEAD, PVC, PRFV, inox** → o artigo **não** serve. Citá-lo para esses seria
  atribuição falsa. A planilha completa da ICE (v5, junho/2026) traz plásticos,
  mas é distribuída por formulário na Circular Ecology e não tem DOI — se for
  usada, precisa ser arquivada no repositório com a versão registrada.

Fontes primárias adequadas para o que a ICE não cobre por artigo:

| Material | Fonte primária a recuperar |
| :--- | :--- |
| PEAD, PVC | *Eco-profiles* da PlasticsEurope (cradle-to-gate, por kg de resina) |
| Aço inox AISI 304 | LCI do worldstainless / ISSF |
| PRFV | EuCIA *Eco Impact Calculator* ou artigo revisado por pares |
| Rede elétrica BR | SIRENE/MCTI, **com o ano explícito** e o arquivo arquivado |
| Água potável | inventário de concessionária ou artigo brasileiro |

---

## Referências já recuperadas e verificadas

| Chave | Registro | DOI | Recuperado por | Serve para |
| :--- | :--- | :--- | :--- | :--- |
| `hammond_jones_2008` | Hammond & Jones (2008), *Proc. ICE — Energy*, 161(2), 87–98 | 10.1680/ener.2008.161.2.87 | scite | concreto; metodologia de carbono incorporado |
| `ghimire_2014` | Ghimire, Johnston & Ingwersen (2014), *Environ. Sci. Technol.*, 48(7), 4069–4077 | 10.1021/es500189f | scite | ACV de sistemas de aproveitamento pluvial (acesso fechado) |
| `scolaro_ghisi_2025` | Scolaro & Ghisi (2025), *Sustainability*, 17(13), 5782 | 10.3390/su17135782 | OpenAlex | ACV de coberturas no Brasil |

---

## Tabela de conciliação (a preencher)

Formato: cada valor recebe origem completa ou permanece rotulado como triagem.

| Valor atual | Unidade | Local no código | Fonte | Fronteira | Situação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 3,00 | kg CO₂e/kg PEAD | `environmental.py:35` | — | — | **pendente** |
| 0,14 | kg CO₂e/kg concreto armado | `environmental.py:43` | — | — | **pendente** |
| 4,25 | kg CO₂e/kg PRFV | `environmental.py:51` | — | — | **pendente** |
| 2,89 | kg CO₂e/kg inox AISI 304 | `environmental.py:59` | — | — | **pendente** |
| 2,80 | kg CO₂e/kg PVC | `environmental.py:68–80` | — | — | **pendente** |
| 22 / 1200 / 20 / 38 | kg material/m³ útil | `environmental.py:34,42,50,58` | — | — | **pendente** |
| 11 valores | kg CO₂e/m de tubo por DN | `environmental.py:69–79` | — | — | **pendente** |
| 6 valores | kg CO₂e/motobomba por CV | `environmental.py:85–90` | — | — | **pendente** (4 dos 6 são extrapolação aritmética do valor de 0,5 CV) |
| ~~0,085~~ → **0,0461** | kg CO₂/kWh (rede BR) | `environmental.py` | MCTI/SIRENE, fator médio anual 2025 | geração do SIN, CO₂ apenas | ✅ **resolvido** — ver §Rede elétrica |
| 0,35 | kg CO₂e/m³ água potável | `environmental.py:167` | — | — | **pendente** |
| 25,0 | kg CO₂e/kg Cl₂ | `environmental.py:171` | — | — | **pendente** |
| 1,85 | kg CO₂e/kg hipoclorito | `water_quality.py:253` | «Ecoinvent v3.8» sem processo nem UUID | — | **pendente** |
| 0,40 | kWh/m³ (bomba) | `environmental.py:130` | — | — | **pendente** |
| 20 | anos (vida útil) | `environmental.py:175` | — | — | **pendente** |

---

## Rede elétrica — resolvido

**Fonte.** MCTI/SIRENE, *Fatores de emissão de CO₂ para inventários
corporativos* (fator médio de geração do Sistema Interligado Nacional).
Planilha `Inventario_2026_janjul.xlsx`, recuperada em 2026-09-08 de
<https://www.gov.br/mcti/pt-br/acompanhe-o-mcti/sirene/dados-e-ferramentas/fatores-de-emissao>,
arquivada em `data/fontes_externas/` com SHA-256 registrado. A série de
2006 a 2025 foi extraída por script — **nenhum valor foi redigitado** — para
`netuno/data/fatores_emissao_rede_mcti.json`.

**O que se descobriu.** O valor antigo, 0,085, não corresponde a ano nenhum da
série. Está próximo da faixa de 2016–2019 (0,074 a 0,093) e é **1,8×** o fator
de 2025. E o fator varia muito mais do que se supunha:

| Ano | kg CO₂/kWh | | Ano | kg CO₂/kWh |
| ---: | ---: | :-- | ---: | ---: |
| 2009 | 0,0246 *(mínimo)* | | 2021 | 0,1263 |
| 2014 | 0,1355 *(máximo)* | | 2023 | 0,0385 |
| 2020 | 0,0617 | | 2024 | 0,0545 |
| — | — | | **2025** | **0,0461** *(padrão adotado)* |

Entre o mínimo e o máximo há um fator de **5,5**. Um estudo que não declare o
ano do fator não é reproduzível, e comparar dois estudos com anos diferentes sem
dizê-lo não compara coisa alguma.

**Grandeza.** A série corporativa do MCTI é de **CO₂ apenas**, não de
CO₂-equivalente: metano e óxido nitroso da geração não entram. O campo do
programa chamava-se `grid_co2_factor_kg_kwh` e era descrito como CO₂e — a
descrição estava errada e foi corrigida.

**Fronteira.** Geração elétrica do SIN. Não inclui perdas de transmissão e
distribuição nem a cadeia a montante dos combustíveis.

**No código.** `netuno/core/grid_emission_factors.py` expõe `fator_anual(ano)`,
`fator_mensal(ano, mês)` e `procedencia()`. `EnvironmentalConfig` passou a
carregar o fator da série e a **declarar o ano** num campo próprio
(`grid_co2_factor_year`). O número 0,085 estava transcrito em oito lugares —
CLI (3), interface (4), teste (1) — e num deles ocupava o campo errado: era o
valor inicial da **energia específica da bomba** (kWh/m³), cujo padrão é 0,40.
A interface partia de um valor 4,7× menor que o do motor. Todos foram
substituídos por leitura da série, e o teste
`tests/unit/test_grid_emission_factors.py` impede o reaparecimento de qualquer
fator transcrito.

---

---

## Correção: CO₂ não é CO₂-equivalente

Uma versão intermediária deste trabalho trocou o fator da rede elétrica, 0,085,
pela série anual do MCTI/SIRENE (0,0461 kg CO₂/kWh em 2025). **Foi um erro de
grandeza, e está desfeito.** A série do MCTI cobre **CO₂ apenas** e apenas a
**geração**; uma ACV precisa de CO₂-equivalente e de fronteira que inclua
transmissão, distribuição, construção das usinas e as emissões biogênicas e de
uso da terra.

A diferença está medida em Vaz, Scolaro & Ghisi (2025), *Science of the Total
Environment*, 986, 179774 (DOI 10.1016/j.scitotenv.2025.179774), §3.6 e Fig. 11:
a intensidade sobe de cerca de 0,07 kg CO₂/kWh pela série do SIRENE para até
**0,20 kg CO₂e/kWh** quando os demais gases e processos entram na conta.

Bases documentadas, todas disponíveis em
`netuno.core.grid_emission_factors.bases_disponiveis()`:

| Base | kg/kWh | Gás | Origem |
| :--- | ---: | :--- | :--- |
| SIDAC | 0,070 | CO₂ | base de construção civil, reportada por Vaz et al. (2025), Fig. 11 |
| CaDI, Brasil | 0,074 | CO₂e | Carbon Database Initiative, reportada por Vaz et al. (2025), §3.6 |
| **Adotada pelo programa** | **0,085** | CO₂e | escolha declarada, entre o SIDAC e o percentil 5 do indicador fóssil de Vaz et al. |
| Vaz et al. 2025, fóssil, matriz 2022 | 0,104 | CO₂e | Tabela 5 ÷ ECHU de 2.121 kWh/domicílio·ano; faixa 0,075–0,146 |
| Vaz et al. 2025, total, matriz 2022 | 0,151 | CO₂e | idem, somando fóssil, biogênico e LULUC; faixa 0,108–0,214 |
| MCTI/SIRENE, 2025 | 0,046 | **CO₂** | série anual oficial — **não usar em ACV** |

Para comparação internacional, o CaDI reporta 0,166 kg CO₂e/kWh em Portugal,
0,375 nos Estados Unidos, 0,376 na Argentina, 0,380 na Alemanha e 0,661 na China.

O teste `test_o_fator_da_acv_nao_e_o_do_mcti` reprova se o fator da ACV algum dia
voltar a ser menor ou igual ao de CO₂ da geração — que é a assinatura exata deste
engano.

---

## Materiais: valores substituídos por fontes recuperadas

| Fator | Antes | Depois | Fonte | Fronteira |
| :--- | ---: | ---: | :--- | :--- |
| PEAD, resina | 3,00 | **1,612** | Franklin Associates para o American Chemistry Council (out/2020), Tabela 6 | berço-ao-portão da resina; TRACI 2.1 / IPCC 2013 GWP-100; EUA |
| PVC, tubo | 2,80 | **2,36** | EPD Australasia S-P-05503, RXP PVC Pipes (25/11/2022), Tabela 8, módulos A1–A3 | 1 kg de **tubo instalado**; EN 15804+A2 |

Duas observações sobre a escolha:

1. **O PEAD não se explica por fronteira.** A decomposição interna anterior
   declarava extração e refino, polimerização e transporte — exatamente a
   fronteira do relatório do ACC. O valor antigo simplesmente superestimava a
   resina em cerca de 86%.
2. **Para o PVC preferiu-se a EPD ao valor de resina.** O American Chemistry
   Council publica 2,095 kg CO₂e/kg de *resina*; a EPD publica 2,36 kg CO₂e/kg de
   *tubo instalado*, já com composto e extrusão. É o tubo que se instala, não a
   resina. Outras linhas da mesma EPD vão de 2,36 a 2,73.

**Impacto**, para uma cisterna de 5.000 L em PEAD, 45 m de tubulação, bomba de
1/2 CV e 100 m³/ano aproveitados:

| Saída | Antes | Depois | Variação |
| :--- | ---: | ---: | ---: |
| CO₂ incorporado da cisterna | 330,0 kg | 177,3 kg | −46,3% |
| CO₂ incorporado das tubulações | 96,6 kg | 81,4 kg | −15,7% |
| CO₂ incorporado total | 444,6 kg | 276,7 kg | −37,8% |
| Payback ambiental | 14,1 anos | 8,8 anos | −37,8% |
| Economia líquida em 20 anos | 187,4 kg | 355,3 kg | **+89,6%** |

Os sistemas pluviais saem substancialmente melhores na ACV do que a versão
anterior indicava. Estudos ambientais feitos com o Netuno até a 5.0.7
**subestimavam** o benefício de carbono, e a diferença não é marginal.

**Ressalva de escopo, que precisa acompanhar qualquer publicação.** As duas
fontes são norte-americana e australasiana. A resina consumida no Brasil tem
matriz elétrica e cadeia de matéria-prima próprias. Para um estudo definitivo,
prefira a EPD do fabricante efetivamente empregado.

---

## Água potável evitada: valor corroborado

Os 0,35 kg CO₂e/m³ deixam de ser hipótese solta. Garfí, Cadena, Sanchez-Ramos &
Ferrer (2016), *Journal of Cleaner Production*, 137, 997–1003
(DOI 10.1016/j.jclepro.2016.07.218), com unidade funcional de 1 m³, dão
**0,512 kg CO₂e/m³** para tratamento convencional acrescido de osmose reversa
doméstica no caso base; o tratamento convencional sozinho fica abaixo disso
(Fig. 1d). Os 0,35 adotados caem dentro da faixa.

Continua sendo uma corroboração de ordem de grandeza, não um inventário da
concessionária local. Para publicação, o ideal é o inventário da CASAN.


---

## Versão 5.0.8 — tubulações e reservatórios com dados de fabricante

### Massa linear dos tubos

Era a maior lacuna quantitativa que restava, e o erro não era pequeno nem
sistemático.

| DN | kg/m antes | kg/m agora | Erro do valor antigo | Origem do novo valor |
| ---: | ---: | ---: | ---: | :--- |
| 20 | 0,180 | 0,132 | +36% | peso real Amanco Wavin |
| 25 | 0,240 | 0,189 | +27% | peso real Amanco Wavin |
| 32 | 0,340 | 0,299 | +14% | peso real Amanco Wavin |
| 40 | 0,440 | 0,427 | +3% | peso real Amanco Wavin |
| 50 | 0,550 | 0,668 | −18% | peso real Amanco Wavin |
| 60 | 0,700 | 0,884 | −21% | peso real Amanco Wavin |
| 75 | 0,950 | 1,412 | −33% | geometria NBR 5648 |
| 85 | 1,150 | 1,792 | −36% | geometria NBR 5648 |
| 100 | 1,400 | 1,176 | +19% | geometria NBR 5688, série reforçada |
| 110 | 1,600 | 3,009 | **−47%** | geometria NBR 5648 |
| 150 | 2,800 | 2,502 | +12% | geometria NBR 5688, série reforçada |

**Fontes.** Peso de produto: ficha técnica FTC000021 da Amanco Wavin, revisão de
outubro de 2025, linha Soldável Água Fria, tubo ponta-bolsa de 6 m. Geometria de
pressão: ABNT NBR 5648, diâmetro externo e espessura de parede. Geometria de
drenagem: ABNT NBR 5688:2018, Tabela 1, série reforçada — que é a série que a
própria norma destina à água pluvial.

**Método.** Os seis pesos reais implicam densidade efetiva de **1,511 g/cm³**,
com dispersão de apenas 1,504 a 1,516. Essa consistência é o que valida o
método: a mesma densidade, aplicada à seção anular dos diâmetros sem peso
publicado, estende a tabela sem inventar nada. A densidade é maior que a do
PVC-U puro porque incorpora a massa da bolsa, que o tubo comercial traz.

**Por que o DN 100 é mais leve que o DN 85.** Não é erro. São normas e serviços
distintos: o DN 85 é tubo de pressão com parede de 4,7 mm, e o DN 100 é tubo de
drenagem com parede de 2,5 mm. O teste de monotonia foi escrito por família, e
não globalmente, justamente por isso.

### Massa dos reservatórios em PRFV

O programa usava densidade constante de 20 kg por m³ útil. O catálogo Fortlev
mostra economia de escala clara, e o erro cresce com o porte:

| Capacidade | Massa real | Modelo antigo | Erro |
| ---: | ---: | ---: | ---: |
| 1.000 L | 20,3 kg | 20,0 kg | −2% |
| 2.000 L | 34,8 kg | 40,0 kg | +15% |
| 5.000 L | 74,9 kg | 100,0 kg | +34% |
| 10.000 L | 136,7 kg | 200,0 kg | **+46%** |
| 20.000 L | 278,1 kg | 400,0 kg | +44% |

A massa passa a ser interpolada da tabela do fabricante. Fora da faixa tabelada,
extrapola-se pela densidade do extremo mais próximo, porque extrapolação linear
da curva daria massa negativa para volumes pequenos.

### Concreto, corroborado por inventário brasileiro

O SIDAC publica, para concreto dosado em central, de cerca de 310 kg CO₂/m³ a
20 MPa até cerca de 480 a 40 MPa. O fator do programa, 0,14 kg CO₂e/kg, equivale
a **336 kg CO₂/m³** a 2.400 kg/m³, e cai dentro da faixa de um concreto de 25 a
30 MPa. Deixa de ser cenário interno e passa a ter corroboração nacional.

### Massa dos reservatórios em polietileno

Especificações de fabricante consultadas na internet dão 10,1 a 10,5 kg num
reservatório de 500 L, 17,0 a 17,5 kg num de 1.000 L e 34,0 a 34,5 kg num de
2.000 L — ou seja, entre 17 e 21 kg/m³. Um reservatório de 5.000 L aparece com
111 kg, o que dá 22 kg/m³ e quebra a tendência, provavelmente por incluir tampa
ou embalagem. **Os dados não são consistentes o bastante para virar tabela**, e
os 22 kg/m³ do programa permanecem, agora dentro da faixa observada em vez de
sem referência nenhuma.

---

## Cloração: três convenções incompatíveis, unificadas

Não eram duas contas divergentes, eram três, e nenhuma podia concordar com as
outras porque as bases eram diferentes:

| Módulo | Dose | Base do fator | Resultado |
| :--- | :--- | :--- | ---: |
| Ambiental | 2,0 mg/L | por kg de Cl₂ puro, fator 25,0 | 0,0500 kg CO₂e/m³ |
| Qualidade | 1,5 mg/L | por kg de pastilha a 65%, fator 1,85 | 0,0043 kg CO₂e/m³ |
| Econômico | 2,0 mg/L | cobrava o preço sobre cloro ativo | subestimava o custo em 35% |

O fator de 25,0 kg CO₂e/kg saiu. Não tinha fonte, é implausível por uma ordem de
grandeza para cloro de rota cloro-álcali, e era **idêntico** ao
`chlorine_cost_per_kg = 25,00` (R$/kg) do `costs_database.json`. A coincidência
com o preço denuncia a origem do engano.

A cadeia única está em `netuno/core/chlorination.py`: a dose é de cloro ativo, o
fator é por quilo de produto comercial, e a pureza faz a ponte entre os dois. Os
três módulos passaram a usá-la.

---

## Linha de tratamento: erro conceitual corrigido

O programa tratava cloro, ultravioleta e ozônio como escolhas mutuamente
exclusivas, e ainda admitia «sem desinfecção». Isso contraria a própria norma: o
item 4.6.5 da NBR 15527:2019 trabalha com cloro **residual livre**, e residual é
proteção continuada dentro do reservatório e da rede. Ultravioleta e ozônio
desinfetam na passagem e não deixam residual nenhum — somam-se à cloração, não a
substituem.

A cloração passou a ser sempre aplicada, e as demais barreiras entram como
estágios adicionais. Corrigiu-se junto um defeito que fazia o reator UV aparecer
quase de graça: a energia era calculada e não entrava nem no custo operacional
nem na emissão.

---

## Situação por fator, em 2026-09-08

| Grupo | Valores | Situação |
| :--- | ---: | :--- |
| Rede elétrica | 1 | ✅ resolvido — base de CO₂e declarada; série do MCTI mantida à parte, rotulada como CO₂ |
| Materiais de reservatório | 8 | 🟡 parcial — PEAD (ACC 2020) e concreto (SIDAC) resolvidos; massa do PRFV do catálogo Fortlev; fator do PRFV e o inox pendentes |
| Tubulações | 12 | ✅ resolvido — fator da EPD Australasia S-P-05503; massas lineares de peso de produto (Amanco Wavin) e das NBR 5648 e 5688 |
| Motobombas | 6 | ⬜ pendente — quatro dos seis são extrapolação aritmética; a granularidade por CV pode não existir na literatura |
| Água potável evitada | 1 | 🟡 corroborado por Garfí et al. (2016); falta inventário da concessionária |
| Cloro e hipoclorito | 3 | 🟡 cadeia unificada e fator implausível removido; falta o processo exato do Ecoinvent |
| Vida útil e energia específica | 2 | ⬜ pendente — ver nota abaixo |

### Nota: energia específica de bombeamento (0,40 kWh/m³)

Vieira, Beal, Ghisi & Stewart (2014, DOI 10.1016/j.rser.2014.03.012, texto integral
recuperado) publicam, para sistemas reais de aproveitamento pluvial:

| Configuração | kWh/m³ |
| :--- | ---: |
| Mediana dos estudos empíricos revisados | 1,40 |
| Recalque direto, média (faixa 2,00–3,90) | 2,95 |
| Com desinfecção UV, média (faixa 4,60–5,70) | 5,10 |
| Abastecimento público, mediana | 0,48 |
| Sistemas por gravidade com reservatório elevado | ≈ 0 (neutros) |

O padrão do Netuno, **0,40 kWh/m³**, fica abaixo da mediana revisada e até do
abastecimento público. Só é defensável para o arranjo indireto — cisterna inferior
recalcando para reservatório superior, com altura manométrica pequena —, que é
justamente o arranjo brasileiro corrente e o que o programa modela por padrão. Falta
declarar isso ao lado do número, e oferecer os valores de recalque direto como
alternativa selecionável.

### Nota: água potável evitada (0,35 kg CO₂/m³)

Uma verificação de ordem de grandeza: se o abastecimento público consome
0,48 kWh/m³ (Vieira et al., 2014) e a rede brasileira emitiu 0,0461 kg CO₂/kWh em
2025 (MCTI), a parcela **energética** da emissão da água tratada é de cerca de
**0,022 kg CO₂/m³** — dezesseis vezes menor que os 0,35 adotados. A diferença não
invalida o valor: 0,35 presumivelmente abrange produtos químicos, infraestrutura e
tratamento, não só bombeamento. Mas mostra que o número **não** pode ser justificado
pela energia, e que precisa de um inventário completo de concessionária para se
sustentar.

---

## Defeitos encontrados durante o levantamento

Independem da procedência e devem ser corrigidos:

1. ✅ **`tab_environmental.py`** — `QLineEdit("0.085")` para a energia
   específica da bomba (kWh/m³), quando o padrão do modelo é **0,40**. Era o fator
   da rede elétrica, copiado da linha seguinte: divergência de 4,7×. **Corrigido**;
   o campo agora nasce de `PumpInput.specific_kwh_per_m3`.
2. ✅ **`charts.py`** — 0,35 kg CO₂e/m³ estava *hardcoded*: editar o fator na
   interface não alterava o gráfico de balanço. **Corrigido**; o gráfico recupera o
   fator efetivamente usado a partir do resultado da ACV.
3. **`water_quality.py:269`** — `uv_kwh` é calculado e não entra em
   `disinf_opex` nem em `total_etap_co2e_kg_yr`. O reator UV aparece sem custo
   nem emissão de energia.
4. **`costs_database.json:86`** — `chlorine_cost_per_kg: 25.00` (R$/kg) é
   numericamente idêntico a `chlorine_co2_kg_per_kg = 25.0` (kg CO₂e/kg).
   Grandezas distintas com o mesmo número, o que confunde qualquer auditoria.
