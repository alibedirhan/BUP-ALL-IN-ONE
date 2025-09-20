import os
import sys
import traceback

def setup_environment():
    """Alt program için gerekli ortamı kurar"""
    try:
        # Frozen durumu için
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
            # Ana programın dizinini sys.path'e ekle
            if application_path not in sys.path:
                sys.path.insert(0, application_path)
        else:
            application_path = os.path.dirname(os.path.abspath(__file__))
        
        return True
        
    except Exception as e:
        print(f"Environment setup error: {e}")
        return False

# Ortamı kur
if not setup_environment():
    print("Environment setup failed!")
    input("Press Enter to exit...")
    sys.exit(1)

# BASİT VE ETKİLİ IMPORT
try:
    # Önce ana programdan yardım al
    try:
        # Ana programın modüllerini kullanmayı dene
        from BUPILIC_ANA_PROGRAM import ensure_dependencies
        ensure_dependencies()
    except:
        pass
    
    # Sonra import etmeyi dene
    import pandas as pd
    import numpy as np
    import pdfplumber
    
except ImportError as e:
    print(f"Import error: {e}")
    print("This is a frozen application. Please make sure all dependencies are included in the build.")
    print("Contact support for assistance.")
    input("Press Enter to exit...")
    sys.exit(1)

# Geri kalan importlar
from datetime import datetime, timedelta
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import logging
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns

# Geri kalan kodlar...

# Geri kalan kodlar...


import os
import sys
import traceback

try:
    # Frozen durumu için
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    
    # Gerekli modülleri yükleme hatasını yakala
    try:
        import pdfplumber
    except ImportError:
        print("ERROR: pdfplumber modülü bulunamadı!")
        print("Lütfen şu komutu çalıştırın: pip install pdfplumber")
        input("Devam etmek için Enter'a basın...")
        sys.exit(1)
        
    # Diğer importlar
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import json
    import logging
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import seaborn as sns
    
except Exception as e:
    print(f"CRITICAL ERROR: {e}")
    print(traceback.format_exc())
    input("Program kapatılacak. Enter'a basın...")
    sys.exit(1)

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

if __name__ == "__main__":
    main()
