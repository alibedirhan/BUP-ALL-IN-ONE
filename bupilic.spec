# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.building.build_main import Analysis, EXE, PYZ
from PyInstaller.building.datastruct import TOC, Tree

block_cipher = None

# TÜM YOLLARI EKLE
pathex = [
    os.path.dirname(os.path.abspath(__file__)),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ISKONTO_HESABI'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'KARLILIK_ANALIZI'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Musteri_Sayisi_Kontrolu'),
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'YASLANDIRMA'),
]

# TÜM DOSYALARI TOPLA - KESİN ÇÖZÜM
def get_all_data_files():
    datas = []
    
    # Tüm alt program klasörlerini ekle
    modules = ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']
    
    for module in modules:
        module_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), module)
        if os.path.exists(module_path):
            # Tüm Python dosyalarını ekle
            for root, dirs, files in os.walk(module_path):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        full_path = os.path.join(root, file)
                        # Hedef yolunu hesapla
                        dest_path = os.path.relpath(root, os.path.dirname(os.path.abspath(__file__)))
                        datas.append((full_path, dest_path))
    
    # Icon dosyalarını ekle
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon')
    if os.path.exists(icon_path):
        datas.append((icon_path, 'icon'))
    
    return datas

# ANALİZ
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=pathex,
    binaries=[],
    datas=get_all_data_files(),  # TÜM DOSYALARI EKLE
    hiddenimports=[
        # TÜM MODÜLLER
        'ISKONTO_HESABI', 'ISKONTO_HESABI.main', 'ISKONTO_HESABI.ui_components',
        'ISKONTO_HESABI.pdf_processor', 'ISKONTO_HESABI.export_manager',
        
        'KARLILIK_ANALIZI', 'KARLILIK_ANALIZI.gui', 'KARLILIK_ANALIZI.karlilik',
        'KARLILIK_ANALIZI.analiz_dashboard', 'KARLILIK_ANALIZI.dashboard_components',
        'KARLILIK_ANALIZI.data_operations', 'KARLILIK_ANALIZI.themes',
        'KARLILIK_ANALIZI.ui_components', 'KARLILIK_ANALIZI.veri_analizi',
        'KARLILIK_ANALIZI.zaman_analizi',
        
        'Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu.main',
        'Musteri_Sayisi_Kontrolu.ui', 'Musteri_Sayisi_Kontrolu.kurulum',
        
        'YASLANDIRMA', 'YASLANDIRMA.main', 'YASLANDIRMA.gui',
        'YASLANDIRMA.excel_processor', 'YASLANDIRMA.utils', 'YASLANDIRMA.setup',
        'YASLANDIRMA.gui.main_gui', 'YASLANDIRMA.gui.file_tab',
        'YASLANDIRMA.gui.analysis_tabs', 'YASLANDIRMA.gui.other_tabs',
        'YASLANDIRMA.gui.file_operations', 'YASLANDIRMA.gui.analysis_operations',
        'YASLANDIRMA.gui.tab_methods', 'YASLANDIRMA.gui.ui_helpers',
        'YASLANDIRMA.modules.analysis', 'YASLANDIRMA.modules.analysis_gui',
        'YASLANDIRMA.modules.assignment', 'YASLANDIRMA.modules.data_manager',
        'YASLANDIRMA.modules.reports', 'YASLANDIRMA.modules.visualization',
        
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
    console=False,  # Pencereli mod
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'bupilic_logo.ico') if os.path.exists(os.path.join('icon', 'bupilic_logo.ico')) else None,
)
