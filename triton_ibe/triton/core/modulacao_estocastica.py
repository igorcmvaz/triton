# -*- coding: utf-8 -*-
"""Modulação probabilística: o estudo pronto, refeito com premissas sorteadas.

O estudo determinístico responde com um número por volume, para premissas fixas. Na
prática muitas são incertas — o consumo per capita, o número de pessoas, a fração não
potável, a área efetiva de captação, a chuva dos próximos anos, a tarifa, a taxa de
desconto, o preço da obra — e esta ferramenta mede o quanto isso mexe no resultado **sem
mudar o estudo**: ele continua alimentando todas as abas, os relatórios e a linha de
comando.

O usuário escolhe no `CATALOGO` o que variar e com que distribuição. Cada realização
sorteia as variáveis escolhidas **uma vez** — o nível, e não o ruído de um dia para o
outro, que se cancela numa série longa (ver `triton/core/demanda_estocastica.py`) — e
refaz a cadeia técnica → econômica → ambiental → TOPSIS para **todos** os volumes com a
mesma amostra. A comparação entre volumes é pareada: a diferença entre dois volumes numa
realização é efeito do volume, não do sorteio. A variação diária do consumo pode ser
acrescentada (``cv_diario_pct``).

O resultado é um painel de robustez: estatísticas no volume que o estudo escolheu
(média, desvio-padrão, coeficiente de variação, percentis), faixas P5–P50–P95 por volume,
a probabilidade de o investimento se pagar e de o saldo de carbono ser positivo, com
intervalo de 95% de Wilson, a frequência com que cada volume é o ideal técnico, o ótimo
econômico (menor payback descontado) e o vencedor do TOPSIS, a sensibilidade (ρ de
Spearman) e a convergência. Semente, número de realizações e distribuições vão no
resultado: a análise se refaz igual.
"""

from __future__ import annotations

import copy
import math
from dataclasses import asdict, dataclass, field
from typing import Any, Callable, Dict, List, Optional, Sequence

import numpy as np

from triton.core.fracao_atendivel import fracao_total

TIPOS = ("normal", "lognormal", "triangular", "uniforme")
PERCENTIS = (5, 50, 95)
#: Tentativas da truncagem por rejeição antes de recorrer ao recorte.
_TENTATIVAS = 50
#: Atributos que a cadeia econômica lê (ver `triton/cli.py::_economic_row`): o fator do
#: investimento inteiro, o do preço da cisterna e o do custeio anual de operação e manutenção.
ATRIBUTO_FATOR_DE_INVESTIMENTO = "fator_de_investimento_estocastico"
ATRIBUTO_FATOR_DA_CISTERNA = "fator_da_cisterna_estocastico"
ATRIBUTO_FATOR_DE_OM = "fator_de_om_estocastico"


@dataclass(frozen=True)
class Variavel:
    """Uma premissa que a ferramenta sabe sortear."""
    chave: str
    rotulo: str
    unidade: str
    grupo: str
    descricao: str
    casas: int = 1
    #: Ligada por padrão na tela (as três premissas de consumo).
    padrao: bool = False


#: As variáveis que podem entrar no contexto estocástico, na ordem da tela.
CATALOGO: Dict[str, Variavel] = {v.chave: v for v in (
    Variavel("per_capita_l_dia", "Consumo per capita", "L/hab.dia", "Demanda",
             "Consumo médio por pessoa; incerto quando não há medição.", 1, True),
    Variavel("pessoas", "Número de pessoas", "pessoas", "Demanda",
             "Ocupação da edificação; sorteada como inteiro, ao menos 1.", 0, True),
    Variavel("fracao_nao_potavel_pct", "Fração não potável interna", "%", "Demanda",
             "Parte do consumo interno que a água de chuva pode atender (bacias, máquina de lavar).", 1, True),
    Variavel("demanda_externa_l_dia", "Demanda externa", "L/dia", "Demanda",
             "Rega e lavagem de áreas externas.", 0),
    Variavel("area_m2", "Área de captação", "m²", "Captação",
             "Área de cobertura efetivamente ligada à cisterna.", 1),
    Variavel("coef_escoamento", "Coeficiente de escoamento", "—", "Captação",
             "Perdas por absorção, evaporação e transbordamento de calhas.", 2),
    Variavel("descarte_mm", "Lâmina de descarte", "mm", "Captação",
             "Primeira chuva desviada pelo dispositivo de descarte.", 1),
    Variavel("fator_chuva", "Fator da chuva", "×", "Chuva",
             "Multiplica toda a série diária: chuva futura mais seca ou mais úmida que a histórica.", 2),
    Variavel("fator_tarifa", "Fator das tarifas de água e esgoto", "×", "Tarifas",
             "Multiplica todos os valores em reais da estrutura de água (faixas, parcela fixa, conta "
             "mínima) e o esgoto cobrado em reais; o esgoto em % da água acompanha a água.", 2),
    Variavel("fator_esgoto", "Fator do esgoto", "×", "Tarifas",
             "Multiplica só a tarifa de esgoto, no modo em que o projeto a declara (% da água, R$ fixo ou R$/m³).", 2),
    Variavel("reajuste_tarifa_pct", "Reajuste tarifário", "% por período", "Tarifas",
             "Reajuste da água e do esgoto a cada período de reajuste.", 1),
    Variavel("tarifa_energia", "Tarifa de energia", "R$/kWh", "Tarifas",
             "Preço da energia do bombeamento; substitui o do projeto.", 3),
    Variavel("reajuste_energia_pct", "Reajuste da energia", "% por período", "Tarifas",
             "Reajuste da tarifa de energia a cada período de reajuste.", 1),
    Variavel("fator_investimento", "Fator do investimento", "×", "Custos",
             "Multiplica o investimento inicial inteiro de cada volume: cisterna, reservatório superior, "
             "motobomba, tubulação, acessórios, mão de obra e linha de tratamento.", 2),
    Variavel("fator_cisterna", "Fator do preço da cisterna", "×", "Custos",
             "Multiplica só o preço da cisterna, a parte do investimento que cresce com o volume; a mão de "
             "obra automática acompanha.", 2),
    Variavel("fator_om", "Fator do custeio (O&M)", "×", "Custos",
             "Multiplica o custo anual de operação e manutenção: itens declarados, custeio da linha de "
             "tratamento e cloro. A energia tem variável própria.", 2),
    Variavel("inflacao_om_pct_mes", "Inflação do custeio", "% ao mês", "Custos",
             "Correção anual do custeio de operação e manutenção.", 2),
    Variavel("tma_pct_mes", "Taxa mínima de atratividade", "% ao mês", "Fluxo de caixa",
             "Taxa de desconto do fluxo de caixa.", 2),
    Variavel("periodo_analise_anos", "Período de análise", "anos", "Fluxo de caixa",
             "Horizonte do fluxo de caixa e da avaliação ambiental; sorteado como inteiro, ao menos 1.", 0),
    Variavel("fator_emissao_agua", "Fator da emissão da água potável", "×", "Ambiente",
             "Multiplica a emissão por m³ da água da rede que a cisterna evita.", 2),
    Variavel("fator_emissao_rede", "Fator da emissão da rede elétrica", "×", "Ambiente",
             "Multiplica o fator de emissão da energia do bombeamento.", 2),
)}
GRUPOS = ("Demanda", "Captação", "Chuva", "Tarifas", "Custos", "Fluxo de caixa", "Ambiente")
#: As três premissas de consumo, ligadas por padrão.
PARAMETROS = ("per_capita_l_dia", "pessoas", "fracao_nao_potavel_pct")


