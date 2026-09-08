"""
Módulo de Atualização de Tarifas de Energia Elétrica Residencial B1 via ANEEL.
Baixa e processa a base aberta oficial de tarifas homologadas das distribuidoras.
"""

from __future__ import annotations

import os
import csv
import io
import datetime as dt
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, Optional, List
import requests

ANEEL_OPEN_DATA_URL = (
    "https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/"
    "resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4/download/"
    "tarifas-homologadas-distribuidoras-energia-eletrica.csv"
)

ANEEL_METHOD_URL = (
    "https://www.gov.br/aneel/pt-br/centrais-de-conteudos/relatorios-e-indicadores/"
    "tarifas-e-informacoes-economico-financeiras"
)

# Mapeamento canônico de nomes de distribuidoras da base municipal para a nomenclatura ANEEL
ANEEL_DISTRIBUTOR_ALIASES = {
    "Amazonas Energia": "Âmbar Amazonas",
    "CEEE Equatorial": "CEEE-D",
    "CEMIG Distribuição": "CEMIG-D",
    "COCEL": "COCEL",
    "COPEL Distribuição": "COPEL-DIS",
    "CPFL Paulista": "CPFL-PAULISTA",
    "CPFL Piratininga": "CPFL-PIRATINING",
    "CPFL Piratininga – Oeste": "CPFL-PIRATINING",
    "CPFL Santa Cruz": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Jaguari": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Leste Paulista": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Mococa": "CPFL Santa Cruz",
    "CPFL Santa Cruz – Sul Paulista": "CPFL Santa Cruz",
    "Cooperaliança": "COOPERALIANÇA",
    "DCELT": "DCELT",
    "DEMEI": "DEMEI",
    "DMED Poços de Caldas": "DMED",
    "EDP Espírito Santo": "EDP ES",
    "EDP São Paulo": "EDP SP",
    "ELFSM – Empresa Luz e Força Santa Maria": "ELFSM",
    "ENEL Distribuição São Paulo": "ELETROPAULO",
    "Enel Distribuição São Paulo – Sul": "ELETROPAULO",
    "Eletrocar": "ELETROCAR",
    "Enel Ceará": "ENEL CE",
    "Enel Distribuição Rio": "ENEL RJ",
    "Energisa Acre (EAC)": "EAC",
    "Energisa Mato Grosso": "EMT",
    "Energisa Mato Grosso do Sul": "EMS",
    "Energisa Minas Gerais (EMG)": "EMR",
    "Energisa Minas Rio": "EMR",
    "Energisa Paraíba": "EPB",
    "Energisa Rondônia": "ERO",
    "Energisa Sergipe": "ESE",
    "Energisa Sul-Sudeste – Leste": "ESS",
    "Energisa Sul-Sudeste – Norte": "ESS",
    "Energisa Sul-Sudeste – Oeste": "ESS",
    "Energisa Sul-Sudeste – Sul": "ESS",
    "Energisa Tocantins": "ETO",
    "Equatorial Alagoas": "EQUATORIAL AL",
    "Equatorial Amapá": "CEA",
    "Equatorial Goiás": "EQUATORIAL GO",
    "Equatorial Maranhão": "EQUATORIAL MA",
    "Equatorial Pará": "EQUATORIAL PA",
    "Equatorial Piauí": "EQUATORIAL PI",
    "CELESC Distribuição": "CELESC",
    "Sulgipe": "SULGIPE",
    "Light Serviços de Eletricidade": "LIGHT SESA",
    "Light Serviços de Eletricidade – Vale do Paraíba": "LIGHT SESA",
    "Neoenergia Brasília": "Neoenergia Brasília",
    "Neoenergia Coelba": "COELBA",
    "Neoenergia Cosern": "COSERN",
    "Neoenergia Elektro": "ELEKTRO",
    "Neoenergia Elektro – Leste": "ELEKTRO",
    "Neoenergia Elektro – Oeste": "ELEKTRO",
    "Neoenergia Elektro – Sul": "ELEKTRO",
    "Neoenergia Pernambuco (Celpe)": "Neoenergia PE",
    "RGE Sul (CPFL)": "RGE",
    "Roraima Energia": "ÂMBAR ENERGIA RR",
}


def _strip_accents(text: str) -> str:
    """Normaliza texto removendo acentos e convertendo para minúsculas."""
    if not text:
        return ""
    normalized = unicodedata.normalize("NFKD", str(text))
    return "".join(c for c in normalized if not unicodedata.combining(c)).strip().lower()


def _num(val: Any) -> Optional[float]:
    """Converte valor numérico com vírgula para float."""
    if val is None:
        return None
    s = str(val).strip()
    if not s or s.lower() == "null":
        return None
    try:
        return float(s.replace(",", "."))
    except ValueError:
        return None


