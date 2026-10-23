"""Folha de estilo sem seletor, em widget que contém outros, vaza para os filhos.

O Qt propaga aos descendentes toda folha escrita sem seletor. Num quadro que
serve de cartão, `setStyleSheet("background: #fff; border: 1px solid ...;
padding: 8px 10px;")` não pinta só o cartão: pinta cada rótulo, cada caixa de
combinação e cada barra deslizante dentro dele. O sintoma é sempre o mesmo —
rótulos viram caixinhas com borda, e o `padding` desloca o que deveria estar
centrado na linha.

Foram cinco quadros assim no programa, e um deles desalinhava a barra do
simulador de fatura. Escrever `#nomeDoQuadro { ... }` prende a folha ao quadro.
Este teste recusa a volta do padrão.
"""
import ast
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INTERFACE = os.path.join(RAIZ, "triton", "ui")

#: Tipos que contêm outros widgets. Neles, a folha sem seletor vaza.
CONTEINERES = {"QWidget", "QFrame", "QGroupBox", "QScrollArea", "QTabWidget",
               "QSplitter", "QDialog", "QStackedWidget", "QToolBox", "QMainWindow"}

#: Quadros sem filhos, usados como traço divisor: não há para onde vazar.
DISPENSADOS = {
    ("sidebar.py", "line"),
    ("sidebar.py", "sep"),
}


def _texto_do_argumento(arg):
    """O conteúdo da folha, seja literal ou f-string com partes calculadas."""
    try:
        valor = ast.literal_eval(arg)
        return valor if isinstance(valor, str) else None
    except Exception:
        pass
    if isinstance(arg, ast.JoinedStr):
        return "".join(v.value for v in arg.values if isinstance(v, ast.Constant))
    return None


def _folhas_sem_seletor_em_conteiner():
    achados = []
    for pasta, _, arquivos in os.walk(INTERFACE):
        if "__pycache__" in pasta:
            continue
        for arquivo in sorted(arquivos):
            if not arquivo.endswith(".py"):
                continue
            caminho = os.path.join(pasta, arquivo)
            arvore = ast.parse(open(caminho, encoding="utf-8").read(), filename=caminho)
            # nome da variável -> classe com que foi construída
            tipos = {}
            for no in ast.walk(arvore):
                if isinstance(no, ast.Assign) and isinstance(no.value, ast.Call) \
                        and isinstance(no.value.func, ast.Name):
                    for alvo in no.targets:
                        tipos[ast.unparse(alvo)] = no.value.func.id
            for no in ast.walk(arvore):
                if not (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)
                        and no.func.attr == "setStyleSheet" and no.args):
                    continue
                texto = _texto_do_argumento(no.args[0])
                if texto is None or "{" in texto:
                    continue                      # tem seletor: não vaza
                alvo = ast.unparse(no.func.value)
                if tipos.get(alvo) not in CONTEINERES:
                    continue
                if (arquivo, alvo) in DISPENSADOS:
                    continue
                achados.append(f"{arquivo}:{no.lineno} {alvo} [{tipos[alvo]}]")
    return achados


def test_nenhum_conteiner_veste_folha_sem_seletor():
    """Se falhar: dê um objectName ao widget e escreva `#nome {{ ... }}`."""
    achados = _folhas_sem_seletor_em_conteiner()
    assert not achados, ("folha sem seletor em contêiner, vaza para os filhos: "
                         + "; ".join(achados))


def test_os_dispensados_ainda_existem():
    """Uma dispensa que perdeu o alvo é dispensa que ninguém revisa."""
    for arquivo, alvo in DISPENSADOS:
        caminho = os.path.join(INTERFACE, arquivo)
        assert os.path.exists(caminho), caminho
        assert f"{alvo} = QFrame()" in open(caminho, encoding="utf-8").read(), (arquivo, alvo)
