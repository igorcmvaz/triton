# -*- coding: utf-8 -*-
"""O que o programa comunica tem de coincidir com o que o programa faz.

A auditoria dos documentos encontrou o mesmo defeito em várias superfícies: um
número ou uma regra certa num lugar e diferente em outro. O manual dava faixas de
coeficiente sem fonte enquanto a interface aplicava outros valores; o README
anunciava pontuação LEED que o código não concede; as traduções citavam uma versão
que não existe; e mensagens de erro novas não estavam no manual.

Estes testes amarram cada superfície à fonte única: quando o programa mudar, o
teste falha e aponta o documento que ficou para trás.
"""

import importlib.util
import os
import re
import sys
import unicodedata

import numpy as np
import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _ler(*partes):
    return open(os.path.join(RAIZ, *partes), encoding="utf-8").read()


def _normal(texto):
    """Minúsculas, sem acento e com espaços simples, para comparar mensagens."""
    sem = unicodedata.normalize("NFKD", texto)
    sem = "".join(c for c in sem if not unicodedata.combining(c))
    return " ".join(sem.lower().split())


# ══════════════════════════════════════════════════════════════════════════════
# README
# ══════════════════════════════════════════════════════════════════════════════

def test_links_relativos_do_readme_existem():
    texto = _ler("README.md")
    alvos = re.findall(r"\]\(([^)#\s]+)\)", texto)
    locais = [a for a in alvos if not a.startswith(("http://", "https://", "mailto:"))]
    faltando = [a for a in locais if not os.path.exists(os.path.join(RAIZ, a))]
    assert not faltando, faltando


def test_readme_so_cita_a_versao_atual():
    from netuno import __version__
    texto = _ler("README.md")
    versoes = set(re.findall(r"5[._]0[._]\d", texto))
    permitidas = {__version__, __version__.replace(".", "_")}
    assert versoes <= permitidas, versoes - permitidas


def test_readme_descreve_o_leed_que_o_codigo_pontua():
    texto = _ler("README.md")
    assert "20% a 45%" not in texto
    assert "25% a 50%" in texto


# ══════════════════════════════════════════════════════════════════════════════
# Coeficiente de escoamento por material: uma tabela, quatro superfícies
# ══════════════════════════════════════════════════════════════════════════════

def _tabela_do_nucleo():
    from netuno.core.hydrology_defaults import COEFICIENTES_POR_MATERIAL
    return {nome: valor for nome, valor in COEFICIENTES_POR_MATERIAL}


@pytest.mark.parametrize("arquivo", ["tab_building.py"])
def test_listas_da_interface_usam_a_tabela_do_nucleo(arquivo):
    texto = _ler("netuno", "ui", arquivo)
    itens = re.findall(
        r'addItem\((?:tr\()?"([^"(]+?) \((\d,\d\d)\)"\)?,\s*([\d.]+)\)', texto)
    assert itens, arquivo
    tabela = _tabela_do_nucleo()
    for rotulo, exibido, dado in itens:
        assert float(exibido.replace(",", ".")) == float(dado), (rotulo, exibido, dado)
        assert rotulo in tabela, rotulo
        assert tabela[rotulo] == float(dado), (rotulo, tabela[rotulo], dado)
    assert len(itens) == len(tabela)


def test_documentacao_embutida_usa_a_tabela_do_nucleo():
    texto = _ler("netuno", "ui", "tab_documentation.py")
    bloco = texto.split("def create_tab_roof_materials", 1)[1].split("def create_tab_", 1)[0]
    valores = sorted(float(v.replace(",", "."))
                     for v in re.findall(r"<td align='center'><b>(\d,\d\d)</b></td>", bloco))
    esperado = sorted(_tabela_do_nucleo().values())
    # A tabela aparece duas vezes, em inglês e em português.
    assert valores == sorted(esperado * 2)


def test_figura_do_manual_le_a_tabela_do_nucleo():
    texto = _ler("manual", "gerar_infograficos.py")
    corpo = texto.split("def info_escoamento", 1)[1].split("\ndef ", 1)[0]
    assert "COEFICIENTES_POR_MATERIAL" in corpo
    assert "0.80, 0.90" not in corpo


