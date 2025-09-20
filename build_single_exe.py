# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

def build_single_exe():
    print("🚀 Building SINGLE EXE with ALL programs...")
    
    # Tüm alt programların kodlarını oku ve birleştir
    programs = {
        'ISKONTO_HESABI': 'ISKONTO_HESABI/main.py',
        'KARLILIK_ANALIZI': 'KARLILIK_ANALIZI/gui.py', 
        'Musteri_Sayisi_Kontrolu': 'Musteri_Sayisi_Kontrolu/main.py',
        'YASLANDIRMA': 'YASLANDIRMA/main.py'
    }
    
    # Ana program kodunu oku
    with open('BUPILIC_ANA_PROGRAM.py', 'r', encoding='utf-8') as f:
        main_code = f.read()
    
    # Tüm alt program kodlarını ana programa embed et
    embedded_code = "\n\n# ===== EMBEDDED SUBPROGRAMS =====\n\n"
    
    for prog_name, prog_path in programs.items():
        if os.path.exists(prog_path):
            try:
                with open(prog_path, 'r', encoding='utf-8') as f:
                    prog_code = f.read()
                
                # Fonksiyonları değiştirerek embed et
                prog_code = prog_code.replace('if __name__ == "__main__":', 
                                            f'def run_{prog_name}():')
                prog_code = prog_code.replace('sys.exit(', 'return')
                
                embedded_code += f"# --- {prog_name} ---\n{prog_code}\n\n"
                print(f"✅ Embedded {prog_name}")
                
            except Exception as e:
                print(f"❌ Error embedding {prog_name}: {e}")
        else:
            print(f"⚠️ {prog_path} not found")
    
    # Ana koda embedded kodları ekle
    main_code = main_code.replace('# GERI KALAN IMPORTLAR', embedded_code + '\n# GERI KALAN IMPORTLAR')
    
    # Yeni ana programı kaydet
    with open('BUPILIC_SINGLE_EXE.py', 'w', encoding='utf-8') as f:
        f.write(main_code)
    
    print("✅ Single EXE source created!")
    return True

def create_final_spec():
    """Final spec dosyasını oluştur"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import os
import sys

block_cipher = None

# Tüm gerekli dosyalar
data_files = []

# Icon dosyası
if os.path.exists('icon/bupilic_logo.ico'):
    data_files.append(('icon/bupilic_logo.ico', '.'))

# Gerekli klasörler
folders = ['config', 'data', 'icon']
for folder in folders:
    if os.path.exists(folder):
        for root, dirs, files in os.walk(folder):
            for file in files:
                if not file.endswith('.pyc'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(root, os.getcwd())
                    data_files.append((full_path, rel_path))

a = Analysis(
    ['BUPILIC_SINGLE_EXE.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=data_files,
    hiddenimports=[
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'PIL', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'dateutil', 'tkcalendar',
        
        # Pillow için
        'PIL.Image', 'PIL.ImageTk', 'PIL.ImageOps', 'PIL.ImageFile',
        'PIL.JpegImagePlugin', 'PIL.PngImagePlugin', 'PIL.GifImagePlugin',
        
        # Python-dateutil için
        'dateutil.parser', 'dateutil.relativedelta', 'dateutil.tz',
        'dateutil.easter', 'dateutil.rrule',
        
        # Diğer gerekli modüller
        'pandas._libs', 'pandas.core', 'pandas.io', 'pandas.api',
        'matplotlib.backends.backend_tkagg', 'matplotlib.pyplot', 'matplotlib.figure',
        'pdfplumber.pdf', 'pdfplumber.page', 'pdfplumber.utils',
        'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk',
        'os', 'sys', 'subprocess', 'threading', 'json',
        'logging', 'datetime', 'shutil', 'tempfile', 'urllib',
        'zipfile', 'importlib', 'packaging', 'pathlib',
        'urllib.request', 'urllib.parse', 'urllib.error',
        'requests', 'socket', 'ssl', 'http', 'email',
        'ctypes', 'struct', 'hashlib', 'base64', 'binascii',
        'collections', 'itertools', 'functools', 'operator',
        're', 'math', 'statistics', 'random', 'time',
        
        # CustomTkinter için
        'customtkinter.windows.widgets', 'customtkinter.windows.ctk_tk',
        'customtkinter.windows.ctk_theme', 'customtkinter.windows.core_rendering'
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
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon/bupilic_logo.ico' if os.path.exists('icon/bupilic_logo.ico') else None,
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
'''
    
    with open('BupiliC_FINAL.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Final spec file created!")
    return True

if __name__ == "__main__":
    print("🛠️  Building BupiliC SINGLE EXE...")
    print("=" * 50)
    
    if build_single_exe() and create_final_spec():
        print("\n🎉 Now run this command:")
        print("pyinstaller BupiliC_FINAL.spec --clean --noconfirm")
        print("\n🚀 This will create a SINGLE EXE with ALL programs!")
    else:
        print("❌ Build failed!")
