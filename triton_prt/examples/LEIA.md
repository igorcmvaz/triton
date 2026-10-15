# Projetos de exemplo (Edição Portugal)

Três projetos, uma edificação, três cidades. A edificação é a moradia do tutorial do manual, igual nas três
para que os resultados se comparem: 150 m² de cobertura (coeficiente de escoamento 0,85), 4 residentes,
150 L/hab·dia, 28% da procura não potável (autoclismos e usos exteriores), descarte das primeiras águas
de 2 mm, abastecimento por sobrepressor, varrimento de volumes até 20 000 L em passos de 1000 L.

| Ficheiro | Cidade | Chuva | Tarifário em vigor desde |
|---|---|---|---|
| `portugal/lisboa.triton` | Lisboa | E-OBS v33.0e, concelho de Lisboa, 1991–2020 (719 mm/ano) | 01/01/2026 |
| `portugal/porto.triton` | Porto | E-OBS v33.0e, concelho do Porto, 1991–2020 (1199 mm/ano) | 01/01/2026 |
| `portugal/funchal.triton` | Funchal | `data/rainfall/Funchal.csv`, reanálise ERA5 (538 mm/ano) | 01/01/2026 |

Os projetos são gerados por `scripts/gerar_exemplos_prt.py` (mesmas entradas, mesmos ficheiros) e
conferidos por `tests/unit/test_exemplos_da_edicao.py`, que refaz à mão cada fatura com os números impressos
nos tarifários. Os relatórios dos três exemplos (executivo, ambiental/ESG e dossiê técnico; PDF, em português
de Portugal) estão em `reports/exemplos/<cidade>/`, feitos por `scripts/gerar_relatorios_exemplo.py`.

**Os custos não estão definidos.** Custos de obra, de bomba, de tratamento e de manutenção ficam a zero: dependem
do local e do mercado, e não se usou fonte oficial para eles. Introduza os seus na etapa 5. Até lá, a análise
económica mostra apenas a poupança na fatura de água (o período de recuperação e o VAL dizem então pouco).
Cada projeto leva este aviso no bloco `analysis`. A tarifa de eletricidade só existe no Funchal (abaixo);
em Lisboa e no Porto o custo de bombagem fica a zero até o utilizador introduzir a sua.

A chuva do Funchal é reanálise ERA5 (célula de grelha de cerca de 9 km), não registo de estação:
a E-OBS não cobre o Funchal (22% de dias sem dados, acima do limite de 1%). Para um projeto real, use a série
medida (ver `data/rainfall/LEIA.md`).

**Por definir, de propósito:** não há CAPEX nem OPEX locais para estes exemplos, e nenhum foi inventado: custos de
cisterna, bomba, tubagem, mão de obra, manutenção e cloro ficam a zero (custos a informar pelo utilizador). O fator de
emissão da rede também não tem valor local: o projeto não define nenhum (vale o valor de partida do programa até
introduzir o seu). O período de recuperação e o VAL destes projetos **não são resultados**; os testes afirmam apenas a
poupança de água potável e a fatura de água.

## Tarifários (transcritos em `triton/data/portugal_tarifarios.json`)

Utilizador doméstico, tarifário geral, contador até 25 mm (Funchal: até 15 mm), meses de 30 dias. Os documentos
estão em `tarifas_portugal/fontes/` (fora do Git); o endereço de origem e o SHA-256 de cada um estão em
`tarifas_portugal/fontes/FONTES.tsv` (coletados em 07/10/2026).

