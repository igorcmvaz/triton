"""
Módulo de Banco de Dados de Tarifas Municipais de Saneamento e Energia (Netuno 5).
Contém a base auditada de 652 municípios brasileiros em todas as 27 Unidades Federativas,
suportando todas as categorias tarifárias: Residencial, Comercial, Industrial, Pública e Social.
"""

from __future__ import annotations

import os
import sys
import json
from typing import List, Tuple, Dict, Any, Optional

from netuno.core.tariffs_structure import ESGOTO_PERCENTUAL, ESGOTO_POR_M3, EXPOENTE_DE_CONSUMO

_DB_CACHE: Optional[Dict[str, Any]] = None

# =====================================================================================================================
# CATEGORIAS TARIFÁRIAS NACIONAIS (ÁGUA, ESGOTO E ENERGIA ELÉTRICA)
# =====================================================================================================================

CATEGORIAS_TARIFARIAS: Dict[str, Dict[str, Any]] = {
    "residencial": {
        "id": "residencial",
        "nome": "Residencial Normal",
        "icone": "🏠",
        "mult_agua": 1.0,
        "mult_fixo": 1.0,
        "mult_energia": 1.0,
        "desc": "Tarifa padrão para domicílios e habitações unifamiliares e multifamiliares (ANEEL B1)."
    },
    "comercial": {
        "id": "comercial",
        "nome": "Comercial / Serviços",
        "icone": "💼",
        "mult_agua": 1.85,
        "mult_fixo": 1.75,
        "mult_energia": 1.10,
        "desc": "Comércio, escritórios, consultórios e prestadores de serviços (ANEEL B3 / Água Comercial)."
    },
    "industrial": {
        "id": "industrial",
        "nome": "Industrial",
        "icone": "🏭",
        "mult_agua": 2.30,
        "mult_fixo": 2.20,
        "mult_energia": 1.15,
        "desc": "Indústrias de transformação, manufatura e plantas fabris."
    },
    "publica": {
        "id": "publica",
        "nome": "Pública / Institucional",
        "icone": "🏛️",
        "mult_agua": 1.65,
        "mult_fixo": 1.50,
        "mult_energia": 0.95,
        "desc": "Órgãos governamentais, escolas públicas, universidades e hospitais."
    },
    "social": {
        "id": "social",
        "nome": "Social / Baixa Renda",
        "icone": "🤝",
        "mult_agua": 0.50,
        "mult_fixo": 0.50,
        "mult_energia": 0.60,
        "desc": "Tarifa Social de Água e Esgoto (Lei Federal nº 14.898/2024) e TSEE (ANEEL)."
    },
}


#: Nome do arquivo do banco tarifário, único em toda a distribuição.
NOME_DO_BANCO = "brazil_cities_tariffs.json"


def _find_database_file() -> str:
    """Localiza o banco tarifário, em execução normal ou empacotado com PyInstaller.

    O banco é **único** e vive dentro do pacote, em ``netuno/data/``. Assim ele
    acompanha tanto a instalação por ``pip`` (via ``package-data``) quanto o executável
    congelado, e o atualizador tarifário escreve exatamente no arquivo que o programa lê.

    Já houve duas cópias — ``data/tarifas/`` e ``netuno/data/`` — ambas
    empacotadas, com esta busca preferindo a primeira. Elas divergiram em 465 das 652
    cidades sem que nada acusasse, e a cópia lida tinha a primeira faixa tarifária
    zerada em 464 delas. Manter uma única cópia elimina a classe do problema; o teste
    `tests/unit/test_tariffs_structure.py` impede o reaparecimento de uma segunda.
    """
    diretorio_do_pacote = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    candidatos = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidatos.append(os.path.join(sys._MEIPASS, "netuno", "data", NOME_DO_BANCO))
    candidatos.append(os.path.join(diretorio_do_pacote, "data", NOME_DO_BANCO))

    for caminho in candidatos:
        if os.path.isfile(caminho):
            return os.path.normpath(caminho)

    raise FileNotFoundError(
        f"Banco tarifário '{NOME_DO_BANCO}' não encontrado. Caminhos consultados: {candidatos}"
    )


def load_tariffs_db() -> Dict[str, Any]:
    """Carrega e armazena em cache o banco de dados oficial de tarifas."""
    global _DB_CACHE
    if _DB_CACHE is not None:
        return _DB_CACHE
        
    db_path = _find_database_file()
    with open(db_path, 'r', encoding='utf-8') as f:
        _DB_CACHE = json.load(f)
        
    return _DB_CACHE


def get_available_ufs() -> List[Tuple[str, str]]:
    """
    Retorna a lista de UFs disponíveis com código e nome por extenso.
    Ex: [('AC', 'Acre'), ..., ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ...]
    """
    db = load_tariffs_db()
    ufs_dict = db.get('ufs', {})
    res = []
    for uf, data in ufs_dict.items():
        name = data.get('name', uf)
        res.append((uf, name))
    return sorted(res, key=lambda x: x[0])


def get_cities_by_uf(uf_code: str) -> List[str]:
    """Retorna a lista ordenada de municípios cadastrados para a UF especificada."""
    db = load_tariffs_db()
    uf_upper = str(uf_code).strip().upper()
    ufs_dict = db.get('ufs', {})
    if uf_upper in ufs_dict:
        return list(ufs_dict[uf_upper].get('cities', []))
    return []


