"""O percentual de esgoto tem de reproduzir a tarifa coletada.

O banco de execução guarda o esgoto como percentual da conta de água. A coleta
auditada, em `tarifas/tarifas_detalhadas_auditadas.csv`, tem a tarifa de esgoto
**por m³** para 543 municípios — dado mais primário que o percentual, e que o
percentual deveria reproduzir.

Em 89 deles não reproduzia: todos guardavam 80,0%, o valor de recurso, aplicado
onde a coleta trazia outro. O erro tem os dois sentidos e nenhum é pequeno:

| Município | Guardado | Coletado |
| :--- | ---: | ---: |
| Goiânia e mais 62 da SANEAGO | 80% | 100% |
| Blumenau | 80% | 112% |
| Caxias do Sul | 80% | 38% |

**Atenção ao denominador**, que é onde esta área produz erro: `esgoto_pct` é
percentual da tarifa de ÁGUA, não da fatura. A CASAN cobra 100% — o esgoto
iguala a água, e por isso responde por metade da fatura total. Como a parcela
de esgoto acompanha a de água metro cúbico a metro cúbico, um erro no
percentual se propaga inteiro para a economia atribuída ao sistema pluvial: em Goiânia a conta de esgoto saía 20%
abaixo, e portanto a economia também.

Catorze municípios têm percentual que **varia entre faixas** — Caxias do Sul de
21,6% a 69,9%. Nenhum número único representa essa estrutura, e por isso ficam
marcados em vez de corrigidos: é o caso que pede faixas próprias de esgoto, que o
motor ainda não tem.
"""

from __future__ import annotations

import collections
import csv
import os

import pytest

from netuno.core.tariffs_database import load_tariffs_db

CIDADES = load_tariffs_db()["cities"]

_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_CSV = os.path.join(_RAIZ, "tarifas", "tarifas_detalhadas_auditadas.csv")

#: Espalhamento acima do qual nenhum percentual único representa a estrutura.
ESPALHAMENTO_ACEITAVEL_PP = 5.0

#: Tolerância entre o percentual guardado e o que a coleta implica.
TOLERANCIA_PP = 2.0


def _numero(v):
    v = (v or "").strip().replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


@pytest.fixture(scope="module")
def razoes_coletadas():
    """Percentual esgoto/água implicado pela coleta, por município e faixa."""
    if not os.path.isfile(_CSV):
        pytest.skip("a coleta detalhada não está disponível nesta cópia")
    with open(_CSV, encoding="utf-8-sig") as f:
        linhas = list(csv.DictReader(f))

    razoes = collections.defaultdict(list)
    for l in linhas:
        agua, esgoto = _numero(l.get("tarifa_agua_r_m3")), _numero(l.get("tarifa_esgoto_r_m3"))
        if agua and esgoto and agua > 0:
            razoes[(l["uf"], l["municipio"])].append(100.0 * esgoto / agua)
    return razoes


@pytest.fixture(scope="module")
def por_nome():
    return {(c.get("uf"), c.get("municipio")): c for c in CIDADES.values()}


# ─────────────────── o percentual guardado bate com a coleta ───────────────────

def test_o_percentual_guardado_reproduz_a_tarifa_coletada(razoes_coletadas, por_nome):
    """A coleta por m³ é o dado primário; o percentual é derivado dele.

    Onde a coleta é consistente entre as faixas, os dois têm de concordar. Se
    divergirem, alguém aplicou o valor de recurso por cima do dado.
    """
    divergentes = []
    for chave, valores in razoes_coletadas.items():
        registro = por_nome.get(chave)
        if registro is None or registro.get("esgoto_pct") is None:
            continue
        if max(valores) - min(valores) > ESPALHAMENTO_ACEITAVEL_PP:
            continue        # varia por faixa; verificado no teste seguinte
        media = sum(valores) / len(valores)
        guardado = float(registro["esgoto_pct"])
        if abs(media - guardado) > TOLERANCIA_PP:
            divergentes.append(f"{chave[0]}/{chave[1]}: {guardado:.1f}% vs {media:.1f}%")
    assert not divergentes, divergentes[:8]


def test_os_de_percentual_variavel_estao_marcados(razoes_coletadas, por_nome):
    """Nenhum número único os representa, e o programa tem de dizer isso."""
    variaveis = [
        chave for chave, valores in razoes_coletadas.items()
        if max(valores) - min(valores) > ESPALHAMENTO_ACEITAVEL_PP
    ]
    assert variaveis, "a coleta deveria ter municípios com percentual variável"

    for chave in variaveis:
        registro = por_nome.get(chave)
        if registro is None:
            continue
        assert registro.get("esgoto_pct_varia_por_faixa") is True, chave
        assert registro.get("_ressalva_esgoto"), chave


def test_caxias_do_sul_e_o_caso_extremo(por_nome):
    """De 21,6% a 69,9% entre faixas: guardar 80% erra em qualquer consumo."""
    registro = por_nome.get(("RS", "Caxias do Sul"))
    assert registro is not None
    assert registro.get("esgoto_pct_varia_por_faixa") is True
    assert "21.6" in registro["_ressalva_esgoto"] or "21,6" in registro["_ressalva_esgoto"]


