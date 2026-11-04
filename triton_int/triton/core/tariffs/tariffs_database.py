"""
Módulo de Banco de Dados de Tarifas Municipais de Saneamento e Energia (Triton).
Contém a base auditada de 652 municípios brasileiros em todas as 27 Unidades Federativas,
com a categoria Residencial para os 652 municípios e as demais categorias onde a tabela
oficial do prestador foi coletada.
"""

from __future__ import annotations

import os
import sys
import json
from typing import List, Tuple, Dict, Any, Optional

from triton.core.tariffs_structure import ESGOTO_PERCENTUAL, ESGOTO_POR_M3

_DB_CACHE: Optional[Dict[str, Any]] = None

# =====================================================================================================================
# CATEGORIAS TARIFÁRIAS NACIONAIS (ÁGUA, ESGOTO E ENERGIA ELÉTRICA)
# =====================================================================================================================

#: As categorias de consumidor das tabelas das concessionárias. Só a residencial foi
#: coletada para os 652 municípios; as outras entram município a município, em
#: ``categorias`` do registro, à medida que a tabela oficial de cada prestador é
#: levantada (tarifas/categorias/). Não há multiplicador sobre a residencial: uma
#: categoria sem tabela coletada não é oferecida como dado do catálogo.
CATEGORIAS_TARIFARIAS: Dict[str, Dict[str, Any]] = {
    "residencial": {"id": "residencial", "nome": "Residencial Normal", "icone": "🏠",
                    "desc": "Domicílios unifamiliares e multifamiliares."},
    "comercial": {"id": "comercial", "nome": "Comercial / Serviços", "icone": "💼",
                  "desc": "Comércio, escritórios, consultórios e prestadores de serviços."},
    "industrial": {"id": "industrial", "nome": "Industrial", "icone": "🏭",
                   "desc": "Indústrias de transformação e plantas fabris."},
    "publica": {"id": "publica", "nome": "Pública / Institucional", "icone": "🏛️",
                "desc": "Órgãos públicos, escolas públicas, universidades e hospitais públicos."},
    "social": {"id": "social", "nome": "Social / Baixa Renda", "icone": "🤝",
               "desc": "Tarifa social de água e esgoto (Lei nº 14.898/2024)."},
}


#: Nome do arquivo do banco tarifário, único em toda a distribuição.
NOME_DO_BANCO = "brazil_cities_tariffs.json"


def _find_database_file() -> str:
    """Localiza o banco tarifário, em execução normal ou empacotado com PyInstaller.

    O banco é **único** e vive dentro do pacote, em ``triton/data/``. Assim ele
    acompanha tanto a instalação por ``pip`` (via ``package-data``) quanto o executável
    congelado, e o atualizador tarifário escreve exatamente no arquivo que o programa lê.

    Já houve duas cópias — ``data/tarifas/`` e ``triton/data/`` — ambas
    empacotadas, com esta busca preferindo a primeira. Elas divergiram em 465 das 652
    cidades sem que nada acusasse, e a cópia lida tinha a primeira faixa tarifária
    zerada em 464 delas. Manter uma única cópia elimina a classe do problema; o teste
    `tests/unit/test_tariffs_structure.py` impede o reaparecimento de uma segunda.
    """
    diretorio_do_pacote = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # triton/

    candidatos = []
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        candidatos.append(os.path.join(sys._MEIPASS, "triton", "data", NOME_DO_BANCO))
    candidatos.append(os.path.join(diretorio_do_pacote, "data", NOME_DO_BANCO))
    candidatos.append(os.path.join(os.path.dirname(diretorio_do_pacote), "data", NOME_DO_BANCO))

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
        
    try:
        db_path = _find_database_file()
    except FileNotFoundError:
        # Só a Edição Brasil traz o banco de 652 municípios. Nas outras, ele não existe, e as
        # telas e rotinas que o consultam recebem um banco vazio em vez de um erro. Na Brasil a
        # falta do arquivo continua sendo erro (instalação quebrada).
        from triton.core.edition import EDITION_BRL, get_current_edition
        if get_current_edition() == EDITION_BRL:
            raise
        _DB_CACHE = {"ufs": {}, "cities": {}}
        return _DB_CACHE
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


