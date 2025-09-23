#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BupiliÇ Single EXE Builder
Tüm alt programları içeren tek bir exe dosyası oluşturur
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
import argparse

class BupilicBuilder:
    def __init__(self, debug=False):
        self.debug = debug
        self.project_root = Path.cwd()
        self.app_name = "BupiliC"
        self.main_script = "BUPILIC_ANA_PROGRAM.py"
        self.submodules = [
            "ISKONTO_HESABI",
            "KARLILIK_ANALIZI", 
            "Musteri_Sayisi_Kontrolu",
            "YASLANDIRMA"
        ]
        
    def log(self, msg, level="INFO"):
        """Loglama fonksiyonu"""
        prefix = "🔍" if self.debug else "📦"
        if level == "ERROR":
            prefix = "❌"
        elif level == "SUCCESS":
            prefix = "✅"
        elif level == "WARNING":
            prefix = "⚠️"
        print(f"{prefix} [{level}] {msg}")
    
    def check_requirements(self):
        """Gerekli dosyaların varlığını kontrol et"""
        self.log("Checking requirements...")
        
        # Ana program kontrolü
        if not (self.project_root / self.main_script).exists():
            self.log(f"{self.main_script} not found!", "ERROR")
            return False
            
        # Alt modül kontrolü
        for module in self.submodules:
            module_path = self.project_root / module
            if not module_path.exists():
                self.log(f"Module {module} not found!", "ERROR")
                return False
            
            # __init__.py kontrolü
            init_file = module_path / "__init__.py"
            if not init_file.exists():
                self.log(f"Creating {module}/__init__.py", "WARNING")
                init_file.write_text("")
        
        # Icon kontrolü
        icon_path = self.project_root / "icon" / "bupilic_logo.png"
        if not icon_path.exists():
            self.log("Icon file not found", "WARNING")
        
        self.log("All requirements checked", "SUCCESS")
        return True
    
    def install_dependencies(self):
        """Bağımlılıkları yükle"""
        self.log("Installing dependencies...")
        
        # PyInstaller kurulumu
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pyinstaller==6.3.0"], check=True)
        
        # requirements.txt varsa yükle
        req_file = self.project_root / "requirements.txt"
        if req_file.exists():
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        
        self.log("Dependencies installed", "SUCCESS")
    
    def create_icon(self):
        """PNG'den ICO oluştur"""
        self.log("Creating icon...")
        
        png_path = self.project_root / "icon" / "bupilic_logo.png"
        ico_path = self.project_root / "build" / "app_icon.ico"
        
        # Build klasörünü oluştur
        ico_path.parent.mkdir(exist_ok=True)
        
        if png_path.exists():
            try:
                from PIL import Image
                img = Image.open(png_path)
                img.save(ico_path, format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
                self.log("Icon created", "SUCCESS")
                return str(ico_path)
            except Exception as e:
                self.log(f"Icon creation failed: {e}", "WARNING")
        
        return None
    
    def generate_spec_file(self, icon_path=None):
        """Spec dosyasını oluştur"""
        self.log("Generating spec file...")
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

block_cipher = None
project_root = Path(r"{self.project_root}").resolve()

# Tüm alt programları dahil et
datas = [
    (str(project_root / "icon" / "bupilic_logo.png"), "icon"),
'''
        
        # Alt modülleri ekle
        for module in self.submodules:
            spec_content += f'    (str(project_root / "{module}"), "{module}"),\n'
        
        spec_content += ''']

# Hidden imports
hiddenimports = [
    'customtkinter',
    'PIL',
    'PIL._tkinter_finder',
    'pandas',
    'numpy', 
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'pdfplumber',
    'openpyxl',
    'psutil',
    'seaborn',
    'xlsxwriter',
    'xlrd',
    'xlwt',
    'dateutil',
    'tkcalendar',
    'tkinter',
    'tkinter.ttk',
'''
        
        # Alt modül importlarını ekle
        for module in self.submodules:
            spec_content += f'    "{module}",\n'
            spec_content += f'    "{module}.main",\n'
        
        spec_content += f''']

# Analysis
a = Analysis(
    ['{self.main_script}'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
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
    name='{self.app_name}',
    debug={'True' if self.debug else 'False'},
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console={'True' if self.debug else 'False'},
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,'''
        
        if icon_path:
            spec_content += f"\n    icon=r'{icon_path}',"
        
        spec_content += "\n)"
        
        # Spec dosyasını kaydet
        spec_file = self.project_root / f"{self.app_name.lower()}_auto.spec"
        spec_file.write_text(spec_content, encoding='utf-8')
        
        self.log(f"Spec file generated: {spec_file}", "SUCCESS")
        return spec_file
    
    def build_exe(self, spec_file):
        """PyInstaller ile exe oluştur"""
        self.log("Building executable...")
        
        # Eski build dosyalarını temizle
        dist_dir = self.project_root / "dist"
        build_dir = self.project_root / "build"
        
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        if build_dir.exists() and (build_dir / self.app_name.lower()).exists():
            shutil.rmtree(build_dir / self.app_name.lower())
        
        # PyInstaller komutunu çalıştır
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--noconfirm",
            "--clean",
            str(spec_file)
        ]
        
        if self.debug:
            cmd.append("--log-level=DEBUG")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            self.log("Build failed!", "ERROR")
            self.log(f"Error: {result.stderr}", "ERROR")
            return False
        
        # Exe dosyasını kontrol et
        exe_path = dist_dir / f"{self.app_name}.exe"
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            self.log(f"Executable created: {exe_path} ({size_mb:.2f} MB)", "SUCCESS")
            return True
        else:
            self.log("Executable not found in dist folder", "ERROR")
            return False
    
    def test_exe(self):
        """Oluşturulan exe'yi test et"""
        exe_path = self.project_root / "dist" / f"{self.app_name}.exe"
        
        if not exe_path.exists():
            self.log("Executable not found for testing", "ERROR")
            return False
        
        self.log(f"Testing {exe_path}...")
        
        # Boyut kontrolü
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        if size_mb < 5:
            self.log(f"Warning: Executable is very small ({size_mb:.2f} MB)", "WARNING")
        
        self.log(f"Executable size: {size_mb:.2f} MB", "SUCCESS")
        return True
    
    def clean_build_files(self):
        """Build artıklarını temizle"""
        self.log("Cleaning build files...")
        
        for folder in ["build", "__pycache__", ".pytest_cache"]:
            folder_path = self.project_root / folder
            if folder_path.exists():
                shutil.rmtree(folder_path)
        
        # .pyc dosyalarını sil
        for pyc in self.project_root.rglob("*.pyc"):
            pyc.unlink()
        
        # .pyo dosyalarını sil
        for pyo in self.project_root.rglob("*.pyo"):
            pyo.unlink()
        
        self.log("Build files cleaned", "SUCCESS")
    
    def run(self):
        """Ana build işlemi"""
        self.log(f"Starting BupiliÇ build process...")
        self.log(f"Project root: {self.project_root}")
        
        # Gereksinimleri kontrol et
        if not self.check_requirements():
            return False
        
        # Bağımlılıkları yükle
        try:
            self.install_dependencies()
        except Exception as e:
            self.log(f"Dependency installation failed: {e}", "ERROR")
            return False
        
        # Icon oluştur
        icon_path = self.create_icon()
        
        # Spec dosyasını oluştur
        spec_file = self.generate_spec_file(icon_path)
        
        # Exe'yi build et
        if not self.build_exe(spec_file):
            return False
        
        # Test et
        if not self.test_exe():
            return False
        
        # Temizlik (opsiyonel)
        if not self.debug:
            self.clean_build_files()
        
        self.log("Build completed successfully!", "SUCCESS")
        self.log(f"Executable: dist/{self.app_name}.exe", "SUCCESS")
        return True


def main():
    parser = argparse.ArgumentParser(description="BupiliÇ Single EXE Builder")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--clean", action="store_true", help="Clean build files only")
    
    args = parser.parse_args()
    
    builder = BupilicBuilder(debug=args.debug)
    
    if args.clean:
        builder.clean_build_files()
    else:
        success = builder.run()
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
