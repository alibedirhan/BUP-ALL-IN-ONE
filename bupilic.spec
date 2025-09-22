# bupilic.spec  (tam içerik)
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
    # GUI ve alt modüller
    'tkinter', 'tkinter.ttk',
    'PIL', 'PIL._tkinter_finder',
    'matplotlib', 'matplotlib.backends.backend_tkagg',

    # Analiz ve IO
    'pandas', 'numpy', 'pdfplumber', 'openpyxl',
    'xlsxwriter', 'xlrd', 'xlwt', 'psutil', 'dateutil',
    'seaborn', 'tkcalendar',

    # Karlilik / zaman analizi ihtiyacı
    'babel', 'babel.numbers',

    # ISKONTO bağımlılıkları
    'fpdf',

    # YASLANDIRMA tarafında eksik düşebilen
    'pydoc',

    # Proje alt paketleri
    'ISKONTO_HESABI', 'ISKONTO_HESABI.main', 'ISKONTO_HESABI.ui_components',
    'KARLILIK_ANALIZI', 'KARLILIK_ANALIZI.gui', 'KARLILIK_ANALIZI.karlilik',
    'Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu.main', 'Musteri_Sayisi_Kontrolu.ui',
    'YASLANDIRMA', 'YASLANDIRMA.main', 'YASLANDIRMA.gui', 'YASLANDIRMA.gui.main_gui',
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
    console=False,  # Debug istiyorsan True yapabilirsin
    icon=str(project_root / "build" / "app_icon.ico") if (project_root / "build" / "app_icon.ico").exists() else None,
)
