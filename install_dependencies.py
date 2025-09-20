#!/usr/bin/env python3
"""
BupiliC - Otomatik Bağımlılık Yükleyici
"""

import sys
import subprocess
import importlib
from packaging import version

def install_dependencies():
    """Tüm gerekli bağımlılıkları yükler"""
    
    required_packages = {
        'customtkinter': '5.2.2',
        'pandas': '2.1.4',
        'numpy': '1.24.3',
        'matplotlib': '3.7.2',
        'pdfplumber': '0.10.3',
        'openpyxl': '3.1.2',
        'psutil': '5.9.6',
        'Pillow': '10.1.0',
        'seaborn': '0.13.2',
        'xlsxwriter': '3.1.9',
        'xlrd': '2.0.1',
        'xlwt': '1.3.0',
        'python-dateutil': '2.8.2',
        'tkcalendar': '1.6.1'
    }
    
    print("📦 BupiliC Bağımlılık Yükleyici")
    print("=" * 40)
    
    success = True
    
    for package, required_version in required_packages.items():
        try:
            # Modülü kontrol et
            mod = importlib.import_module(package)
            if hasattr(mod, '__version__'):
                current_version = mod.__version__
                if version.parse(current_version) >= version.parse(required_version):
                    print(f"✅ {package} {current_version} (zaten yüklü)")
                    continue
            
            # Yükleme gerekiyor
            print(f"⬇️  {package}>={required_version} yükleniyor...")
            
            # pip ile yükle
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                f"{package}>={required_version}"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} başarıyla yüklendi")
            else:
                print(f"❌ {package} yükleme hatası: {result.stderr}")
                success = False
                
        except ImportError:
            # Modül yüklü değil, yükle
            print(f"⬇️  {package}>={required_version} yükleniyor...")
            
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                f"{package}>={required_version}"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package} başarıyla yüklendi")
            else:
                print(f"❌ {package} yükleme hatası: {result.stderr}")
                success = False
        except Exception as e:
            print(f"❌ {package} kontrol hatası: {e}")
            success = False
    
    return success

if __name__ == "__main__":
    try:
        success = install_dependencies()
        if success:
            print("\n🎉 Tüm bağımlılıklar başarıyla yüklendi!")
            sys.exit(0)
        else:
            print("\n⚠️  Bazı bağımlılıklar yüklenemedi!")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")
        sys.exit(1)
