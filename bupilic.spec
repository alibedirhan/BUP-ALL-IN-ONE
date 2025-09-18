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
]

# ===============================================
# HIDDEN IMPORTS (Explicitly include dependencies)
# ===============================================
hiddenimports = [
    # CustomTkinter and GUI - CRITICAL FIXES
    'customtkinter',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'tkinter.commondialog',  # Critical fix for ImportError
    
    # PIL/Pillow for images
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageOps',
    'PIL.ImageFilter',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    
    # Data processing
    'pandas',
    'pandas._libs',
    'numpy',
    'openpyxl',
    'xlsxwriter',
    'xlrd',
    'xlwt',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    
    # Plotting and visualization
    'matplotlib',
    'matplotlib.backends',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.pyplot',
    'matplotlib.figure',
    'matplotlib.axes',
    'seaborn',
    'seaborn.utils',
    'seaborn.palettes',
    
    # System utilities
    'psutil',
    'subprocess',
    'threading',
    'multiprocessing',
    'multiprocessing.pool',
    
<<<<<<< Updated upstream
    # URL and path libraries - CRITICAL FIX
=======
    # URL and path libraries
>>>>>>> Stashed changes
    'urllib',
    'urllib.request',
    'urllib.parse',
    'urllib.error',
    'pathlib',
    'importlib',
    'importlib.resources',
<<<<<<< Updated upstream
    'pkgutil',
    
    # Standard libraries that might be needed
=======
    'importlib.metadata',
    'pkgutil',
    
    # Standard libraries
>>>>>>> Stashed changes
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
    'collections.abc',
    'itertools',
    'functools',
    'time',
    'calendar',
    'base64',
    'hashlib',
    'ssl',
    'socket',
    'email',
<<<<<<< Updated upstream
=======
    'email.mime',
    'email.mime.text',
    'email.mime.multipart',
>>>>>>> Stashed changes
    'xml',
    'html',
    'zipfile',
    'tarfile',
    'gzip',
<<<<<<< Updated upstream
=======
    'shutil',
    'tempfile',
    'weakref',
    'types',
    'copy',
    'pickle',
    'shelve',
    'sqlite3',
    'glob',
    'fnmatch',
    'linecache',
    'traceback',
    'warnings',
    'abc',
    'atexit',
    'codecs',
    'contextlib',
    'operator',
    'pprint',
    'textwrap',
    'tokenize',
    'unicodedata',
>>>>>>> Stashed changes
]

# ===============================================
# BINARIES (Additional binary files)
# ===============================================
binaries = []

# ===============================================
# HOOKS CONFIGURATION
# ===============================================
<<<<<<< Updated upstream
hookspath = []
=======
hookspath = ['hooks']
>>>>>>> Stashed changes

# ===============================================
# RUNTIME HOOKS
# ===============================================
runtime_hooks = [
    'hooks/tkinter_hook.py'
]

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
<<<<<<< Updated upstream
    'tkinter.dnd',
    'tkinter.colorchooser',
    'tkinter.commondialog',
    'tkinter.font',
    'tkinter.scrolledtext',
    'tkinter.simpledialog',
    'tkinter.tix',
=======
>>>>>>> Stashed changes
    'matplotlib.tests',
    'pandas.tests',
    'numpy.tests',
    'asyncio',
<<<<<<< Updated upstream
    'sqlite3',
=======
>>>>>>> Stashed changes
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
    hooksconfig={},
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
    version_file=None,
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
