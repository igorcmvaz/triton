# 13. O relatório, e o que declarar num artigo

> Ao terminar este capítulo você terá o relatório emitido e, se pretende publicar, a
> lista do que precisa constar no método do artigo. Essa lista é o capítulo mais
> curto e o mais importante do manual.

---

## 13.1. Os três relatórios

O programa emite três, e eles têm públicos diferentes.

**Executivo.** Quatro a seis páginas. Resultado técnico, investimento, retorno e
uma conclusão. É o que se entrega ao cliente.

**Ambiental e ESG.** Inventário de ciclo de vida item a item, saldo de carbono, e o
enquadramento nas certificações: LEED, AQUA-HQE, Selo Casa Azul, EDGE e GRI 303.
É o que se anexa a processo de certificação.

**Científico.** Método completo, premissas declaradas, série utilizada, e os
resultados com a precisão que um artigo exige. É a base para publicação.

Além deles, a etapa **10. Exportação** gera desenho em DXF, modelo em IFC e planilhas com a
série diária e a varredura completa.

---

## 13.2. O que o relatório não decide por você

O relatório traz os números. Não traz o **contexto** que torna os números
reproduzíveis. Esse contexto é seu, e é o assunto do resto do capítulo.

---

## 13.3. A lista de declaração

Um estudo feito com o Netuno que não declare os itens abaixo não é reproduzível, e
não é comparável com outro estudo do mesmo programa. Copie a lista no método do seu
artigo.

### Programa e versão

- **Versão do Netuno**, incluindo o número de revisão. Correções entre versões mudam
  resultados: a correção da energia de bombeamento da 5.0.8 mudou o consumo da
  motobomba em 65%.

### Série de precipitação

- **Origem**: estação, base nacional, ou modelo climático.
- Se for base nacional: **modelo, cenário e janela temporal**.
- **Recorte**: datas de início e fim, e número de anos.
- **Tratamento de falhas** e critério de descarte de ano incompleto.

### Edificação e demanda

- Área de captação e **como foi obtida** — projeção horizontal.
- Coeficiente de escoamento e sua origem.
- Consumo per capita e se é **medido ou de referência**.
- **Fração atendível por água pluvial** e os usos finais que a compõem. É o teto do
  resultado, e sem ele o potencial não se interpreta.

### Descarte de primeiras águas

- Lâmina adotada e **modo** entre os três.
- **A divergência em relação ao Netuno 4**, se o estudo comparar as versões: o
  Netuno 4 trata a lâmina como limiar do evento, o Netuno 5 a subtrai, e a diferença
  vale de 2,3 a 2,7 pontos percentuais de economia sobre 4.050 casos de referência.

### Volume e critério de escolha

- Se veio de varredura: **limiar de ganho marginal adotado**. Sem ele, «volume
  ideal» não significa nada.
- Se veio de multicritério: **os pesos dos sete critérios** e o método, TOPSIS ou
  SMAA-VIKOR.
- Que a normalização do TOPSIS é uma **variante** com translação por `x − min(x)`.

### Análise econômica

- **Município e concessionária**, com a data de vigência da tabela tarifária.
- **Regime de mínimo** entre os cinco. É o que mais muda resultado entre municípios.
- Percentual de esgoto, e que ele incide sobre a **tarifa de água**.
- Taxa mínima de atratividade, inflação, período de análise.
- **Reajustes tarifários** de água, esgoto e energia, com o intervalo.

### Avaliação de ciclo de vida

- **Fronteira**: água entregue, e não produzida.
- **Vida útil** adotada e sua justificativa.
- **Material** do reservatório. Ele inverte o sinal do resultado, como o capítulo 11
  mostra.
- Base do fator de emissão da rede elétrica, **com o ano**.
- Quais fatores carregam **rótulo de triagem**.

### Certificações

- Que as classes 2 a 4 de qualidade são **adaptações do programa**, não da NBR 15527.
- No caso do EDGE, que o programa avalia **apenas a barra de água**, e que o
  caso-base usado é o declarado ou a demanda modelada.

---

## 13.4. O parágrafo pronto

Para o nosso projeto, o método ficaria assim:

> A simulação foi conduzida no Netuno 5.0.8, com modelo comportamental de base
> diária (YAS, extravasamento anterior à retirada da demanda), sobre série de
> precipitação de Florianópolis com 30 anos (10.950 dias, média de 1.795 mm/ano).
> Adotou-se área de captação de 150 m² em projeção horizontal, coeficiente de
> escoamento de 0,85 (telha cerâmica) e descarte de primeiras águas de 2,0 mm em
> todo evento, subtraído da lâmina diária — divergência deliberada em relação ao
> Netuno 4, que trata o valor como limiar do evento. A demanda total adotada foi de
> 600 L/dia (4 moradores, 150 L/hab·dia), com fração atendível por água pluvial de
> 40%, correspondente a bacia sanitária, máquina de lavar e usos externos. O volume
> de 5.000 L resultou do critério de ganho marginal com limiar de 1 %/m³ e foi
> confirmado por análise multicritério TOPSIS com pesos iguais sobre sete critérios,
> com normalização em variante de Hwang e Yoon translada por x − min(x). A análise
> econômica utilizou a estrutura tarifária da CASAN vigente desde 01/04/2026, regime
> de disponibilidade, esgoto a 100% da tarifa de água, TMA de 0,5% ao mês, inflação
> de 0,35% ao mês, reajustes de 5% ao ano em intervalos de 12 meses e período de 20
> anos. A avaliação de ciclo de vida adotou fronteira de água entregue, reservatório
> em polietileno e vida útil de 20 anos.

Duzentas e cinquenta palavras. É o que separa um estudo reproduzível de um número
solto.

---

## 13.5. O fim do tutorial

Dez capítulos, um projeto, e um estudo completo. A tabela do capítulo 12 é o
resultado.

O que fazer agora depende do que você quer:

- **Resolver um caso diferente do tutorial** — a Parte 3, os guias de tarefa.
- **Entender de onde vem cada número** — a Parte 4, o método.
- **Não cometer os erros que o programa não impede** — o capítulo 33.
- **Defender o estudo diante de um revisor** — a Parte 6.
