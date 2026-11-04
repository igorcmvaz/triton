"""
Formalização da estrutura tarifária: códigos, famílias e validação.

O catálogo do Triton representa cada tarifa como uma lista de quádruplas
``(minimo_m3, maximo_m3, valor, codigo)``, em que ``codigo`` determina como o campo
``valor`` deve ser lido. Esses códigos já foram números literais
espalhados por `economic.py` e pelos testes, sem definição única — o que já produziu
um teste desatualizado, que rejeitava o código ``-2`` por desconhecê-lo.

Este módulo é a definição única dos **códigos**. Não altera nenhum cálculo: nomeia os
códigos, descreve as famílias efetivamente presentes no catálogo das 652 cidades e
oferece validação estrutural.

São dois níveis, e ambos fazem falta. O **código** diz como ler um campo da quádrupla;
o **regime** diz o que a cobrança significa para quem economiza água — se reduzir o
consumo reduz a conta, e a partir de que volume. Os regimes estão em
`triton/core/tariff_regimes.py`, e importam os códigos daqui em vez de repeti-los.

Famílias observadas no catálogo (apuração de 8 de setembro de 2026)
-------------------------------------------------------------------
======================  =========  ==========================================
Códigos presentes       Cidades    Estrutura
======================  =========  ==========================================
``{-1, 1}``             486        taxa fixa de disponibilidade + faixas progressivas
``{1}``                 165        apenas faixas progressivas
``{-2, 1}``             1          franquia de consumo mínimo + faixas progressivas
``{-1, 2, 3}``          34         serviço básico + fórmula exponencial (CORSAN)
======================  =========  ==========================================

A família exponencial modela a estrutura tarifária não linear da CORSAN (RS).
"""

from __future__ import annotations

import math
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

#: Preço-base da fórmula exponencial da CORSAN: a água custa ``PB × Cⁿ``, em que ``C``
#: é o consumo do mês inteiro e ``n`` vem da tabela exponencial. ``valor`` é o PB em
#: R$/m³ e ``maximo_m3`` o consumo até o qual a fórmula vale — sem teto na categoria
#: residencial da CORSAN, 1.000 m³ na industrial; acima do teto, o excedente é
#: cobrado pelas faixas progressivas que começam ali.
PRECO_BASE_EXPONENCIAL = 2

#: Uma linha da tabela exponencial. ``valor`` é o expoente ``n`` aplicado quando o
#: consumo total do mês cai em ``(minimo_m3, maximo_m3]`` (a primeira linha inclui o
#: zero). O expoente vale para o volume inteiro, não só para o que está na faixa.
EXPOENTE_DE_CONSUMO = 3

#: Modo de cobrança do esgoto (``esgoto_modo`` na base, ``sewage_mode`` no projeto):
#: 0 = valor fixo em R$; 1 = percentual da parcela de água; 2 = preço por m³ do
#: consumo de água. O modo 2 é o da CORSAN: o esgoto não carrega o serviço básico
#: nem o expoente da água, e cresce linearmente com o consumo. O modo 3 é o da fatura
#: portuguesa: escalões próprios por m³, aplicados a uma fração do volume de água (o
#: «coeficiente de recolha»; Lisboa fatura 90%), com ``sewage_tariffs`` e
#: ``sewage_volume_factor`` no projeto (triton/core/fatura_portuguesa.py).
ESGOTO_FIXO, ESGOTO_PERCENTUAL, ESGOTO_POR_M3, ESGOTO_POR_FAIXAS = 0, 1, 2, 3

CODIGOS_VALIDOS = frozenset({
    PRECO_BASE_EXPONENCIAL,
    EXPOENTE_DE_CONSUMO,
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
    PRECO_BASE_EXPONENCIAL: "preço-base da fórmula exponencial PB × Cⁿ (R$/m³)",
    EXPOENTE_DE_CONSUMO: "expoente n da tabela exponencial, pelo consumo do mês",
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


def expoente_do_consumo(faixas: Sequence[Sequence], consumo_m3: float) -> float:
    """O ``n`` da tabela exponencial para o consumo total do mês.

    Cada linha cobre ``(minimo, maximo]``; a primeira inclui o zero. Sem tabela, o
    expoente é 1 e a fórmula se reduz a ``PB × C``, a forma linear.
    """
    linhas = sorted((q for q in _quadruplas(faixas) if q[3] == EXPOENTE_DE_CONSUMO),
                    key=lambda q: q[0])
    for _minimo, maximo, expoente, _ in linhas:
        if consumo_m3 <= maximo:
            return expoente
    return linhas[-1][2] if linhas else 1.0


def parcela_exponencial(faixas: Sequence[Sequence], consumo_m3: float) -> float:
    """``PB × Cⁿ``, com ``C`` limitado ao teto da fórmula; zero sem preço-base.

    O excedente acima do teto não entra aqui: é cobrado pelas faixas progressivas
    que começam no teto, como qualquer outra faixa.
    """
    base = next((q for q in _quadruplas(faixas) if q[3] == PRECO_BASE_EXPONENCIAL), None)
    if base is None or consumo_m3 <= 0:
        return 0.0
    _minimo, teto, preco_base, _ = base
    consumo = min(consumo_m3, teto) if teto > 0 else consumo_m3

    def potencia(c: float) -> float:
        return preco_base * c ** expoente_do_consumo(faixas, c) if c > 0 else 0.0

    # O hidrômetro fatura m³ inteiros e a fração passa para a leitura seguinte; a conta
    # esperada de um consumo médio fracionário é a reta entre os dois inteiros. Sem
    # isso, o expoente saltaria dentro do m³ (20 m³ com n = 1,00; 20,01 m³ com 1,01 no
    # volume todo) e a tarifa evitada oscilaria com a casa decimal do consumo médio.
    abaixo = math.floor(consumo)
    if consumo == abaixo:
        return potencia(consumo)
    fracao = consumo - abaixo
    return potencia(abaixo) + fracao * (potencia(abaixo + 1.0) - potencia(abaixo))


def custo_volumetrico(faixas: Sequence[Sequence], consumo_m3: float) -> float:
    """Parcela da conta que depende do volume, ignorando taxas fixas.

    Reproduz a lógica de `economic.calculate_water_bill` restrita às faixas
    progressivas, para permitir o diagnóstico sem construir uma conta completa.
    """
    total = parcela_exponencial(faixas, consumo_m3)
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
    tem_progressiva = bool(progressivas) or PRECO_BASE_EXPONENCIAL in codigos
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
