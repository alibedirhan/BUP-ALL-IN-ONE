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
        bundle_dir = sys._MEIPASS

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

        try:
            if sys.stdout and hasattr(sys.stdout, "buffer"):
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            if sys.stderr and hasattr(sys.stderr, "buffer"):
                sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
        except Exception as e:
            print(f"[HOOK] stdout/stderr encoding ayarlanamadı: {e}")

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

ensure_dependencies()
fix_matplotlib()
print("Runtime hook executed successfully")
