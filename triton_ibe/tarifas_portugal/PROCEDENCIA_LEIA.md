# Procedência e confiança dos tarifários por concelho: como retomar

Feito em 23/10/2026, na branch `feature/ibe-qualidade` (sem commit, sem push). A edição continua a chamar-se `triton_ibe` / `IBE` no código; a troca do nome é uma etapa à parte.

## O esquema (consenso do debate interno da IBE, de 23/10/2026; o registo do debate não é público)

Três estados, por concelho **e por serviço** (água, saneamento, resíduos urbanos), só para o utilizador doméstico.

| Estado | Exigências |
| :--- | :--- |
| verde, verificado | documento oficial arquivado com URL e SHA-256; `confirmado_em` há menos de 12 meses; transcrição conferida com as contas impressas (o teste reproduz); verificação **independente** em `verificado_por` (`fatura` ±0,05 € ou `humano`, pessoa diferente do transcritor; um modelo de IA nunca conta); nenhuma pendência com efeito acima de 1 % na conta de 10 m³ |
| amarelo, a validar | há documento arquivado ou transcrito, mas falta algum requisito do verde |
| cinza, sem dado | sem documento, entidade a identificar, ou dado ruim (`dado_ruim` em `entidades.json`) |

O concelho é verde se os três serviços forem verdes, cinza se forem todos cinza, amarelo nos restantes casos. A regra está num só sítio, `triton/core/tarifarios_portugal.py::avaliar_servico`, usada pelo programa (concelhos transcritos) e por `procedencia_pt.py` (os 280). Particularidades portuguesas que o esquema respeita: serviços de entidades diferentes (cada um com a sua entidade e documento), saneamento por escalões, IVA sempre do documento, TRH como parcela, tarifa fixa por calibre.

Nota sobre o pedido inicial (várias classes e pontuação 0 a 100): foi substituído pelo consenso que o coordenador enviou a meio do trabalho. Não há pontuação nem «classes».

## Ficheiros

| Ficheiro | O que é | No Git? |
| :--- | :--- | :--- |
| `entidades.json` | entidade gestora → serviço → concelhos → documentos; os 280 concelhos com distrito e a ficha tarifária ERSAR mais recente de cada serviço; `documentos` (curados à mão) | sim |
| `fontes/FONTES.tsv` | registo mínimo de cada ficheiro, **11 colunas, sem cabeçalho**: caminho, url, sha256, data_coleta, entidade, concelhos, tipo, vigencia, confirmado_em, verificado_por, redistribuivel. As 4 primeiras são as de sempre (`gerar_apendices.py` lê só essas). `redistribuivel` = 0 em todos (documentos de terceiros não vão no instalador) | sim |
| `CONFIANCA_POR_CONCELHO.csv` / `.md` | resultado: concelho, distrito, entidade, estado e estado de cada serviço, vigência, o que falta, URL do documento, URL da ficha ERSAR, `gerado_em` | sim |
| `FILA.md` | resultado do monitor (mudou / não respondeu / sem alteração / sem URL) | sim |
| `procedencia_pt.py` | calcula o CSV e o MD; `texto_manual()` devolve a secção do apêndice D | não (`tarifas_portugal/*.py` está no .gitignore) |
| `importar_ersar.py` | monta `entidades.json` do índice da ERSAR e completa `FONTES.tsv`; os `documentos` vêm do dicionário `DOCUMENTOS` no ficheiro, preservados se `entidades.json` já existir | não |
| `monitorar_tarifas.py` | vigia os URLs de `FONTES.tsv` (ferramenta **manual** do mantenedor; nada agendado) | não |
| `fontes/_indice_ersar/tarifa-concelho.json` | cópia local do índice da ERSAR (713 608 bytes) | não (`fontes/*` está ignorada) |

No programa: `portugal_tarifarios.json` ganhou, para Lisboa, Porto e Funchal, o campo `procedencia` (serviços transcritos, documentos com url/sha256/confirmado_em/verificado_por, conferência, vigência e `pendencias` com `servicos` e `efeito_pct`; `null` = não quantificável). `tarifarios_portugal.procedencia(concelho)` e `.estados(concelho)` leem-no, e o cartão do tarifário (`tab_project._preview_portugal`) mostra a linha «Procedência» onde o Brasil mostra a auditoria. Código editado em `triton_int` e copiado para BRL e IBE (só `tarifarios_portugal.py` e `ui/tab_project.py`; sem mudança de comportamento fora da IBE).

## Fonte do concelho → entidade (aberta e verificada)

