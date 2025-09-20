import os
import sys
import time

# Önce ana programın path'ini ekle
if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if app_path not in sys.path:
    sys.path.insert(0, app_path)

# Ana programın bağımlılık yükleyicisini çalıştır
try:
    from BUPILIC_ANA_PROGRAM import ensure_all_dependencies
    ensure_all_dependencies()
except:
    pass

# Bekle ve sonra import et
time.sleep(2)  # Kurulum için biraz bekle

# BASİT IMPORT - hata olursa bile devam et
try:
    import pandas as pd
    import numpy as np
    import pdfplumber
except ImportError as e:
    print(f"Import error: {e}")
    print("Dependencies are being installed in background...")
    print("Please wait or restart the application.")
    # Hata olsa bile devam et
    pass

# Geri kalan kodlar...

# GERİ KALAN KODLARINIZ BURADAN SONRA GELMELİ


import sys
import os
import logging
from pathlib import Path

def main():
    # Türkçe karakter desteği için encoding ayarı
    if sys.platform.startswith('win'):
        try:
            import locale
            locale.setlocale(locale.LC_ALL, 'Turkish_Turkey.1254')
        except Exception as e:
            logging.warning(f"Locale ayarlanamadı: {e}")
    
    # Logging ayarları
    log_file = Path('bupilic_app.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    try:
        # UI components'i import et
        from ui_components import ModernPriceCalculatorUI
    except ImportError as e:
        logging.error(f"UI bileşenleri yüklenemedi: {e}")
        print("HATA: ui_components.py dosyası bulunamadı veya hatalı!")
        sys.exit(1)
    
    # Ana pencereyi oluştur
    root = tk.Tk()
    root.title("Bupiliç İskontolu Fiyat Hesaplayıcı v3.0")
    
    # Pencere boyutları
    root.geometry("1400x800")
    root.minsize(1200, 700)
    
    # Icon ayarı
    icon_path = Path('icon.ico')
    if icon_path.exists():
        try:
            root.iconbitmap(str(icon_path))
        except Exception as e:
            logging.warning(f"Icon yüklenemedi: {e}")
    
    # Pencereyi ortala
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    try:
        # Uygulamayı başlat
        app = ModernPriceCalculatorUI(root)
        logging.info("Bupiliç İskontolu Fiyat Hesaplayıcı v3.0 başlatıldı")
        
        # Ana döngüyü başlat
        root.mainloop()
    except Exception as e:
        logging.error(f"Uygulama başlatma hatası: {e}", exc_info=True)
        print(f"HATA: Uygulama başlatılamadı - {e}")
        sys.exit(1)
        
def main():
    print("İskonto programı başlatılıyor...")
    # Burada ISKONTO_HESABI programınızı başlatacak kodlar

if __name__ == "__main__":
    main()

