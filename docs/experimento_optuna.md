# Experimento: busca em grade do Triton x busca bayesiana do optuna

Experimento de desenvolvimento, opcional e fora do programa. Etapa 7 do plano das iniciativas
(`auditoria/iniciativas/AVALIACAO.md`). Nada daqui entra no instalador, em `requirements.txt`, em `Triton.spec`, em
`build_exe.py` ou no `estudo run`, que promete arquivos de resultado byte a byte iguais. O pacote `optuna` vem só do extra
`otimizacao` e é importado por `triton.core._opcional`; sem ele o script sai com a mensagem de instalação.

## Pergunta

Para o mesmo problema, quantas simulações a busca bayesiana (TPE, e NSGA-II no caso de dois objetivos) precisa para chegar ao
ótimo que a grade do Triton encontra por varredura completa? Quanto custa em tempo? Que diferença sobra no VPL e no volume? E o
ponto escolhido pelo optuna se confirma no motor determinístico?

## Método

Script: `scripts/experimento_optuna.py` (raiz do monorepo; `--help` lista as opções). Reprodução, da raiz, com o extra instalado
(`pip install "triton-int[otimizacao]"` ou, num ambiente descartável, `pip install optuna`):

```
python scripts/experimento_optuna.py --edicao brl --json auditoria/iniciativas/resultados/brl.json
python scripts/experimento_optuna.py --edicao ibe
python scripts/experimento_optuna.py --edicao int --experimento 1d --experimento 2d
```

**Problema por edição** (o mesmo projeto vai para a grade e para o optuna):

| Edição | Projeto | Clima |
| :-- | :-- | :-- |
| Brasil | `triton_brl/estudos/santa-catarina/comercial/comercial.triton` (arquétipo comercial, 1 200 m² de captação, 300 usuários, 45 L/dia por usuário, fração pluvial 50 %) | Florianópolis, CLIMBra, modelo INM-CM4, histórico 1981-2010 (10 957 dias) |
| Ibérica | `triton_ibe/examples/portugal/lisboa.triton` (150 m², 4 moradores) | Lisboa, 10 957 dias |
| Internacional | `triton_int/examples/london.triton` (150 m², 4 moradores) | Londres, 10 958 dias |

Os exemplos de Lisboa e de Londres não trazem custos de implantação (capex zero): neles o VPL só cresce com o volume e com a
área, e o ótimo é a borda da grade ou um patamar. Só o arquétipo de Santa Catarina tem custos (estimativas de arquétipo, ver o
`LEIA.md` do estudo) e, por isso, é o resultado principal. Os custos do arquétipo são os do projeto, sem alteração.

**Experimentos** (objetivo: maximizar o VPL, salvo o último):

| Código | Espaço de busca | Pontos da grade (Brasil) |
| :-- | :-- | --: |
| `1d` | volume do reservatório inferior na grade do projeto (a do `estudo run`: máximo 80 m³, passo pedido 1,5 m³, passo efetivo 3 m³) | 28 (incluindo 0 L) |
| `1da` | o mesmo, ampliado 5 vezes (máximo 400 m³, 40 volumes, o limite da varredura do Triton), onde o ótimo sai da borda | 41 |
| `2d` | volume (grade ampliada) x área de captação (29 valores, de 0,25 a 2 vezes a área do projeto) | 1 189 |
| `nsga` | pares (água pluvial aproveitada a maximizar, custo de implantação a minimizar) na grade do `2d`, com NSGA-II; sem custo no projeto, o custo é o volume do reservatório | 1 189 |

**A grade é a verdade.** É a varredura oficial do Triton (`cli.run_analysis`, tipo `economic`, que usa `run_sweep_simulation` e a
linha econômica `_economic_row` com preço da cisterna por volume), uma por valor de área. O optuna busca índices inteiros da mesma
grade (`suggest_int`), de modo que «o ótimo exato» é um ponto da grade e a comparação é direta. Cada tentativa do optuna chama
`_run_technical` (`run_single_simulation`) e `_economic_row`; pontos repetidos não são resimulados (conta-se a simulação distinta).

**Medidas.**

- Tentativas e simulações distintas até o primeiro ponto com VPL igual ao ótimo da grade (tolerância relativa de 1e-6) e até
  um VPL a 1 % do ótimo («mesma classe de resultado»). Mediana e pior caso das 5 sementes; «não chegou» quando a semente não alcança
  o ponto dentro do orçamento (60 tentativas em `1d` e `1da`, 300 em `2d`, 400 em `nsga`).
- Custo em «grades»: tempo do método dividido pelo tempo da grade inteira medido na mesma condição da máquina (1,00 = tanto
  quanto a grade). Ver «Sobre os tempos».
