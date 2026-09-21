"""Rotas de produção da água que o sistema pluvial substitui.

A emissão evitada por metro cúbico já foi um número só, 0,35 kg
CO₂e/m³, tratado como se fosse propriedade do sistema pluvial. Não é: **é
propriedade da água que se deixa de consumir**. Substituir água dessalinizada e
substituir água de manancial tratada por gravidade são coisas diferentes por uma
ordem de grandeza, e o mesmo reservatório muda de mérito conforme o caso.

O módulo permite declarar a rota e recalcular a emissão evitada a partir dela.

Duas famílias de rota, porque as fontes disponíveis não são homogêneas:

``energia_mais_outros``
    A rota declara intensidade energética (kWh/m³) e uma parcela não energética.
    O CO₂ é recomposto com o **fator de rede escolhido pelo usuário**. É o
    tratamento correto para rotas dominadas por eletricidade — a dessalinização
    à frente —, cujo impacto muda com a matriz local. Uma planta de osmose
    reversa no Brasil e outra na Alemanha consomem a mesma energia e emitem
    coisas muito diferentes.

``total_publicado``
    Só se conhece o total publicado. Usa-se como está, e declara-se a matriz
    elétrica que a fonte assumiu, para que fique visível o limite da
    transposição. Não se rescala o que não se sabe decompor.
"""

from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict, List, Optional

NOME_DO_ARQUIVO = "rotas_producao_agua.json"

_CACHE: Optional[Dict[str, Any]] = None


def _localizar_arquivo() -> str:
    """Mesma estratégia de :mod:`netuno.core.tariffs_database`: cópia única no pacote."""
    diretorio_do_pacote = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    candidatos = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidatos.append(os.path.join(sys._MEIPASS, "netuno", "data", NOME_DO_ARQUIVO))
    candidatos.append(os.path.join(diretorio_do_pacote, "data", NOME_DO_ARQUIVO))

    for caminho in candidatos:
        if os.path.isfile(caminho):
            return os.path.normpath(caminho)

    raise FileNotFoundError(
        f"Catálogo de rotas '{NOME_DO_ARQUIVO}' não encontrado. Caminhos: {candidatos}"
    )


def _carregar() -> Dict[str, Any]:
    global _CACHE
    if _CACHE is None:
        with open(_localizar_arquivo(), "r", encoding="utf-8") as arquivo:
            _CACHE = json.load(arquivo)
    return _CACHE


ROTA_PADRAO = "convencional_br"


def rotas_disponiveis() -> Dict[str, Dict[str, Any]]:
    """Todas as rotas, com fonte e tipo declarados."""
    return dict(_carregar()["rotas"])


def chaves_das_rotas() -> List[str]:
    return list(_carregar()["rotas"].keys())


def rota(chave: str) -> Dict[str, Any]:
    rotas = _carregar()["rotas"]
    if chave not in rotas:
        raise KeyError(f"Rota desconhecida: {chave!r}. Disponíveis: {sorted(rotas)}.")
    return dict(rotas[chave])


def nome_da_rota(chave: str, lang: str = "pt") -> str:
    registro = rota(chave)
    return registro["nome_pt"] if lang == "pt" else registro.get("nome_en", registro["nome_pt"])


def co2_evitado_por_m3(chave: str = ROTA_PADRAO, fator_da_rede_kg_kwh: Optional[float] = None) -> float:
    """Emissão evitada por m³ de água pluvial aproveitada, em kg CO₂e/m³.

    ``fator_da_rede_kg_kwh`` só é usado pelas rotas do tipo
    ``energia_mais_outros``. Quando omitido, adota-se o padrão do módulo de
    fatores de rede — que é CO₂-equivalente, não a série de CO₂ do MCTI.
    """
    registro = rota(chave)
    tipo = registro.get("tipo")

    if tipo == "total_publicado":
        return float(registro["co2_total_kg_m3"])

    if tipo == "energia_mais_outros":
        if fator_da_rede_kg_kwh is None:
            # Importação tardia: evita ciclo com environmental.py.
            from netuno.core.grid_emission_factors import BASE_PADRAO, fator_co2eq

            fator_da_rede_kg_kwh = fator_co2eq(BASE_PADRAO)
        energia = float(registro["kwh_por_m3"]) * float(fator_da_rede_kg_kwh)
        return energia + float(registro.get("co2_nao_energetico_kg_m3", 0.0))

    raise ValueError(f"Tipo de rota não reconhecido em {chave!r}: {tipo!r}")


#: Valor de base do programa, em kg CO2e/m3. É o da rota padrão, e existe como
#: constante para que a interface e os relatórios possam dizê-lo sem repetir o
#: número. Escolhido por ficar logo abaixo das faixas publicadas para tratamento
#: convencional, tanto com matriz europeia quanto com brasileira: subestimar o
#: benefício do sistema pluvial é o erro conservador.
BASE_DO_PROGRAMA_KG_M3 = 0.35

_CAMPOS_DE_PROCEDENCIA = (
    "fonte",
    "doi_da_fonte",
    "matriz_da_fonte",
    "fronteira",
    "tecnologia",
    "fronteira_incompleta",
    "observacao",
    "faixa",
    "aproximado",
    "conservador",
)


def procedencia_da_rota(chave: str) -> Dict[str, Any]:
    """Fonte, DOI, matriz, tecnologia, fronteira e ressalvas de uma rota.

    A **tecnologia** e a **fronteira** são o que torna a escolha informada. Sem
    elas, dois valores muito diferentes parecem discordar quando na verdade
    descrevem a mesma coisa medida de dois jeitos: 0,236 e 0,394 kg CO2e/m3 são
    o mesmo tratamento convencional brasileiro, um por m3 produzido na estação e
    outro por m3 entregue na edificação, e o que os separa são as perdas de
    distribuição.
    """
    registro = rota(chave)
    return {campo: registro[campo] for campo in _CAMPOS_DE_PROCEDENCIA if campo in registro}


def fronteira_e_incompleta(chave: str) -> bool:
    """Diz se a rota declara fronteira parcial.

    Uma rota assim subestima por construção, e não serve como estimativa central
    da emissão evitada: ou foi publicada na porta da estação, sem as perdas de
    distribuição, ou cobre apenas a energia, sem produtos químicos nem
    infraestrutura. Continua no catálogo como limite inferior declarado.
    """
    return bool(rota(chave).get("fronteira_incompleta", False))


def chaves_com_fronteira_completa() -> List[str]:
    """As rotas que servem como estimativa central da emissão evitada."""
    return [c for c in chaves_das_rotas() if not fronteira_e_incompleta(c)]


def comparar_rotas(fator_da_rede_kg_kwh: Optional[float] = None) -> List[Dict[str, Any]]:
    """Todas as rotas, ordenadas da menor emissão evitada para a maior.

    É a tabela que responde à pergunta que motivou o módulo: *quanto muda o
    mérito ambiental do sistema conforme o que ele substitui?*
    """
    linhas = []
    for chave in chaves_das_rotas():
        linhas.append(
            {
                "chave": chave,
                "nome_pt": nome_da_rota(chave, "pt"),
                "nome_en": nome_da_rota(chave, "en"),
                "co2_evitado_kg_m3": co2_evitado_por_m3(chave, fator_da_rede_kg_kwh),
                "tipo": rota(chave).get("tipo"),
                **procedencia_da_rota(chave),
            }
        )
    return sorted(linhas, key=lambda linha: linha["co2_evitado_kg_m3"])
