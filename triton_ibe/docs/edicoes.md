# A Edição Ibérica (IBE)

O Triton sai em edições a partir do **mesmo código**: Brasil (BRL), International (INT) e
Ibérica (IBE). O motor de cálculo — balanço diário, descarte inicial, coeficientes de
escoamento, análise económica, ACV, TOPSIS — é um só. O que separa as edições são os
**dados nacionais**. A Edição Ibérica parte do núcleo neutro, está em português de Portugal,
trabalha em euros e traz dados de Portugal: precipitação diária por concelho (E-OBS) e os
tarifários de Lisboa, do Porto e do Funchal.

**Nome e códigos.** A edição chamava-se «Portugal» (código `PRT`, antes `POR`) e passou a chamar-se **Triton IBE**, de Península Ibérica. O valor interno é `IBE`; `PRT` e `POR` continuam aceites como sinónimos (variável `TRITON_EDITION`, `--edition`, `set_current_edition`) e normalizam para `IBE`, e `is_prt_edition` é alias de `is_ibe_edition`. Hoje só os concelhos de Portugal têm dados (a linha de cobertura mostra «Espanha: 0 locais»); não há dados espanhóis inventados.

Este documento é o mapa para quem mantém o programa. English version:
[`en/editions.md`](en/editions.md).

---

## 1. O que o utilizador vê

| | Edição Ibérica (IBE) |
| :--- | :--- |
| idioma ao abrir | português de Portugal (VAL, entidade gestora, ficheiro, escalões) |
| selo na barra lateral, título da janela, rodapé dos relatórios e exportações | «Edição Ibérica (IBE)», vermelho |
| chuva | base E-OBS por concelho (278 do Continente, observada, 1950–2025) ou série própria; Açores e Madeira só com série própria; série de exemplo do Funchal (reanálise ERA5) |
| tarifas de água, saneamento e resíduos | tarifários transcritos dos documentos oficiais de Lisboa (EPAL e Câmara Municipal), do Porto e do Funchal; nos outros concelhos, digitadas |
| energia | digitada |
| moeda | euro, a única oferecida |
| custos de referência (motobomba, cloro, manutenções, arranjo, mão de obra) | zerados; digitados |
| catálogo de bombas do assistente | «modelos de referência» A a E (curvas, bocais, potências), sem marca nem preço |
| perfis de inflação, atualização e reajuste | genéricos, definidos pelo utilizador |
| fator de emissão da rede e da água potável | digitado, para o local do projeto |
| certificações | LEED, EDGE, GRI |
| normas citadas | nenhuma por número; os textos dizem «norma de referência» |
| manual que o programa abre | o manual desta edição, quando está instalado |
| preferências (QSettings) | `UFSC/Triton-IBE` |

---

## 2. Onde está no código

A pergunta que cada ecrã faz antes de oferecer um dado nacional é `usa_dados_do_brasil()`
(só Brasil) ou `usa_dados_de_portugal()` (só Portugal), em `triton/core/edition.py`. A edição
vem da variável de ambiente `TRITON_EDITION`, que o `main.py` de cada pasta fixa (ou a opção
`main.py --edition brl|int|por`). Fora de Portugal, a resposta a `usa_dados_de_portugal()` é
negativa; a Edição Ibérica recebe a resposta neutra a `usa_dados_do_brasil()`.

