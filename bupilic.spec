# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for single EXE including all 4 sub-apps
import os
import sys
from pathlib import Path

block_cipher = None

project_root = Path(".").resolve()
app_name = "BupiliC"
main_script = "BUPILIC_ANA_PROGRAM.py"

# Data files (kept alongside the exe at runtime inside the bundle)
datas = [
    (str(project_root / "icon" / "bupilic_logo.png"), "icon"),
    (str(project_root / "ISKONTO_HESABI"), "ISKONTO_HESABI"),
    (str(project_root / "KARLILIK_ANALIZI"), "KARLILIK_ANALIZI"),
    (str(project_root / "Musteri_Sayisi_Kontrolu"), "Musteri_Sayisi_Kontrolu"),
    (str(project_root / "YASLANDIRMA"), "YASLANDIRMA"),
]

# Hidden imports to satisfy PyInstaller's static analysis due to dynamic imports
hiddenimports = [
    "customtkinter",
    "tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "PIL",
    "PIL.Image",
    "PIL.ImageTk",
    "PIL._tkinter_finder",
    "pandas",
    "numpy",
    "matplotlib",
    "matplotlib.backends.backend_tkagg",
    "pdfplumber",
    "openpyxl",
    "psutil",
    "seaborn",
    "xlsxwriter",
    "xlrd",
    "xlwt",
    "dateutil",
    "tkcalendar",
    # sub-app entry points
    "ISKONTO_HESABI",
    "ISKONTO_HESABI.main",
    "KARLILIK_ANALIZI",
    "KARLILIK_ANALIZI.main",
    "KARLILIK_ANALIZI.gui",
    "Musteri_Sayisi_Kontrolu",
    "Musteri_Sayisi_Kontrolu.main",
    "YASLANDIRMA",
    "YASLANDIRMA.main",
]

# Use our runtime hook to fix paths & matplotlib backend in frozen mode
runtime_hooks = [str(project_root / "runtime_hook.py")]

a = Analysis(
    [main_script],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=runtime_hooks,
    excludes=[
        "tests", "test", "unittest",
        "distutils", "_pytest", "pytest", "pdb", "doctest",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# One-file EXE (no COLLECT step)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=str(project_root / "build" / "app_icon.ico") if (project_root / "build" / "app_icon.ico").exists() else None,
)