- Diferença final de VPL (%) e de volume (L) do melhor ponto do optuna em relação ao ótimo da grade (pior das 5 sementes).
- No `nsga`: fração da frente de Pareto da grade encontrada e razão de hipervolume (normalizado, referência água 0 e custo máximo).
- Referência: busca aleatória (`RandomSampler`) com as mesmas sementes e orçamentos. É o teste de sanidade: o TPE só vale se
  ganhar dela.

**Reavaliação no motor determinístico.** O melhor ponto de cada semente é reavaliado por outro caminho: cópia nova do projeto
(`_load_bundle`) e varredura oficial da área do ponto, lendo a linha do volume. A diferença entre o VPL da tentativa e o da
reavaliação é a coluna «Diferença na reavaliação» (no `nsga`, a diferença de água aproveitada em até 3 pontos da frente de cada
semente).

**Reprodutibilidade.** `TPESampler(seed=s)`, `RandomSampler(seed=s)`, `NSGAIISampler(seed=s, population_size=30)`, `n_jobs=1`,
armazenamento em memória (sem SQLite), sementes 42 a 46. Cada estudo roda 5 vezes e as trajetórias (sequência de pontos
sugeridos) precisam sair idênticas, senão o script aborta: elas saíram idênticas em todas as execuções. Duas execuções completas
do experimento do Brasil (a primeira com outro controle de tempo) deram as mesmas contagens.

**Ambiente da medição** (02/11/2026, uma execução de cada edição):

| Item | Valor |
| :-- | :-- |
| Máquina | Windows 11 Home 10.0.26200, Intel Core i7-13650HX (20 processadores lógicos), 23,7 GB de memória |
| Python / numpy / numba | 3.13.1 / 2.4.6 / 0.67.0 (numba ativo no motor) |
| optuna | 5.0.0, num venv descartável (`auditoria/iniciativas/venv_tmp`, ignorado pelo Git, com `--system-site-packages`); o Python do sistema e o `requirements.txt` ficaram intactos |
| Triton | 0.1.0, ramo `feature/ibe-qualidade`, base `d69a81b` |
| Sementes | 42, 43, 44, 45, 46 |

## Resultados medidos: arquétipo comercial de Santa Catarina (Brasil)

Ótimos da grade: `1d`, VPL R$ 563 836 no volume de 80 000 L (a borda: o VPL ainda cresce nessa grade); `1da`, VPL R$ 564 403 em
90 000 L (ótimo interior); `2d`, VPL R$ 924 023 em 190 000 L e 2 400 m² (volume interior, área na borda: a área não tem custo no
modelo). Células: mediana (pior caso entre as 5 sementes).

| Experimento | Método | Tentativas até o ótimo exato | Simulações distintas | Custo até o ótimo (grades) | Tentativas até 1 % | Pior dif. de VPL (%) | Pior dif. de volume (L) | Dif. na reavaliação |
| :-- | :-- | --: | --: | --: | --: | --: | --: | --: |
| `1d` (28 pontos) | TPE | 11 (11) | 9 (10) | 0,54 (0,57) | 2 (6) | 0 | 0 | 0 |
| `1d` | aleatória | 22 (36) | 17 (20) | 0,80 (0,98) | 2 (6) | 0 | 0 | 0 |
| `1da` (41 pontos) | TPE | 22 (33) | 16 (22) | 0,91 (1,39) | 4 (16) | 0 | 0 | 0 |
| `1da` | aleatória | 23 (não chegou em 2 de 5) | 15 (idem) | 0,48 (idem) | 4 (15) | 0,1003 | 10 000 | 0 |
| `2d` (1 189 pontos) | TPE | 60 (92) | 54 (76) | 0,16 (0,26) | 13 (14) | 0 | 0 | 0 |
| `2d` | aleatória | não chegou (0 de 5 em 300) | - | - | 70 (192) | 0,0766 | 30 000 | 0 |

Custo do orçamento inteiro (todas as tentativas, em grades): `1d` TPE 3,51 e aleatória 1,26; `1da` 2,64 e 1,07; `2d` 0,80 e 0,31.
Isto é, num problema de 28 pontos o TPE gastou o equivalente a 3,5 grades para 60 tentativas.

`nsga` (grade de 1 189 pontos, frente de Pareto com 146 pontos; hipervolume e frente: mediana; pior caso):

| Tentativas | NSGA-II: razão de hipervolume | NSGA-II: frente achada | Aleatória: razão de hipervolume | Aleatória: frente achada |
| --: | :-- | :-- | :-- | :-- |
| 60 | 0,9482; 0,8890 | 6 %; 3 % | 0,9536; 0,9308 | 7 %; 5 % |
| 120 | 0,9699; 0,9545 | 14 %; 8 % | 0,9692; 0,9547 | 12 %; 9 % |
| 240 | 0,9855; 0,9777 | 29 %; 21 % | 0,9834; 0,9794 | 22 %; 19 % |
| 400 | 0,9948; 0,9914 | 45 %; 40 % | 0,9887; 0,9839 | 32 %; 32 % |

