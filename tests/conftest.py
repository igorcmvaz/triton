"""
Configuração global do Pytest para a suíte do Netuno 5.

Garante execução headless para Qt/PySide6 e Matplotlib (Agg) e permite que a
verificação numérica do núcleo seja executada num ambiente mínimo, sem a stack
gráfica instalada.

Por que a degradação importa
----------------------------
Os testes de invariantes e propriedades científicas não dependem de interface, mas
o `conftest` já importou PySide6 no topo e instalava um
`QApplication` com `autouse=True`. Consequência: *todo* teste, inclusive os
puramente numéricos, exigia Qt instalado. Isso impedia rodar a verificação em
contêineres mínimos de integração contínua e obrigava `--noconftest` para exercitar
os kernels acelerados num ambiente isolado com `numba`.

Sem PySide6 disponível, os módulos que dependem de interface simplesmente não são
coletados, e o restante da suíte executa normalmente.
"""

import os
import sys

import pytest

# Renderização offscreen antes de qualquer importação de Qt.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# A aba de volumetria usa o visualizador WebGL (QtWebEngine) no programa; nos
# testes, o de QPainter, que não sobe um Chromium nem depende de GPU. O WebGL é
# verificado por tests/unit/test_volumetria_web.py e pela conferência manual.
os.environ.setdefault("NETUNO_VOLUMETRIA_SIMPLES", "1")

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


# Módulos que exercitam a interface desktop, direta ou indiretamente (via netuno.ui).
# Mantido explícito, e não por descoberta automática, para que a exclusão de um
# módulo da execução mínima seja sempre uma decisão visível em revisão.
MODULOS_QUE_EXIGEM_INTERFACE = [
    "ui",
    "integration/test_national_climate_flow.py",
    "integration/test_new_tools.py",
    "integration/test_report_generator.py",
    "unit/test_environmental_report.py",
    "unit/test_esg_certifications.py",
    "unit/test_pump_wizard.py",
    "unit/test_tariffs_database.py",
    "unit/test_date_picker.py",
    "unit/test_economic.py",
    "unit/test_environmental.py",
    "unit/test_export_tab_and_exporters.py",
    "unit/test_pump_energy_details.py",
    "unit/test_tab_building_ui.py",
    "unit/test_tab_project_ui.py",
    "unit/test_tariffs_manager_tab.py",
    "unit/test_technical_only_simulation.py",
    "unit/test_topsis.py",
    "unit/test_traducao_completa.py",
    "unit/test_traducao_sem_mistura.py",
    "unit/test_o_que_se_comunica.py",
    "unit/test_figuras_sem_corte.py",
    # Não testa interface, mas alcança Qt por uma inversão de camadas:
    # netuno/core/report_generator.py importa netuno.ui.translation, que importa
    # PySide6.QtCore. Enquanto o núcleo depender da camada de interface apenas para
    # traduzir strings, este módulo exige Qt. Ver docs/verificacao_e_validacao.md, §6.
    "unit/test_report_service.py",
]

collect_ignore = [] if TEM_INTERFACE_GRAFICA else list(MODULOS_QUE_EXIGEM_INTERFACE)


def _base_climatica_disponivel() -> bool:
    """A base CMIP6 das 652 cidades está presente nesta instalação?

    São ~6,5 GB e 37 mil arquivos, distribuídos separadamente do código: não cabem em
    repositório. Um clone limpo — e portanto qualquer execução de integração contínua —
    não os tem.
    """
    try:
        from netuno.core.climate_database import get_climate_database_dir

        return os.path.isdir(get_climate_database_dir())
    except Exception:
        return False


TEM_BASE_CLIMATICA = _base_climatica_disponivel()

#: Módulos que só fazem sentido com a base climática presente.
MODULOS_QUE_EXIGEM_BASE_CLIMATICA = [
    "unit/test_climate_database.py",
    "integration/test_national_climate_flow.py",
]

if not TEM_BASE_CLIMATICA:
    collect_ignore.extend(MODULOS_QUE_EXIGEM_BASE_CLIMATICA)

#: Testes avulsos, em módulos de outra natureza, que dependem da base climática.
#: Identificados pelo nome porque marcá-los exigiria editar módulos alheios ao tema.
TESTES_QUE_EXIGEM_BASE_CLIMATICA = {
    "test_tab_project_defaults",
    "test_tab_project_tariff_location",
    "test_toda_cidade_ofertada_no_combo_tem_serie_climatica",
}


def pytest_collection_modifyitems(config, items):
    """Ignora, sem falhar, o que depende de dados não distribuídos com o código."""
    if TEM_BASE_CLIMATICA:
        return

    motivo = pytest.mark.skip(
        reason="base climática CMIP6 ausente (distribuída separadamente, ~6,5 GB)"
    )
    for item in items:
        if item.name.split("[")[0] in TESTES_QUE_EXIGEM_BASE_CLIMATICA:
            item.add_marker(motivo)


def pytest_report_header(config):
    """Registra no cabeçalho qual kernel e qual stack estão sendo exercitados."""
    try:
        from netuno.core import simulation

        kernel = "JIT (numba)" if simulation.HAS_NUMBA else "Python (referência)"
    except Exception:  # pragma: no cover - diagnóstico
        kernel = "indeterminado"

    interface = "Qt disponível" if TEM_INTERFACE_GRAFICA else (
        f"sem Qt — {len(MODULOS_QUE_EXIGEM_INTERFACE)} módulos de interface não coletados"
    )
    clima = "base climática presente" if TEM_BASE_CLIMATICA else "sem base climática"
    return f"netuno: kernel {kernel} | {interface} | {clima}"


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
    from netuno.ui import translation

    gravado = QSettings("UFSC", "Netuno5").value("language")
    em_uso = translation._runtime_language
    translation._runtime_language = "pt"
    try:
        yield
    finally:
        translation._runtime_language = em_uso
        settings = QSettings("UFSC", "Netuno5")
        if gravado is None:
            settings.remove("language")
        else:
            settings.setValue("language", gravado)
        settings.sync()


@pytest.fixture(scope="session", autouse=True)
def qapp():
    """Instância única de QApplication para os testes de interface.

    Continua `autouse` para não exigir alteração nos testes existentes, mas agora
    é inerte quando a stack gráfica não está presente.
    """
    if not TEM_INTERFACE_GRAFICA:
        yield None
        return

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    yield app
