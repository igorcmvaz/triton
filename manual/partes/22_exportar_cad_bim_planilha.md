# 22. Exportar para CAD, BIM e planilha

> **Pergunta que este guia responde:** como levar o resultado para o projeto
> executivo e para a análise própria?

---

## 22.1. O que cada formato leva

| Formato | Extensão | O que leva | Para quê |
| :--- | :--- | :--- | :--- |
| relatório | HTML, PDF | resultado completo e premissas | entregar |
| planilha | XLSX | série diária e varredura | reanalisar |
| desenho | DXF | esquema hidráulico dimensionado | projeto executivo |
| modelo | IFC | componentes com propriedades | compatibilização BIM |

---

## 22.2. Planilha

O caminho de quem vai fazer análise própria.

**Série diária.** Uma linha por dia da simulação, com chuva, chuva efetiva,
captação, demanda, consumo pluvial, consumo de rede, extravasamento, volume nos dois
reservatórios, recalque e classe de atendimento. É a base de qualquer gráfico ou
estatística que o programa não ofereça.

**Varredura.** Uma linha por volume simulado, com todos os indicadores. É a base da
curva de retorno do capítulo 7.

> **Um aviso de tamanho.** Trinta anos de série diária são 10.950 linhas por
> simulação. Uma varredura de doze volumes com série detalhada gera cento e trinta
> mil linhas. Exporte a série detalhada só do volume que interessa.

---

## 22.3. Desenho em DXF

O programa gera o esquema hidráulico do sistema dimensionado: cisterna, filtro,
descarte, bomba quando houver, reservatório superior, e a tubulação com os diâmetros
adotados.

É um **esquema**, não um projeto executivo. Ele traz os componentes e as
conexões lógicas, e serve de base para o projetista desenhar em planta, com as
cotas e o traçado reais.

O que o programa **não** dimensiona:

- traçado e declividade da tubulação;
- perda de carga real da instalação;
- reservatório de autolimpeza do descarte, cujo volume é `A × d_f`;
- extravasor e ligação à drenagem;
- fundação e impermeabilização da cisterna.

---

## 22.4. Modelo em IFC

Para compatibilização com o modelo BIM da edificação. Os componentes saem com
propriedades: volume, material, e os parâmetros do dimensionamento.

Vale para coordenação e para quantitativos. Não substitui a modelagem da instalação
hidráulica, que é do projetista.

---

## 22.5. Relatórios

Os três do capítulo 13: executivo, ambiental com ESG, e científico. Em HTML para
consulta e em PDF para entrega.

> O programa tem dois geradores de PDF e usa o mais completo que a máquina permitir.
> Quando cai para o alternativo, o documento sai mais simples, com o mesmo conteúdo e
> os mesmos números.

---

## 22.6. Um conselho de arquivo

Ao fechar um estudo, guarde junto, na mesma pasta:

1. o arquivo `.netuno`;
2. a **série de chuva** usada, ou sua identificação exata na base;
3. o relatório científico em PDF;
4. a planilha da varredura;
5. se houve lote, o **script** com os comandos;
6. um arquivo de texto com a **versão do programa**.

São seis itens que tornam o estudo reproduzível daqui a cinco anos. Sem eles, o
relatório em PDF é só uma afirmação.
