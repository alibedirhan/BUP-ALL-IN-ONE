# -*- mode: python ; coding: utf-8 -*-
"""
BUPİLİÇ - TÜM ALT PROGRAMLAR DAHİL SPEC DOSYASI
"""

import os
import sys
from pathlib import Path

block_cipher = None

# ==================== CRITICAL FIX ====================
# TÜM ALT PROGRAM DOSYALARINI AL - BU ŞEKİLDE OLMALI
def get_data_files():
    datas = []
    
    # Ana dizinler - DOĞRU FORMAT
    directories = [
        'ISKONTO_HESABI',
        'KARLILIK_ANALIZI', 
        'Musteri_Sayisi_Kontrolu',
        'YASLANDIRMA',
        'icon',
        'config',
        'data'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"📁 Adding directory: {directory}")
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # Sadece gerekli dosyaları ekle (.pyc ve cache hariç)
                    if (not file.endswith('.pyc') and 
                        '__pycache__' not in root and
                        not file.endswith('.log')):
                        
                        full_path = os.path.join(root, file)
                        # HEDEF: alt programlar ana dizinde olacak
                        target_dir = os.path.basename(root)
                        datas.append((full_path, target_dir))
    
    return datas

# ==================== ANALYSIS ====================
a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],  # Sadece ana program
    
    pathex=[os.getcwd()],  # Current directory'i ekle
    
    binaries=[],
    
    datas=get_data_files(),  # TÜM dosyaları ekle
    
    hiddenimports=[
        'customtkinter', 'pandas', 'numpy', 'matplotlib', 
        'openpyxl', 'xlsxwriter', 'xlrd', 'xlwt',
        'PIL', 'PIL.Image', 'PIL.ImageTk',
        'tkinter', 'tkinter.filedialog', 'tkinter.messagebox',
        'os', 'sys', 'subprocess', 'threading', 'json',
        'logging', 'datetime', 'shutil', 'tempfile'
    ],
    
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    
    excludes=[
        'test', 'tests', 'unittest', 'distutils', 'setuptools'
    ],
    
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ==================== PYZ ====================
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ==================== EXE ====================
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
    console=True,  # 🚨 DEBUG İÇİN ÖNCE TRUE - HATALARI GÖRELİM
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'bupilic_logo.ico') if os.path.exists(os.path.join('icon', 'bupilic_logo.ico')) else None,
)

# ==================== COLLECT ====================
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='BupiliC',
)
