# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

block_cipher = None
base_dir = Path(SPECPATH) if "SPECPATH" in globals() else Path.cwd()

datas = [
    (str(base_dir / 'data'), 'data'),
    (str(base_dir / 'templates'), 'templates'),
    (str(base_dir / 'tarifas'), 'tarifas'),
    (str(base_dir / 'icons'), 'icons'),
    (str(base_dir / 'netuno' / 'data'), 'netuno/data'),
    (str(base_dir / 'additional_material'), 'additional_material'),
    (str(base_dir / 'integrations'), 'integrations'),
]

# Filtra apenas diretórios existentes para evitar avisos
datas = [(src, dst) for src, dst in datas if os.path.exists(src)]

hiddenimports = [
    'PySide6.QtCore',
    'PySide6.QtGui',
    'PySide6.QtWidgets',
    'matplotlib.backends.backend_qtagg',
    'numpy',
    'pandas',
    'openpyxl',
    'reportlab',
    'ezdxf',
    'netuno.core.mcdm_methods',
    'netuno.core.environmental_sync',
    'netuno.core.esg_certifications',
]

a = Analysis(
    ['main.py'],
    pathex=[str(base_dir)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

icon_file = str(base_dir / 'icons' / 'icon.ico') if os.path.exists(base_dir / 'icons' / 'icon.ico') else None

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
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Netuno',
)
