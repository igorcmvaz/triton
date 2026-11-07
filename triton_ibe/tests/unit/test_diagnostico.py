"""O diagnóstico do pacote acusa o que falta, e o build o usa para recusar pacote incompleto."""

from triton.core import diagnostico


def test_o_diagnostico_cobre_o_3d_a_base_e_as_tarifas():
    nomes = [nome for nome, _, _ in diagnostico.verificacoes()]
    for item in ("Arranjo 3D e volumetria", "Base climática CLIMBra", "Banco tarifário", "Manual em PDF"):
        assert item in nomes
    assert set(diagnostico.OBRIGATORIOS) <= set(nomes)


def test_o_arranjo_3d_e_as_tarifas_passam_no_codigo_fonte():
    from triton.core.edition import usa_dados_do_brasil
    itens = {nome: (ok, detalhe) for nome, ok, detalhe in diagnostico.verificacoes()}
    assert itens["Arranjo 3D e volumetria"][0] is True, itens["Arranjo 3D e volumetria"][1]
    ok, detalhe = itens["Banco tarifário"]
    if usa_dados_do_brasil():
        assert ok is True and "CORSAN na fórmula exponencial: 34 de 34" in detalhe
    else:
        assert ok is None



def test_falta_do_visualizador_reprova_o_pacote(monkeypatch, tmp_path):
    import triton.core.volumetry_export as exportacao

    monkeypatch.setattr(exportacao, "VIEWER_BUNDLE", tmp_path / "ausente.js")
    itens = diagnostico.verificacoes()
    assert "Volumetria 3D (WebGL)" in diagnostico.faltam_obrigatorios(itens)
    assert "[FALTA] Volumetria 3D (WebGL)" in diagnostico.relatorio(itens)


def test_banco_neutro_nao_reprova_o_arranjo_por_custo_zero(monkeypatch):
    """Nas edições INT/IBE o arquivo de custos distribuído não traz preços: custo zero não é lacuna."""
    import triton.core.cost_estimates as ce
    from triton.core.quantitativo_do_arranjo import conferir_cobertura, levantar
    from triton.core.study_layout import generate_study_layout

    layout = generate_study_layout({"lower_vol": 5000, "area": 150, "pump_count": 2})
    monkeypatch.setattr(ce, "PIPE_COST_PER_METER", {dn: 0.0 for dn in ce.PIPE_COST_PER_METER})
    monkeypatch.setattr(ce, "banco_tem_precos", lambda: False)
    assert not [f for f in conferir_cobertura(levantar(layout)) if "sem custo" in f]
    monkeypatch.setattr(ce, "banco_tem_precos", lambda: True)
    assert [f for f in conferir_cobertura(levantar(layout)) if "sem custo" in f]


def test_o_diagnostico_procura_o_manual_da_edicao():
    from triton.core.edition import is_int_edition
    detalhe = diagnostico._manual()[2]
    assert ("Triton-User-Manual.pdf" in detalhe) == is_int_edition()