# ────────────────────────── sanidade do valor guardado ─────────────────────────

def test_todo_percentual_de_esgoto_e_plausivel():
    """Acima de 100% é legítimo, e a faixa observada vai de 50% a 140%.

    Onde a concessionária cobra coleta e tratamento em rubricas separadas, o
    esgoto passa da água: Mogi Mirim está em 140% pela Resolução ARES-PCJ
    706/2026, Ribeirão Preto em 127,5% e Campinas em 123%, todos consistentes em
    todas as faixas da coleta. O limite existe para pegar erro de digitação —
    um percentual gravado como fração, ou uma casa decimal a mais — e não para
    rejeitar a estrutura real.
    """
    for c in CIDADES.values():
        if c.get("esgoto_modo") != 1:
            continue
        pct = c.get("esgoto_pct")
        if pct is None:
            continue
        assert 0.0 <= float(pct) <= 150.0, (c.get("municipio"), pct)


def test_o_esgoto_acima_da_agua_e_raro_e_documentado():
    """Só quatro municípios passam de 110%, e todos vêm de resolução citada."""
    acima = [c for c in CIDADES.values()
             if c.get("esgoto_modo") == 1 and float(c.get("esgoto_pct") or 0) > 110.0]
    assert len(acima) <= 6, [c["municipio"] for c in acima]
    for c in acima:
        assert c.get("fonte_url"), c.get("municipio")


def test_o_esgoto_de_goias_e_pleno():
    """A SANEAGO cobra esgoto a 100% da água, e o banco guardava 80%."""
    goiania = next(c for c in CIDADES.values()
                   if c.get("municipio") == "Goiânia" and c.get("uf") == "GO")
    assert float(goiania["esgoto_pct"]) == pytest.approx(100.0, abs=0.5)


def test_toda_correcao_de_esgoto_esta_registrada():
    """Mudar tarifa sem dizer de onde veio não é auditável."""
    corrigidos = [c for c in CIDADES.values() if c.get("_correcao_esgoto")]
    assert len(corrigidos) >= 70
    for c in corrigidos:
        corr = c["_correcao_esgoto"]
        for campo in ("em", "de", "para", "origem", "motivo"):
            assert corr.get(campo) is not None, (c.get("municipio"), campo)
        assert corr["de"] != corr["para"]


def test_a_conta_de_esgoto_acompanha_o_percentual():
    """O elo entre o dado e o motor, que é o que torna a correção útil."""
    from netuno.core.economic import calculate_water_bill

    faixas = [[0.0, 999999.0, 5.0, 1]]
    so_agua = calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=0.0)
    com_80 = calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=80.0)
    com_100 = calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=100.0)

    assert com_80 == pytest.approx(so_agua * 1.80)
    assert com_100 == pytest.approx(so_agua * 2.00)
    # Os 20 pontos de diferença são 11% da fatura: é o tamanho do erro em Goiás.
    assert (com_100 - com_80) / com_100 == pytest.approx(0.10, abs=0.01)


# ─────────────────────── o denominador, que é onde se erra ─────────────────────

def test_o_percentual_e_da_tarifa_de_agua_e_nao_da_fatura():
    """Florianópolis é o caso concreto, e o que separa as duas leituras.

    A CASAN cobra `esgoto_pct = 100`. Isso NÃO quer dizer que o esgoto seja a
    fatura inteira: quer dizer que o esgoto **iguala a água**, e portanto responde
    por metade da fatura total. Os dois enunciados são o mesmo com denominadores
    diferentes, e trocá-los dobra ou divide pela metade a conta.
    """
    from netuno.core.economic import calculate_water_bill

    casan = next(c for c in CIDADES.values() if c.get("municipio") == "Florianópolis")
    assert float(casan["esgoto_pct"]) == pytest.approx(100.0)

    for m3 in (10, 15, 20, 30):
        agua = calculate_water_bill(m3 * 1000.0, casan["faixas"], sewage_mode=1, sewage_rate=0.0)
        total = calculate_water_bill(
            m3 * 1000.0, casan["faixas"], sewage_mode=1, sewage_rate=casan["esgoto_pct"]
        )
        esgoto = total - agua
        assert esgoto == pytest.approx(agua), m3          # 100% da ÁGUA
        assert esgoto / total == pytest.approx(0.50), m3  # 50% da FATURA


def test_o_denominador_vale_para_qualquer_percentual():
    """A regra geral: esgoto/fatura = pct / (100 + pct)."""
    from netuno.core.economic import calculate_water_bill

    faixas = [[0.0, 999999.0, 5.0, 1]]
    for pct in (38.0, 74.0, 80.0, 100.0, 140.0):
        agua = calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=0.0)
        total = calculate_water_bill(10_000.0, faixas, sewage_mode=1, sewage_rate=pct)
        esgoto = total - agua
        assert esgoto == pytest.approx(agua * pct / 100.0)
        assert esgoto / total == pytest.approx(pct / (100.0 + pct))
