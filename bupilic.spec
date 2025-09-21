# bupilic.spec
# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

project_root = Path(os.getcwd()).resolve()
block_cipher = None

# Tüm alt programları ve icon'u dahil et
datas = [
    (str(project_root / "icon" / "bupilic_logo.png"), "icon"),
    (str(project_root / "ISKONTO_HESABI"), "ISKONTO_HESABI"),
    (str(project_root / "KARLILIK_ANALIZI"), "KARLILIK_ANALIZI"),
    (str(project_root / "Musteri_Sayisi_Kontrolu"), "Musteri_Sayisi_Kontrolu"),
    (str(project_root / "YASLANDIRMA"), "YASLANDIRMA"),
]

# Gerekli tüm modülleri dahil et
hiddenimports = [
    'customtkinter',
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
    'tkinter',
    'tkinter.ttk',
    # Alt programların modüllerini ekle
    'ISKONTO_HESABI',
    'ISKONTO_HESABI.main',
    'ISKONTO_HESABI.export_manager',
    'ISKONTO_HESABI.pdf_processor',
    'ISKONTO_HESABI.ui_components',
    'KARLILIK_ANALIZI',
    'KARLILIK_ANALIZI.gui',
    'KARLILIK_ANALIZI.karlilik',
    'KARLILIK_ANALIZI.analiz_dashboard',
    'KARLILIK_ANALIZI.dashboard_components',
    'KARLILIK_ANALIZI.data_operations',
    'KARLILIK_ANALIZI.themes',
    'KARLILIK_ANALIZI.ui_components',
    'KARLILIK_ANALIZI.veri_analizi',
    'KARLILIK_ANALIZI.zaman_analizi',
    'Musteri_Sayisi_Kontrolu',
    'Musteri_Sayisi_Kontrolu.main',
    'Musteri_Sayisi_Kontrolu.kurulum',
    'Musteri_Sayisi_Kontrolu.ui',
    'YASLANDIRMA',
    'YASLANDIRMA.main',
    'YASLANDIRMA.gui',
    'YASLANDIRMA.gui.main_gui',
    'YASLANDIRMA.excel_processor',
    'YASLANDIRMA.utils',
    'YASLANDIRMA.modules',
    'YASLANDIRMA.modules.analysis',
    'YASLANDIRMA.modules.analysis_gui',
    'YASLANDIRMA.modules.assignment',
    'YASLANDIRMA.modules.data_manager',
    'YASLANDIRMA.modules.reports',
    'YASLANDIRMA.modules.visualization',
]

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[
        str(project_root),
        str(project_root / 'ISKONTO_HESABI'),
        str(project_root / 'KARLILIK_ANALIZI'),
        str(project_root / 'Musteri_Sayisi_Kontrolu'),
        str(project_root / 'YASLANDIRMA'),
    ],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[str(project_root / 'hooks')] if (project_root / 'hooks').exists() else [],
    runtime_hooks=['runtime_hook.py'] if (project_root / 'runtime_hook.py').exists() else [],
    excludes=[
        'test',
        'tests',
        'unittest',
        'email',
        'http',
        'xml',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher,
)

# TEK DOSYA (ONEFILE) BUILD
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI app - konsol penceresi gösterme
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(project_root / "build" / "app_icon.ico") if (project_root / "build" / "app_icon.ico").exists() else None,
)
