"""
Configuração global do Pytest para a suíte do Triton.

Este arquivo é IDÊNTICO nas três edições (triton_brl, triton_int, triton_prt): a edição
vem da variável TRITON_EDITION e, se ela não estiver definida, do nome da pasta em que a
suíte está (`triton_brl` -> BRL, `triton_int` -> INT, `triton_prt` -> PRT; qualquer outro
nome -> BRL, o padrão do programa). Assim `python -m pytest` dentro de uma pasta de edição
testa aquela edição, com ou sem a variável.

Garante execução headless para Qt/PySide6 e Matplotlib (Agg) e permite que a
verificação numérica do núcleo seja executada num ambiente mínimo, sem a stack
gráfica instalada.

Por que a degradação importa
----------------------------
Os testes de invariantes e propriedades científicas não dependem de interface. Sem
PySide6 instalado, os módulos que dependem da interface simplesmente não são coletados
(`MODULOS_QUE_EXIGEM_INTERFACE`), e o restante da suíte executa normalmente, o que permite
rodar a verificação em contêineres mínimos de integração contínua.

Listas por edição
-----------------
Dois arquivos de texto, ao lado deste, dizem o que só faz sentido com os dados de uma edição:

- ``so_da_brl.txt``: depende de dado brasileiro (banco de 652 municípios, CLIMBra, CASAN...).
  Fora da BRL, é saltado.
- ``so_da_prt.txt``: depende de dado de Portugal (tarifários, base E-OBS). Fora da PRT, é saltado.

Cada linha é um arquivo inteiro (``tests/unit/x.py``, que nem é importado) ou um teste
(``tests/unit/x.py::test_y``, ``tests/x.py::Classe::test_y``; vale também para as variantes
parametrizadas). Linhas em branco e iniciadas por ``#`` são comentários.
O motor (simulação, economia, ACV, decisão multicritério) NÃO está nessas listas: ele roda em
todas as edições, com o ``TritonConfig()`` cru, que traz os padrões históricos em qualquer uma.
"""

import os
import sys

import pytest

_SINONIMOS = {"POR": "PRT"}
_PASTAS = {"triton_brl": "BRL", "triton_int": "INT", "triton_prt": "PRT"}


def _edicao_da_suite() -> str:
    """A edição da suíte: TRITON_EDITION, ou a da pasta, ou BRL."""
    ed = (os.environ.get("TRITON_EDITION") or "").strip().upper()
    if not ed:
        pasta = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).lower()
        ed = _PASTAS.get(pasta, "BRL")
    return _SINONIMOS.get(ed, ed)


EDICAO = _edicao_da_suite()

# Renderização offscreen antes de qualquer importação de Qt.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# O programa lê a edição da mesma variável: a suíte e o código testado concordam.
os.environ["TRITON_EDITION"] = EDICAO
# A aba de volumetria usa o visualizador WebGL (QtWebEngine) no programa; nos
# testes, o de QPainter, que não sobe um Chromium nem depende de GPU. O WebGL é
# verificado por tests/unit/test_volumetria_web.py e pela conferência manual.
os.environ.setdefault("TRITON_VOLUMETRIA_SIMPLES", "1")

try:
    import matplotlib

    matplotlib.use("Agg")
except ImportError:  # ambiente mínimo, sem backend gráfico
    pass

try:
    from PySide6.QtWidgets import QApplication

    TEM_INTERFACE_GRAFICA = True
except ImportError:
    QApplication = None
    TEM_INTERFACE_GRAFICA = False


# Módulos que exercitam a interface desktop, direta ou indiretamente (via triton.ui).
# Mantido explícito, e não por descoberta automática, para que a exclusão de um
# módulo da execução mínima seja sempre uma decisão visível em revisão.
MODULOS_QUE_EXIGEM_INTERFACE = [
    # A suíte essencial de interface. Leva também o teste do serviço de relatórios, que não
    # testa interface mas alcança Qt por uma inversão de camadas: triton/core/report_generator.py
    # importa triton.ui.translation, que importa PySide6.QtCore. Ver docs/verificacao_e_validacao.md, §6.
    "test_essencial_interface.py",
    "integration/test_report_generator.py",
    "unit/test_tariffs_database.py",
    "unit/test_economic.py",
    "unit/test_traducao_completa.py",
    "unit/test_traducao_sem_mistura.py",
    "unit/test_o_que_se_comunica.py",
    "unit/test_figuras_sem_corte.py",
]

collect_ignore = [] if TEM_INTERFACE_GRAFICA else list(MODULOS_QUE_EXIGEM_INTERFACE)


def _base_climatica_disponivel() -> bool:
    """A base CMIP6 das 652 cidades está presente nesta instalação?

    São ~6,5 GB e 37 mil arquivos, distribuídos separadamente do código: não cabem em
    repositório. Um clone limpo — e portanto qualquer execução de integração contínua —
    não os tem.
    """
    try:
        from triton.core.climate_database import get_climate_database_dir

        return os.path.isdir(get_climate_database_dir())
    except Exception:
        return False


TEM_BASE_CLIMATICA = _base_climatica_disponivel()

