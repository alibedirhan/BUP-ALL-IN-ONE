import sys
import os
import locale
import codecs

def ensure_dependencies():
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
                print(f"[HOOK] Added to sys.path: {subdir}")
    
    # Set UTF-8 encoding for Windows
    if sys.platform == 'win32':
        # Force UTF-8 encoding
        try:
            if sys.stdout and hasattr(sys.stdout, "buffer"):
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            if sys.stderr and hasattr(sys.stderr, "buffer"):
                sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
        except Exception as e:
            print(f"[HOOK WARNING] stdout/stderr encoding setup failed: {e}")
        
        # Set locale
        try:
            locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
        except:
            try:
                locale.setlocale(locale.LC_ALL, '')
            except:
                pass

def fix_matplotlib():
    try:
        import matplotlib
        matplotlib.use('Agg')
    except ImportError:
        pass

# Run setup
ensure_dependencies()
fix_matplotlib()

print("[HOOK] Runtime hook executed successfully")