@dataclass
class Distribuicao:
    """A incerteza de uma premissa.

    ``normal`` e ``lognormal`` usam ``media`` e ``desvio``; ``triangular`` usa ``minimo``,
    ``moda`` e ``maximo``; ``uniforme`` usa ``minimo`` e ``maximo``. ``limite_inferior`` e
    ``limite_superior`` truncam qualquer uma. ``variar=False`` mantém o valor do projeto.
    """
    tipo: str = "normal"
    media: float = 0.0
    desvio: float = 0.0
    minimo: float = 0.0
    moda: float = 0.0
    maximo: float = 0.0
    limite_inferior: Optional[float] = None
    limite_superior: Optional[float] = None
    variar: bool = True

    def validar(self, nome: str = "parâmetro") -> None:
        if self.tipo not in TIPOS:
            raise ValueError(f"{nome}: distribuição desconhecida «{self.tipo}»; use {', '.join(TIPOS)}.")
        if not self.variar:
            return
        if self.tipo in ("normal", "lognormal"):
            if self.desvio < 0:
                raise ValueError(f"{nome}: o desvio não pode ser negativo.")
            if self.tipo == "lognormal" and self.media <= 0:
                raise ValueError(f"{nome}: a lognormal pede média positiva.")
        elif self.tipo == "triangular":
            if not self.minimo <= self.moda <= self.maximo:
                raise ValueError(f"{nome}: a triangular pede mínimo ≤ moda ≤ máximo.")
        elif self.maximo < self.minimo:
            raise ValueError(f"{nome}: o máximo não pode ser menor que o mínimo.")
        if (self.limite_inferior is not None and self.limite_superior is not None
                and self.limite_superior < self.limite_inferior):
            raise ValueError(f"{nome}: o limite superior não pode ser menor que o inferior.")

    def _cru(self, gerador: np.random.Generator, n: int) -> np.ndarray:
        if self.tipo == "normal":
            return gerador.normal(self.media, self.desvio, n) if self.desvio > 0 else np.full(n, self.media)
        if self.tipo == "lognormal":
            if self.desvio <= 0:
                return np.full(n, self.media)
            # Parâmetros da lognormal que devolvem a média e o desvio pedidos.
            sigma = math.sqrt(math.log(1.0 + (self.desvio / self.media) ** 2))
            mu = math.log(self.media) - sigma ** 2 / 2.0
            return gerador.lognormal(mu, sigma, n)
        if self.tipo == "triangular":
            if self.maximo == self.minimo:
                return np.full(n, self.minimo)
            return gerador.triangular(self.minimo, self.moda, self.maximo, n)
        if self.maximo == self.minimo:
            return np.full(n, self.minimo)
        return gerador.uniform(self.minimo, self.maximo, n)

    def sortear(self, gerador: np.random.Generator, n: int) -> np.ndarray:
        """``n`` valores, truncados por rejeição aos limites (recorte só como último recurso)."""
        lo = -np.inf if self.limite_inferior is None else float(self.limite_inferior)
        hi = np.inf if self.limite_superior is None else float(self.limite_superior)
        valores = self._cru(gerador, n)
        for _ in range(_TENTATIVAS):
            fora = (valores < lo) | (valores > hi)
            if not fora.any():
                break
            valores[fora] = self._cru(gerador, int(fora.sum()))
        return np.clip(valores, lo, hi)

    def valor_central(self) -> float:
        """A média (normal, lognormal), a moda (triangular) ou o meio (uniforme)."""
        if self.tipo in ("normal", "lognormal"):
            return float(self.media)
        if self.tipo == "triangular":
            return float(self.moda)
        return (float(self.minimo) + float(self.maximo)) / 2.0


