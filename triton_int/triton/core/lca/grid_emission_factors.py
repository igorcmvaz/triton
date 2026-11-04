"""Fatores de emissão da rede elétrica brasileira (MCTI/SIRENE).

O programa já usou um único número — 0,085 kg CO₂/kWh — anotado
no código como «hipótese editável; selecionar série MCTI/SIRENE do período». A
instrução nunca foi cumprida: o valor não correspondia a ano nenhum.

O fator do Sistema Interligado Nacional **varia por ano** com o despacho
termelétrico, e a variação é grande — de 0,0246 (2009) a 0,1355 (2014), um fator
de 5,5 entre extremos. Um estudo que não declare o ano do fator não é
reproduzível, e comparar dois estudos com anos diferentes sem dizer não é
comparar coisa alguma.

A série oficial completa está em ``triton/data/fatores_emissao_rede_mcti.json``,
gerada a partir da planilha do MCTI arquivada em ``data/fontes_externas/`` com o
respectivo SHA-256. Nenhum valor foi redigitado.

**Atenção à grandeza.** A série corporativa do MCTI é de **CO₂ apenas**, não de
CO₂-equivalente: metano e óxido nitroso da geração não entram. Quem precisar de
CO₂e deve dizê-lo explicitamente e usar outra fonte.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, Optional

NOME_DO_ARQUIVO = "fatores_emissao_rede_mcti.json"

#: Onde o arquivo do MCTI não vai (Internacional e Portugal): um arquivo sem série oficial e
#: com uma só base, de valor zero, que o usuário substitui pelo fator da rede do seu projeto.
NOME_DO_ARQUIVO_PADRAO = "fatores_emissao_rede_padrao.json"

# Ano adotado como padrão quando se pede um fator **de CO₂** por ano. É o último
# ano completo da série publicada — não o mais favorável, nem uma média de
# conveniência.
ANO_PADRAO = 2025

# Base adotada como padrão do módulo ambiental. Ver `bases_co2eq` no JSON.
BASE_PADRAO = "adotado_triton"

_CACHE: Optional[Dict[str, Any]] = None

#: Último recurso fora da Brasil, se nem o arquivo padrão estiver presente: nenhuma série e nenhuma
#: base com valor (fator zero).
_SERIE_NEUTRA: Dict[str, Any] = {
    "_fonte": {"orgao": "", "serie": "sem série oficial nesta edição", "unidade": "kgCO2e/kWh"},
    "fator_medio_anual_tco2_por_mwh": {},
    "fator_medio_mensal_tco2_por_mwh": {},
    "bases_co2eq": {
        "adotado_triton": {
            "valor": 0.0,
            "gas": "CO2e",
            "fronteira": "informada pelo usuário",
            "fonte": "Sem valor predefinido: informe o fator de emissão da rede elétrica do projeto.",
        }
    },
}


def _localizar_arquivo(nome: str = NOME_DO_ARQUIVO) -> str:
    """Localiza a série, em execução normal ou empacotada com PyInstaller.

    Segue o mesmo desenho de :func:`triton.core.tariffs_database._find_database_file`:
    cópia **única** dentro do pacote, em ``triton/data/``.
    """
    diretorio_do_pacote = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # triton/

    candidatos = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidatos.append(os.path.join(sys._MEIPASS, "triton", "data", nome))
    candidatos.append(os.path.join(diretorio_do_pacote, "data", nome))
    candidatos.append(os.path.join(os.path.dirname(diretorio_do_pacote), "data", nome))

    for caminho in candidatos:
        if os.path.isfile(caminho):
            return os.path.normpath(caminho)

    raise FileNotFoundError(
        f"Série de fatores de emissão '{nome}' não encontrada. "
        f"Caminhos consultados: {candidatos}"
    )


def carregar_serie() -> Dict[str, Any]:
    """Carrega e mantém em cache a série do MCTI, ou a série padrão onde ela não existe.

    Só a Edição Brasil traz o arquivo do MCTI. Nas outras, vale o arquivo padrão (sem anos
    publicados e com fator zero), ou, na falta dele, a mesma série neutra embutida.
    Na Brasil, faltar o arquivo continua sendo erro: um fator silencioso falsearia a ACV.
    """
    global _CACHE
    if _CACHE is None:
        try:
            caminho = _localizar_arquivo()
        except FileNotFoundError:
            from triton.core.edition import EDITION_BRL, get_current_edition
            if get_current_edition() == EDITION_BRL:
                raise
            try:
                caminho = _localizar_arquivo(NOME_DO_ARQUIVO_PADRAO)
            except FileNotFoundError:
                _CACHE = _SERIE_NEUTRA
                return _CACHE
        with open(caminho, "r", encoding="utf-8") as arquivo:
            _CACHE = json.load(arquivo)
    return _CACHE


def anos_disponiveis() -> list[int]:
    """Anos com fator médio anual publicado, em ordem crescente."""
    serie = carregar_serie()["fator_medio_anual_tco2_por_mwh"]
    return sorted(int(ano) for ano in serie)


def fator_anual(ano: int = ANO_PADRAO) -> float:
    """Fator médio anual do SIN, em **kg CO₂/kWh**.

    A planilha do MCTI publica em tCO₂/MWh, que é numericamente igual a
    kg CO₂/kWh — mil quilos por mil quilowatts-hora. Não há conversão a fazer, e
    é justamente por isso que o engano é fácil: registrar aqui evita que alguém
    “corrija” o número por mil em qualquer direção.
    """
    serie = carregar_serie()["fator_medio_anual_tco2_por_mwh"]
    chave = str(int(ano))
    if chave not in serie:
        disponiveis = anos_disponiveis()
        if not disponiveis:
            raise KeyError("Esta edição não traz série anual de fatores de emissão da rede.")
        raise KeyError(
            f"Não há fator publicado para {ano}. "
            f"A série cobre {disponiveis[0]}–{disponiveis[-1]}."
        )
    return float(serie[chave])


def fator_mensal(ano: int, mes: int) -> float:
    """Fator médio mensal do SIN, em kg CO₂/kWh. ``mes`` de 1 a 12."""
    if not 1 <= mes <= 12:
        raise ValueError(f"Mês deve estar entre 1 e 12; recebido {mes}.")
    serie = carregar_serie()["fator_medio_mensal_tco2_por_mwh"]
    chave = str(int(ano))
    if chave not in serie:
        raise KeyError(f"Não há série mensal publicada para {ano}.")
    meses = serie[chave]
    if mes > len(meses):
        raise KeyError(
            f"O ano {ano} está incompleto na fonte: há {len(meses)} meses publicados."
        )
    return float(meses[mes - 1])


def procedencia() -> Dict[str, Any]:
    """Metadados da fonte: órgão, arquivo arquivado, SHA-256, fronteira, gás.

    Exposto para que a interface e os relatórios possam declarar a origem do
    número em vez de exibi-lo solto.
    """
    return dict(carregar_serie()["_fonte"])


def bases_disponiveis() -> Dict[str, Dict[str, Any]]:
    """Fatores em kg CO₂e/kWh para uso em ACV, cada um com fonte e fronteira."""
    bases = dict(carregar_serie()["bases_co2eq"])
    bases.pop("_nota", None)
    return bases


def fator_co2eq(base: str = BASE_PADRAO) -> float:
    """Fator de emissão da rede **em CO₂-equivalente**, para uso em ACV.

    É esta a função que o módulo ambiental deve usar — não :func:`fator_anual`.

    A distinção não é preciosismo. A série do MCTI cobre **CO₂ apenas** e só a
    **geração**; uma ACV precisa de CO₂-equivalente e de fronteira mais ampla,
    que inclui a rede de transmissão e distribuição, a construção das usinas e
    as emissões biogênicas e de uso da terra. Vaz, Scolaro & Ghisi (2025,
    DOI 10.1016/j.scitotenv.2025.179774) mediram a diferença: a intensidade sobe
    de cerca de 0,07 kg CO₂/kWh pela série do SIRENE para até 0,20 kg CO₂e/kWh
    quando os demais processos e gases entram na conta.

    Tomar o número do MCTI por CO₂e, como esta implementação chegou a fazer,
    **subestima** o impacto do bombeamento e, por consequência, superestima o
    saldo ambiental do sistema.
    """
    bases = bases_disponiveis()
    if base not in bases:
        raise KeyError(
            f"Base desconhecida: {base!r}. Disponíveis: {sorted(bases)}."
        )
    return float(bases[base]["valor"])


def procedencia_da_base(base: str = BASE_PADRAO) -> Dict[str, Any]:
    """Fonte, gás e fronteira de uma das bases de CO₂e."""
    bases = bases_disponiveis()
    if base not in bases:
        raise KeyError(f"Base desconhecida: {base!r}. Disponíveis: {sorted(bases)}.")
    return dict(bases[base])
