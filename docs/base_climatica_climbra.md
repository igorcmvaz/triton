# Base de dados CLIMBra (CMIP6) no Netuno 5

Este documento descreve a procedência científica, a estrutura de dados, o processo de compilação em alta densidade e a integração do conjunto de dados **CLIMBra** (*Climate Change Dataset for Brazil*) no **Netuno 5**.

---

## 1. Procedência e Fundamentação Científica

A base de dados CLIMBra incorporada ao Netuno 5 é oriunda do esforço de pesquisa de Ballarin et al. (2023), publicado no periódico *Nature Scientific Data*, fornecendo projeções climáticas em grade diária de alta resolução para todo o território brasileiro.

- **Artigo de Referência:**  
  BALLARIN, A. S.; SONE, J. S.; GESUALDO, G. C.; SCHWAMBACK, D.; REIS, A.; ALMAGRO, A.; WENDLAND, E. C. *CLIMBra - Climate Change Dataset for Brazil*. **Scientific Data**, v. 10, n. 1, art. 47, 2023.  
  DOI: [10.1038/s41597-023-01956-z](https://doi.org/10.1038/s41597-023-01956-z)
- **Repositório de Dados Abertos:**  
  *Science Data Bank*, licença pública mundial CC0 1.0 Universal (Domínio Público).  
  DOI: [10.57760/sciencedb.02316](https://doi.org/10.57760/sciencedb.02316)
- **Base Observacional de Calibração:**  
  Série em grade diária de Xavier, King e Scanlon (2016), derivada de interpolação geoestatística de estações meteorológicas do INMET, ANA e DAEE.

### Metodologia de Correção de Viés (QDM)
Os dados brutos dos Modelos de Circulação Global (GCMs/ESMs) do CMIP6 apresentam desvios sistemáticos de precipitação em escala regional. No CLIMBra, todas as variáveis diárias foram corrigidas estatisticamente pelo algoritmo **Quantile Delta Mapping (QDM)** em grade regular de **0,25° × 0,25°** (~28 km). O QDM preserva as variações temporais relativas de extremos projetados pelo CMIP6 enquanto corrige com rigor as probabilidades de dias secos e chuvas torrenciais em relação ao histórico observado.

---

## 2. Escopo Geográfico e Modelos CMIP6

O Netuno 5 disponibiliza séries contínuas para **652 municípios brasileiros** (todas as 27 capitais, regiões metropolitanas e polos urbanos de todas as unidades da federação).

### 19 Modelos Climáticos Globais (GCMs/ESMs) Disponíveis
1. `INM-CM4` (Modelo padrão de referência no Netuno 5)
2. `ACCESS-CM2`
3. `ACCESS-ESM1-5`
4. `CMCC-ESM2`
5. `EC-EARTH3`
6. `GFDL-CM4`
7. `GFDL-ESM4`
8. `HadGEM3-GC31-LL`
9. `INM-CM5`
10. `IPSL-CM6A-LR`
11. `KACE`
12. `KIOST`
13. `MIROC6`
14. `MPI-ESM1-2`
15. `MRI-ESM2`
16. `NESM3`
17. `NorESM2-MM`
18. `TaiESM1`
19. `UKESM1-0-LL`

### Cenários de Emissões e Horizontes Temporais
Para cada município e modelo, existem três séries temporais diárias completas e ininterruptas:

| Cenário | Descrição | Período Contínuo | Total de Dias |
| :--- | :--- | :--- | :--- |
| **Histórico** (`HIST`) | Baseline histórico simulado pelo modelo | 01/01/1980 a 31/12/2013 | 12.419 dias (34 anos) |
| **SSP2-4.5** (`SSP245`) | Trajetória intermediária de mitigação moderada | 01/01/2015 a 31/12/2100 | 31.411 dias (86 anos) |
| **SSP5-8.5** (`SSP585`) | Trajetória extrema de intensificação fóssil | 01/01/2015 a 31/12/2100 | 31.411 dias (86 anos) |

*Nota:* O Netuno 5 permite recortes arbitrários por data, oferecendo botões rápidos para as normais climatológicas sugeridas (30 anos):
- **Série Completa** (1980–2013 ou 2015–2100)
- **Futuro Próximo** (2021–2050)
- **Meados do Século** (2041–2070)
- **Fim do Século** (2071–2100)

---

## 3. Otimização e Armazenamento em Alta Densidade (`climbra.db`)

Originalmente, a base de 652 cidades é composta por **37.164 arquivos CSV individuais** que ocupam **6,24 GB** no disco. A leitura em CSV consome dezenas de milissegundos por série e torna o empacotamento em um único instalador inviável ou proibitivamente lento.

Para solucionar isso, o Netuno 5 implementou uma infraestrutura de **banco de dados SQLite compactado** (`data/climbra.db`).

### Esquema Relacional do Banco SQLite
```sql
-- Metadados de versão, compilação e licença
CREATE TABLE climbra_meta (
    key TEXT PRIMARY KEY,
    value TEXT
);

-- Catálogo de municípios para busca instantânea e tolerância a acentos
CREATE TABLE climbra_cities (
    city TEXT PRIMARY KEY,
    city_norm TEXT NOT NULL
);
CREATE INDEX idx_climbra_cities_norm ON climbra_cities(city_norm);

-- Séries de precipitação compactadas em binário
CREATE TABLE climbra_series (
    city TEXT NOT NULL,
    model TEXT NOT NULL,
    scenario TEXT NOT NULL,
    count INTEGER NOT NULL,
    data BLOB NOT NULL,
    PRIMARY KEY (city, model, scenario)
);
```

### Compressão e Fidelidade Numérica
- **Tipo de dado:** `np.float16` (2 bytes por dia de simulação).
- **Compressão de fluxo:** `zlib` com nível de compressão 6.
- **Tamanho resultante:** O banco completo ocupa apenas **~1,1 GB** (redução de **82,4%** no espaço em disco).
- **Precisão hidrológica:** A diferença na conservação de massa e no potencial de economia de água potável no motor de simulação diária entre `float64` e `float16` é de apenas **0,000045%** (45 partes por bilhão), uma grandeza infinitamente inferior à incerteza instrumental dos pluviômetros físicos (geralmente ±2% a ±5%).
- **Tempo de carregamento:** A descompressão direta de memória leva **~0,3 ms** por série (mais de **30× mais rápido** que o parsing textual de linhas em CSV).

---

## 4. Prioridade de Resolução de Arquivos

O módulo [`netuno/core/climate_database.py`](../netuno/core/climate_database.py) resolve a origem dos dados na seguinte ordem de precedência:

1. **Variável de Ambiente:** `NETUNO_CLIMBRA_DB` ou `NETUNO_CLIMATE_DATA_DIR`
2. **Banco SQLite Compilado:**
   - `<pasta_do_executavel>/data/climbra.db` (em instalações via instalador / PyInstaller)
   - `<raiz_do_projeto>/data/climbra.db` (em ambiente de desenvolvimento)
3. **Fallback para CSVs soltos:**
   - `<raiz_do_projeto>/Netuno future files for 652 cities/`

Se o banco `climbra.db` estiver presente, o Netuno carrega tudo a partir dele instantaneamente. Caso contrário, ele recorre com total retrocompatibilidade aos arquivos CSV individuais.

---

## 5. Como Regerar ou Recompilar o Banco

O script [`scripts/compilar_base_climbra.py`](../scripts/compilar_base_climbra.py) automatiza 100% da compilação:

```bash
# Compilação padrão multiprocessada com float16 (recomendado: ~1,1 GB)
python scripts/compilar_base_climbra.py

# Compilação com float32 (se for desejada precisão IEEE-754 simples: ~1,8 GB)
python scripts/compilar_base_climbra.py --dtype float32

# Apenas verificar a integridade e precisão de um banco já gerado
python scripts/compilar_base_climbra.py --verify-only
```
