# -*- coding: utf-8 -*-
import os
import sys
import subprocess

def ensure_dependencies():
    """EXE çalıştığında bağımlılıkları kontrol et"""
    print("🔧 Checking dependencies in runtime...")
    
    # Gerekli paketler
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'PIL', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'python-dateutil', 'tkcalendar'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"⚠️ Missing packages: {missing_packages}")
        print("🚀 Attempting to install missing packages...")
        
        # Python executable'ı bul
        python_exe = sys.executable
        
        # Pip ile kurmayı dene
        for package in missing_packages:
            try:
                print(f"⬇️ Installing {package}...")
                result = subprocess.run([
                    python_exe, "-m", "pip", "install", package
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"❌ Failed to install {package}")
            except Exception as e:
                print(f"❌ Error installing {package}: {e}")
    else:
        print("🎉 All dependencies are available!")

# EXE çalıştığında bağımlılıkları kontrol et
if getattr(sys, 'frozen', False):
    ensure_dependencies()
