# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_root = Path(os.getcwd()).resolve()
block_cipher = None

datas = [
    ('icon/bupilic_logo.png', 'icon'),
]

# Library assets
datas += collect_data_files('customtkinter')
datas += collect_data_files('PIL')

hiddenimports = [
    'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk', 'tkinter.commondialog',
    'PIL.ImageTk',
    'module_bootstrap',
]

# Include all Python subpackages for your sub-apps (compiled into the EXE)
for pkg in ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']:
    try:
        hiddenimports += collect_submodules(pkg)
        # If these are proper packages (contain __init__.py), this also grabs non-.py assets
        try:
            datas += collect_data_files(pkg)
        except Exception:
            pass
    except Exception:
        pass

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'] if (project_root / 'hooks').exists() else [],
    runtime_hooks=['runtime_hook.py'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # keep console true for first tests
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'build' / 'app_icon.ico') if (project_root / 'build' / 'app_icon.ico').exists() else None,
)
