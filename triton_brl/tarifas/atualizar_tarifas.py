#!/usr/bin/env python3
"""
===============================================================================
TRITON 5 — ATUALIZADOR, WEBSCRAPER & MONITOR DE MUDANÇAS DE TARIFAS
===============================================================================
Script oficial de atualização periódica das tarifas de saneamento e energia
para as 652 cidades do estudo Triton.

USO RÁPIDO (Linha de Comando):
  python tarifas/atualizar_tarifas.py                # Atualização completa + Dashboard HTML
  python tarifas/atualizar_tarifas.py --check        # Modo Simulação / Dry-run (sem alterar o banco)
  python tarifas/atualizar_tarifas.py --aneel-only   # Atualiza exclusivamente a base ANEEL B1
  python tarifas/atualizar_tarifas.py --uf SC        # Atualiza apenas municípios de Santa Catarina
  python tarifas/atualizar_tarifas.py --city "Florianópolis" # Atualiza apenas uma cidade
  python tarifas/atualizar_tarifas.py --detect-changes       # Varre links governamentais buscando novos atos

Para detalhes completos sobre quando e como atualizar, consulte:
  tarifas/README.md  ou  tarifas/FONTES_E_METODOLOGIA.md
===============================================================================
"""

from __future__ import annotations

import os
import sys
import argparse
from pathlib import Path

# Reconfigura saída para UTF-8 seguro em consoles Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# Garante que a raiz do projeto esteja no PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from triton.core.tariff_updater import (
    TariffUpdateEngine,
    generate_update_report,
    TariffChangeDetector,
    generate_interactive_dashboard,
)


def main():
    parser = argparse.ArgumentParser(
        description="Atualizador, Webscraper, Monitor de Mudanças e Dashboard de Tarifas das 652 Cidades (Triton)"
    )
    parser.add_argument(
        "--all", action="store_true", default=True,
        help="Executa atualização completa (ANEEL + Saneamento)"
    )
    parser.add_argument(
        "--detect-changes", action="store_true",
        help="Executa verificação de integridade e hash SHA-256 das URLs oficiais"
    )
    parser.add_argument(
        "--aneel-only", action="store_true",
        help="Atualiza exclusivamente as tarifas de energia elétrica residencial B1 da ANEEL"
    )
    parser.add_argument(
        "--sanitation-only", action="store_true",
        help="Atualiza exclusivamente as tarifas de saneamento (água e esgoto)"
    )
    parser.add_argument(
        "--check", action="store_true",
        help="Modo Dry-Run: simula a atualização e audita fontes sem sobrescrever o banco de dados"
    )
    parser.add_argument(
        "--force-download", action="store_true",
        help="Força o download de um novo CSV diretamente do portal de dados abertos da ANEEL"
    )
    parser.add_argument(
        "--uf", type=str, default=None,
        help="Filtra a execução por Unidade Federativa (ex: SP, SC, MG, BA)"
    )
    parser.add_argument(
        "--city", type=str, default=None,
        help="Filtra a execução por nome de município (ex: 'São Paulo', 'Joinville')"
    )
    parser.add_argument(
        "--output-report", type=str, default="outputs/relatorio_atualizacao_tarifas.md",
        help="Caminho do relatório de auditoria gerado em Markdown"
    )
    parser.add_argument(
        "--output-dashboard", type=str, default="outputs/dashboard_tarifas.html",
        help="Caminho do Dashboard HTML interativo"
    )

    args = parser.parse_args()

    mode = "all"
    if args.aneel_only:
        mode = "aneel"
    elif args.sanitation_only:
        mode = "sanitation"

    print("=" * 80)
    print(" [TRITON 5] ATUALIZADOR, DETECTOR DE MUDANÇAS & DASHBOARD DE TARIFAS")
    print(f" Modo de Execução : {mode.upper()}")
    print(f" Simulação/Dry-run: {'SIM (Somente Leitura)' if args.check else 'NÃO (Gravação Oficial)'}")
    if args.uf:
        print(f" Filtro por UF    : {args.uf.upper()}")
    if args.city:
        print(f" Filtro por Cidade: {args.city}")
    print("=" * 80)

    engine = TariffUpdateEngine(root_dir=ROOT_DIR)
    
    try:
        results = engine.run_update(
            mode=mode,
            target_uf=args.uf,
            target_city=args.city,
            force_download=args.force_download,
            dry_run=args.check,
        )
    except Exception as e:
        print(f"\n[ERRO CRÍTICO] Falha durante a execução do motor: {e}")
        sys.exit(1)

    # Detecção de mudanças em URLs oficiais
    change_detector = TariffChangeDetector(root_dir=ROOT_DIR)
    
    if args.detect_changes or (mode == "all" and not args.uf and not args.city):
        import json
        with open(engine.json_db_path, "r", encoding="utf-8") as f:
            full_db = json.load(f)
        change_detector.check_all_cities(full_db.get("cities", {}))

    # Geração do Relatório Markdown
    report_path = ROOT_DIR / args.output_report
    generate_update_report(results, output_path=report_path)

    # Geração do Dashboard HTML Interativo
    import json
    with open(engine.json_db_path, "r", encoding="utf-8") as f:
        current_db = json.load(f)
    dashboard_path = ROOT_DIR / args.output_dashboard
    generate_interactive_dashboard(
        current_db.get("cities", {}),
        change_detector._registry,
        output_path=dashboard_path
    )

    stats = results["stats"]
    processed = max(1, stats.get("processed", 0))
    auto_ver = stats.get("overall_auto_or_verified", 0)
    manual_cnt = stats.get("overall_manual_needed", 0)

    print("\n" + "=" * 80)
    print(" [RESUMO DE EXECUÇÃO E MONITORAMENTO]")
    print("=" * 80)
    print(f" Total de Municípios Processados    : {stats.get('processed', 0)}")
    print(f" [*] Confiabilidade Alta (Auto/Audit) : {auto_ver} ({(auto_ver/processed)*100:.1f}%)")
    print(f" [!] Requer Conferência de Decreto   : {manual_cnt} ({(manual_cnt/processed)*100:.1f}%)")
    print(f" [E] ANEEL B1 - Atos Vigentes         : {stats.get('energy_auto_updated', 0)}")
    print(f" [W] Saneamento - Scraped / Auditado : {stats.get('sanitation_scraped', 0) + stats.get('sanitation_verified', 0)}")
    print("=" * 80)
    print(f" [📋] Relatório Markdown salvo em     : {report_path}")
    print(f" [📊] Dashboard HTML interativo em   : {dashboard_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
