# 20. Análise de sensibilidade

> **Pergunta que este guia responde:** qual premissa mais move o meu resultado, e o
> quanto ele aguenta?

Todo estudo pluvial repousa sobre premissas incertas: a tarifa vai subir 5% ao ano?
A demanda é mesmo 150 L por pessoa? A cisterna custa mesmo isso? A análise de
sensibilidade mede quanto dessas dúvidas chega ao resultado.

---

## 20.1. Monte Carlo, pela linha de comando

```bash
python -m netuno.cli uncertainty projeto.netuno \
  --samples 2000 --seed 42 \
  --rainfall-cv 10 --demand-cv 15 --area-cv 5 --capex-cv 20 \
  --analysis all --format json --output incerteza.json
```

Cada `--*-cv` é o **coeficiente de variação**, em percentual, da premissa
correspondente. O programa sorteia, roda, e devolve a distribuição do resultado em
vez de um número.

| Opção | O que perturba |
| :--- | :--- |
| `--rainfall-cv` | a lâmina de chuva |
| `--area-cv` | a área de captação |
| `--demand-cv` | a demanda |
| `--capex-cv` | o investimento |
| `--samples` | número de sorteios |
| `--seed` | semente, obrigatória para reprodutibilidade |

---

## 20.2. Escolher os coeficientes

O coeficiente de variação não é palpite: ele vem do que você sabe sobre a incerteza
de cada dado.

| Premissa | CV plausível | Por quê |
| :--- | ---: | :--- |
| área de captação | 2 a 5% | é medida em projeto; o erro é de leitura |
| demanda, se medida | 5 a 10% | variação real entre meses |
| demanda, se de referência | 15 a 25% | a dispersão da literatura é grande |
| chuva | 10 a 20% | variabilidade interanual |
| investimento | 15 a 30% | dispersão de orçamento é notória |

> **Não sorteie o que você conhece.** Se a área foi medida em levantamento, o CV é
> pequeno; inflá-lo produz uma incerteza artificial que dilui o resultado.

---

## 20.3. Sensibilidade dos pesos do multicritério

Caso diferente, e frequentemente mais útil. Se o volume recomendado depende dos
pesos, o estudo precisa mostrar **quanto** depende:

```bash
python -m netuno.cli run projeto.netuno \
  --analysis topsis --weight-sensitivity 1000 --seed 42
```

O programa sorteia mil combinações de pesos e informa com que **frequência** cada
volume vence. Um volume que vence em 80% dos sorteios é uma recomendação robusta;
um que vence em 30% é uma recomendação frágil, e o texto precisa dizer isso.

É o mesmo princípio do SMAA-VIKOR, disponível na interface.

---

## 20.4. A premissa que quase sempre domina

Em estudos econômicos de aproveitamento pluvial, a premissa que mais move o
resultado costuma ser o **reajuste tarifário**, e ela **não** está entre as opções
de `uncertainty`.

Cinco por cento ao ano durante vinte anos multiplica a tarifa por 2,65. Três por
cento multiplica por 1,81; sete por cento, por 3,87. O valor presente líquido varia
proporcionalmente.

Para testar isso, rode o caso com reajustes diferentes e compare:

```bash
for r in 3 5 7; do
  python -m netuno.cli run projeto.netuno --analysis economic \
    --set water_tariff_escalation=$r --set sewage_tariff_escalation=$r \
    --format json --output "saida/reajuste_${r}.json"
done
```

> **Num artigo, mostre essa faixa.** Um VPL único com reajuste de 5% ao ano
> apresentado sem sensibilidade sugere uma precisão que a premissa não tem.

---

## 20.5. Como apresentar

Três formas, da mais simples à mais completa:

**Tabela de cenários.** Pessimista, provável e otimista, com as premissas de cada
um declaradas. Simples e defensável.

**Gráfico de tornado.** Uma barra por premissa, mostrando o quanto o resultado varia
quando ela varia sozinha. Ordena as premissas por importância e é a apresentação mais
informativa por área de página.

**Distribuição.** Histograma ou faixa de confiança do Monte Carlo. Exige declarar as
distribuições adotadas, e não só os coeficientes de variação.

---

## 20.6. O que declarar

- os **coeficientes de variação** e a origem de cada um;
- o número de **amostras** e a **semente**;
- a **distribuição** adotada, quando não for a padrão do programa;
- para sensibilidade de pesos, o número de sorteios e a frequência vencedora;
- **quais premissas não foram perturbadas**, e por quê.

A última é a que mais se esquece, e a que um revisor mais cobra.