A página «Pesquisa por concelho» da ERSAR (https://www.ersar.pt/pt_consumidor_tarifas-dos-servicos_encargos-tarifarios_pesquisa-por-concelho_ano.html) carrega `https://www.ersar.pt/docs/pesquisa-tarifa-concelho/tarifa-concelho.json`: 2 331 registos (2024 a 2026), 278 concelhos continentais, 314 entidades, por serviço (AA, AR, RU) e com o PDF da ficha tarifária. Acedido em 23/10/2026, SHA-256 `20057b868191dda9f465d7652d3f80eb05cd490a8430d532a232c1f98a701fad`. Vale a entidade do ano mais recente de cada concelho e serviço. Nada foi inferido pelo nome. Fora do índice: Funchal e Ponta Delgada (a entidade vem do documento arquivado), Leiria na água e saneamento (do documento SMAS), Ponte de Lima nos resíduos e Ponta Delgada nos resíduos (**«a identificar»**).

As fichas ERSAR (PDF) não foram descarregadas; só se verificou, com pedidos HEAD, que existem (`http` em `fichas_ersar` de `entidades.json`, quando verificado). Entidades com mais de uma por serviço (Loulé, Grândola, Penacova, Santo Tirso, Vila Nova de Cerveira) aparecem todas.

## Retomar

1. Documento novo: pôr em `fontes/<entidade>/`, acrescentar a linha em `FONTES.tsv` (4 colunas) e o documento em `DOCUMENTOS` de `importar_ersar.py` (ou em `entidades.json`), correr `python tarifas_portugal/importar_ersar.py` (completa as 11 colunas) e depois `python tarifas_portugal/procedencia_pt.py`.
2. Índice ERSAR novo: guardar em `fontes/_indice_ersar/`, actualizar a linha de FONTES.tsv (SHA-256) e correr `importar_ersar.py`.
3. Transcrever um concelho: acrescentar a entrada a `portugal_tarifarios.json` **com** `procedencia` (copiar o bloco de Lisboa; url/sha256/confirmado_em/verificado_por têm de ser iguais aos de FONTES.tsv, o teste confere).
4. Verificação independente: em `FONTES.tsv` (coluna 10, `verificado_por`) e no `procedencia.documentos` do JSON, escrever `fatura` ou `humano`. Só então um serviço pode ficar verde (e só se também não houver pendência acima de 1 %). Nada foi marcado: **não existe nenhuma verificação independente registada, por isso não há verde**.
5. Anualmente: `python tarifas_portugal/monitorar_tarifas.py` (um GET por URL, 3 s de pausa, 403/429 não repetidos); ver `FILA.md`; para o que não mudou e continua em vigor, `--atualizar-confirmacao` grava `confirmado_em` = hoje.
6. Manual: `manual/gerar_apendices.py` (gera A, B e D; a secção da confiança vem de `procedencia_pt.texto_manual()`; sem a ferramenta, omite-a). O apêndice D `.md` foi editado à mão com o mesmo texto, **sem correr nenhum gerador**.
7. Testes: `cd triton_ibe; TRITON_EDITION=IBE QT_QPA_PLATFORM=offscreen python -m pytest tests/unit/test_procedencia_tarifaria_pt.py tests/unit/test_tarifarios_porto_funchal.py -q -p no:cacheprovider`. O teste só vale na IBE (`tests/so_da_ibe.txt`) e falha se existir verde sem `verificado_por`.

## Estado em 23/10/2026 e pendências

- Contagens: ver `CONFIANCA_POR_CONCELHO.md` (verde 0; amarelo e cinza no resto).
- `confirmado_em` começou igual a `data_coleta` (07/10/2026); `verificado_por` vazio em todos. Três documentos oficiais (Alto Minho, Portalegre p. 4, Bragança) e os secundários foram «entregues pelo autor» sem URL: não são vigiáveis e o serviço fica amarelo por «sem URL de origem».
- Documentos de entidade inteira (Alto Minho, AdRA, ADIN) não nomeiam concelhos: a aplicação aos outros concelhos da entidade fica «a confirmar» no «o que falta».
- Divergências a resolver: Guarda (o edital 16/2026 é da Câmara, a ERSAR indica Águas Públicas em Altitude em 2025) e Bragança (resíduos hoje de «Resíduos do Nordeste»).
- Vigência com mais de 12 meses: Beja (01/01/2025), Évora (01/02/2025), Ponta Delgada (2025), Bragança (01/2021); a ERSAR já tem ficha 2026 para alguns.
- Lisboa: o monitor teve resposta 403 do anfitrião `lisboa.pt` e não insistiu; os dois PDFs da Câmara ficam «não respondeu» em `FILA.md`. As páginas HTML de Santarém mudaram de hash (conteúdo dinâmico; conferir à vista).
- Pendências de Funchal (escalão 1, regra dos escalões, IVA 4 %, TRH), Lisboa (IVA do saneamento e resíduos, adicional, 30 dias) e Porto (disponibilidade por inferência do layout, IVA da TRH) estão em `portugal_tarifarios.json`, com efeito estimado; as estimativas da TRH do Funchal e dos 30 dias de Lisboa são ordens de grandeza, rotuladas.
- Não se tocou nos capítulos 10 e 29 nem em `triton_brl/manual`. Não se correu `gerar.py`, `gerar_pdf.py`, `gerar_site.py`.
- Deriva pré-existente entre as edições (não corrigida, fora do âmbito): `triton_int` difere de BRL e IBE em `ui/tab_documentation.py`, `tests/test_essencial.py`, `tests/unit/test_mini_manuais.py` e `tests/unit/test_modulacao_estocastica.py`; `sync_nucleo.py --aplicar` copiaria esses ficheiros por cima. Aplicou-se a sincronização à mão, só nos ficheiros desta tarefa.
- Dois testes de `tests/test_essencial_interface.py` (`TestTariffsMultiCategoryAndTab`, categorias do catálogo brasileiro) falham na IBE por `get_city_data` devolver `None`; não têm relação com este trabalho (não verificado contra o HEAD).