Simulações distintas em 400 tentativas: NSGA-II 273, aleatória 343 (medianas). Custo do orçamento de 400 tentativas: 0,42 grade
(NSGA-II) e 0,40 (aleatória). Diferença na reavaliação: 0 m³/ano.

## Resultados medidos: exemplos de Lisboa (Ibérica) e de Londres (Internacional)

Sem custos de implantação, o VPL é uma função crescente (ou de patamar) do volume e da área; o ótimo é a borda ou um patamar, e
«atingir o ótimo exato» vira, muitas vezes, acertar um ponto de um patamar (por isso aparecem 1 tentativa e diferenças de volume
de dezenas de milhares de litros com diferença de VPL nula). Estes números mostram o comportamento do método num problema fácil,
não uma otimização econômica.

| Edição | Experimento | Pontos | Método | Tentativas até o ótimo exato | Simulações distintas | Pior dif. de VPL (%) | Dif. na reavaliação |
| :-- | :-- | --: | :-- | --: | --: | --: | --: |
| Ibérica (Lisboa) | `1d` | 21 | TPE | 11 (11) | 9 (10) | 0 | 0 |
| | | | aleatória | 12 (26) | 10 (15) | 0 | 0 |
| | `1da` | 41 | TPE | 1 (6) | 1 (6) | 0 | 0 |
| | | | aleatória | 1 (6) | 1 (6) | 0 | 0 |
| | `2d` | 1 189 | TPE | 11 (12) | 11 (12) | 0 | 0 |
| | | | aleatória | 18 (36) | 18 (35) | 0 | 0 |
| Internacional (Londres) | `1d` | 21 | TPE | 11 (11) | 9 (10) | 0 | 0 |
| | | | aleatória | 12 (26) | 10 (15) | 0 | 0 |
| | `1da` | 41 | TPE | 1 (2) | 1 (2) | 0 | 0 |
| | | | aleatória | 1 (2) | 1 (2) | 0 | 0 |
| | `2d` | 1 189 | TPE | 8 (12) | 8 (12) | 0 | 0 |
| | | | aleatória | 8 (36) | 8 (35) | 0 | 0 |

`nsga` com o volume do reservatório como custo (frente de 46 pontos na Ibérica e 40 na Internacional; razão de hipervolume em
400 tentativas, mediana; pior): Ibérica, NSGA-II 0,9993; 0,9989 e aleatória 0,9984; 0,9975, com 67 % e 30 % da frente achada
(pior caso 46 % e 24 %); Internacional, NSGA-II 0,9998; 0,9995 e aleatória 0,9993; 0,9986, com 57 % e 32 % da frente (pior caso
35 % e 25 %). Diferença na reavaliação: 0 m³/ano. A tabela completa de cada execução está em `auditoria/iniciativas/resultados/`
(`brl|ibe|int`, `.md` e `.json`; pasta ignorada pelo Git).

## Sobre os tempos

A CPU desta máquina reduz o desempenho depois de poucos segundos de carga contínua. Um laço de Python puro, sem relação com o
Triton, passou de 0,03 s para cerca de 0,15 s após uns 3 s de uso, e um pytest de outra sessão ocupava a máquina durante a
medição. O mesmo código do Triton mediu 0,56 ms por ponto de grade no começo de um processo (grade `1d` do Brasil, 15,6 ms para
28 pontos) e cerca de 3 ms por ponto depois de alguns segundos de carga (grades `1da` e `2d` do Brasil). Por isso os tempos
absolutos medidos aqui valem só como ordem de grandeza; as comparações usam o **custo em grades**, em que o tempo de cada
estudo é dividido pelo tempo de uma varredura de referência medida logo antes e logo depois dele, na mesma condição da máquina
(cada estudo roda 5 vezes e vale a repetição de menor razão). As contagens de tentativas e de simulações não dependem do relógio.

Uma estimativa derivada dos números acima: no `2d` do Brasil, 300 tentativas do TPE levaram cerca de 2,8 s, dos quais as 140
simulações distintas (mediana) valeriam cerca de 0,4 s a 3 ms por ponto; o resto, perto de 85 %, é o próprio optuna (amostrador,
estudo, registro). Com a CPU em desempenho pleno a proporção deve ser parecida, porque as duas partes são Python/numpy.

## Conclusão

**O que se confirma.**

