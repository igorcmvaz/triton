"""A categoria tarifária que cada tipologia de edificação exigiria.

O programa oferece oito tipologias de edificação e cada uma ajusta o consumo per
capita e a fração não potável. Isso funciona: a demanda muda e atravessa o
programa.

O catálogo tarifário, porém, tem **uma só categoria**: «Residencial normal», nos
652 municípios. Um estudo de hospital ou de escola sai com a demanda certa e a
**tarifa errada**, e a diferença não é pequena — na Tabela Tarifária CASAN
04/2026 a primeira faixa custa R$ 3,08/m³ no residencial e R$ 6,81/m³ no
comercial, no industrial e no público, mais que o dobro. A taxa fixa de
disponibilidade é a mesma R$ 46,34 em todas.

Como a economia de água é avaliada pela tarifa, **subestimar a tarifa subestima a
economia na mesma proporção**: um estudo de escola com tarifa residencial mostra
menos da metade do retorno que o projeto teria.

Não dá para corrigir o dado aqui: as outras categorias não foram coletadas para
os 652 municípios, e inventá-las seria pior que a lacuna. Dá para tornar a
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

#: Razão entre a tarifa da categoria e a residencial na primeira faixa, medida na
#: Tabela Tarifária CASAN 04/2026 (R$ 6,81 comercial contra R$ 3,08 residencial).
#: Serve para dimensionar o aviso, não para corrigir conta nenhuma: a proporção
#: varia entre concessionárias, e o programa não a aplica a lugar algum.
RAZAO_DE_REFERENCIA_CASAN = 6.81 / 3.08


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

    tipologia = NOME_DA_TIPOLOGIA.get(str(template_id), str(template_id))
    categoria = categoria_exigida(template_id)
    return (
        f"A tipologia escolhida é «{tipologia}», que a concessionária fatura na "
        f"categoria {categoria}. O catálogo do programa tem apenas a categoria "
        f"{CATEGORIA_COLETADA}, de modo que a conta de água está sendo calculada "
        f"com a tarifa errada.\n\n"
        f"O erro tem sentido conhecido: as categorias não residenciais são mais "
        f"caras, e portanto a economia e o retorno estão SUBESTIMADOS. Na Tabela "
        f"Tarifária CASAN 04/2026 a primeira faixa custa R$ 6,81/m³ no comercial "
        f"contra R$ 3,08/m³ no residencial — mais que o dobro.\n\n"
        f"Para um estudo publicável, lance a estrutura da categoria {categoria} "
        f"da sua concessionária no modo Personalizado do diálogo de tarifas."
    )
