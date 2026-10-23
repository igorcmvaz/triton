# 📁 Modelos e Templates — Triton

Esta pasta reúne todos os arquivos de template e modelos estruturados utilizados pelo **Triton** para importação, simulação e configuração de projetos.

---

## 📋 Catálogo de Templates

| Arquivo | Formato | Descrição e Finalidade |
|---|---|---|
| [`template_consumo_diario_365dias.csv`](template_consumo_diario_365dias.csv) | CSV (ponto e vírgula `;`) | Série diária de 365 dias de consumo de água (litros/dia) para importação na aba **Edificação** da interface gráfica. |
| [`template_projeto_base.triton`](template_projeto_base.triton) | JSON (.triton) | Estrutura canônica de arquivo de projeto do Triton contendo localização, dados prediais, dimensionamento e parâmetros econômicos. |
| [`template_cenarios_simulacao.csv`](template_cenarios_simulacao.csv) | CSV (ponto e vírgula `;`) | Matriz de múltiplos cenários para execução automatizada de simulações em lote via CLI (`triton cli batch`). |
| [`template_serie_pluviometrica.csv`](template_serie_pluviometrica.csv) | CSV (ponto e vírgula `;`) | Modelo padrão para importação de séries históricas personalizadas de precipitação diária (`Data;Chuva_mm`). |

---

## 🛠️ Instruções de Uso

### 1. Importação de Demanda Diária na Interface (GUI)
1. Abra o Triton e navegue até a aba **Edificação**.
2. No painel de demanda, selecione **Importar Série Diária**.
3. Escolha o arquivo `template_consumo_diario_365dias.csv` (ou preencha seus dados reais com base nele).

### 2. Simulação em Lote via CLI
Execute no terminal:
```bash
python triton/cli.py batch --scenarios templates/template_cenarios_simulacao.csv --city "Florianópolis" --uf "SC"
```
