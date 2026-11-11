# Triton — Edição Brasil

*Dimensionamento e simulação de aproveitamento de água de chuva*

[![Python Version](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI Framework](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licence: academic source-available](https://img.shields.io/badge/Licence-academic%20source--available-lightgrey.svg)](LICENSE.md)
[![Research Group](https://img.shields.io/badge/UFSC-Ambientes%20Sustent%C3%A1veis-005a36)](https://sustainability.ufsc.br/)

*English: [docs/en/README.md](docs/en/README.md) — resumo em inglês, com a documentação técnica em [`docs/en/`](docs/en/).*

O **Triton** é uma plataforma computacional avançada desenvolvida pelo **Grupo de Pesquisa em Ambientes Sustentáveis da Universidade Federal de Santa Catarina (UFSC)** para dimensionamento, simulação hidrológica diária, análise de viabilidade econômico-financeira de alta fidelidade, avaliação de ciclo de vida ambiental (ACV) e tomada de decisão multicritério robusta (**TOPSIS** e **SMAA-VIKOR**).

---

## Esta é a Edição Brasil (BRL)

O programa sai em três edições, do mesmo código e com o mesmo motor de cálculo e número de versão (ver o
[README do repositório](../README.md)). A **Edição Brasil** traz os dados brasileiros auditados: base
climática CLIMBra (652 cidades, CMIP6, 19 modelos), tarifas de água e esgoto de 652 municípios com procedência
por documento, energia da ANEEL, custos de referência em reais, fatores de emissão do MCTI e as certificações e incentivos
nacionais (AQUA-HQE, Selo Casa Azul, IPTU Verde). Os recursos 2 e 3 abaixo, a base climática nacional e os
fatores brasileiros são desta edição. O mapa do que cada edição mostra, onde está no código e o que vai em cada
pacote está em [`docs/edicoes.md`](docs/edicoes.md).

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

3. **Engenharia de Custos Paramétrica (Edição Brasil):**
   - Catálogo de referência em reais para tubulações (DN 50, 75, 100 e 150 mm), conexões, registros, filtros e reservatórios; só os preços de reservatório têm fonte e data registradas, e o usuário pode digitar os seus valores.
   - Tabela de fatores regionais por UF: existe e é testada, mas hoje não altera o investimento do projeto (manual, seção 10).
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
   - Planta 3D em DXF, esquema 3D com as medidas reais, volumetria girável no programa e exportação em glTF (`.glb`) e HTML interativo, além do manifesto BIM lido pelo Revit ([`integrations/revit`](additional_material/integrations/revit/README.md)).
   - Arranjo pré-preenchido pelo estudo conforme ABNT NBR 15527:2019 e NBR 5626:2020: filtro, descarte inicial, freio d'água, sucção flutuante com válvula de pé e crivo, chaves de nível, respiros com tela, extravasores (ladrão sifonado com antirrefluxo na cisterna; aviso visível na caixa), limpeza com registro, registros de manutenção dos dois lados da bomba, retenção no recalque, quadro de comando e backup potável (hidrômetro, registro e válvula solenoide) descarregando por *air gap* na caixa superior.
   - Volumetria em WebGL ([three.js](https://threejs.org)), a mesma no programa e no HTML exportado: peças detalhadas (tanques, motobomba, filtro, descarte, registros, válvula solenoide, hidrômetro, freio d'água, sucção flutuante), materiais físicos, céu HDRI do Poly Haven (CC0), sombras, fluxo animado por sistema, corte por cota, raio-X, medição e imagem PNG. Funciona sem internet; sem WebGL, a aba usa o visualizador simples. Código em [`web/volumetria`](web/volumetria/README.md).

---

## Estado da versão 0.1.0

**Pronto.** Balanço diário, dimensionamento, economia com a base tarifária de 652 municípios, ACV, linha de
tratamento, certificações, decisão multicritério, modulação probabilística, laudos em PDF, exportações CAD/BIM, o
manual completo e a documentação de cada conjunto de dados. A base CLIMBra (652 municípios, 19 modelos, 37.164
séries) vai embutida em 19 arquivos, um por modelo, todos abaixo de 50 MiB.

**Ainda não há.** Chuva medida (as séries da base e as dos exemplos são do CLIMBra, isto é, modeladas); tarifa de
energia com tributos e bandeiras; fonte e data para todos os preços de referência do CAPEX (só os de reservatório as
têm); estrutura tarifária conferida nos 5 municípios do Tocantins (grau C).

**Limitações conhecidas.** 140 municípios com a referência de energia expirada; custo anual do resumo sem as rotinas
de manutenção (entram no fluxo de caixa à parte); espanhol e chinês traduzidos em parte; algumas licenças de dados
por verificar. A lista completa está nas [notas de lançamento](docs/NOTAS_DE_LANCAMENTO_0.1.0.md) e no
[histórico de versões](CHANGELOG.md).

---

## 📚 Documentação e Artigos Técnicos

- [Manual do usuário (PDF)](manual/Manual-Triton.pdf) — a Edição Internacional publica o manual em inglês
- [Notas de lançamento 0.1.0](docs/NOTAS_DE_LANCAMENTO_0.1.0.md) e [histórico de versões](CHANGELOG.md)
- [Dados da edição: fontes, licenças, cobertura e qualidade](docs/DADOS.md)
- [As três edições: Brasil, International e Ibérica](docs/edicoes.md)
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
triton_brl/
├── triton/                     # Pacote Python: motor de cálculo, interface e linha de comando
│   ├── core/                   # Hidrologia, economia, ACV, decisão multicritério, tarifas, unidades
│   ├── ui/                     # Interface desktop PySide6 (abas, gráficos, diálogos, traduções)
│   ├── data/                   # Bases embutidas: tarifas, custos, fatores de emissão, rotas de água
│   ├── docs/                   # Relatórios de validação e fluxogramas distribuídos com o programa
│   └── cli.py                  # Interface de linha de comando
├── tests/                      # Suíte automatizada: unit, integration, invariants, ui, benchmarking
├── manual/                     # O manual pronto: PDFs, site offline, volumes avulsos e casos
│                               #   (os geradores e as partes ficam no disco do mantenedor, fora do Git)
├── docs/                       # Documentação técnica: metodologia, verificação, procedência dos fatores
├── examples/                   # Estudos de caso e projetos de exemplo (.triton)
├── templates/                  # Modelos de projeto e planilhas de entrada
├── data/                       # Base CLIMBra (climbra_<modelo>.db), séries pluviométricas e referências do Netuno 4
├── tarifas/                    # Base tarifária auditada das 652 cidades
├── scripts/                    # Base CLIMBra, tarifas, auditoria e estudos em lote (não vão ao instalador)
├── additional_material/        # Biblioteca CAD/BIM, integração com Revit e documentos de referência
├── icons/                      # Ícones da aplicação
├── infos_licenses/             # Licença, textos do instalador e README distribuído
├── pyproject.toml              # Metadados do pacote (PEP 621); o estado de lançamento é declarado aqui
├── requirements.txt            # Dependências de produção
├── requirements-dev.txt        # Dependências de desenvolvimento e testes
├── CITATION.cff                # Como citar o programa
├── LICENSE.md                  # Licença: código-fonte disponível para fins acadêmicos
└── main.py                     # Ponto de entrada da aplicação desktop
```

A base climática compilada está **no Git**: um banco SQLite por modelo CMIP6, `data/climbra_<modelo>.db`
(19 arquivos de 40 a 43 MiB, 785 MiB no total, abaixo do limite de 50 MiB por arquivo do projeto, mais rígido que os 100 MiB do GitHub), mais o manifesto
`data/climbra_partes.json`. O programa as lê direto. Como foram geradas, divididas e verificadas: [`scripts/README.md`](scripts/README.md).

Fora do controle de versão, por tamanho, por serem regeneráveis ou por serem de terceiros: os CSV brutos da
CLIMBra (`climbra_data/`, ~6,5 GB), os documentos dos prestadores de saneamento (`tarifas/fontes/`) e o banco
que os reúne, as saídas de simulação em lote em `data/simulation_outputs/` (exceto as duas `Planilha.csv` de
referência do Netuno 4 e os três arquivos de teste do leitor), `tmp/`, e os laudos gerados em `reports/` (exceto `reports/exemplos/`).

---

## 🚀 Instalação e Execução

### Pré-requisitos
- Para usar sem Python: o instalador `.exe` para Windows (traz tudo) está no registro do Zenodo, DOI 10.5281/zenodo.23402916 (`Triton_Brasil_Setup_v0.1.0.exe`).
- Para desenvolver ou rodar a partir do código: Python 3.12 ou superior (o código usa a sintaxe de f-strings do 3.12).

### 1. Instalação em Modo de Desenvolvimento
```bash
# Acesse a pasta raiz do programa
cd triton_brl

# Instale o pacote e suas dependências
pip install -e .

# Ou instale via requirements:
pip install -r requirements-dev.txt
```

### 2. Executando a Versão Desktop
```bash
# A edição desta pasta já é o padrão:
python main.py

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

## 📦 Instalador Windows

O instalador não faz parte deste repositório: é publicado no registro do Zenodo (DOI [10.5281/zenodo.23402916](https://doi.org/10.5281/zenodo.23402916)). O repositório traz só o que é preciso para rodar o programa e a linha de comando a partir do código; as ferramentas de empacotamento ficam com o mantenedor. O que muda entre os pacotes das três edições está em [`docs/edicoes.md`](docs/edicoes.md).

---

## 🧪 Testes Automatizados

Para executar a suíte de testes unitários, testes de interface e validações de invariantes:

```bash
# Executar todos os testes:
pytest

# Só a base climática dividida por modelo (partes, manifesto e leitor):
pytest tests/unit/test_climbra_particionada.py tests/unit/test_climate_database.py -v

# Testes específicos com cobertura detalhada:
pytest tests/test_essencial.py tests/test_essencial_interface.py -v
```

---

## 📄 Licença, citação e créditos

Desenvolvido pelo **Grupo de Pesquisa em Ambientes Sustentáveis** — Universidade Federal de Santa Catarina (UFSC).
Código-fonte disponível para fins acadêmicos, com todos os direitos reservados e uso gratuito não comercial. Consulte o arquivo [`LICENSE.md`](LICENSE.md) para os termos completos. A citação do programa é obrigatória em qualquer trabalho que use os seus resultados ([`CITATION.cff`](CITATION.cff)):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações.* Universidade Federal de Santa Catarina (UFSC), Florianópolis, Brasil.

Dados: CLIMBra (Ballarin et al., 2023, *Scientific Data*, doi:10.1038/s41597-023-01956-z; CC0 1.0). Dúvidas e erros: igor.catao@posgrad.ufsc.br.
