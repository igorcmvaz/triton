# Tarifários da Edição Ibérica (POR)

Documentos oficiais das entidades gestoras, um por pasta em `fontes/<entidade>/`, para
transcrever na fatura portuguesa (`triton/core/fatura_portuguesa.py`). Fica separado de
`tarifas/` de propósito: `tarifas/processar_entrada.py` identifica prestadores brasileiros
pelo nome e atribuiria «Porto» ou «Santarém» a municípios homônimos do Brasil.

`fontes/FONTES.tsv` traz, por arquivo: caminho, endereço de origem, SHA-256 e data da
coleta. Todo PDF foi conferido (começa com `%PDF`); toda página HTML, conferida como não
sendo página de erro.

## Coletados em 07/10/2026

| Capital | Entidade | Documento |
| :--- | :--- | :--- |
| Lisboa | EPAL | preços 2026 (só água; saneamento e resíduos são da Câmara) |
| Porto | Águas e Energia do Porto | tarifário geral 2026 |
| Coimbra | Águas de Coimbra | água, águas residuais, editais n.º 433 e 438/2025 (resíduos e 2026) |
| Braga | AGERE | tarifário fev. 2026 |
| Setúbal | SMS Setúbal | água, saneamento e resíduos 2026 |
| Leiria | SMAS Leiria | tarifário 2026 |
| Faro | FAGAR | tarifário 2026 |
| Aveiro | AdRA | tarifário 2026 |
| Viseu | Águas de Viseu | tarifários abr. 2026 |
| Beja | EMAS Beja | tarifário 2025 (em vigor desde 01/01/2025) |
| Évora | Câmara de Évora | tarifário 2025 (em vigor desde fev. 2025) |
| Castelo Branco | SM Castelo Branco | tarifário em vigor (publicado em 24/02/2026) |
| Santarém | Águas de Santarém | páginas do tarifário geral e do saneamento 2026 |
| Ponta Delgada | SMAS Ponta Delgada | tarifário 2026 |

## Entregues pelo autor em 07/10/2026

| Capital | Documento | Situação |
| :--- | :--- | :--- |
| Viana do Castelo | Águas do Alto Minho, cartaz do tarifário 2026 (água e saneamento) | oficial; saneamento = 90% da tarifa variável de água |
| Portalegre | SMAT, edital 2026 em imagens, páginas 1–5 (em vigor desde 01/01/2026) | completo; água 1–3, saneamento por escalões e TRH na 4, ligações na 5; **sem resíduos** no edital |
| Guarda | Câmara, Edital n.º 16/2026 (em vigor desde 09/02/2026) | oficial, digitalizado; água, saneamento por escalões e resíduos numa tabela (pág. 2): renderizar em alta resolução para transcrever |
| Vila Real | ADIN, Tarifas 2026 (água e saneamento, ambos por escalões, TRH) + Câmara, tarifário de resíduos 2026 | oficiais |
| Lisboa | Câmara, tarifário do saneamento 2026 (por escalões) e de resíduos urbanos 2026 | oficiais; completam a água da EPAL |
| Funchal | Câmara, Tabela de Taxas Municipais 2026 | oficial; resíduos (sec. II) e saneamento (sec. IV) com parte por m³ em escalões; conferir se a água está no cap. III |
| Bragança | Edital n.º 68/2020 da Câmara (água, águas residuais e RSU), reproduzido na ficha do estudo da APFN | oficial, mas em vigor desde jan. 2021; falta o tarifário atual |

Secundários (`_secundarios/`, para conferir, nunca transcrever): ficha APFN do Funchal
(2024) e ficha APFN de Bragança (2018, anterior ao edital de 2020).
`_fora_do_tema/` guarda um artigo sobre o IPI brasileiro que veio junto, por engano.
Repetidos que saíram (mesmo SHA-256): `preços-2026.pdf` (= EPAL), `page-0001 (1).jpg`,
`Tarifas-2026 (1).pdf` e uma segunda cópia da `page-0004.jpg` de Portalegre.

## Pendentes

Bragança: tarifário em vigor (o site da Câmara recusa conexão automática).

## Antes de transcrever

- Ler cada documento inteiro, inclusive notas de rodapé sobre IVA e resíduos indexados.
- Taxa de IVA: a do próprio documento; se ele só disser «à taxa legal», buscar no Código
  do IVA em fonte oficial e citar.
- Saneamento por escalões ainda não tem campo no motor: a transcrição deve parar e avisar.
  É a regra, não a exceção: Portalegre, Guarda, Vila Real (ADIN), Lisboa e Funchal cobram
  saneamento (e, no Funchal, resíduos) por escalões de m³ de água; a Águas do Alto Minho
  cobra 90% da tarifa variável da água. O motor precisa das duas formas antes da transcrição.
