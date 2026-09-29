# -*- coding: utf-8 -*-
"""Gera os relatórios de exemplo em reports/exemplos/, pela própria interface.

Os exemplos precisam sair do mesmo caminho que o usuário percorre: carregar o
projeto, simular, rodar a economia, a ACV e a decisão multicritério, e exportar
os três laudos oficiais. Este script faz exatamente isso, com a janela
principal criada mas não exibida, sobre os três estudos de caso de examples/.

Cada etapa é conferida, e o script interrompe em vez de gravar um laudo vazio:
a simulação tem de rodar, a economia de água tem de ser positiva, e cada PDF
tem de citar a cidade do caso e trazer algum percentual diferente de zero.

Rodar de novo sempre que o programa mudar algo que apareça num laudo — do
contrário os exemplos passam a mostrar números que a versão atual não produz.

    python scripts/gerar_relatorios_exemplo.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

SAIDA = RAIZ / "reports" / "exemplos"

CASOS = [  # arquivo, pasta de saída, idiomas, cidade que o laudo tem de citar
    ("estudo_caso_1_florianopolis1.netuno", "01_Florianopolis", ("pt", "en"), "Florian"),
    ("estudo_caso_2_brasilia2.netuno", "02_Brasilia", ("pt",), "Bras"),
    ("estudo_caso_3_manaus3.netuno", "03_Manaus", ("pt",), "Manaus"),
]
LAUDOS = [
    ("economic", "Laudo_Executivo", "Executive_Report"),
    ("environmental", "Auditoria_Ambiental_ESG", "Environmental_ESG_Audit"),
    ("research", "Dossie_Tecnico", "Technical_Dossier"),
]


def _silenciar_dialogos():
    """Os avisos modais travariam a automação; aqui viram linhas de log.

    Um aviso de erro interrompe: não se grava laudo de uma rodada que falhou.
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


def _conferir_pdf(caminho: Path, cidade: str):
    import fitz
    texto = " ".join(pg.get_text() for pg in fitz.open(caminho))
    if cidade.lower() not in texto.lower():
        raise RuntimeError(f"{caminho.name}: o laudo não cita {cidade}")
    if not re.search(r"[1-9]\d*[.,]\d+\s*%", texto):
        raise RuntimeError(f"{caminho.name}: nenhum percentual diferente de zero")


def gerar():
    from PySide6.QtWidgets import QApplication
    from netuno.core.report_generator import save_pdf_report
    from netuno.ui.main_window import MainWindow

    app = QApplication.instance() or QApplication(sys.argv)
    _silenciar_dialogos()
    gerados = []
    # O idioma global NÃO muda aqui. Trocá-lo para gerar o laudo em inglês
    # deixava o caso seguinte carregando em inglês, a simulação recusava rodar
    # e os laudos saíam vazios. O idioma vai só para cada relatório.
    for arquivo, pasta, idiomas, cidade in CASOS:
        print(f"\n{arquivo}")
        janela = MainWindow()
        janela.on_load_simulation(str(RAIZ / "examples" / arquivo))
        sim = janela.tab_tanks_simulation
        sim.verified_dialogs = {"capex", "motobomba", "opex", "tariffs"}
        sim.run_simulation(force=True)
        if sim.last_single_result is None or sim.last_sweep_result is None:
            raise RuntimeError(f"{arquivo}: a simulação não rodou")
        economia = sim.last_single_result.potential_potable_savings_pct
        if not economia > 0:
            raise RuntimeError(f"{arquivo}: economia de água potável nula")
        janela.tab_economic.calculate_economics(force=True)
        janela.tab_environmental.recalculate_and_update()
        janela.tab_global_optimizer.recalculate_all()
        app.processEvents()
        print(f"    simulado: economia de água potável de {economia:.2f}%")

        destino = SAIDA / pasta
        destino.mkdir(parents=True, exist_ok=True)
        rel = janela.tab_reports
        for lang in idiomas:
            for tipo, nome_pt, nome_en in LAUDOS:
                rel.combo_report_type.setCurrentIndex(rel.combo_report_type.findData(tipo))
                rel.update_report_preview()
                html = rel.generate_html_content(lang=lang)
                caminho = destino / f"{nome_pt if lang == 'pt' else nome_en}_{lang}.pdf"
                save_pdf_report(str(caminho), html)
                app.processEvents()
                _conferir_pdf(caminho, cidade)
                print(f"    {caminho.relative_to(RAIZ)}  {caminho.stat().st_size // 1024} KB")
                gerados.append(caminho)
        janela.close()
        janela.deleteLater()
        app.processEvents()

    print(f"\n{len(gerados)} relatórios em {SAIDA.relative_to(RAIZ)}, todos conferidos")
    return gerados


if __name__ == "__main__":
    gerar()
