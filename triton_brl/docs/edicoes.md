# As três edições: Brasil (BRL), International (INT) e Ibérica (IBE)

O Triton sai em três edições a partir do **mesmo código**. O motor de cálculo — balanço
diário, descarte inicial, coeficientes de escoamento, análise econômica, ACV, TOPSIS — é
um só. O que separa as edições são **dados nacionais**: a Brasil traz os brasileiros
auditados; a International é o núcleo neutro, em que o usuário informa os dados do país do
projeto; a Portugal parte do núcleo neutro, fala português de Portugal, trabalha em euros e
recebe os dados portugueses — precipitação por concelho e tarifários das entidades gestoras —
à medida que são coletados e conferidos (decisões de 07/10/2026).


**Nome e códigos.** A edição chamava-se «Portugal» (código `PRT`, antes `POR`) e passou a chamar-se **Triton IBE**, de Península Ibérica. O valor interno é `IBE`; `PRT` e `POR` continuam aceites como sinónimos (variável `TRITON_EDITION`, `--edition`, `set_current_edition`) e normalizam para `IBE`, e `is_prt_edition` é alias de `is_ibe_edition`. Hoje só os concelhos de Portugal têm dados (a linha de cobertura mostra «Espanha: 0 locais»); não há dados espanhóis inventados.

Este documento é o mapa para quem mantém o programa. O usuário encontra o resumo na
seção 2 do manual («As duas edições»), em português e em inglês. English version:
[`en/editions.md`](en/editions.md).

---

## 1. O que o usuário vê

| | Edição Brasil (BRL) | International Edition (INT) | Edição Ibérica (IBE) |
| :--- | :--- | :--- | :--- |
| idioma ao abrir | português do Brasil | inglês | português de Portugal (VAL, entidade gestora, ficheiro, escalões) |
| selo na barra lateral, título da janela, rodapé de relatórios e exportações | «Edição Brasil (BRL)», verde | «International Edition (INT)», azul | «Edição Ibérica (IBE)», vermelho |
| chuva | base CLIMBra (652 cidades, CMIP6) ou série própria | série própria | base E-OBS por concelho (278 do Continente, observada, 1950–2025) ou série própria; Açores e Madeira só com série própria |
| tarifas de água e esgoto | catálogo de 652 municípios, com procedência por documento, ou digitadas | digitadas | digitadas; tarifários das capitais de distrito em construção |
| etapa 12, Gestor de Tarifas | presente | ausente | ausente até haver tarifários |
| aviso de categoria tarifária não residencial | presente | ausente | ausente |
| energia | tarifa ANEEL B1 da distribuidora ou digitada; bandeiras tarifárias | digitada | digitada |
| moeda | real, a única oferecida | nenhuma ao abrir («Moeda não definida (¤)»); o usuário escolhe dólar, euro, libra, yuan, rand, rupia e outras | euro, o único oferecido |
| custos de referência (motobomba, cloro, manutenções, arranjo, mão de obra) | preços brasileiros | zerados; digitados | zerados; digitados |
| IPTU Verde | presente | ausente | ausente |
| fator de emissão da rede e da água potável | MCTI e rotas por região | do país do projeto; sem ele, a ACV não é calculada | digitado, como na International |
| certificações | LEED, EDGE, GRI, AQUA-HQE, Selo Casa Azul | LEED, EDGE, GRI | LEED, EDGE, GRI |
| manual que o programa abre | português; inglês nas demais línguas da interface | inglês | português |
| preferências (QSettings) | `UFSC/Triton` | `UFSC/Triton-INT` | `UFSC/Triton-IBE` |

---

## 2. Onde está no código

A pergunta que cada tela faz antes de oferecer um dado brasileiro é
`usa_dados_do_brasil()`, em `triton/core/edition.py`; a de um dado português,
`usa_dados_de_portugal()`. A edição vem da variável de ambiente `TRITON_EDITION` (`BRL` por
padrão), que o `main.py` de cada pasta fixa (ou a opção
`main.py --edition brl|int|por`). Fora da Brasil, a Portugal se comporta como a
International (núcleo neutro), salvo onde a tabela diz outra coisa.

