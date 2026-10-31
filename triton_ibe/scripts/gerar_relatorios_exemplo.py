# -*- coding: utf-8 -*-
"""Gera os relatórios de exemplo (INT e IBE) em reports/exemplos/<cidade>/, pela própria interface.

Os exemplos saem do mesmo caminho que o utilizador percorre: abrir o projeto, simular, correr a economia,
a ACV e a decisão multicritério, e exportar os três relatórios oficiais (executivo, ambiental e dossiê).
A janela principal é criada mas não é exibida. Não use QT_QPA_PLATFORM=offscreen: nessa plataforma
não há fontes e o PDF sai com os caracteres em quadrados (sem texto extraível).

Os casos são os projetos de ``examples/`` (INT) ou ``examples/portugal/`` (IBE); a edição vem de
``TRITON_EDITION`` ou, sem ela, do marcador da pasta (``triton/data/edicao_padrao.txt``).
INT sai em inglês; IBE em português de Portugal. Cada etapa é conferida e o script pára em vez de
gravar um relatório vazio: a simulação tem de correr, a economia de água tem de ser positiva, e cada PDF
tem de citar a cidade do caso e trazer algum percentual diferente de zero. Se o QtWebEngine
devolver um PDF em branco (acontece fora de uma sessão gráfica completa), grava-se pelo caminho de reserva (QTextDocument).

Termos do Brasil encontrados nos PDFs são listados no fim (e fazem o script falhar com ``--estrito``).

Voltar a correr sempre que o programa mudar algo que apareça num relatório.

    python scripts/gerar_relatorios_exemplo.py [--estrito] [cidade ...]
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _edicao() -> str:
    """A edição desta pasta (INT ou IBE): ``TRITON_EDITION`` ou o marcador ``triton/data/edicao_padrao.txt``."""
    if str(RAIZ) not in sys.path:
        sys.path.insert(0, str(RAIZ))
    from triton.core.edition import get_current_edition
    return get_current_edition()


EDICAO = _edicao()
if EDICAO not in ("INT", "IBE"):
    raise SystemExit("Este gerador serve às pastas da Internacional e da Ibérica.")
os.environ["TRITON_EDITION"] = EDICAO

SAIDA = RAIZ / "reports" / "exemplos"

#: Idioma e nomes dos ficheiros por edição: (tipo do relatório, nome do ficheiro).
IDIOMA = {"INT": "en", "IBE": "pt"}[EDICAO]
RELATORIOS = {
    "INT": [("economic", "Executive_Report"), ("environmental", "Environmental_ESG_Audit"),
            ("research", "Technical_Dossier")],
    "IBE": [("economic", "Relatorio_Executivo"), ("environmental", "Auditoria_Ambiental_ESG"),
            ("research", "Dossie_Tecnico")],
}[EDICAO]
#: Palavras que denunciam o Brasil (ou, na INT, também Portugal) num relatório de exemplo.
TERMOS_DO_BRASIL = ("Florianópolis", "Florianopolis", "Brasília", "Manaus", "São Paulo", "R$", "CASAN", "CELESC",
                    "CLIMBra", "SABESP", "ANEEL", "NBR", "ABNT", "IPTU", "Selic",
                    "CREA", "SNIS", "MCTI", "INMET", "Casa Azul", "AQUA-HQE")
TERMOS_DE_PORTUGAL = ("E-OBS", "Iberia01", "EPAL", "ERSAR", "Lisboa", "Funchal")
#: O que o rodapé de cada edição tem de trazer (a licença e o crédito da chuva; na IBE, também o nível e a cobertura).
EXIGIDOS = {"INT": ("Open-Meteo", "CC BY 4.0"),
            "IBE": ("Cobertura",)}[EDICAO]


def _cidades():
    """(arquivo do projeto, pasta de saída, texto que o relatório tem de citar) por exemplo da edição."""
    import json
    pastas = [RAIZ / "examples" / "portugal", RAIZ / "examples" / "espanha"] if EDICAO == "IBE" else [RAIZ / "examples"]
    casos = []
    for pasta in pastas:
        for arquivo in sorted(pasta.glob("*.triton")):
            if arquivo.name.startswith("triton-"):
                continue
            dados = json.loads(arquivo.read_text(encoding="utf-8"))
            # «Lisboa [PT-1106]»: o relatório cita o nome, e o código vai à parte (o rodapé confere-o)
            casos.append((arquivo, arquivo.stem, str(dados["rainfall"]["climate_city_name"]).split(" [")[0]))
    return casos


def _silenciar_dialogos():
    """Os avisos modais travariam a automação; aqui viram linhas de registo.

    Um aviso de erro interrompe: não se grava relatório de uma corrida que falhou.
    """
    from PySide6.QtWidgets import QMessageBox

    def _registro(nivel):
        def _f(parent, titulo, texto, *a, **k):
            print(f"    [{nivel}] {titulo}: {str(texto).splitlines()[0][:120]}")
            if nivel in ("aviso", "erro"):
                raise RuntimeError(f"{titulo}: {texto}")
            return QMessageBox.StandardButton.Ok
        return _f

    QMessageBox.information = staticmethod(_registro("info"))
    QMessageBox.warning = staticmethod(_registro("aviso"))
    QMessageBox.critical = staticmethod(_registro("erro"))
    QMessageBox.question = staticmethod(lambda *a, **k: QMessageBox.StandardButton.Yes)


def _texto_do_pdf(caminho: Path) -> str:
    import fitz
    with fitz.open(caminho) as pdf:
        return " ".join(pg.get_text() for pg in pdf)


def _em_branco(caminho: Path, cidade: str) -> bool:
    try:
        return cidade.lower() not in _texto_do_pdf(caminho).lower()
    except Exception:
        return True


def _gravar(caminho: Path, html: str, cidade: str):
    """Grava o PDF; se o QtWebEngine o devolver em branco, regrava pelo QTextDocument."""
    from triton.core import report_generator as rg
    rg.save_pdf_report(str(caminho), html)
    if _em_branco(caminho, cidade):
        original = rg._save_pdf_report_with_webengine
        rg._save_pdf_report_with_webengine = lambda *a, **k: False
        try:
            rg.save_pdf_report(str(caminho), html)
        finally:
            rg._save_pdf_report_with_webengine = original
        print("      (QtWebEngine em branco: gravado pelo QTextDocument)")


def _conferir_pdf(caminho: Path, cidade: str) -> list:
    texto = " ".join(_texto_do_pdf(caminho).split())      # quebras de linha do PDF não contam
    if cidade.lower() not in texto.lower():
        raise RuntimeError(f"{caminho.name}: o relatório não cita {cidade}")
    if not re.search(r"[1-9]\d*[.,]\d+\s*%", texto):
        raise RuntimeError(f"{caminho.name}: nenhum percentual diferente de zero")
    # IBE: chuva do Iberia01 (ODbL, com a atribuição de Herrera et al. 2019), ou ERA5 nas ilhas (CC BY, nível C).
    # Nenhum relatório de exemplo da IBE pode carregar a restrição não comercial da E-OBS.
    exigidos = EXIGIDOS
    if EDICAO == "IBE":
        exigidos = EXIGIDOS + ("Qualidade da chuva",) + (
            ("Open-Meteo", "ERA5", "CC BY 4.0") if cidade == "Funchal"
            else ("Iberia01", "ODbL", "Herrera", "10.5194/essd-11-1947-2019"))
        proibidos = [t for t in ("NÃO PODE SER USADA COMERCIALMENTE", "não comerciais", "NÃO COMERCIAL", "E-OBS",
                                 "pressupostos implementadas", "pressupostos implementada ") if t in texto]
        if proibidos:
            raise RuntimeError(f"{caminho.name}: o relatório traz o que não devia: {', '.join(proibidos)}")
    em_falta = [t for t in exigidos if t not in texto]
    if em_falta:
        raise RuntimeError(f"{caminho.name}: falta no rodapé: {', '.join(em_falta)}")
    termos = TERMOS_DO_BRASIL + (TERMOS_DE_PORTUGAL if EDICAO == "INT" else ())
    return sorted({t for t in termos if t in texto})


def gerar(cidades=None, estrito: bool = False):
    from PySide6.QtWidgets import QApplication
    from triton.core.report_generator import save_pdf_report  # noqa: F401 (falha cedo se faltar o núcleo)
    from triton.ui.main_window import MainWindow

    casos = _cidades()
    if cidades:
        casos = [c for c in casos if c[1] in cidades]
    app = QApplication.instance() or QApplication(sys.argv)
    _silenciar_dialogos()
    gerados, achados = [], {}
    # O idioma global NÃO muda aqui: trocá-lo para gerar o relatório noutra língua deixava o caso
    # seguinte a carregar nessa língua. O idioma vai só para cada relatório.
    for arquivo, pasta, cidade in casos:
        print(f"\n{arquivo.name}")
        janela = MainWindow()
        janela.on_load_simulation(str(arquivo))
        sim = janela.tab_tanks_simulation
        sim.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
        sim.run_simulation(force=True)
        if sim.last_single_result is None or sim.last_sweep_result is None:
            raise RuntimeError(f"{arquivo.name}: a simulação não correu")
        economia = sim.last_single_result.potential_potable_savings_pct
        if not economia > 0:
            raise RuntimeError(f"{arquivo.name}: economia de água potável nula")
        janela.tab_economic.calculate_economics(force=True)
        janela.tab_environmental.recalculate_and_update()
        janela.tab_global_optimizer.recalculate_all()
        app.processEvents()
        print(f"    simulado: poupança de água potável de {economia:.2f}%")

        destino = SAIDA / pasta
        destino.mkdir(parents=True, exist_ok=True)
        rel = janela.tab_reports
        for tipo, nome in RELATORIOS:
            rel.combo_report_type.setCurrentIndex(rel.combo_report_type.findData(tipo))
            rel.update_report_preview()
            html = rel.generate_html_content(lang=IDIOMA)
            caminho = destino / f"{nome}_{IDIOMA}.pdf"
            _gravar(caminho, html, cidade)
            app.processEvents()
            termos = _conferir_pdf(caminho, cidade)
            if termos:
                achados[str(caminho.relative_to(RAIZ))] = termos
            print(f"    {caminho.relative_to(RAIZ)}  {caminho.stat().st_size // 1024} KB"
                  + (f"  TERMOS A NEUTRALIZAR: {', '.join(termos)}" if termos else ""))
            gerados.append(caminho)
        janela.close()
        janela.deleteLater()
        app.processEvents()

    print(f"\n{len(gerados)} relatórios em {SAIDA.relative_to(RAIZ)}")
    if achados:
        print(f"{len(achados)} com termos que não deviam estar na edição {EDICAO}: {achados}")
        if estrito:
            raise SystemExit(1)
    return gerados


if __name__ == "__main__":
    argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
    gerar(argumentos or None, estrito="--estrito" in sys.argv)
