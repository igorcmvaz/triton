# -*- coding: utf-8 -*-
"""Português de Portugal para a Edição Portugal (PRT).

O catálogo da interface é escrito em português do Brasil. Na Edição Portugal, o mesmo
texto passa por este glossário, que troca o vocabulário — e não a gramática — pelo de
Portugal: VPL por VAL, arquivo por ficheiro, usuário por utilizador, esgoto por
saneamento. A troca respeita a fronteira de palavra e a caixa (minúscula, inicial
maiúscula, tudo maiúsculo), e os termos mais longos vêm primeiro, para que «valor
presente líquido» seja trocado inteiro antes de «presente».

Termos técnicos com sentido próprio no programa (TIR, payback, TOPSIS, ACV) não mudam.
"""

from __future__ import annotations

import re
from functools import lru_cache

#: Concordância: onde o termo de Portugal muda de gênero, o artigo e a preposição vêm junto.
_CONCORDANCIA = tuple(
    (f"{art_br} {br}", f"{art_pt} {pt}")
    for br, pt, pares in (
        ("prestador", "entidade gestora", (("o", "a"), ("do", "da"), ("no", "na"), ("ao", "à"), ("pelo", "pela"),
                                          ("um", "uma"), ("este", "esta"), ("esse", "essa"), ("seu", "sua"))),
        ("prestadores", "entidades gestoras", (("os", "as"), ("dos", "das"), ("aos", "às"), ("pelos", "pelas"))),
        ("tela", "ecrã", (("a", "o"), ("da", "do"), ("na", "no"), ("à", "ao"), ("pela", "pelo"), ("uma", "um"),
                         ("esta", "este"), ("nesta", "neste"), ("desta", "deste"), ("essa", "esse"))),
        ("telas", "ecrãs", (("as", "os"), ("das", "dos"), ("nas", "nos"), ("às", "aos"))),
        ("caixa superior", "reservatório superior", (("a", "o"), ("da", "do"), ("na", "no"), ("à", "ao"),
                                                    ("pela", "pelo"), ("uma", "um"))),
        ("bacias sanitárias", "autoclismos", (("as", "os"), ("das", "dos"), ("nas", "nos"))),
    )
    for art_br, art_pt in pares
)

#: (português do Brasil, português de Portugal), em minúsculas.
TERMOS = _CONCORDANCIA + (
    # economia e tarifa
    ("valor presente líquido", "valor atual líquido"),
    ("vpl", "VAL"),
    ("taxa mínima de atratividade", "taxa de atualização"),
    ("concessionárias", "entidades gestoras"),
    ("concessionária", "entidade gestora"),
    ("prestadores de saneamento", "entidades gestoras"),
    ("prestador de saneamento", "entidade gestora"),
    ("prestadores", "entidades gestoras"),
    ("prestador", "entidade gestora"),
    ("faixas tarifárias", "escalões tarifários"),
    ("faixa tarifária", "escalão tarifário"),
    ("faixas de consumo", "escalões de consumo"),
    ("faixa de consumo", "escalão de consumo"),
    ("conta de água", "fatura da água"),
    ("contas de água", "faturas da água"),
    ("tarifa de esgoto", "tarifa de saneamento"),
    ("esgotamento sanitário", "saneamento de águas residuais"),
    ("esgoto", "saneamento"),
    ("econômicos", "económicos"),
    ("econômicas", "económicas"),
    ("econômico", "económico"),
    ("econômica", "económica"),
    # informática e interface
    ("vazões", "caudais"),
    ("vazão", "caudal"),
    ("tubulações", "tubagens"),
    ("tubulação", "tubagem"),
    ("arquivos", "ficheiros"),
    ("arquivo", "ficheiro"),
    ("usuários", "utilizadores"),
    ("usuário", "utilizador"),
    ("planilhas", "folhas de cálculo"),
    ("planilha", "folha de cálculo"),
    ("salvar como", "guardar como"),
    ("salvar", "guardar"),
    ("salvo", "guardado"),
    ("salva", "guardada"),
    ("baixar", "transferir"),
    ("tela", "ecrã"),
    ("telas", "ecrãs"),
    ("registrar", "registar"),
    ("registro", "registo"),
    ("registros", "registos"),
    ("cadastrado", "registado"),
    ("cadastrada", "registada"),
    ("cadastro", "registo"),
    ("gerenciar", "gerir"),
    ("gerenciamento", "gestão"),
    ("contato", "contacto"),
    ("seção", "secção"),
    ("seções", "secções"),
    # instalação predial
    ("caixa d'água", "reservatório"),
    ("caixas d'água", "reservatórios"),
    ("caixa superior", "reservatório superior"),
    ("motobombas", "eletrobombas"),
    ("motobomba", "eletrobomba"),
    ("vaso sanitário", "autoclismo"),
    ("bacias sanitárias", "autoclismos"),
    # acentuação (ê/ô diante de m/n)
    ("acadêmico", "académico"),
    ("acadêmica", "académica"),
    ("fenômeno", "fenómeno"),
    ("fenômenos", "fenómenos"),
    ("quilômetros", "quilómetros"),
    ("quilômetro", "quilómetro"),
    ("anônimo", "anónimo"),
    ("gênero", "género"),
    ("polinômio", "polinómio"),
    ("milênio", "milénio"),
)


def _variantes(origem: str, destino: str):
    """Minúsculas, inicial maiúscula, cada palavra com maiúscula e tudo maiúsculo."""
    yield origem, destino
    yield origem[:1].upper() + origem[1:], destino[:1].upper() + destino[1:]
    def titulo(s):
        return " ".join(p[:1].upper() + p[1:] if len(p) > 2 else p for p in s.split(" "))
    yield titulo(origem), titulo(destino)
    yield origem.upper(), destino.upper()


_TABELA = {}
for _o, _d in TERMOS:
    for _a, _b in _variantes(_o, _d):
        _TABELA.setdefault(_a, _b)
# Siglas não variam com a caixa: «VPL» fica «VAL» (a variante maiúscula já cobre).
_PADRAO = re.compile(
    r"(?<![\w])(" + "|".join(re.escape(t) for t in sorted(_TABELA, key=len, reverse=True)) + r")(?![\w])")


@lru_cache(maxsize=20000)
def para_portugal(texto: str) -> str:
    """O texto em português do Brasil, com o vocabulário de Portugal."""
    if not texto or not isinstance(texto, str):
        return texto
    return _PADRAO.sub(lambda m: _TABELA[m.group(1)], texto)
