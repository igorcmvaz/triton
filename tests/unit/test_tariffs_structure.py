"""
Integridade estrutural do catálogo tarifário das 652 cidades.

O catálogo representa cada tarifa como quádruplas ``(mínimo, máximo, valor, código)``.
`netuno/core/tariffs_structure.py` define os códigos e valida a estrutura; este módulo
verifica o catálogo inteiro contra essa definição.

Duas verificações têm consequência científica direta:

1. **Todo código presente é conhecido.** Um código não previsto seria interpretado de
   forma silenciosamente errada pelo motor econômico. Foi por não conhecer o código
   ``-2`` que um teste anterior rejeitava a tarifa legítima da DAE Americana.

2. **A conta responde ao consumo.** Se a parcela volumétrica não cresce com o volume,
   economizar água não reduz a fatura, e o Netuno calcula retorno econômico nulo para
   qualquer sistema naquele município — independentemente do seu desempenho hídrico.
   Não é falha de cálculo: é lacuna no dado tarifário registrado.

Registro de municípios afetados
-------------------------------
43 dos 652 municípios (6.6%) têm tarifa que não responde ao
consumo, quase todos por terem a tarifa volumétrica registrada como ``0,0`` ao lado de
uma taxa fixa de disponibilidade. A concentração no Rio Grande do Sul sugere que a
estrutura da CORSAN foi transcrita apenas na parcela fixa.

Estas cidades **não foram corrigidas**: obter a tarifa correta exige consultar as
resoluções vigentes de cada prestador, o que é trabalho de fonte primária e não de
verificação. O registro abaixo existe para que a lista não cresça sem ser notada e para
que os estudos que incluam esses municípios saibam o que esperar.
"""

import pytest

from netuno.core.tariffs_database import (
    get_available_ufs,
    get_cities_by_uf,
    get_city_data,
)
from netuno.core.tariffs_structure import (
    CODIGOS_VALIDOS,
    DESCRICAO_DO_CODIGO,
    diagnosticar,
)

# Municípios com tarifa que não responde ao consumo, apurados em 2026-09-08.
# Corrigir um deles significa removê-lo desta lista.
SEM_RESPOSTA_AO_CONSUMO = {
    ("MG", "Mariana"),  # SAAE Mariana
    ("MG", "Sete Lagoas"),  # SAAE Sete Lagoas
    ("MG", "Viçosa"),  # SAAE Viçosa
    ("RS", "Alegrete"),  # CORSAN
    ("RS", "Alvorada"),  # CORSAN
    ("RS", "Bento Gonçalves"),  # CORSAN
    ("RS", "Cachoeira do Sul"),  # CORSAN
    ("RS", "Cachoeirinha"),  # CORSAN
    ("RS", "Camaquã"),  # CORSAN
    ("RS", "Campo Bom"),  # CORSAN
    ("RS", "Canoas"),  # CORSAN
    ("RS", "Capão da Canoa"),  # CORSAN
    ("RS", "Carazinho"),  # CORSAN
    ("RS", "Cruz Alta"),  # CORSAN
    ("RS", "Erechim"),  # CORSAN
    ("RS", "Esteio"),  # CORSAN
    ("RS", "Farroupilha"),  # CORSAN
    ("RS", "Gravataí"),  # CORSAN
    ("RS", "Guaíba"),  # CORSAN
    ("RS", "Ijuí"),  # CORSAN
    ("RS", "Lajeado"),  # CORSAN
    ("RS", "Montenegro"),  # CORSAN
    ("RS", "Novo Hamburgo"),  # COMUSA Novo Hamburgo
    ("RS", "Parobé"),  # CORSAN
    ("RS", "Passo Fundo"),  # CORSAN
    ("RS", "Rio Grande"),  # CORSAN
    ("RS", "Santa Cruz do Sul"),  # CORSAN
    ("RS", "Santa Maria"),  # CORSAN
    ("RS", "Santa Rosa"),  # CORSAN
    ("RS", "Santo Ângelo"),  # CORSAN
    ("RS", "Sapiranga"),  # CORSAN
    ("RS", "Sapucaia do Sul"),  # CORSAN
    ("RS", "São Borja"),  # CORSAN
    ("RS", "São Gabriel"),  # São Gabriel Saneamento S.A.
    ("RS", "Taquara"),  # CORSAN
    ("RS", "Tramandaí"),  # CORSAN
    ("RS", "Vacaria"),  # CORSAN
    ("RS", "Venâncio Aires"),  # CORSAN
    ("RS", "Viamão"),  # CORSAN
    ("SP", "Bauru"),  # DAE Bauru
    ("SP", "Bebedouro"),  # SAAEB Ambiental
    ("SP", "Pirassununga"),  # SAEP Pirassununga
    ("SP", "São José do Rio Pardo"),  # SAERP São José do Rio Pardo
}


