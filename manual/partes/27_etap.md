# Dimensionamento da ETAP

> Este capítulo formaliza como o programa dimensiona a linha de tratamento, e
> explica a **regra incremental** que impede o tratamento de ser contado duas vezes.

---

## O que a ETAP compreende

Três estágios, em série:

1. **filtro mecânico de entrada**, que retira folhas e sólidos grosseiros;
2. **desinfecção**, que é o estágio obrigatório;
3. **filtro de polimento**, opcional.

O dimensionamento consome três entradas: a **classe de qualidade alvo**, a **área de
cobertura** e o **volume pluvial anual consumido**, que vem do balanço da seção {{n:23}}.

---

## O filtro de entrada

Dimensionado pela **área de cobertura**, e não pela classe:

| Cobertura | Equipamento | Malha |
| :--- | :--- | ---: |
| até 200 m² | vórtex autolimpante DN 100 | 350 µm |
| até 500 m² | vórtex autolimpante DN 150 | 400 µm |
| acima de 500 m² | cesto ou ciclônico DN 200 | 500 µm |

> Os limites de faixa acompanham a área que o próprio produto declara atender. Até a
> versão 5.0.7 eram 150 e 400 m², contra rótulos de «até 200 m²» e «até 500 m²»: um
> telhado de 180 m² recebia o filtro da faixa seguinte, mais caro, embora o da
> primeira faixa fosse declarado suficiente.

---

## A desinfecção

| Opção | Residual | O que entra no custeio |
| :--- | :---: | :--- |
| cloração por pastilhas | **sim** | massa anual de produto |
| ultravioleta | não | lâmpada e energia |
| ozonização | não | gerador e energia |

**Ultravioleta e ozônio entram como barreira adicional à cloração, e não como
substitutas.** Sem residual, a água tratada volta a se contaminar no percurso até o
ponto de uso, e a prática correta mantém a cloração para proteger o reservatório e a
rede interna.

Por isso as duas opções **somam** o custo do cloro, e a escolha nunca reduz custeio.

### A massa de cloro

```
massa de produto por m³ = (dose em mg Cl₂/L ÷ 1000) ÷ pureza
```

> **O que se compra é o produto, e não o cloro puro.** Pastilha de hipoclorito de
> cálcio tem cerca de 65% de cloro ativo, e o preço em reais por quilograma é do
> produto. Até a versão 5.0.7 a conta usava a massa de cloro ativo, subestimando o
> custo em `1/0,65` — cerca de 35%.

---

## O filtro de polimento

Opcional, e é o único ponto em que a **classe alvo** interfere no dimensionamento.

| Classe | Recomenda polimento? | Equipamento quando marcado |
| :--- | :---: | :--- |
| 1 — NBR 15527:2019 | não | filtro de areia ou cartucho de 20 µm |
| 2 — irrigação e lavagem | sim | idem |
| 3 — torres e caldeiras | sim | idem |
| 4 — lavagem de roupas | sim | **carvão ativado em bloco** |

**A recomendação não é imposição.** O filtro só entra se o usuário marcar. Quando a
classe recomenda e o usuário recusa, o programa registra a recusa no campo
`polishing_recommended_but_declined`, e o relatório a exibe.

> Até a versão 5.0.8 a condição era «marcado **ou** a classe exige», e a classe
> sobrepunha a escolha em silêncio: desmarcar a caixa não surtia efeito nenhum nas
> classes 2 a 4.

> **As classes 2 a 4 são adaptações do programa, não da NBR 15527.** A matriz de
> parâmetros por uso é característica da versão de 2007 da norma e não sobreviveu à
> revisão. Num estudo publicado, apresente-as como critério adotado, e não como
> requisito normativo.

---

## A regra incremental

É a parte que mais erra quem implementa este cálculo por conta própria.

**No investimento.** O orçamento de um sistema pluvial já traz uma verba genérica de
tratamento dentro da rubrica «Acessórios». Somar a linha detalhada por cima dela
contaria o tratamento duas vezes. O programa desconta a verba genérica e soma apenas
o **incremento**:

```
CAPEX_ETAP_incremental = CAPEX_da_linha − verba_genérica_de_tratamento
```

**No custeio.** A cloração já é paga na linha de insumos químicos do fluxo de caixa.
O custeio incremental da ETAP desconta essa parcela, de modo que o hipoclorito seja
pago **uma vez só**.

**Na avaliação de ciclo de vida.** A linha de tratamento **substitui** o termo de
cloração, em vez de somar a ele.

> A regra vive num módulo único, consumido pelos **dois** motores econômicos do
> programa. Duas cópias divergiriam, e foi assim que a cloração chegou a ter cinco
> convenções diferentes numa versão anterior.

---

## Desligar a ETAP

Com `etap_enabled` falso, o dimensionamento não roda e o programa reproduz
exatamente o comportamento da versão 5.0.7. É a chave de compatibilidade para
comparar resultados entre versões.

---

## O que o programa não dimensiona

- **o reservatório de autolimpeza** do descarte, cujo volume é `A × d_f`;
- a **tubulação** e a perda de carga da linha de tratamento;
- o **regime de manutenção**: troca de elemento filtrante, limpeza do vórtex,
  reposição de pastilha;
- o **controle de qualidade**: o programa dimensiona equipamento, e não substitui
  ensaio laboratorial.

A NBR 15527 trata do controle e da manutenção, e esse plano é do projetista.