def test_manual_avisa_que_a_ceramica_da_lista_nao_e_o_085_do_tutorial():
    texto = _ler("manual", "partes", "04_o_projeto_e_a_chuva.md")
    assert "0,75" in texto and "Personalizado" in texto


# ══════════════════════════════════════════════════════════════════════════════
# Toda mensagem de validação está documentada no manual
# ══════════════════════════════════════════════════════════════════════════════

def _mensagem(fn):
    with pytest.raises(ValueError) as erro:
        fn()
    return _normal(str(erro.value))


def _casos_de_validacao():
    from netuno.core.simulation import (
        build_sweep_volume_grid, run_single_simulation, validar_serie_precipitacao)
    serie = np.array([0.0, 10.0, 0.0])
    base = dict(area=100.0, runoff_coeff=0.85, discard_mm=2.0,
                total_demand_per_day=300.0, rainwater_share=0.4)

    def sim(**troca):
        kw = dict(base)
        vol = troca.pop("lower_tank_vol", 1000.0)
        kw.update(troca)
        return lambda: run_single_simulation(precip_data=serie, lower_tank_vol=vol, **kw)

    return [
        (sim(lower_tank_vol=-1.0), "volume do reservatorio inferior negativo"),
        (sim(upper_tank_vol=-1.0), "volume do reservatorio superior negativo"),
        (sim(area=-1.0), "area de captacao negativa"),
        (sim(runoff_coeff=1.5), "coeficiente de escoamento fora de [0, 1]"),
        (sim(discard_mm=-1.0), "lamina de descarte negativa"),
        (sim(total_demand_per_day=-1.0), "demanda diaria negativa"),
        (sim(rainwater_share=40.0), "fracao atendivel por agua pluvial fora de [0, 1]"),
        (sim(area=float("nan")), "nao e um numero finito"),
        (sim(discard_mode=9), "modo de descarte desconhecido"),
        (sim(discard_mode=3, discard_days_interval=0), "intervalo de descarte invalido"),
        (sim(pumping_threshold=-5.0), "nivel de acionamento da motobomba negativo"),
        (lambda: validar_serie_precipitacao([]), "serie de precipitacao esta vazia"),
        (lambda: validar_serie_precipitacao([1.0, float("nan")]), "sem valor numerico"),
        (lambda: validar_serie_precipitacao([1.0, -999.0]), "valor(es) negativo(s)"),
        (lambda: build_sweep_volume_grid(-1.0, 250.0),
         "o volume maximo da varredura deve ser finito e nao negativo"),
        (lambda: build_sweep_volume_grid(1000.0, 0.0),
         "o passo de varredura deve ser finito e maior que zero"),
    ] + _casos_fora_do_motor()


def _casos_fora_do_motor():
    """Cloração, motobomba, economia e multicritério: as outras mensagens visíveis."""
    from netuno.core.chlorination import Cloracao
    from netuno.core.economic import run_robust_economic_analysis
    from netuno.core.pump_hydraulics import energia_especifica_kwh_por_m3
    from netuno.core.topsis import _criterion_weights

    def eco(**troca):
        kw = dict(initial_investment=1000.0, annual_water_saved_m3=50.0,
                  water_tariff_per_m3=5.0)
        kw.update(troca)
        return lambda: run_robust_economic_analysis(**kw)

    return [
        (lambda: Cloracao(dose_mg_por_litro=-1.0), "a dose nao pode ser negativa"),
        (lambda: Cloracao(pureza=65.0), "pureza deve ficar em (0, 1]"),
        (lambda: Cloracao(fator_kg_co2e_por_kg_produto=-1.0),
         "o fator de emissao nao pode ser negativo"),
        (lambda: energia_especifica_kwh_por_m3(10.0, rendimento=55.0),
         "rendimento deve ficar em (0, 1]"),
        (lambda: energia_especifica_kwh_por_m3(10.0, 0.5, rendimento_do_motor_=2.0),
         "rendimento do motor deve ficar em (0, 1]"),
        (eco(initial_investment=-1.0), "deve ser um numero finito e nao negativo"),
        (eco(analysis_period_years=0), "o periodo de analise deve ser um numero inteiro de anos"),
        (eco(discount_rate=-1.5), "deve ser um numero finito e maior que -100%"),
        (eco(discount_rate=8.0), "parece estar em percentual"),
        (lambda: _criterion_weights([1.0, 1.0]),
         "informe 3 pesos de eixo ou 7 pesos de criterios topsis"),
        (lambda: _criterion_weights([1.0, -1.0, 1.0]),
         "os pesos topsis devem ser finitos e nao negativos"),
        (lambda: _criterion_weights([0.0, 0.0, 0.0]),
         "ao menos um peso topsis deve ser maior que zero"),
    ]


