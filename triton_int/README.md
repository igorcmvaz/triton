# Triton — Dimensionamento e Simulação de Aproveitamento de Água de Chuva

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Research Group](https://img.shields.io/badge/UFSC-Gestão%20do%20Espaço%20Sustentável-005a36)](https://sustainability.ufsc.br/)

*English: [README.en.md](README.en.md) — resumo em inglês, com a documentação técnica em [`docs/en/`](docs/en/).*

O **Triton** é uma plataforma computacional avançada desenvolvida pelo **Grupo de Pesquisa em Ambientes Sustentáveis da Universidade Federal de Santa Catarina (UFSC)** para dimensionamento, simulação hidrológica diária, análise de viabilidade econômico-financeira de alta fidelidade, avaliação de ciclo de vida ambiental (ACV) e tomada de decisão multicritério robusta (**TOPSIS** e **SMAA-VIKOR**).

---

## Duas edições: Brasil (BRL) e International (INT)

O programa sai em duas edições, do mesmo código e com o mesmo motor de cálculo. A
**Edição Brasil** traz os dados brasileiros auditados: base climática CLIMBra (652
cidades, CMIP6), tarifas de água e esgoto de 652 municípios com procedência por documento,
energia da ANEEL, custos em reais, fatores de emissão do MCTI e as certificações e
incentivos nacionais (AQUA-HQE, Selo Casa Azul, IPTU Verde). A **International Edition**
é o núcleo neutro: abre em inglês, com a moeda escolhida pelo usuário e tarifa, custos e
fatores de emissão informados por ele, e só as certificações internacionais (LEED, EDGE,
GRI). Os recursos 2 e 3 abaixo, a base climática nacional e os fatores brasileiros são da
Edição Brasil. O mapa completo — o que o usuário vê, onde está no código, o que vai em
cada pacote — está em [`docs/edicoes.md`](docs/edicoes.md).

---

## 🌟 Principais Recursos e Inovações Metodológicas

1. **Balanço Hídrico Diário de Alta Precisão:**
   - Extravasamento calculado antes do consumo, com a chuva do dia disponível para a demanda do dia: ordem intermediária entre as regras YAS e YBS (seção do balanço diário no manual).
   - Simulação contínua com descarte inicial de primeira chuva (*first flush*) em três modos: em todos os eventos, no primeiro evento após estiagem ou a cada intervalo de dias.
   - Suporte a demandas não potáveis constantes ou moduladas (modulação semanal, mensal ou por série diária).
   - Varredura paramétrica de volumes de reservatório inferior e superior com motobomba.

2. **Base Tarifária Nacional Auditada de 652 Municípios (Edição Brasil):**
   - Estrutura tarifária progressiva por faixas de consumo de água e esgoto regulado (0% a 100%).
   - Tarifas residenciais de energia elétrica B1 homologadas pela ANEEL por distribuidora.
   - Premissa de desembolso real: tributos e impostos inclusos nos cálculos de economia tarifária.

3. **Engenharia de Custos Paramétrica e Fatores Regionais SINAPI / CUB (27 UFs; Edição Brasil):**
   - Composições paramétricas SINAPI para tubulações (DN 50, 75, 100 e 150 mm), conexões, registros e filtros.
   - Ponderação regional por estado (55% materiais, 30% mão de obra, 15% logística).
   - Fluxo de caixa completo: CAPEX, OPEX anual, VPL líquido, TIR, Payback Simples e Descontado, e LCOW.

4. **Avaliação Simplificada de Ciclo de Vida (ACV / Pegada de Carbono):**
   - Sincronização física bidirecional com os materiais do CAPEX.
   - Balanço de carbono ao longo de 20 anos: emissões incorporadas nos materiais + energia operacional vs. emissões evitadas no tratamento da água da rede.

5. **Tomada de Decisão Multicritério Integrada:**
   - **🏆 TOPSIS:** Ordenação por proximidade relativa às soluções ideais sob perfis de pesos declarados (Equilibrado, Econômico, Ambiental, Técnico ou Customizado).
   - **🎲 SMAA-VIKOR:** Análise de aceitabilidade estocástica via simulações Monte Carlo (1.000 a 50.000 simulações) no simplex uniforme de pesos, calculando índices de aceitabilidade de 1º lugar ($b_i^1$), fatores de confiança e vetor central de pesos ($w_i^c$). Implementação independente sobre NumPy, seguindo o desenho de [`crispyn`](https://github.com/energyinpython/crispyn) (A. Bączkiewicz, MIT) e as formulações de Lahdelma & Salminen (2001) e Opricovic & Tzeng (2004).

6. **Enquadramento em Certificações Sustentáveis & Critérios ESG:**
   - **🌱 LEED v4 / v4.1 (BD+C & O+M):** Até 8 pontos diretos na Categoria Eficiência Hídrica (WEc1 Uso Externo: 0 a 2 pts; WEc2 Uso Interno: 1 a 6 pts para reduções de 25% a 50%, com pré-requisito de 20%). Registro de projetos aberto até 30/06/2027.
   - **🌱 LEED v5 BD+C (novembro de 2025):** WEc2 *Enhanced Water Efficiency* até 8 pontos, pela Opção 1 (redução do uso de água do projeto inteiro, de 30% a 65%) ou pela soma das Opções 2 a 6, incluindo a Opção 6 de reúso no lote (2 pts), além do ponto de reúso do SSc3.
   - **🏗️ EDGE (IFC / Banco Mundial):** Barra de água pela medida WEM14, comparada ao caso-base local.
   - **💧 Processo AQUA-HQE (Fundação Vanzolini):** Avaliação de desempenho na Categoria 4 (Gestão da Água) com enquadramento em Nível Base (≥ 10%), Boas Práticas (≥ 25%) ou Excelente (≥ 40%).
   - **🏠 Selo Casa Azul CAIXA:** Pontuação e elegibilidade direta no Critério 2.1 (Conservação de Recursos Hídricos) nas graduações Prata (+2 pts), Ouro (+3 pts) e Diamante (+5 pts), com bonificação em financiamentos habitacionais.
   - **📊 GRI Standard 303 & Water Positive Index:** Quantificação auditável de captação evitada de água tratada (GRI 303-3) e circularidade hídrica no empreendimento (GRI 303-5).

7. **Planta 3D, Esquema e Volumetria da Tubulação:**
   - Trechos organizados pelo projetista na ordem de montagem, a partir de pontos de conexão dos componentes (`RS-01:topo`, `RS-01:fundo`, laterais superior e inferior).
   - Conferência do destino de cada trecho, declividade mínima dos sistemas por gravidade (ABNT NBR 10844) e recusa de tubos que ocupam o mesmo espaço.
   - Planta 3D em DXF, esquema 3D com as medidas reais, volumetria girável no programa e exportação em glTF (`.glb`) e HTML interativo, além do manifesto BIM lido pelo Revit ([`integrations/revit`](integrations/revit/README.md)).
   - Arranjo pré-preenchido pelo estudo conforme ABNT NBR 15527:2019 e NBR 5626:2020: filtro, descarte inicial, freio d'água, sucção flutuante com válvula de pé e crivo, chaves de nível, respiros com tela, extravasores (ladrão sifonado com antirrefluxo na cisterna; aviso visível na caixa), limpeza com registro, registros de manutenção dos dois lados da bomba, retenção no recalque, quadro de comando e backup potável (hidrômetro, registro e válvula solenoide) descarregando por *air gap* na caixa superior.
   - Volumetria em WebGL ([three.js](https://threejs.org)), a mesma no programa e no HTML exportado: peças detalhadas (tanques, motobomba, filtro, descarte, registros, válvula solenoide, hidrômetro, freio d'água, sucção flutuante), materiais físicos, céu HDRI do Poly Haven (CC0), sombras, fluxo animado por sistema, corte por cota, raio-X, medição e imagem PNG. Funciona sem internet; sem WebGL, a aba usa o visualizador simples. Código em [`web/volumetria`](web/volumetria/README.md).

---

## 📚 Documentação e Artigos Técnicos

- [Manual do usuário (PDF)](manual/Manual-Triton.pdf) — em inglês, [`manual/en/Triton-User-Manual.pdf`](manual/en/Triton-User-Manual.pdf), o que a International Edition abre
- [As duas edições, Brasil e International](docs/edicoes.md)
- [Metodologia, equações e fronteiras do modelo](docs/metodologia.md)
- [Relatório de Verificação e Validação](docs/verificacao_e_validacao.md)
- [Fluxogramas Metodológicos](triton/docs/fluxogramas_metodologicos.md)
- [Diretrizes de Decisão Robusta](triton/docs/proximos_passos_decisao_robusta.md)
- [Relatório de Validação dos Algoritmos](triton/docs/relatorio_validacao.md)

---

## 🏛️ Arquitetura dos Módulos Principais

| Módulo | Descrição Técnica |
| :--- | :--- |
| [`triton.core.simulation`](triton/core/simulation.py) | Motor de simulação de balanço hídrico diário (extravasamento antes do consumo), descarte de primeira chuva e varredura |
| [`triton.core.economic`](triton/core/economic.py) | Análise econômico-financeira (tarifas progressivas, fluxo de caixa, VPL, TIR e Payback) |
| [`triton.core.cost_estimates`](triton/core/cost_estimates.py) | Engenharia de custos paramétricos, composições SINAPI e fatores regionais por UF |
| [`triton.core.tariffs_database`](triton/core/tariffs_database.py) | Catálogo auditado de tarifas de saneamento e eletricidade ANEEL para 652 cidades |
| [`triton.core.environmental_sync`](triton/core/environmental_sync.py) | Sincronização física de materiais, energia e pegada de carbono para ACV |
| [`triton.core.topsis`](triton/core/topsis.py) | Algoritmo de tomada de decisão multicritério (TOPSIS e SMAA-VIKOR) |

---

## 📂 Estrutura do Repositório

```text
triton/
├── triton/                     # Pacote Python: motor de cálculo, interface e linha de comando
│   ├── core/                   # Hidrologia, economia, ACV, decisão multicritério, tarifas, unidades
│   ├── ui/                     # Interface desktop PySide6 (abas, gráficos, diálogos, traduções)
│   ├── data/                   # Bases embutidas: tarifas, custos, fatores de emissão, rotas de água
│   ├── docs/                   # Relatórios de validação e fluxogramas distribuídos com o programa
│   └── cli.py                  # Interface de linha de comando
├── tests/                      # Suíte automatizada: unit, integration, invariants, ui, benchmarking
├── manual/                     # Fonte do manual: partes/, apendices/, casos/, figuras/ e geradores
│                               #   (Manual-Triton.md e .pdf são gerados e não são versionados)
├── docs/                       # Documentação técnica: metodologia, verificação, procedência dos fatores
├── examples/                   # Estudos de caso e projetos de exemplo (.triton)
├── templates/                  # Modelos de projeto e planilhas de entrada
├── data/                       # Séries pluviométricas e planilhas de referência do Netuno 4
├── tarifas/                    # Base tarifária auditada das 652 cidades
├── scripts/                    # Auditoria, estudos em lote e geração de artigos (não vão ao instalador)
├── integrations/               # Integração com Revit
├── additional_material/        # Biblioteca CAD/BIM e documentos de referência
├── icons/                      # Ícones da aplicação
├── infos_licenses/             # Licença, textos do instalador e README distribuído
├── .github/workflows/          # Integração contínua: núcleo com e sem numba, replicação do Netuno 4
├── pyproject.toml              # Metadados do pacote (PEP 621); o estado de lançamento é declarado aqui
├── requirements.txt            # Dependências de produção
├── requirements-dev.txt        # Dependências de desenvolvimento e testes
├── build_exe.py                # Compilação do executável (PyInstaller) e do instalador
├── Triton.spec                 # Especificação do PyInstaller
├── setup_script.iss            # Script do instalador Inno Setup 6
├── CITATION.cff                # Como citar o programa
└── main.py                     # Ponto de entrada da aplicação desktop
```

Fora do controle de versão, por tamanho ou por serem regeneráveis: a base climática
CMIP6 — os CSV brutos (`climbra_data/`, ~6,5 GB) e o banco compilado `data/climbra.db`
(~784 MB, gerado por `scripts/compilar_base_climbra.py` e embutido no executável da Edição
Brasil pelo `build_exe.py`) —, as saídas de
simulação em lote em `data/simulation_outputs/` (exceto as `Planilha.csv` de referência),
`tmp/`, os laudos gerados em `reports/` (exceto `reports/exemplos/`), o manual montado e o PDF.

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Para usar: o instalador `.exe` para Windows já traz tudo, sem Python.
- Para desenvolver ou rodar a partir do código: Python 3.12 ou superior (o código usa a sintaxe de f-strings do 3.12).

### 1. Instalação em Modo de Desenvolvimento
```bash
# Acesse a pasta raiz do programa
cd triton

# Instale o pacote e suas dependências
pip install -e .

# Ou instale via requirements:
pip install -r requirements-dev.txt
```

### 2. Executando a Versão Desktop
```bash
# Via script principal (Edição Brasil):
python main.py

# Edição Brasil ou Internacional explicitamente:
python main_brl.py          # ou: python main.py --edition brl
python main_int.py          # ou: python main.py --edition int

# Ou via comando registrado no PATH:
triton-gui
```

### 3. Executando via Linha de Comando (CLI)
```bash
# Exibir opções e ajuda do CLI:
python -m triton.cli --help

# Ou diretamente:
triton --help
```

> **Nota sobre a versão Web:** a interface web experimental (FastAPI + React, com o Chromium
> como interface) foi **descontinuada**. O Triton é exclusivamente desktop.

---

## 📦 Compilação do Executável Windows (.exe e Instalador)

O script [`build_exe.py`](build_exe.py) automatiza a compilação do executável standalone e do instalador oficial:

```bash
# Compilação padrão (pasta standalone em dist/Triton/):
python build_exe.py

# Compilação limpa com executável único:
python build_exe.py --clean --onefile

# Compilação com geração automática do instalador Inno Setup (.exe):
python build_exe.py --clean --installer

# Edição Internacional (dist/Triton_INT/) ou as duas edições:
python build_exe.py --edition int
python build_exe.py --edition both --clean
```

O instalador compilado será gerado em `dist/Triton_Setup_1_0_0.exe`, a partir da Edição
Brasil em `dist/Triton/`, e o da International em `dist/Triton_INT_Setup_1_0_0.exe`, a
partir de `dist/Triton_INT/`. A International sai sem a base CLIMBra e sem a pasta
`tarifas/`; o que mais muda entre os pacotes está em [`docs/edicoes.md`](docs/edicoes.md).
A compilação exige Python 3.12 ou superior.

A Edição Brasil sai com a base CLIMBra compilada embutida (`data/climbra.db`, 652 cidades):
o `build_exe.py` a compila a partir de `climbra_data/` se o banco faltar e interrompe se
não houver nenhum dos dois, em vez de gerar um instalador sem a base. Detalhes em
[`docs/instalador.md`](docs/instalador.md).

---

## 🧪 Testes Automatizados

Para executar a suíte de testes unitários, testes de interface e validações de invariantes:

```bash
# Executar todos os testes:
pytest

# Executar testes específicos com cobertura detalhada:
pytest tests/test_essencial.py tests/test_essencial_interface.py -v
```

---

## 📄 Licença e Créditos

Desenvolvido pelo **Grupo de Pesquisa em Ambientes Sustentáveis** — Universidade Federal de Santa Catarina (UFSC).  
Distribuído sob a **GNU General Public License v3.0 ou posterior**. Consulte o arquivo [`LICENSE`](LICENSE) para o texto integral.
