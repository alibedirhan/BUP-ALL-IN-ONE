# -*- mode: python ; coding: utf-8 -*-

import os
import sys

block_cipher = None

# Ana dizinler
directories = [
    'ISKONTO_HESABI',
    'KARLILIK_ANALIZI', 
    'Musteri_Sayisi_Kontrolu',
    'YASLANDIRMA',
    'icon',
    'config',
    'data'
]

def get_data_files():
    datas = []
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    if not file.endswith('.pyc') and '__pycache__' not in root:
                        full_path = os.path.join(root, file)
                        target_dir = os.path.join('.', os.path.relpath(root, os.getcwd()))
                        datas.append((full_path, target_dir))
    
    # Ek olarak requirements.txt ve diğer gerekli dosyaları ekle
    additional_files = ['requirements.txt', 'README.md']
    for file in additional_files:
        if os.path.exists(file):
            datas.append((file, '.'))
    
    return datas

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=get_data_files(),
    hiddenimports=[
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'Pillow', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'python-dateutil', 'tkcalendar',
        'pandas._libs', 'pandas.core', 'pandas.io', 'pandas.api',
        'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot', 'matplotlib.figure',
        'pdfplumber.pdf', 'pdfplumber.page', 'pdfplumber.utils',
        'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk',
        'PIL', 'PIL.Image', 'PIL.ImageTk', 'PIL.ImageOps',
        'os', 'sys', 'subprocess', 'threading', 'json',
        'logging', 'datetime', 'shutil', 'tempfile', 'urllib',
        'zipfile', 'importlib', 'packaging', 'pathlib',
        'urllib.request', 'urllib.parse', 'urllib.error',
        'requests', 'socket', 'ssl', 'http', 'email',
        'ctypes', 'struct', 'hashlib', 'base64', 'binascii',
        'collections', 'itertools', 'functools', 'operator',
        're', 'math', 'statistics', 'random', 'time'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['test', 'tests', 'unittest'],
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
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Hata görüntülemek için True yap, sonra False yapabilirsin
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join('icon', 'bupilic_logo.ico') if os.path.exists(os.path.join('icon', 'bupilic_logo.ico')) else None,
)

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