def test_convencao_das_taxas_e_a_que_o_manual_descreve():
    """Percentual na interface e no arquivo; fração na função anual; mês e ano compostos."""
    from netuno.core.economic import run_robust_economic_analysis
    from netuno.core.taxas import anual_pct_para_mensal_pct, mensal_pct_para_anual_pct
    base = dict(initial_investment=1000.0, annual_water_saved_m3=50.0,
                water_tariff_per_m3=5.0, analysis_period_years=10)
    run_robust_economic_analysis(discount_rate=0.05, **base)
    with pytest.raises(ValueError, match="percentual"):
        run_robust_economic_analysis(discount_rate=5.0, **base)
    assert mensal_pct_para_anual_pct(1.0) == pytest.approx(12.6825, abs=1e-4)
    assert anual_pct_para_mensal_pct(mensal_pct_para_anual_pct(0.7)) == pytest.approx(0.7)
    texto = _normal(_ler("manual", "partes", "37_mensagens_de_erro.md"))
    assert "a conversao entre mes e ano e composta" in texto
    assert "12,68% ao ano" in texto


def test_projeto_grava_a_tma_em_percentual_ao_mes():
    """A aba econômica gravava a taxa anual no campo mensal do arquivo."""
    texto = _ler("netuno", "ui", "tab_economic_integrated.py")
    assert "cfg.tma       = ts.get_tma_monthly_pct()" in texto
    assert "cfg.tma / 100.0 if cfg.tma > 1.0" not in texto
    for arquivo in ("tab_economic_integrated.py", "tab_economic_global_optimizer.py"):
        assert "if cfg.inflation > 1.0" not in _ler("netuno", "ui", arquivo), arquivo


def test_campo_de_taxa_vazio_usa_o_padrao_anual_em_qualquer_unidade(qapp):
    """Com «% a.m.» e o campo vazio, a TMA padrão de 12% ao ano virava 12% ao mês."""
    from netuno.ui.tab_tanks_simulation import TabTanksSimulation
    aba = TabTanksSimulation()
    for modo in ("month", "year"):
        aba._tma_mode = aba._inf_mode = modo
        aba.txt_tma.setText("-")
        aba.txt_inflation.setText("")
        assert aba.get_tma_annual_pct() == pytest.approx(12.0), modo
        assert aba.get_inflation_annual_pct() == pytest.approx(4.5), modo
    aba._tma_mode = "month"
    aba.txt_tma.setText("1")
    assert aba.get_tma_annual_pct() == pytest.approx(12.6825, abs=1e-4)


def test_fracao_atendivel_percentual_onde_se_digita_fracao_onde_se_guarda():
    """A unidade é fixada pelo lugar, e nunca adivinhada pelo valor."""
    from netuno.core.fracao_atendivel import (
        aviso_percentual_pequeno, fracao_para_percentual, percentual_para_fracao, validar_fracao)
    assert percentual_para_fracao("x", 40) == pytest.approx(0.40)
    assert percentual_para_fracao("x", 1) == pytest.approx(0.01)   # 1% é 1%, e não 100%
    assert fracao_para_percentual("x", 0.4) == pytest.approx(40.0)
    with pytest.raises(ValueError, match="parece estar em percentual"):
        validar_fracao("x", 40.0)
    with pytest.raises(ValueError, match=r"fora de \[0, 100\]"):
        percentual_para_fracao("x", 140.0)
    assert aviso_percentual_pequeno(0.4) and "digite 40" in aviso_percentual_pequeno(0.4)
    assert aviso_percentual_pequeno(40) is None and aviso_percentual_pequeno(0) is None


