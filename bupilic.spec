# -*- mode: python ; coding: utf-8 -*-

import os
import sys

# Ana dizin
block_cipher = None
MAIN_DIR = os.path.dirname(os.path.abspath(os.getcwd()))

# Tüm alt modüllerin path'lerini ekle
pathex = [
    '.',
    'ISKONTO_HESABI',
    'KARLILIK_ANALIZI', 
    'Musteri_Sayisi_Kontrolu',
    'YASLANDIRMA',
    'YASLANDIRMA/gui',
    'YASLANDIRMA/modules'
]

# Ana script analizi
a = Analysis(
    ['main.py'],  # Ana script dosyanız
    pathex=pathex,
    binaries=[],
    datas=[
        # Tüm Python dosyalarını dahil et
        ('ISKONTO_HESABI/*.py', 'ISKONTO_HESABI'),
        ('KARLILIK_ANALIZI/*.py', 'KARLILIK_ANALIZI'),
        ('Musteri_Sayisi_Kontrolu/*.py', 'Musteri_Sayisi_Kontrolu'),
        ('YASLANDIRMA/*.py', 'YASLANDIRMA'),
        ('YASLANDIRMA/gui/*.py', 'YASLANDIRMA/gui'),
        ('YASLANDIRMA/modules/*.py', 'YASLANDIRMA/modules'),
        
        # Eğer varsa data dosyaları
        ('*.txt', '.'),
        ('*.csv', '.'),
        ('*.json', '.'),
        ('*.ico', '.'),
        ('*.png', '.'),
        ('*.jpg', '.'),
    ],
    hiddenimports=[
        # Tüm alt modülleri belirt
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
        
        # Temel kütüphaneler
        'pandas',
        'numpy',
        'matplotlib',
        'matplotlib.pyplot',
        'matplotlib.figure',
        'matplotlib.backends.backend_tkagg',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'customtkinter',
        'openpyxl',
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
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Gereksiz dosyaları temizle
a.binaries = [x for x in a.binaries if not x[0].startswith('tcl')]
a.binaries = [x for x in a.binaries if not x[0].startswith('tk')]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# TEK DOSYA EXE - Bu kısım çok önemli!
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Bupilic_Yonetim_Sistemi',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Debug için True yapın, sonra False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