def procedencia_tarifaria(dados: Optional[Dict[str, Any]]) -> str:
    """De onde vem a residencial do município, em uma linha, para as telas.

    Com documento: o arquivo guardado em `tarifas/fontes/`, a tabela usada e a vigência,
    e a regra de abrangência quando o documento é geral e não nomeia o município.
    Sem documento: diz isso, e o motivo quando o dado é sabidamente ruim (grau D).
    """
    if not dados:
        return "--"
    doc = dados.get("fonte_documento")
    if doc and dados.get("fonte_registro"):
        tabela = dados.get("fonte_tabela")
        vig = dados.get("vigencia_saneamento")
        texto = f"documento oficial «{doc}»"
        if tabela:
            texto += f", {tabela}"
        if vig:
            texto += f"; vigência {vig}"
        if dados.get("fonte_abrangencia"):
            texto += f"; aplicado por abrangência: {dados['fonte_abrangencia']}"
        if dados.get("tarifa_representativa"):
            texto += (f"; tarifa representativa ({dados['tarifa_representativa']}), "
                      f"{len(dados.get('variantes') or [])} alternativa(s)")
            intervalo = intervalo_entre_tabelas(dados)
            if intervalo:
                texto += f"; conta de água e esgoto entre as tabelas: {intervalo}"
        return texto
    grau = str(dados.get("confianca_grau") or "")
    if grau.startswith("D"):
        return "dado a revisar: " + (dados.get("motivo_dado_ruim") or grau.split("—", 1)[-1].strip())
    return "catálogo sem documento oficial guardado" + (f" (grau {grau})" if grau else "")


def tabelas_do_municipio(dados: Optional[Dict[str, Any]]) -> List[Tuple[str, Dict[str, Any]]]:
    """A residencial e as alternativas do município: [(rótulo, tabela)], a principal primeiro.

    Município com tarifa por bairro ou área (Rio de Janeiro) ou com «Tarifa 1» para quem
    consome pouco guarda uma tabela representativa e as demais em ``variantes``.
    """
    if not dados:
        return []
    principal = "representativa" if dados.get("tarifa_representativa") else "residencial"
    return [(principal, dados)] + [(v.get("rotulo", "alternativa"), v) for v in (dados.get("variantes") or [])]


def intervalo_entre_tabelas(dados: Optional[Dict[str, Any]], consumos=(10.0, 20.0)) -> str:
    """«10 m³: R$ 80,10 a R$ 96,20; 20 m³: …», conta de água e esgoto entre as tabelas do município.

    Vazio quando o município só tem uma tabela.
    """
    tabelas = tabelas_do_municipio(dados)
    if len(tabelas) < 2:
        return ""
    from triton.core.economic import calculate_water_bill
    partes = []
    for q in consumos:
        contas = []
        for _, t in tabelas:
            modo, valor = esgoto_do_municipio(t)
            contas.append(calculate_water_bill(q * 1000.0, [tuple(f) for f in t["faixas"]], modo, valor))
        fmt = lambda v: f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        partes.append(f"{q:g} m³: {fmt(min(contas))} a {fmt(max(contas))}")
    return "; ".join(partes)


def categorias_coletadas(data: Optional[Dict[str, Any]]) -> List[str]:
    """As categorias com tabela oficial no registro do município, residencial primeiro."""
    if not data:
        return []
    extras = [c for c in (data.get("categorias") or {}) if c in CATEGORIAS_TARIFARIAS and c != "residencial"]
    return ["residencial"] + [c for c in CATEGORIAS_TARIFARIAS if c in extras]


def get_city_tariffs_by_category(
    uf_code: str,
    city_name: str,
    category: str = "residencial"
) -> Optional[Dict[str, Any]]:
    """A estrutura tarifária do município na categoria pedida, como a tabela oficial a traz.

    A residencial é o registro do catálogo. As demais vêm de ``categorias`` do registro,
    que guarda, por categoria, as faixas, a parcela fixa, o esgoto, a fonte e a vigência
    levantados da resolução do prestador; o que a categoria não traz é herdado do registro
    (o prestador, a agência, a energia). Categoria sem tabela coletada devolve ``None``:
    o programa não estima uma tarifa a partir de outra.
    """
    base_data = get_city_data(uf_code, city_name)
    if not base_data:
        return None

    cat_key = str(category or "residencial").strip().lower()
    if cat_key not in CATEGORIAS_TARIFARIAS:
        return None
    if cat_key == "residencial":
        res = dict(base_data)
    else:
        coletada = (base_data.get("categorias") or {}).get(cat_key)
        if not coletada:
            return None
        res = dict(base_data)
        res.update(coletada)
    res.pop("categorias", None)
    cat_info = CATEGORIAS_TARIFARIAS[cat_key]
    res["categoria_tarifaria"] = cat_key
    res["categoria_nome"] = cat_info["nome"]
    res["categoria_icone"] = cat_info["icone"]
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
