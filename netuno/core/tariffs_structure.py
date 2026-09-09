"""
Formalização da estrutura tarifária: códigos, famílias e validação.

O catálogo do Netuno representa cada tarifa como uma lista de quádruplas
``(minimo_m3, maximo_m3, valor, codigo)``, em que ``codigo`` determina como o campo
``valor`` deve ser lido. Até a versão 5.0.7 esses códigos eram números literais
espalhados por `economic.py` e pelos testes, sem definição única — o que já produziu
um teste desatualizado, que rejeitava o código ``-2`` por desconhecê-lo.

Este módulo é a definição única dos **códigos**. Não altera nenhum cálculo: nomeia os
códigos, descreve as famílias efetivamente presentes no catálogo das 652 cidades e
oferece validação estrutural.

São dois níveis, e ambos fazem falta. O **código** diz como ler um campo da quádrupla;
o **regime** diz o que a cobrança significa para quem economiza água — se reduzir o
consumo reduz a conta, e a partir de que volume. Os regimes estão em
`netuno/core/tariff_regimes.py`, e importam os códigos daqui em vez de repeti-los.

Famílias observadas no catálogo (apuração de 8 de setembro de 2026)
-------------------------------------------------------------------
======================  =========  ==========================================
Códigos presentes       Cidades    Estrutura
======================  =========  ==========================================
``{-1, 1}``             486        taxa fixa de disponibilidade + faixas progressivas
``{1}``                 165        apenas faixas progressivas
``{-2, 1}``             1          franquia de consumo mínimo + faixas progressivas
======================  =========  ==========================================
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Sequence, Tuple

# ---------------------------------------------------------------------------------
# Códigos do quarto campo da quádrupla tarifária
# ---------------------------------------------------------------------------------

#: Faixa progressiva. ``valor`` é a tarifa em R$/m³ aplicada ao volume dentro da faixa.
FAIXA_PROGRESSIVA = 1

#: Faixa sem cobrança volumétrica. Reconhecido pelo motor econômico, ausente do catálogo.
FAIXA_ISENTA = 0

#: Taxa fixa de disponibilidade. ``valor`` é um custo em R$ somado à conta,
#: independentemente do consumo. Os campos de mínimo e máximo são ignorados.
TAXA_FIXA_DE_DISPONIBILIDADE = -1

#: Franquia de consumo mínimo com taxa fixa inclusa. Até ``maximo_m3`` a conta é
#: ``valor`` (R$); excedido esse volume, todo o consumo desde 0 m³ passa a ser cobrado
#: pelas faixas progressivas. Ex.: DAE Americana — até 6 m³, R$ 14,30 fixos.
FRANQUIA_DE_CONSUMO_MINIMO = -2

#: Piso de pagamento. ``valor`` é o mínimo que a conta pode atingir: cobra-se pelas
#: faixas, mas o total nunca fica abaixo dele. Distinto da taxa de disponibilidade,
#: que **soma** por cima do consumo medido — o piso **limita** por baixo. A diferença
#: é a economia que um sistema de aproveitamento pode creditar no primeiro bloco.
PISO_DE_PAGAMENTO = -3

CODIGOS_VALIDOS = frozenset({
    FAIXA_PROGRESSIVA,
    FAIXA_ISENTA,
    TAXA_FIXA_DE_DISPONIBILIDADE,
    FRANQUIA_DE_CONSUMO_MINIMO,
    PISO_DE_PAGAMENTO,
})

DESCRICAO_DO_CODIGO = {
    FAIXA_PROGRESSIVA: "faixa progressiva (R$/m³)",
    FAIXA_ISENTA: "faixa sem cobrança volumétrica",
    TAXA_FIXA_DE_DISPONIBILIDADE: "taxa fixa de disponibilidade (R$)",
    FRANQUIA_DE_CONSUMO_MINIMO: "franquia de consumo mínimo com taxa inclusa (R$)",
    PISO_DE_PAGAMENTO: "piso de pagamento: a conta nunca fica abaixo deste valor (R$)",
}

#: Valor convencional usado para representar “sem teto” na última faixa progressiva.
#: Faixas terminais abaixo deste patamar deixam consumo sem cobertura tarifária.
TETO_ABERTO_M3 = 9999.0


# ---------------------------------------------------------------------------------
# Diagnóstico estrutural
# ---------------------------------------------------------------------------------

@dataclass
class DiagnosticoTarifario:
    """Resultado da inspeção estrutural de uma tarifa."""

    codigos_presentes: frozenset
    tem_faixa_progressiva: bool
    cobre_consumo_ilimitado: bool
    responde_ao_consumo: bool
    problemas: List[str] = field(default_factory=list)

    @property
    def utilizavel_para_analise_economica(self) -> bool:
        """A tarifa permite estimar economia ao reduzir o consumo?

        Uma tarifa que não responde ao consumo produz economia monetária nula para
        qualquer sistema de aproveitamento, independentemente do desempenho hídrico.
        """
        return self.responde_ao_consumo


def _quadruplas(faixas: Iterable[Sequence]) -> List[Tuple[float, float, float, int]]:
    return [(float(f[0]), float(f[1]), float(f[2]), int(f[3])) for f in faixas]


def custo_volumetrico(faixas: Sequence[Sequence], consumo_m3: float) -> float:
    """Parcela da conta que depende do volume, ignorando taxas fixas.

    Reproduz a lógica de `economic.calculate_water_bill` restrita às faixas
    progressivas, para permitir o diagnóstico sem construir uma conta completa.
    """
    total = 0.0
    for minimo, maximo, valor, codigo in _quadruplas(faixas):
        if codigo not in (FAIXA_PROGRESSIVA, FAIXA_ISENTA):
            continue
        if consumo_m3 > minimo:
            volume_na_faixa = min(consumo_m3, maximo) - minimo
            if volume_na_faixa > 0:
                total += volume_na_faixa * valor
    return total


def diagnosticar(faixas: Sequence[Sequence]) -> DiagnosticoTarifario:
    """Inspeciona a estrutura de uma tarifa e aponta problemas.

    A verificação central é se a conta **responde ao consumo**: comparam-se dois
    patamares residenciais típicos (10 m³ e 25 m³ mensais). Se a parcela volumétrica
    não crescer entre eles, nenhuma redução de consumo gera economia.
    """
    problemas: List[str] = []

    if not faixas:
        return DiagnosticoTarifario(frozenset(), False, False, False,
                                    ["tarifa sem nenhuma faixa declarada"])

    quadruplas = _quadruplas(faixas)
    codigos = frozenset(c for *_, c in quadruplas)

    for codigo in sorted(codigos):
        if codigo not in CODIGOS_VALIDOS:
            problemas.append(f"código de faixa desconhecido: {codigo}")

    progressivas = sorted(
        [q for q in quadruplas if q[3] == FAIXA_PROGRESSIVA], key=lambda q: q[0]
    )
    tem_progressiva = bool(progressivas)
    if not tem_progressiva:
        problemas.append("nenhuma faixa progressiva: a conta não pode variar com o consumo")

    cobre_ilimitado = bool(progressivas) and progressivas[-1][1] >= TETO_ABERTO_M3
    if progressivas and not cobre_ilimitado:
        problemas.append(
            f"última faixa termina em {progressivas[-1][1]:g} m³: consumo acima disso "
            "fica sem cobertura tarifária"
        )

    if any(valor < 0 for *_, valor, _ in [(q[0], q[1], q[2], q[3]) for q in quadruplas]):
        problemas.append("faixa com valor negativo")

    responde = (custo_volumetrico(faixas, 25.0) - custo_volumetrico(faixas, 10.0)) > 1e-9
    if not responde:
        problemas.append(
            "a parcela volumétrica não cresce entre 10 e 25 m³: economizar água não "
            "reduz a conta, e a análise econômica resultará em retorno nulo"
        )

    return DiagnosticoTarifario(
        codigos_presentes=codigos,
        tem_faixa_progressiva=tem_progressiva,
        cobre_consumo_ilimitado=cobre_ilimitado,
        responde_ao_consumo=responde,
        problemas=problemas,
    )