@dataclass
class ParametrosIncertos:
    """As variáveis escolhidas, cada uma com a sua distribuição, e a variação diária opcional.

    Só entram no sorteio as variáveis de ``variaveis`` com ``variar=True``; as demais ficam
    com o valor do projeto.
    """
    variaveis: Dict[str, Distribuicao] = field(default_factory=dict)
    #: Variação de um dia para o outro em torno do nível sorteado (%, lognormal); 0 = sem.
    cv_diario_pct: float = 0.0
    #: Modelos climáticos da base CLIMBra entre os quais cada realização sorteia a série de
    #: chuva (mesma cidade, cenário e recorte do projeto); vazio = a série do projeto.
    modelos_climaticos: List[str] = field(default_factory=list)

    def ativas(self) -> List[str]:
        return [k for k in CATALOGO if k in self.variaveis and self.variaveis[k].variar]

    def validar(self) -> None:
        for nome, dist in self.variaveis.items():
            if nome not in CATALOGO:
                raise ValueError(f"Variável desconhecida: «{nome}». Use uma de: {', '.join(CATALOGO)}.")
            dist.validar(CATALOGO[nome].rotulo)
        if self.cv_diario_pct < 0:
            raise ValueError("O coeficiente de variação diário não pode ser negativo.")
        if self.modelos_climaticos:
            from triton.core.climate_database import CLIMATE_MODELS
            desconhecidos = [m for m in self.modelos_climaticos if m not in CLIMATE_MODELS]
            if desconhecidos:
                raise ValueError(f"Modelo climático desconhecido: {', '.join(desconhecidos)}. "
                                 f"Use um de: {', '.join(CLIMATE_MODELS)}.")
            if len(set(self.modelos_climaticos)) != len(self.modelos_climaticos):
                raise ValueError("Modelo climático repetido na lista.")

    def para_dict(self) -> Dict[str, Any]:
        return {"variaveis": {k: asdict(v) for k, v in self.variaveis.items()}, "cv_diario_pct": self.cv_diario_pct,
                "modelos_climaticos": list(self.modelos_climaticos)}

    @classmethod
    def de_dict(cls, dados: Optional[Dict[str, Any]]) -> "ParametrosIncertos":
        dados = dict(dados or {})
        bruto = dados.get("variaveis")
        if bruto is None:  # formato da primeira versão: as três premissas no nível de cima
            bruto = {k: dados[k] for k in PARAMETROS if isinstance(dados.get(k), dict)}
        variaveis = {k: Distribuicao(**v) for k, v in bruto.items() if k in CATALOGO and isinstance(v, dict)}
        return cls(variaveis=variaveis, cv_diario_pct=float(dados.get("cv_diario_pct", 0.0)),
                   modelos_climaticos=[str(m) for m in dados.get("modelos_climaticos") or []])

    def __getattr__(self, nome):
        # Acesso direto por chave do catálogo (parametros.pessoas, parametros.area_m2…).
        variaveis = self.__dict__.get("variaveis", {})
        if nome in CATALOGO and nome in variaveis:
            return variaveis[nome]
        raise AttributeError(nome)


def valor_do_projeto(cfg, chave: str) -> float:
    """O valor que o estudo determinístico usa para a variável."""
    def g(nome, padrao=0.0):
        v = getattr(cfg, nome, padrao)
        return float(padrao if v is None else v)
    return {
        "per_capita_l_dia": lambda: g("demand_value"),
        "pessoas": lambda: g("residents_count", 1.0) or 1.0,
        "fracao_nao_potavel_pct": lambda: 100.0 * g("non_potable_indoor_share"),
        "demanda_externa_l_dia": lambda: g("irrigation_liters_per_day"),
        "area_m2": lambda: g("area"),
        "coef_escoamento": lambda: g("runoff_coeff"),
        "descarte_mm": lambda: g("discard"),
        "fator_chuva": lambda: 1.0,
        "fator_tarifa": lambda: 1.0,
        "fator_esgoto": lambda: 1.0,
        "reajuste_tarifa_pct": lambda: g("water_tariff_escalation"),
        "tarifa_energia": lambda: g("elec_tariff"),
        "reajuste_energia_pct": lambda: g("elec_tariff_escalation"),
        "fator_investimento": lambda: 1.0,
        "fator_cisterna": lambda: 1.0,
        "fator_om": lambda: 1.0,
        "inflacao_om_pct_mes": lambda: g("inflation"),
        "tma_pct_mes": lambda: g("tma"),
        "periodo_analise_anos": lambda: g("analysis_period_years", 20.0) or 20.0,
        "fator_emissao_agua": lambda: 1.0,
        "fator_emissao_rede": lambda: 1.0,
    }[chave]()


def distribuicao_de_triagem(cfg, chave: str) -> Distribuicao:
    """Distribuição inicial centrada no projeto. São valores de triagem: o autor os ajusta."""
    x = valor_do_projeto(cfg, chave)
    liga = CATALOGO[chave].padrao

    def normal(desvio, lo=0.0, hi=None, tipo="normal"):
        return Distribuicao(tipo, media=x, desvio=desvio, minimo=max(lo, x - 2 * desvio), moda=x,
                            maximo=x + 2 * desvio if hi is None else min(hi, x + 2 * desvio),
                            limite_inferior=lo, limite_superior=hi, variar=liga)
    regras = {
        "per_capita_l_dia": lambda: normal(0.20 * x, tipo="lognormal"),
        "pessoas": lambda: normal(1.0, lo=1.0, hi=max(2.0, 2.0 * x)),
        "fracao_nao_potavel_pct": lambda: normal(5.0, hi=100.0),
        "demanda_externa_l_dia": lambda: normal(0.30 * x),
        "area_m2": lambda: normal(0.05 * x),
        "coef_escoamento": lambda: Distribuicao("triangular", media=x, desvio=0.05, minimo=max(0.0, x - 0.10),
                                                moda=x, maximo=min(1.0, x + 0.05), limite_inferior=0.0,
                                                limite_superior=1.0, variar=liga),
        "descarte_mm": lambda: Distribuicao("uniforme", media=x, desvio=0.5, minimo=max(0.0, x - 1.0), moda=x,
                                            maximo=x + 1.0, limite_inferior=0.0, variar=liga),
        "fator_chuva": lambda: normal(0.10),
        "fator_tarifa": lambda: normal(0.10),
        "fator_esgoto": lambda: normal(0.10),
        "reajuste_tarifa_pct": lambda: normal(2.0, lo=-50.0),
        "tarifa_energia": lambda: normal(0.10 * x),
        "reajuste_energia_pct": lambda: normal(2.0, lo=-50.0),
        "fator_investimento": lambda: normal(0.15, tipo="lognormal"),
        "fator_cisterna": lambda: normal(0.15, tipo="lognormal"),
        "fator_om": lambda: normal(0.25, tipo="lognormal"),
        "inflacao_om_pct_mes": lambda: normal(0.10, lo=-5.0),
        "tma_pct_mes": lambda: normal(0.25),
        "periodo_analise_anos": lambda: Distribuicao("triangular", media=x, desvio=5.0, minimo=max(1.0, x - 5.0),
                                                     moda=x, maximo=x + 5.0, limite_inferior=1.0, variar=liga),
        "fator_emissao_agua": lambda: normal(0.20),
        "fator_emissao_rede": lambda: normal(0.20),
    }
    return regras[chave]()


