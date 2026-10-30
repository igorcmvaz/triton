"""Arranjo de abastecimento: como a água sai da cisterna e chega aos pontos de uso.

Até a revisão de setembro de 2026 nenhum módulo sabia disso. O econômico só
cobrava energia com caixa superior; a ACV contava caixa superior por padrão e,
sem kWh informado, cobrava bombeamento de todo o volume pluvial; e a cloração da
ACV sumia ao desmarcar a caixa. Este módulo é o lugar único da resposta, e os
três consumidores — econômico, ACV e relatórios — a leem daqui.

"""

from __future__ import annotations

#: Cisterna embaixo, motobomba enche a caixa superior, que abastece por gravidade.
RECALQUE = "recalque"
#: Pressurizador ligado à cisterna, acionado por pressostato a cada uso.
PRESSURIZACAO = "pressurizacao"
#: Cisterna acima dos pontos de uso; não há bomba.
GRAVIDADE = "gravidade"
#: Projeto antigo sem caixa superior, gravado antes de o arranjo existir.
NAO_INFORMADO = "nao_informado"

ARRANJOS = (RECALQUE, PRESSURIZACAO, GRAVIDADE)

ROTULOS = {
    RECALQUE: "Recalque para caixa superior",
    PRESSURIZACAO: "Pressurização direta",
    GRAVIDADE: "Gravidade, sem bomba",
    NAO_INFORMADO: "Não informado",
}

#: Pressão de trabalho do pressurizador, em m.c.a.: a média da faixa do
#: pressostato do Komeco TP 820 (1/4 CV), que liga a 12 e desliga a 24 m.c.a.
#: (manual do fabricante, ficha técnica). Abaixo do limite de 40 m.c.a. de
#: pressão estática nos pontos de utilização da ABNT NBR 5626:2020, item 6.9.4.
PRESSAO_DE_TRABALHO_PADRAO_M = 18.0

#: Usos por pessoa por dia que acionam o pressurizador nos usos não potáveis:
#: 5,05 descargas e 0,37 ciclos de máquina de lavar (Mayer, DeOreo et al., 1999,
#: Residential End Uses of Water, AWWARF, seção «Fixture Utilization»). O padrão
#: conta só as descargas: a lavagem de roupa está fora dos usos do item 4.1.7 da
#: ABNT NBR 15527:2019. Quem a incluir soma os 0,37 ciclos.
DESCARGAS_POR_PESSOA_DIA = 5.05
ACIONAMENTOS_POR_PESSOA_DIA = DESCARGAS_POR_PESSOA_DIA


def arranjo_de(config) -> str:
    """O arranjo declarado no projeto, ou o que se deduz de um arquivo antigo.

    Arquivo com caixa superior vira recalque, com os mesmos números de antes.
    Arquivo sem caixa vira «não informado»: o programa não adivinha se há
    pressurizador ou gravidade, e a interface pede a escolha.
    """
    declarado = str(getattr(config, "supply_arrangement", "") or "").strip()
    if declarado in ARRANJOS:
        return declarado
    return RECALQUE if bool(getattr(config, "upper_tank_used", True)) else NAO_INFORMADO


def usa_caixa_superior(arranjo: str) -> bool:
    return arranjo == RECALQUE


def usa_bomba(arranjo: str) -> bool:
    return arranjo in (RECALQUE, PRESSURIZACAO)