class AneelTariffUpdater:
    """Gerencia a consulta e processamento das tarifas de energia residencial B1 da ANEEL."""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or (Path(__file__).resolve().parents[3] / "tmp")
        self.cache_file = self.cache_dir / "aneel_tarifas_homologadas_2026.csv"
        self._parsed_tariffs: Dict[str, Dict[str, Any]] = {}
        self._normalized_index: Dict[str, str] = {}

    def fetch_latest_csv(self, force_download: bool = False) -> str:
        """
        Baixa o CSV mais recente da ANEEL ou utiliza o cache local se disponível.
        Retorna o caminho do arquivo CSV pronto para leitura.
        """
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        if not force_download and self.cache_file.exists() and self.cache_file.stat().st_size > 1024:
            return str(self.cache_file)
            
        print(" [⚡ ANEEL] Baixando catálogo atualizado de tarifas homologadas...")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/csv,text/plain,*/*"
        }
        try:
            resp = requests.get(ANEEL_OPEN_DATA_URL, headers=headers, timeout=60, stream=True)
            resp.raise_for_status()
            with open(self.cache_file, "wb") as f:
                for chunk in resp.iter_content(chunk_size=128 * 1024):
                    if chunk:
                        f.write(chunk)
            print(f" [⚡ ANEEL] Download concluído com sucesso ({self.cache_file.stat().st_size:,} bytes).")
        except Exception as e:
            if self.cache_file.exists():
                print(f" [⚡ ANEEL] Falha no download ({e}). Utilizando arquivo de cache local existente.")
            else:
                raise RuntimeError(f"Não foi possível obter dados da ANEEL: {e}")
                
        return str(self.cache_file)

    def load_and_parse(self, force_download: bool = False) -> Dict[str, Dict[str, Any]]:
        """
        Processa o CSV e extrai para cada distribuidora o ato homologatório vigente mais recente
        com a tarifa residencial B1 convencional (TUSD + TE em R$/kWh).
        """
        csv_path = self.fetch_latest_csv(force_download=force_download)
        
        candidates = defaultdict(list)
        today = dt.date.today()

        with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f, delimiter=";")
            for row in reader:
                try:
                    start = dt.date.fromisoformat(row["DatInicioVigencia"])
                    end = dt.date.fromisoformat(row["DatFimVigencia"])
                except (ValueError, TypeError, KeyError):
                    continue

                # Critérios oficiais ANEEL para Tarifa Residencial B1 Convencional
                base_tar = str(row.get("DscBaseTarifaria", "")).strip()
                subgrupo = str(row.get("DscSubGrupo", "")).strip()
                modalidade = str(row.get("DscModalidadeTarifaria", "")).strip()
                classe = str(row.get("DscClasse", "")).strip()
                subclasse = str(row.get("DscSubClasse", "")).strip()
                detalhe = str(row.get("DscDetalhe", "")).strip()
                unidade = str(row.get("DscUnidadeTerciaria", "")).strip()

                if base_tar != "Tarifa de Aplicação":
                    continue
                if subgrupo != "B1":
                    continue
                if modalidade != "Convencional":
                    continue
                if classe != "Residencial":
                    continue
                if subclasse != "Residencial":
                    continue
                if detalhe != "Não se aplica":
                    continue
                if unidade != "MWh":
                    continue

                tusd = _num(row.get("VlrTUSD"))
                te = _num(row.get("VlrTE"))
                if tusd is None or te is None:
                    continue

                # Tarifa expressa em R$/kWh (valores no CSV são em R$/MWh)
                rate_kwh = (tusd + te) / 1000.0
                if rate_kwh <= 0.01 or rate_kwh > 5.0:
                    continue

                agent = str(row.get("SigAgente", "")).strip()
                if not agent:
                    continue

                ato = str(row.get("DscREH", "") or row.get("NumAtoConcessao", "")).strip()
                is_current = (start <= today <= end)

                candidates[agent].append({
                    "distribuidora": agent,
                    "energia_r_kwh": round(rate_kwh, 5),
                    "energia_ato": ato,
                    "energia_inicio_vigencia": start.isoformat(),
                    "energia_fim_vigencia": end.isoformat(),
                    "energia_status_vigencia": "VIGENTE" if is_current else "EXPIRADA",
                    "fonte_url": ANEEL_OPEN_DATA_URL,
                    "metodologia_url": ANEEL_METHOD_URL,
                    "_end": end,
                })

        current: Dict[str, Dict[str, Any]] = {}
        for agent, records in candidates.items():
            valid = [r for r in records if r["energia_status_vigencia"] == "VIGENTE"]
            chosen = max(valid or records, key=lambda r: r["_end"])
            
            if chosen["energia_status_vigencia"] == "EXPIRADA":
                days = (today - chosen["_end"]).days
                chosen["energia_status_vigencia"] = f"EXPIRADA_HA_{days}_DIAS_REFERENCIA_MAIS_RECENTE"
                
            chosen_clean = {k: v for k, v in chosen.items() if not k.startswith("_")}
            current[agent] = chosen_clean

        self._parsed_tariffs = current
        self._normalized_index = {
            _strip_accents(agent): agent for agent in current.keys()
        }
        return self._parsed_tariffs

    def get_tariff_for_distributor(self, distributor_name: str) -> Optional[Dict[str, Any]]:
        """
        Retorna os dados homologados para o nome da distribuidora (usando mapa de aliases e matching flexível).
        """
        if not self._parsed_tariffs:
            self.load_and_parse()

        name = str(distributor_name).strip()
        # 1. Checa alias direto
        if name in ANEEL_DISTRIBUTOR_ALIASES:
            aneel_key = ANEEL_DISTRIBUTOR_ALIASES[name]
            if aneel_key in self._parsed_tariffs:
                return self._parsed_tariffs[aneel_key]

        # 2. Checa chave exata
        if name in self._parsed_tariffs:
            return self._parsed_tariffs[name]

        # 3. Checa busca normalizada
        norm = _strip_accents(name)
        if norm in self._normalized_index:
            return self._parsed_tariffs[self._normalized_index[norm]]

        # 4. Busca por substring
        for agent_norm, orig_agent in self._normalized_index.items():
            if norm in agent_norm or agent_norm in norm:
                return self._parsed_tariffs[orig_agent]

        return None