def test_motor_recusa_percentual_nos_vetores_de_fracao():
    """O vetor semanal com 30 no lugar de 0,30 era dividido por cem em silêncio."""
    from netuno.core.simulation import build_detailed_daily_demand_vectors
    cfg = {"demand_mode": "weekly", "weekly_demands": [100.0] * 7,
           "weekly_residents": [4.0] * 7, "weekly_shares": [30.0] * 7}
    with pytest.raises(ValueError, match="parece estar em percentual"):
        build_detailed_daily_demand_vectors(n_days=7, building_config=cfg,
                                            precip_data=np.zeros(7), start_date_str="07/01/2002")


def test_nenhum_ponto_adivinha_a_unidade_da_fracao_atendivel():
    """A regra «acima de 1 é percentual» não volta por nenhum caminho."""
    arquivos = [("netuno", "core", "simulation.py"), ("netuno", "core", "scenarios.py"),
                ("netuno", "core", "parser.py"), ("netuno", "core", "excel_scenarios.py"),
                ("netuno", "core", "report_generator.py"), ("netuno", "core", "cad_exporter.py"),
                ("netuno", "cli.py"), ("netuno", "ui", "tab_tanks_simulation.py"),
                ("netuno", "ui", "tab_building.py"), ("netuno", "ui", "tab_reports_pdf.py")]
    padrao = re.compile(r"/\s*100(\.0)?\s+if\s+[\w\[\]\"'().]+\s*>\s*1(\.0)?\s+else"
                        r"|\*\s*100(\.0)?\s+if\s+[\w\[\]\"'().]+\s*<=\s*1(\.0)?\s+else"
                        r"|if\s+0\.0\s*<=?\s*share\w*\s*<=\s*1\.0")
    for arquivo in arquivos:
        achados = padrao.findall(_ler(*arquivo))
        assert not achados, (arquivo, achados)


def test_campo_em_percentual_fica_laranja_com_valor_de_fracao(qapp):
    """O marcador da tela: 0,4 num campo em percentual é aceito, mas assinalado."""
    from netuno.ui.tab_building import TabBuilding
    aba = TabBuilding()
    aba.txt_share.setText("0,4")
    aba.check_input_highlight(aba.txt_share)
    assert "#f97316" in aba.txt_share.styleSheet() or "#fb923c" in aba.txt_share.styleSheet()
    assert "digite 40" in aba.txt_share.toolTip()
    aba.txt_share.setText("40")
    aba.check_input_highlight(aba.txt_share)
    assert "#f97316" not in aba.txt_share.styleSheet()
    assert "40 significa 40%" in aba.txt_share.toolTip()
    assert "⚠" not in aba.txt_share.toolTip()


def test_manual_justifica_a_unidade_da_fracao_atendivel():
    texto = _normal(_ler("manual", "partes", "05_a_edificacao_e_a_demanda.md"))
    assert "percentual na tela, fracao no arquivo" in texto
    assert "nunca adivinhada pelo valor" in texto
    assert "acima de 1 e percentual" in texto
    erros = _normal(_ler("manual", "partes", "37_mensagens_de_erro.md"))
    assert "aceitam as duas formas" not in erros
    assert "simular mesmo assim" in erros


