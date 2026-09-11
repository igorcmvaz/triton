# Indicadores de eficiência

> Este capítulo define formalmente cada indicador que o programa reporta, com
> unidade, e diz **o que cada um não mede**.

Um indicador mal interpretado é pior que nenhum. Os dois primeiros deste capítulo são
frequentemente confundidos na literatura.

---

## Potencial de economia de água potável

O potencial de economia de água potável é o indicador central do programa e aquele que
figura no resumo de qualquer estudo. Ele expressa a fração do consumo **total** da
edificação que a água pluvial conseguiu substituir ao longo de toda a série simulada, e
não apenas da parcela que a chuva poderia atender.

```equacao:potencial
Epot = ( Σ V_con,t ÷ Σ D_t ) × 100
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Epot` | potencial de economia de água potável | % |
| `V_con,t` | volume de água pluvial consumido no dia `t` | L |
| `D_t` | demanda total da edificação no dia `t` | L |
| `Σ` | somatório sobre todos os dias da série simulada | — |

O denominador da Equação {{eq:potencial}} é a demanda **total**, e essa escolha é a
origem da confusão mais comum na leitura de resultados. Um sistema que atendesse
integralmente toda a demanda que lhe cabe, sem falhar um único dia, ainda assim
apresentaria potencial de economia igual à fração atendível declarada, e não a cem por
cento. O teto, portanto, não é uma limitação do sistema: é uma consequência aritmética
da definição do indicador.

---

## Confiabilidade volumétrica

A confiabilidade volumétrica responde a uma pergunta diferente, e complementar: da água
que o sistema **deveria** fornecer, quanto ele de fato forneceu? O denominador aqui é a
demanda pluvial, e não a demanda total.

```equacao:confiabilidade
Rv = ( Σ V_con,t ÷ Σ D_pl,t ) × 100
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Rv` | confiabilidade volumétrica do sistema | % |
| `V_con,t` | volume de água pluvial consumido no dia `t` | L |
| `D_pl,t` | demanda pluvial do dia `t`, isto é, a parcela atendível por chuva | L |
| `Σ` | somatório sobre todos os dias da série simulada | — |

As Equações {{eq:potencial}} e {{eq:confiabilidade}} diferem apenas no denominador, e
essa diferença basta para que se relacionem por uma identidade exata, útil como
conferência rápida de qualquer resultado.

```equacao:relacao_indicadores
Epot = Rv × f
```

| Símbolo | Significado | Unidade |
| :--- | :--- | :--- |
| `Epot` | potencial de economia de água potável | % |
| `Rv` | confiabilidade volumétrica | % |
| `f` | fração da demanda total atendível por água pluvial | adimensional |

==Um sistema com 94% de confiabilidade e 40% de fração atendível economiza 37,5% do
consumo total, e os três números dizem a mesma coisa de três maneiras.== Relatar apenas
um deles, sem declarar a fração atendível adotada, torna o resultado impossível de
comparar com o de outro estudo — e é a causa mais frequente de comparações indevidas na
literatura da área.

---

## Confiabilidade temporal

Os três percentuais de dias, que somam 100%:

| Classe | Definição |
| :--- | :--- |
| **pleno** | `V_con,t = D_pl,t`, com tolerância de 10⁻⁵ L |
| **parcial** | `0 < V_con,t < D_pl,t` |
| **nulo** | `V_con,t = 0` |

**O que mede:** com que frequência o usuário pode contar com o sistema.

**O que não mede:** o volume. Um sistema pode ter 95% de dias plenos e potencial
baixo se a demanda pluvial for pequena, e o contrário também acontece.

> A confiabilidade temporal é o indicador que mais importa para o **projeto
> hidráulico**. Muitos dias nulos exigem alimentação automática de reserva bem
> dimensionada, e o usuário percebe a alternância entre as duas fontes.

---

## Extravasamento

```
Vext = média diária do volume que transbordou     [L/dia]
```

**O que mede:** o quanto a cisterna é pequena em relação aos eventos de chuva.

**O que não mede:** desperdício. A água que extravasa vai para a drenagem urbana,
como iria sem o sistema. Não há perda em relação ao cenário sem sistema — há apenas
oportunidade não aproveitada.

> O extravasamento **nunca zera** num sistema real. Ele tende a um piso que é a
> diferença entre o que a cobertura capta e o que a demanda consome, e no tutorial
> esse piso é mais da metade da água captada. Quem quer retenção de cheia precisa de
> um reservatório de detenção, que é outro projeto com outra lógica.

---

## Volume anual poupado

```
Vpoup = média diária consumida de pluvial × 365,25 ÷ 1000     [m³/ano]
```

**O que mede:** a base de cálculo do econômico e da avaliação de ciclo de vida.

> **Aprofundamento: o 365,25 não é descuido.** A conversão usa o ano médio, incluindo bissextos,
> porque séries longas os contêm. Usar 365 introduziria um viés sistemático de
> 0,07% — pequeno, mas gratuito.

---

## Ganho marginal

```
Δ = variação do potencial ÷ variação de volume     [%/m³]
```

Definido na seção {{n:24}}. É o indicador que decide o volume ideal, e **só existe numa
varredura** — uma simulação de volume único não o produz.

---

## Demanda não atendida

```
Vnao = média diária da demanda que ninguém forneceu     [L/dia]
```

Terceira parcela do balanço de demanda, introduzida na versão 5.0.8. É zero na
configuração padrão e deixa de ser zero quando o suprimento de reserva da irrigação
está desligado.

**Por que existe:** sem ela, o balanço fecharia por construção, atribuindo à rede
toda a demanda que a chuva não atendeu. A seção {{n:23}} detalha.

---

## Quadro-resumo

| Indicador | Unidade | Denominador | Responde |
| :--- | :--- | :--- | :--- |
| potencial de economia | % | demanda total | quanto da conta cai |
| confiabilidade volumétrica | % | demanda pluvial | quanto do pretendido se atendeu |
| dias plenos, parciais, nulos | % | dias da série | com que frequência se pode contar |
| extravasamento | L/dia | — | o reservatório é pequeno? |
| volume poupado | m³/ano | — | base do dinheiro e do carbono |
| ganho marginal | %/m³ | — | vale ampliar? |
| demanda não atendida | L/dia | — | o que ninguém forneceu |
