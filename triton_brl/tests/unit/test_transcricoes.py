"""As transcrições de `tarifas/transcricoes/` contra os documentos e contra o banco.

Cada transcrição cita um documento guardado em `tarifas/fontes/` e traz, em
`conferencia`, contas de água calculadas com os números impressos no próprio documento.
O banco tem de reproduzi-las ao centavo, pelo mesmo cálculo que o programa usa. O
teste também segura a procedência: município com documento tem arquivo, vigência e
item do registro, e o atualizador automático não sobrescreve o que veio de documento.
"""

from __future__ import annotations

import glob
import json
import os
import sys
import unicodedata

import pytest

from triton.core.tariffs_database import get_city_tariffs_by_category, load_tariffs_db, procedencia_tarifaria
from triton.core.tariffs_structure import custo_volumetrico

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PASTA = os.path.join(RAIZ, "tarifas", "transcricoes")
REGISTRO = {i["id"]: i for i in json.load(open(os.path.join(RAIZ, "tarifas", "fontes", "registro.json"),
                                                 encoding="utf-8"))["itens"]}
TRANSCRICOES = [(os.path.basename(c), json.load(open(c, encoding="utf-8")))
                for c in sorted(glob.glob(os.path.join(PASTA, "*.json")))
                if os.path.basename(c) not in ("historico.json", "cobertura.json", "imagens_conferidas.json")]
CONFERENCIAS = [(nome, c) for nome, t in TRANSCRICOES for c in t.get("conferencia", [])]


def _conta_de_agua(dados: dict, consumo: float) -> float:
    """A conta de água (sem esgoto) que o motor do programa calcula, em qualquer regime."""
    from triton.core.economic import calculate_water_bill
    return calculate_water_bill(consumo * 1000.0, [tuple(f) for f in dados["faixas"]], 1, 0.0)


@pytest.mark.parametrize("nome,t", TRANSCRICOES, ids=[n for n, _ in TRANSCRICOES])
def test_a_transcricao_cita_um_documento_registrado_e_guardado(nome, t):
    assert t["registro"], nome
    arquivos = set()
    for id_ in t["registro"]:
        item = REGISTRO[id_]
        assert item["guardado_em"], (nome, id_)
        assert os.path.isfile(os.path.join(RAIZ, item["guardado_em"])), (nome, item["guardado_em"])
        arquivos.add(unicodedata.normalize("NFC", item["arquivo"]))
    assert unicodedata.normalize("NFC", t["documento"]) in arquivos, f"{nome}: «{t['documento']}» não é arquivo dos itens {t['registro']}"
    assert t["vigencia"] and t["fonte_url"] and t["leitura"]


@pytest.mark.parametrize("nome,c", CONFERENCIAS, ids=[f"{n}:{c['municipio']}:{c['categoria']}" for n, c in CONFERENCIAS])
def test_o_banco_reproduz_o_valor_impresso(nome, c):
    uf, municipio = c["municipio"].split(" - ", 1)
    vigente = load_tariffs_db()["cities"][c["municipio"]].get("fonte_transcricao", "")
    if not vigente.endswith("/" + nome):
        pytest.skip(f"substituída por {vigente} (vigência mais recente)")
    dados = get_city_tariffs_by_category(uf, municipio, c["categoria"])
    assert dados is not None, (nome, c)
    assert _conta_de_agua(dados, c["consumo_m3"]) == pytest.approx(c["conta_agua"], abs=0.02), c["impresso"]


def test_toda_transcricao_com_tabela_tem_conferencia():
    for nome, t in TRANSCRICOES:
        transcreve = any("residencial" in tab for tab in t["tabelas"])
        assert not transcreve or t.get("conferencia"), f"{nome}: transcrição sem valor impresso conferido"


def test_municipio_documentado_tem_procedencia_completa():
    cidades = load_tariffs_db()["cities"]
    documentados = [d for d in cidades.values() if d.get("fonte_registro")]
    assert len(documentados) > 300
    for d in documentados:
        assert d.get("fonte_documento") and d.get("vigencia_saneamento") and d.get("fonte_tabela"), d["municipio"]
        for id_ in d["fonte_registro"]:
            assert REGISTRO[id_]["situacao"] in ("transcrito", "consultado"), (d["municipio"], id_)


def test_o_atualizador_nao_sobrescreve_tarifa_documentada():
    from triton.core.tariff_updater.sanitation_scrapers import SanitationScraperRegistry

    dados = dict(load_tariffs_db()["cities"]["SP - São Paulo"])
    antes = json.dumps(dados, sort_keys=True)
    depois = SanitationScraperRegistry().update_city_sanitation("São Paulo", "SP", dados)
    assert json.dumps(depois, sort_keys=True) == antes


def test_a_tela_mostra_o_documento_ou_a_falta_dele():
    cidades = load_tariffs_db()["cities"]
    assert "NT_1__REAJUSTE" in procedencia_tarifaria(cidades["SP - São Paulo"])
    assert "Tabela 1" in procedencia_tarifaria(cidades["SP - São Paulo"])
    sem = next(d for d in cidades.values() if not d.get("fonte_registro") and not str(d.get("confianca_grau", "")).startswith("D"))
    assert procedencia_tarifaria(sem).startswith("catálogo sem documento")
    # Nenhum município está hoje como dado ruim; a tela continua dizendo quando estiver.
    ruim = dict(sem, confianca_grau="D — contradito por documento",
                motivo_dado_ruim="o documento desmente a base")
    assert procedencia_tarifaria(ruim).startswith("dado a revisar")


