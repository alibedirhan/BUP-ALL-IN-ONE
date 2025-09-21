# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None
project_root = Path(".").resolve()

datas = [
    (str(project_root / "icon" / "bupilic_logo.png"), "icon"),
    (str(project_root / "ISKONTO_HESABI"), "ISKONTO_HESABI"),
    (str(project_root / "KARLILIK_ANALIZI"), "KARLILIK_ANALIZI"),
    (str(project_root / "Musteri_Sayisi_Kontrolu"), "Musteri_Sayisi_Kontrolu"),
    (str(project_root / "YASLANDIRMA"), "YASLANDIRMA"),
]

hiddenimports = [
    'customtkinter',
    'tkinter',
    'tkinter.ttk',
    'PIL',
    'PIL._tkinter_finder',
    'pandas',
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'pdfplumber',
    'openpyxl',
    'psutil',
    'seaborn',
    'xlsxwriter',
    'xlrd',
    'xlwt',
    'dateutil',
    'tkcalendar',
    'customtkinter.windows.widgets.core_rendering.ctk_canvas',
    'customtkinter.windows.widgets.core_rendering.ctk_shape_renderer',
    'customtkinter.windows.widgets.core_rendering',
    'customtkinter.windows.widgets',
    'customtkinter.windows',
    'ISKONTO_HESABI',
    'ISKONTO_HESABI.main',
    'KARLILIK_ANALIZI',
    'KARLILIK_ANALIZI.main',
    'KARLILIK_ANALIZI.gui',
    'Musteri_Sayisi_Kontrolu',
    'Musteri_Sayisi_Kontrolu.main',
    'YASLANDIRMA',
    'YASLANDIRMA.main',
]

a = Analysis(
    ["BUPILIC_ANA_PROGRAM.py"],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["runtime_hook.py"],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="BupiliC",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=str(project_root / "build" / "app_icon.ico") if (project_root / "build" / "app_icon.ico").exists() else None,
)
