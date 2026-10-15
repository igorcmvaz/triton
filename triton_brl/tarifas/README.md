# 💧⚡ Banco de Tarifas e Motor de Atualização (Triton)

> **Só na Edição Brasil (BRL).** O catálogo tarifário é brasileiro: a International
> Edition não o usa nem o leva no pacote (veja [`../docs/edicoes.md`](../docs/edicoes.md)).
> O programa lê só `triton/data/brazil_cities_tariffs.json`; esta pasta, sem a `entrada`,
> acompanha a Edição Brasil como procedência consultável dos documentos oficiais.

Esta pasta centraliza **todos os scripts de atualização, webscrapers, motores de auditoria, bases de dados homologadas e relatórios de governança tarifária** para os 652 municípios brasileiros analisados pelo Triton.

---

## 📄 Documentos oficiais → transcrição → banco

As tarifas de saneamento passam a valer com **procedência**: cada município aponta o
documento oficial guardado de onde saiu a sua tarifa, a tabela usada e a vigência.

| Etapa | Onde | Comando |
| :--- | :--- | :--- |
| 1. Soltar o material, com qualquer nome | `tarifas/entrada/` | — |
| 2. Registrar e mover para o arquivo definitivo | `tarifas/fontes/<prestador>/`, `fontes/registro.json` | `python tarifas/processar_entrada.py` |
| 3. Transcrever cada documento (tabelas, municípios, conta conferida) | `tarifas/transcricoes/<prestador>.json` | à mão, com o documento aberto |
| 4. Gravar no banco, com o antes e o depois | `triton/data/brazil_cities_tariffs.json`, `transcricoes/ALTERACOES.md` | `python tarifas/aplicar_transcricoes.py --aplicar` |
| 5. Ver o que falta e baixar | `o_que_buscar.html` (o lote de buscas), `transcricoes/FILA.md`, `lista_de_coleta.html` (mapa); o resultado de cada rodada é combinado na conversa | regerados nas etapas 2 e 4 |

Por município vale a transcrição de **vigência mais recente**; quando chega o reajuste de
um prestador, a transcrição nova entra ao lado da antiga. O atualizador automático
(`atualizar_tarifas.py`) não sobrescreve município documentado. Cada transcrição tem, em
`conferencia`, contas calculadas com os números impressos no documento, que
`tests/unit/test_transcricoes.py` exige reproduzidas pelo banco ao centavo.

**Documento geral.** Uma tabela que não lista os municípios vale para todos os do
prestador quando o próprio documento se declara a tabela única dele (o Anexo VII da
COSANPA, «municípios originalmente atendidos pela Cosanpa»; a TRA única da Rio+
Saneamento) ou traz a regra de enquadramento (as localidades «Tarifa B» da Águas do Rio).
A transcrição leva a lista explícita e, em `abrangencia`, a regra, que o município guarda
em `fonte_abrangencia` e o programa mostra na procedência. Prestador com tabelas regionais
sem o mapa município → região continua documentando só o município nomeado.

Cada município cai numa classe (`tarifas/procedencia.py`): documentado com as quatro
categorias; só a residencial documentada; documentado com vigência de mais de 12 meses (a
renovar); auditado pelo catálogo antigo, sem documento guardado; a confirmar; dado ruim.
O mapa da lista de coleta mostra a classe de cada cidade e, ao clicar, o documento-base.

Formas tarifárias que o banco ainda não representa ficam como «dado ruim», com o motivo,
e ainda não são suportadas: parcela fixa que muda com a faixa
(CESAN, desde 01/09/2026) e cobrança direta de todo o volume pelo preço da faixa (Valinhos,
Americana, Lucas do Rio Verde). A fórmula exponencial (CORSAN, COMUSA, DMAE de Porto Alegre)
se transcreve com o campo `exponencial` (docstring de `aplicar_transcricoes.py`).

---

## 📅 Quando Devo Atualizar as Tarifas?

Recomenda-se executar a rotina de atualização nos seguintes momentos:

