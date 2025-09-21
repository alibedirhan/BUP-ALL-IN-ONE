# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.building.build_main import Analysis, EXE, PYZ

# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# EN BASİT ve ETKİLİ YOL - TÜM DOSYALARI EKLE
datas = [
    ('ISKONTO_HESABI', 'ISKONTO_HESABI'),
    ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI'),
    ('Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu'),
    ('YASLANDIRMA', 'YASLANDIRMA'),
    ('icon', 'icon'),
]

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # SADECE ANA MODÜLLER
        'ISKONTO_HESABI.main',
        'KARLILIK_ANALIZI.gui',
        'Musteri_Sayisi_Kontrolu.main', 
        'YASLANDIRMA.main',
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
    console=True,  # DEBUG İÇİN TRUE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/bupilic_logo.ico',
)

# MEVCUT DİZİN
current_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

# TÜM YOLLARI EKLE
pathex = [
    current_dir,
    os.path.join(current_dir, 'ISKONTO_HESABI'),
    os.path.join(current_dir, 'KARLILIK_ANALIZI'),
    os.path.join(current_dir, 'Musteri_Sayisi_Kontrolu'),
    os.path.join(current_dir, 'YASLANDIRMA'),
]

# TÜM DOSYALARI TOPLA - BASİT ve ETKİLİ YÖNTEM
datas = []

# Tüm alt program klasörlerini ekle
modules = ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']
for module in modules:
    module_dir = os.path.join(current_dir, module)
    if os.path.exists(module_dir):
        datas.append((module_dir, module))

# Icon klasörünü ekle
icon_dir = os.path.join(current_dir, 'icon')
if os.path.exists(icon_dir):
    datas.append((icon_dir, 'icon'))

# ANALİZ
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=pathex,
    binaries=[],
    datas=datas,
    hiddenimports=[
        # TÜM MODÜLLER
        'ISKONTO_HESABI.main', 'ISKONTO_HESABI.ui_components',
        'ISKONTO_HESABI.pdf_processor', 'ISKONTO_HESABI.export_manager',
        
        'KARLILIK_ANALIZI.gui', 'KARLILIK_ANALIZI.karlilik',
        'KARLILIK_ANALIZI.analiz_dashboard', 'KARLILIK_ANALIZI.dashboard_components',
        'KARLILIK_ANALIZI.data_operations', 'KARLILIK_ANALIZI.themes',
        'KARLILIK_ANALIZI.ui_components', 'KARLILIK_ANALIZI.veri_analizi',
        'KARLILIK_ANALIZI.zaman_analizi',
        
        'Musteri_Sayisi_Kontrolu.main', 'Musteri_Sayisi_Kontrolu.ui', 
        'Musteri_Sayisi_Kontrolu.kurulum',
        
        'YASLANDIRMA.main', 'YASLANDIRMA.gui', 'YASLANDIRMA.excel_processor', 
        'YASLANDIRMA.utils', 'YASLANDIRMA.setup',
        
        # KÜTÜPHANELER
        'pandas', 'numpy', 'matplotlib', 'customtkinter',
        'pdfplumber', 'PIL', 'openpyxl', 'seaborn',
        'tkcalendar', 'python-dateutil', 'psutil'
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

# EXE OLUŞTUR - TEK DOSYA
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
    console=True,  # DEBUG için True
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'bupilic_logo.ico') if os.path.exists(os.path.join('icon', 'bupilic_logo.ico')) else None,
)
