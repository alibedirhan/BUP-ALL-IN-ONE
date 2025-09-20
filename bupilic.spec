# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.building.build_main import Analysis, EXE, PYZ
from PyInstaller.building.datastruct import TOC

# Ana dizin
block_cipher = None

# Tüm alt modüllerin path'lerini ekle
pathex = [
    '.',
    './ISKONTO_HESABI',
    './KARLILIK_ANALIZI', 
    './Musteri_Sayisi_Kontrolu',
    './YASLANDIRMA',
    './YASLANDIRMA/gui',
    './YASLANDIRMA/modules'
]

# Ana script analizi - BUPILIC_ANA_PROGRAM.py kullan
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],  # Ana script dosyanız
    pathex=pathex,
    binaries=[],
    datas=[
        # Tüm Python dosyalarını ve klasör yapısını dahil et
        ('ISKONTO_HESABI/**/*.py', 'ISKONTO_HESABI'),
        ('KARLILIK_ANALIZI/**/*.py', 'KARLILIK_ANALIZI'),
        ('Musteri_Sayisi_Kontrolu/**/*.py', 'Musteri_Sayisi_Kontrolu'),
        ('YASLANDIRMA/**/*.py', 'YASLANDIRMA'),
        
        # Gerekli data dosyaları
        ('*.txt', '.'),
        ('*.csv', '.'),
        ('*.json', '.'),
        ('icon/*.ico', 'icon'),
        ('icon/*.png', 'icon'),
    ],
    hiddenimports=[
        # Tüm alt modülleri belirt
        'ISKONTO_HESABI.main',
        'ISKONTO_HESABI.ui_components',
        'ISKONTO_HESABI.pdf_processor',
        'ISKONTO_HESABI.export_manager',
        
        'KARLILIK_ANALIZI.gui',
        'KARLILIK_ANALIZI.karlilik',
        'KARLILIK_ANALIZI.analiz_dashboard',
        'KARLILIK_ANALIZI.dashboard_components',
        'KARLILIK_ANALIZI.data_operations',
        'KARLILIK_ANALIZI.themes',
        'KARLILIK_ANALIZI.ui_components',
        'KARLILIK_ANALIZI.veri_analizi',
        'KARLILIK_ANALIZI.zaman_analizi',
        
        'Musteri_Sayisi_Kontrolu.main',
        'Musteri_Sayisi_Kontrolu.ui',
        'Musteri_Sayisi_Kontrolu.kurulum',
        
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
        
        # Gerekli kütüphaneler
        'pandas',
        'numpy',
        'matplotlib',
        'matplotlib.backends.backend_tkagg',
        'customtkinter',
        'pdfplumber',
        'PIL',
        'openpyxl',
        'seaborn',
        'xlsxwriter',
        'xlrd',
        'xlwt',
        'psutil',
        'tkcalendar',
        'python-dateutil',
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

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# TEK DOSYA EXE
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Final versiyonda False yapın
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'bupilic_logo.ico') if os.path.exists(os.path.join('icon', 'bupilic_logo.ico')) else None,
)
