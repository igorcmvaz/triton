#!/usr/bin/env python3
"""
Pipeline de Atualização, Detecção de Mudanças e Dashboard de Tarifas (Netuno 5).

Uso:
  python scripts/update_all_tariffs.py               # Atualização completa + Detecção + Dashboard HTML
  python scripts/update_all_tariffs.py --check       # Simulação/Dry-run com emissão de relatório e dashboard
  python scripts/update_all_tariffs.py --detect-changes # Apenas verifica integridade e mudanças nas URLs
  python scripts/update_all_tariffs.py --aneel-only  # Atualiza somente base de energia ANEEL
  python scripts/update_all_tariffs.py --uf SC       # Executa apenas para o estado de Santa Catarina
  python scripts/update_all_tariffs.py --city "Manaus" # Executa apenas para Manaus
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

from netuno.core.tariff_updater import (
    TariffUpdateEngine,
    generate_update_report,
    TariffChangeDetector,
    generate_interactive_dashboard,
)


def main():
    parser = argparse.ArgumentParser(
        description="Atualizador, Monitor de Mudanças e Dashboard de Tarifas das 652 Cidades (Netuno 5)"
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
    print(" [NETUNO 5] ATUALIZADOR, DETECTOR DE MUDANÇAS & DASHBOARD DE TARIFAS")
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
    print(f" [[lista]] Relatório Markdown salvo em     : {report_path}")
    print(f" [[dados]] Dashboard HTML interativo em   : {dashboard_path}")
    print("=" * 80)


if __name__ == "__main__":
    main()
