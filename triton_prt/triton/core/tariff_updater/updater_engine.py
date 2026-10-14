"""
Motor de Atualização e Orquestração das Tarifas Nacionais (Triton).
Integra os scrapers da ANEEL e de saneamento, recompila o banco de dados unificado compacto
e gera métricas transparentes de qualidade e necessidade de revisão manual.
"""

from __future__ import annotations

import os
import json
import csv
import datetime as dt
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

from .aneel_updater import AneelTariffUpdater
from .sanitation_scrapers import SanitationScraperRegistry

from triton.core.tariff_regimes import validar_estrutura


class TariffUpdateEngine:
    """Orquestrador do processo completo de atualização e auditoria tarifária."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path(__file__).resolve().parents[3]
        self.json_db_path = self.root_dir / "triton" / "data" / "brazil_cities_tariffs.json"
        self.csv_catalog_path = self.root_dir / "tarifas" / "catalogo_tarifas_auditado_652.csv"
        
        self.aneel_updater = AneelTariffUpdater(cache_dir=self.root_dir / "tmp")
        self.sanitation_registry = SanitationScraperRegistry()

    def run_update(
        self,
        mode: str = "all",  # "all", "aneel", "sanitation"
        target_uf: Optional[str] = None,
        target_city: Optional[str] = None,
        force_download: bool = False,
        dry_run: bool = False,
    ) -> Dict[str, Any]:
        """
        Executa a atualização das tarifas para as 652 cidades.
        
        Retorna um dicionário com:
        - "stats": contagem de status de energia, saneamento e global
        - "cities_results": lista detalhada com os dados de cada município
        - "manual_review_needed": lista de cidades que requerem revisão humana
        - "dry_run": boolean indicando se gravou em disco
        """
        if not self.json_db_path.exists():
            raise FileNotFoundError(f"Banco de tarifas não encontrado: {self.json_db_path}")

        with open(self.json_db_path, "r", encoding="utf-8") as f:
            db_data = json.load(f)

        # 1. Carrega base ANEEL se aplicável
        if mode in ("all", "aneel"):
            print(" [🔍 Engine] Carregando e parseando catálogo homologado da ANEEL...")
            self.aneel_updater.load_and_parse(force_download=force_download)

        cities_dict = db_data.get("cities", {})
        results: List[Dict[str, Any]] = []
        manual_reviews: List[Dict[str, Any]] = []
        
        stats = {
            "total_cities": len(cities_dict),
            "processed": 0,
            "energy_auto_updated": 0,
            "energy_expired_ref": 0,
            "energy_manual": 0,
            "sanitation_scraped": 0,
            "sanitation_verified": 0,
            "sanitation_manual": 0,
            "overall_auto_or_verified": 0,
            "overall_manual_needed": 0,
        }

        print(f" [⚙️ Engine] Processando {len(cities_dict)} municípios (Modo: {mode.upper()})...")

        for key, city_data in cities_dict.items():
            uf = city_data.get("uf", "").strip().upper()
            muni = city_data.get("municipio", "").strip()

            # Filtros opcionais de UF e Cidade
            if target_uf and uf != target_uf.upper():
                continue
            if target_city and target_city.lower() not in muni.lower():
                continue

            stats["processed"] += 1
            updated_city = dict(city_data)

            # 2. Atualização de Energia Elétrica (ANEEL)
            if mode in ("all", "aneel"):
                distributor = city_data.get("distribuidora_energia", "")
                aneel_match = self.aneel_updater.get_tariff_for_distributor(distributor)
                
                if aneel_match:
                    updated_city["energia_r_kwh"] = aneel_match["energia_r_kwh"]
                    updated_city["energia_ato"] = aneel_match["energia_ato"]
                    updated_city["energia_fonte_url"] = aneel_match["fonte_url"]
                    
                    status_vig = aneel_match.get("energia_status_vigencia", "VIGENTE")
                    if status_vig == "VIGENTE":
                        updated_city["status_energia"] = "AUTO_UPDATED"
                        stats["energy_auto_updated"] += 1
                    else:
                        updated_city["status_energia"] = "EXPIRED_ANEEL_REF"
                        stats["energy_expired_ref"] += 1
                else:
                    updated_city["status_energia"] = "MANUAL_REVIEW"
                    stats["energy_manual"] += 1

            # 3. Atualização de Saneamento (Água e Esgoto)
            if mode in ("all", "sanitation"):
                san_res = self.sanitation_registry.update_city_sanitation(muni, uf, updated_city)
                updated_city.update(san_res)
                
                san_status = updated_city.get("update_status_sanitation", "VERIFIED_AUDIT")
                if san_status == "AUTO_SCRAPED":
                    stats["sanitation_scraped"] += 1
                elif san_status == "VERIFIED_AUDIT":
                    stats["sanitation_verified"] += 1
                else:
                    stats["sanitation_manual"] += 1

            # 4. Status Global do Município
            has_manual_san = updated_city.get("update_status_sanitation") == "MANUAL_REVIEW_NEEDED"
            has_manual_ene = updated_city.get("status_energia") == "MANUAL_REVIEW"
            
            if has_manual_san or has_manual_ene:
                updated_city["status_global"] = "MANUAL_REVIEW_NEEDED"
                stats["overall_manual_needed"] += 1
                manual_reviews.append({
                    "uf": uf,
                    "municipio": muni,
                    "prestador": updated_city.get("prestador_saneamento"),
                    "distribuidora": updated_city.get("distribuidora_energia"),
                    "motivo_saneamento": updated_city.get("status_desc_sanitation") if has_manual_san else None,
                    "fonte_url": updated_city.get("fonte_url"),
                })
            else:
                updated_city["status_global"] = "AUTO_OR_VERIFIED"
                stats["overall_auto_or_verified"] += 1

            # PORTA DE VALIDACAO ESTRUTURAL
            #
            # O motor raspa fontes das concessionarias, e antes desta revisao gravava o
            # que raspasse sem conferir a ESTRUTURA. Isso reintroduzia, a cada
            # rodada, os defeitos que esta revisao corrigiu: minimo diluido em
            # tarifa unitaria, tabela truncada, lacuna entre faixas. Automatico e
            # periodico, e portanto pior que o defeito original.
            #
            # A porta nao derruba a rodada: conserva o registro ANTERIOR do
            # municipio cuja estrutura nova tem erro e o manda para revisao
            # manual. Uma pagina que mudou de layout nao pode nem derrubar a base
            # nem entrar nela em silencio.
            erros_estrutura = [
                a for a in validar_estrutura(updated_city) if a.gravidade == "erro"
            ]
            if erros_estrutura:
                anterior = cities_dict.get(key)
                motivo = "; ".join(a.mensagem for a in erros_estrutura)
                stats["structure_rejected"] = stats.get("structure_rejected", 0) + 1
                manual_reviews.append({
                    "uf": uf,
                    "municipio": muni,
                    "prestador": updated_city.get("prestador_saneamento"),
                    "distribuidora": updated_city.get("distribuidora_energia"),
                    "motivo_saneamento": f"estrutura tarifária rejeitada: {motivo}",
                    "fonte_url": updated_city.get("fonte_url"),
                })
                if anterior is not None:
                    anterior = dict(anterior)
                    anterior["status_global"] = "MANUAL_REVIEW_NEEDED"
                    anterior["_estrutura_rejeitada_em"] = dt.date.today().isoformat()
                    anterior["_estrutura_rejeitada_motivo"] = motivo
                    cities_dict[key] = anterior
                    results.append(anterior)
                    continue
                # Sem registro anterior, o municipio entra marcado.
                updated_city["status_global"] = "MANUAL_REVIEW_NEEDED"
                updated_city["estrutura_incompleta"] = True
                updated_city["_ressalva_estrutura"] = motivo

            # Atualiza no dicionário mestre
            cities_dict[key] = updated_city
            results.append(updated_city)

        # 5. Gravação dos arquivos se não for dry_run
        if not dry_run and mode == "all" and not target_uf and not target_city:
            db_data["version"] = dt.date.today().isoformat()
            db_data["last_update"] = dt.datetime.now().isoformat()
            
            # Grava JSON compacto oficial
            with open(self.json_db_path, "w", encoding="utf-8") as f:
                json.dump(db_data, f, ensure_ascii=False, separators=(',', ':'))
            print(f" [💾 Engine] Banco JSON oficial compactado atualizado em: {self.json_db_path} ({self.json_db_path.stat().st_size:,} bytes)")
            
            # Atualiza catálogo CSV consolidado
            self._write_csv_catalog(results)

        return {
            "stats": stats,
            "cities_results": results,
            "manual_review_needed": manual_reviews,
            "dry_run": dry_run,
        }

    def _write_csv_catalog(self, cities_list: List[Dict[str, Any]]):
        """Gera o catálogo CSV consolidado de auditoria."""
        if not cities_list:
            return
            
        fieldnames = [
            "regiao", "uf", "municipio", "prestador_saneamento", "agencia_reguladora",
            "tarifa_fixa_agua_r_mes", "esgoto_pct_sobre_agua", "faixas_desc",
            "distribuidora_energia", "energia_aneel_sem_tributos_r_kwh", "energia_aneel_ato",
            "status_energia", "status_saneamento", "status_global", "fonte_saneamento",
            "data_atualizacao"
        ]
        
        self.csv_catalog_path.parent.mkdir(parents=True, exist_ok=True)
        today_str = dt.date.today().isoformat()
        
        with open(self.csv_catalog_path, "w", encoding="utf-8-sig", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for c in cities_list:
                writer.writerow({
                    "regiao": c.get("regiao", ""),
                    "uf": c.get("uf", ""),
                    "municipio": c.get("municipio", ""),
                    "prestador_saneamento": c.get("prestador_saneamento", ""),
                    "agencia_reguladora": c.get("agencia_reguladora", ""),
                    "tarifa_fixa_agua_r_mes": c.get("tarifa_fixa_mensal", 0.0),
                    "esgoto_pct_sobre_agua": c.get("esgoto_pct", 80.0),
                    "faixas_desc": c.get("faixas_desc", ""),
                    "distribuidora_energia": c.get("distribuidora_energia", ""),
                    "energia_aneel_sem_tributos_r_kwh": c.get("energia_r_kwh", 0.0),
                    "energia_aneel_ato": c.get("energia_ato", ""),
                    "status_energia": c.get("status_energia", ""),
                    "status_saneamento": c.get("update_status_sanitation", ""),
                    "status_global": c.get("status_global", ""),
                    "fonte_saneamento": c.get("fonte_url", ""),
                    "data_atualizacao": today_str,
                })
        print(f" [📄 Engine] Catálogo CSV atualizado em: {self.csv_catalog_path}")