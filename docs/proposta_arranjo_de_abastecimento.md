# Proposta: arranjo de abastecimento dos pontos de uso

Situação: **implementada** em 17/09/2026, com as decisões da seção 6. Código em
`netuno/core/supply_arrangement.py` e `netuno/core/pump_energy.py`; testes em
`tests/unit/test_arranjo_de_abastecimento.py`.

## 1. O problema, medido

O programa não tem um lugar único que diga como a água sai da cisterna e chega aos
pontos de uso. Cada módulo presume uma coisa, e no projeto do tutorial (5 m³,
Florianópolis, sem caixa superior) as presunções se contradizem:

| Módulo | O que presume hoje | Efeito no tutorial |
| :--- | :--- | :--- |
| Balanço hídrico | caixa superior só se `upper_tank_used` | sem caixa: atendimento direto da cisterna |
| Econômico | energia só com caixa superior (`economic.py`, `if config.upper_tank_used`) | **0 kWh/ano**; duas motobombas no investimento |
| ACV, tabelas do manual | `EnvironmentalConfig()` nasce com `upper_tank_used=True` e 500 L | **caixa de 11 kg** no carbono incorporado |
| ACV, energia | sem kWh informado, cobra `volume pluvial × kWh/m³` (`environmental.py`, item 5) | **1,01 kg CO₂e/ano** de bombeamento, como se houvesse pressurização |
| ACV, cloração | só conta o cloro `if config.upper_tank_used` | na interface, sem caixa superior, o cloro **some** do carbono, mas continua no custo |

Resultado: o mesmo projeto não tem bomba no custo e tem bomba no carbono, e na
interface perde a emissão do cloro ao desmarcar a caixa superior. A limitação
declarada na seção 5.2 do manual ("sem caixa superior o programa não calcula
energia") é verdadeira no econômico e falsa na ACV.

## 2. A estrutura proposta

Uma pergunta única na etapa **4. Reservatório & Custos**, que substitui a opção
"Não utilizar reservatório superior" do combo atual:

> **Como a água chega aos pontos de uso?**

| Arranjo | Campo `supply_arrangement` | Pede | Energia | Carbono incorporado |
| :--- | :--- | :--- | :--- | :--- |
| Recalque para caixa superior | `recalque` | volume da caixa, nível de acionamento, altura manométrica, bomba | bateladas de enchimento da caixa (o cálculo atual) | caixa + motobombas + sucção e recalque |
| Pressurização direta | `pressurizacao` | pressão de trabalho, bomba, acionamentos por dia, potência em espera | **todo** o volume pluvial consumido, mais partidas e espera | motobombas (pressurizador) + sucção; sem caixa |
| Gravidade | `gravidade` | nada | **zero**, declarado | só a cisterna e a tubulação |

Os campos de cada arranjo só aparecem quando ele é escolhido.

### 2.1 Uma função, três consumidores

```text
energia_de_abastecimento(cfg, resultado_da_simulacao) -> EnergiaDeAbastecimento
    arranjo, kWh/ano, m³ bombeados, partidas/ano, kWh/m³, potência de espera
```

Vive em `netuno/core/pump_energy.py` e é a **única** fonte de energia para o
econômico, a ACV, os relatórios e a linha de comando. A ACV deixa de ter o
fallback `volume × kWh/m³` e deixa de ligar a cloração à caixa superior.

### 2.2 A física da pressurização

Mesma cadeia já usada no recalque, com três diferenças:

```text
e     = ρ · g · H_p / (η_bomba · η_motor)            kWh/m³
E_ano = V_pluvial · e
```

1. **Volume**: todo o pluvial consumido, e não as bateladas de enchimento.
2. **Altura**: a pressão de trabalho do pressurizador, e não a altura da caixa.
3. **Partidas**: contadas (moradores × acionamentos por pessoa por dia) e relatadas,
   mas sem energia própria: a sucção está afogada, não há escorva, e a bomba entrega
   vazão útil desde que o pressostato liga.

## 3. Compatibilidade

| Arquivo antigo | Vira |
| :--- | :--- |
| `upper_tank_used = 1` | `recalque`, números idênticos aos de hoje |
| `upper_tank_used = 0` | `nao_informado`: simula como hoje, e a etapa 4 mostra aviso pedindo a escolha |

`upper_tank_used` continua sendo lido e gravado, derivado do arranjo, para que
versões anteriores abram o arquivo.

## 4. O que muda nos números publicados

O tutorial precisa **declarar** um arranjo. Com qualquer escolha, os números da
seção 4.8 mudam, porque hoje a ACV carrega caixa e bombeamento que o tutorial não
tem. As tabelas, figuras e testes do manual são regenerados; os testes que conferem
o manual acusam cada número deslocado.

## 5. Testes a acrescentar

- `gravidade` dá 0 kWh no econômico e na ACV;
- `recalque` reproduz exatamente os números atuais do caso de referência;
- econômico e ACV recebem **o mesmo** kWh/ano para os três arranjos;
- o cloro entra na ACV nos três arranjos, sempre que a cloração estiver ativa;
- `pressurizacao` cresce com a pressão de trabalho e com os acionamentos;
- arquivo antigo sem caixa abre como `nao_informado`, com aviso, sem mudar número.

## 6. Decisões tomadas

1. **Tutorial**: recalque para caixa superior de 1.000 L, limiar de 100 L, duas
   motobombas de meio CV. As seções anteriores à do reservatório superior estudam a
   cisterna sozinha; da seção do reservatório superior em diante, o projeto inclui a
   caixa, as bombas e a energia.
2. **Pressão de trabalho padrão**: 18 m.c.a., média da faixa do pressostato do Komeco
   TP 820 (liga a 12, desliga a 24 m.c.a.), manual do fabricante em
   `Material_Referencia/Documentos_Consultados/04_EPD_e_Fabricantes`.
3. **Acionamentos**: moradores × 5,42 por pessoa por dia, isto é, 5,05 descargas e 0,37
   ciclos de lavadora (Mayer, DeOreo et al., 1999, AWWARF).
4. **Partida e espera**: não somadas. O pressostato liga quando o uso começa e a bomba
   entrega vazão útil desde então; o pressostato mecânico não consome em espera. A
   limitação está declarada no manual, para pressurizadores com inversor.

## 7. Correções que vieram junto

- A ACV ligava a cloração à caixa superior; agora a liga ao tratamento.
- A função de energia tratava séries menores que um ano como um ano inteiro; agora usa
  a média diária, como o econômico.
- O gráfico de tornado do manual não informava a bomba e usava os padrões da função
  (0,75 kW, 150 h/ano, R$ 1/kWh); agora usa a energia do projeto.
- O manual dizia que o limiar de acionamento imobiliza água; o balanço consome a reserva.
  A perda do arranjo duplo vem do extravasamento da cisterna com a caixa superior ainda
  com espaço.
