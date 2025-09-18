# -*- mode: python ; coding: utf-8 -*-
"""
BupiliÇ PyInstaller Specification File
Optimized for Windows build with CustomTkinter
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.append(os.getcwd())

block_cipher = None

# ===============================================
# APPLICATION CONFIGURATION
# ===============================================
app_name = "BupiliC"
main_script = "BUPILIC_ANA_PROGRAM.py"
icon_path = "build/app_icon.ico"

# ===============================================
# DATA FILES AND DIRECTORIES
# ===============================================
datas = [
    # Application modules
    ('ISKONTO_HESABI', 'ISKONTO_HESABI'),
    ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI'),
    ('Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu'),
    ('YASLANDIRMA', 'YASLANDIRMA'),
    
    # Resources
    ('icon', 'icon'),
    
    # Optional: Include requirements if needed
    # ('requirements.txt', '.'),
]

# ===============================================
# HIDDEN IMPORTS (Explicitly include dependencies)
# ===============================================
hiddenimports = [
    # CustomTkinter and GUI
    'customtkinter',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    
    # PIL/Pillow for images
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageOps',
    'PIL.ImageFilter',
    
    # Data processing
    'pandas',
    'numpy',
    'openpyxl',
    'xlsxwriter',
    'xlrd',
    'xlwt',
    
    # Plotting and visualization
    'matplotlib',
    'matplotlib.backends',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.pyplot',
    'matplotlib.figure',
    'seaborn',
    
    # System utilities
    'psutil',
    'subprocess',
    'threading',
    'multiprocessing',
    'multiprocessing.pool',
    
    # Standard libraries that might be needed
    'json',
    'logging',
    'locale',
    'datetime',
    'os',
    'sys',
    'io',
    're',
    'csv',
    'math',
    'statistics',
    'collections',
    'itertools',
    'functools',
    'threading',
    'time',
    'calendar',
]

# ===============================================
# BINARIES (Additional binary files)
# ===============================================
binaries = []

# ===============================================
# HOOKS CONFIGURATION
# ===============================================
hookspath = []
hooksconfig = {}

# ===============================================
# RUNTIME HOOKS
# ===============================================
runtime_hooks = []

# ===============================================
# EXCLUDES (Optimize package size)
# ===============================================
excludes = [
    'test',
    'tests',
    'unittest',
    'distutils',
    'setuptools',
    'pip',
    'wheel',
    'pkg_resources',
    'email',
    'http',
    'urllib',
    'xml',
    'html',
    'asyncio',
    'sqlite3',
    'tkinter.dnd',
    'tkinter.colorchooser',
    'tkinter.commondialog',
    'tkinter.font',
    'tkinter.scrolledtext',
    'tkinter.simpledialog',
    'tkinter.tix',
    'matplotlib.tests',
    'pandas.tests',
    'numpy.tests',
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
    hookspath=hookspath,
    hooksconfig=hooksconfig,
    runtime_hooks=runtime_hooks,
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# ===============================================
# PYZ (Python ZIP archive)
# ===============================================
pyz = PYZ(
    a.pure, 
    a.zipped_data,
    cipher=block_cipher,
)

# ===============================================
# EXECUTABLE CONFIGURATION
# ===============================================
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name=app_name,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window (GUI application)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path if os.path.exists(icon_path) else None,
)

# ===============================================
# COLLECT (For one-file mode)
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
