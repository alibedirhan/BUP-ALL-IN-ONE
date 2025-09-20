# -*- mode: python ; coding: utf-8 -*-

# BU SPEC DOSYASI TÜM BAĞIMLILIKLARI GARANTILI ŞEKILDE TEK EXE'YE PAKETLER
# KULLANICI HIÇBIR ŞEY YÜKLEMEZ, SADECE ÇIFT TIKLAR

import os
import sys

block_cipher = None

# Tüm modül path'leri
pathex = [
    '.',
    'ISKONTO_HESABI',
    'KARLILIK_ANALIZI', 
    'Musteri_Sayisi_Kontrolu',
    'YASLANDIRMA',
    'YASLANDIRMA/gui',
    'YASLANDIRMA/modules'
]

# Ana analiz - TÜM BAĞIMLILIKLAR DAHİL
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=pathex,
    binaries=[],
    datas=[
        # Python modülleri
        ('ISKONTO_HESABI/*.py', 'ISKONTO_HESABI'),
        ('KARLILIK_ANALIZI/*.py', 'KARLILIK_ANALIZI'),
        ('Musteri_Sayisi_Kontrolu/*.py', 'Musteri_Sayisi_Kontrolu'),
        ('YASLANDIRMA/*.py', 'YASLANDIRMA'),
        ('YASLANDIRMA/gui/*.py', 'YASLANDIRMA/gui'),
        ('YASLANDIRMA/modules/*.py', 'YASLANDIRMA/modules'),
        
        # Data dosyaları (varsa)
        ('*.txt', '.'),
        ('*.csv', '.'),
        ('*.json', '.'),
        ('*.ico', '.'),
        ('*.png', '.'),
        ('*.jpg', '.'),
    ],
    hiddenimports=[
        # Ana modüller
        'ISKONTO_HESABI',
        'ISKONTO_HESABI.main',
        'ISKONTO_HESABI.ui_components',
        'ISKONTO_HESABI.pdf_processor',
        'ISKONTO_HESABI.export_manager',
        
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
        'Musteri_Sayisi_Kontrolu.ui',
        'Musteri_Sayisi_Kontrolu.kurulum',
        
        'YASLANDIRMA',
        'YASLANDIRMA.main',
        'YASLANDIRMA.gui',
        'YASLANDIRMA.excel_processor',
        'YASLANDIRMA.utils',
        'YASLANDIRMA.setup',
        'YASLANDIRMA.gui.main_gui',
        'YASLANDIRMA.gui.file_tab',
        'YASLANDIRMA.gui.analysis_tabs',
        'YASLANDIRMA.gui.other_tabs',
        'YASLANDIRMA.gui.file_operations',
        'YASLANDIRMA.gui.analysis_operations',
        'YASLANDIRMA.gui.tab_methods',
        'YASLANDIRMA.gui.ui_helpers',
        'YASLANDIRMA.modules.analysis',
        'YASLANDIRMA.modules.analysis_gui',
        'YASLANDIRMA.modules.assignment',
        'YASLANDIRMA.modules.data_manager',
        'YASLANDIRMA.modules.reports',
        'YASLANDIRMA.modules.visualization',
        
        # TÜM BAĞIMLILIKLAR ZORUNLU
        'pandas',
        'numpy',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'matplotlib.backends',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.simpledialog',
        'customtkinter',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'pdfplumber',
        'PIL',
        'PIL.Image',
        'PIL.ImageTk',
        'seaborn',
        'xlsxwriter',
        'xlrd',
        'xlwt',
        'psutil',
        'datetime',
        'os',
        'sys',
        'subprocess',
        'logging',
        'json',
        'csv',
        'sqlite3',
        'tkcalendar',
        'locale',
        'threading',
        'time',
        'pathlib',
        'tempfile',
        'shutil',
        'importlib',
        
        # PDF ve Excel için ekstra
        'pdfminer',
        'pdfminer.six',
        'cryptography',
        'charset_normalizer',
        'python_dateutil',
        'pytz',
        'tzdata',
        
        # CustomTkinter için ekstra
        'darkdetect',
        
        # Matplotlib için ekstra
        'contourpy',
        'cycler',
        'fonttools',
        'kiwisolver',
        'pyparsing',
        
        # Windows için ekstra
        'win32api',
        'win32con',
        'win32gui',
        'pywintypes',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Gereksizleri hariç tut
        'FixTk',
        'tcl',
        'tk',
        '_tkinter',
        'test',
        'unittest',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Python bytecode'u paketleme
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# TEK DOSYA EXE - HİÇBİR BAĞIMLILIK KALMASIN
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # GUI aplikasyon
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
