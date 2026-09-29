"""Certificação EDGE (IFC / Banco Mundial): a barra de água e o que o Netuno informa.

O EDGE **não pontua**. Diferentemente do LEED, do AQUA-HQE e do Selo Casa Azul,
que somam pontos por crédito atendido, o EDGE mede **percentual de economia
contra um caso-base local** em três barras independentes — energia, água e
energia incorporada nos materiais — e exige que cada uma cruze um limiar.

Níveis, conforme o processo de certificação publicado pelo IFC:

| Nível | Exigência |
| :--- | :--- |
| EDGE Certified | ≥ 20% de economia em energia, água **e** energia incorporada nos materiais |
| EDGE Advanced (Zero Carbon Ready) | o anterior, mais ≥ 40% de economia de energia no local |
| Zero Carbon | o anterior, mais 100% de energia renovável (local ou fora do local) ou compensação |

Fonte: <https://edgebuildings.com/certify/certification/>, consultado em
10 de setembro de 2026. O EDGE é uma criação do IFC, do Grupo Banco Mundial, e a
certificação é administrada pelo GBCI em mais de 120 países.

O que o Netuno pode e o que não pode dizer
------------------------------------------
O Netuno simula **uma** medida de água: a WEM14, sistema de aproveitamento de
água pluvial. Ele calcula, dia a dia, quanto de água potável a chuva substitui —
que é exatamente o numerador da barra de água do EDGE.

O que ele **não** sabe é o caso-base do aplicativo EDGE. O caso-base é local:
varia por país e por tipo de edificação, e é fixado pelo próprio aplicativo a
partir de referências do mercado local. Por isso este módulo aceita o consumo de
base declarado pelo usuário e, quando ele não é declarado, usa a demanda
modelada do próprio projeto — dizendo que foi isso que fez.

As duas coincidem quando a única medida de água do projeto é o sistema pluvial.
Se o projeto também tiver louças e metais eficientes, o caso-base do EDGE é
**maior** que a demanda modelada, e a contribuição da WEM14 medida contra ele é
percentualmente **menor** — embora a barra total seja maior. Nesse caso o número
daqui é um piso, não o valor da certificação.

**A certificação sai do aplicativo EDGE, não daqui.** O que este módulo entrega
é a contribuição da WEM14 e a área de captação a declarar no campo dela.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

# ── limiares, conforme o processo publicado ───────────────────────────────────
LIMIAR_DE_AGUA_PCT = 20.0
LIMIAR_DE_ENERGIA_PCT = 20.0
LIMIAR_DE_MATERIAIS_PCT = 20.0
LIMIAR_DE_ENERGIA_AVANCADO_PCT = 40.0

FONTE_DOS_LIMIARES = (
    "IFC — EDGE Certification Process, edgebuildings.com/certify/certification/, "
    "consultado em 10/09/2026"
)

NIVEIS = (
    ("EDGE Certified",
     "≥ 20% em energia, água e energia incorporada nos materiais"),
    ("EDGE Advanced (Zero Carbon Ready)",
     "EDGE Certified, mais ≥ 40% de economia de energia no local"),
    ("Zero Carbon",
     "EDGE Advanced, mais 100% de renovável ou compensação"),
)


@dataclass(frozen=True)
class MedidaDeAgua:
    """Uma medida de eficiência hídrica do EDGE, na codificação WEM."""

    codigo: str
    nome: str
    modelada_pelo_netuno: bool
    observacao: str


# Códigos conferidos contra um relatório de avaliação EDGE v3.0.0 emitido para
# projeto residencial certificado (BluHomes Katmon, Filipinas, certificadora
# Philippine Green Building Initiative, ficha 21110410124226). Os valores de
# caso-base de cada medida são locais e não se repetem entre países, por isso não
# são reproduzidos aqui.
MEDIDAS_DE_AGUA = (
    MedidaDeAgua("WEM13", "Sistema eficiente de irrigação paisagística", False,
                 "O Netuno modela o volume de irrigação e a supressão por chuva, "
                 "não a eficiência do sistema de rega."),
    MedidaDeAgua("WEM14", "Sistema de aproveitamento de água pluvial", True,
                 "É a medida que este programa dimensiona. A entrada do EDGE é a "
                 "área de captação em m²."),
    MedidaDeAgua("WEM15", "Tratamento e reúso de águas servidas", False,
                 "Fora do escopo: o Netuno trata água de chuva, não água cinza."),
)


@dataclass
class AvaliacaoEdge:
    """O que o Netuno tem a dizer sobre a barra de água do EDGE."""

    economia_de_agua_pct: float
    atende_o_padrao_de_agua: bool
    margem_pct: float                    # positiva sobra, negativa falta
    consumo_base_anual_m3: float
    volume_pluvial_anual_m3: float
    base_declarada_pelo_usuario: bool
    area_de_captacao_m2: float
    nivel_alcancavel: str
    descricao: str
    ressalva: str
    medidas: List[MedidaDeAgua] = field(default_factory=list)


def consumo_base_anual_m3(
    litros_por_pessoa_dia: float,
    pessoas: float,
    dias: int = 365,
) -> float:
    """Converte o caso-base do EDGE, em L/pessoa·dia, para m³/ano."""
    return max(0.0, float(litros_por_pessoa_dia) * float(pessoas) * int(dias) / 1000.0)


def avaliar_agua_edge(
    volume_pluvial_anual_m3: float,
    demanda_total_anual_m3: float,
    area_de_captacao_m2: float,
    consumo_base_anual_m3_declarado: Optional[float] = None,
) -> AvaliacaoEdge:
    """Contribuição do sistema pluvial para a barra de água do EDGE.

    `demanda_total_anual_m3` é a demanda modelada do projeto, usada como
    caso-base quando o usuário não declara o do aplicativo EDGE.
    """
    pluvial = max(0.0, float(volume_pluvial_anual_m3))
    declarada = (
        consumo_base_anual_m3_declarado is not None
        and float(consumo_base_anual_m3_declarado) > 0.0
    )
    base = float(consumo_base_anual_m3_declarado) if declarada else max(0.0, float(demanda_total_anual_m3))

    pct = (pluvial / base * 100.0) if base > 0.0 else 0.0
    pct = max(0.0, min(100.0, pct))
    atende = pct >= LIMIAR_DE_AGUA_PCT
    margem = pct - LIMIAR_DE_AGUA_PCT

    if atende:
        nivel = (
            "Barra de água atendida. O nível depende também de energia e materiais."
        )
        descricao = (
            f"O sistema pluvial substitui {pct:.1f}% do consumo de base, "
            f"acima do limiar de {LIMIAR_DE_AGUA_PCT:.0f}% do EDGE. "
            f"Só a medida WEM14 já leva a barra de água ao padrão, com "
            f"{margem:.1f} pontos percentuais de folga."
        )
    else:
        nivel = "Barra de água ainda não atendida só com a água pluvial."
        falta_m3 = max(0.0, base * LIMIAR_DE_AGUA_PCT / 100.0 - pluvial)
        descricao = (
            f"O sistema pluvial substitui {pct:.1f}% do consumo de base, "
            f"abaixo do limiar de {LIMIAR_DE_AGUA_PCT:.0f}%. Faltam "
            f"{abs(margem):.1f} pontos percentuais, ou {falta_m3:,.0f} m³/ano, "
            f"que outras medidas de água do EDGE podem cobrir — louças e metais "
            f"eficientes somam na mesma barra."
        )

    if declarada:
        ressalva = (
            "Consumo de base declarado pelo usuário. Confira que é o mesmo "
            "caso-base que o aplicativo EDGE adota para este país e tipologia."
        )
    else:
        ressalva = (
            "Sem caso-base declarado, usou-se a demanda modelada do projeto "
            f"({base:,.0f} m³/ano). O caso-base do EDGE é local e fixado pelo "
            "aplicativo; se o projeto tiver louças e metais eficientes, o "
            "caso-base é maior e este percentual é um piso."
        )

    return AvaliacaoEdge(
        economia_de_agua_pct=pct,
        atende_o_padrao_de_agua=atende,
        margem_pct=margem,
        consumo_base_anual_m3=base,
        volume_pluvial_anual_m3=pluvial,
        base_declarada_pelo_usuario=declarada,
        area_de_captacao_m2=max(0.0, float(area_de_captacao_m2)),
        nivel_alcancavel=nivel,
        descricao=descricao,
        ressalva=ressalva,
        medidas=list(MEDIDAS_DE_AGUA),
    )


def regra_da_barra_de_agua() -> str:
    """A regra, em uma linha, para exibir ao lado do resultado."""
    return (
        f"Barra de água ≥ {LIMIAR_DE_AGUA_PCT:.0f}% contra o caso-base local. "
        f"O EDGE não atribui pontos: mede percentual e compara com o limiar."
    )
