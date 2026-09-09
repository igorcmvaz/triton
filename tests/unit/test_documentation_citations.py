"""Verificação da bibliografia da Documentação.

A promessa é «pelo menos três citações por aba, mostrando o estado da arte».
Uma promessa dessas se cumpre uma vez e se perde na primeira edição seguinte, a
menos que alguma coisa a cobre. É o que estes testes fazem.

O teste mais importante não é o da contagem: é o
`test_nenhuma_referencia_veio_de_memoria`. Ao montar a bibliografia, três DOIs
escritos de memória foram conferidos no Crossref e apontavam para artigos sem
relação nenhuma com o assunto, e uma referência que já estava no programa trazia
periódico e páginas errados. Citação não conferida é citação errada com
aparência de rigor — e nenhum leitor tem como distinguir as duas.
"""

from __future__ import annotations

import datetime
import re

import pytest

from netuno.core import bibliography as bib


def test_toda_secao_tecnica_tem_o_minimo_de_citacoes():
    faltantes = {
        secao: len(chaves)
        for secao, chaves in bib.REFERENCIAS_POR_SECAO.items()
        if secao not in bib.SECOES_ISENTAS and len(chaves) < bib.MINIMO_DE_CITACOES
    }
    assert not faltantes, (
        f"Seções abaixo de {bib.MINIMO_DE_CITACOES} citações: {faltantes}"
    )


def test_isencoes_sao_poucas_e_declaradas():
    """A isenção existe para documentação de operação, não para escapar do trabalho."""
    assert bib.SECOES_ISENTAS == ("cli",)
    for secao in bib.SECOES_ISENTAS:
        assert secao in bib.REFERENCIAS_POR_SECAO


def test_toda_chave_citada_existe():
    desconhecidas = {
        (secao, chave)
        for secao, chaves in bib.REFERENCIAS_POR_SECAO.items()
        for chave in chaves
        if chave not in bib.REFERENCIAS
    }
    assert not desconhecidas, f"Chaves sem registro: {sorted(desconhecidas)}"


def test_nenhuma_referencia_fica_orfa():
    """Referência que não é citada por seção nenhuma não deveria estar no módulo."""
    citadas = {chave for chaves in bib.REFERENCIAS_POR_SECAO.values() for chave in chaves}
    orfas = sorted(set(bib.REFERENCIAS) - citadas)
    assert not orfas, f"Referências registradas e nunca citadas: {orfas}"


def test_chave_do_registro_bate_com_a_do_dicionario():
    divergentes = [
        (chave, ref.chave) for chave, ref in bib.REFERENCIAS.items() if chave != ref.chave
    ]
    assert not divergentes, f"Chave do dicionário diferente da do registro: {divergentes}"


def test_nenhuma_referencia_veio_de_memoria():
    """Toda referência tem de ter sido recuperada de uma base, nunca lembrada."""
    origens_validas = {"crossref", "openalex", "scite", "editor", "usuario"}
    invalidas = {
        chave: ref.recuperado_por
        for chave, ref in bib.REFERENCIAS.items()
        if ref.recuperado_por not in origens_validas
    }
    assert not invalidas, f"Origem de recuperação inválida: {invalidas}"


def test_doi_tem_forma_valida():
    padrao = re.compile(r"^10\.\d{4,9}/\S+$")
    quebradas = {
        chave: ref.doi
        for chave, ref in bib.REFERENCIAS.items()
        if ref.doi and not padrao.match(ref.doi)
    }
    assert not quebradas, f"DOI malformado: {quebradas}"


def test_todo_registro_tem_doi_ou_url():
    sem_localizador = [
        chave for chave, ref in bib.REFERENCIAS.items() if not ref.doi and not ref.url
    ]
    assert not sem_localizador, (
        f"Referências sem DOI nem URL — irrecuperáveis pelo leitor: {sem_localizador}"
    )