1. **Reajustes Anuais da ANEEL (Energia Elétrica B1 Residencial)**:
   * Cada distribuidora de energia elétrica (ex: Celesc, Enel SP, Copel, Cemig, Neoenergia) possui uma **data-base anual** fixada em contrato de concessão para o seu reajuste tarifário.
   * O script baixa diretamente o CSV oficial de dados abertos da ANEEL e atualiza as 652 cidades de forma 100% automatizada.
2. **Reajustes Tarifários de Saneamento (Água e Esgoto)**:
   * Quando concessionárias estaduais (SABESP, COPASA, CASAN, EMBASA, COMPESA, CORSAN, SANEPAR, etc.) ou serviços municipais (ex: SEMAE, DAE, DMAE) publicam suas tabelas tarifárias anuais.
3. **Publicação de Novas Resoluções de Agências Reguladoras**:
   * Quando agências infranacionais (ARESC, ARSESP, ARSAB, AGERGS, ADASA, AGERBA, AGR, etc.) homologam novas estruturas tarifárias, novos valores de TFDI ou alterações nas alíquotas de esgoto.
4. **Antes de Emitir Relatórios Executivos ou Rodar Estudos Científicos**:
   * Para garantir que as métricas financeiras (VPL, Payback, TIR, LCOW e Economia Anual em R$) reflitam exatamente as tarifas vigentes no dia do estudo.

---

## 🚀 Como Atualizar as Tarifas (Linha de Comando)

Abra o terminal na pasta raiz da edição (`triton_brl`) e execute os comandos abaixo conforme a sua necessidade:

### 1. Atualização Completa (Energia ANEEL + Saneamento + Dashboard Interativo)
Executa o download dos dados da ANEEL, faz a varredura das fontes de saneamento, detecta alterações nas páginas oficiais e gera o relatório Markdown e o Dashboard HTML:
```bash
python tarifas/atualizar_tarifas.py
```

### 2. Modo Simulação / Dry-Run (Somente Leitura)
Executa toda a auditoria e compara as tarifas com as fontes governamentais **sem modificar os arquivos do banco de dados**:
```bash
python tarifas/atualizar_tarifas.py --check
```

### 3. Atualizar Apenas Tarifas de Energia Elétrica (ANEEL B1)
Atualiza exclusivamente as tarifas residenciais de eletricidade baixando o arquivo mais recente do Portal de Dados Abertos do Governo Federal:
```bash
python tarifas/atualizar_tarifas.py --aneel-only
```

### 4. Atualizar Apenas Tarifas de Saneamento (Água e Esgoto)
Atualiza exclusivamente as estruturas tarifárias de água, esgoto e TFDI:
```bash
python tarifas/atualizar_tarifas.py --sanitation-only
```

### 5. Atualizar Apenas um Estado (por UF)
Filtra a execução para um estado específico (ex: Santa Catarina, São Paulo, Minas Gerais):
```bash
python tarifas/atualizar_tarifas.py --uf SC
python tarifas/atualizar_tarifas.py --uf SP
```

### 6. Atualizar Apenas um Município
Filtra a execução para uma cidade específica:
```bash
python tarifas/atualizar_tarifas.py --city "Florianópolis"
python tarifas/atualizar_tarifas.py --city "São Paulo"
```

### 7. Monitorar Mudanças em URLs e Decretos Oficiais
Varre as URLs e armazena hashes SHA-256 das páginas de agências reguladoras para identificar se um novo decreto ou PDF foi publicado:
```bash
python tarifas/atualizar_tarifas.py --detect-changes
```

---

## 📁 Estrutura de Arquivos da Pasta `tarifas/`

