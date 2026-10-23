# Fila dos tarifários de Portugal

Gerado em 2026-10-23 01:34 por `tarifas_portugal/monitorar_tarifas.py`. Não edite à mão.

Um pedido GET por URL de `fontes/FONTES.tsv`, com User-Agent identificado e pausa entre pedidos; 403 e 429 não são repetidos. Compara o SHA-256 (e o tamanho do ficheiro arquivado, quando existe) com o registado. Nada é descarregado para o disco.

Resumo: **2 mudou**, **2 não respondeu**, **27 sem alteração**, 6 sem URL (não vigiáveis).

## Mudou

Candidatos a nova recolha (as páginas HTML podem mudar por razões triviais: conferir à vista).

| Ficheiro | URL | SHA-256 registado | SHA-256 agora | Tamanho registado | Tamanho agora |
| :--- | :--- | :--- | :--- | ---: | ---: |
| Aguas_de_Santarem/tarifario-geral-2026.html | https://aguasdesantarem.pt/clientes/tarifario-2026/tarifario-geral/ | `c38c65c2034d…` | `e625b03a5591…` | 435717 | 439689 |
| Aguas_de_Santarem/tarifario-servicos-de-saneamento-2026.html | https://aguasdesantarem.pt/clientes/tarifario-2026/tarifario-servicos-de-saneamento/ | `ece853565ab8…` | `236b5dab308a…` | 438943 | 442915 |

## Não respondeu

| Ficheiro | URL | Resposta | Nota |
| :--- | :--- | :--- | :--- |
| CM_Lisboa/tarifario_saneamento_2026.pdf | https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_saneamento_2026.pdf | 403 |  |
| CM_Lisboa/tarifario_residuos_urbanos_2026.pdf | https://www.lisboa.pt/fileadmin/portal/municipio/organizacao/financas/taxas/tarifario_residuos_urbanos_2026.pdf | sem resposta | anfitrião recusou antes (403/429): não insistido |

## Sem alteração

