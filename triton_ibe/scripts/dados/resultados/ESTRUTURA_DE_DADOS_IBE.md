# Estrutura de dados de chuva para a Península Ibérica (proposta)

Escopo: Portugal e Espanha (edição PRT hoje; poderá chamar-se Triton IBE). Decisões já tomadas: E-OBS como série base; correção de escala opcional e desligada por defeito (q16); ilhas só com estação (q17); falhas: abaixo de 1 % preenche, acima exclui (q12); sem aviso de tendência no programa, só no manual (q18).

## Princípios
1. **Guardar a célula, não o concelho.** A série de um concelho ou município é a média ponderada das células da grade. Guardar a célula uma vez evita repetir os mesmos 27 759 valores (hoje 7 concelhos repetem a série de outro) e permite consultar qualquer ponto por latitude e longitude, mesmo sem polígono administrativo.
2. **Dado bruto e correção separados.** A série da E-OBS nunca é alterada. A correção de escala é um conjunto de parâmetros por unidade, aplicada por quem a ligar. Tudo fica rastreável.
3. **Toda a série tem procedência.** Fonte, versão, licença, citação, data de obtenção e SHA-256 numa tabela só, ligada a cada célula e a cada estação.
4. **Qualidade é dado.** O que a validação mediu (diferença para o Iberia01, correlação, extremos, estações vizinhas) vai para uma tabela e o programa lê dela para avisar o utilizador, em vez de o manual dizer uma coisa e o programa outra.
5. **Pacotes por região.** O instalador leva Portugal; Espanha vem em pacotes (decisão anterior: pacotes pré-extraídos pelos mantenedores).

## Tamanho (medido com a E-OBS real, 40 células sorteadas, 1950–2025, 27 759 dias)
| Codificação | KB por célula | Península (6 988 células) |
|---|---|---|
| float32 + zlib (como hoje) | 15,2 | 109 MB |
| uint16 em 0,1 mm + zlib | 11,6 | 83 MB |
| uint16 em planos de byte + zlib | 9,8 | 70 MB |
Portugal continental sozinho (cerca de 900 células E-OBS): cerca de 9 MB.

## Esquema (SQLite)
```sql
-- procedência de cada conjunto de dados
CREATE TABLE fonte (
  id TEXT PRIMARY KEY,            -- 'eobs_v33', 'iberia01_v1', 'ghcnd', 'ecad', 'ipma_mensal'
  tipo TEXT,                      -- 'grade' | 'estacao'
  nome TEXT, versao TEXT, resolucao_graus REAL, inicio TEXT, fim TEXT,
  convencao_dia TEXT,             -- E-OBS: 06–06 UTC; estações: 09 UTC (registar)
  licenca TEXT, citacao TEXT, url TEXT, obtido_em TEXT, sha256 TEXT, redistribuivel INTEGER
);

-- células da grade (E-OBS 0,1°) e estações num mesmo cadastro de pontos
CREATE TABLE ponto (
  id INTEGER PRIMARY KEY, fonte_id TEXT REFERENCES fonte(id),
  tipo TEXT,                      -- 'celula' | 'estacao'
  lat REAL, lon REAL, altitude_m REAL, codigo_externo TEXT, nome TEXT, pais TEXT   -- 'PT' | 'ES'
);

-- séries diárias em blocos de 10 anos, para acrescentar anos novos sem reescrever
CREATE TABLE serie_bloco (
  ponto_id INTEGER REFERENCES ponto(id), ano_ini INTEGER, dias INTEGER,
  dados BLOB,                     -- uint16 em 0,1 mm, 65535 = sem dado, planos de byte + zlib
  marcas BLOB,                    -- bits por dia: 0 medido, 1 preenchido, 2 estimado (só estações)
  PRIMARY KEY (ponto_id, ano_ini)
);

-- unidades administrativas: concelho (PT, código DTMN), município (ES, código INE), e as suas agregações
CREATE TABLE unidade (
  id TEXT PRIMARY KEY,            -- 'PT-0101', 'ES-28079'
  nome TEXT, pais TEXT, nivel TEXT,    -- 'concelho' | 'municipio'
  distrito_ou_provincia TEXT, regiao TEXT, lat_ref REAL, lon_ref REAL, area_km2 REAL
);
-- a série da unidade = soma dos pesos x séries das células
CREATE TABLE unidade_ponto (
  unidade_id TEXT REFERENCES unidade(id), ponto_id INTEGER REFERENCES ponto(id),
  peso REAL, metodo TEXT          -- 'dentro' | 'centroide'
);

-- o que a validação mediu, por unidade
CREATE TABLE qualidade (
  unidade_id TEXT REFERENCES unidade(id), fonte_id TEXT,
  n_celulas INTEGER, celulas_partilhadas_com TEXT,       -- ex.: Lisboa e Odivelas
  estacao_ponto_id INTEGER, dist_estacao_km REAL, estacao_independente INTEGER,
  pbias_pct REAL, r_diario REAL, kge_mensal REAL, dias1mm_dif_pct REAL, dp95_pct REAL, drx1_pct REAL,
  ref_iberia01_dtot_pct REAL,                            -- diferença contra a rede densa na célula
  nivel TEXT, aviso TEXT                                  -- 'A' | 'B' | 'C' e o texto do aviso
);

-- correção de escala opcional (desligada por defeito)
CREATE TABLE correcao (
  unidade_id TEXT REFERENCES unidade(id), mes INTEGER,   -- 1 a 12
  fator_total REAL,                                       -- multiplica a chuva do mês
  fator_extremos REAL, limiar_mm REAL,                    -- ajuste para dias acima do limiar
  referencia TEXT, periodo_calibracao TEXT, n_estacoes INTEGER, incerteza REAL
);

CREATE TABLE nao_coberto (unidade_id TEXT, motivo TEXT);
CREATE TABLE metadados (chave TEXT PRIMARY KEY, valor TEXT);
```

