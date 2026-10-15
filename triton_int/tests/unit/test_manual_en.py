"""O manual em inglês acompanha o português, e a edição Internacional abre o inglês.

O português é a referência: cada seção de `gerar.ESTRUTURA` tem um arquivo em
`manual/en`, com o mesmo esqueleto (títulos, figuras, equações, inclusões, número de
tabelas) e sem português esquecido no texto. `manual/en/conferir.py` faz a conferência;
aqui ela vira teste, para que uma seção nova ou mudada em português não chegue ao
lançamento sem a inglesa.

As partes geradas — as tabelas de `_tabelas` e os apêndices A, B e D — são conferidas
contra o que os geradores produziriam agora: uma tabela regerada em português e
esquecida em inglês aparece aqui.
"""
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MANUAL = os.path.join(RAIZ, "manual")
EN = os.path.join(MANUAL, "en")
for _p in (MANUAL, EN):
    if _p not in sys.path:
        sys.path.insert(0, _p)

try:
    import conferir
    import gerar
except ModuleNotFoundError:
    pytest.skip("geradores do manual nao versionados (ficam no disco do mantenedor)", allow_module_level=True)


def _ler(caminho):
    with open(caminho, encoding="utf-8") as f:
        return f.read()


@pytest.mark.parametrize("pasta,chave", list(conferir.secoes()))
def test_a_secao_inglesa_segue_a_portuguesa(pasta, chave):
    """Se falhar: rode `python manual/en/conferir.py` e traga a seção inglesa ao português."""
    achados = conferir.problemas_da_secao(pasta, chave)
    assert not achados, "\n".join(achados)


def test_toda_secao_tem_titulo_e_toda_equacao_tem_nome_em_ingles():
    import textos_en as T
    chaves = [c for _, _, cs in gerar.ESTRUTURA for c in cs]
    assert [c for c in chaves if c not in T.TITULOS] == []
    assert len(T.CAPITULOS) == len(gerar.ESTRUTURA)
    equacoes = set()
    for pasta, chave in conferir.secoes():
        caminho = os.path.join(EN, pasta, chave + ".md")
        equacoes |= set(re.findall(r"^```equacao:([^\s:]+)", _ler(caminho), flags=re.M))
    assert sorted(equacoes - set(T.EQUACOES)) == []


def test_as_tabelas_traduzidas_estao_em_dia():
    """Se falhar: rode `python manual/en/traduzir_tabelas.py`."""
    import traduzir_tabelas as TT
    origem = sorted(n for n in os.listdir(TT.ORIGEM) if n.endswith(".md"))
    destino = sorted(n for n in os.listdir(TT.DESTINO) if n.endswith(".md"))
    assert origem == destino
    faltam = []
    desatualizadas = []
    for nome in origem:
        esperado = TT.traduzir(_ler(os.path.join(TT.ORIGEM, nome)), faltam)
        if _ler(os.path.join(TT.DESTINO, nome)) != esperado:
            desatualizadas.append(nome)
    assert not faltam, "células sem tradução: " + "; ".join(dict.fromkeys(faltam))
    assert not desatualizadas, "tabelas inglesas desatualizadas: " + ", ".join(desatualizadas)


@pytest.mark.parametrize("nome,funcao", [("A_parametros.md", "apendice_a"),
                                         ("B_processos.md", "apendice_b"),
                                         ("D_regimes_tarifarios.md", "apendice_d")])
def test_os_apendices_gerados_estao_em_dia(nome, funcao):
    """Se falhar: rode `python manual/en/apendices_en.py`."""
    import apendices_en
    texto, _ = getattr(apendices_en, funcao)()
    if texto is None:
        pytest.skip("a fonte do apêndice não está nesta árvore")
    gravado = _ler(os.path.join(EN, "apendices", nome))
    assert gravado == texto + "\n", f"{nome} em inglês não corresponde ao gerador"


def test_o_manual_montado_tem_todas_as_secoes():
    """O .md montado é o que vira PDF; uma seção que falte nele falta no PDF."""
    import textos_en as T
    caminho = os.path.join(EN, T.ARQUIVO_MONTADO)
    if not os.path.isfile(caminho):
        pytest.skip("o manual inglês não foi montado nesta árvore")
    montado = _ler(caminho)
    assert "Section not yet written" not in montado
    assert "{{" not in montado, "marca de remissão sem resolver no manual inglês"
    faltam = [t for t in T.TITULOS.values() if t not in montado]
    assert not faltam, "seções ausentes do manual inglês montado: " + ", ".join(faltam)


# ── Qual manual o programa abre ──────────────────────────────────────────────

@pytest.fixture
def edicao(monkeypatch):
    import triton.core.edition as ed

    def _usar(valor):
        monkeypatch.setattr(ed, "get_current_edition", lambda: valor)
        return ed
    return _usar


def test_a_internacional_abre_o_manual_ingles_em_qualquer_lingua(edicao):
    ed = edicao("INT")
    assert ed.manual_do_usuario("en") == ed.MANUAL_EN
    assert ed.manual_do_usuario("pt") == ed.MANUAL_EN


def test_a_brasil_segue_a_lingua_da_interface(edicao):
    ed = edicao("BRL")
    assert ed.manual_do_usuario("pt") == ed.MANUAL_PT
    for lingua in ("en", "es", "zh"):
        assert ed.manual_do_usuario(lingua) == ed.MANUAL_EN


def test_o_manual_ingles_existe_e_e_o_que_o_textos_en_declara():
    import triton.core.edition as ed
    import textos_en as T
    assert ed.MANUAL_EN == "manual/en/" + T.ARQUIVO_PDF
    if not os.path.isfile(os.path.join(RAIZ, ed.MANUAL_EN)):
        pytest.skip("o PDF inglês não foi gerado nesta árvore")


def test_o_executavel_e_o_instalador_levam_o_manual_ingles():
    import triton.core.edition as ed
    assert ed.MANUAL_EN in _ler(os.path.join(RAIZ, "build_exe.py"))
    assert ed.MANUAL_EN in _ler(os.path.join(RAIZ, "Triton.spec"))
    iss = _ler(os.path.join(RAIZ, "setup_script.iss"))
    bloco_int = iss[iss.index('#if Edition == "INT"'):iss.index("#else")]
    assert ed.MANUAL_EN.replace("/", "\\") in bloco_int.replace("_internal\\", "")
