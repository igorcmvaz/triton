"""
Gerador do Dashboard Visual e Interativo de Tarifas do Netuno 5 (Tema Claro / Normal).
Inclui modal com gráfico dinâmico das faixas, curva de fatura, simulação de custos em tempo real
e discriminação clara da tarifa de disponibilidade vs franquia de consumo mínimo.
"""

from __future__ import annotations

import json
import datetime as dt
from pathlib import Path
from typing import Dict, Any, List, Optional


def generate_interactive_dashboard(
    cities_dict: Dict[str, Any],
    change_registry: Dict[str, Any],
    output_path: Optional[Path] = None
) -> str:
    """
    Compila os dados de todas as 652 cidades e do registro de detecção de mudanças
    em um dashboard HTML moderno, limpo, responsivo e interativo (Tema Claro / Padrão).
    """
    now_str = dt.datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    monitored_urls = change_registry.get("monitored_urls", {})

    records = []
    total_cities = len(cities_dict)
    count_auto = 0
    count_manual = 0
    count_changed = 0

    for key, c in cities_dict.items():
        url = c.get("fonte_url", "")
        url_info = monitored_urls.get(url, {})
        url_status = url_info.get("status", "UNCHANGED")
        requires_manual = c.get("status_global") == "MANUAL_REVIEW_NEEDED" or url_info.get("requires_manual_action", False)
        
        if requires_manual:
            count_manual += 1
        else:
            count_auto += 1

        if "CHANGED" in url_status:
            count_changed += 1

        faixas = c.get("faixas", [])
        faixa_ini_str = "R$ 0,00"
        for inf, sup, rate, t_tipo in faixas:
            if t_tipo == 2:
                faixa_ini_str = f"PB R$ {rate:.2f}/m³ × Cⁿ"
                break
            if t_tipo == 1:
                faixa_ini_str = f"R$ {rate:.2f}/m³"
                break
            elif t_tipo == -1:
                faixa_ini_str = f"R$ {rate:.2f} (mín)"

        # Determina a modalidade da disponibilidade
        tarifa_fixa = float(c.get("tarifa_fixa_mensal", 0.0) or 0.0)
        tem_minima = any(t[3] == -1 for t in faixas)
        
        if any(t[3] == 2 for t in faixas):
            disp_tipo = "Fórmula Exponencial (PB × Cⁿ)"
            disp_desc = f"Serviço básico de R$ {tarifa_fixa:.2f}/mês mais o preço-base elevado ao expoente da tabela exponencial."
        elif tarifa_fixa > 0 and tem_minima:
            disp_tipo = "Franquia / Consumo Mínimo"
            disp_desc = f"Cobrança mínima de R$ {tarifa_fixa:.2f}/mês cobrindo a faixa inicial."
        elif tarifa_fixa > 0:
            disp_tipo = "Custo Fixo de Disponibilidade"
            disp_desc = f"Parcela fixa de R$ {tarifa_fixa:.2f}/mês adicionada ao consumo medido."
        else:
            disp_tipo = "Sem Parcela Fixa"
            disp_desc = "Cobrança estritamente proporcional/progressiva por m³ consumido."

        rec = {
            "uf": c.get("uf", ""),
            "municipio": c.get("municipio", ""),
            "regiao": c.get("regiao", ""),
            "prestador": c.get("prestador_saneamento", ""),
            "agencia": c.get("agencia_reguladora", ""),
            "tarifa_fixa": tarifa_fixa,
            "disp_tipo": disp_tipo,
            "disp_desc": disp_desc,
            "esgoto_pct": float(c.get("esgoto_pct", 80.0) or 80.0),
            "faixa_inicial": faixa_ini_str,
            "faixas": faixas,
            "distribuidora": c.get("distribuidora_energia", ""),
            "energia_kwh": float(c.get("energia_r_kwh", 0.0) or 0.0),
            "energia_ato": c.get("energia_ato", "Ato Homologatório ANEEL"),
            "fonte_url": url,
            "url_status": url_status,
            "hash_sha256": url_info.get("content_sha256", "")[:10] if url_info.get("content_sha256") else "N/A",
            "last_checked": url_info.get("last_checked", now_str),
            "requires_manual": requires_manual,
            "status_desc": url_info.get("status_desc", c.get("status_desc_sanitation", "Dados auditados e conciliados.")),
            "status_global": c.get("status_global", "AUTO_OR_VERIFIED")
        }
        records.append(rec)

    records_json = json.dumps(records, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Dashboard de Monitoramento de Tarifas e Scrapers — Netuno 5</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg-base: #f8fafc;
      --bg-surface: #ffffff;
      --bg-card: #ffffff;
      --border-color: #e2e8f0;
      --border-hover: #0284c7;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --primary: #0284c7;
      --primary-light: #e0f2fe;
      --success: #059669;
      --success-light: #ecfdf5;
      --warning: #d97706;
      --warning-light: #fffbeb;
      --danger: #dc2626;
      --danger-light: #fef2f2;
      --purple: #7c3aed;
      --purple-light: #f5f3ff;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      background-color: var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      padding: 24px;
      line-height: 1.5;
    }}

    .container {{
      max-width: 1560px;
      margin: 0 auto;
    }}

    /* HEADER */
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 24px 32px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      margin-bottom: 20px;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    .header-title {{
      display: flex;
      align-items: center;
      gap: 16px;
    }}

    .logo-badge {{
      background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
      color: white;
      font-weight: 800;
      font-size: 20px;
      padding: 10px 16px;
      border-radius: 12px;
      box-shadow: 0 4px 12px rgba(2, 132, 199, 0.25);
    }}

    .header-text h1 {{
      font-size: 22px;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }}

    .header-text p {{
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .header-meta {{
      display: flex;
      gap: 12px;
      align-items: center;
    }}

    .refresh-badge {{
      background: var(--success-light);
      border: 1px solid #a7f3d0;
      color: var(--success);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .pulse {{
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 6px var(--success);
      animation: pulseAnim 2s infinite;
    }}

    @keyframes pulseAnim {{
      0% {{ opacity: 0.4; }}
      50% {{ opacity: 1; }}
      100% {{ opacity: 0.4; }}
    }}

    /* BANNER DE CONTATO */
    .contact-banner {{
      background: #f0f9ff;
      border: 1px solid #bae6fd;
      border-radius: 12px;
      padding: 12px 20px;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13px;
      color: #0369a1;
      box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    }}

    /* KPIS */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 16px;
      margin-bottom: 24px;
    }}

    .kpi-card {{
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 20px 24px;
      transition: all 0.2s ease;
      position: relative;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
    }}

    .kpi-card:hover {{
      border-color: var(--border-hover);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
      transform: translateY(-2px);
    }}

    .kpi-title {{
      font-size: 12px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .kpi-val {{
      font-size: 32px;
      font-weight: 800;
      margin: 8px 0 4px 0;
      color: var(--text-main);
      letter-spacing: -0.03em;
    }}

    .kpi-sub {{
      font-size: 12px;
      color: var(--text-muted);
    }}

    .kpi-card::before {{
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 5px;
      height: 100%;
    }}

    .kpi-card.blue::before {{ background: var(--primary); }}
    .kpi-card.green::before {{ background: var(--success); }}
    .kpi-card.amber::before {{ background: var(--warning); }}
    .kpi-card.purple::before {{ background: var(--purple); }}

    /* CONTROLS & FILTERS */
    .controls {{
      display: flex;
      flex-wrap: wrap;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
      margin-bottom: 20px;
      background: var(--bg-surface);
      padding: 16px 20px;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }}

    .search-box {{
      position: relative;
      flex: 1;
      min-width: 280px;
    }}

    .search-box input {{
      width: 100%;
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: var(--text-main);
      padding: 10px 16px 10px 40px;
      border-radius: 8px;
      font-size: 14px;
      outline: none;
      transition: all 0.2s;
    }}

    .search-box input:focus {{
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.15);
    }}

    .search-icon {{
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
    }}

    .filter-tabs {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
    }}

    .tab-btn {{
      background: #f1f5f9;
      border: 1px solid #e2e8f0;
      color: #334155;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }}

    .tab-btn:hover {{
      background: #e2e8f0;
      color: var(--text-main);
    }}

    .tab-btn.active {{
      background: var(--primary);
      color: #ffffff;
      font-weight: 700;
      border-color: var(--primary);
      box-shadow: 0 2px 8px rgba(2, 132, 199, 0.25);
    }}

    .select-uf {{
      background: #ffffff;
      border: 1px solid #cbd5e1;
      color: var(--text-main);
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 500;
      outline: none;
      cursor: pointer;
    }}

    /* TABLE */
    .table-container {{
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 13px;
    }}

    th {{
      background: #f8fafc;
      color: #475569;
      font-weight: 700;
      text-transform: uppercase;
      font-size: 11px;
      letter-spacing: 0.05em;
      padding: 14px 16px;
      border-bottom: 2px solid var(--border-color);
      position: sticky;
      top: 0;
    }}

    td {{
      padding: 13px 16px;
      border-bottom: 1px solid var(--border-color);
      color: var(--text-main);
      vertical-align: middle;
    }}

    tr:hover td {{
      background: #f1f5f9;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 8px;
      border-radius: 6px;
      font-size: 11px;
      font-weight: 600;
    }}

    .badge.green {{
      background: var(--success-light);
      color: #065f46;
      border: 1px solid #a7f3d0;
    }}

    .badge.amber {{
      background: var(--warning-light);
      color: #92400e;
      border: 1px solid #fde68a;
    }}

    .badge.blue {{
      background: var(--primary-light);
      color: #0369a1;
      border: 1px solid #bae6fd;
    }}

    .badge.red {{
      background: var(--danger-light);
      color: #991b1b;
      border: 1px solid #fecaca;
    }}

    .btn-chart {{
      background-color: #0284c7;
      color: white;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      transition: all 0.2s;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.2);
    }}

    .btn-chart:hover {{
      background-color: #0369a1;
      transform: translateY(-1px);
    }}

    .link-btn {{
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
    }}

    .link-btn:hover {{
      color: #0369a1;
      text-decoration: underline;
    }}

    .uf-tag {{
      display: inline-block;
      font-weight: 700;
      color: var(--primary);
      background: var(--primary-light);
      padding: 3px 7px;
      border-radius: 4px;
      font-size: 11px;
      border: 1px solid #bae6fd;
    }}

    .disp-tag {{
      display: block;
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }}

    .pagination {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 20px;
      font-size: 13px;
      color: var(--text-muted);
      background: #ffffff;
      border-top: 1px solid var(--border-color);
    }}

    .page-btns {{
      display: flex;
      gap: 6px;
    }}

    .page-btn {{
      background: #f1f5f9;
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 6px 14px;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      font-weight: 600;
      transition: all 0.2s;
    }}

    .page-btn:hover:not(:disabled) {{
      background: #e2e8f0;
    }}

    .page-btn:disabled {{
      opacity: 0.4;
      cursor: not-allowed;
    }}

    /* MODAL DE GRÁFICO E SIMULAÇÃO */
    .modal-backdrop {{
      display: none;
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }}

    .modal-backdrop.active {{
      display: flex;
    }}

    .modal-content {{
      background: #ffffff;
      border-radius: 16px;
      width: 100%;
      max-width: 1050px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
      border: 1px solid var(--border-color);
      display: flex;
      flex-direction: column;
      animation: modalFadeIn 0.25s ease;
    }}

    @keyframes modalFadeIn {{
      from {{ opacity: 0; transform: scale(0.96); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}

    .modal-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-color);
      background: #f8fafc;
      border-top-left-radius: 16px;
      border-top-right-radius: 16px;
    }}

    .modal-header h2 {{
      font-size: 18px;
      font-weight: 700;
      color: var(--text-main);
    }}

    .btn-close {{
      background: transparent;
      border: none;
      font-size: 24px;
      font-weight: bold;
      color: var(--text-muted);
      cursor: pointer;
      line-height: 1;
      padding: 4px 8px;
      border-radius: 6px;
    }}

    .btn-close:hover {{
      color: var(--danger);
      background: #f1f5f9;
    }}

    .modal-body {{
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }}

    .modal-grid {{
      display: grid;
      grid-template-columns: 1fr 1.15fr;
      gap: 24px;
    }}

    @media (max-width: 900px) {{
      .modal-grid {{
        grid-template-columns: 1fr;
      }}
    }}

    .chart-box {{
      background: #ffffff;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }}

    .chart-box h3 {{
      font-size: 14px;
      font-weight: 700;
      color: #334155;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-between;
    }}

    canvas {{
      width: 100%;
      height: 240px;
    }}

    .sim-panel {{
      background: #f8fafc;
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }}

    .sim-panel h3 {{
      font-size: 15px;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    .sim-input-row {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}

    .sim-slider {{
      flex: 1;
      cursor: pointer;
    }}

    .sim-num-input {{
      width: 90px;
      padding: 8px 12px;
      border: 1px solid #cbd5e1;
      border-radius: 6px;
      font-size: 14px;
      font-weight: bold;
      color: var(--primary);
      text-align: center;
      outline: none;
    }}

    .breakdown-card {{
      background: #ffffff;
      border: 1px solid #bae6fd;
      border-radius: 10px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 13px;
    }}

    .breakdown-row {{
      display: flex;
      justify-content: space-between;
      color: #475569;
    }}

    .breakdown-row.total {{
      border-top: 2px solid #e2e8f0;
      padding-top: 10px;
      margin-top: 4px;
      font-size: 16px;
      font-weight: 800;
      color: #0284c7;
    }}

    .disp-callout {{
      background: #fffbeb;
      border: 1px solid #fde68a;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 12px;
      color: #92400e;
      line-height: 1.4;
    }}
  </style>
</head>
<body>
  <div class="container">
    
    <!-- HEADER -->
    <header class="header">
      <div class="header-title">
        <div class="logo-badge">N5</div>
        <div class="header-text">
          <h1>Monitor de Tarifas & Integridade de Scrapers</h1>
          <p>Catálogo Nacional de Saneamento e Energia — 652 Municípios (27 UFs)</p>
        </div>
      </div>
      <div class="header-meta">
        <div class="refresh-badge">
          <div class="pulse"></div>
          <span>Atualizado: {now_str}</span>
        </div>
      </div>
    </header>

    <!-- BANNER DE CONTATO -->
    <div class="contact-banner">
      <span style="font-size:18px;">📌</span>
      <span><strong>Canal de Transparência & Atualizações:</strong> Caso algum valor tarifário esteja incorreto ou defasado em relação à sua fatura municipal recente, favor contatar pelo e-mail: <a href="mailto:igorcmvaz@gmail.com?subject=Netuno%205%20-%20Ajuste%20de%20Tarifa" style="color:#0284c7; font-weight:bold; text-decoration:underline;">igorcmvaz@gmail.com</a></span>
    </div>

    <!-- KPIS -->
    <div class="kpi-grid">
      <div class="kpi-card blue">
        <div class="kpi-title">Universo Monitorado</div>
        <div class="kpi-val">{total_cities}</div>
        <div class="kpi-sub">Municípios em 27 Estados</div>
      </div>

      <div class="kpi-card green">
        <div class="kpi-title">Confiabilidade Alta</div>
        <div class="kpi-val">{count_auto}</div>
        <div class="kpi-sub">{(count_auto/max(1, total_cities))*100:.1f}% do catálogo conciliado</div>
      </div>

      <div class="kpi-card amber">
        <div class="kpi-title">Revisão Manual / Decretos</div>
        <div class="kpi-val">{count_manual}</div>
        <div class="kpi-sub">{(count_manual/max(1, total_cities))*100:.1f}% autarquias / decretos PDF</div>
      </div>

      <div class="kpi-card purple">
        <div class="kpi-title">Energia Elétrica (ANEEL)</div>
        <div class="kpi-val">100%</div>
        <div class="kpi-sub">116 distribuidoras cadastradas</div>
      </div>
    </div>

    <!-- CONTROLS -->
    <div class="controls">
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" placeholder="Buscar por município, UF, concessionária ou agência..." oninput="onSearchChange()">
      </div>

      <div class="filter-tabs">
        <button class="tab-btn active" onclick="setFilter('all', this)">Todas ({total_cities})</button>
        <button class="tab-btn" onclick="setFilter('verified', this)">🟢 Alta Confiabilidade ({count_auto})</button>
        <button class="tab-btn" onclick="setFilter('manual', this)">🟡 Requer Revisão ({count_manual})</button>
        
        <select class="select-uf" id="categoryFilter" onchange="onCategoryChange()" style="font-weight: bold; color: #0284c7; background-color: #f0f9ff; border-color: #bae6fd;">
          <option value="residencial">🏠 Residencial Normal (1.0x)</option>
          <option value="comercial">💼 Comercial / Serviços (~1.85x)</option>
          <option value="industrial">🏭 Industrial (~2.30x)</option>
          <option value="publica">🏛️ Pública / Institucional (~1.65x)</option>
          <option value="social">🤝 Social / Baixa Renda (0.50x)</option>
        </select>

        <select class="select-uf" id="ufFilter" onchange="onUfChange()">
          <option value="">Todas as UFs (27)</option>
        </select>
      </div>
    </div>

    <!-- TABLE -->
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>UF</th>
            <th>Município</th>
            <th>Prestador Saneamento</th>
            <th>Tarifa Fixa / Disponibilidade</th>
            <th>1ª Faixa</th>
            <th>Esgoto</th>
            <th>Energia ANEEL</th>
            <th>Status / Integridade</th>
            <th>Ações & Análise</th>
          </tr>
        </thead>
        <tbody id="tableBody">
          <!-- Linhas geradas via JavaScript -->
        </tbody>
      </table>

      <div class="pagination">
        <span id="pageInfo">Exibindo 1 a 50 de 652 registros</span>
        <div class="page-btns">
          <button class="page-btn" id="btnPrev" onclick="prevPage()">Anterior</button>
          <button class="page-btn" id="btnNext" onclick="nextPage()">Próximo</button>
        </div>
      </div>
    </div>

  </div>

  <!-- MODAL DE GRÁFICO E SIMULAÇÃO -->
  <div class="modal-backdrop" id="modalBackdrop" onclick="closeModalOnBackdrop(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <div class="modal-header">
        <div>
          <h2 id="modalCityTitle">📊 Estrutura Tarifária & Simulação</h2>
          <p style="font-size:12px; color:var(--text-muted);" id="modalCitySubtitle">Prestador: - | Agência: -</p>
        </div>
        <button class="btn-close" onclick="closeModal()">×</button>
      </div>
      
      <div class="modal-body">
        
        <!-- CALLOUT DE DISPONIBILIDADE -->
        <div class="disp-callout" id="modalDispCallout">
          🏷️ <strong>Tarifa de Disponibilidade:</strong> -
        </div>

        <div class="modal-grid">
          
          <!-- COLUNA ESQUERDA: GRÁFICOS -->
          <div class="chart-box">
            <h3>📈 Curva de Degraus (Tarifa Marginal R$/m³)</h3>
            <canvas id="stepChart" width="450" height="220"></canvas>
            
            <h3 style="margin-top:16px;">💰 Curva de Custo Total da Fatura (R$)</h3>
            <canvas id="billCurveChart" width="450" height="200"></canvas>
          </div>

          <!-- COLUNA DIREITA: SIMULADOR DE FATURA -->
          <div class="sim-panel">
            <h3>🧮 Simulador de Consumo Mensal</h3>
            <p style="font-size:12.5px; color:#64748b;">
              Ajuste o volume para calcular a fatura exata com parcelas de água, esgoto e disponibilidade:
            </p>

            <div class="sim-input-row">
              <input type="range" class="sim-slider" id="simSlider" min="0" max="60" step="1" value="15" oninput="onSimVolumeChange(this.value)">
              <input type="number" class="sim-num-input" id="simNumber" min="0" max="500" value="15" oninput="onSimVolumeChange(this.value)">
              <span style="font-weight:bold; font-size:13px; color:#475569;">m³/mês</span>
            </div>

            <!-- DEMONSTRATIVO DE FATURA -->
            <div class="breakdown-card">
              <div class="breakdown-row">
                <span>🏷️ Parcela Fixa / Disponibilidade:</span>
                <strong id="bkFixed">R$ 0,00</strong>
              </div>
              <div class="breakdown-row">
                <span>💧 Consumo Medido de Água:</span>
                <strong id="bkWater">R$ 0,00</strong>
              </div>
              <div class="breakdown-row">
                <span id="bkSewageLabel">🚽 Esgoto (80%):</span>
                <strong id="bkSewage">R$ 0,00</strong>
              </div>
              <div class="breakdown-row total">
                <span>TOTAL DA FATURA:</span>
                <span id="bkTotal">R$ 0,00 / mês</span>
              </div>
              <div class="breakdown-row" style="margin-top:4px; font-size:11.5px; color:#0369a1;">
                <span>⚡ Tarifa Média Efetiva:</span>
                <strong id="bkEffective">R$ 0,00 / m³</strong>
              </div>
            </div>

            <!-- TABELA DE FAIXAS -->
            <div style="background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:12px; font-size:12px;">
              <strong style="color:#334155; display:block; margin-bottom:6px;">Matriz de Faixas da Concessionária:</strong>
              <div id="modalTiersTable" style="display:flex; flex-direction:column; gap:4px;"></div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:8px;">
              <a class="link-btn" id="modalFonteLink" href="#" target="_blank" rel="noopener noreferrer">🌐 Acessar Decreto / Resolução Oficial ↗</a>
              <button class="page-btn" onclick="closeModal()">Fechar</button>
            </div>

          </div>

        </div>

      </div>
    </div>
  </div>

  <script>
    const ALL_RECORDS = {records_json};
    let currentFiltered = [...ALL_RECORDS];
    let currentTab = 'all';
    let currentUf = '';
    let currentPage = 1;
    const PAGE_SIZE = 50;

    const CATEGORY_MULTS = {{
      'residencial': {{ agua: 1.0, fixo: 1.0, energia: 1.0 }},
      'comercial': {{ agua: 1.85, fixo: 1.75, energia: 1.10 }},
      'industrial': {{ agua: 2.30, fixo: 2.20, energia: 1.15 }},
      'publica': {{ agua: 1.65, fixo: 1.50, energia: 0.95 }},
      'social': {{ agua: 0.50, fixo: 0.50, energia: 0.60 }}
    }};
    let currentCategory = 'residencial';
    let activeModalCity = null;

    // Popula dropdown de UFs
    const ufs = Array.from(new Set(ALL_RECORDS.map(r => r.uf))).sort();
    const ufSelect = document.getElementById('ufFilter');
    ufs.forEach(uf => {{
      const opt = document.createElement('option');
      opt.value = uf;
      opt.textContent = uf;
      ufSelect.appendChild(opt);
    }});

    function renderTable() {{
      const tbody = document.getElementById('tableBody');
      tbody.innerHTML = '';

      const mults = CATEGORY_MULTS[currentCategory] || CATEGORY_MULTS['residencial'];
      const start = (currentPage - 1) * PAGE_SIZE;
      const pageData = currentFiltered.slice(start, start + PAGE_SIZE);

      if (pageData.length === 0) {{
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center; padding: 32px; color: var(--text-muted);">Nenhum município encontrado com os filtros selecionados.</td></tr>';
        document.getElementById('pageInfo').textContent = '0 registros encontrados';
        return;
      }}

      pageData.forEach(r => {{
        const tr = document.createElement('tr');
        
        let statusBadge = '<span class="badge green">🟢 Íntegro</span>';
        if (r.requires_manual) {{
          statusBadge = '<span class="badge amber">🟡 Revisão</span>';
        }}
        if (r.url_status === 'PAGE_CHANGED_PARSED') {{
          statusBadge = '<span class="badge blue">🔵 Atualizado</span>';
        }} else if (r.url_status === 'PAGE_CHANGED_MANUAL_REVIEW_REQUIRED') {{
          statusBadge = '<span class="badge amber">⚠️ Mudou (Ajuste)</span>';
        }}

        const tFixa = (r.tarifa_fixa * mults.fixo);
        const tEne = (r.energia_kwh * mults.energia);

        let faixaStr = r.faixa_inicial;
        if (currentCategory !== 'residencial' && r.faixa_inicial.includes('R$')) {{
          try {{
            const numPart = parseFloat(r.faixa_inicial.replace('R$', '').replace('/m³', '').replace('(mín)', '').replace(',', '.').trim());
            if (!isNaN(numPart)) {{
              const adjNum = numPart * mults.agua;
              faixaStr = r.faixa_inicial.includes('(mín)') ? `R$ ${{adjNum.toFixed(2)}} (mín)` : `R$ ${{adjNum.toFixed(2)}}/m³`;
            }}
          }} catch (e) {{}}
        }}

        tr.innerHTML = `
          <td><span class="uf-tag">${{r.uf}}</span></td>
          <td><strong>${{r.municipio}}</strong><br><span style="font-size:11px;color:var(--text-muted);">${{r.regiao}}</span></td>
          <td>${{r.prestador}}</td>
          <td>
            <strong>R$ ${{tFixa.toFixed(2)}}</strong>
            <span class="disp-tag">${{r.disp_tipo}}</span>
          </td>
          <td>${{faixaStr}}</td>
          <td>${{r.esgoto_pct.toFixed(0)}}%</td>
          <td>R$ ${{tEne.toFixed(4)}}/kWh<br><span style="font-size:10px;color:var(--text-muted);">${{r.distribuidora}}</span></td>
          <td>${{statusBadge}}</td>
          <td>
            <div style="display:flex; flex-direction:column; gap:6px;">
              <button class="btn-chart" onclick="openCityModal('${{r.uf}}', '${{r.municipio.replace(/'/g, "\\\\\\'")}}')">📊 Ver Gráfico & Simulação</button>
              <a class="link-btn" href="${{r.fonte_url}}" target="_blank" rel="noopener noreferrer">Fonte Oficial ↗</a>
            </div>
          </td>
        `;
        tbody.appendChild(tr);
      }});

      const end = Math.min(start + PAGE_SIZE, currentFiltered.length);
      document.getElementById('pageInfo').textContent = `Exibindo ${{start + 1}} a ${{end}} de ${{currentFiltered.length}} registros`;
      document.getElementById('btnPrev').disabled = (currentPage === 1);
      document.getElementById('btnNext').disabled = (end >= currentFiltered.length);
    }}

    function onCategoryChange() {{
      currentCategory = document.getElementById('categoryFilter').value;
      renderTable();
      if (activeModalCity) {{
        updateModalCalculations();
      }}
    }}

    function cleanStr(str) {{
      if (!str) return '';
      return String(str).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
    }}

    function applyFilters() {{
      const query = cleanStr(document.getElementById('searchInput').value);
      
      currentFiltered = ALL_RECORDS.filter(r => {{
        if (currentTab === 'verified' && r.requires_manual) return false;
        if (currentTab === 'manual' && !r.requires_manual) return false;
        if (currentUf && r.uf !== currentUf) return false;

        if (query) {{
          const match = cleanStr(r.municipio).includes(query) ||
                        cleanStr(r.uf).includes(query) ||
                        cleanStr(r.prestador).includes(query) ||
                        cleanStr(r.agencia).includes(query) ||
                        cleanStr(r.distribuidora).includes(query);
          if (!match) return false;
        }}
        return true;
      }});

      currentPage = 1;
      renderTable();
    }}

    function onSearchChange() {{
      applyFilters();
    }}

    function onUfChange() {{
      currentUf = document.getElementById('ufFilter').value;
      applyFilters();
    }}

    function setFilter(tab, btn) {{
      currentTab = tab;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      applyFilters();
    }}

    function prevPage() {{
      if (currentPage > 1) {{
        currentPage--;
        renderTable();
      }}
    }}

    function nextPage() {{
      if ((currentPage * PAGE_SIZE) < currentFiltered.length) {{
        currentPage++;
        renderTable();
      }}
    }}

    // ==============================================================================================
    // MODAL DE ANÁLISE, GRÁFICO E SIMULAÇÃO
    // ==============================================================================================
    function openCityModal(uf, city) {{
      const rec = ALL_RECORDS.find(r => r.uf === uf && r.municipio === city);
      if (!rec) return;
      
      activeModalCity = rec;

      document.getElementById('modalCityTitle').textContent = `📊 ${{rec.municipio}} (${{rec.uf}}) — Estrutura Tarifária & Simulação`;
      document.getElementById('modalCitySubtitle').textContent = `Prestador: ${{rec.prestador}} | Regulação: ${{rec.agencia || 'Órgão Municipal'}} | Região: ${{rec.regiao}}`;
      document.getElementById('modalFonteLink').href = rec.fonte_url;

      const mults = CATEGORY_MULTS[currentCategory] || CATEGORY_MULTS['residencial'];
      const tFixa = rec.tarifa_fixa * mults.fixo;

      document.getElementById('modalDispCallout').innerHTML = `
        🏷️ <strong>${{rec.disp_tipo}}:</strong> R$ ${{tFixa.toFixed(2)}}/mês. ${{rec.disp_desc}}
      `;

      // Renderiza tabela de faixas
      const tblDiv = document.getElementById('modalTiersTable');
      tblDiv.innerHTML = '';
      rec.faixas.forEach((f, idx) => {{
        const inf = f[0];
        const sup = f[1] < 99999 ? `${{f[1]}} m³` : '> 99999 m³';
        const rate = (f[2] * mults.agua).toFixed(4);
        const tipo = f[3] === -1 ? 'Tarifa Mínima Fixa' : 'Marginal Progressiva';
        
        const row = document.createElement('div');
        row.style.cssText = 'display:flex; justify-content:space-between; padding:3px 0; border-bottom:1px solid #f1f5f9;';
        row.innerHTML = `<span>Faixa ${{idx+1}}: <strong>${{inf}} a ${{sup}}</strong></span> <span>R$ ${{rate}}/m³ <em style="color:#64748b;">(${{tipo}})</em></span>`;
        tblDiv.appendChild(row);
      }});

      document.getElementById('modalBackdrop').classList.add('active');
      updateModalCalculations();
    }}

    function closeModal() {{
      document.getElementById('modalBackdrop').classList.remove('active');
      activeModalCity = null;
    }}

    function closeModalOnBackdrop(e) {{
      if (e.target.id === 'modalBackdrop') {{
        closeModal();
      }}
    }}

    document.addEventListener('keydown', (e) => {{
      if (e.key === 'Escape') closeModal();
    }});

    function onSimVolumeChange(val) {{
      const num = parseFloat(val) || 0;
      document.getElementById('simSlider').value = num;
      document.getElementById('simNumber').value = num;
      updateModalCalculations();
    }}

    function calculateBill(rec, vol, category) {{
      const mults = CATEGORY_MULTS[category] || CATEGORY_MULTS['residencial'];
      const tFixa = (rec.tarifa_fixa * mults.fixo);
      const faixas = rec.faixas || [];
      const esgPct = rec.esgoto_pct || 80.0;

      let fixedWater = 0.0;
      let meteredWater = 0.0;

      faixas.forEach(f => {{
        const inf = f[0];
        const sup = f[1];
        const rate = f[2] * mults.agua;
        const tTipo = f[3];

        if (tTipo === -1) {{
          fixedWater += rate;
        }} else if (tTipo === 1) {{
          if (vol > inf) {{
            const volInTier = Math.min(vol, sup) - inf;
            if (volInTier > 0) meteredWater += volInTier * rate;
          }}
        }}
      }});

      if (tFixa > 0 && fixedWater === 0.0) {{
        fixedWater = tFixa;
      }}

      const aguaTotal = fixedWater + meteredWater;
      const esgotoVal = aguaTotal * (esgPct / 100.0);
      const totalVal = aguaTotal + esgotoVal;
      const effectiveRate = vol > 0 ? (totalVal / vol) : 0.0;

      return {{
        valorFixo: fixedWater,
        aguaVal: meteredWater,
        esgotoVal,
        totalVal,
        effectiveRate
      }};
    }}

    function updateModalCalculations() {{
      if (!activeModalCity) return;
      const vol = parseFloat(document.getElementById('simNumber').value) || 0;
      const res = calculateBill(activeModalCity, vol, currentCategory);

      document.getElementById('bkFixed').textContent = `R$ ${{res.valorFixo.toFixed(2)}}`;
      document.getElementById('bkWater').textContent = `R$ ${{res.aguaVal.toFixed(2)}}`;
      document.getElementById('bkSewageLabel').textContent = `🚽 Esgoto (${{activeModalCity.esgoto_pct.toFixed(0)}}%):`;
      document.getElementById('bkSewage').textContent = `R$ ${{res.esgotoVal.toFixed(2)}}`;
      document.getElementById('bkTotal').textContent = `R$ ${{res.totalVal.toFixed(2)}} / mês`;
      document.getElementById('bkEffective').textContent = `R$ ${{res.effectiveRate.toFixed(2)}} / m³`;

      renderStepChart(activeModalCity, vol);
      renderBillCurveChart(activeModalCity, vol);
    }}

    function renderStepChart(rec, selectedVol) {{
      const canvas = document.getElementById('stepChart');
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const mults = CATEGORY_MULTS[currentCategory] || CATEGORY_MULTS['residencial'];

      ctx.clearRect(0, 0, w, h);

      // Faixas até 40m³
      const maxVol = 40;
      const rates = [];
      rec.faixas.forEach(f => {{
        if (f[3] === 1) {{
          rates.push(f[2] * mults.agua);
        }}
      }});
      const maxRate = Math.max(...rates, 15) * 1.25;

      const padding = {{ top: 20, right: 20, bottom: 35, left: 45 }};
      const plotW = w - padding.left - padding.right;
      const plotH = h - padding.top - padding.bottom;

      // Eixos
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding.left, padding.top);
      ctx.lineTo(padding.left, h - padding.bottom);
      ctx.lineTo(w - padding.right, h - padding.bottom);
      ctx.stroke();

      // Linhas de Grade e Labels Y
      ctx.fillStyle = '#64748b';
      ctx.font = '10px Inter';
      ctx.textAlign = 'right';
      for (let i = 0; i <= 4; i++) {{
        const yVal = (maxRate / 4) * i;
        const yPos = h - padding.bottom - (plotH / 4) * i;
        ctx.fillText(`R$ ${{yVal.toFixed(0)}}`, padding.left - 6, yPos + 3);
        
        if (i > 0) {{
          ctx.strokeStyle = '#f1f5f9';
          ctx.beginPath();
          ctx.moveTo(padding.left, yPos);
          ctx.lineTo(w - padding.right, yPos);
          ctx.stroke();
        }}
      }}

      // Labels X
      ctx.textAlign = 'center';
      for (let v = 0; v <= maxVol; v += 10) {{
        const xPos = padding.left + (plotW / maxVol) * v;
        ctx.fillText(`${{v}} m³`, xPos, h - padding.bottom + 15);
      }}

      // Desenha Step-Curve
      ctx.strokeStyle = '#0284c7';
      ctx.lineWidth = 3;
      ctx.fillStyle = 'rgba(2, 132, 199, 0.12)';

      ctx.beginPath();
      let prevX = padding.left;
      let prevY = h - padding.bottom;

      rec.faixas.forEach((f, idx) => {{
        if (f[3] === 1) {{
          const inf = Math.min(maxVol, f[0]);
          const sup = Math.min(maxVol, f[1]);
          const rate = f[2] * mults.agua;
          
          const x1 = padding.left + (plotW / maxVol) * inf;
          const x2 = padding.left + (plotW / maxVol) * sup;
          const y = h - padding.bottom - (plotH / maxRate) * rate;

          if (idx === 0) {{
            ctx.moveTo(x1, y);
          }} else {{
            ctx.lineTo(x1, y);
          }}
          ctx.lineTo(x2, y);
        }}
      }});
      ctx.stroke();

      // Indicador do volume selecionado
      if (selectedVol >= 0 && selectedVol <= maxVol) {{
        const selX = padding.left + (plotW / maxVol) * selectedVol;
        ctx.strokeStyle = '#ef4444';
        ctx.setLineDash([4, 4]);
        ctx.beginPath();
        ctx.moveTo(selX, padding.top);
        ctx.lineTo(selX, h - padding.bottom);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(selX, h - padding.bottom, 5, 0, 2 * Math.PI);
        ctx.fill();
      }}
    }}

    function renderBillCurveChart(rec, selectedVol) {{
      const canvas = document.getElementById('billCurveChart');
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;

      ctx.clearRect(0, 0, w, h);

      const maxVol = 40;
      const bills = [];
      for (let v = 0; v <= maxVol; v += 2) {{
        bills.push(calculateBill(rec, v, currentCategory).totalVal);
      }}
      const maxBill = Math.max(...bills, 100) * 1.15;

      const padding = {{ top: 15, right: 20, bottom: 30, left: 55 }};
      const plotW = w - padding.left - padding.right;
      const plotH = h - padding.top - padding.bottom;

      // Eixos
      ctx.strokeStyle = '#cbd5e1';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(padding.left, padding.top);
      ctx.lineTo(padding.left, h - padding.bottom);
      ctx.lineTo(w - padding.right, h - padding.bottom);
      ctx.stroke();

      // Labels Y
      ctx.fillStyle = '#64748b';
      ctx.font = '10px Inter';
      ctx.textAlign = 'right';
      for (let i = 0; i <= 3; i++) {{
        const yVal = (maxBill / 3) * i;
        const yPos = h - padding.bottom - (plotH / 3) * i;
        ctx.fillText(`R$ ${{yVal.toFixed(0)}}`, padding.left - 6, yPos + 3);
        if (i > 0) {{
          ctx.strokeStyle = '#f1f5f9';
          ctx.beginPath();
          ctx.moveTo(padding.left, yPos);
          ctx.lineTo(w - padding.right, yPos);
          ctx.stroke();
        }}
      }}

      // Labels X
      ctx.textAlign = 'center';
      for (let v = 0; v <= maxVol; v += 10) {{
        const xPos = padding.left + (plotW / maxVol) * v;
        ctx.fillText(`${{v}} m³`, xPos, h - padding.bottom + 15);
      }}

      // Curva Total da Conta
      ctx.strokeStyle = '#10b981';
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (let v = 0; v <= maxVol; v++) {{
        const b = calculateBill(rec, v, currentCategory).totalVal;
        const x = padding.left + (plotW / maxVol) * v;
        const y = h - padding.bottom - (plotH / maxBill) * b;
        if (v === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      }}
      ctx.stroke();

      // Ponto no volume selecionado
      if (selectedVol >= 0 && selectedVol <= maxVol) {{
        const bSel = calculateBill(rec, selectedVol, currentCategory).totalVal;
        const selX = padding.left + (plotW / maxVol) * selectedVol;
        const selY = h - padding.bottom - (plotH / maxBill) * bSel;

        ctx.strokeStyle = '#ef4444';
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(selX, selY);
        ctx.lineTo(selX, h - padding.bottom);
        ctx.moveTo(padding.left, selY);
        ctx.lineTo(selX, selY);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#ef4444';
        ctx.beginPath();
        ctx.arc(selX, selY, 5, 0, 2 * Math.PI);
        ctx.fill();
      }}
    }}

    // Render inicial
    applyFilters();
  </script>
</body>
</html>
"""

    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f" [Dashboard] Dashboard HTML gerado com sucesso em: {output_path}")

    return html_content