| Arquivo | Descrição |
| :--- | :--- |
| 🐍 **`atualizar_tarifas.py`** | **Script principal de atualização automática, webscraping e monitoramento de mudanças.** |
| 📊 **`catalogo_tarifas_auditado_652.xlsx`** | Planilha Excel oficial formatada contendo o resumo consolidado de todas as 652 cidades. |
| 📄 **`catalogo_tarifas_auditado_652.csv`** | Versão em texto plano (CSV) do catálogo das 652 cidades para leitura rápida por scripts. |
| 📄 **`tarifas_detalhadas_auditadas.csv`** | Base de dados exaustiva com todas as faixas tarifárias (m³), cobranças mínimas, alíquotas de esgoto e fontes. |
| 🗄️ **`validated_cidades_50k.json`** | Banco de dados mestre estruturado em JSON com as coordenadas, prestadores e parâmetros de cada cidade. |
| 📖 **`FONTES_E_METODOLOGIA.md`** | Documentação completa com as fontes primárias oficiais (ANEEL, SINISA, Agências Reguladoras). |
| 📖 **`PANORAMA_TARIFAS_E_CONFIABILIDADE.md`** | Panorama analítico com as estatísticas de auditoria e confiabilidade do catálogo. |
| 📥 **`entrada/`** | Caixa de entrada do material coletado; fica só com o que ainda não foi processado. |
| 🗂️ **`fontes/`** | Documentos oficiais guardados, um diretório por prestador, e o registro (`registro.json`, `REGISTRO.md`). |
| 🐍 **`processar_entrada.py`** | Identifica, registra e move para `fontes/` o que está na entrada. |
| 🐍 **`registro_de_fontes.py`** | Registro dos documentos: conferir, registrar, mudar situação, reatribuir prestador. |
| ✍️ **`transcricoes/`** | Uma transcrição por documento; `ALTERACOES.md` e `historico.json` com o antes e o depois; `FILA.md` com o que falta. |
| 🐍 **`aplicar_transcricoes.py`** | Grava as transcrições no banco, com procedência, da vigência mais antiga para a mais nova. |
| 🐍 **`procedencia.py`** | Classe de procedência de cada município e geração do `FILA.md`. |
| 🔎 **`o_que_buscar.html`** | O que buscar: um cartão por cidade (ou companhia estadual) com o motivo e a busca pronta no Google (gerada por `gerar_o_que_buscar.py`). |
| 🗺️ **`lista_de_coleta.html`** | Lista de sites a visitar e estatísticas, com o mapa do documento-base por cidade (gerada por `gerar_lista_de_coleta.py`). |
| 📁 **`categorias/`** | Transcrições do formato anterior (CORSAN, CASAN), lidas pelos scripts `scripts/aplicar_categorias_*.py`. |

> **Onde ficam os demais scripts.** `audit_tariffs.py`, `generate_uf_tariffs_breakdown.py`,
> `plot_tariff_tiers_summary.py` e `build_tariff_workbook.mjs` existiam em cópias idênticas
> aqui e em [`../scripts/`](../scripts/). Passaram a existir apenas em `scripts/`, que é o
> diretório de scripts do projeto; duas cópias do mesmo arquivo divergem com o tempo.
>
> **Onde fica o banco tarifário.** O arquivo `brazil_cities_tariffs.json` é único e vive em
> [`../triton/data/`](../triton/data/), dentro do pacote — ver
> [`../docs/verificacao_e_validacao.md`](../docs/verificacao_e_validacao.md) §6 para o
> defeito que a duplicação anterior causou.

---

## 📊 Arquivos Gerados Automaticamente após a Execução

Ao rodar o `python tarifas/atualizar_tarifas.py`, os seguintes relatórios são atualizados na pasta `outputs/`:
* `outputs/relatorio_atualizacao_tarifas.md`: Relatório executivo com o log de cada município e eventuais alertas de revisão.
* `outputs/dashboard_tarifas.html`: Dashboard visual e interativo em HTML para navegar, filtrar por estado/grau de confiança e inspecionar os links oficiais de cada cidade no navegador.

---

## 📥 Material recebido: registro obrigatório

Todo PDF, planilha ou página oficial que chega para a base é registrado em
`tarifas/fontes/registro.json` por `tarifas/registro_de_fontes.py`, que guarda a impressão
digital SHA-256, a data, o prestador, o conteúdo, a vigência e o que foi feito com ele.
Um arquivo reenviado é reconhecido pela impressão digital, ainda que com outro nome.
`tarifas/fontes/REGISTRO.md`, gerado do registro, diz o que já chegou e o que falta
coletar, por prestador:

```bash
python tarifas/registro_de_fontes.py conferir arquivo.pdf
python tarifas/registro_de_fontes.py registrar arquivo.pdf --prestador SABESP --conteudo "Deliberação ARSESP, todas as categorias" --vigencia 01/01/2026
```