def padroes_do_projeto(cfg) -> ParametrosIncertos:
    """Todo o catálogo com distribuições de triagem; ligadas só as três de consumo."""
    return ParametrosIncertos(variaveis={k: distribuicao_de_triagem(cfg, k) for k in CATALOGO})


def sortear_amostras(cfg, parametros: ParametrosIncertos, n: int, semente: Optional[int]) -> List[Dict[str, float]]:
    """As ``n`` amostras de todas as variáveis do catálogo; as que não variam ficam com o valor do projeto."""
    parametros.validar()
    gerador = np.random.default_rng(semente)
    colunas = {}
    for chave in CATALOGO:
        dist = parametros.variaveis.get(chave)
        if dist is not None and dist.variar:
            colunas[chave] = dist.sortear(gerador, n)
        else:
            colunas[chave] = np.full(n, valor_do_projeto(cfg, chave))
    colunas["pessoas"] = np.maximum(1.0, np.rint(colunas["pessoas"]))
    colunas["fracao_nao_potavel_pct"] = np.clip(colunas["fracao_nao_potavel_pct"], 0.0, 100.0)
    colunas["coef_escoamento"] = np.clip(colunas["coef_escoamento"], 0.0, 1.0)
    colunas["periodo_analise_anos"] = np.maximum(1.0, np.rint(colunas["periodo_analise_anos"]))
    for chave in ("per_capita_l_dia", "demanda_externa_l_dia", "area_m2", "descarte_mm", "fator_chuva",
                  "fator_tarifa", "fator_esgoto", "tarifa_energia", "fator_investimento", "fator_cisterna",
                  "fator_om", "fator_emissao_agua", "fator_emissao_rede"):
        colunas[chave] = np.maximum(0.0, colunas[chave])
    # Uma semente por realização para a variação diária, tirada do mesmo gerador.
    sementes_diarias = gerador.integers(0, 2 ** 31 - 1, n)
    amostras = [{**{k: float(colunas[k][i]) for k in CATALOGO}, "semente_diaria": int(sementes_diarias[i])}
                for i in range(n)]
    # O modelo climático é sorteado por último, para não mudar os demais sorteios da mesma semente.
    modelos = list(parametros.modelos_climaticos)
    if modelos:
        indices = gerador.integers(0, len(modelos), n)
        for amostra, j in zip(amostras, indices):
            amostra["modelo_climatico"] = modelos[int(j)]
    return amostras


def _escala(lista, fator: float, teto: Optional[float] = None, inteiro: bool = False):
    if not lista:
        return lista
    saida = []
    for v in lista:
        x = float(v) * fator
        if teto is not None:
            x = min(x, teto)
        saida.append(max(1, int(round(x))) if inteiro else x)
    return saida


#: Códigos de faixa cujo valor é dinheiro (o expoente, código 3, não se multiplica).
_CODIGOS_MONETARIOS = (-3, -2, -1, 0, 1, 2)


