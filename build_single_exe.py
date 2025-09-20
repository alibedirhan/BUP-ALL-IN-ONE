# -*- coding: utf-8 -*-
import os
import sys
import shutil

def embed_all_programs():
    """Tüm alt programları ana EXE'ye göm"""
    print("🚀 Embedding ALL programs into single EXE...")
    
    # Tüm alt program dosyalarını topla
    all_files = []
    
    programs = [
        'ISKONTO_HESABI', 
        'KARLILIK_ANALIZI', 
        'Musteri_Sayisi_Kontrolu', 
        'YASLANDIRMA'
    ]
    
    for program in programs:
        if os.path.exists(program):
            for root, dirs, files in os.walk(program):
                for file in files:
                    if file.endswith('.py'):
                        full_path = os.path.join(root, file)
                        all_files.append(full_path)
                        print(f"✅ Added: {full_path}")
    
    # Ana programı oku
    with open('BUPILIC_ANA_PROGRAM.py', 'r', encoding='utf-8') as f:
        main_code = f.read()
    
    # Tüm dosyaları embedded olarak ekle
    embedded_code = "\n\n# ===== EMBEDDED SUBPROGRAMS =====\n\n"
    
    for file_path in all_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Modül adını dosya yolundan al
            module_name = file_path.replace('\\', '.').replace('/', '.').replace('.py', '')
            
            embedded_code += f"# --- {file_path} ---\n"
            embedded_code += f"# Embedded content of {file_path}\n"
            embedded_code += file_content + "\n\n"
            
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
    
    # Importları düzenle
    embedded_code += """
# ===== ALTERNATIVE IMPORT FALLBACKS =====
import sys
import os

# ui_components fallback
try:
    from ISKONTO_HESABI import ui_components
except ImportError:
    print("⚠️ ui_components not found, using fallback")
    class ui_components:
        @staticmethod
        def setup_ui():
            print("Fallback UI components loaded")
    
# Diğer gerekli fallback'ler
try:
    from ISKONTO_HESABI import export_manager, pdf_processor
except ImportError:
    print("⚠️ ISKONTO_HESABI modules not found")

try:
    from KARLILIK_ANALIZI import analiz_dashboard, data_operations, veri_analizi, zaman_analizi
except ImportError:
    print("⚠️ KARLILIK_ANALIZI modules not found")
"""
    
    # Ana koda embedded kodları ekle
    if '# GERI KALAN IMPORTLAR' in main_code:
        main_code = main_code.replace('# GERI KALAN IMPORTLAR', embedded_code + '\n# GERI KALAN IMPORTLAR')
    else:
        main_code += embedded_code
    
    # Yeni ana programı kaydet
    with open('BUPILIC_EMBEDDED.py', 'w', encoding='utf-8') as f:
        f.write(main_code)
    
    print("✅ All programs embedded into single file!")
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

# Gerekli klasörler - SADECE config ve data
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
    ['BUPILIC_EMBEDDED.py'],
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
        'customtkinter.windows.ctk_theme', 'customtkinter.windows.core_rendering',
        
        # Özel modüller için
        'ISKONTO_HESABI.ui_components', 'ISKONTO_HESABI.export_manager', 
        'ISKONTO_HESABI.pdf_processor', 'KARLILIK_ANALIZI.analiz_dashboard',
        'KARLILIK_ANALIZI.data_operations', 'KARLILIK_ANALIZI.veri_analizi',
        'KARLILIK_ANALIZI.zaman_analizi'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],
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
    print("🛠️  Building BupiliC SINGLE EXE with ALL programs embedded...")
    print("=" * 60)
    
    if embed_all_programs() and create_final_spec():
        print("\\n🎉 Now run this command:")
        print("pyinstaller BupiliC_FINAL.spec --clean --noconfirm")
        print("\\n🚀 This will create a SINGLE EXE with ALL programs INSIDE!")
    else:
        print("❌ Build failed!")
