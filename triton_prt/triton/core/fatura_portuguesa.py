# -*- coding: utf-8 -*-
"""A fatura portuguesa de água, saneamento e resíduos, nos campos do motor tarifário.

Uma fatura doméstica em Portugal soma, por mês, a água (tarifa fixa e escalões por m³), o
saneamento e os resíduos urbanos (tarifa fixa e tarifa variável, em regra indexada ao m³ de
água consumido), a taxa de recursos hídricos (por m³) e o IVA de cada parcela, à taxa que o
tarifário declara. Nenhuma taxa de IVA fica no código: cada parcela leva a do documento.

O motor (``economic.calculate_water_bill``) conhece água por faixas, esgoto (fixo, % da água
ou por m³), uma taxa fixa e uma taxa % sobre a água. A fatura cabe nele sem perda:

- água: escalões → ``water_tariffs``; IVA da água → ``water_tax_var`` (% sobre a parcela
  de água, tarifa fixa incluída);
- parcelas variáveis indexadas ao m³ de água (saneamento, resíduos, TRH), cada uma com o seu
  IVA → um preço único por m³ no esgoto por m³ (``sewage_mode`` 2), que é a parte que
  reajusta pelo índice do esgoto;
- saneamento por escalões (Lisboa, Porto, Guarda...): escalões próprios sobre o volume
  recolhido (coeficiente de recolha × água; Lisboa, 90%) → esgoto por escalões
  (``sewage_mode`` 3). A TRH do saneamento e o IVA entram no preço de cada escalão, e as
  parcelas por m³ de água, divididas pelo coeficiente, também: tudo é linear no volume, e
  a conta sai igual à soma parcela a parcela;
- tarifas fixas das demais parcelas, com IVA → ``water_tax_fixed`` (não variam com o
  consumo e se anulam na economia; entram para a conta mensal sair igual à impressa).

``conta_mensal`` soma a fatura parcela a parcela, independentemente do motor;
``tests/test_essencial.py`` exige que o motor, com os campos de ``aplicar_ao_projeto``,
reproduza essa soma em qualquer volume.

Resíduos por escalões (Funchal) ainda não têm campo: entram só por m³ único.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

#: Modo do esgoto «preço por m³ de água consumido» (triton/core/tariffs_structure.py).
_ESGOTO_POR_M3, _ESGOTO_POR_FAIXAS = 2, 3


@dataclass
class Escalao:
    """Escalão de água: de ``inicio`` a ``fim`` m³/mês (``None`` = sem limite), a ``preco`` por m³."""
    inicio: float
    fim: Optional[float]
    preco: float


@dataclass
class Parcela:
    """Saneamento, resíduos, TRH ou outra parcela da fatura que não é a água.

    ``fixa`` é o valor por mês; ``por_m3``, o preço por m³ de água consumido. ``iva_pct`` é
    a taxa que o tarifário declara para a parcela (0 se ela não leva IVA).
    """
    nome: str
    fixa: float = 0.0
    por_m3: float = 0.0
    iva_pct: float = 0.0


@dataclass
class FaturaPortuguesa:
    entidade: str
    concelho: str
    fixa_agua: float
    escaloes: List[Escalao]
    iva_agua_pct: float
    parcelas: List[Parcela] = field(default_factory=list)
    #: Saneamento por escalões sobre o volume recolhido (coef_recolha × água), com a TRH do
    #: saneamento por m³ recolhido. Vazio = saneamento, se houver, vai em ``parcelas``.
    saneamento_escaloes: List[Escalao] = field(default_factory=list)
    saneamento_fixa: float = 0.0
    saneamento_trh_m3: float = 0.0
    coef_recolha: float = 1.0
    iva_saneamento_pct: float = 0.0
    fonte: str = ""
    vigencia: str = ""

    def validar(self) -> None:
        if not self.escaloes:
            raise ValueError("A fatura precisa de pelo menos um escalão de água.")
        _validar_escaloes(self.escaloes, "água")
        for p in self.parcelas:
            if min(p.fixa, p.por_m3, p.iva_pct) < 0:
                raise ValueError(f"Valor negativo na parcela «{p.nome}».")
        if self.iva_agua_pct < 0:
            raise ValueError("IVA da água negativo.")
        if self.saneamento_escaloes:
            _validar_escaloes(self.saneamento_escaloes, "saneamento")
        if not 0 < self.coef_recolha <= 1.0:
            raise ValueError("O coeficiente de recolha fica entre 0 e 1.")
        if min(self.saneamento_fixa, self.saneamento_trh_m3, self.iva_saneamento_pct) < 0:
            raise ValueError("Valor negativo no saneamento.")


def _validar_escaloes(escaloes: List[Escalao], servico: str) -> None:
    anterior = 0.0
    for e in escaloes:
        if abs(e.inicio - anterior) > 1e-9:
            raise ValueError(f"Os escalões de {servico} precisam ser contíguos desde 0 m³; "
                             f"há um salto em {anterior} m³.")
        if e.preco < 0:
            raise ValueError("Preço de escalão negativo.")
        if e.fim is None:
            return
        if e.fim <= e.inicio:
            raise ValueError(f"Escalão {e.inicio}–{e.fim} m³ vazio ou invertido.")
        anterior = e.fim
    raise ValueError(f"O último escalão de {servico} precisa ficar sem limite superior.")


def _pelos_escaloes(escaloes: List[Escalao], m3: float) -> float:
    total = 0.0
    for e in escaloes:
        topo = m3 if e.fim is None else min(m3, e.fim)
        if topo > e.inicio:
            total += (topo - e.inicio) * e.preco
    return total


def _com_iva(valor: float, iva_pct: float) -> float:
    return valor * (1.0 + iva_pct / 100.0)


def conta_mensal(f: FaturaPortuguesa, m3: float) -> float:
    """A conta de um mês com ``m3`` de água, somada parcela a parcela (referência)."""
    f.validar()
    total = _com_iva(f.fixa_agua + _pelos_escaloes(f.escaloes, m3), f.iva_agua_pct)
    if f.saneamento_escaloes:
        recolhido = f.coef_recolha * m3
        total += _com_iva(f.saneamento_fixa + _pelos_escaloes(f.saneamento_escaloes, recolhido)
                          + f.saneamento_trh_m3 * recolhido, f.iva_saneamento_pct)
    for p in f.parcelas:
        total += _com_iva(p.fixa + p.por_m3 * m3, p.iva_pct)
    return total


def campos_do_motor(f: FaturaPortuguesa) -> dict:
    """Os campos tarifários do projeto que reproduzem a fatura (argumentos de ``calculate_water_bill``)."""
    f.validar()
    faixas = [(0.0, 0.0, float(f.fixa_agua), -1)] if f.fixa_agua else []
    faixas += [(float(e.inicio), float(e.fim if e.fim is not None else 999999.0), float(e.preco), 1)
               for e in f.escaloes]
    por_m3 = sum(_com_iva(p.por_m3, p.iva_pct) for p in f.parcelas)
    fixas = sum(_com_iva(p.fixa, p.iva_pct) for p in f.parcelas)
    campos = {"tariffs": faixas, "water_tax_var": float(f.iva_agua_pct),
              "sewage_mode": _ESGOTO_POR_M3, "sewage_rate": por_m3, "water_tax_fixed": fixas,
              "sewage_tariffs": [], "sewage_volume_factor": 1.0}
    if f.saneamento_escaloes:
        # Por m³ recolhido: escalão + TRH, com o IVA do saneamento; as parcelas por m³ de água
        # valem por m³ recolhido divididas pelo coeficiente.
        extra = por_m3 / f.coef_recolha
        campos.update(
            sewage_mode=_ESGOTO_POR_FAIXAS, sewage_rate=0.0,
            sewage_tariffs=[(float(e.inicio), None if e.fim is None else float(e.fim),
                             _com_iva(e.preco + f.saneamento_trh_m3, f.iva_saneamento_pct) + extra)
                            for e in f.saneamento_escaloes],
            sewage_volume_factor=float(f.coef_recolha),
            water_tax_fixed=fixas + _com_iva(f.saneamento_fixa, f.iva_saneamento_pct))
    return campos


def aplicar_ao_projeto(f: FaturaPortuguesa, cfg) -> None:
    """Grava a fatura nos campos tarifários do projeto."""
    c = campos_do_motor(f)
    cfg.water_tariffs = c["tariffs"]
    cfg.sewage_mode, cfg.sewage_rate = c["sewage_mode"], c["sewage_rate"]
    cfg.water_tax_fixed, cfg.water_tax_var = c["water_tax_fixed"], c["water_tax_var"]
    cfg.sewage_tariffs, cfg.sewage_volume_factor = c["sewage_tariffs"], c["sewage_volume_factor"]