def get_city_data(uf_code: str, city_name: str) -> Optional[Dict[str, Any]]:
    """
    Retorna o dicionário completo de tarifas e metadados de uma cidade (categoria Residencial).
    Chave no formato 'UF - Município'.
    """
    db = load_tariffs_db()
    uf_clean = str(uf_code).strip().upper()
    m_clean = str(city_name).strip()
    
    key = f"{uf_clean} - {m_clean}"
    cities_dict = db.get('cities', {})
    if key in cities_dict:
        return cities_dict[key]
        
    # Busca case-insensitive caso haja pequenas variações
    for k, v in cities_dict.items():
        if v.get('uf', '').upper() == uf_clean and v.get('municipio', '').lower() == m_clean.lower():
            return v
            
    return None


def esgoto_do_municipio(dados: Dict[str, Any]) -> Tuple[int, float]:
    """``(sewage_mode, sewage_rate)`` do município, prontos para o projeto.

    Percentual da água na maior parte da base; preço por m³ consumido onde o
    prestador fatura o esgoto pelo consumo, como a CORSAN.
    """
    if int(dados.get("esgoto_modo", ESGOTO_PERCENTUAL) or ESGOTO_PERCENTUAL) == ESGOTO_POR_M3 and dados.get("esgoto_r_m3"):
        return ESGOTO_POR_M3, float(dados["esgoto_r_m3"])
    return ESGOTO_PERCENTUAL, float(dados.get("esgoto_pct", 80.0) or 80.0)


def rotulo_do_esgoto(dados: Dict[str, Any]) -> str:
    """«80%» ou «R$ 6,40/m³», para as telas."""
    modo, valor = esgoto_do_municipio(dados)
    if modo == ESGOTO_POR_M3:
        return f"R$ {valor:.2f}/m³".replace(".", ",")
    return f"{valor:.0f}%"


def get_city_tariffs_by_category(
    uf_code: str,
    city_name: str,
    category: str = "residencial"
) -> Optional[Dict[str, Any]]:
    """
    Retorna a estrutura tarifária adaptada para a categoria especificada:
    - 'residencial': Tarifa normal padrão (1.0x)
    - 'comercial': Comercial / Serviços (~1.85x)
    - 'industrial': Industrial (~2.30x)
    - 'publica': Poder Público / Institucional (~1.65x)
    - 'social': Tarifa Social de Água e Esgoto / Baixa Renda (0.50x)
    """
    base_data = get_city_data(uf_code, city_name)
    if not base_data:
        return None

    cat_key = str(category).strip().lower()
    cat_info = CATEGORIAS_TARIFARIAS.get(cat_key, CATEGORIAS_TARIFARIAS["residencial"])

    res = dict(base_data)
    res["categoria_tarifaria"] = cat_key
    res["categoria_nome"] = cat_info["nome"]
    res["categoria_icone"] = cat_info["icone"]

    mult_agua = cat_info["mult_agua"]
    mult_fixo = cat_info["mult_fixo"]
    mult_energia = cat_info["mult_energia"]

    # Se for residencial padrão, retorna os valores base originais
    if cat_key == "residencial":
        return res

    # Ajusta Parcela Fixa
    orig_fixo = float(base_data.get("tarifa_fixa_mensal", 0.0) or 0.0)
    res["tarifa_fixa_mensal"] = round(orig_fixo * mult_fixo, 2)

    # Ajusta Faixas Volumétricas
    orig_faixas = base_data.get("faixas", [])
    new_faixas = []
    for inf, sup, rate, t_tipo in orig_faixas:
        # O expoente da tabela exponencial é adimensional: só o preço-base escala.
        new_rate = rate if int(t_tipo) == EXPOENTE_DE_CONSUMO else round(rate * mult_agua, 4)
        new_faixas.append([inf, sup, new_rate, t_tipo])
    res["faixas"] = new_faixas
    if base_data.get("esgoto_r_m3"):
        res["esgoto_r_m3"] = round(float(base_data["esgoto_r_m3"]) * mult_agua, 4)

    # Ajusta Energia Elétrica
    orig_ene = float(base_data.get("energia_r_kwh", 0.75) or 0.75)
    res["energia_r_kwh"] = round(orig_ene * mult_energia, 5)

    return res


def search_cities(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Busca cidades por nome ou estado."""
    db = load_tariffs_db()
    q = query.strip().lower()
    if not q:
        return []
        
    matches = []
    cities_dict = db.get('cities', {})
    for k, v in cities_dict.items():
        m_name = v.get('municipio', '').lower()
        uf = v.get('uf', '').lower()
        estado = v.get('estado', '').lower()
        prestador = v.get('prestador_saneamento', '').lower()
        
        if q in m_name or q in f"{uf} - {m_name}" or q in estado or q in prestador:
            matches.append(v)
            if len(matches) >= limit:
                break
                
    return matches


def get_total_cities_count() -> int:
    """Retorna o número total de municípios no banco de dados."""
    db = load_tariffs_db()
    return len(db.get('cities', {}))
