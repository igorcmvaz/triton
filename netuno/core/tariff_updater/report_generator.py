"""
Módulo de Relatórios e Transparência do Processo de Atualização de Tarifas (Netuno 5).
Gera relatórios executivos em Markdown e visualização formatada no console.
"""

from __future__ import annotations

import os
import datetime as dt
from pathlib import Path
from typing import Dict, Any, List


def generate_update_report(
    update_result: Dict[str, Any],
    output_path: Optional[Path] = None
) -> str:
    """
    Gera o relatório em Markdown com estatísticas completas, cidades atualizadas por webscraping,
    evidências primárias auditadas e a lista transparente de municípios que requerem conferência manual.
    """
    stats = update_result["stats"]
    manual_reviews = update_result["manual_review_needed"]
    dry_run = update_result.get("dry_run", False)
    
    total = stats.get("total_cities", 0)
    processed = stats.get("processed", 0)
    auto_ver = stats.get("overall_auto_or_verified", 0)
    manual_cnt = stats.get("overall_manual_needed", 0)
    
    pct_auto = (auto_ver / max(1, processed)) * 100.0
    pct_manual = (manual_cnt / max(1, processed)) * 100.0

    lines = [
        "# Relatório Executivo de Atualização Tarifária — Netuno 5",
        "",
        f"**Data de Execução:** {dt.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}  ",
        f"**Modo:** {'Simulação (Dry Run — Sem Gravação)' if dry_run else 'Gravação Oficial (Banco Compacto Atualizado)'}  ",
        f"**Universo Processado:** {processed} de {total} municípios  ",
        "",
        "---",
        "",
        "## 1. Resumo Executivo e Confiabilidade",
        "",
        "| Componente | Categoria | Quantidade | % do Universo |",
        "|---|---|---:|---:|",
        f"| **Energia Elétrica (ANEEL B1)** | Atualizado Automaticamente (Ato Vigente) | {stats.get('energy_auto_updated', 0)} | {(stats.get('energy_auto_updated', 0)/max(1, processed))*100:.1f}% |",
        f"| | Referência ANEEL mais Recente (Ato Expirado / Aguarda Homologação) | {stats.get('energy_expired_ref', 0)} | {(stats.get('energy_expired_ref', 0)/max(1, processed))*100:.1f}% |",
        f"| | Revisão Manual ANEEL | {stats.get('energy_manual', 0)} | {(stats.get('energy_manual', 0)/max(1, processed))*100:.1f}% |",
        f"| **Saneamento (Água/Esgoto)** | Scraped / Portais Concessionárias | {stats.get('sanitation_scraped', 0)} | {(stats.get('sanitation_scraped', 0)/max(1, processed))*100:.1f}% |",
        f"| | Evidência Primária Homologada e Auditada | {stats.get('sanitation_verified', 0)} | {(stats.get('sanitation_verified', 0)/max(1, processed))*100:.1f}% |",
        f"| | Requer Conferência Manual de Decreto Local | {stats.get('sanitation_manual', 0)} | {(stats.get('sanitation_manual', 0)/max(1, processed))*100:.1f}% |",
        f"| **STATUS GLOBAL** | **🟢 Confiabilidade Alta (Automático / Auditado)** | **{auto_ver}** | **{pct_auto:.1f}%** |",
        f"| | **🟡 Requer Conferência de Decreto Municipal** | **{manual_cnt}** | **{pct_manual:.1f}%** |",
        "",
        "---",
        "",
        "## 2. Metodologia de Atualização Transparente",
        "",
        "1. **Energia Elétrica**: As tarifas são extraídas diretamente do portal de dados abertos da **ANEEL**, considerando a classe residencial B1 convencional sem incidência de impostos estaduais (ICMS) e bandeiras tarifárias.",
        "2. **Saneamento Automatizado**: Grandes concessionárias estaduais (ex: SABESP, CASAN, EMBASA, SANEAGO, COPASA, SANEPAR, etc.) são atualizadas por webscraping e mapeamento canônico de resoluções de agências reguladoras (ARSESP, ARESC, AGERSA, AGEPAR, ARSAE-MG, etc.).",
        "3. **Auditoria de SAAEs e Autarquias Municipais**: Municípios com prestação direta ou autarquias isoladas que publicam apenas decretos em PDF no Diário Oficial são identificados formalmente para revisão periódica humana.",
        "",
        "---",
        "",
        "## 3. Municípios que Requerem Conferência Manual de Decretos",
        "",
        "Abaixo estão listados os municípios com prestadores locais cujos decretos ou tabelas devem ser validados manualmente:",
        "",
        "| UF | Município | Prestador | Motivo / Observação | URL da Fonte Oficial |",
        "|---|---|---|---|---|",
    ]

    for m in manual_reviews:
        uf = m.get("uf", "")
        city = m.get("municipio", "")
        prest = m.get("prestador", "")
        motivo = m.get("motivo_saneamento", "Decreto municipal PDF a verificar")
        url = m.get("fonte_url", "https://www.gov.br/cidades/pt-br/acesso-a-informacao/acoes-e-programas/saneamento/sinisa")
        lines.append(f"| {uf} | {city} | {prest} | {motivo} | [{prest}]({url}) |")

    lines.extend([
        "",
        "---",
        "",
        "## 4. Próximos Passos Recomendados",
        "",
        "- Para atualizar um município específico manualmente, edite diretamente o diálogo de tarifas na interface do Netuno ou utilize a ferramenta de inspeção.",
        "- Caso novos atos da ANEEL sejam publicados, basta rodar novamente `python scripts/update_all_tariffs.py` para sincronizar os dados.",
        ""
    ])

    report_text = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(report_text)
        print(f" [📋 Relatório] Relatório detalhado exportado para: {output_path}")

    return report_text
