from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DETAIL = ROOT / "examples" / "DETALHAMENTO_COMPLETO_TRES_MODELOS.md"
VALIDATION = ROOT / "examples" / "ESTUDO_DE_CASO_TRES_MODELOS_REFERENCIA.md"
PARAMETERS = ROOT / "examples" / "PARAMETROS_DEPENDENTES_DO_VOLUME_RESERVATORIO.md"
ATLAS = ROOT / "triton" / "docs" / "fluxogramas_metodologicos.md"
ROADMAP = ROOT / "triton" / "docs" / "proximos_passos_decisao_robusta.md"
PORTABLE_DOCS = (
    ROOT / "README.md",
    PARAMETERS,
    DETAIL,
    VALIDATION,
    ROADMAP,
)


def _pt_number(raw: str) -> float:
    cleaned = (
        raw.strip()
        .replace("R$", "")
        .replace("%", "")
        .replace(".", "")
        .replace(",", ".")
    )
    return float(cleaned)


def test_complete_detail_preserves_diagram_and_all_comparison_layers():
    detail = DETAIL.read_text(encoding="utf-8")
    parameters = PARAMETERS.read_text(encoding="utf-8")

    assert "Documento gerado por `python scripts/generate_reference_case_studies.py`" in detail
    assert "```mermaid" in detail
    assert "Capacidade inferior V" in detail
    assert "```mermaid" in parameters

    assert detail.count("### Comparação direta das quatro decisões") == 3
    assert detail.count("### Varredura técnica completa") == 3
    assert detail.count("### Varredura econômica completa") == 3
    assert detail.count("### Varredura ambiental e multicritério completa") == 3
    assert "## 5. Cobertura e rastreabilidade" in detail


def test_methodology_atlas_covers_the_full_calculation_chain():
    atlas = ATLAS.read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    parameters = PARAMETERS.read_text(encoding="utf-8")

    mermaid_blocks = atlas.split("```mermaid")[1:]
    assert len(mermaid_blocks) == 11
    for block in mermaid_blocks:
        diagram, separator, _ = block.partition("```")
        assert separator
        assert diagram.strip().startswith("flowchart")

    required_topics = (
        "Chuva efetiva e captação",
        "Balanço hídrico YAS",
        "Dois reservatórios e ciclo de recalque",
        "Varredura de capacidades e ótimo técnico",
        "Modelo econômico-financeiro",
        "Cloração: cálculo implementado e limite sanitário",
        "ACV simplificada e fronteira ambiental",
        "TOPSIS e diagnóstico da concessão",
        "Verificação interna e rastreabilidade",
    )
    assert all(topic in atlas for topic in required_topics)
    assert "triton/docs/fluxogramas_metodologicos.md" in readme
    assert "../triton/docs/fluxogramas_metodologicos.md" in parameters


def test_robust_decision_roadmap_separates_current_features_from_future_work():
    roadmap = ROADMAP.read_text(encoding="utf-8")
    readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "proximos_passos_decisao_robusta.md" in readme
    assert "Monte Carlo comparativo" in roadmap
    assert "fronteira de Pareto" in roadmap
    assert "Minimax arrependimento" in roadmap
    assert "AssumptionRegistry" in roadmap
    assert "Recibo de decisão" in roadmap
    assert "A CLI atual amostra" in roadmap


def test_retired_triton_41_web_app_is_not_exposed():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    cli_source = (ROOT / "triton" / "cli.py").read_text(encoding="utf-8")

    assert not (ROOT / "triton" / "app").exists()
    assert "triton.cli serve" not in readme
    assert 'add_parser("serve"' not in cli_source
    assert "triton.app.server" not in cli_source


def test_manual_itemwise_and_cashflow_residuals_remain_numerically_closed():
    text = VALIDATION.read_text(encoding="utf-8")
    assert text.count("### 7. Comparação item a item: conta manual × sistema") == 3

    item_residuals = []
    cash_residuals = []
    mode = None
    item_rows_per_case = []
    current_item_rows = 0

    for line in text.splitlines():
        if line.startswith("### 7. Comparação item a item"):
            if current_item_rows:
                item_rows_per_case.append(current_item_rows)
            current_item_rows = 0
            mode = "item"
            continue
        if line.startswith("#### TOPSIS") or line.startswith("### 6."):
            if mode == "item":
                item_rows_per_case.append(current_item_rows)
                current_item_rows = 0
            mode = None
        if line.startswith("#### Fluxo de caixa"):
            mode = "cash_nominal"
            continue
        if line.startswith("##### Fluxos nominais"):
            mode = "cash_nominal"
            continue
        if line.startswith("##### Desconto e acumulado"):
            mode = "cash_discount"
            continue
        if (
            not line.startswith("|")
            or line.startswith("| ---")
            or line.startswith("| Item")
            or line.startswith("| Ano")
        ):
            continue

        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if mode == "item" and len(cells) >= 5:
            current_item_rows += 1
            item_residuals.append(_pt_number(cells[-1]))
        elif mode == "cash_nominal" and len(cells) == 9:
            cash_residuals.append(_pt_number(cells[-1]))
        elif mode == "cash_discount" and len(cells) == 6:
            cash_residuals.extend((_pt_number(cells[3]), _pt_number(cells[5])))

    if current_item_rows:
        item_rows_per_case.append(current_item_rows)

    assert len(item_rows_per_case) == 3
    assert all(row_count >= 45 for row_count in item_rows_per_case)
    assert item_residuals and max(item_residuals) <= 1e-6
    assert cash_residuals and max(cash_residuals) <= 1e-6


def test_markdown_tables_are_portable_to_vscode_preview():
    for path in PORTABLE_DOCS:
        lines = path.read_text(encoding="utf-8").splitlines()
        in_fence = False
        table_widths = []
        current_table = []

        for line in lines + [""]:
            if line.startswith("```"):
                in_fence = not in_fence
            if not in_fence and line.startswith("|") and line.endswith("|"):
                unescaped = line.replace(r"\|", "")
                width = unescaped.count("|") - 1
                current_table.append((width, len(line)))
            elif current_table:
                widths = {width for width, _ in current_table}
                assert len(widths) == 1, f"Tabela inconsistente em {path}: {widths}"
                table_widths.append(next(iter(widths)))
                assert max(length for _, length in current_table) <= 360, path
                current_table = []

        assert table_widths, path
        assert max(table_widths) <= 9, f"Tabela larga demais em {path}: {max(table_widths)} colunas"
