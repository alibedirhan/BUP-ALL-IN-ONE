# -*- coding: utf-8 -*-
import sys
import os
import locale
import codecs

def ensure_dependencies():
    # 1) LOCALE: Tk'nin 'screen distance' parse'ı bozulmasın diye NUMERIC=C
    try:
        # Saat/tarih Türkçe olabilir ama NUMERIC mutlaka C olmalı
        try:
            locale.setlocale(locale.LC_TIME, 'Turkish_Turkey.1254')
        except Exception:
            try:
                locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
            except Exception:
                pass
        # KÖK ÇÖZÜM: ondalık ayırıcıyı nokta yapan C
        locale.setlocale(locale.LC_NUMERIC, 'C')
    except Exception:
        pass

    # 2) PyInstaller bundle path
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
                print(f"[HOOK] Added to sys.path: {subdir}")

    # 3) Windows stdout/stderr UTF-8 sarmalayıcı (güvenli)
    if sys.platform == 'win32':
        try:
            if sys.stdout and hasattr(sys.stdout, "buffer"):
                sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
            if sys.stderr and hasattr(sys.stderr, "buffer"):
                sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")
        except Exception as e:
            print(f"[HOOK WARNING] stdout/stderr encoding setup failed: {e}")

def fix_matplotlib():
    # Frozen modda GUI backend açmaya çalışma
    try:
        import matplotlib
        matplotlib.use('Agg')
    except Exception:
        pass

ensure_dependencies()
fix_matplotlib()
print("[HOOK] Runtime hook executed successfully")
