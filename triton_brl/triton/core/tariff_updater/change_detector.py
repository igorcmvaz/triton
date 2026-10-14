"""
Módulo de Detecção Inteligente de Alterações e Monitoramento de Integridade Tarifária.
Utiliza assinaturas criptográficas (SHA-256), cabeçalhos HTTP (ETag, Last-Modified)
e controle de histórico para alertar quando páginas ou resoluções de concessionárias forem alteradas.
"""

from __future__ import annotations

import os
import io
import json
import hashlib
import datetime as dt
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests


class TariffChangeDetector:
    """Gerencia o registro de assinaturas e a detecção de alterações em links oficiais."""

    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = root_dir or Path(__file__).resolve().parents[3]
        self.registry_path = self.root_dir / "data" / "tarifas" / "change_tracking_registry.json"
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,application/pdf,*/*;q=0.8",
        })
        self._registry: Dict[str, Any] = self.load_registry()

    def load_registry(self) -> Dict[str, Any]:
        """Carrega o registro persistente de hashes e histórico de mudanças."""
        if self.registry_path.exists():
            try:
                with open(self.registry_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "last_check_all": None,
            "monitored_urls": {}
        }

    def save_registry(self):
        """Salva o registro em formato JSON compacto."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(self._registry, f, ensure_ascii=False, indent=2)

    @staticmethod
    def compute_sha256(content: bytes) -> str:
        """Calcula o hash SHA-256 do conteúdo binário ou texto."""
        return hashlib.sha256(content).hexdigest()

    def check_url(
        self,
        url: str,
        provider_name: str,
        uf: str,
        scraper_parsed_ok: Optional[bool] = None,
        timeout: int = 10
    ) -> Dict[str, Any]:
        """
        Verifica se a URL sofreu modificação desde a última checagem.
        Retorna o status detalhado da URL e atualiza o registro.
        """
        now_iso = dt.datetime.now().isoformat()
        current_entry = self._registry.get("monitored_urls", {}).get(url, {})
        old_hash = current_entry.get("content_sha256")
        old_etag = current_entry.get("etag")
        old_last_mod = current_entry.get("last_modified_header")
        history = current_entry.get("change_history", [])

        result = {
            "url": url,
            "provider": provider_name,
            "uf": uf,
            "last_checked": now_iso,
            "http_status": None,
            "content_sha256": old_hash,
            "content_length": current_entry.get("content_length", 0),
            "etag": old_etag,
            "last_modified_header": old_last_mod,
            "status": "UNCHANGED",
            "status_desc": "Página e documento íntegros, sem alterações detectadas.",
            "requires_manual_action": False,
            "change_history": history,
        }

        if not url or not url.startswith("http"):
            result["status"] = "INVALID_URL"
            result["status_desc"] = "URL ausente ou inválida."
            result["requires_manual_action"] = True
            return result

        try:
            # Requisição GET leve (até 2MB por documento)
            resp = self.session.get(url, timeout=timeout, stream=True, allow_redirects=True)
            result["http_status"] = resp.status_code
            result["etag"] = resp.headers.get("ETag") or old_etag
            result["last_modified_header"] = resp.headers.get("Last-Modified") or old_last_mod

            if resp.status_code >= 400:
                result["status"] = "HTTP_ERROR"
                result["status_desc"] = f"Erro HTTP {resp.status_code} ao acessar o link oficial."
                result["requires_manual_action"] = True
                return result

            # Lê conteúdo com limite seguro
            raw_bytes = bytearray()
            for chunk in resp.iter_content(chunk_size=64 * 1024):
                raw_bytes.extend(chunk)
                if len(raw_bytes) > 2 * 1024 * 1024:  # Limite de 2MB para hash
                    break

            new_hash = self.compute_sha256(bytes(raw_bytes))
            result["content_sha256"] = new_hash
            result["content_length"] = len(raw_bytes)

            if old_hash is None:
                # Primeira vez que a URL é registrada
                result["status"] = "INITIALIZED"
                result["status_desc"] = "Assinatura digital inicial registrada com sucesso."
                result["requires_manual_action"] = False
                history.append({
                    "timestamp": now_iso,
                    "event": "INITIAL_FINGERPRINT",
                    "hash": new_hash[:12],
                })
            elif new_hash != old_hash:
                # Mudança de conteúdo detectada!
                if scraper_parsed_ok is True:
                    result["status"] = "PAGE_CHANGED_PARSED"
                    result["status_desc"] = "Página atualizada pela concessionária! Novo valor extraído com sucesso pelo scraper."
                    result["requires_manual_action"] = False
                else:
                    result["status"] = "PAGE_CHANGED_MANUAL_REVIEW_REQUIRED"
                    result["status_desc"] = "ALERTA: A página/resolução mudou! Scraper requer validação manual das novas faixas."
                    result["requires_manual_action"] = True

                history.append({
                    "timestamp": now_iso,
                    "event": "CONTENT_CHANGED",
                    "old_hash": old_hash[:12] if old_hash else "None",
                    "new_hash": new_hash[:12],
                    "requires_manual": result["requires_manual_action"],
                })
            else:
                # Hash idêntico
                result["status"] = "UNCHANGED"
                result["status_desc"] = "Conteúdo verificado e inalterado na fonte oficial."
                result["requires_manual_action"] = False

        except requests.exceptions.Timeout:
            result["status"] = "CONNECTION_TIMEOUT"
            result["status_desc"] = "Tempo limite esgotado ao conectar ao portal da concessionária."
            result["requires_manual_action"] = False
        except requests.exceptions.RequestException as e:
            result["status"] = "CONNECTION_FAILED"
            result["status_desc"] = f"Falha de conexão com a fonte oficial ({type(e).__name__})."
            result["requires_manual_action"] = True

        result["change_history"] = history[-10:]  # Mantém os últimos 10 eventos
        
        # Salva no dicionário interno
        self._registry.setdefault("monitored_urls", {})[url] = result
        return result

    def check_all_cities(
        self,
        cities_dict: Dict[str, Any],
        max_workers: int = 8
    ) -> Dict[str, Any]:
        """
        Executa verificação paralela de todas as URLs únicas do catálogo nacional (652 cidades).
        """
        unique_targets: Dict[str, Tuple[str, str]] = {}
        for key, c in cities_dict.items():
            url = c.get("fonte_url")
            if url and url.startswith("http"):
                prest = c.get("prestador_saneamento", "Concessionária")
                uf = c.get("uf", "BR")
                if url not in unique_targets:
                    unique_targets[url] = (prest, uf)

        print(f" [📡 ChangeDetector] Verificando integridade de {len(unique_targets)} URLs oficiais únicas...")

        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.check_url, url, prest, uf): url
                for url, (prest, uf) in unique_targets.items()
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    res = future.result()
                    results[url] = res
                except Exception as e:
                    results[url] = {
                        "url": url,
                        "status": "CHECK_ERROR",
                        "status_desc": str(e),
                        "requires_manual_action": True
                    }

        self._registry["last_check_all"] = dt.datetime.now().isoformat()
        self.save_registry()

        # Estatísticas consolidadas
        stats = {
            "total_urls": len(unique_targets),
            "unchanged_or_init": sum(1 for r in results.values() if r["status"] in ("UNCHANGED", "INITIALIZED")),
            "changed_auto_parsed": sum(1 for r in results.values() if r["status"] == "PAGE_CHANGED_PARSED"),
            "changed_manual_required": sum(1 for r in results.values() if r["status"] == "PAGE_CHANGED_MANUAL_REVIEW_REQUIRED"),
            "connection_issues": sum(1 for r in results.values() if r["status"] in ("HTTP_ERROR", "CONNECTION_FAILED", "CONNECTION_TIMEOUT")),
        }
        return {
            "stats": stats,
            "url_results": results,
        }
