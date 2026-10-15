# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('data', 'data'), ('templates', 'templates'), ('tarifas', 'tarifas'), ('icons', 'icons'), ('triton/data', 'triton/data'), ('additional_material', 'additional_material'), ('manual/casos', 'casos'), ('examples', 'exemplos'), ('docs', 'docs'), ('manual/Manual-Triton.pdf', 'manual'), ('manual/en/Triton-User-Manual.pdf', 'manual/en'), ('manual/mini', 'manual/mini'), ('manual/site', 'manual/site')],
    hiddenimports=['PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets', 'matplotlib.backends.backend_qtagg', 'numpy', 'pandas', 'openpyxl', 'ezdxf', 'triton.core.mcdm_methods', 'triton.core.environmental_sync', 'triton.core.esg_certifications', 'triton.core.comprimento_de_serie', 'triton.core.demanda_estocastica', 'triton.ui.dialogs.dialog_comprimento_de_serie', 'triton.core.excel_scenarios', 'triton.ui.tab_economic_global_optimizer', 'triton.core.edition', 'triton.core.vigencia_tarifaria', 'triton.core.component_geometry', 'triton.core.pipe_network', 'triton.core.plant_3d', 'triton.core.schematic_3d', 'triton.core.study_layout', 'triton.core.exportar_tudo', 'triton.core.quantitativo_do_arranjo', 'triton.core.diagnostico', 'triton.core.volumetry', 'triton.core.volumetry_export', 'triton.ui.volumetry_view', 'triton.ui.volumetry_web', 'PySide6.QtWebEngineWidgets', 'PySide6.QtWebEngineCore', 'triton.ui.dialogs.pipe_runs_dialog', 'PySide6.QtSvg', 'ezdxf.render.forms', 'triton.cli', 'triton.core.modulacao_estocastica', 'triton.ui.tab_modulacao_estocastica', 'triton.ui.portugues_de_portugal', 'triton.core.base_climatica_portugal', 'triton.core.dados_do_relatorio', 'triton.ui.moeda_na_interface'],
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
    name='Triton',
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
    icon=['icons\\triton.ico'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Triton',
)