def test_fontes_nao_bibliograficas_declaram_data_de_acesso():
    """Norma, base de dados e software mudam sem aviso; sem data não são citáveis."""
    faltando = [
        chave
        for chave, ref in bib.REFERENCIAS.items()
        if ref.tipo in {"norma", "base_de_dados", "software", "relatorio"}
        and ref.acessado_em is None
    ]
    assert not faltando, f"Sem data de acesso: {faltando}"


def test_nenhuma_data_de_acesso_no_futuro():
    """A lista antiga trazia acessos datados de 2026 em conteúdo anterior a isso."""
    hoje = datetime.date.today()
    futuras = {
        chave: ref.acessado_em
        for chave, ref in bib.REFERENCIAS.items()
        if ref.acessado_em and ref.acessado_em > hoje
    }
    assert not futuras, f"Data de acesso no futuro: {futuras}"


def test_anos_sao_plausiveis():
    hoje = datetime.date.today().year
    estranhos = {
        chave: ref.ano
        for chave, ref in bib.REFERENCIAS.items()
        if not (1900 <= ref.ano <= hoje + 1)
    }
    assert not estranhos, f"Ano implausível: {estranhos}"


def test_toda_referencia_diz_o_que_sustenta():
    """Lista de referências sem nota é ornamento: não se sabe qual afirmação depende de qual fonte."""
    mudas = [chave for chave, ref in bib.REFERENCIAS.items() if not ref.nota_pt.strip()]
    assert not mudas, f"Referências sem nota explicando o que sustentam: {mudas}"


@pytest.mark.parametrize("lang", ["pt", "en"])
def test_bloco_renderiza_nos_dois_idiomas(lang):
    for secao in bib.REFERENCIAS_POR_SECAO:
        bloco = bib.render_bloco_da_secao(secao, lang)
        if secao in bib.SECOES_ISENTAS:
            assert bloco == ""
            continue
        assert "<ol" in bloco and "</ol>" in bloco
        # Uma entrada <li> por referência declarada.
        assert bloco.count("<li") == len(bib.REFERENCIAS_POR_SECAO[secao])


def test_os_dois_idiomas_listam_a_mesma_quantidade():
    for secao in bib.REFERENCIAS_POR_SECAO:
        pt = bib.render_bloco_da_secao(secao, "pt").count("<li")
        en = bib.render_bloco_da_secao(secao, "en").count("<li")
        assert pt == en, f"{secao}: {pt} referências em PT contra {en} em EN"


def test_secao_desconhecida_falha_alto():
    with pytest.raises(KeyError):
        bib.render_bloco_da_secao("secao_que_nao_existe")


def test_html_gerado_e_compativel_com_qtextbrowser():
    """O QTextBrowser aceita HTML 4 / CSS 2.1 — não flex, grid nem pseudo-classes."""
    proibidos = ("display: flex", "display:flex", "display: grid", "display:grid", ":hover", "var(--")
    for secao in bib.REFERENCIAS_POR_SECAO:
        for lang in ("pt", "en"):
            bloco = bib.render_bloco_da_secao(secao, lang)
            for termo in proibidos:
                assert termo not in bloco, f"{secao}/{lang}: CSS não suportado ({termo})"


def test_bibliografia_completa_cobre_todos_os_registros():
    completa = bib.render_bibliografia_completa("pt")
    assert completa.count("<li") == len(bib.REFERENCIAS)


def test_atribuicao_do_hammond_jones_registra_o_limite():
    """A ICE não publica plásticos no artigo — citá-la para PEAD seria falso.

    Esta é a armadilha mais provável de quem for estender a ACV: o nome «ICE»
    parece cobrir tudo. A nota da referência precisa dizer que não cobre.
    """
    ref = bib.REFERENCIAS["hammond_jones_2008"]
    assert "plástico" in ref.nota_pt.lower() or "plastic" in ref.nota_en.lower()


def test_walsh_lawler_com_o_veiculo_correto():
    """A referência anterior do programa trazia periódico e páginas errados."""
    ref = bib.REFERENCIAS["walsh_lawler_1981"]
    assert ref.veiculo == "Weather"
    assert "36" in ref.detalhe and "201" in ref.detalhe