| Arquivo | O que faz |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` e o modelo de planilha partem da fábrica da edição (`configuracao_da_edicao`) e da série de exemplo dela; fora da Brasil, sem tarifa, preço, IPTU Verde nem fator de rede de partida; `compare-mass` e `run-vaz-study` (replicação do Brasil) só na Brasil; a ajuda sai em inglês (INT) ou português de Ibérica (IBE) |
| `triton/cli_textos.py` | textos da ajuda e das mensagens da linha de comando por edição (inglês na International, glossário de Portugal na Portugal) |
| `triton/core/bibliography.py` | a lista de referências deixa de fora, fora da Brasil, os registros que citam normas, bases e fabricantes brasileiros |
| `triton/core/cad_exporter.py` | selo e camadas do desenho técnico (DXF e SVG) sem norma nacional fora da Brasil |
| `triton/core/dados_do_relatorio.py` | dados dos laudos que dependem da edição: normas, registro profissional e entidade que abastece o local |
| `triton/core/diagnostico.py` | a base CLIMBra «não se aplica» fora da Brasil; o diagnóstico diz a edição |
| `triton/core/edition.py` | a edição ativa, o rótulo, o idioma, a moeda e o manual; as fábricas `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` e `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` zera tarifas, energia, motobomba, cloro, manutenções, IPTU Verde e a localidade do projeto novo |
| `triton/core/licenca_eobs.py` | só na Portugal (IBE): aviso de licença da E-OBS, escolha de uso lembrada, bloqueio atrás de constante desligada e rodapé de licença e citação dos laudos |
| `triton/core/environmental_justifications.py` | justificativas da ACV sem fabricantes, normas e inventários nacionais fora da Brasil |
| `triton/core/esg_certifications.py` | síntese ESG e matriz de créditos só com as certificações internacionais fora da Brasil |
| `triton/core/parser.py` | o leitor de `.triton` e de CSV parte de `configuracao_da_edicao()`: o que o arquivo não traz cai no padrão histórico (BRL) ou no neutro (INT e IBE) |
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

`tests/unit/test_edicoes_documentadas.py` falha se um ficheiro passar a perguntar pela
edição sem constar desta tabela. `tests/unit/test_neutralidade_interface.py` abre a janela,
percorre as etapas, os diálogos e o separador Documentação, e falha se algum texto citar um
dado do Brasil ou usar o vocabulário do Brasil.

**A linha de comandos segue a edição.** `triton init` escreve um modelo sem tarifa, preço,
localidade nem fator de rede do Brasil; `triton init-catalog` escreve o catálogo climático da
série de exemplo desta edição. Um projeto guardado numa edição dá o mesmo resultado nas
outras e na CLI.

---

## 3. Empacotamento

| | Portugal |
| :--- | :--- |
| ponto de entrada | `main.py` em `triton_ibe` |
| compilação | `python build_exe.py`, dentro da pasta |
| pasta | `dist/Triton_IBE/`, `Triton_IBE.exe` |
| instalador | `Triton_IBE_Setup_0_1_0.exe` (`/DEdition=IBE`) |
| pasta de instalação | `Triton Portugal` |
| associação dos `.triton` | desmarcada |
| base E-OBS de Portugal (`data/portugal_eobs.db`, ~6 MB, no git) | embutida; a compilação para se faltar |
| fontes brutas de Portugal (`data/portugal/fontes`, ~3 GB, fora do git) | retiradas |

Detalhes do instalador em [`instalador.md`](instalador.md).

---

## 4. Dados e documentos desta edição

**Precipitação.** Precipitação diária por concelho extraída da E-OBS v33.0e
(Copernicus/KNMI, grelha de 0,1°, 1950–2025; citar Cornes et al., 2018,
doi:10.1029/2017JD028200, e reconhecer UERRA, C3S e ECA&D), com os limites da CAOP2025 (DGT):
a série é a média das células com centro dentro do concelho. O script
`compilar_base_eobs_portugal.py` (pasta `scripts/`) gera `data/portugal_eobs.db` a partir das
fontes em `data/portugal/fontes` (endereços e SHA-256 em `LEIA.txt`). Ficam sem série, com o
motivo gravado na base, os 19 concelhos dos Açores (fora do domínio da E-OBS, a oeste de
25° W) e os 11 da Madeira (a E-OBS só tem ali as células das estações em funcionamento; o
Funchal fica sem dado em 22% dos dias de 1991–2020, e o critério admite no máximo 1%).

**Tarifários.** `triton/data/portugal_tarifarios.json` traz os de Lisboa (EPAL e Câmara
Municipal), do Porto (Tarifário Geral 2026) e do Funchal (Tabela de Taxas Municipais 2026),
transcritos dos documentos oficiais; cada um leva as notas do que ficou por confirmar. A
fatura portuguesa soma água, saneamento, resíduos (muitas vezes indexados ao m³ de água), a
taxa de recursos hídricos e o IVA.

**Método e verificação.** [`metodologia.md`](metodologia.md),
[`verificacao_e_validacao.md`](verificacao_e_validacao.md),
[`conferencia_dos_casos_analiticos.md`](conferencia_dos_casos_analiticos.md) e
[`certificacao_edge.md`](certificacao_edge.md); a guia de linha de comandos está em
[`../infos_licenses/CLI_USAGE.md`](../infos_licenses/CLI_USAGE.md).

## 5. Ao acrescentar um dado nacional

1. Pergunte `usa_dados_do_brasil()` ou `usa_dados_de_portugal()` antes de o oferecer; fora da
   edição do país, o campo começa vazio ou a zero, e o utilizador informa-o.
2. Acrescente o ficheiro à tabela da secção 2.
3. Corra `tests/unit/test_neutralidade_interface.py` nas três edições.
