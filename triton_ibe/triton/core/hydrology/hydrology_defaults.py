"""Padrões hidrológicos e coeficientes de escoamento superficial com fontes normativas e bibliográficas."""

from __future__ import annotations

#: Coeficiente de escoamento padrão adotado para telha cerâmica (NBR 15527:2019 e MIX Sustentável 2020).
COEFICIENTE_DE_ESCOAMENTO_PADRAO = 0.75

#: Lâmina de descarte da primeira chuva padrão (ABNT NBR 15527:2019, item 4.1.5).
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

#: Coeficientes de escoamento por material da cobertura (MIX Sustentável, 2020).
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
