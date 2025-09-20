# -*- mode: python ; coding: utf-8 -*-
"""
BupiliÇ PyInstaller Specification File - OPTIMIZED VERSION
"""

import sys
import os
from pathlib import Path

block_cipher = None

# ===============================================
# APPLICATION CONFIGURATION
# ===============================================
app_name = "BupiliC"
main_script = "BUPILIC_ANA_PROGRAM.py"
icon_path = "build/app_icon.ico"

# ===============================================
# DATA FILES AND DIRECTORIES - CRITICAL FIX
# ===============================================
def get_data_files():
    """Tüm alt programları ve dosyalarını recursive olarak topla"""
    datas = []
    
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
    
    for directory in directories:
        if os.path.exists(directory):
            for root, dirs, files in os.walk(directory):
                for file in files:
                    # .pyc ve __pycache__ dosyalarını hariç tut
                    if not file.endswith('.pyc') and '__pycache__' not in root:
                        full_path = os.path.join(root, file)
                        # PyInstaller formatı: (kaynak, hedef_klasör)
                        target_path = os.path.dirname(full_path)
                        datas.append((full_path, target_path))
    
    return datas

datas = get_data_files()

# ===============================================
# HIDDEN IMPORTS - OPTIMIZED
# ===============================================
hiddenimports = [
    # Core dependencies
    'customtkinter', 'tkinter', 'PIL', 'pandas', 'numpy', 'matplotlib',
    
    # Tkinter submodules - CRITICAL
    'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk', 
    'tkinter.commondialog', 'tkinter.constants',
    
    # PIL submodules
    'PIL.Image', 'PIL.ImageTk', 'PIL.ImageOps', 'PIL.ImageFilter',
    
    # Pandas submodules  
    'pandas._libs', 'pandas.core', 'pandas.io',
    
    # Matplotlib submodules
    'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot',
    
    # Other required
    'openpyxl', 'xlsxwriter', 'xlrd', 'xlwt', 'psutil', 'seaborn',
    
    # Standard libs that might be missing
    'logging', 'json', 'locale', 'datetime', 'os', 'sys', 'subprocess',
    'threading', 'pathlib', 'shutil', 'tempfile'
]

# ===============================================
# BINARIES
# ===============================================
binaries = []

# ===============================================
# EXCLUDES (Size optimization)
# ===============================================
excludes = [
    'test', 'tests', 'unittest', 'distutils', 'setuptools', 'pip', 'wheel',
    'pkg_resources', 'matplotlib.tests', 'pandas.tests', 'numpy.tests',
    'asyncio', 'email', 'xml', 'html', 'http', 'urllib3',
]

# ===============================================
# ANALYSIS
# ===============================================
a = Analysis(
    [main_script],
    pathex=[os.getcwd()],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ===============================================
# PYZ
# ===============================================
pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher,
)

# ===============================================
# EXECUTABLE CONFIGURATION - WINDOWED MODE
# ===============================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
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
    icon=icon_path if os.path.exists(icon_path) else None,
)

# ===============================================
# COLLECT (For one-dir mode - RECOMMENDED)
# ===============================================
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=app_name,
)