def aplicar_amostra(cfg, amostra: Dict[str, float], n_dias: int = 0, cv_diario_pct: float = 0.0):
    """Cópia do projeto com os valores da amostra.

    Demanda: troca o per capita, as pessoas, a fração interna e a demanda externa e
    recalcula a fração total atendível (`fracao_atendivel.fracao_total`); nos modos
    semanal, mensal e diário, as séries recebem o fator da amostra sobre o valor do
    projeto (o perfil se mantém, o nível muda). Captação e economia: troca o campo, ou
    multiplica (tarifas, investimento). O fator da chuva é aplicado à série em `simular`.
    Variável ausente da amostra fica com o valor do projeto.
    """
    novo = copy.deepcopy(cfg)
    a = {k: amostra.get(k, valor_do_projeto(cfg, k)) for k in CATALOGO}
    pc0, n0 = valor_do_projeto(cfg, "per_capita_l_dia"), valor_do_projeto(cfg, "pessoas")
    fi0 = valor_do_projeto(cfg, "fracao_nao_potavel_pct") / 100.0
    pc, n, fi = a["per_capita_l_dia"], a["pessoas"], a["fracao_nao_potavel_pct"] / 100.0
    f_pc = pc / pc0 if pc0 > 0 else 1.0
    f_n = n / n0 if n0 > 0 else 1.0
    f_fi = fi / fi0 if fi0 > 0 else 1.0

    novo.demand_value = pc
    novo.residents_count = int(n)
    novo.non_potable_indoor_share = fi
    novo.potable_indoor_share = 1.0 - fi
    for nome in ("demand_monthly", "weekly_demands", "daily_demands"):
        setattr(novo, nome, _escala(getattr(cfg, nome, None), f_pc))
    for nome in ("residents_monthly", "weekly_residents"):
        setattr(novo, nome, _escala(getattr(cfg, nome, None), f_n, inteiro=True))
    novo.daily_residents = _escala(getattr(cfg, "daily_residents", None), f_n)
    for nome in ("monthly_shares", "weekly_shares", "daily_shares"):
        lista = getattr(cfg, nome, None)
        teto = 100.0 if lista and max(float(v) for v in lista) > 1.0 else 1.0
        setattr(novo, nome, _escala(lista, f_fi, teto=teto))

    de = a["demanda_externa_l_dia"]
    novo.irrigation_liters_per_day = de
    novo.rainwater_share = fracao_total(pc * n, fi, de)
    try:
        novo._fracoes_lidas = (novo.rainwater_share, fi, de)
    except AttributeError:
        pass

    novo.area = a["area_m2"]
    novo.runoff_coeff = a["coef_escoamento"]
    novo.discard = a["descarte_mm"]
    if a["fator_tarifa"] != 1.0:
        novo.water_tariffs = [(f[0], f[1], float(f[2]) * a["fator_tarifa"] if int(f[3]) in _CODIGOS_MONETARIOS
                               else f[2], f[3]) for f in (cfg.water_tariffs or [])]
    # Esgoto em R$ (fixo ou por m³) acompanha o fator das tarifas; em % da água, já acompanha a
    # água. O fator do esgoto multiplica a tarifa de esgoto em qualquer modo.
    f_esgoto = a["fator_esgoto"] * (a["fator_tarifa"] if int(getattr(cfg, "sewage_mode", 1)) in (0, 2, 3) else 1.0)
    if f_esgoto != 1.0:
        novo.sewage_rate = float(cfg.sewage_rate) * f_esgoto
        novo.sewage_tariffs = [(f[0], f[1], float(f[2]) * f_esgoto) for f in (getattr(cfg, "sewage_tariffs", None) or [])]
    if a["reajuste_tarifa_pct"] != valor_do_projeto(cfg, "reajuste_tarifa_pct"):
        novo.water_tariff_escalation = a["reajuste_tarifa_pct"]
        novo.sewage_tariff_escalation = a["reajuste_tarifa_pct"]
    novo.elec_tariff = a["tarifa_energia"]
    novo.elec_tariff_escalation = a["reajuste_energia_pct"]
    novo.inflation = a["inflacao_om_pct_mes"]
    novo.tma = a["tma_pct_mes"]
    novo.analysis_period_years = int(round(a["periodo_analise_anos"]))
    setattr(novo, ATRIBUTO_FATOR_DE_INVESTIMENTO, a["fator_investimento"])
    setattr(novo, ATRIBUTO_FATOR_DA_CISTERNA, a["fator_cisterna"])
    setattr(novo, ATRIBUTO_FATOR_DE_OM, a["fator_om"])

    if cv_diario_pct > 0 and n_dias > 0 and (getattr(cfg, "demand_mode", "constant") or "constant") == "constant":
        from triton.core.demanda_estocastica import PerfilDeConsumo, sortear_demanda
        gerador = np.random.default_rng(int(amostra.get("semente_diaria", 0)))
        perfil = PerfilDeConsumo(media_l_dia=pc, cv_pct=cv_diario_pct, distribuicao="lognormal")
        novo.demand_mode = "daily"
        novo.daily_demands = sortear_demanda(perfil, n_dias, gerador).tolist()
        novo.daily_residents = [float(n)] * n_dias
        novo.daily_shares = []
    return novo


def estatisticas(valores: Sequence[float]) -> Dict[str, Optional[float]]:
    """Média, desvio-padrão amostral, coeficiente de variação (%) e percentis P5, P50 e P95."""
    v = np.asarray([x for x in valores if x is not None and np.isfinite(x)], dtype=float)
    if v.size == 0:
        return {"n": 0, "media": None, "desvio": None, "cv_pct": None, **{f"p{p}": None for p in PERCENTIS}}
    media = float(v.mean())
    desvio = float(v.std(ddof=1)) if v.size > 1 else 0.0
    return {"n": int(v.size), "media": media, "desvio": desvio,
            "cv_pct": 100.0 * desvio / abs(media) if media else None,
            **{f"p{p}": float(np.percentile(v, p)) for p in PERCENTIS}}


def intervalo_de_wilson(sucessos: int, n: int, z: float = 1.959964) -> Dict[str, Optional[float]]:
    """Proporção (%) e intervalo de confiança de 95% de Wilson, adequado a N pequeno e a 0% ou 100%."""
    if n <= 0:
        return {"pct": None, "ic95_inf": None, "ic95_sup": None}
    p = sucessos / n
    centro = (p + z * z / (2 * n)) / (1 + z * z / n)
    meia = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / (1 + z * z / n)
    return {"pct": 100.0 * p, "ic95_inf": 100.0 * max(0.0, centro - meia), "ic95_sup": 100.0 * min(1.0, centro + meia)}


def _percentis(valores: Sequence[float]) -> Dict[str, Optional[float]]:
    v = np.asarray([x for x in valores if x is not None and np.isfinite(x)], dtype=float)
    if v.size == 0:
        return {f"p{p}": None for p in PERCENTIS}
    return {f"p{p}": float(np.percentile(v, p)) for p in PERCENTIS}


def _postos(x: np.ndarray) -> np.ndarray:
    ordem = np.argsort(x, kind="mergesort")
    postos = np.empty(len(x), dtype=float)
    postos[ordem] = np.arange(len(x), dtype=float)
    # Empates recebem o posto médio.
    _, inverso, contagem = np.unique(x, return_inverse=True, return_counts=True)
    soma = np.bincount(inverso, weights=postos)
    return soma[inverso] / contagem[inverso]


