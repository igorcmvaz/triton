"""
Configuração global do Pytest para a suíte do Netuno 5.

Garante execução headless para Qt/PySide6 e Matplotlib (Agg) e permite que a
verificação numérica do núcleo seja executada num ambiente mínimo, sem a stack
gráfica instalada.

Por que a degradação importa
----------------------------
Os testes de invariantes e propriedades científicas não dependem de interface, mas
até a versão 5.0.7 o `conftest` importava PySide6 no topo e instalava um
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
    "test_environmental_report.py",
    "test_esg_certifications.py",
    "test_pump_wizard.py",
    "test_tariffs_database.py",
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
    # Não testa interface, mas alcança Qt por uma inversão de camadas:
    # netuno/core/report_generator.py importa netuno.ui.translation, que importa
    # PySide6.QtCore. Enquanto o núcleo depender da camada de interface apenas para
    # traduzir strings, este módulo exige Qt. Ver docs/verificacao_e_validacao.md, §6.
    "unit/test_report_service.py",
]

collect_ignore = [] if TEM_INTERFACE_GRAFICA else list(MODULOS_QUE_EXIGEM_INTERFACE)


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
    return f"netuno: kernel {kernel} | {interface}"


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
