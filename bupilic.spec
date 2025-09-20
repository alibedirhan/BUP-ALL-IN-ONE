# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

block_cipher = None

# Mevcut dosyaları kontrol eden güvenli fonksiyon
def safe_glob(pattern):
    """Sadece mevcut dosyaları döndürür"""
    import glob
    files = glob.glob(pattern)
    result = []
    for file in files:
        if os.path.exists(file):
            result.append((file, '.'))
    return result

# Ana modül path'leri
pathex = [
    '.',
    'ISKONTO_HESABI',
    'KARLILIK_ANALIZI', 
    'Musteri_Sayisi_Kontrolu',
    'YASLANDIRMA',
    'YASLANDIRMA/gui',
    'YASLANDIRMA/modules'
]

# Data dosyaları - sadece mevcut olanlar
data_files = []

# Python modülleri - zorunlu
required_modules = [
    ('ISKONTO_HESABI', 'ISKONTO_HESABI'),
    ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI'),
    ('Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu'),
    ('YASLANDIRMA', 'YASLANDIRMA'),
]

for src_dir, dst_dir in required_modules:
    if os.path.exists(src_dir):
        # Python dosyalarını ekle
        for py_file in Path(src_dir).rglob('*.py'):
            rel_path = str(py_file.relative_to(src_dir))
            data_files.append((str(py_file), f'{dst_dir}/{os.path.dirname(rel_path)}' if os.path.dirname(rel_path) else dst_dir))

# Opsiyonel dosyalar - varsa ekle
optional_patterns = ['*.txt', '*.csv', '*.json', '*.ico', '*.png', '*.jpg']
for pattern in optional_patterns:
    data_files.extend(safe_glob(pattern))

# Ana PyInstaller analizi
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=pathex,
    binaries=[],
    datas=data_files,
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
        'tkinter.simpledialog',
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
        'tkcalendar',
        
        # Sistem modülleri
        'datetime',
        'os',
        'sys',
        'subprocess',
        'logging',
        'json',
        'csv',
        'sqlite3',
        'locale',
        'threading',
        'time',
        'pathlib',
        'tempfile',
        'shutil',
        'importlib',
        'platform',
        'collections',
        'itertools',
        'functools',
        'traceback',
        'warnings',
        
        # Veri işleme
        'python_dateutil',
        'pytz',
        'tzdata',
        
        # PDF işleme
        'pdfminer.six',
        'cryptography',
        'charset_normalizer',
        
        # GUI gelişmiş
        'darkdetect',
        'babel',
        
        # Matplotlib gelişmiş
        'contourpy',
        'cycler',
        'fonttools',
        'kiwisolver',
        'pyparsing',
        'packaging',
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
    [],
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
