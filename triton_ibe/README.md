# Triton IBE — Edição Ibérica

[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)](https://www.python.org/)
[![GUI](https://img.shields.io/badge/GUI-PySide6%20(Qt6)-green)](https://www.qt.io/)
[![Licença: código-fonte disponível para fins académicos](https://img.shields.io/badge/licen%C3%A7a-fins%20acad%C3%A9micos-lightgrey.svg)](LICENSE.md)
[![Grupo de investigação](https://img.shields.io/badge/UFSC-Ambientes%20Sustent%C3%A1veis-005a36)](https://sustainability.ufsc.br/)

O **Triton** dimensiona sistemas de aproveitamento de água da chuva em edifícios. Simula o balanço hídrico
diário sobre uma série de precipitação, varre uma gama de volumes de reservatório e indica o que cada volume
rende em água poupada, em dinheiro, em carbono do ciclo de vida e em peso do sistema; depois ordena as
alternativas por decisão multicritério (TOPSIS e SMAA-VIKOR), com oito critérios em quatro eixos.

Esta é a **Edição Ibérica** (**Triton IBE**, Península Ibérica; chamou-se Edição Portugal, PRT). Abre em português de Portugal, trabalha em euros e traz a chuva de toda a Península (Portugal 308 locais; Espanha 8 131 locais; as ilhas com ERA5, nível C). Os projetos e os scripts que ainda dizem `PRT` ou `POR` continuam a funcionar: abrem como IBE.

- **Precipitação do Iberia01 por município**, 1971 a 2015 (Iberia01 v1.0, grelha de 0,1°, ODbL; limites CAOP 2025 e
  Eurostat/GISCO LAU 2023), período padrão 1986–2015: Portugal continental, Espanha peninsular e Baleares (8 319
  municípios, chave por código INE ou DTMN). Canárias, Madeira e Açores (118 locais) usam a reanálise ERA5, sempre
  com nível C; Ceuta e Melilla ficam sem série. A E-OBS (1950–2025, só uso não comercial) é uma fonte opcional.
- **Tarifários de água e saneamento** de Lisboa, Porto e Funchal, com a entidade gestora, a vigência e a fonte
  de cada valor. Em Espanha, 7 municípios com tarifário transcrito (ainda não conferido) e a média regional do INE
  para os restantes, só indicativa.
- **Exemplos completos** para Lisboa, Porto, Funchal, Madrid e Palma.

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
- **Decisão.** Ordenação multicritério com TOPSIS, VIKOR, SMAA-VIKOR e PROMETHEE II, sobre oito critérios em
  quatro eixos: técnico (fiabilidade volumétrica e eficiência de armazenamento), económico (economia financeira
  líquida, custo nivelado da água e período de recuperação descontado), ambiental (CO₂e de ciclo de vida) e
  estrutural (massa a seco dos materiais e extravasamento anual). Quatro pesos de eixo, 25% cada por omissão,
  repartidos pelas partes no eixo; ou oito pesos de critério.
- **Peso do sistema.** Massa a seco, carga de água e carga em operação, em kg e kN, no subsolo, na cobertura e
  nas prumadas e rede, com alertas quando a carga passa um limiar de atenção do programa (não de norma).
- **Resultados.** Relatório executivo, auditoria ambiental e dossiê técnico em PDF; exportação para folha de
  cálculo, CAD (DXF) e BIM; planta 3D e modelos glTF/HTML da tubagem.

## Estado da versão 0.2.0

**Pronto.** O balanço diário, o varrimento de volumes, a economia (escalões, VAL, TIR, período de recuperação),
a avaliação do ciclo de vida, a linha de tratamento, as certificações, a decisão multicritério de oito critérios, o peso do sistema, a modulação
probabilística, os laudos (PDF), a folha de cálculo, as exportações DXF/glTF/BIM, o manual completo e a
documentação de cada conjunto de dados. A chuva de cada município tem nível de
qualidade A, B ou C (A 461, B 7 857, C 119; as ilhas são C); Lisboa, Porto e Funchal têm tarifário transcrito e exemplo completo.

**Cobertura e o que falta.**

| Área | Estado na versão 0.2.0 |
| :--- | :--- |
| Chuva, Portugal continental | pronta: 278 concelhos (Iberia01), nível A (140) ou B (138) |
| Chuva, Espanha e Baleares | pronta: 8 041 municípios (Iberia01), nível A (321), B (7 719) ou C (1) |
| Chuva, ilhas | Canárias, Madeira e Açores: 118 locais pela ERA5, nível C; Ceuta e Melilla sem série |
| Tarifários, Portugal | Lisboa, Porto e Funchal transcritos; nenhum concelho em verde |
| Tarifas, Espanha | 7 municípios com tarifário transcrito, ainda não conferido (Madrid, Sevilla, Murcia, A Coruña, Las Palmas de Gran Canaria, Gijón e Valladolid); os outros 8 124 usam a média regional do INE (indicativa) |
| Preços e CAPEX | partem de zero e são do utilizador; o programa não traz preços de Portugal |
| Fator de emissão da rede | sem valor até o utilizador o indicar |
| Correção de escala da chuva | não faz parte desta versão |

**Limitações conhecidas.** A licença da E-OBS é de uso não comercial em investigação e educação e omissa quanto à
redistribuição; o diálogo do CAPEX não tem campo para o preço da cisterna (o manual dá o contorno); o espanhol e o
chinês estão traduzidos em parte. A lista completa está nas notas de lançamento da
[0.2.0](docs/NOTAS_DE_LANCAMENTO_0.2.0.md) e da [0.1.0](docs/NOTAS_DE_LANCAMENTO_0.1.0.md) e no
[histórico de versões](CHANGELOG.md).

**O que muda na 0.2.0.** O multicritério passa de sete critérios em três eixos a oito critérios em quatro eixos,
e o volume que ele escolhe pode mudar: no tutorial de Lisboa, com pesos iguais, o TOPSIS passa de 5 000 L para
3 000 L. Projetos e estudos com três pesos de eixo continuam a abrir (o eixo estrutural recebe a média dos três);
sete pesos ou sete partes são recusados. Para reproduzir um estudo feito com a 0.1.0, use a 0.1.0.

## Instalar e executar

**Instalador para Windows.** Os registos do Zenodo estão reunidos no DOI de todas as versões,
[10.5281/zenodo.23402915](https://doi.org/10.5281/zenodo.23402915), que aponta sempre para a mais recente. O da 0.1.0
(`Triton_Iberica_Setup_v0.1.0.exe`, com a soma de verificação SHA-256 em `SHA256SUMS.txt`; sem assinatura digital) está
no registo da 0.1.0, DOI [10.5281/zenodo.23402916](https://doi.org/10.5281/zenodo.23402916); a 0.2.0 ainda não tem
registo próprio. Não precisa de Python.

**A partir do código** (Python 3.12 ou superior):

```bash
cd triton_ibe
pip install -r requirements.txt
python main.py                      # interface gráfica
python -m triton.cli --help         # linha de comandos
```

**Abrir um exemplo.** Com o programa aberto, use **Ficheiro > Abrir** e escolha `examples/portugal/lisboa.triton` (ou `porto.triton`, `funchal.triton`).
O manual (`manual/Manual-Triton.pdf`) explica as 13 etapas a partir daí.

Opcional: `pip install -e ".[acelerado]"` instala o `numba`, que acelera estudos em lote (os resultados são
os mesmos).

## Testes

```bash
cd triton_ibe
pip install -r requirements.txt -r requirements-dev.txt
TRITON_EDITION=IBE python -m pytest tests/unit tests/test_essencial.py
```

No PowerShell do Windows: `$env:TRITON_EDITION = "IBE"; python -m pytest tests/unit tests/test_essencial.py`.
Os testes da interface Qt só são recolhidos com o PySide6 instalado.

## Instalador

O instalador não faz parte deste repositório: sai no registo do Zenodo de cada versão (DOI de todas as versões [10.5281/zenodo.23402915](https://doi.org/10.5281/zenodo.23402915)). A base `data/portugal_eobs.db` (6 MB) gera-se com `scripts/dados/compilar_base_eobs_portugal.py` a partir dos ficheiros E-OBS e CAOP (cerca de 3 GB, fora do Git; ver `scripts/dados/LEIA.md`).

## Documentação

- [Manual do utilizador (PDF)](manual/Manual-Triton.pdf)
- Notas de lançamento da [0.2.0](docs/NOTAS_DE_LANCAMENTO_0.2.0.md) e da [0.1.0](docs/NOTAS_DE_LANCAMENTO_0.1.0.md), e [histórico de versões](CHANGELOG.md)
- [Guia de início](docs/en/getting-started.md), [modelo](docs/en/model.md), [verificação](docs/en/verification.md)
  e [as três edições](docs/en/editions.md) (em inglês)
- [Dados da edição: fontes, licenças, cobertura e qualidade](docs/DADOS.md)
- [Metodologia](docs/metodologia.md) e [verificação e validação](docs/verificacao_e_validacao.md)
- [Guia da linha de comandos](infos_licenses/CLI_USAGE.md)

## Estrutura do repositório

```text
triton_ibe/
├── triton/            Pacote Python: motor de cálculo, interface e linha de comandos
├── tests/             Bateria automática (unitários, integração, invariantes, interface)
├── manual/            O manual pronto: PDF, sítio offline, volumes curtos e casos
├── docs/              Documentação técnica (método, equações, verificação)
├── examples/          Exemplos e modelos de projeto (.triton)
├── data/              Chuva do Iberia01 (4 partes) e da ERA5 das ilhas, municípios e níveis, E-OBS opcional, idiomas
├── templates/         Modelos de projeto e de folha de cálculo
├── scripts/           Ferramentas de manutenção (ver scripts/README.md)
├── infos_licenses/    Textos de licença, do instalador e avisos de terceiros
├── pyproject.toml     Metadados do pacote
└── main.py            Ponto de entrada da aplicação de ambiente de trabalho
```

Fora do controlo de versões, por tamanho ou por serem de terceiros: as fontes brutas E-OBS e CAOP
(`data/portugal/`, ~3 GB), os documentos dos tarifários (`tarifas_portugal/fontes/`) e o banco que os reúne.

## Licença e citação

Código-fonte disponível para fins académicos, com todos os direitos reservados e uso gratuito não comercial.
A citação do programa é obrigatória em qualquer trabalho que use os seus resultados. Os termos completos estão em
[`LICENSE.md`](LICENSE.md); a forma de citar, em [`CITATION.cff`](CITATION.cff):

> Vaz, I. C. M., & Ghisi, E. (2026). *Triton: Plataforma Computacional para Simulação de Aproveitamento de Água de Chuva em Edificações* (versão 0.2.0). Universidade Federal de Santa Catarina (UFSC). https://doi.org/10.5281/zenodo.23402915

O DOI 10.5281/zenodo.23402915 reúne todas as versões e aponta sempre para a mais recente; a 0.2.0 ainda não tem DOI
próprio. A 0.1.0 tem o DOI 10.5281/zenodo.23402916.

A chuva da Península e das Baleares vem do Iberia01 v1.0 (Herrera et al., 2019, doi:10.5194/essd-11-1947-2019):
*Contains information from Iberia01, made available under the Open Database License (ODbL 1.0).* A chuva das
Canárias, da Madeira e dos Açores vem da reanálise ERA5 (Hersbach et al., 2020, doi:10.1002/qj.3803; dados
Open-Meteo.com, CC BY 4.0): *Contains modified Copernicus Climate Change Service information.* A E-OBS, opcional e
só para uso não comercial, pede a citação de Cornes et al. (2018, doi:10.1029/2017JD028200) e o reconhecimento do
projeto UERRA (https://www.uerra.eu), do Copernicus Climate Change Service e dos fornecedores de dados do ECA&D
(https://www.ecad.eu). Os limites são da CAOP 2025 (Direção-Geral do Território) e do Eurostat/GISCO LAU 2023
(© EuroGeographics). As atribuições completas estão em [`data/LICENCA_DOS_DADOS.md`](data/LICENCA_DOS_DADOS.md) e
em [`docs/DADOS.md`](docs/DADOS.md).

Desenvolvido pelo Grupo de Pesquisa em Ambientes Sustentáveis, Universidade Federal de Santa Catarina.
Dúvidas e erros: igorcmvaz@gmail.com.