| Ficheiro | URL | SHA-256 |
| :--- | :--- | :--- |
| Aguas_do_Porto/Tarifario_Geral_2026.pdf | https://www.aguasdoporto.pt/files/uploads/cms/Tarif%C3%A1rio%20Geral%202026.pdf | `7d6b5d0ceeef…` |
| Aguas_de_Coimbra/Tarifario-Abastecimento-de-Agua.pdf | https://www.aguasdecoimbra.pt/wp-content/uploads/Tarifario-Abastecimento-de-Agua.pdf | `b877ad1c36d0…` |
| Aguas_de_Coimbra/Tarifario-Aguas-Residuais.pdf | https://www.aguasdecoimbra.pt/wp-content/uploads/Tarifario-Aguas-Residuais.pdf | `fc75a40bca31…` |
| Aguas_de_Coimbra/Edital-n.o-433_2025.pdf | https://www.aguasdecoimbra.pt/wp-content/uploads/Edital-n.o-433_2025.pdf | `24e06729bae1…` |
| Aguas_de_Coimbra/Edital-n.o-438_2025.pdf | https://www.aguasdecoimbra.pt/wp-content/uploads/Edital-n.o-438_2025.pdf | `5ea9577ce06b…` |
| AGERE_Braga/AGERE_Tarifario-Fev2026.pdf | https://agere.pt/wp-content/uploads/2026/02/AGERE_Tarifario-Fev2026-.pdf | `dbb02a6e17a9…` |
| SMS_Setubal/01-Tarifario-2026_Agua.pdf | https://sms-setubal.pt/wp-content/uploads/2026/03/01-Tarifario-2026_Agua.pdf | `e4b870a34630…` |
| SMS_Setubal/02-Tarifario-2026_Saneamento.pdf | https://sms-setubal.pt/wp-content/uploads/2026/03/02-Tarifario-2026_Saneamento.pdf | `70b695682016…` |
| SMS_Setubal/Tarifario-2026_Residuos-VC.pdf | https://sms-setubal.pt/wp-content/uploads/2026/03/Tarifario-2026_Residuos-VC.pdf | `2f222afe6319…` |
| SMAS_Leiria/tarifario_2026_F.pdf | https://smas-leiria.pt/wp-content/uploads/2025/12/tarifario_2026_F.pdf | `3aac89840876…` |
| FAGAR_Faro/tarifario_2026.pdf | https://fagar.pt/sites/default/files/documentos/tarifario_2026.pdf | `a86a07e44689…` |
| AdRA_Aveiro/ADRA_TARIFARIO2026_H_ONLINE_0.pdf | https://adra.pt/adra/sites/default/files/ADRA_TARIFARIO2026_H_ONLINE_0.pdf | `9edda7d24234…` |
| Aguas_de_Viseu/Tarifarios_Aguas_Viseu-ABR2026.pdf | https://www.aguasdeviseu.pt/source/tarif%C3%A1rios/Tarif%C3%A1rio%202026/WEB-Tarifarios_Aguas%20Viseu-ABR2026-H.pdf | `9cb5c12df7fc…` |
| EMAS_Beja/Tarifario_2025.pdf | https://emas-beja.pt/files/pdf/anos_anteriores/2025.pdf | `e22a3fae8b82…` |
| CM_Evora/Tarifario-2025.pdf | https://www.cm-evora.pt/wp-content/uploads/2025/01/Tarifario-2025.pdf | `9843ecbc06bd…` |
| EPAL_Lisboa/precos-2026.pdf | https://www.epal.pt/EPAL/docs/default-source/clientes/pre%c3%a7os-2026.pdf?sfvrsn=0 | `d0ebc13e3069…` |
| SM_Castelo_Branco/Tarifario_em_vigor_2026-02-24.pdf | https://www.sm-castelobranco.pt/uploads/conteudos/anexo_699dc879a344d_1771948153.pdf | `a05566989578…` |
| SMAS_Ponta_Delgada/tarifario-2026.pdf | https://smaspdl.pt/wp-content/uploads/2026/01/tarifario-2026.pdf | `132e6ec90744…` |
| SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0001.jpg | https://www.cm-portalegre.pt/wp-content/uploads/2025/12/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0001.jpg | `c12341c4f2c2…` |
| SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0002.jpg | https://www.cm-portalegre.pt/wp-content/uploads/2025/12/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0002.jpg | `00178165f8e4…` |
| SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0003.jpg | https://www.cm-portalegre.pt/wp-content/uploads/2025/12/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0003.jpg | `35894f7076bd…` |
| SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0005.jpg | https://www.cm-portalegre.pt/wp-content/uploads/2025/12/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0005.jpg | `3e9414fc89e2…` |
| ADIN_Vila_Real/Tarifas_2026.pdf | https://adin.pt/wp-content/plugins/download-attachments/includes/download.php?id=3659 | `2d6762a5b109…` |
| CM_Vila_Real/tarifario_residuos_2026.pdf | https://www.cm-vilareal.pt/images/areas_servicos/ambiente/tarifario2026.pdf | `59243414477f…` |
| CM_Guarda/Edital_16-2026_tarifario.pdf | https://od.mun-guarda.pt/Docs/Editais/af67909c-ee25-426f-a115-5e93296f8a01 | `d08cf693e09b…` |
| CM_Funchal/Tabela_de_Taxas_Municipais_2026_.pdf | https://cmfdoc.funchal.pt/media/k2/attachments/Tabela_de_Taxas_Municipais_2026_.pdf | `97084c0265bf…` |
| _indice_ersar/tarifa-concelho.json | https://www.ersar.pt/docs/pesquisa-tarifa-concelho/tarifa-concelho.json | `20057b868191…` |

## Sem URL

Documentos entregues pelo autor, sem endereço de origem em FONTES.tsv: não há o que vigiar. Quando possível, procurar o endereço no sítio da entidade e registá-lo.

| Ficheiro | Origem registada |
| :--- | :--- |
| Aguas_do_Alto_Minho/tarifario_AdM2026_Cartaz.pdf | entregue pelo autor |
| SMAT_Portalegre/EDITAL-Tarifarios-dos-Servicos-de-Aguas-Saneamento-Ramais-Roturas-e-Outros-2026_page-0004.jpg | entregue pelo autor |
| CM_Braganca/APFN_ficha_Braganca_Edital_68-2020.pdf | entregue pelo autor |
| _secundarios/APFN_Estudo_Agua_Ficha_2024_290.pdf | entregue pelo autor |
| _secundarios/APFN_ficha_Braganca_2018.pdf | entregue pelo autor |
| _fora_do_tema/2316,+A+EXTRAFISCALIDADE+TRIBUTÁRIA+DO+IPI.pdf | entregue pelo autor (fora do tema) |