#: Módulos que só fazem sentido com a base climática presente.
MODULOS_QUE_EXIGEM_BASE_CLIMATICA = [
    "unit/test_climate_database.py",
]

if not TEM_BASE_CLIMATICA:
    collect_ignore.extend(MODULOS_QUE_EXIGEM_BASE_CLIMATICA)

#: Testes avulsos, em módulos de outra natureza, que dependem da base climática.
#: Identificados pelo nome porque marcá-los exigiria editar módulos alheios ao tema.
TESTES_QUE_EXIGEM_BASE_CLIMATICA = {
    "test_national_climate_and_tariff_integration_flow",  # tests/test_essencial_interface.py
    "test_tab_project_tariff_location",
    "test_toda_cidade_ofertada_no_combo_tem_serie_climatica",
}


# --- testes que dependem de dados de uma edição só ---------------------------------------

_PASTA = os.path.dirname(os.path.abspath(__file__))
#: Nome do arquivo de lista -> a edição que tem os dados.
LISTAS_POR_EDICAO = {"so_da_brl.txt": "BRL", "so_da_prt.txt": "PRT"}


def ler_lista(nome_do_arquivo: str):
    """As entradas de uma lista (arquivo ausente = lista vazia)."""
    caminho = os.path.join(_PASTA, nome_do_arquivo)
    if not os.path.isfile(caminho):
        return []
    with open(caminho, encoding="utf-8") as f:
        linhas = [l.strip() for l in f]
    return [l for l in linhas if l and not l.startswith("#")]


def entradas_que_nao_se_aplicam(edicao: str = EDICAO):
    """Entradas das listas cujos dados esta edição não tem."""
    fora = []
    for nome, dona in LISTAS_POR_EDICAO.items():
        if edicao != dona:
            fora.extend(ler_lista(nome))
    return fora


_FORA = entradas_que_nao_se_aplicam()

# Arquivos inteiros: nem são importados (o import falharia sem os dados).
collect_ignore.extend(p[len("tests/"):] for p in _FORA if "::" not in p and p.startswith("tests/"))
_TESTES_FORA = [p for p in _FORA if "::" in p]


def _casa(nodeid: str, entrada: str) -> bool:
    """O nodeid é a entrada, um teste dentro dela (classe) ou uma variante parametrizada dela."""
    return nodeid == entrada or nodeid.startswith((entrada + "::", entrada + "["))


def pytest_collection_modifyitems(config, items):
    """Ignora, sem falhar, o que depende de dados não distribuídos com o código ou de outra edição."""
    if not TEM_BASE_CLIMATICA:
        motivo = pytest.mark.skip(
            reason="base climática CMIP6 ausente (distribuída separadamente, ~6,5 GB)"
        )
        for item in items:
            if item.name.split("[")[0] in TESTES_QUE_EXIGEM_BASE_CLIMATICA:
                item.add_marker(motivo)

    if _TESTES_FORA:
        saltados = [i for i in items
                    if any(_casa(i.nodeid.replace("\\", "/"), p) for p in _TESTES_FORA)]
        if saltados:
            config.hook.pytest_deselected(items=saltados)
            ids = {id(i) for i in saltados}
            items[:] = [i for i in items if id(i) not in ids]


def pytest_report_header(config):
    """Registra no cabeçalho a edição, qual kernel e qual stack estão sendo exercitados."""
    try:
        from triton.core import simulation

        kernel = "JIT (numba)" if simulation.HAS_NUMBA else "Python (referência)"
    except Exception:  # pragma: no cover - diagnóstico
        kernel = "indeterminado"

    interface = "Qt disponível" if TEM_INTERFACE_GRAFICA else (
        f"sem Qt — {len(MODULOS_QUE_EXIGEM_INTERFACE)} módulos de interface não coletados"
    )
    clima = "base climática presente" if TEM_BASE_CLIMATICA else "sem base climática"
    return (f"triton: edição {EDICAO} | kernel {kernel} | {interface} | {clima} | "
            f"{len(_FORA)} entradas de outra edição fora da execução")


@pytest.fixture(autouse=True)
def idioma_portugues_isolado():
    """Cada teste começa em português e não deixa idioma trocado para o seguinte.

    `set_current_lang` grava o idioma no registro do usuário (QSettings). Um teste
    que troca para inglês e falha antes de voltar deixaria os testes seguintes, e o
    próprio programa instalado, em inglês.
    """
    if not TEM_INTERFACE_GRAFICA:
        yield
        return
    from PySide6.QtCore import QSettings
    from triton.ui import translation

    gravado = QSettings("UFSC", "Triton").value("language")
    em_uso = translation._runtime_language
    translation._runtime_language = "pt"
    try:
        yield
    finally:
        translation._runtime_language = em_uso
        settings = QSettings("UFSC", "Triton")
        if gravado is None:
            settings.remove("language")
        else:
            settings.setValue("language", gravado)
        settings.sync()


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """Instância única de QApplication para os testes de interface.

    Continua `autouse` para não exigir alteração nos testes existentes, mas é
    inerte quando a stack gráfica não está presente.
    """
    if not TEM_INTERFACE_GRAFICA:
        yield None
        return

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
