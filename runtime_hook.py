# -*- coding: utf-8 -*-
"""
Runtime hook for PyInstaller
Ensures all dependencies are available at runtime
"""
import sys
import os

def ensure_dependencies():
    """Setup sys.path for frozen executable"""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        bundle_dir = sys._MEIPASS
        
        # Add subdirectories to path
        subdirs = [
            'ISKONTO_HESABI',
            'KARLILIK_ANALIZI', 
            'Musteri_Sayisi_Kontrolu',
            'YASLANDIRMA'
        ]
        
        for subdir in subdirs:
            subdir_path = os.path.join(bundle_dir, subdir)
            if os.path.exists(subdir_path) and subdir_path not in sys.path:
                sys.path.insert(0, subdir_path)
                print(f"Added to path: {subdir}")
    
    # Set UTF-8 encoding for Windows
    if sys.platform == 'win32':
        import locale
        import codecs
        
        # Force UTF-8 encoding
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
        
        # Set locale
        try:
            locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
        except:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass

def fix_matplotlib():
    """Fix matplotlib backend for frozen executable"""
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
    except ImportError:
        pass

# Run setup
ensure_dependencies()
fix_matplotlib()

print("Runtime hook executed successfully")