def _todas_as_cidades():
    for uf, _ in get_available_ufs():
        for cidade in get_cities_by_uf(uf):
            dados = get_city_data(uf, cidade)
            if dados:
                yield uf, cidade, dados


def test_todos_os_codigos_do_catalogo_sao_conhecidos():
    """Nenhum município usa código de faixa fora da definição."""
    desconhecidos = {}
    for uf, cidade, dados in _todas_as_cidades():
        for faixa in dados["faixas"]:
            codigo = int(faixa[3])
            if codigo not in CODIGOS_VALIDOS:
                desconhecidos.setdefault(codigo, []).append(f"{uf}/{cidade}")

    assert not desconhecidos, (
        "códigos de faixa não previstos em tariffs_structure.py: "
        + "; ".join(f"{cod} em {locais[:3]}" for cod, locais in desconhecidos.items())
        + f". Códigos conhecidos: { {c: DESCRICAO_DO_CODIGO[c] for c in sorted(CODIGOS_VALIDOS)} }"
    )


def test_catalogo_cobre_as_652_cidades():
    """A contagem do catálogo não pode encolher sem que se perceba."""
    assert sum(1 for _ in _todas_as_cidades()) == 652


def test_lista_de_municipios_sem_resposta_ao_consumo_nao_cresceu():
    """Trava o defeito conhecido de dado tarifário.

    Falha em dois sentidos: se um município novo passar a não responder ao consumo
    (regressão), e se um da lista for corrigido sem que a lista seja atualizada
    (registro obsoleto).
    """
    encontrados = {
        (uf, cidade)
        for uf, cidade, dados in _todas_as_cidades()
        if not diagnosticar(dados["faixas"]).utilizavel_para_analise_economica
    }

    novos = encontrados - SEM_RESPOSTA_AO_CONSUMO
    corrigidos = SEM_RESPOSTA_AO_CONSUMO - encontrados

    assert not novos, (
        f"{len(novos)} município(s) passaram a ter tarifa insensível ao consumo: "
        f"{sorted(novos)}"
    )
    assert not corrigidos, (
        f"{len(corrigidos)} município(s) foram corrigidos mas continuam no registro; "
        f"remova-os de SEM_RESPOSTA_AO_CONSUMO: {sorted(corrigidos)}"
    )


def test_a_grande_maioria_do_catalogo_e_utilizavel():
    """Ao menos 90% dos municípios permitem análise econômica significativa."""
    total = utilizaveis = 0
    for _uf, _cidade, dados in _todas_as_cidades():
        total += 1
        if diagnosticar(dados["faixas"]).utilizavel_para_analise_economica:
            utilizaveis += 1

    fracao = utilizaveis / total
    assert fracao >= 0.90, (
        f"apenas {fracao:.1%} dos municípios têm tarifa utilizável para análise "
        f"econômica ({utilizaveis} de {total})"
    )


@pytest.mark.parametrize("uf,cidade", [
    ("SC", "Florianópolis"), ("SP", "São Paulo"), ("AM", "Manaus"), ("DF", "Brasília"),
])
def test_capitais_de_referencia_tem_tarifa_integra(uf, cidade):
    """As cidades usadas nos estudos de referência não podem ter lacuna tarifária."""
    dados = get_city_data(uf, cidade)
    if not dados:
        pytest.skip(f"{uf}/{cidade} ausente do catálogo")

    diagnostico = diagnosticar(dados["faixas"])
    assert not diagnostico.problemas, (
        f"{uf}/{cidade} apresenta problemas estruturais: {diagnostico.problemas}"
    )


def test_franquia_de_consumo_minimo_e_reconhecida():
    """A tarifa da DAE Americana (código -2) é estruturalmente válida.

    Foi esta tarifa que um teste desatualizado rejeitava, por desconhecer o código.
    """
    dados = get_city_data("SP", "Americana")
    if not dados:
        pytest.skip("SP/Americana ausente do catálogo")

    codigos = {int(f[3]) for f in dados["faixas"]}
    assert -2 in codigos, "a franquia de consumo mínimo desapareceu do catálogo"
    assert codigos <= CODIGOS_VALIDOS
    assert diagnosticar(dados["faixas"]).utilizavel_para_analise_economica
