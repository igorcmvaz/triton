# Netuno 5 — Dimensionamento e Simulação de Aproveitamento de Água de Chuva

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Research Group](https://img.shields.io/badge/UFSC-Gestão%20do%20Espaço%20Sustentável-005a36)](https://sustainability.ufsc.br/)

O **Netuno 5** é uma plataforma computacional avançada desenvolvida pelo **Grupo de Pesquisa Gestão do Espaço Sustentável da Universidade Federal de Santa Catarina (UFSC)** para dimensionamento, simulação hidrológica diária, análise de viabilidade econômico-financeira de alta fidelidade, avaliação de ciclo de vida ambiental (ACV) e tomada de decisão multicritério robusta (**TOPSIS** e **SMAA-VIKOR**).

---

## 🌟 Principais Recursos e Inovações Metodológicas

1. **Balanço Hídrico Diário de Alta Precisão (Yield-After-Spill - YAS):**
   - Simulação contínua com descarte inicial de primeira chuva (*first flush*) configurável (fixo ou por período de estiagem).
   - Suporte a demandas não potáveis constantes ou moduladas (sazonalidade mensal, semanal e horária).
   - Varredura paramétrica de volumes de reservatório inferior e superior com motobomba.

2. **Base Tarifária Nacional Auditada de 652 Municípios:**
   - Estrutura tarifária progressiva por faixas de consumo de água e esgoto regulado (0% a 100%).
   - Tarifas residenciais de energia elétrica B1 homologadas pela ANEEL por distribuidora.
   - Premissa de desembolso real: tributos e impostos inclusos nos cálculos de economia tarifária.

3. **Engenharia de Custos Paramétrica e Fatores Regionais SINAPI / CUB (27 UFs):**
   - Composições paramétricas SINAPI para tubulações (DN 50, 75, 100 e 150 mm), conexões, registros e filtros.
   - Ponderação regional por estado (55% materiais, 30% mão de obra, 15% logística).
   - Fluxo de caixa completo: CAPEX, OPEX anual, VPL líquido, TIR, Payback Simples e Descontado, e LCOW.

4. **Avaliação Simplificada de Ciclo de Vida (ACV / Pegada de Carbono):**
   - Sincronização física bidirecional com os materiais do CAPEX.
   - Balanço de carbono ao longo de 20 anos: emissões incorporadas nos materiais + energia operacional vs. emissões evitadas no tratamento da água da rede.

5. **Tomada de Decisão Multicritério Integrada:**
   - **🏆 TOPSIS:** Ordenação por proximidade relativa às soluções ideais sob perfis de pesos declarados (Equilibrado, Econômico, Ambiental, Técnico ou Customizado).
   - **🎲 SMAA-VIKOR (Padrão Cryspin):** Análise de aceitabilidade estocástica via simulações Monte Carlo (1.000 a 50.000 simulações) no simplex uniforme de pesos, calculando índices de aceitabilidade de 1º lugar ($b_i^1$), fatores de confiança e vetor central de pesos ($w_i^c$).

6. **Enquadramento em Certificações Sustentáveis & Critérios ESG:**
   - **🌱 LEED v4 / v4.1 (BD+C & O+M):** Até 8 pontos diretos na Categoria Eficiência Hídrica (WEc1 Uso Externo: 0 a 2 pts; WEc2 Uso Interno: 1 a 6 pts para reduções de 20% a 45%+).
   - **💧 Processo AQUA-HQE (Fundação Vanzolini):** Avaliação de desempenho na Categoria 4 (Gestão da Água) com enquadramento em Nível Base (≥ 10%), Boas Práticas (≥ 25%) ou Excelente (≥ 40%).
   - **🏠 Selo Casa Azul CAIXA:** Pontuação e elegibilidade direta no Critério 2.1 (Conservação de Recursos Hídricos) nas graduações Prata (+2 pts), Ouro (+3 pts) e Diamante (+5 pts), com bonificação em financiamentos habitacionais.
   - **📊 GRI Standard 303 & Water Positive Index:** Quantificação auditável de captação evitada de água tratada (GRI 303-3) e circularidade hídrica no empreendimento (GRI 303-5).

---

## 📚 Documentação e Artigos Técnicos

- [Metodologia, equações e fronteiras do modelo](docs/metodologia.md)
- [Relatório de Verificação e Validação](docs/verificacao_e_validacao.md)
- [Fluxogramas Metodológicos](netuno/docs/fluxogramas_metodologicos.md)
- [Diretrizes de Decisão Robusta](netuno/docs/proximos_passos_decisao_robusta.md)
- [Relatório de Validação dos Algoritmos](netuno/docs/relatorio_validacao.md)

---

## 🏛️ Arquitetura dos Módulos Principais

| Módulo | Descrição Técnica |
| :--- | :--- |
| [`netuno.core.simulation`](netuno/core/simulation.py) | Motor de simulação de balanço hídrico diário (YAS), descarte de primeira chuva e varredura |
| [`netuno.core.economic`](netuno/core/economic.py) | Análise econômico-financeira (tarifas progressivas, fluxo de caixa, VPL, TIR e Payback) |
| [`netuno.core.cost_estimates`](netuno/core/cost_estimates.py) | Engenharia de custos paramétricos, composições SINAPI e fatores regionais por UF |
| [`netuno.core.tariffs_database`](netuno/core/tariffs_database.py) | Catálogo auditado de tarifas de saneamento e eletricidade ANEEL para 652 cidades |
| [`netuno.core.environmental_sync`](netuno/core/environmental_sync.py) | Sincronização física de materiais, energia e pegada de carbono para ACV |
| [`netuno.core.topsis`](netuno/core/topsis.py) | Algoritmo de tomada de decisão multicritério (TOPSIS e SMAA-VIKOR) |

---

## 📂 Estrutura do Repositório

```text
Netuno5_0_7 (atual)/
├── netuno/                     # Pacote Python Principal (Core Engine & Desktop UI)
│   ├── core/                   # Motores de cálculo (hidrologia, economia, ACV, MCDM, tarifas)
│   ├── ui/                     # Interface gráfica desktop PySide6 (abas, gráficos, diálogos)
│   ├── data/                   # Bases de dados embutidas (tarifas municipais, custos SINAPI)
│   ├── docs/                   # Documentação técnica e fluxogramas metodológicos
│   └── cli.py                  # Interface de linha de comando (CLI)
├── Netuno future files for 652 cities/  # Base climática CMIP6 (histórico + SSP245/SSP585) — exigida pelo motor
├── LegadoWeb/                  # Arquivo histórico da versão web descontinuada (.tar.xz)
├── data/                       # Arquivos de dados, séries pluviométricas e dicionários
├── templates/                  # Modelos de projetos (.netuno) e planilhas de entrada
├── icons/                      # Identidade visual e ícones oficiais da aplicação
├── scripts/                    # Scripts de auditoria, estudos de caso e processamento em lote
├── tests/                      # Suíte de testes automatizados (unitários, integração e UI)
├── infos_licenses/             # Licenças, documentação legal e scripts Inno Setup
├── pyproject.toml              # Metadados e configuração de empacotamento padrão PEP 517/621
├── requirements.txt            # Dependências de produção
├── requirements-dev.txt        # Dependências de desenvolvimento e testes
├── build_exe.py                # Script utilitário de compilação (PyInstaller + Inno Setup)
├── setup_script.iss            # Script de compilação do Instalador Inno Setup 6
├── main.py                     # Ponto de entrada da aplicação Desktop
└── README.md                   # Documentação principal
```

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Para usar: o instalador `.exe` para Windows já traz tudo, sem Python.
- Para desenvolver ou rodar a partir do código: Python 3.12 ou superior (o código usa a sintaxe de f-strings do 3.12).

### 1. Instalação em Modo de Desenvolvimento
```bash
# Acesse a pasta raiz do programa
cd "Netuno5_0_7 (atual)"

# Instale o pacote e suas dependências
pip install -e .

# Ou instale via requirements:
pip install -r requirements-dev.txt
```

### 2. Executando a Versão Desktop
```bash
# Via script principal:
python main.py

# Ou via comando registrado no PATH:
netuno-gui
```

### 3. Executando via Linha de Comando (CLI)
```bash
# Exibir opções e ajuda do CLI:
python -m netuno.cli --help

# Ou diretamente:
netuno --help
```

> **Nota sobre a versão Web:** a interface web experimental (FastAPI + React, com o Chromium
> como interface) foi **descontinuada na versão 5.0.7**. O Netuno é agora exclusivamente
> desktop. O código está preservado, comprimido, em [`LegadoWeb/`](LegadoWeb/README.md).

---

## 📦 Compilação do Executável Windows (.exe e Instalador)

O script [`build_exe.py`](build_exe.py) automatiza a compilação do executável standalone e do instalador oficial:

```bash
# Compilação padrão (pasta standalone em dist/Netuno/):
python build_exe.py

# Compilação limpa com executável único:
python build_exe.py --clean --onefile

# Compilação com geração automática do instalador Inno Setup (.exe):
python build_exe.py --clean --installer
```

O instalador compilado será gerado em `dist/Netuno_Setup_5_0_7.exe`.

---

## 🧪 Testes Automatizados

Para executar a suíte de testes unitários, testes de interface e validações de invariantes:

```bash
# Executar todos os testes:
pytest

# Executar testes específicos com cobertura detalhada:
pytest tests/unit/test_mcdm_methods.py tests/ui/ -v
```

---

## 📄 Licença e Créditos

Desenvolvido pelo **Grupo de Pesquisa Gestão do Espaço Sustentável** — Universidade Federal de Santa Catarina (UFSC).  
Distribuído sob a **GNU General Public License v3.0 ou posterior**. Consulte o arquivo [`LICENSE`](LICENSE) para o texto integral.
