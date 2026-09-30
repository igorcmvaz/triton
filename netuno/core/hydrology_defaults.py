"""Padrões hidrológicos com fonte declarada.

O coeficiente de escoamento estava com **quatro** valores de recurso diferentes
espalhados pelo programa — 0,75 na interface e no gerador de relatório, 0,85 no
exportador CAD, 0,90 no motor de simulação e na leitura de planilha. Como cada
caminho de entrada pegava um deles, o mesmo projeto podia render captações
diferentes conforme fosse aberto por arquivo, por planilha ou pela interface.

Aqui existe um valor só, com a razão de ser dele escrita ao lado.
"""

from __future__ import annotations

# O valor de recurso é o da telha cerâmica, 0,75, o material mais comum nas
# coberturas residenciais brasileiras e o primeiro da lista de materiais. É o
# mesmo que a interface pré-seleciona: um valor só, para que o projeto aberto
# por arquivo, por planilha ou pela tela renda a mesma captação.
#
# A ABNT NBR 15527:2019, item 4.1.6, recomenda outro número, eta = 0,85, para a
# eficiência do sistema de captação na falta de dados. O manual o usa no
# tutorial, digitado como valor personalizado, e declara a diferença.
COEFICIENTE_DE_ESCOAMENTO_PADRAO = 0.75

# A lâmina de descarte da primeira chuva tinha o mesmo defeito: 1,0 mm no
# arquivo de projeto, na leitura de planilha e no motor, contra 2,0 mm no
# exportador CAD, na linha de comando, no gerador de relatório e na dica do
# próprio campo da tela. O mesmo projeto descartava o dobro conforme o caminho.
#
# Fica 2,0 mm, que é o que a ABNT NBR 15527:2019, item 4.1.5, recomenda na
# ausência de dado local. Quem tem ensaio da própria cobertura digita o valor
# medido; quem não tem recebe o da norma, e não um número sem procedência.
LAMINA_DE_DESCARTE_PADRAO_MM = 2.0

FONTE_DA_LAMINA_DE_DESCARTE = (
    "ABNT NBR 15527:2019 — Aproveitamento de água de chuva de coberturas para "
    "fins não potáveis: requisitos, item 4.1.5."
)

FONTE_DO_COEFICIENTE = (
    "Telha cerâmica, 0,75: ESTUDO sobre materiais para coberturas utilizadas em "
    "sistemas de aproveitamento de água pluvial residenciais. MIX Sustentável, "
    "v. 6, n. 2, p. 53-66, 2020."
)

# Coeficientes por material da cobertura, na ordem em que a interface os lista.
# Sao os valores do estudo de materiais de cobertura publicado na revista MIX
# Sustentavel (2020), que a aba de Documentacao cita. A interface, a documentacao
# embutida e o manual precisam trazer exatamente estes numeros, e um teste
# confere: antes o manual mostrava faixas sem fonte (ceramica de 0,80 a 0,90)
# enquanto a lista do programa aplicava 0,75.
COEFICIENTES_POR_MATERIAL = (
    ("Telha Cerâmica", 0.75),
    ("Telha Metálica", 0.88),
    ("Telha de Cimento / Fibrocimento", 0.73),
    ("Telhados verdes", 0.24),
    ("Alumínio", 0.70),
    ("Plástico / Policarbonato", 0.94),
    ("Concreto Asfáltico", 0.90),
    ("Aço Galvanizado", 0.92),
)

FONTE_DOS_COEFICIENTES_POR_MATERIAL = (
    "ESTUDO sobre materiais para coberturas utilizadas em sistemas de "
    "aproveitamento de água pluvial residenciais. MIX Sustentável, v. 6, n. 2, "
    "p. 53-66, 2020. DOI 10.29183/2447-3073.MIX2020.v6.n2.53-66."
)