def test_aceitabilidade_smaa_tem_unidade_fixa():
    """Percentual em `first_rank_probs`, fração em `first_rank_acceptabilities`, sempre.

    A conversão adivinhava pelo máximo: com nenhuma alternativa acima de 1%, a
    fração saía cem vezes maior.
    """
    from netuno.core.mcdm_methods import SmaaResult
    res = SmaaResult(candidates=[None, None], rank_acceptabilities=np.array([[0.5, 99.5], [0.5, 99.5]]),
                     first_rank_probs=np.array([0.5, 0.5]), central_weights=np.zeros((2, 3)),
                     most_acceptable_index=0)
    assert np.allclose(res.first_rank_acceptabilities, [0.005, 0.005])
    padrao = re.compile(r"/\s*100(\.0)?\s+if\s+.*>\s*1(\.0)?\s+else|\*\s*100(\.0)?\s+if\s+.*<=\s*1(\.0)?\s+else")
    for arquivo in (("netuno", "core", "mcdm_methods.py"), ("netuno", "ui", "charts.py")):
        assert not padrao.findall(_ler(*arquivo)), arquivo


def test_mensagem_ao_usuario_nao_expoe_nome_interno_de_variavel():
    """«initial_investment deve ser finito» chegava assim à tela."""
    from netuno.core.economic import run_robust_economic_analysis
    with pytest.raises(ValueError) as erro:
        run_robust_economic_analysis(initial_investment=-1.0,
                                     annual_water_saved_m3=1.0,
                                     water_tariff_per_m3=1.0)
    assert not re.search(r"\b[a-z]+_[a-z_]+\b", str(erro.value)), str(erro.value)


def test_toda_mensagem_de_validacao_esta_documentada_no_manual():
    manual = _normal(_ler("manual", "partes", "37_mensagens_de_erro.md"))
    ausentes, divergentes = [], []
    for disparo, frase in _casos_de_validacao():
        mensagem = _mensagem(disparo)
        if frase not in mensagem:
            divergentes.append((frase, mensagem[:90]))
        if frase not in manual:
            ausentes.append(frase)
    assert not divergentes, divergentes
    assert not ausentes, ausentes


# ══════════════════════════════════════════════════════════════════════════════
# Traduções e relatórios
# ══════════════════════════════════════════════════════════════════════════════

def test_traducoes_so_citam_a_versao_atual():
    from netuno import __version__
    texto = _ler("netuno", "ui", "translation.py")
    versoes = set(re.findall(r"Netuno (5\.0\.\d)", texto))
    assert versoes <= {__version__}, versoes


