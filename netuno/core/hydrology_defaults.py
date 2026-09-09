"""Padrões hidrológicos com fonte declarada.

O coeficiente de escoamento estava com **quatro** valores de recurso diferentes
espalhados pelo programa — 0,75 na interface e no gerador de relatório, 0,85 no
exportador CAD, 0,90 no motor de simulação e na leitura de planilha. Como cada
caminho de entrada pegava um deles, o mesmo projeto podia render captações
diferentes conforme fosse aberto por arquivo, por planilha ou pela interface.

Aqui existe um valor só, com a razão de ser dele escrita ao lado.
"""

from __future__ import annotations

# ABNT NBR 15527:2019, item 4.1.6, dá a disponibilidade anual, mensal ou diária
# por ``V_disp = P x A x C x eta``, e recomenda **eta = 0,85** na falta de dados,
# sendo eta a eficiência do sistema de captação.
#
# Este programa trabalha com um coeficiente único, que absorve tanto o
# escoamento superficial da cobertura (C) quanto a eficiência de captação
# (eta). Quando o usuário escolhe o material do telhado, o coeficiente vem da
# tabela de materiais; este valor é o de recurso, para quando não há escolha.
COEFICIENTE_DE_ESCOAMENTO_PADRAO = 0.85

FONTE_DO_COEFICIENTE = (
    "ABNT NBR 15527:2019, item 4.1.6: na falta de dados, recomenda-se o fator "
    "de captação de 0,85."
)
