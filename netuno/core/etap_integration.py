"""A linha de tratamento deixa de ser uma ilha.

Até a versão 5.0.7 a estação de tratamento de água pluvial (ETAP) era
dimensionada apenas pela aba de Qualidade da Água, que exibia investimento,
custo operacional e emissão — e não os entregava a ninguém. Escolher
ultravioleta na interface não alterava payback, valor presente líquido nem
emissão anual, embora o reator responda por até 69% do investimento e por mais
emissão operacional que o sistema inteiro.

Este módulo é o ponto único onde a ETAP é dimensionada a partir da configuração
do projeto. O econômico e a ACV passam a chamá-lo, de modo que a escolha feita
na interface percorre o programa em vez de ficar guardada.

Duas regras de contagem, que são a razão de o acoplamento não ser uma soma
simples:

1. **A cloração é contada uma vez.** O econômico já custeia o hipoclorito e a
   ACV já emite por ele. O que a ETAP acrescenta é o resto da linha — filtro de
   entrada, reator ultravioleta ou ozonizador, filtro de polimento. Por isso
   existem `opex_anual_sem_cloro` e `co2e_anual_sem_cloro`.
2. **A dose, a pureza e o preço vêm da configuração**, não de valores fixos no
   dimensionamento. Sem isso a mesma cloração aparecia com dois preços na mesma
   tela.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from netuno.core.chlorination import (
    DOSE_PADRAO_MG_POR_LITRO,
    FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO,
    PUREZA_PADRAO,
    Cloracao,
)
from netuno.core.water_quality import EtapSizingResult, size_etap

#: Volume pluvial anual de recurso, em m³, quando não há simulação carregada.
#: É a ordem de grandeza de uma residência unifamiliar de quatro pessoas com
#: cobertura de 100 m² em clima subtropical úmido, e existe apenas para que a
#: interface tenha o que mostrar antes de o usuário rodar a simulação.
VOLUME_PLUVIAL_DE_RECURSO_M3 = 120.0

#: Área de cobertura de recurso, em m², coerente com o volume acima.
AREA_DE_RECURSO_M2 = 100.0


def volume_pluvial_anual_m3(config: Any = None, sim_result: Any = None) -> float:
    """Resolve o volume pluvial anual efetivamente consumido, em m³.

    A precedência importa: o resultado da simulação é medido, a configuração é
    declarada, e o valor de recurso é apenas um marcador de ordem de grandeza.

    A aba de Qualidade da Água pedia `annual_pluvial_consumed_m3` à
    configuração, e esse atributo não existe em `NetunoConfig` — é propriedade
    do resultado da simulação. O `getattr` devolvia sempre o valor de recurso,
    de modo que a ETAP era dimensionada para 120 m³/ano qualquer que fosse o
    projeto.
    """
    for fonte in (sim_result, config):
        if fonte is None:
            continue
        for nome in ("annual_pluvial_consumed_m3", "annual_water_saved_m3"):
            valor = getattr(fonte, nome, None)
            if valor is None:
                continue
            try:
                valor = float(valor)
            except (TypeError, ValueError):
                continue
            if valor > 0:
                return valor
    return VOLUME_PLUVIAL_DE_RECURSO_M3


def area_de_captacao_m2(config: Any = None) -> float:
    """Área de cobertura que dimensiona o filtro de entrada da ETAP."""
    for nome in ("roof_area_m2", "area", "catchment_area_m2"):
        valor = getattr(config, nome, None) if config is not None else None
        if valor is None:
            continue
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            continue
        if valor > 0:
            return valor
    return AREA_DE_RECURSO_M2


@dataclass(frozen=True)
class EtapDoProjeto:
    """A ETAP dimensionada, mais as parcelas que evitam contagem dupla.

    `capex` e `opex_anual` são os totais, para exibição. O econômico e a ACV
    consomem as versões `_sem_cloro`, porque já contam o hipoclorito por conta
    própria.
    """

    resultado: EtapSizingResult
    capex: float
    opex_anual: float
    co2e_anual: float
    opex_anual_sem_cloro: float
    co2e_anual_sem_cloro: float
    volume_pluvial_m3: float
    custo_anual_do_cloro: float
    co2e_anual_do_cloro: float
    first_flush_capex: float = 0.0
    first_flush_volume_l: float = 0.0
    first_flush_embodied_co2_kg: float = 0.0

    @property
    def metodo(self) -> str:
        return self.resultado.disinfection_method

    @property
    def estagios(self) -> list:
        return list(self.resultado.disinfection_stages)


def dimensionar_etap_do_projeto(
    config: Any = None,
    annual_pluvial_m3: Optional[float] = None,
    sim_result: Any = None,
    regional_factor: float = 1.0,
) -> EtapDoProjeto:
    """Dimensiona a ETAP a partir da configuração do projeto.

    Aceita tanto `NetunoConfig` quanto `EnvironmentalConfig`: os dois carregam
    os mesmos três campos de escolha, e o que faltar cai no padrão declarado.
    """
    volume = (
        float(annual_pluvial_m3)
        if annual_pluvial_m3 is not None and float(annual_pluvial_m3) > 0
        else volume_pluvial_anual_m3(config, sim_result)
    )

    classe = str(getattr(config, "water_quality_target_class", "classe_1") or "classe_1")
    metodo = str(getattr(config, "water_quality_disinfection", "cloro") or "cloro")
    polimento = bool(getattr(config, "water_quality_polishing", False))
    discard = float(getattr(config, "discard", 0.0) or 0.0)
    include_ff = bool(getattr(config, "first_flush_system_enabled", False))

    dose = float(getattr(config, "chlorine_dose_mg_l", DOSE_PADRAO_MG_POR_LITRO) or DOSE_PADRAO_MG_POR_LITRO)
    pureza = float(getattr(config, "chlorine_product_purity", PUREZA_PADRAO) or PUREZA_PADRAO)
    preco = float(getattr(config, "chlorine_cost_per_kg", 25.0) or 25.0)
    fator_cloro = float(
        getattr(config, "chlorine_co2_kg_per_kg", FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO)
        or FATOR_PADRAO_KG_CO2E_POR_KG_PRODUTO
    )
    fator_rede = getattr(config, "grid_co2_factor_kg_kwh", None)

    resultado = size_etap(
        target_class_id=classe,
        annual_pluvial_consumed_m3=volume,
        roof_area_m2=area_de_captacao_m2(config),
        disinfection_choice=metodo,
        include_polishing_filter=polimento,
        chlorine_dose_mg_l=dose,
        chlorine_product_purity=pureza,
        chlorine_kg_price_brl=preco,
        chlorine_co2_kg_per_kg=fator_cloro,
        regional_factor=regional_factor,
        grid_co2_factor_kg_kwh=float(fator_rede) if fator_rede else None,
        discard_mm=discard,
        include_first_flush=include_ff,
    )

    # A parcela da cloração, que os dois módulos já contabilizam por si.
    cloracao = Cloracao(
        dose_mg_por_litro=max(0.0, dose),
        pureza=max(1e-6, pureza),
        fator_kg_co2e_por_kg_produto=max(0.0, fator_cloro),
    )
    custo_cloro = cloracao.massa_anual_de_produto_kg(volume) * preco
    co2e_cloro = cloracao.co2e_anual_kg(volume)

    return EtapDoProjeto(
        resultado=resultado,
        capex=resultado.total_etap_capex,
        opex_anual=resultado.total_etap_annual_opex,
        co2e_anual=resultado.total_etap_co2e_kg_yr,
        opex_anual_sem_cloro=max(0.0, resultado.total_etap_annual_opex - custo_cloro),
        co2e_anual_sem_cloro=max(0.0, resultado.total_etap_co2e_kg_yr - co2e_cloro),
        volume_pluvial_m3=volume,
        custo_anual_do_cloro=custo_cloro,
        co2e_anual_do_cloro=co2e_cloro,
        first_flush_capex=resultado.first_flush_capex,
        first_flush_volume_l=resultado.first_flush_diverter_vol_l,
        first_flush_embodied_co2_kg=resultado.first_flush_embodied_co2_kg,
    )


def capex_incremental_da_etap(
    config: Any = None,
    annual_pluvial_m3: Optional[float] = None,
    sim_result: Any = None,
) -> float:
    """Investimento da linha de tratamento que ainda NÃO está no CAPEX.

    O estimador de custos já embute em «Acessórios» uma verba de filtração e
    tratamento — R$ 350 na casa unifamiliar térrea, R$ 2.100 na tipologia
    industrial. A linha dimensionada substitui essa verba, de modo que só a
    diferença é investimento novo. Somar o total contaria o filtro duas vezes.

    O desconto só se aplica quando há acessórios orçados: sem eles não existe
    verba a deslocar.

    Esta é a definição única da regra. O módulo econômico e a aba econômica
    integrada a consomem, em vez de cada um somar por conta própria.
    """
    if not bool(getattr(config, "etap_enabled", True)):
        return 0.0

    # Importado aqui para não criar ciclo: `cost_estimates` não depende deste
    # módulo, mas o econômico depende dos dois.
    from netuno.core.cost_estimates import verba_generica_de_tratamento_brl

    etap = dimensionar_etap_do_projeto(config, annual_pluvial_m3, sim_result)
    verba = verba_generica_de_tratamento_brl(getattr(config, "building_typology", "UTI"))
    deslocavel = verba if float(getattr(config, "cost_accessories", 0.0) or 0.0) > 0 else 0.0
    return max(0.0, etap.capex - deslocavel)


def opex_anual_incremental_da_etap(
    config: Any = None,
    annual_pluvial_m3: Optional[float] = None,
    sim_result: Any = None,
) -> float:
    """Custeio anual da linha de tratamento que ainda NÃO está no fluxo de caixa.

    Os dois motores econômicos já custeiam o hipoclorito por uma linha própria.
    O que a ETAP acrescenta é o resto: lâmpada germicida, energia do reator,
    refil do filtro de polimento.
    """
    if not bool(getattr(config, "etap_enabled", True)):
        return 0.0
    return dimensionar_etap_do_projeto(config, annual_pluvial_m3, sim_result).opex_anual_sem_cloro
