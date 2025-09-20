# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import glob
from PyInstaller.building.build_main import Analysis, EXE, PYZ
from PyInstaller.building.datastruct import TOC

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[],
    binaries=[],
    datas=[
        # TÜM DOSYALARI TEK TEK EKLEYİN
        ('ISKONTO_HESABI', 'ISKONTO_HESABI'),
        ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI'),
        ('Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu'),
        ('Musteri_Sayisi_KONTROLU', 'Musteri_Sayisi_KONTROLU'),  # İki isim de olabilir
        ('YASLANDIRMA', 'YASLANDIRMA'),
        ('icon', 'icon'),
    ],
    hiddenimports=[
        # TÜM GEREKLİ MODÜLLER
        'ISKONTO_HESABI.main',
        'KARLILIK_ANALIZI.gui', 
        'Musteri_Sayisi_Kontrolu.main',
        'Musteri_Sayisi_KONTROLU.main',
        'YASLANDIRMA.main',
        'pandas', 'numpy', 'matplotlib', 'customtkinter',
        'pdfplumber', 'PIL', 'openpyxl', 'seaborn'
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
    console=True,  # DEBUG için True, sonra False yapın
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/bupilic_logo.ico' if os.path.exists('icon/bupilic_logo.ico') else None,
)

# Tüm Python dosyalarını topla - YENİ YÖNTEM
def collect_all_py_files(directory):
    py_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py') and not file.startswith('__'):
                full_path = os.path.join(root, file)
                # Temp dizinindeki yolu hesapla
                dest_path = os.path.relpath(root, '.')
                py_files.append((full_path, dest_path))
    return py_files

# Tüm alt program dosyalarını topla
all_datas = []
for module in ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_KONTROLU', 'YASLANDIRMA']:
    if os.path.exists(module):
        all_datas.extend(collect_all_py_files(module))

# Icon ve diğer dosyaları ekle
if os.path.exists('icon'):
    all_datas.append(('icon/*', 'icon'))

# Ana script analizi
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=pathex,
    binaries=[],
    datas=all_datas,  # Tüm dosyaları burada kullan
    hiddenimports=[
        # TÜM MODÜLLERİ TEK TEK EKLEYİN
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
        
        'Musteri_Sayisi_KONTROLU.main',
        'Musteri_Sayisi_KONTROLU.ui',
        'Musteri_Sayisi_KONTROLU.kurulum',
        
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
        
        # GEREKLİ KÜTÜPHANELER
        'pandas', 'numpy', 'matplotlib', 'customtkinter',
        'pdfplumber', 'PIL', 'openpyxl', 'seaborn', 
        'xlsxwriter', 'xlrd', 'xlwt', 'psutil',
        'tkcalendar', 'python-dateutil'
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/bupilic_logo.ico' if os.path.exists('icon/bupilic_logo.ico') else None,
)