@pytest.fixture(scope="module")
def dados_de_relatorio():
    """Os dados de projeto dos testes de relatório já existentes."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    pytest.importorskip("PySide6")
    from PySide6.QtWidgets import QApplication
    from netuno.ui import translation
    anterior = translation._runtime_language
    translation._runtime_language = "pt"
    QApplication.instance() or QApplication([])

    caminho = os.path.join(RAIZ, "tests", "integration", "test_report_generator.py")
    spec = importlib.util.spec_from_file_location("_relatorios_referencia", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    capturados = {}
    for nome in ("generate_executive_html_report", "generate_research_html_report"):
        original = getattr(modulo, nome)

        def espia(dados, *a, _o=original, _n=nome, **k):
            capturados.setdefault(_n, dados)
            return _o(dados, *a, **k)

        setattr(modulo, nome, espia)
    try:
        modulo.test_generate_executive_html_report()
        modulo.test_generate_research_html_report()
    finally:
        translation._runtime_language = anterior
    return capturados


INDEFINIDOS = {
    "nan": r"\bnan\b",
    "None": r"\bNone\b",
    "inf": r"\binf\b",
    "marcador não resolvido": r"\{[a-z_]+\}",
}


@pytest.mark.parametrize("tipo", ["economic", "environmental", "research"])
@pytest.mark.parametrize("lang", ["pt", "en"])
def test_relatorio_nao_traz_valor_indefinido(dados_de_relatorio, tipo, lang):
    from netuno.core.report_service import generate_report_html
    chave = ("generate_executive_html_report" if tipo == "economic"
             else "generate_research_html_report")
    html = generate_report_html(tipo, dict(dados_de_relatorio[chave]), lang=lang)
    texto = re.sub(r"data:image/[^\s\"']+", "", re.sub(r"<[^>]+>", " ", html))
    achados = {k: re.findall(p, texto)[:3] for k, p in INDEFINIDOS.items()
               if re.search(p, texto)}
    # Versão antiga: qualquer 5.x.y que não seja a atual.
    from netuno import __version__
    antigas = sorted({v for v in re.findall(r"5\.\d+\.\d+", texto) if v != __version__})
    if antigas:
        achados["versão antiga"] = antigas[:3]
    assert not achados, achados


# ══════════════════════════════════════════════════════════════════════════════
# Documentos distribuídos: versão, autoria e numeração
# ══════════════════════════════════════════════════════════════════════════════

#: Tudo o que sai do repositório para as mãos de alguém: o instalador, os textos
#: que ele mostra, os relatórios que a interface abre e os guias dos exemplos.
DISTRIBUIDOS = [
    "README.md",
    "CITATION.cff",
    "pyproject.toml",
    "setup_script.iss",
    "infos_licenses/README.md",
    "infos_licenses/info_before.txt",
    "infos_licenses/info_after.txt",
    "infos_licenses/license.txt",
    "docs/README.md",
    "netuno/docs/relatorio_validacao.md",
    "netuno/docs/relatorio_validacao_en.md",
    "netuno/docs/fluxogramas_metodologicos.md",
    "netuno/docs/proximos_passos_decisao_robusta.md",
    "manual/casos/README.md",
]


def _em_beta():
    """O pyproject é a fonte única do estado de lançamento."""
    return "Development Status :: 4 - Beta" in _ler("pyproject.toml")


def test_estado_beta_e_o_mesmo_no_pacote_e_no_manual():
    """O pacote dizia «Production/Stable» enquanto o manual e a capa diziam beta."""
    manual_diz_beta = "(beta)" in _ler("manual", "gerar.py")
    assert _em_beta() == manual_diz_beta


@pytest.mark.parametrize("relativo", DISTRIBUIDOS)
def test_documento_distribuido_so_cita_a_versao_atual(relativo):
    """O instalador de uma versão não pode entregar um README que cite outra.

    Durante o beta, o histórico de versões anteriores fica nos documentos por
    decisão do autor (2026-09-15). O teste volta a valer sozinho no lançamento:
    basta o pyproject deixar de declarar Beta, e o teste acima obriga o manual a
    acompanhar.
    """
    if _em_beta():
        pytest.skip("beta: menções a versões anteriores são mantidas até o lançamento")
    from netuno import __version__
    caminho = os.path.join(RAIZ, *relativo.split("/"))
    if not os.path.exists(caminho):
        pytest.skip(f"{relativo} ausente")
    texto = open(caminho, encoding="utf-8", errors="ignore").read()
    versoes = set(re.findall(r"(?<![\d.])5[._]0[._]\d(?!\d)", texto))
    permitidas = {__version__, __version__.replace(".", "_")}
    assert versoes <= permitidas, (relativo, versoes - permitidas)


def test_citacoes_creditam_os_autores_do_netuno_5():
    """Toda citação do programa credita Vaz e Ghisi.

    O README distribuído com o instalador ainda citava «GHISI; CORDOVA, Netuno
    5». Cordova é coautor do Netuno 4, e continua citado como tal nas
    referências do manual; a citação do Netuno 5 é outra.
    """
    fontes = {
        "infos_licenses/README.md": _ler("infos_licenses", "README.md"),
        "netuno/ui/main_window.py": _ler("netuno", "ui", "main_window.py"),
        "manual/gerar.py": _ler("manual", "gerar.py"),
    }
    for nome, texto in fontes.items():
        normal = _normal(texto)
        assert "vaz" in normal and "ghisi" in normal, nome
        assert "cordova, m. m. netuno 5" not in normal, nome
        assert "cordova, marcelo marcel}" not in normal, nome


def test_guia_dos_casos_cita_secoes_que_existem():
    """A coluna de seção do guia dos casos usa a numeração atual do manual."""
    sys.path.insert(0, os.path.join(RAIZ, "manual"))
    from gerar import indice_das_secoes
    validas = set(indice_das_secoes().values())
    for arquivo in (("manual", "casos", "README.md"),
                    ("manual", "apendices", "J_arquivos_de_exemplo.md")):
        texto = _ler(*arquivo)
        citadas = set(re.findall(r"(?<![\d.,])(\d\.\d{1,2})(?![\d,%])", texto))
        assert citadas, arquivo
        assert citadas <= validas, (arquivo, citadas - validas)
        assert "Capítulo |" not in texto, arquivo


def test_o_manual_cita_o_numero_de_parametros_que_o_projeto_tem():
    """«Os 103 parâmetros» ficou escrito em quatro seções quando o programa já tinha 104.

    O apêndice A é gerado do código e acompanhava o programa; o texto corrido
    não. Toda menção ao total de parâmetros ou campos do projeto precisa bater
    com os campos da classe de configuração.
    """
    import dataclasses
    from netuno.core.parser import NetunoConfig
    total = len(dataclasses.fields(NetunoConfig))
    pasta = os.path.join(RAIZ, "manual")
    citados = []
    for sub in ("partes", "apendices"):
        for nome in os.listdir(os.path.join(pasta, sub)):
            if not nome.endswith(".md"):
                continue
            texto = open(os.path.join(pasta, sub, nome), encoding="utf-8").read()
            for m in re.finditer(r"(?:[Oo]s|São \*\*)(\d{2,3})\*{0,2} (parâmetros|campos)", texto):
                citados.append((nome, int(m.group(1))))
    assert citados, "o manual deixou de citar o total de parâmetros"
    errados = [(nome, n) for nome, n in citados if n != total]
    assert not errados, (total, errados)


#: Onde o programa descreve o descarte ao usuário: a documentação embutida, o
#: relatório de verificação que a interface abre e o gerador de relatórios.
DESCRICOES_DO_DESCARTE = [
    ("netuno", "ui", "tab_documentation.py"),
    ("netuno", "docs", "relatorio_validacao.md"),
    ("netuno", "docs", "relatorio_validacao_en.md"),
    ("netuno", "core", "report_generator.py"),
]


@pytest.mark.parametrize("partes", DESCRICOES_DO_DESCARTE, ids=lambda p: p[-1])
def test_nenhum_documento_descreve_o_descarte_como_limiar(partes):
    """O motor subtrai a lâmina; três superfícies diziam que não.

    A página de método em inglês, a lista de vantagens da simulação diária nos
    dois idiomas e o relatório de verificação exibido pela interface afirmavam
    a regra do Netuno 4, que aceita a chuva inteira ao atingir o limiar. É a
    regra que mais pesa no resultado, e o documento contradizia o cálculo.
    """
    texto = _normal(_ler(*partes))
    proibidas = ["does not subtract", "nao subtrai", "legacy rule", "regra legada",
                 "full daily rainfall is accepted", "chuva diaria integral e aceita"]
    achadas = [frase for frase in proibidas if frase in texto]
    assert not achadas, achadas


def test_o_motor_de_fato_subtrai_a_lamina():
    """A afirmação que os documentos passam a fazer, conferida no cálculo."""
    from netuno.core.simulation import run_single_simulation
    r = run_single_simulation(precip_data=np.array([1.5, 2.0, 5.0]),
                              lower_tank_vol=1000.0, area=100.0,
                              runoff_coeff=1.0, discard_mm=2.0, discard_mode=1,
                              total_demand_per_day=0.0, rainwater_share=0.4,
                              store_daily_details=True)
    assert [d.eff_precip_mm for d in r.daily_results] == pytest.approx([0.0, 0.0, 3.0])


def test_nomes_dos_casos_nao_citam_numeracao_antiga():
    pasta = os.path.join(RAIZ, "manual", "casos")
    for nome in os.listdir(pasta):
        if nome.endswith(".netuno"):
            texto = open(os.path.join(pasta, nome), encoding="utf-8").read(4000)
            assert not re.search(r"capitulo \d|guia \d", texto), nome
