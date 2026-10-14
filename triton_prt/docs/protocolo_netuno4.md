# Protocolo de verificação com o Netuno 4

Roteiro para gerar, na interface do Netuno 4, os casos de referência que hoje faltam ao
Triton. Cada caso indica exatamente o que preencher, o que exportar e o que a
comparação verifica.

---

## 1. O que o Netuno 4 pode e não pode verificar

Levantado no [Manual do Usuário do Netuno 4](../additional_material/documentation/Manual-Triton-4_Junho2014.pdf)
(junho/2014). Nem toda lacuna do Triton tem antecessor com que comparar:

| Recurso do Triton | Netuno 4 tem? | Consequência |
| :--- | :---: | :--- |
| Balanço com reservatório inferior | sim | verificável |
| Reservatório superior e recalque | sim | verificável |
| Análise econômica (VPL, payback, TIR) | sim | **verificável — e hoje sem nenhuma referência externa** |
| Simulação de cenários | sim | verificável |
| Descarte de primeira chuva | sim, com **outra regra** | comparável, com a emulação descrita em §2 |
| Modulação de demanda semanal/mensal/diária | **não** | sem antecessor; exige outra estratégia |
| Irrigação com supressão por chuva | **não** | idem |
| Modos de descarte 2 e 3 | **não** | idem |

Os três últimos são acréscimos do Triton. Verificá-los exige cálculo manual documentado
ou casos analíticos, não comparação com o predecessor.

---

## 2. A diferença de descarte, e como neutralizá-la

O manual do Netuno 4, seção 3.1, define:

> «Caso a precipitação em um dado dia esteja abaixo desse valor, o Triton considerará que
> não houve precipitação.»

É a regra de **limiar**: abaixo do descarte, nada é captado; acima, capta-se a chuva
inteira. O Triton **subtrai** a lâmina (ver [`metodologia.md`](metodologia.md) §1).

Por isso toda comparação deve ser feita duas vezes:

- **sem** `--descarte-como-limiar` → mede a diferença total entre os programas;
- **com** `--descarte-como-limiar` → isola o balanço hídrico, neutralizando a diferença
  deliberada.

A emulação transforma a série de entrada e **não altera o motor**, de modo que a medição
não corre o risco de validar código que não é o distribuído.

Alternativa mais simples para quem opera a interface: **rodar com descarte = 0**. Sem
descarte as duas regras coincidem, e a comparação fica direta.

---

## 3. Casos a executar, em ordem de valor

### Caso A — Análise econômica *(prioridade máxima)*

**Por que:** o módulo econômico do Triton — VPL, TIR, payback — não tem **nenhuma**
referência externa. É a maior lacuna de verificação que resta, e o Netuno 4 a preenche.

**Na interface:** simulação normal seguida de «Análise Econômica».

| Campo | Valor |
| :--- | :--- |
| Série de precipitação | `Florianopolis1.csv` |
| Área de captação | 150 m² |
| Demanda total | 150 L/hab·dia |
| Moradores | 4 |
| Percentual pluvial | 50% |
| Coeficiente de escoamento | 0,80 |
| **Descarte** | **0 mm** (evita a diferença de regra) |
| Reservatório inferior | volume conhecido, 5.000 L |
| Reservatório superior | não utilizar |

Na janela econômica, registre **todos** os campos preenchidos: período de análise,
inflação mensal, período de reajuste, taxa mínima de atratividade mensal, mês de
instalação, custos iniciais e custos operacionais. O Netuno 4 usa taxas **mensais**; o
Triton, anuais — a conversão precisa ser explícita para a comparação valer.

**Exportar:** a tabela de fluxo de caixa e os indicadores (VPL, TIR, payback).

---

### Caso B — Reservatório duplo com recalque

**Por que:** o balanço com reservatório superior já foi verificado indiretamente (§4), mas
as saídas de **bombeamento** — energia, número de partidas, volume recalcado — não têm
referência.

| Campo | Valor |
| :--- | :--- |
| Série | `Florianopolis2.csv` |
| Área | 100 m² · Demanda 100 L/hab·dia · 4 moradores |
| Percentual pluvial | 90% · Coeficiente 0,80 |
| **Descarte** | **0 mm** |
| Reservatório superior | 500 L |
| Reservatório inferior | intervalo de 0 a 5.000 L, passo 500 L |

**Exportar:** a tabela de varredura (uma linha por volume).

---

### Caso C — Varredura ampla, reservatório único

**Por que:** amplia a grade de volumes e a faixa de parâmetros da verificação atual, que
se concentra em poucos valores.

| Campo | Valor |
| :--- | :--- |
| Série | `Manaus1.csv` |
| Área | 200 m² · Demanda 200 L/hab·dia · 5 moradores |
| Percentual pluvial | 40% · Coeficiente 0,90 |
| **Descarte** | **0 mm** |
| Reservatório inferior | intervalo de 0 a 20.000 L, passo 1.000 L |

---

### Caso D — Sensibilidade ao descarte

**Por que:** mede diretamente a diferença entre as duas regras, em vez de inferi-la.

Repita o Caso C três vezes, mudando apenas o descarte: **0 mm, 2 mm e 5 mm**. Com
descarte 0 os programas devem coincidir; a divergência que aparecer em 2 e 5 mm é
inteiramente atribuível à diferença de regra.

---

## 4. O que já foi verificado com o material existente

O repositório já continha uma exportação de varredura do Netuno 4
(`data/simulation_outputs/Florianopolis2_Descarte2_Area100_...csv`). Comparando-a com o
motor do Triton, com a regra de limiar emulada e reservatório superior de 500 L:

| Saída | Erro médio | Erro máximo |
| :--- | ---: | ---: |
| Potencial de economia | 0,13 pp | 0,34 pp |
| Extravasamento | 0,45 L/dia | 1,28 L/dia |

O caminho de **reservatório duplo** replica o Netuno 4 tão bem quanto o de reservatório
único, o que antes não se sabia — a comparação em lote nunca o exercitava.

---

## 5. Como rodar a comparação

```bash
python scripts/comparar_exportacao_netuno4.py CAMINHO/DA/EXPORTACAO.csv \
    --serie Florianopolis2.csv --area 100 --demanda 100 --moradores 4 \
    --percentual 90 --coeficiente 0.8 --descarte 0 \
    --reservatorio-superior 500 --limiar-recalque 0
```

A comparação confronta **sete saídas por volume** — potencial de economia, consumo
pluvial, consumo potável, extravasamento e os três percentuais de atendimento —, e não
apenas o indicador agregado.

---

## 6. Ao devolver os arquivos

Guarde cada exportação em `data/simulation_outputs/`, com um nome que registre os
parâmetros, e anote junto **todos os campos preenchidos na interface** — sobretudo os da
janela econômica, que não aparecem no arquivo exportado. Sem eles a comparação não é
reproduzível.