| Arquivo | O que muda fora da Brasil |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` e o modelo de planilha partem da fábrica da edição (`configuracao_da_edicao`) e da série de exemplo dela; fora da Brasil, sem tarifa, preço, IPTU Verde nem fator de rede de partida; `compare-mass` e `run-vaz-study` (replicação do Brasil) só na Brasil; a ajuda sai em inglês (INT) ou português de Ibérica (IBE) |
| `triton/cli_estudo.py` | `triton estudo` (`init`, `validate`, `run`, `resumo`, `lote`, `texto`, `esquema`, `apelidos`): argumentos, mensagens e códigos de saída (0 certo, 1 caso com erro, 2 uso inválido); o texto da ajuda sai por `cli_textos` e o catálogo de apelidos e métricas, na língua da edição |
| `triton/cli_textos.py` | textos da ajuda e das mensagens da linha de comando por edição (inglês na International, glossário de Portugal na Portugal) |
| `triton/core/cost_estimates.py` | banco de custos: fora da Brasil o arquivo `costs_database.json` não traz preços e o estimador devolve zero (o usuário informa os custos) |
| `triton/core/bibliography.py` | a lista de referências deixa de fora, fora da Brasil, os registros que citam normas, bases e fabricantes brasileiros |
| `triton/core/cad_exporter.py` | selo e camadas do desenho técnico (DXF e SVG) sem norma nacional fora da Brasil |
| `triton/core/dados_do_relatorio.py` | dados dos laudos que dependem da edição: normas, registro profissional e entidade que abastece o local |
| `triton/core/diagnostico.py` | a base CLIMBra «não se aplica» fora da Brasil; o diagnóstico diz a edição |
| `triton/core/edition.py` | a edição ativa, o rótulo, o idioma, a moeda e o manual; as fábricas `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` e `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` zera tarifas, energia, motobomba, cloro, manutenções, IPTU Verde e a localidade do projeto novo |
| `triton/core/licenca_eobs.py` | só na Portugal (IBE): aviso de licença da E-OBS, escolha de uso lembrada, bloqueio atrás de constante desligada e rodapé de licença e citação dos laudos |
| `triton/core/environmental_justifications.py` | justificativas da ACV sem fabricantes, normas e inventários nacionais fora da Brasil |
| `triton/core/esg_certifications.py` | síntese ESG e matriz de créditos só com as certificações internacionais fora da Brasil |
| `triton/core/estudo.py` | estudos em lote por JSON: esquema do `estudo.json`, apelidos de parâmetros, métricas e tabelas para artigos; o idioma das saídas (`auto`) é pt-BR na Brasil, pt-PT na Portugal e inglês na International; o modelo de projeto «edicao» parte da fábrica da edição; sem moeda declarada no projeto vale o real (BRL), o euro (IBE) ou nenhuma (INT) |
| `triton/core/parser.py` | o leitor de `.triton` e de CSV parte de `configuracao_da_edicao()`: o que o arquivo não traz cai no padrão histórico (BRL) ou no neutro (INT e IBE) |
| `triton/core/numero.py` | convenção numérica da interface: vírgula decimal e ponto de milhar em português e espanhol e na BRL; ponto decimal e vírgula de milhar em inglês e chinês fora da BRL (ler e mostrar passam por aqui) |
| `triton/core/report_generator.py` | laudos sem certificações, normas e referências nacionais fora da Brasil |
| `triton/core/tariff_category.py` | sem aviso de categoria tarifária (não há catálogo) |
| `triton/ui/dialogs/dialog_economic.py` | sem o seletor de município da tarifa e da energia; guia de custos de tubulação e regime de cobrança sem referência nacional |
| `triton/ui/dialogs/pump_wizard_dialog.py` | catálogo de «modelos de referência» (curvas, bocais e potências), sem marca nem preço fora da Brasil |
| `triton/ui/laudo_em_ingles.py` | textos do laudo em inglês, para a International |
| `triton/ui/main_window.py` | projeto novo pela fábrica da edição (`projeto_novo_da_edicao`), também em Arquivo > Novo Projeto; sem a página do Gestor de Tarifas; «Como citar» e «Sobre» sem norma nem local nacional; os textos fixos em reais passam à moeda do projeto (`triton/ui/moeda_na_interface.py`) |
| `triton/ui/sidebar.py` | selo azul (INT) ou vermelho (IBE); sem a etapa Gestor de Tarifas, e a numeração segue sem salto |
| `triton/ui/tab_documentation.py` | as páginas saem sem seção, item, linha ou frase que cite o Brasil (`textos_da_edicao.html_da_edicao`); a página que fica sem texto não é oferecida; na Portugal em português passa pelo glossário; sem manual de reserva de outro país |
| `triton/ui/tab_economic_integrated.py` | sem IPTU Verde e bandeiras tarifárias |
| `triton/ui/tab_environmental.py` | fatores de emissão vazios e obrigatórios; água substituída: «rede com fator informado» ou «personalizado»; sem rotas nem certificações nacionais |
| `triton/ui/tab_export.py` | nomes sugeridos nos seletores de arquivo e prancha técnica sem norma nacional |
| `triton/ui/tab_modulacao_estocastica.py` | sem o sorteio entre modelos climáticos da base CLIMBra; valores na moeda do projeto |
| `triton/ui/tab_project.py` | sem o quadro de tarifas da cidade; a base nacional de chuva é a CLIMBra (BRL), a E-OBS por distrito e concelho (IBE) ou nenhuma (INT: abre a série de exemplo da edição, em arquivo) |
| `triton/ui/tab_reports_pdf.py` | idiomas do laudo e normas citadas da edição |
| `triton/ui/tab_tanks_simulation.py` | perfis de inflação, desconto e reajuste: os do Brasil só na Brasil, genéricos nas outras; moedas: International sem moeda predefinida (¤) e com dólar, euro, libra, yuan, rand, rupia e outras à escolha; Portugal só o euro; Brasil só o real; o projeto grava o código da moeda |
| `triton/ui/tab_water_quality.py` | ETAP e descarte sem preços de catálogo em reais nem norma nacional (só o cloro, pelo preço informado); a energia do reator UV emite pelo fator da rede informado na ACV |
| `triton/ui/textos_da_edicao.py` | as variantes por edição de normas, registro profissional, títulos, nomes de arquivo e descritivos do núcleo; o filtro que tira o Brasil do HTML da documentação |
| `triton/ui/translation.py` | inglês ao abrir (INT) ou português de Portugal (IBE, glossário em `triton/ui/portugues_de_portugal.py`); preferências separadas; os textos neutros de `translation_neutralidade.py` substituem os do catálogo |

`tests/unit/test_edicoes_documentadas.py` falha se um arquivo passar a perguntar pela
edição sem constar desta tabela.

**A linha de comando segue a edição.** `triton/cli.py` calcula com o que o arquivo de projeto declara — tarifa, custos, fatores —, sem consultar o catálogo nem a base CLIMBra por conta própria; o modelo que `init` cria, porém, parte da fábrica da edição (`configuracao_da_edicao`): na Brasil, os padrões históricos; na International e na Portugal, sem tarifa, preço nem localidade do Brasil. Um projeto salvo numa edição dá o mesmo resultado na outra e na CLI. A exceção é pedida: `probabilistic-study --climate-models` lê da base CLIMBra as séries dos modelos escolhidos. Um projeto que grava a chuva como referência à base (CLIMBra, ou E-OBS na Portugal) é relido da base em qualquer edição e na CLI.

---

## 3. Empacotamento

| | Brasil | International | Portugal |
| :--- | :--- | :--- | :--- |
| ponto de entrada | `main.py` em `triton_brl` | `main.py` em `triton_int` | `main.py` em `triton_ibe` |
| compilação | `python build_exe.py`, dentro de cada pasta | idem | idem |
| pasta | `dist/Triton/`, `Triton.exe` | `dist/Triton_INT/`, `Triton_INT.exe` | `dist/Triton_IBE/`, `Triton_IBE.exe` |
| instalador | `Triton_Setup_0_1_0.exe` (`/DEdition=BRL`) | `Triton_INT_Setup_0_1_0.exe` (`/DEdition=INT`) | `Triton_IBE_Setup_0_1_0.exe` (`/DEdition=IBE`) |
| pasta de instalação | `Triton` | `Triton International` | `Triton IBE` |
| associação dos `.triton` | marcada | desmarcada | desmarcada |
| base CLIMBra (`data/climbra.db`, ~784 MB) | embutida; o build para se faltar | retirada após o PyInstaller | retirada após o PyInstaller |
| base E-OBS de Portugal (`data/portugal_eobs.db`, ~6 MB, no git) | retirada após o PyInstaller | retirada após o PyInstaller | embutida; o build para se faltar |
| fontes brutas de Portugal (`data/portugal/fontes`, ~3 GB, fora do git) | retiradas | retiradas | retiradas |
| pasta `tarifas/` (documentos oficiais e transcrições, ~150 MB) | vai, sem a `entrada` | retirada após o PyInstaller | retirada após o PyInstaller |
| manuais no pacote | português e inglês | português e inglês | português e inglês |

`python build_exe.py --edition all` compila as três.

Detalhes do instalador em [`instalador.md`](instalador.md).

---

## 4. Dados e documentos de cada edição

**Só da Edição Brasil.** Tudo o que alimenta os dados brasileiros:

| Material | Conteúdo |
| :--- | :--- |
| [`../tarifas/`](../tarifas/README.md) | catálogo de 652 municípios, documentos oficiais, transcrições e procedência |
| `triton/data/brazil_cities_tariffs.json` | o banco tarifário que o programa lê |
| [`base_climatica_climbra.md`](base_climatica_climbra.md) | a base climática nacional |
| [`../tarifas/categorias/`](../tarifas/categorias/) | tabelas oficiais das categorias não residenciais |

**Das duas edições.** Método, verificação e uso:
[`metodologia.md`](metodologia.md), [`verificacao_e_validacao.md`](verificacao_e_validacao.md),
[`normas_nbr_x_en16941.md`](normas_nbr_x_en16941.md) (o que muda entre a NBR e a norma
europeia, útil sobretudo na International), [`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md),
[`certificacao_edge.md`](certificacao_edge.md), [`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md).
[`procedencia_fatores_co2.md`](procedencia_fatores_co2.md) vale para as duas, mas os
fatores da rede e da água potável que ele documenta são os que só a Brasil pré-preenche.

**O manual.** Um só, nas duas línguas, para as duas edições. O que só existe na Brasil leva
a nota «Só na Edição Brasil (BRL)» / «Brazil Edition (BRL) only»; o modo de seguir na
International, a nota «Na International Edition (INT)» / «In the International Edition
(INT)». `manual/en/conferir.py` exige as mesmas notas, na mesma ordem, nas duas línguas.

---

**Só da Edição Ibérica.** Precipitação diária por concelho extraída da E-OBS v33.0e
(Copernicus/KNMI, grade de 0,1°, 1950–2025; citar Cornes et al., 2018, doi:10.1029/2017JD028200,
e reconhecer UERRA, C3S e ECA&D), com os limites da CAOP2025 (DGT): a série é a média das
células com centro dentro do concelho. O script `compilar_base_eobs_portugal.py` da Edição Ibérica gera
`data/portugal_eobs.db` a partir das fontes em `data/portugal/fontes` (endereços e SHA-256 em
`LEIA.txt`). Ficam sem série, com o motivo gravado na base, os 19 concelhos dos Açores (fora do
domínio da E-OBS, a oeste de 25° W) e os 11 da Madeira (a E-OBS só tem ali as células das
estações em funcionamento; o Funchal fica sem dado em 22% dos dias de 1991–2020, e o critério
admite no máximo 1%). Em construção: tarifários das entidades gestoras, a começar pelas capitais de distrito, transcritos dos
documentos oficiais e conferidos como os brasileiros. A fatura portuguesa soma água,
saneamento, resíduos (muitas vezes indexados ao m³ de água), a taxa de recursos hídricos e
o IVA; o motor tarifário passará a representar essas parcelas.

## 5. Ao acrescentar um dado brasileiro

1. Pergunte `usa_dados_do_brasil()` antes de oferecê-lo; na International, o campo começa
   vazio ou zerado, e o usuário o informa.
2. Acrescente o arquivo à tabela da seção 2.
3. Teste as duas edições em `tests/test_essencial_interface.py`, seção «Interface» (e, se o
   dado entra no cálculo, a paridade com a CLI).
4. No manual, marque com as notas de edição nas duas línguas.