def spearman(x: Sequence[float], y: Sequence[float]) -> Optional[float]:
    """Correlação de postos; None quando uma das séries não varia."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    x, y = x[ok], y[ok]
    if len(x) < 3 or np.ptp(x) == 0 or np.ptp(y) == 0:
        return None
    rx, ry = _postos(x), _postos(y)
    return float(np.corrcoef(rx, ry)[0, 1])


def razao_de_correlacao(categorias: Sequence[str], y: Sequence[float]) -> Optional[float]:
    """η²: fração da variância de ``y`` explicada pela categoria (aqui, o modelo climático).

    É o análogo, para uma variável categórica, do quadrado de uma correlação: 0 quando a
    média é a mesma em todas as categorias, 1 quando toda a variação está entre elas.
    """
    y = np.asarray(y, dtype=float)
    cats = np.asarray(list(categorias), dtype=object)
    ok = np.isfinite(y)
    y, cats = y[ok], cats[ok]
    if len(y) < 3 or np.ptp(y) == 0 or len(set(cats)) < 2:
        return None
    media = y.mean()
    entre = sum(len(y[cats == c]) * (y[cats == c].mean() - media) ** 2 for c in set(cats))
    return float(entre / ((y - media) ** 2).sum())


def classes_por_decil(x: Sequence[float]) -> List[str]:
    """Cada valor na sua classe: o próprio valor, se há até dez distintos; senão, o decil.

    Com as classes, o η² de uma variável contínua estima o índice de sensibilidade de
    primeira ordem, Var(E[Y|X])/Var(Y) (Saltelli et al., 2008), na mesma escala do η² do
    modelo climático.
    """
    x = np.asarray(x, dtype=float)
    if len(np.unique(x)) <= 10:
        return [f"{v:.12g}" for v in x]
    cortes = np.unique(np.percentile(x, np.arange(10, 100, 10)))
    return [str(int(c)) for c in np.searchsorted(cortes, x, side="right")]


def pode_sortear_modelos(cfg) -> bool:
    """A chuva do projeto vem da base CLIMBra (só ela tem os 19 modelos para a mesma cidade)."""
    return (getattr(cfg, "climate_source_mode", "national_db") or "national_db") == "national_db"


def series_dos_modelos_climaticos(cfg, modelos: Sequence[str]) -> Dict[str, np.ndarray]:
    """A série diária de cada modelo, com a cidade, o cenário e o recorte de datas do projeto."""
    if not pode_sortear_modelos(cfg):
        raise ValueError("O sorteio entre modelos climáticos pede a chuva da base CLIMBra (etapa 1); "
                         "este projeto usa um arquivo próprio.")
    from triton.core.climate_database import load_national_climate_series
    series = {}
    for modelo in modelos:
        series[modelo] = load_national_climate_series(
            cfg.climate_city_name, modelo, cfg.climate_scenario,
            cfg.climate_start_date, cfg.climate_end_date)[0]
    return series


def _otimo_economico(economicas: List[dict], volumes: List[float]) -> Optional[float]:
    """Menor payback descontado entre os que se pagam; desempate pelo maior VPL e pelo menor volume."""
    from triton.core.topsis import payback_do_criterio
    melhores = []
    for vol, e in zip(volumes, economicas):
        meses = e.get("discounted_payback_months")
        pb = payback_do_criterio(meses / 12.0 if meses is not None else None, e.get("npv_brl"))
        if vol > 0 and pb is not None:
            melhores.append((pb, -float(e.get("npv_brl") or 0.0), vol))
    return min(melhores)[2] if melhores else None


def _resumo_de_uma_realizacao(relatorio: Dict[str, Any]) -> Dict[str, Any]:
    tecnicas = relatorio["technical"]["alternatives"]
    economicas = relatorio.get("economic", {}).get("alternatives", [])
    ambientais = relatorio.get("environmental", {}).get("alternatives", [])
    volumes = [float(t["lower_tank_volume_l"]) for t in tecnicas]
    return {
        "volumes": volumes,
        "potencial": [float(t["potable_savings_pct"]) for t in tecnicas],
        "vpl": [float(e["npv_brl"]) for e in economicas],
        "payback_meses": [e.get("discounted_payback_months") for e in economicas],
        "co2": [float(a["lifetime_net_co2_saved_kg"]) for a in ambientais],
        "ideal_tecnico": relatorio["technical"]["summary"].get("optimal_volume_l"),
        "otimo_economico": _otimo_economico(economicas, volumes),
        "vencedor_topsis": (relatorio.get("topsis") or {}).get("best_volume_l"),
    }


def simular(
    cfg,
    precip: Sequence[float],
    parametros: ParametrosIncertos,
    *,
    amostras: int = 1000,
    semente: Optional[int] = 42,
    ao_progredir: Optional[Callable[[int, int], None]] = None,
    cancelar: Optional[Callable[[], bool]] = None,
    analise: Optional[Callable[..., Dict[str, Any]]] = None,
    pesos: Optional[Sequence[float]] = None,
    ambiental: Optional[Dict[str, Any]] = None,
    series_dos_modelos: Optional[Dict[str, Sequence[float]]] = None,
) -> Dict[str, Any]:
    """Refaz o estudo ``amostras`` vezes, cada uma com as variáveis escolhidas sorteadas.

    ``analise`` é a cadeia completa do programa (por padrão, `triton.cli.run_analysis`,
    a mesma da linha de comando e conferida contra a interface). ``cancelar`` é
    consultado entre realizações; cancelado, o resultado traz só as já feitas.
    ``pesos`` (TOPSIS) e ``ambiental`` (parâmetros da avaliação ambiental) são os do
    projeto, os mesmos que a linha de comando lê do arquivo. Com modelos climáticos
    escolhidos, ``series_dos_modelos`` traz a série de cada um; ausente, elas são lidas da
    base CLIMBra com a cidade, o cenário e o recorte do projeto (`series_dos_modelos_climaticos`).
    O caso-base usa sempre a série do projeto.
    """
    if amostras < 1:
        raise ValueError("É preciso ao menos uma realização.")
    parametros.validar()
    if analise is None:
        from triton.cli import run_analysis as analise
    serie = np.asarray(precip, dtype=float)
    series: Dict[str, np.ndarray] = {}
    if parametros.modelos_climaticos:
        if series_dos_modelos is None:
            series_dos_modelos = series_dos_modelos_climaticos(cfg, parametros.modelos_climaticos)
        faltam = [m for m in parametros.modelos_climaticos if m not in series_dos_modelos]
        if faltam:
            raise ValueError(f"Falta a série de chuva dos modelos: {', '.join(faltam)}.")
        series = {m: np.asarray(series_dos_modelos[m], dtype=float) for m in parametros.modelos_climaticos}
    extras: Dict[str, Any] = {"smaa": False}
    if pesos is not None:
        extras["weights"] = tuple(float(p) for p in pesos)
    if ambiental:
        extras["environmental"] = ambiental
    emissao_base = None
    if any(k in parametros.ativas() for k in ("fator_emissao_agua", "fator_emissao_rede")):
        from triton.cli import fatores_de_emissao
        emissao_base = fatores_de_emissao(ambiental)

    def rodar(c, chuva, amostra=None):
        kw = extras
        if emissao_base is not None and amostra is not None:
            kw = {**extras, "environmental": {
                **(ambiental or {}),
                "potable_water_co2_kg_m3": emissao_base["potable_water_co2_kg_m3"] * amostra["fator_emissao_agua"],
                "grid_co2_factor_kg_kwh": emissao_base["grid_co2_factor_kg_kwh"] * amostra["fator_emissao_rede"]}}
        return _resumo_de_uma_realizacao(analise(c, chuva, "all", **kw))

    base = rodar(copy.deepcopy(cfg), serie)
    sorteios = sortear_amostras(cfg, parametros, amostras, semente)
    realizacoes: List[Dict[str, Any]] = []
    for i, amostra in enumerate(sorteios):
        if cancelar is not None and cancelar():
            break
        bruta = series[amostra["modelo_climatico"]] if "modelo_climatico" in amostra else serie
        chuva = bruta * amostra["fator_chuva"] if amostra["fator_chuva"] != 1.0 else bruta
        r = rodar(aplicar_amostra(cfg, amostra, len(chuva), parametros.cv_diario_pct), chuva, amostra)
        if r["volumes"] != base["volumes"]:
            raise RuntimeError("A grade de volumes mudou entre realizações; a comparação deixaria de ser pareada.")
        realizacoes.append({**r, "amostra": amostra})
        if ao_progredir is not None:
            ao_progredir(i + 1, amostras)
    return agregar(base, realizacoes, parametros, semente, amostras)


def agregar(base: Dict[str, Any], realizacoes: List[Dict[str, Any]], parametros: ParametrosIncertos,
            semente: Optional[int], pedidas: int) -> Dict[str, Any]:
    """O painel de robustez a partir das realizações feitas."""
    volumes = base["volumes"]
    n = len(realizacoes)
    por_volume = []
    for j, vol in enumerate(volumes):
        pot = [r["potencial"][j] for r in realizacoes]
        vpl = [r["vpl"][j] for r in realizacoes] if base["vpl"] else []
        co2 = [r["co2"][j] for r in realizacoes] if base["co2"] else []
        pb = [r["payback_meses"][j] for r in realizacoes] if base["payback_meses"] else []
        por_volume.append({
            "volume_l": vol,
            "base": {"potencial_pct": base["potencial"][j],
                     "vpl_brl": base["vpl"][j] if base["vpl"] else None,
                     "co2_kg": base["co2"][j] if base["co2"] else None},
            "potencial_pct": _percentis(pot),
            "vpl_brl": _percentis(vpl),
            "payback_meses": _percentis([p for p in pb if p is not None]),
            "co2_kg": _percentis(co2),
            "prob_vpl_positivo_pct": 100.0 * sum(v > 0 for v in vpl) / n if n and vpl else None,
            "prob_co2_positivo_pct": 100.0 * sum(c > 0 for c in co2) / n if n and co2 else None,
        })

    def frequencia(chave: str) -> Dict[str, float]:
        cont: Dict[str, int] = {}
        for r in realizacoes:
            v = r.get(chave)
            rotulo = "nenhum" if v is None else f"{float(v):.0f}"
            cont[rotulo] = cont.get(rotulo, 0) + 1
        ordem = sorted(cont.items(), key=lambda kv: (kv[0] == "nenhum", float(kv[0]) if kv[0] != "nenhum" else 0.0))
        return {k: 100.0 * c / n for k, c in ordem} if n else {}

    # Referência: o volume que o estudo escolheu (vencedor TOPSIS do caso-base, ou o ideal técnico).
    ref = base.get("vencedor_topsis") or base.get("ideal_tecnico") or (volumes[-1] if volumes else None)
    j_ref = min(range(len(volumes)), key=lambda j: abs(volumes[j] - float(ref))) if ref is not None and volumes else None

    ativas = parametros.ativas()
    sensibilidade = {}
    if j_ref is not None and n >= 3:
        for nome in ativas:
            xs = [r["amostra"][nome] for r in realizacoes]
            sensibilidade[nome] = {
                "potencial_pct": spearman(xs, [r["potencial"][j_ref] for r in realizacoes]),
                "vpl_brl": spearman(xs, [r["vpl"][j_ref] for r in realizacoes]) if base["vpl"] else None,
                "co2_kg": spearman(xs, [r["co2"][j_ref] for r in realizacoes]) if base["co2"] else None,
            }

    # Convergência: média acumulada do VPL no volume de referência e o seu intervalo de 95%
    # (erro-padrão de Monte Carlo, desvio/√k). A faixa que estreita diz se o N basta.
    convergencia = []
    if j_ref is not None and base["vpl"] and n >= 5:
        passo = max(1, n // 40)
        for k in range(max(5, passo), n + 1, passo):
            v = np.asarray([r["vpl"][j_ref] for r in realizacoes[:k]], dtype=float)
            erro = float(v.std(ddof=1) / math.sqrt(k)) if k > 1 else 0.0
            convergencia.append({"realizacoes": k, "vpl_media": float(v.mean()),
                                 "ic95_inf": float(v.mean() - 1.959964 * erro),
                                 "ic95_sup": float(v.mean() + 1.959964 * erro),
                                 "vpl_p50": float(np.median(v))})

    referencia = {}
    if j_ref is not None:
        def col(chave):
            return [r[chave][j_ref] for r in realizacoes] if base[chave] else []
        pb = [m / 12.0 for m in col("payback_meses") if m is not None]
        vpl_ref, co2_ref = col("vpl"), col("co2")
        pb_base = base["payback_meses"][j_ref] if base["payback_meses"] else None
        referencia = {
            "volume_l": volumes[j_ref],
            "base": {"potencial_pct": base["potencial"][j_ref],
                     "vpl_brl": base["vpl"][j_ref] if base["vpl"] else None,
                     "payback_anos": pb_base / 12.0 if pb_base is not None else None,
                     "co2_kg": base["co2"][j_ref] if base["co2"] else None},
            "potencial_pct": estatisticas(col("potencial")),
            "vpl_brl": estatisticas(vpl_ref),
            "payback_anos": estatisticas(pb),
            "co2_kg": estatisticas(co2_ref),
            "prob_vpl_positivo": intervalo_de_wilson(sum(v > 0 for v in vpl_ref), n) if vpl_ref else None,
            "prob_co2_positivo": intervalo_de_wilson(sum(c > 0 for c in co2_ref), n) if co2_ref else None,
            "realizacoes_que_se_pagam": len(pb),
        }

    # As variáveis sorteadas: o que de fato entrou (média, desvio, percentis da amostra).
    entradas = {nome: estatisticas([r["amostra"][nome] for r in realizacoes]) for nome in ativas}

    # O modelo climático: quantas vezes saiu cada um, o resultado no volume de referência com
    # cada um e o η², a parte da variância explicada pelo modelo.
    modelos = list(parametros.modelos_climaticos)
    por_modelo, sensibilidade_modelo = [], {}
    if modelos and j_ref is not None and n:
        sorteados = [r["amostra"].get("modelo_climatico") for r in realizacoes]
        for m in modelos:
            rs = [r for r, s in zip(realizacoes, sorteados) if s == m]
            vpl_m = [r["vpl"][j_ref] for r in rs] if base["vpl"] else []
            por_modelo.append({
                "modelo": m, "realizacoes": len(rs),
                "potencial_pct": estatisticas([r["potencial"][j_ref] for r in rs]),
                "vpl_brl": estatisticas(vpl_m),
                "prob_vpl_positivo": intervalo_de_wilson(sum(v > 0 for v in vpl_m), len(rs)) if vpl_m else None,
            })
        sensibilidade_modelo = {
            "potencial_pct": razao_de_correlacao(sorteados, [r["potencial"][j_ref] for r in realizacoes]),
            "vpl_brl": razao_de_correlacao(sorteados, [r["vpl"][j_ref] for r in realizacoes]) if base["vpl"] else None,
            "co2_kg": razao_de_correlacao(sorteados, [r["co2"][j_ref] for r in realizacoes]) if base["co2"] else None,
        }

    # Parte da variância explicada (η²) por cada fonte, na mesma escala: o modelo pelas suas
    # categorias, as variáveis contínuas pelos decis.
    variancia_explicada: Dict[str, Dict[str, Optional[float]]] = {}
    if j_ref is not None and n >= 10:
        fontes = {nome: classes_por_decil([r["amostra"][nome] for r in realizacoes]) for nome in ativas}
        if modelos:
            fontes["modelo_climatico"] = [str(r["amostra"].get("modelo_climatico")) for r in realizacoes]
        for nome, classes in fontes.items():
            variancia_explicada[nome] = {
                "potencial_pct": razao_de_correlacao(classes, [r["potencial"][j_ref] for r in realizacoes]),
                "vpl_brl": razao_de_correlacao(classes, [r["vpl"][j_ref] for r in realizacoes]) if base["vpl"] else None,
                "co2_kg": razao_de_correlacao(classes, [r["co2"][j_ref] for r in realizacoes]) if base["co2"] else None,
            }

    return {
        "schema": {"name": "triton-modulacao-estocastica", "version": 3},
        "semente": semente,
        "realizacoes_pedidas": pedidas,
        "realizacoes_feitas": n,
        "cancelado": n < pedidas,
        "parametros": parametros.para_dict(),
        "variaveis_ativas": ativas,
        "entradas": entradas,
        "volume_de_referencia_l": volumes[j_ref] if j_ref is not None else None,
        "referencia": referencia,
        "caso_base": {"ideal_tecnico_l": base["ideal_tecnico"], "otimo_economico_l": base["otimo_economico"],
                      "vencedor_topsis_l": base["vencedor_topsis"]},
        "por_volume": por_volume,
        "frequencia_pct": {"ideal_tecnico": frequencia("ideal_tecnico"),
                           "otimo_economico": frequencia("otimo_economico"),
                           "vencedor_topsis": frequencia("vencedor_topsis")},
        "sensibilidade_spearman": sensibilidade,
        "modelos_climaticos": modelos,
        "por_modelo": por_modelo,
        "sensibilidade_modelo_eta2": sensibilidade_modelo,
        "variancia_explicada_eta2": variancia_explicada,
        "convergencia": convergencia,
        "amostras": [{**{k: r["amostra"][k] for k in ativas},
                      **({"modelo_climatico": r["amostra"].get("modelo_climatico")} if modelos else {}),
                      "ideal_tecnico_l": r["ideal_tecnico"], "otimo_economico_l": r["otimo_economico"],
                      "vencedor_topsis_l": r["vencedor_topsis"],
                      "economia_ref_pct": r["potencial"][j_ref] if j_ref is not None else None,
                      "vpl_ref_brl": r["vpl"][j_ref] if j_ref is not None and r["vpl"] else None,
                      "co2_ref_kg": r["co2"][j_ref] if j_ref is not None and r["co2"] else None}
                     for r in realizacoes],
    }
