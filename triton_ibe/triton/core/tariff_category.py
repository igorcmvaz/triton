"""A categoria tarifária que cada tipologia de edificação exigiria.

O programa oferece oito tipologias de edificação e cada uma ajusta o consumo per
capita e a fração não potável. Isso funciona: a demanda muda e atravessa o
programa.

O catálogo tarifário tem a categoria «Residencial normal» nos 652 municípios; as
demais só onde a tabela oficial do prestador foi coletada. Um estudo de hospital ou de escola sai com a demanda certa e a
**tarifa errada**, e a diferença não é pequena — na Tabela Tarifária CASAN
04/2026 a primeira faixa custa R$ 3,08/m³ no residencial e R$ 6,81/m³ no
comercial, no industrial e no público, mais que o dobro. A taxa fixa de
disponibilidade é a mesma R$ 46,34 em todas.

Como a economia de água é avaliada pela tarifa, **subestimar a tarifa subestima a
economia na mesma proporção**: um estudo de escola com tarifa residencial mostra
menos da metade do retorno que o projeto teria.

Não dá para corrigir o dado aqui: onde a categoria não foi coletada, inventá-la
(multiplicando a residencial, como o programa fazia antes da 0.1.0) seria pior que a lacuna. Dá para tornar a
incompatibilidade **visível**, que é o que impede o estudo errado de sair calado.

Este módulo é o mapa entre as duas coisas, e a função que diz quando elas não
combinam.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

#: Categoria do catálogo tarifário efetivamente coletada para os 652 municípios.
CATEGORIA_COLETADA = "Residencial normal"

#: Categoria tarifária que cada tipologia de edificação exigiria. Os rótulos
#: seguem os das tabelas das concessionárias.
CATEGORIA_POR_TIPOLOGIA: Dict[str, str] = {
    "res_medio": "Residencial",
    "res_popular": "Residencial",
    "res_alto": "Residencial",
    "res_multi": "Residencial",
    "comercial": "Comercial",
    "escola": "Pública",
    "hotel": "Comercial",
    "hospital": "Pública",
}

#: Da categoria exigida para o identificador de CATEGORIAS_TARIFARIAS.
ID_DA_CATEGORIA: Dict[str, str] = {
    "Residencial": "residencial", "Comercial": "comercial",
    "Industrial": "industrial", "Pública": "publica",
}

NOME_DA_CATEGORIA: Dict[str, str] = {
    "residencial": CATEGORIA_COLETADA, "comercial": "Comercial",
    "industrial": "Industrial", "publica": "Pública", "social": "Social",
}

#: Nome legível de cada tipologia, para a mensagem de aviso.
NOME_DA_TIPOLOGIA: Dict[str, str] = {
    "res_medio": "Residencial Unifamiliar — Padrão Médio",
    "res_popular": "Residencial Unifamiliar — Econômico",
    "res_alto": "Residencial Unifamiliar — Alto Padrão",
    "res_multi": "Edifício Residencial Multifamiliar",
    "comercial": "Comercial / Escritórios",
    "escola": "Escola / Creche",
    "hotel": "Hotel / Pousada",
    "hospital": "Hospital / Clínica",
}


def categoria_exigida(template_id: Optional[str]) -> str:
    """Categoria tarifária que a tipologia escolhida exigiria."""
    return CATEGORIA_POR_TIPOLOGIA.get(str(template_id or "res_medio"), "Residencial")


def e_residencial(template_id: Optional[str]) -> bool:
    """A tipologia é atendida pela categoria que o catálogo tem?"""
    return categoria_exigida(template_id) == "Residencial"


def incompatibilidade_de_categoria(config: Any) -> Optional[str]:
    """Mensagem quando a tipologia escolhida não é a que o catálogo cobre.

    Devolve ``None`` quando não há incompatibilidade. A mensagem diz o que está
    errado, o sentido do erro e o que fazer — as três coisas de que o projetista
    precisa para não publicar um resultado que não se sustenta.
    """
    template_id = getattr(config, "building_template_id", "res_medio")
    if e_residencial(template_id):
        return None
    # Na International Edition não há catálogo: a tarifa é digitada pelo usuário,
    # que lança a da categoria certa. O aviso falaria de um catálogo que não existe.
    from triton.core.edition import usa_dados_do_brasil
    if not usa_dados_do_brasil():
        return None

    tipologia = NOME_DA_TIPOLOGIA.get(str(template_id), str(template_id))
    categoria = categoria_exigida(template_id)
    # A tarifa aplicada já é da categoria certa, coletada ou digitada pelo usuário.
    aplicada = str(getattr(config, "tariff_category", "residencial") or "residencial")
    if aplicada == "personalizada" or ID_DA_CATEGORIA.get(categoria) == aplicada:
        return None
    return (
        f"A tipologia escolhida é «{tipologia}», que a concessionária fatura na "
        f"categoria {categoria}, mas a tarifa aplicada ao projeto é a da categoria "
        f"{NOME_DA_CATEGORIA.get(aplicada, aplicada)}: a conta de água está sendo calculada com a tarifa "
        f"errada.\n\n"
        f"O erro tem sentido conhecido: as categorias não residenciais são mais "
        f"caras, e portanto a economia e o retorno estão SUBESTIMADOS. Na Tabela "
        f"Tarifária CASAN 04/2026 a primeira faixa custa R$ 6,81/m³ no comercial "
        f"contra R$ 3,08/m³ no residencial — mais que o dobro.\n\n"
        f"Escolha a categoria {categoria} no diálogo de tarifas, se a tabela dela "
        f"já foi coletada para o município, ou lance a estrutura da sua "
        f"concessionária no modo Personalizado."
    )
