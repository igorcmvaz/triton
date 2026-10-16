# Triton — Edição Portugal

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licença: código-fonte disponível para fins académicos](https://img.shields.io/badge/licen%C3%A7a-fins%20acad%C3%A9micos-lightgrey.svg)](LICENSE.md)
[![Grupo de investigação](https://img.shields.io/badge/UFSC-Ambientes%20Sustent%C3%A1veis-005a36)](https://sustainability.ufsc.br/)

O **Triton** dimensiona sistemas de aproveitamento de água da chuva em edifícios. Simula o balanço hídrico
diário sobre uma série de precipitação, varre uma gama de volumes de reservatório e indica o que cada volume
rende em água poupada, em dinheiro e em carbono do ciclo de vida; depois ordena as alternativas por decisão
multicritério (TOPSIS e SMAA-VIKOR).

Esta é a **Edição Portugal**: abre em português de Portugal, trabalha em euros e traz dados portugueses.

- **Precipitação E-OBS por concelho**, 1950 a 2025 (E-OBS v33.0e, grelha de 0,1°, limites CAOP 2025): 278 dos
  308 concelhos têm série; os restantes ficam de fora por terem mais de 1% de dias sem dado em 1991–2020. Para
  esses locais usa-se uma série do próprio utilizador.
- **Tarifários de água e saneamento** de Lisboa, Porto e Funchal, com a entidade gestora, a vigência e a fonte
  de cada valor.
- **Exemplos completos** para Lisboa, Porto e Funchal.

As restantes edições usam o mesmo motor e o mesmo número de versão. Ver o
[README do repositório](../README.md).

---

## O que faz

- **Balanço hídrico.** Simulação diária do reservatório com verificação do fecho de massa, descarte da
  primeira água e um ou dois reservatórios (inferior mais superior com bomba).
- **Dimensionamento.** Varrimento de volumes, volume ideal por ganho marginal e sensibilidade à procura e à
  área de captação.
- **Economia.** Tarifários de água, saneamento e energia (incluindo escalões), CAPEX e OPEX, período de
  recuperação, valor atual líquido e taxa interna de rentabilidade, em euros.
- **Ambiente.** Avaliação simplificada do ciclo de vida e balanço de carbono; pontuação em LEED v4/v4.1 (até
  8 pontos em Eficiência Hídrica; o WEc2, uso interno, vale de 1 a 6 pontos para reduções de 25% a 50%, com
  pré-requisito de 20%), EDGE e GRI 303.
- **Decisão.** Ordenação multicritério com TOPSIS e SMAA-VIKOR.
- **Resultados.** Relatório executivo, auditoria ambiental e dossiê técnico em PDF; exportação para folha de
  cálculo, CAD (DXF) e BIM; planta 3D e modelos glTF/HTML da tubagem.

## Instalar e executar

**Instalador para Windows.** Publicado no [Zenodo](../README.md#download), com a soma de verificação SHA-256:
`Triton_PRT_Setup_0_1_0.exe`. Não precisa de Python.

**A partir do código** (Python 3.12 ou superior):

```bash
cd triton_prt
pip install -r requirements.txt
python main.py                      # interface gráfica
python -m triton.cli --help         # linha de comandos
```

Opcional: `pip install -e ".[acelerado]"` instala o `numba`, que acelera estudos em lote (os resultados são
os mesmos).

## Testes

```bash
cd triton_prt
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=PRT python -m pytest tests/unit tests/test_essencial.py
```

No PowerShell do Windows: `$env:TRITON_EDITION = "PRT"; python -m pytest tests/unit tests/test_essencial.py`.
Os testes da interface Qt só são recolhidos com o PySide6 instalado.

## Construir o instalador

```bash
python build_exe.py --installer      # dist/Triton_PRT/ e dist/Triton_PRT_Setup_0_1_0.exe
```

Requer Python 3.12 ou superior, PyInstaller (`requirements-dev.txt`) e o [Inno Setup 6](https://jrsoftware.org/isinfo.php).
O pacote leva a base `data/portugal_eobs.db` (6 MB), que se gera com `scripts/compilar_base_eobs_portugal.py` a
partir dos ficheiros E-OBS e CAOP (cerca de 3 GB, fora do Git; ver o `scripts/README.md`). Para um pacote de teste
sem a base: `--sem-base-climatica`.

## Documentação

- [Manual do utilizador (PDF)](manual/Manual-Triton.pdf)
- [Guia de início](docs/en/getting-started.md), [modelo](docs/en/model.md), [verificação](docs/en/verification.md)
  e [as três edições](docs/en/editions.md) (em inglês)
- [Metodologia](docs/metodologia.md) e [verificação e validação](docs/verificacao_e_validacao.md)
- [Guia da linha de comandos](infos_licenses/CLI_USAGE.md)

## Estrutura do repositório

```text
triton_prt/
├── triton/            Pacote Python: motor de cálculo, interface e linha de comandos
├── tests/             Bateria automática (unitários, integração, invariantes, interface)
├── manual/            O manual pronto: PDF, sítio offline, volumes curtos e casos
├── docs/              Documentação técnica (método, equações, verificação)
├── examples/          Exemplos e modelos de projeto (.triton)
├── data/              Pacotes de idioma, séries de exemplo e a base E-OBS por concelho
├── templates/         Modelos de projeto e de folha de cálculo
├── scripts/           Ferramentas de manutenção (ver scripts/README.md)
├── infos_licenses/    Textos de licença, do instalador e avisos de terceiros
├── pyproject.toml     Metadados do pacote
├── build_exe.py       Construção do executável (PyInstaller) e do instalador (Inno Setup)
└── main.py            Ponto de entrada da aplicação de ambiente de trabalho
```

Fora do controlo de versões, por tamanho ou por serem de terceiros: as fontes brutas E-OBS e CAOP
(`data/portugal/`, ~3 GB), os documentos dos tarifários (`tarifas_portugal/fontes/`) e o banco que os reúne.

## Licença e citação

Código-fonte disponível para fins académicos, com todos os direitos reservados e uso gratuito não comercial.
A citação do programa é obrigatória em qualquer trabalho que use os seus resultados. Os termos completos estão em
[`LICENSE.md`](LICENSE.md); a forma de citar, em [`CITATION.cff`](CITATION.cff):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações.* Universidade Federal de Santa Catarina (UFSC).

Os dados de precipitação são do E-OBS (Cornes et al., 2018, doi:10.1029/2017JD028200): reconhecemos o conjunto
E-OBS do projeto UERRA do 6.º Programa-Quadro da UE (https://www.uerra.eu), o Copernicus Climate Change Service
e os fornecedores de dados do projeto ECA&D (https://www.ecad.eu). Os limites dos concelhos são da CAOP 2025, da
Direção-Geral do Território.

Desenvolvido pelo Grupo de Pesquisa em Ambientes Sustentáveis (GPAS), Universidade Federal de Santa Catarina.
Dúvidas e erros: igor.catao@posgrad.ufsc.br.
