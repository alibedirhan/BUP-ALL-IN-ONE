# -*- mode: python ; coding: utf-8 -*-

# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path

project_root = Path(os.getcwd()).resolve()
block_cipher = None


block_cipher = None

# include folders as data (each tuple: source, dest)
datas = [
    (str(project_root / "icon" / "bupilic_logo.png"), "icon"),
    (str(project_root / "ISKONTO_HESABI"), "ISKONTO_HESABI"),
    (str(project_root / "KARLILIK_ANALIZI"), "KARLILIK_ANALIZI"),
    (str(project_root / "Musteri_Sayisi_Kontrolu"), "Musteri_Sayisi_Kontrolu"),
    (str(project_root / "YASLANDIRMA"), "YASLANDIRMA"),
]

# Hidden imports that pyinstaller may not detect automatically
hiddenimports = [
    "customtkinter",
    "PIL",
    # add other modules pyinstaller misses
]

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],  # entry-point
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=['runtime_hook.py'] if (project_root / 'runtime_hook.py').exists() else [],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # set to False to avoid AV false positives; set True if UPX installed and safe
    console=False,
    icon=str(project_root / "build" / "app_icon.ico") if (project_root / "build" / "app_icon.ico").exists() else None
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='BupiliC'
)

# If you want single-file (onefile), use the following instead of EXE+COLLECT:
# from PyInstaller.building import EXE, COLLECT, MERGE
# exe = EXE(pyz, a.scripts, [], exclude_binaries=True, name='BupiliC', debug=False, strip=False, upx=False, console=False)
# coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=False, name='BupiliC')
