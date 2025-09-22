# -*- coding: utf-8 -*-
"""
Runtime hook for PyInstaller
Ensures all dependencies are available at runtime (e.g. sys.path, matplotlib, stdout)
"""

import sys
import os
import locale
import codecs

def ensure_dependencies():
    """Setup sys.path and encoding for frozen executable"""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle path
        bundle_dir = sys._MEIPASS

        # Add subdirectories to path (alt program klasörleri)
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
                print(f"[HOOK] Added to sys.path: {subdir}")

    # UTF-8 encoding fix (Windows)
    if sys.platform == 'win32':
        try:
            if sys.stdout and hasattr(sys.stdout, "buffer"):
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            if sys.stderr and hasattr(sys.stderr, "buffer"):
                sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
        except Exception as e:
            print(f"[HOOK WARNING] stdout/stderr encoding setup failed: {e}")

        # Locale ayarı
        try:
            locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
        except:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass

def fix_matplotlib():
    """Use non-interactive backend in frozen mode"""
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ImportError:
        pass

# Çalıştır
ensure_dependencies()
fix_matplotlib()
print("[HOOK] Runtime hook executed successfully")