def test_montar_declara_o_regime_pela_forma_do_documento():
    sys.path.insert(0, os.path.join(RAIZ, "tarifas"))
    from aplicar_transcricoes import montar

    franquia = montar({"fixo": 40.42, "franquia": 10, "faixas": [[10, None, 5.69]], "esgoto_pct": 80})
    assert franquia["regime_tarifario"] == "franquia_no_minimo"
    assert franquia["faixas"][:2] == [[0.0, 0.0, 40.42, -1], [0.0, 10.0, 0.0, 1]]
    disp = montar({"fixo": 17.46, "faixas": [[0, None, 5.77]], "esgoto_pct": 100})
    assert disp["regime_tarifario"] == "disponibilidade"
    sem = montar({"faixas": [[0, None, 4.93]], "esgoto_pct": 80})
    assert sem["regime_tarifario"] == "sem_minimo" and sem["tarifa_fixa_mensal"] == 0.0
    por_m3 = montar({"faixas": [[0, None, 1.0]], "esgoto_r_m3": 7.1})
    assert por_m3["esgoto_modo"] == 2 and por_m3["esgoto_r_m3"] == 7.1


_TEXTOS = {}


def _texto_do_item(i: int) -> str:
    """Texto inteiro do documento guardado, sem acento (vazio para imagem ou digitalizado)."""
    if i not in _TEXTOS:
        import processar_entrada as E
        caminho = os.path.join(RAIZ, REGISTRO[i].get("guardado_em") or "")
        _TEXTOS[i] = E._sem_acento(E._texto(caminho)) if os.path.isfile(caminho) else ""
    return _TEXTOS[i]


@pytest.mark.parametrize("nome,t", TRANSCRICOES, ids=[n for n, _ in TRANSCRICOES])
def test_todo_municipio_e_nomeado_no_documento_ou_tem_a_regra_de_abrangencia(nome, t):
    """Município entra numa tabela porque o documento o nomeia, ou por uma regra escrita.

    Caso real (05/10/2026): a resolução da SABESP de Olímpia foi aplicada a Arujá, porque o
    script pegou o primeiro município da SABESP em vez de ler o documento.
    """
    import processar_entrada as E
    textos = [_texto_do_item(i) for i in t["registro"]]
    if not any(x.strip() for x in textos):
        pytest.skip("documento sem texto extraível (imagem): conferido visualmente")
    for tab in t["tabelas"]:
        if tab.get("abrangencia"):
            continue
        for m in tab["municipios"]:
            nome_m = E._sem_acento(m)
            assert any(E._citacoes(nome_m, x) or nome_m.lower() in x.lower() for x in textos), (
                f"{nome}, {tab['rotulo']}: «{m}» não aparece no documento e a tabela não tem «abrangencia»")


def _montar_e_cobrar(est, consumos):
    sys.path.insert(0, os.path.join(RAIZ, "tarifas"))
    from aplicar_transcricoes import montar
    from triton.core.economic import calculate_water_bill
    faixas = [tuple(f) for f in montar(est)["faixas"]]
    return [round(calculate_water_bill(c * 1000.0, faixas, 1, 0.0), 2) for c in consumos]


def test_cobranca_direta_reproduz_cada_m3_inteiro():
    """Valinhos (Res. ARES-PCJ 483/2023): 25 m³ × R$ 5,69 = R$ 142,25, todo o volume pela faixa."""
    est = {"direta": {"minimo": [10, 23.73], "precos": [[11, 17, 4.40], [18, 25, 5.69], [26, 35, 7.77],
                                                        [36, 50, 10.69]], "acima": 22.18}, "esgoto_pct": 100}
    assert _montar_e_cobrar(est, [5, 10, 11, 17, 18, 25, 60]) == [23.73, 23.73, 48.40, 74.80, 102.42, 142.25,
                                                                  1330.80]


def test_parcela_fixa_por_faixa_soma_a_variavel_em_cascata():
    """CESAN (Res. ARSP 107/2026): fixa da faixa do consumo total + variável por trecho."""
    est = {"fixo_por_faixa": [[10, 25.73], [15, 30.62], [None, 36.44]],
           "faixas": [[0, 10, 2.42], [10, 15, 4.84], [15, None, 8.71]], "esgoto_pct": 80}
    oficial = lambda c: ((25.73 if c <= 10 else 30.62 if c <= 15 else 36.44)
                         + 2.42 * min(c, 10) + 4.84 * max(0, min(c, 15) - 10) + 8.71 * max(0, c - 15))
    consumos = [0, 9, 10, 11, 15, 16, 30]
    assert _montar_e_cobrar(est, consumos) == [round(oficial(c), 2) for c in consumos]


def test_quadro_ruim_nao_derruba_a_transcricao_que_ja_o_reproduz():
    sys.path.insert(0, os.path.join(RAIZ, "tarifas"))
    from aplicar_transcricoes import _base_ja_confere
    dados = {"faixas": [[0.0, 0.0, 31.15, -1], [0.0, 10.0, 0.0, 1], [10.0, 999999.0, 4.0, 1]]}
    assert _base_ja_confere(dados, [{"consumo_m3": 10, "conta_agua": 31.15}])
    assert not _base_ja_confere(dados, [{"consumo_m3": 10, "conta_agua": 40.42}])
    assert not _base_ja_confere(dados, None)
