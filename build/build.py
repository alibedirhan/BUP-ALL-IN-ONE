#!/usr/bin/env python3
"""
BupiliÇ Local Build Script
Builds Windows executable locally for testing
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from PIL import Image
import argparse
import json
from datetime import datetime

class BupilicBuilder:
    def __init__(self):
        self.app_name = "BupiliC"
        self.main_script = "bupilic_ana_program.py"
        self.build_dir = Path("build")
        self.dist_dir = Path("dist")
        self.icon_dir = Path("icon")
        
        # Colors for console output
        self.colors = {
            'RED': '\033[91m',
            'GREEN': '\033[92m', 
            'YELLOW': '\033[93m',
            'BLUE': '\033[94m',
            'MAGENTA': '\033[95m',
            'CYAN': '\033[96m',
            'WHITE': '\033[97m',
            'RESET': '\033[0m'
        }
        
    def log(self, message, color='WHITE'):
        """Colored logging"""
        if os.name == 'nt':  # Windows
            print(message)  # Windows console may not support colors
        else:
            print(f"{self.colors.get(color, '')}{message}{self.colors['RESET']}")

    def check_requirements(self):
        """Check if all required files exist"""
        self.log("🔍 Checking requirements...", 'CYAN')
        
        required_files = [
            self.main_script,
            "requirements.txt",
            "ISKONTO_HESABI",
            "KARLILIK_ANALIZI", 
            "MUSTERI_SAYISI_KONTROLU",
            "YASLANDIRMA"
        ]
        
        missing = []
        for req in required_files:
            if not Path(req).exists():
                missing.append(req)
        
        if missing:
            self.log(f"❌ Missing required files/folders: {', '.join(missing)}", 'RED')
            return False
            
        self.log("✅ All required files found", 'GREEN')
        return True

    def setup_build_environment(self):
        """Setup build directories and install dependencies"""
        self.log("🔧 Setting up build environment...", 'CYAN')
        
        # Create directories
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
        
        # Install dependencies
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "--upgrade", 
                "pip", "setuptools", "wheel"
            ], check=True)
            
            subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "pyinstaller==6.3.0", "pillow>=10.1.0"
            ], check=True)
            
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], check=True)
            
            self.log("✅ Dependencies installed", 'GREEN')
            return True
            
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to install dependencies: {e}", 'RED')
            return False

    def convert_icon(self):
        """Convert PNG to ICO format"""
        self.log("🎨 Converting icon...", 'CYAN')
        
        png_path = self.icon_dir / "bupilic_logo.png"
        ico_path = self.build_dir / "app_icon.ico"
        
        try:
            if png_path.exists():
                img = Image.open(png_path)
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')
                
                # Create multiple sizes for ICO
                sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
                icons = []
                
                for size in sizes:
                    resized = img.resize(size, Image.Resampling.LANCZOS)
                    icons.append(resized)
                
                # Save as ICO
                icons[0].save(ico_path, format='ICO', sizes=[icon.size for icon in icons])
                self.log(f"✅ Icon converted: {ico_path}", 'GREEN')
                
            else:
                self.log(f"⚠️ PNG icon not found, creating placeholder", 'YELLOW')
                # Create placeholder
                img = Image.new('RGBA', (64, 64), (42, 157, 143, 255))
                img.save(ico_path, format='ICO')
                
            return True
            
        except Exception as e:
            self.log(f"❌ Icon conversion failed: {e}", 'RED')
            return False

    def generate_spec_file(self, debug=False):
        """Generate PyInstaller spec file"""
        self.log("📝 Generating PyInstaller spec...", 'CYAN')
        
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

block_cipher = None

# Define paths
app_name = "{self.app_name}"
main_script = "{self.main_script}"
icon_path = "build/app_icon.ico"

# Data files to include
datas = [
    ('ISKONTO_HESABI', 'ISKONTO_HESABI/'),
    ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI/'),  
    ('MUSTERI_SAYISI_KONTROLU', 'MUSTERI_SAYISI_KONTROLU/'),
    ('YASLANDIRMA', 'YASLANDIRMA/'),
    ('icon', 'icon/'),
]

# Hidden imports for CustomTkinter and dependencies
hiddenimports = [
    'customtkinter',
    'customtkinter.windows',
    'customtkinter.windows.widgets',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.ttk',
    'PIL._tkinter_finder',
    'PIL.ImageTk',
    'PIL.Image',
    'pandas',
    'pandas.io.formats.excel',
    'numpy',
    'matplotlib',
    'matplotlib.backends.backend_tkagg',
    'matplotlib.figure',
    'seaborn',
    'openpyxl',
    'openpyxl.workbook',
    'xlsxwriter',
    'xlrd',
    'xlwt',
    'psutil',
    'subprocess',
    'threading',
    'json',
    'logging',
    'locale',
    'datetime',
    'os',
    'sys',
    'pathlib',
    'collections',
    'itertools',
    'functools',
]

# Analysis
a = Analysis(
    [main_script],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'test',
        'tests',
        'unittest',
        'distutils',
        'setuptools',
        '_pytest',
        'pytest',
        'doctest',
        'pdb',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove duplicate binaries and optimize
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# Create executable
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    debug={'debug'},
    bootloader_ignore_signals=False,
    strip=False,
    upx={'not debug'},
    upx_exclude=[],
    runtime_tmpdir=None,
    console={'debug'},  # Console window for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_path if Path(icon_path).exists() else None,
    version_file=None,
)
'''
        
        spec_file = self.build_dir / "app.spec"
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content.format(debug=str(debug).lower()))
        
        self.log(f"✅ Spec file generated: {spec_file}", 'GREEN')
        return spec_file

    def build_executable(self, spec_file, clean=True):
        """Build the executable using PyInstaller"""
        self.log("🔨 Building executable...", 'CYAN')
        
        cmd = [sys.executable, "-m", "PyInstaller"]
        
        if clean:
            cmd.append("--clean")
        
        cmd.extend(["--noconfirm", str(spec_file)])
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            self.log("✅ Build completed successfully", 'GREEN')
            
            # Check output
            exe_path = self.dist_dir / f"{self.app_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                self.log(f"📊 Executable size: {size_mb:.2f} MB", 'BLUE')
                return exe_path
            else:
                self.log("❌ Executable not found after build", 'RED')
                return None
                
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Build failed: {e}", 'RED')
            if e.stdout:
                self.log(f"STDOUT: {e.stdout}", 'YELLOW')
            if e.stderr:
                self.log(f"STDERR: {e.stderr}", 'RED')
            return None

    def compress_executable(self, exe_path):
        """Compress executable with UPX"""
        self.log("📦 Compressing executable...", 'CYAN')
        
        try:
            # Try to find UPX
            upx_cmd = shutil.which("upx")
            if not upx_cmd:
                self.log("⚠️ UPX not found, skipping compression", 'YELLOW')
                return exe_path
            
            original_size = exe_path.stat().st_size
            
            result = subprocess.run([
                upx_cmd, "--best", "--lzma", str(exe_path)
            ], check=True, capture_output=True, text=True)
            
            new_size = exe_path.stat().st_size
            compression_ratio = (1 - new_size / original_size) * 100
            
            self.log(f"✅ Compressed: {new_size / (1024*1024):.2f} MB ({compression_ratio:.1f}% smaller)", 'GREEN')
            return exe_path
            
        except subprocess.CalledProcessError as e:
            self.log(f"⚠️ UPX compression failed: {e}, continuing...", 'YELLOW')
            return exe_path
        except Exception as e:
            self.log(f"⚠️ Compression error: {e}", 'YELLOW')
            return exe_path

    def generate_build_info(self, exe_path, version="dev"):
        """Generate build information"""
        build_info = {
            "app_name": self.app_name,
            "version": version,
            "build_time": datetime.now().isoformat(),
            "python_version": sys.version,
            "file_size_mb": round(exe_path.stat().st_size / (1024*1024), 2),
            "file_path": str(exe_path),
            "build_machine": os.name,
            "architecture": "x64" if sys.maxsize > 2**32 else "x86"
        }
        
        info_file = exe_path.parent / "build_info.json"
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(build_info, f, indent=2, ensure_ascii=False)
        
        self.log(f"📋 Build info saved: {info_file}", 'BLUE')
        return build_info

    def test_executable(self, exe_path):
        """Quick test of the executable"""
        self.log("🧪 Testing executable...", 'CYAN')
        
        try:
            # Just check if it can start (don't wait for full GUI)
            process = subprocess.Popen([str(exe_path)], 
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE)
            
            # Wait a moment then terminate
            import time
            time.sleep(3)
            
            if process.poll() is None:  # Still running
                process.terminate()
                process.wait(timeout=5)
                self.log("✅ Executable starts successfully", 'GREEN')
                return True
            else:
                stdout, stderr = process.communicate()
                self.log(f"❌ Executable exited immediately", 'RED')
                if stderr:
                    self.log(f"Error: {stderr.decode()}", 'RED')
                return False
                
        except Exception as e:
            self.log(f"⚠️ Could not test executable: {e}", 'YELLOW')
            return False

    def build(self, version="dev", debug=False, test=True):
        """Main build process"""
        self.log(f"🚀 Starting BupiliÇ build process...", 'MAGENTA')
        self.log(f"Version: {version}, Debug: {debug}", 'BLUE')
        
        # Step 1: Check requirements
        if not self.check_requirements():
            return False
        
        # Step 2: Setup environment
        if not self.setup_build_environment():
            return False
        
        # Step 3: Convert icon
        if not self.convert_icon():
            return False
        
        # Step 4: Generate spec file
        spec_file = self.generate_spec_file(debug=debug)
        if not spec_file:
            return False
        
        # Step 5: Build executable
        exe_path = self.build_executable(spec_file)
        if not exe_path:
            return False
        
        # Step 6: Compress (release builds only)
        if not debug:
            exe_path = self.compress_executable(exe_path)
        
        # Step 7: Generate build info
        build_info = self.generate_build_info(exe_path, version)
        
        # Step 8: Test executable
        if test:
            test_success = self.test_executable(exe_path)
        
        # Final report
        self.log("\n" + "="*50, 'MAGENTA')
        self.log("🎉 BUILD COMPLETED!", 'GREEN')
        self.log(f"📁 Executable: {exe_path}", 'CYAN')
        self.log(f"📊 Size: {build_info['file_size_mb']} MB", 'BLUE')
        self.log(f"🏗️ Version: {version}", 'BLUE')
        self.log("="*50, 'MAGENTA')
        
        return exe_path

def main():
    parser = argparse.ArgumentParser(description='Build BupiliÇ Windows executable')
    parser.add_argument('--version', '-v', default='dev', help='Version string')
    parser.add_argument('--debug', '-d', action='store_true', help='Debug build')
    parser.add_argument('--no-test', action='store_true', help='Skip testing')
    parser.add_argument('--clean', '-c', action='store_true', help='Clean build directories first')
    
    args = parser.parse_args()
    
    # Clean build directories if requested
    if args.clean:
        build_dir = Path("build")
        dist_dir = Path("dist")
        if build_dir.exists():
            shutil.rmtree(build_dir)
        if dist_dir.exists():
            shutil.rmtree(dist_dir)
        print("🧹 Cleaned build directories")
    
    # Build
    builder = BupilicBuilder()
    result = builder.build(
        version=args.version,
        debug=args.debug,
        test=not args.no_test
    )
    
    if result:
        print(f"\n🎉 Success! Executable ready: {result}")
        sys.exit(0)
    else:
        print(f"\n❌ Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()