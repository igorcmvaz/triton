"""Cadeia única da cloração: dose, produto e emissão.

Até a versão 5.0.7 o programa tinha **duas** contas de cloro, em bases
diferentes, que nunca poderiam concordar:

| | `environmental.py` | `water_quality.py` |
| :--- | :--- | :--- |
| Dose | 2,0 mg/L | 1,5 mg/L |
| Base do fator | por kg de **Cl₂ puro** | por kg de **produto** (pastilha) |
| Pureza | não considerada | 65% de cloro ativo |
| Fator | 25,0 kg CO₂e/kg | 1,85 kg CO₂e/kg |
| Resultado | 0,0500 kg CO₂e/m³ | 0,0043 kg CO₂e/m³ |

Onze vezes e meia de diferença, dentro do mesmo programa, para a mesma água.

Dois problemas distintos estavam somados:

1. **O fator de 25,0 não tinha fonte, e é implausível.** Cloro de rota
   cloro-álcali fica tipicamente entre 1 e 2 kg CO₂e/kg. O número 25,0 é
   idêntico a ``chlorine_cost_per_kg = 25.00`` (R$/kg) em
   ``costs_database.json`` — quase certamente o custo copiado para o campo de
   emissão. Foi descartado.
2. **As bases eram incomparáveis.** Um fator "por kg de Cl₂" e outro "por kg de
   pastilha a 65%" diferem por 1/0,65 mesmo que o processo fosse o mesmo.
   Nenhum código dizia qual era qual.

Aqui a conta é uma só, e explícita:

    massa de produto por m³ = (dose em mg Cl₂/L ÷ 1000) ÷ pureza
    emissão por m³          = massa de produto × fator por kg de produto

A pureza aparece na fórmula justamente para que ninguém volte a somar um fator
de produto com uma dose de cloro ativo.
"""

from __future__ import annotations

from dataclasses import dataclass

# Dose de cloro ativo. A NBR 15527 trabalha com residual livre entre 0,5 e
# 2,0 mg/L; adota-se o meio da faixa, que é o valor com que o módulo de
# qualidade já dimensionava o dosador real.
DOSE_PADRAO_MG_POR_LITRO = 1.5

# Hipoclorito de cálcio em pastilha, teor comercial corrente de cloro ativo.
PUREZA_PADRAO = 0.65

# kg CO₂e por kg de **produto** (pastilha), não por kg de cloro ativo.
FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO = 1.85

FONTE_DO_FATOR = (
    "Hipoclorito de cálcio, inventário Ecoinvent v3.8. O processo e a versão "
    "exata ainda precisam ser registrados: a atribuição herdada do módulo de "
    "qualidade nomeia a base mas não o dataset."
)


@dataclass(frozen=True)
class Cloracao:
    """Parâmetros da cloração, numa base só.

    ``dose_mg_por_litro`` é de **cloro ativo**; ``fator_kg_co2e_por_kg_produto``
    é por quilo de **produto comercial**. A pureza faz a ponte entre os dois, e
    é por isso que ela é obrigatória aqui.
    """

    dose_mg_por_litro: float = DOSE_PADRAO_MG_POR_LITRO
    pureza: float = PUREZA_PADRAO
    fator_kg_co2e_por_kg_produto: float = FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO

    def __post_init__(self) -> None:
        if self.dose_mg_por_litro < 0:
            raise ValueError("A dose não pode ser negativa.")
        if not 0.0 < self.pureza <= 1.0:
            raise ValueError(
                f"Pureza deve ficar em (0, 1]; recebido {self.pureza}. "
                "Use 0,65 para pastilha a 65% de cloro ativo, não 65."
            )
        if self.fator_kg_co2e_por_kg_produto < 0:
            raise ValueError("O fator de emissão não pode ser negativo.")

    @property
    def cloro_ativo_kg_por_m3(self) -> float:
        """Massa de cloro ativo por m³ tratado."""
        return self.dose_mg_por_litro / 1000.0

    @property
    def produto_kg_por_m3(self) -> float:
        """Massa de **produto comercial** por m³, já corrigida pela pureza."""
        return self.cloro_ativo_kg_por_m3 / self.pureza

    @property
    def co2e_kg_por_m3(self) -> float:
        """Emissão da cloração por m³ tratado, em kg CO₂e/m³."""
        return self.produto_kg_por_m3 * self.fator_kg_co2e_por_kg_produto

    def massa_anual_de_produto_kg(self, volume_anual_m3: float) -> float:
        return max(0.0, volume_anual_m3) * self.produto_kg_por_m3

    def co2e_anual_kg(self, volume_anual_m3: float) -> float:
        return max(0.0, volume_anual_m3) * self.co2e_kg_por_m3


def cloracao_padrao() -> Cloracao:
    return Cloracao()
