"""Arranjo de abastecimento: tipologia de distribuição de água pluvial aos pontos de uso.

Define as configurações hidráulicas suportadas pelo Triton (recalque, pressurização direta e gravidade)
e unifica o comportamento para cálculo de custos de bombeamento, análise de ciclo de vida (ACV) e relatórios.
"""

from __future__ import annotations

#: Cisterna embaixo, motobomba enche a caixa superior, que abastece por gravidade.
RECALQUE = "recalque"
#: Pressurizador ligado à cisterna, acionado por pressostato a cada uso.
PRESSURIZACAO = "pressurizacao"
#: Cisterna acima dos pontos de uso; não há bomba.
GRAVIDADE = "gravidade"
#: Projeto sem caixa superior e sem arranjo informado previamente.
NAO_INFORMADO = "nao_informado"

ARRANJOS = (RECALQUE, PRESSURIZACAO, GRAVIDADE)

ROTULOS = {
    RECALQUE: "Recalque para caixa superior",
    PRESSURIZACAO: "Pressurização direta",
    GRAVIDADE: "Gravidade, sem bomba",
    NAO_INFORMADO: "Não informado",
}

#: Pressão de trabalho do pressurizador, em m.c.a. (Komeco TP 820, média de 18 m.c.a., NBR 5626:2020 item 6.9.4).
PRESSAO_DE_TRABALHO_PADRAO_M = 18.0

#: Usos por pessoa por dia que acionam o pressurizador (Mayer et al., 1999, AWWARF, ABNT NBR 15527:2019 item 4.1.7).
DESCARGAS_POR_PESSOA_DIA = 5.05
ACIONAMENTOS_POR_PESSOA_DIA = DESCARGAS_POR_PESSOA_DIA


def arranjo_de(config) -> str:
    """O arranjo declarado no projeto, com fallback seguro para projetos herdados."""
    declarado = str(getattr(config, "supply_arrangement", "") or "").strip()
    if declarado in ARRANJOS:
        return declarado
    return RECALQUE if bool(getattr(config, "upper_tank_used", True)) else NAO_INFORMADO


def usa_caixa_superior(arranjo: str) -> bool:
    return arranjo == RECALQUE


def usa_bomba(arranjo: str) -> bool:
    return arranjo in (RECALQUE, PRESSURIZACAO)