## Níveis de qualidade por unidade (para o aviso no programa)
Fórmula única (implementada em `triton/core/qualidade_chuva.py`; o banco, o programa e o manual leem os mesmos `LIMIARES`), decidida no debate de 23/10/2026. `dtot` e `drx` são a **diferença para o Iberia01** (E-OBS menos Iberia01, 1971-2000) no total anual e no máximo diário anual; não são viés contra a verdade.
- **Concordância**: A se |dtot| <= 10 % e |drx| <= 15 %; B se |dtot| <= 20 % e |drx| <= 25 %; C nos demais casos.
- **Geometria**: B se `n_eff` < 3, ou método «centroide», ou série repetida de outro concelho; A nos demais. A geometria só rebaixa até B.
- **Nível** = o pior das duas. Resultado no protótipo: A 45, B 159, C 74.
No banco do programa a tabela é `qualidade(dtmn, concelho, n_eff, metodo, repetida, dtot, drx, nivel, motivo)`; os `metadados` levam `pacote_id`, `versao_eobs`, `sha256_pacote`, `qualidade_versao`, `limiares` e `espanha_locais`.

## Ilhas
Madeira e Açores não entram pela grade. Cada ilha com estação (Funchal, Porto Santo, Horta, Flores, Ponta Delgada, Santa Maria, Lajes) entra como `ponto` do tipo estação, com `marcas` para dias em falta, regra de 1 % e `fonte` própria (GHCN-Daily). O aviso diz que é uma estação, não uma média de concelho.

## Fluxo de construção (mantenedores)
1. Extrair a E-OBS da região, 1950 até ao último ano completo, e gravar `serie_bloco`.
2. Cadastrar unidades (CAOP para Portugal; para a Espanha, o limite municipal oficial, licença por confirmar) e pesos por área ou por centro da célula.
3. Rodar a validação (estações GHCN-Daily, ECA&D, Iberia01) e gravar `qualidade` e `correcao`.
4. Gerar o pacote, registar SHA-256 e versão, e correr os testes (integridade, 0 NaN, referências cruzadas, tamanhos).
Atualização anual: acrescentar um bloco (ano novo) e refazer `qualidade` se a fonte mudou.

## Pontos em aberto
- **Licença do Iberia01** (ODbL pelo artigo): o que fazer com os fatores de correção derivados dele, que seriam distribuídos no programa. Ler o texto da licença e, se preciso, perguntar aos autores.
- **Licença da E-OBS** para redistribuir a série derivada: perguntar ao KNMI (`eca@knmi.nl`). Afeta o que já se distribui na edição PRT.
- **Limites municipais da Espanha**: fonte oficial (CNIG) e licença por confirmar.
- **IB02/PT02**: não obtido. Só serviria para 1950–1970, e o Iberia01 já o substitui de 1971 em diante.
- Critério de aceitação por indicador (níveis A, B, C).
