# Edição International (INT)

O Triton sai em edições a partir do **mesmo código**: Brasil (BRL), International (INT) e
Ibérica (IBE). O motor de cálculo é um só. A International é o núcleo neutro: não traz
tarifa, preço, chuva, norma nem fator de emissão de país nenhum, e o usuário informa os do
seu projeto, na moeda que escolher.

Este arquivo existe como ponteiro em português; o mapa completo está em inglês em
[`en/editions.md`](en/editions.md). A tabela abaixo é a mesma.

---

## Onde está no código

A pergunta que cada tela faz antes de oferecer um dado nacional é `usa_dados_do_brasil()`
(só Brasil) ou `usa_dados_de_portugal()` (só Portugal), em `triton/core/edition.py`. A
International recebe a resposta neutra a todas.

| Arquivo | O que faz |
| :--- | :--- |
| `triton/cli.py` | `init`, `init-catalog` e o modelo de planilha partem da fábrica da edição (`configuracao_da_edicao`) e da série de exemplo dela; fora da Brasil, sem tarifa, preço, IPTU Verde nem fator de rede de partida; `compare-mass` e `run-vaz-study` (replicação do Brasil) só na Brasil; a ajuda sai em inglês (INT) ou português de Ibérica (IBE) |
| `triton/cli_estudo.py` | `triton estudo` (`init`, `validate`, `run`, `resumo`, `lote`, `texto`, `esquema`, `apelidos`): argumentos, mensagens e códigos de saída (0 certo, 1 caso com erro, 2 uso inválido); o texto da ajuda sai por `cli_textos` e o catálogo de apelidos e métricas, na língua da edição |
| `triton/cli_textos.py` | textos da ajuda e das mensagens da linha de comando por edição (inglês na International, glossário de Portugal na Portugal) |
| `triton/core/economics/cost_estimates.py` | banco de custos: fora da Brasil o arquivo `costs_database.json` não traz preços e o estimador devolve zero (o usuário informa os custos) |
| `triton/core/system/bibliography.py` | a lista de referências deixa de fora, fora da Brasil, os registros que citam normas, bases e fabricantes brasileiros |
| `triton/core/cad_bim/cad_exporter.py` | selo e camadas do desenho técnico (DXF e SVG) sem norma nacional fora da Brasil |
| `triton/core/reporting/dados_do_relatorio.py` | dados dos laudos que dependem da edição: normas, registro profissional e entidade que abastece o local |
| `triton/core/system/diagnostico.py` | a base CLIMBra «não se aplica» fora da Brasil; o diagnóstico diz a edição |
| `triton/core/system/edition.py` | a edição ativa, o rótulo, o idioma, a moeda e o manual; as fábricas `configuracao_da_edicao`, `projeto_novo_da_edicao`, `tarifa_de_agua_de_reserva` e `serie_de_exemplo_da_edicao`; `neutralizar_para_a_internacional` zera tarifas, energia, motobomba, cloro, manutenções, IPTU Verde e a localidade do projeto novo |
| `triton/core/climate/licenca_eobs.py` | só na Portugal (IBE): aviso de licença da E-OBS, escolha de uso lembrada, bloqueio atrás de constante desligada e rodapé de licença e citação dos laudos |
| `triton/core/lca/environmental_justifications.py` | justificativas da ACV sem fabricantes, normas e inventários nacionais fora da Brasil |
| `triton/core/lca/esg_certifications.py` | síntese ESG e matriz de créditos só com as certificações internacionais fora da Brasil |
| `triton/core/reporting/estudo.py` | estudos em lote por JSON: esquema do `estudo.json`, apelidos de parâmetros, métricas e tabelas para artigos; o idioma das saídas (`auto`) é pt-BR na Brasil, pt-PT na Portugal e inglês na International; o modelo de projeto «edicao» parte da fábrica da edição; sem moeda declarada no projeto vale o real (BRL), o euro (IBE) ou nenhuma (INT) |
| `triton/core/system/parser.py` | o leitor de `.triton` e de CSV parte de `configuracao_da_edicao()`: o que o arquivo não traz cai no padrão histórico (BRL) ou no neutro (INT e IBE) |
| `triton/core/system/numero.py` | convenção numérica da interface: vírgula decimal e ponto de milhar em português e espanhol e na BRL; ponto decimal e vírgula de milhar em inglês e chinês fora da BRL (ler e mostrar passam por aqui) |
| `triton/core/reporting/report_generator.py` | laudos sem certificações, normas e referências nacionais fora da Brasil |
| `triton/core/tariffs/tariff_category.py` | sem aviso de categoria tarifária (não há catálogo) |
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
