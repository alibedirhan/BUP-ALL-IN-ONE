# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, Tree

project_root = Path(os.getcwd()).resolve()
block_cipher = None

datas = [
    ('icon/bupilic_logo.png', 'icon'),
]
# Bundle submodules completely
for sub in ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']:
    if (project_root / sub).exists():
        datas.append(Tree(str(project_root / sub), prefix=sub))

# Library assets
datas += collect_data_files('customtkinter')
datas += collect_data_files('PIL')

hiddenimports = [
    'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk', 'tkinter.commondialog',
    'PIL.ImageTk',
    'module_bootstrap',  # ensure our bootstrap is packed
]

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'] if (project_root / 'hooks').exists() else [],
    runtime_hooks=['runtime_hook.py'],  # tkinter hook is best-effort; optional
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
    console=True,  # keep console during tests to see stacktraces
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / 'build' / 'app_icon.ico') if (project_root / 'build' / 'app_icon.ico').exists() else None,
)
