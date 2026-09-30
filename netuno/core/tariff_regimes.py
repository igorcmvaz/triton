"""Regimes de tarifa mínima, declarados em vez de inferidos.

No Brasil convivem regimes de cobrança que a mesma expressão «tarifa mínima»
designa, e confundi-los muda o resultado de um estudo de aproveitamento
pluvial — porque o que interessa não é a conta, é **quanto a conta cai quando
se consome menos**.

| Regime | Como funciona | Efeito na economia |
| :--- | :--- | :--- |
| Franquia no mínimo | Paga-se um valor fixo que já dá direito a N m³ | Economizar abaixo de N não economiza **nada** |
| Piso de pagamento | Cobra-se por faixa, mas nunca menos que um piso | Idem, até o consumo cujo valor tarifado alcança o piso |
| Disponibilidade | Taxa fixa somada **por cima** do consumo medido desde 0 m³ | Toda economia se converte em desconto |
| Franquia retroativa | Até N m³ paga-se fixo; acima, **todo** o volume desde 0 é tarifado | Descontinuidade em N |
| Sem mínimo | Só faixas progressivas | Toda economia se converte em desconto |
| Exponencial | Serviço básico + `PB × Cⁿ`, com `n` pelo consumo do mês (CORSAN) | Toda economia desconta, pelo preço médio da faixa de `n` |

A distinção não é acadêmica. Numa concessionária com franquia de 15 m³, uma
residência que consome 12 m³ **não economiza um centavo** por instalar cisterna:
a conta é a mesma com 12 ou com 3 m³. Tratá-la como se houvesse desconto
proporcional inventa uma economia que a concessionária não concede, e o payback
sai otimista.

O erro simétrico também existe e é igualmente grave: uma tabela de faixas
truncada, que não cobre o consumo alto, faz a conta parar de crescer — e então o
programa não vê economia nenhuma acima do teto tabelado.

**A regra de codificação.** As faixas são `(min_m³, max_m³, valor, tipo)`:

* `tipo = -1` — custo fixo mensal, somado sempre;
* `tipo = -3` — piso de pagamento: a conta nunca fica abaixo deste valor;
* `tipo = -2` — franquia retroativa;
* `tipo = 0` ou `1` — faixa progressiva, em R$/m³;
* `tipo = 2` — preço-base `PB` da fórmula exponencial, válida até `max_m³`;
* `tipo = 3` — expoente `n` da tabela exponencial, para o consumo em `(min, max]`.

A fórmula exponencial escreve-se como um `-1` com o serviço básico, um `2` com o
preço-base, as linhas `3` da tabela exponencial cobrindo de 0 ao teto da fórmula,
e uma faixa `1` do teto em diante para o excedente.

Franquia no mínimo escreve-se como um `-1` com o valor do mínimo mais uma faixa
`0..N` a **R$ 0,00/m³**. Disponibilidade escreve-se como um `-1` mais a primeira
faixa **cobrando desde 0**. As duas têm a mesma forma e diferem apenas pela
tarifa da primeira faixa, e é por isso que o regime passa a ser declarado: um
erro de digitação numa casa decimal troca um regime pelo outro em silêncio.

Referência normativa: a conta mínima resulta do produto da tarifa mínima pelo
consumo mínimo, de no mínimo 10 m³ mensais por economia na categoria
residencial, conforme os regulamentos dos serviços sob a Lei federal
11.445/2007. A «tarifa de disponibilidade» é instituto distinto do «consumo
mínimo», e não deve ser tratada como sinônimo.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Tuple

from netuno.core.tariffs_structure import (
    EXPOENTE_DE_CONSUMO,
    PRECO_BASE_EXPONENCIAL,
    FAIXA_ISENTA,
    FAIXA_PROGRESSIVA,
    FRANQUIA_DE_CONSUMO_MINIMO,
    PISO_DE_PAGAMENTO as CODIGO_PISO,
    TAXA_FIXA_DE_DISPONIBILIDADE,
    TETO_ABERTO_M3,
)

#: Cobra-se um valor fixo que já dá direito a N m³. Economizar abaixo de N não
#: reduz a conta. É o regime mais comum no Brasil.
FRANQUIA_NO_MINIMO = "franquia_no_minimo"

#: Cobra-se por faixa, mas a conta nunca fica abaixo de um piso.
PISO_DE_PAGAMENTO = "piso_de_pagamento"

#: Taxa fixa somada por cima do consumo medido desde 0 m³. Toda economia vira
#: desconto. Instituto distinto do consumo mínimo.
DISPONIBILIDADE = "disponibilidade"

#: Até N m³ paga-se fixo; acima de N, todo o volume desde 0 é tarifado.
FRANQUIA_RETROATIVA = "franquia_retroativa"

#: Só faixas progressivas, sem mínimo.
SEM_MINIMO = "sem_minimo"

#: Serviço básico mais ``PB × Cⁿ``: o preço-base elevado a um expoente que depende
#: do consumo do mês inteiro (CORSAN). Toda economia desconta, mas não por um
#: preço fixo por m³: o que se poupa vale ``PB × (C₁ⁿ¹ − C₂ⁿ²)``.
EXPONENCIAL = "exponencial"

REGIMES = (
    FRANQUIA_NO_MINIMO,
    PISO_DE_PAGAMENTO,
    DISPONIBILIDADE,
    FRANQUIA_RETROATIVA,
    SEM_MINIMO,
    EXPONENCIAL,
)

#: Maior expoente aceito sem alarme. A tabela da CORSAN fica perto de 1; um
#: expoente 2 faria a conta de 20 m³ quatro vezes a de 10 m³.
EXPOENTE_MAXIMO_PLAUSIVEL = 2.0

#: Consumo mínimo faturado usual na categoria residencial, em m³/mês. Serve de
#: referência para conferência, não de valor adotado.
CONSUMO_MINIMO_USUAL_M3 = 10.0

# Os códigos do quarto campo da quádrupla têm definição única em
# `tariffs_structure.py`, que existe justamente para impedir que sejam repetidos
# como literais. Importam-se de lá; aqui ficam apenas apelidos locais.
TIPO_CUSTO_FIXO = TAXA_FIXA_DE_DISPONIBILIDADE
TIPO_FRANQUIA_RETROATIVA = FRANQUIA_DE_CONSUMO_MINIMO
TIPO_PISO_DE_PAGAMENTO = CODIGO_PISO
TIPOS_DE_FAIXA = (FAIXA_ISENTA, FAIXA_PROGRESSIVA)


Faixa = Sequence[float]


@dataclass(frozen=True)
class Achado:
    """Um problema encontrado numa estrutura tarifária."""

    codigo: str
    gravidade: str          # "erro" | "aviso"
    mensagem: str

    def __str__(self) -> str:  # pragma: no cover - conveniência de depuração
        return f"[{self.gravidade}] {self.codigo}: {self.mensagem}"


@dataclass(frozen=True)
class Estrutura:
    """A leitura estruturada de uma tabela de faixas."""

    regime: str
    custo_fixo_mensal: float
    piso_de_pagamento: float
    consumo_minimo_m3: float
    faixas_progressivas: List[Tuple[float, float, float]] = field(default_factory=list)
    teto_tabelado_m3: float = 0.0
    #: Fórmula exponencial: preço-base (R$/m³), teto da fórmula (m³) e a tabela
    #: ``(min_m³, max_m³, n)``. Vazios fora do regime exponencial.
    preco_base: float = 0.0
    teto_exponencial_m3: float = 0.0
    expoentes: List[Tuple[float, float, float]] = field(default_factory=list)


def _numeros(faixa: Faixa) -> Tuple[float, float, float, int]:
    return float(faixa[0]), float(faixa[1]), float(faixa[2]), int(faixa[3])


def ler_estrutura(faixas: Optional[Sequence[Faixa]]) -> Estrutura:
    """Lê uma tabela de faixas e devolve o que ela representa.

    A leitura não julga: apenas separa custo fixo, piso, franquia e faixas
    progressivas, e infere o regime a partir da forma. `validar_estrutura` é que
    aponta o que não fecha.
    """
    faixas = list(faixas or [])
    fixos = [_numeros(f) for f in faixas if int(f[3]) == TIPO_CUSTO_FIXO]
    pisos = [_numeros(f) for f in faixas if int(f[3]) == TIPO_PISO_DE_PAGAMENTO]
    retro = [_numeros(f) for f in faixas if int(f[3]) == TIPO_FRANQUIA_RETROATIVA]
    bases = [_numeros(f) for f in faixas if int(f[3]) == PRECO_BASE_EXPONENCIAL]
    expoentes = sorted(
        (_numeros(f)[:3] for f in faixas if int(f[3]) == EXPOENTE_DE_CONSUMO),
        key=lambda t: t[0],
    )
    tiers = sorted(
        (_numeros(f)[:3] for f in faixas if int(f[3]) in TIPOS_DE_FAIXA),
        key=lambda t: t[0],
    )

    custo_fixo = sum(f[2] for f in fixos)
    piso = max((p[2] for p in pisos), default=0.0)
    teto = tiers[-1][1] if tiers else 0.0

    if bases:
        regime = EXPONENCIAL
        minimo = 0.0
    elif retro:
        regime = FRANQUIA_RETROATIVA
        minimo = retro[0][1]
    elif piso > 0:
        regime = PISO_DE_PAGAMENTO
        minimo = 0.0
    elif custo_fixo > 0 and tiers and tiers[0][2] == 0.0:
        regime = FRANQUIA_NO_MINIMO
        # A franquia vai até onde a tarifa deixa de ser nula.
        minimo = 0.0
        for inicio, fim, valor in tiers:
            if valor == 0.0:
                minimo = fim
            else:
                break
    elif custo_fixo > 0:
        regime = DISPONIBILIDADE
        minimo = 0.0
    else:
        regime = SEM_MINIMO
        minimo = 0.0

    return Estrutura(
        regime=regime,
        custo_fixo_mensal=custo_fixo,
        piso_de_pagamento=piso,
        consumo_minimo_m3=minimo,
        faixas_progressivas=list(tiers),
        teto_tabelado_m3=teto,
        preco_base=bases[0][2] if bases else 0.0,
        teto_exponencial_m3=bases[0][1] if bases else 0.0,
        expoentes=list(expoentes),
    )


def validar_estrutura(registro: Dict[str, Any]) -> List[Achado]:
    """Aponta o que não fecha numa estrutura tarifária.

    Separa **erro** de **aviso**. Erro é o que produz conta errada em qualquer
    consumo — tabela truncada, faixa negativa, mínimo declarado e não cobrado.
    Aviso é o que merece conferência mas pode ser legítimo, como uma tarifa não
    progressiva, que existe em tarifa social.
    """
    achados: List[Achado] = []
    faixas = registro.get("faixas") or []

    if not faixas:
        return [Achado("sem_faixas", "erro", "nenhuma faixa tarifária cadastrada")]

    for f in faixas:
        if len(f) < 4:
            return [Achado("faixa_malformada", "erro", f"faixa com menos de 4 campos: {f!r}")]
        if int(f[3]) not in TIPOS_DE_FAIXA + (
            TIPO_CUSTO_FIXO,
            TIPO_FRANQUIA_RETROATIVA,
            TIPO_PISO_DE_PAGAMENTO,
            PRECO_BASE_EXPONENCIAL,
            EXPOENTE_DE_CONSUMO,
        ):
            achados.append(Achado("tipo_desconhecido", "erro", f"tipo de faixa {f[3]!r} não reconhecido"))

    est = ler_estrutura(faixas)
    tiers = est.faixas_progressivas
    if est.regime == EXPONENCIAL:
        achados.extend(_validar_exponencial(est, registro))

    # Na fórmula exponencial as faixas começam no teto da fórmula, e não em zero.
    inicio_esperado = est.teto_exponencial_m3 if est.regime == EXPONENCIAL else 0.0
    if tiers:
        if tiers[0][0] != inicio_esperado and est.regime != FRANQUIA_RETROATIVA:
            achados.append(
                Achado("nao_comeca_em_zero", "erro",
                       f"a primeira faixa começa em {tiers[0][0]:.0f} m³ e não em "
                       f"{inicio_esperado:.0f}")
            )
        if est.teto_tabelado_m3 < TETO_ABERTO_M3:
            achados.append(
                Achado(
                    "tabela_truncada", "erro",
                    f"a última faixa termina em {est.teto_tabelado_m3:.0f} m³: acima disso a "
                    "conta não cresce, e o programa não vê economia nenhuma",
                )
            )
        for a, b in zip(tiers, tiers[1:]):
            if abs(a[1] - b[0]) > 1e-6:
                achados.append(
                    Achado("lacuna_entre_faixas", "erro",
                           f"salto de {a[1]:.0f} para {b[0]:.0f} m³ entre faixas")
                )
        if any(t[2] < 0 for t in tiers):
            achados.append(Achado("tarifa_negativa", "erro", "há faixa com tarifa negativa"))

        nao_nulas = [t[2] for t in tiers if t[2] > 0]
        if nao_nulas != sorted(nao_nulas):
            achados.append(
                Achado("nao_progressiva", "aviso",
                       f"a tarifa por m³ não cresce com o consumo: {[round(t[2], 2) for t in tiers]}")
            )

    declarada = registro.get("tarifa_fixa_mensal")
    if declarada is not None:
        declarada = float(declarada)
        cobrada = est.custo_fixo_mensal + est.piso_de_pagamento
        if est.regime == FRANQUIA_RETROATIVA:
            pass  # a franquia carrega o próprio valor
        elif declarada > 0 and cobrada <= 0:
            achados.append(
                Achado(
                    "minimo_declarado_e_nao_cobrado", "erro",
                    f"declara mínimo de R$ {declarada:.2f} e nenhuma faixa o cobra",
                )
            )
        elif declarada > 0 and abs(declarada - cobrada) > max(0.01, 0.01 * declarada):
            achados.append(
                Achado("minimo_diverge", "aviso",
                       f"mínimo declarado R$ {declarada:.2f} contra R$ {cobrada:.2f} nas faixas")
            )

    # A assinatura do mínimo diluído: alguém calculou tarifa x volume para achar
    # o mínimo e gravou a TARIFA, de modo que consumir menos que a franquia
    # passa a reduzir a conta — e não reduz.
    if declarada and declarada > 0 and tiers and tiers[0][2] > 0:
        produto = tiers[0][2] * (tiers[0][1] - tiers[0][0])
        if abs(produto - declarada) < max(0.05, 0.01 * declarada):
            achados.append(
                Achado(
                    "minimo_diluido_em_tarifa", "erro",
                    f"R$ {declarada:.2f} = {tiers[0][2]:.3f} R$/m³ × {tiers[0][1]:.0f} m³: o mínimo "
                    "foi gravado como tarifa unitária, de modo que economizar dentro da franquia "
                    "reduz a conta quando não deveria",
                )
            )

    esgoto_pct = registro.get("esgoto_pct")
    if registro.get("esgoto_modo") == 1 and esgoto_pct is not None:
        if not 0.0 <= float(esgoto_pct) <= 200.0:
            achados.append(
                Achado("esgoto_fora_de_faixa", "erro", f"esgoto de {esgoto_pct}% da água")
            )

    return achados


def _validar_exponencial(est: Estrutura, registro: Dict[str, Any]) -> List[Achado]:
    """O que precisa fechar na fórmula ``PB × Cⁿ``."""
    achados: List[Achado] = []
    if est.preco_base <= 0:
        achados.append(Achado("preco_base_invalido", "erro", "preço-base da fórmula exponencial nulo"))
    if est.teto_exponencial_m3 <= 0:
        achados.append(Achado("teto_exponencial_ausente", "erro",
                              "a fórmula exponencial não declara até que consumo vale"))
    if not est.expoentes:
        achados.append(Achado("sem_tabela_exponencial", "erro",
                              "preço-base sem tabela exponencial: não há expoente a aplicar"))
        return achados
    if est.expoentes[0][0] != 0.0:
        achados.append(Achado("expoente_nao_comeca_em_zero", "erro",
                              f"a tabela exponencial começa em {est.expoentes[0][0]:.0f} m³"))
    for a, b in zip(est.expoentes, est.expoentes[1:]):
        if abs(a[1] - b[0]) > 1e-6:
            achados.append(Achado("lacuna_na_tabela_exponencial", "erro",
                                  f"salto de {a[1]:.0f} para {b[0]:.0f} m³ na tabela exponencial"))
    if est.expoentes[-1][1] < est.teto_exponencial_m3:
        achados.append(Achado("tabela_exponencial_truncada", "erro",
                              f"a tabela exponencial para em {est.expoentes[-1][1]:.0f} m³ e a "
                              f"fórmula vale até {est.teto_exponencial_m3:.0f} m³"))
    fora = [n for *_, n in est.expoentes if not 0.0 < n <= EXPOENTE_MAXIMO_PLAUSIVEL]
    if fora:
        achados.append(Achado("expoente_implausivel", "erro", f"expoentes fora de (0, 2]: {fora}"))
    if registro.get("expoentes_verificados") is False:
        achados.append(Achado(
            "expoentes_pendentes", "aviso",
            "a tabela exponencial gravada não foi conferida com a tabela vigente do "
            "prestador: a conta usa o expoente registrado, e não o homologado",
        ))
    if registro.get("esgoto_modo") == 2 and not float(registro.get("esgoto_r_m3") or 0.0) > 0.0:
        achados.append(Achado("esgoto_sem_preco", "erro",
                              "esgoto cobrado por m³ sem preço por m³ declarado"))

    return achados


def estrutura_confiavel(registro: Dict[str, Any]) -> bool:
    """Diz se a estrutura pode ser usada sem ressalva num estudo."""
    return not any(a.gravidade == "erro" for a in validar_estrutura(registro))


def auditar_base(cidades: Dict[str, Dict[str, Any]]) -> Dict[str, List[Achado]]:
    """Roda a validação sobre a base inteira e devolve só o que tem achado."""
    saida: Dict[str, List[Achado]] = {}
    for chave, registro in cidades.items():
        achados = validar_estrutura(registro)
        if achados:
            saida[chave] = achados
    return saida


def resumo_do_regime(registro: Dict[str, Any], lang: str = "pt") -> str:
    """Frase curta que descreve o regime para a interface.

    O que o projetista precisa saber não é o nome do regime, é se economizar
    água reduz a conta — e a partir de que consumo.
    """
    est = ler_estrutura(registro.get("faixas"))

    if est.regime == FRANQUIA_NO_MINIMO and est.consumo_minimo_m3 > 0:
        return (
            f"Mínimo de R$ {est.custo_fixo_mensal:.2f}/mês com {est.consumo_minimo_m3:.0f} m³ "
            f"inclusos. Abaixo de {est.consumo_minimo_m3:.0f} m³ a conta não cai: o "
            "aproveitamento só gera economia no volume que exceder a franquia."
        )
    if est.regime == PISO_DE_PAGAMENTO:
        return (
            f"Piso de R$ {est.piso_de_pagamento:.2f}/mês. A conta é medida por faixa, mas "
            "nunca fica abaixo do piso, de modo que a economia só aparece acima dele."
        )
    if est.regime == DISPONIBILIDADE:
        return (
            f"Taxa de disponibilidade de R$ {est.custo_fixo_mensal:.2f}/mês somada ao consumo "
            "medido desde o primeiro metro cúbico. Toda economia de água vira desconto."
        )
    if est.regime == EXPONENCIAL:
        teto = (f", até {est.teto_exponencial_m3:.0f} m³"
                if est.teto_exponencial_m3 < TETO_ABERTO_M3 else "")
        return (
            f"Serviço básico de R$ {est.custo_fixo_mensal:.2f}/mês mais a fórmula exponencial "
            f"PB × Cⁿ, com preço-base de R$ {est.preco_base:.2f}/m³ e o expoente n da "
            f"tabela pelo consumo do mês{teto}. Toda economia de água vira desconto, e o "
            "metro cúbico poupado vale mais onde o expoente é maior."
        )
    if est.regime == FRANQUIA_RETROATIVA:
        return (
            f"Franquia de {est.consumo_minimo_m3:.0f} m³ por valor fixo; acima dela, todo o "
            "volume medido é tarifado desde 0 m³."
        )
    return "Somente faixas progressivas, sem mínimo faturado. Toda economia vira desconto."