1. O ponto escolhido pelo optuna reproduz exatamente no motor determinístico: diferença de VPL de R$ 0,00 na reavaliação em todas
   as sementes, edições e experimentos, e trajetória idêntica nas repetições com a mesma semente (semente fixa, `n_jobs=1`,
   memória). Reprodutibilidade não é o obstáculo.
2. Na única edição com custos (Brasil, Santa Catarina), o TPE chega ao ótimo exato da grade de 1 189 pontos com mediana de 54
   simulações distintas (pior caso 76, cerca de 4,5 % a 6,4 % da grade) e a 1 % do ótimo com 13 (pior caso 14). A busca aleatória
   com as mesmas sementes e orçamento de 300 tentativas não achou o ótimo exato em nenhuma das 5 sementes, e ficou a até 0,077 %
   do VPL e 30 m³ de volume dele. Aqui o optuna ajuda.
3. No `nsga`, o NSGA-II ganha da busca aleatória só no fim do orçamento (45 % x 32 % da frente achada em 400 tentativas; os
   hipervolumes diferem na terceira casa decimal) e por margem pequena. Ambos cobrem mais de 98 % do hipervolume da grade com 400
   tentativas (273 simulações distintas do NSGA-II e 343 da aleatória, de 1 189 pontos).

**Onde a grade é melhor.**

1. Problema de uma dimensão (`1d`): o TPE precisou de 11 tentativas (9 a 10 simulações distintas) numa grade de 28 pontos, um terço
   da grade, e a busca aleatória precisou de 22; no problema de 41 pontos (`1da`) o TPE não foi melhor que a aleatória (22 x 23
   tentativas; a aleatória falhou em 2 de 5 sementes, o TPE em nenhuma). Com a grade de 28 pontos custando 15,6 ms, as 60 tentativas
   do TPE custaram 3,5 vezes a grade inteira, quase todo o tempo no próprio optuna. Para uma ou duas dimensões, a grade é mais
   barata, exata e dá a superfície completa.
2. A grade do Triton é barata e determinística: 1 189 pontos em 1,1 a 3,6 s nesta máquina conforme o estado da CPU. No `2d` do
   Brasil o TPE chegou ao ótimo com 0,16 grade (mediana), uma economia de cerca de 84 % do tempo da grade, isto é, de 1 a 3 s; o
   orçamento inteiro de 300 tentativas custou 0,80 grade.
3. O Triton precisa da grade inteira, não só do ótimo: TOPSIS, SMAA-VIKOR e os relatórios usam todas as alternativas de volume, e o
   `estudo run` promete bytes idênticos. O optuna devolve um ponto (ou uma frente amostrada) e perde a superfície.
4. O optuna não acrescenta confiança: o resultado só vale depois de reavaliado, e a reavaliação é a própria simulação que a grade
   já fez. Num espaço discreto de poucos milhares de pontos, a grade é auditável sem ressalvas.

**Limites do experimento.** Um projeto por edição; só o de Santa Catarina tem custos, e são estimativas de arquétipo. A área não
tem custo no modelo, de modo que a frente do `nsga` colapsa para a borda de área máxima e o problema é mais fácil do que parece.
Com 5 sementes, mediana e pior caso são indicativos, não estatística. A comparação usa o TPE com os parâmetros padrão do optuna 5.0.0
(10 tentativas iniciais aleatórias, `multivariate=False`); outros ajustes não foram testados. Não se mediu nenhum problema de 3
dimensões ou mais, que é onde a grade cresce de fato; a ideia de que o ganho do optuna aumenta com o número de dimensões é
hipótese, não resultado deste experimento.

## Recomendação para a 0.2.0

1. **Não integrar o optuna ao programa nem ao `estudo run`.** O ganho medido (alguns segundos, num caso de duas dimensões) não
   paga a dependência de ~14 MiB, a perda do contrato de bytes idênticos nem a perda da superfície de alternativas.
2. **Manter** o extra `otimizacao` e este script como ferramenta experimental de desenvolvimento, com os testes de `--help`, da
   mensagem do extra ausente e da importação sem o optuna (`tests/unit/test_experimento_optuna.py`).
3. **Reabrir a questão** só se surgir um estudo com 3 ou mais parâmetros contínuos ou uma simulação bem mais cara que a diária
   (por exemplo, passo horário), onde a grade fatorial (`_factorial_overrides`) fique em centenas de milhares de pontos. Nesse caso,
   o desenho certo é o do experimento: script à parte, semente fixa, `n_jobs=1`, memória, e reavaliação obrigatória do melhor ponto
   no motor determinístico antes de qualquer número ser reportado.
4. Antes do optuna, uma alternativa sem dependência é refinar a grade em duas passadas (grossa e fina em torno do melhor ponto),
   que preserva o determinismo. Não foi medida aqui.