| Cidade | Entidade | Documento | Endereço de origem | SHA-256 |
|---|---|---|---|---|
| Lisboa (água) | EPAL | Preços de venda de água, 1.ª edição 2026 | https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0 | `d0ebc13e306944db42fc96b57544ade72625478e99b5b0dc26d81fc6f0b5f42d` |
| Lisboa (saneamento) | Câmara Municipal de Lisboa | Tarifário do saneamento 2026 | https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf | `6c6295d9e5da3d09a7cd5476abe242757edd761b137359d5a4b561d1f080c37a` |
| Lisboa (resíduos) | Câmara Municipal de Lisboa | Tarifário dos resíduos urbanos 2026 | https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf | `7fa873127affb4e33306166292c9da937f0d68b39987a97ead767a866e32e54f` |
| Porto | Águas e Energia do Porto, EM | Tarifário Geral 2026 | https://www.aguasdoporto.pt/files/uploads/cms/Tarif%C3%A1rio%20Geral%202026.pdf | `7d6b5d0ceeef749d558018b4b1b24e661f3a415a1d55cab09f0de7aae340e0de` |
| Funchal | Câmara Municipal do Funchal | Tabela de Taxas e Outras Receitas Municipais 2026 | https://cmfdoc.funchal.pt/media/k2/attachments/Tabela_de_Taxas_Municipais_2026_.pdf (entregue pelo autor) | `97084c0265bfcb75c75e7b9e2d95aebab3417973f3cd0964b34696d3eea76f87` |

Faturas conferidas à mão (10 m³ e 30 m³ por mês; os testes pedem ainda 3, 18 e 60 m³):

| Cidade | 10 m³ | 30 m³ | IVA aplicado |
|---|---|---|---|
| Lisboa | 25,8683 € | 94,3767 € | 6% na água; sem IVA no saneamento e nos resíduos (como declara o tarifário) |
| Porto | 20,2995 € | 93,3293 € | 6% na água, no saneamento e na TRH |
| Funchal | 17,0872 € | 67,5272 € | 4% (a confirmar) |

### Hipóteses e dúvidas por confirmar

- **Lisboa.** O «Adicional C.M. Lisboa» (0,1483 €/m³) está impresso na tabela da EPAL sem dizer se leva IVA: tratado sem IVA.
  Saneamento e resíduos da Câmara sem IVA, posição da Autoridade Tributária contestada pela Provedora de Justiça (Público,
  05/12/2024).
- **Porto.** A disponibilidade de água de 0,1242 €/dia vem da pág. 2 do PDF (utilizadores domésticos); a pág. 3 repete a
  tabela com 0,1367 €/dia, lida como a dos não domésticos (inferência do layout; confirmar com a entidade). A TRH das águas
  residuais (0,0112 €/m³, pág. 4, bloco dos não domésticos) não foi incluída: pode valer também para os domésticos
  (+0,12 € a 10 m³). A taxa de 6% de IVA é a reduzida do Continente e não está impressa no PDF. Os resíduos são da
  Porto Ambiente e ficam fora.
- **Funchal.** O IVA de 4% **não foi confirmado** (nem a taxa, nem o diploma, nem a aplicação à água, ao saneamento e aos
  resíduos; com 5%, a fatura de 10 m³ passa de 17,0872 € para 17,2515 €): **o IVA da Madeira fica por confirmar**. O 1.º escalão
  (até 5 m³) do saneamento e dos resíduos não tem valor impresso: tratado como zero (pode ser isenção ou omissão da
  tabela). Os escalões variáveis dos resíduos foram somados aos do saneamento (o programa ainda não tem campo para resíduos por
  escalões): na interface, o «saneamento» do Funchal inclui os resíduos variáveis. A TRH não vem impressa (zero). Os
  escalões aplicam-se por faixa, como nos outros tarifários; a tabela não diz se o preço do escalão atingido vale para todo o
  volume.

## Eletricidade (só o Funchal)

Tarifa Base da EEM (Empresa de Eletricidade da Madeira), 6,90 kVA: **0,1673 €/kWh**, sem IVA, e 0,3386 €/dia de potência
contratada. Fonte: comparador luzegas.pt («Tarifas da eletricidade da Madeira»), atualizada em 20/02/2025 —
**fonte secundária**, não o tarifário da entidade (a confirmar na EEM/ERSE). Só o preço por kWh entra no projeto
(`elec_tariff`, para o custo de bombagem); a potência contratada paga-se com ou sem o sistema e não afeta a poupança.
O IVA da eletricidade não foi aplicado (preço sem IVA).
