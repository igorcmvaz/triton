# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\AAAA_TEMPORARIO_AREATRABALHO\\NetunoReplicacao\\Netuno5_0_0\\main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('templates', 'templates'), ('tarifas', 'tarifas'), ('icons', 'icons'), ('netuno/data', 'netuno/data'), ('additional_material', 'additional_material'), ('manual/casos', 'casos'), ('examples', 'exemplos'), ('docs', 'docs'), ('manual/Manual-Netuno-5.pdf', 'manual'), ('manual/mini', 'manual/mini'), ('manual/site', 'manual/site')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'matplotlib.backends.backend_qtagg', 'numpy', 'pandas', 'openpyxl', 'reportlab', 'ezdxf', 'netuno.core.mcdm_methods', 'netuno.core.environmental_sync', 'netuno.core.esg_certifications', 'netuno.core.comprimento_de_serie', 'netuno.core.demanda_estocastica', 'netuno.ui.dialogs.dialog_comprimento_de_serie', 'netuno.core.excel_scenarios', 'netuno.ui.tab_economic_global_optimizer', 'netuno.core.edition', 'netuno.core.component_geometry', 'netuno.core.pipe_network', 'netuno.core.plant_3d', 'netuno.core.schematic_3d', 'netuno.core.study_layout', 'netuno.core.exportar_tudo', 'netuno.core.volumetry', 'netuno.core.volumetry_export', 'netuno.ui.volumetry_view', 'netuno.ui.volumetry_web', 'PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore', 'netuno.ui.dialogs.pipe_runs_dialog', 'PySide6.QtSvg', 'ezdxf.render.forms'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Netuno',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\AAAA_TEMPORARIO_AREATRABALHO\\NetunoReplicacao\\Netuno5_0_0\\icons\\netuno5.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Netuno',
)
