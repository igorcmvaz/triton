# 💧⚡ Banco de Tarifas e Motor de Atualização (Netuno 5)

Esta pasta centraliza **todos os scripts de atualização, webscrapers, motores de auditoria, bases de dados homologadas e relatórios de governança tarifária** para os 652 municípios brasileiros analisados pelo Netuno.

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

Abra o terminal na pasta raiz do projeto (`NetunoReplicacao`) e execute os comandos abaixo conforme a sua necessidade:

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
| 🐍 **`audit_tariffs.py`** | Motor detalhado de auditoria de consistência, cálculo de scores de confiança (A, B, C, D) e validação de faixas. |
| 📊 **`catalogo_tarifas_auditado_652.xlsx`** | Planilha Excel oficial formatada contendo o resumo consolidado de todas as 652 cidades. |
| 📄 **`catalogo_tarifas_auditado_652.csv`** | Versão em texto plano (CSV) do catálogo das 652 cidades para leitura rápida por scripts. |
| 📄 **`tarifas_detalhadas_auditadas.csv`** | Base de dados exaustiva com todas as faixas tarifárias (m³), cobranças mínimas, alíquotas de esgoto e fontes. |
| 🗄️ **`validated_cidades_50k.json`** | Banco de dados mestre estruturado em JSON com as coordenadas, prestadores e parâmetros de cada cidade. |
| 🐍 **`generate_uf_tariffs_breakdown.py`** | Gera gráficos e tabelas de dispersão de tarifas por Unidade da Federação. |
| 🐍 **`plot_tariff_tiers_summary.py`** | Gera gráficos da estrutura de blocos e faixas progressivas de consumo. |
| 📖 **`FONTES_E_METODOLOGIA.md`** | Documentação completa com as fontes primárias oficiais (ANEEL, SINISA, Agências Reguladoras). |
| 📖 **`PANORAMA_TARIFAS_E_CONFIABILIDADE.md`** | Panorama analítico com as estatísticas de auditoria e confiabilidade do catálogo. |

---

## 📊 Arquivos Gerados Automaticamente após a Execução

Ao rodar o `python tarifas/atualizar_tarifas.py`, os seguintes relatórios são atualizados na pasta `outputs/`:
* `outputs/relatorio_atualizacao_tarifas.md`: Relatório executivo com o log de cada município e eventuais alertas de revisão.
* `outputs/dashboard_tarifas.html`: Dashboard visual e interativo em HTML para navegar, filtrar por estado/grau de confiança e inspecionar os links oficiais de cada cidade no navegador.
