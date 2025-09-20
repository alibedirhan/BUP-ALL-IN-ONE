import os
import sys
import time

print("=" * 50)
print(f"🚀 Starting {os.path.basename(os.path.dirname(__file__))}")
print("=" * 50)

# FROZEN DURUMU İÇİN KRİTİK AYAR
if getattr(sys, 'frozen', False):
    print("❄️ Frozen mode detected")
    
    # 1. MEIPASS yolunu al
    base_path = sys._MEIPASS
    print(f"📦 MEIPASS: {base_path}")
    
    # 2. Programın kendi yolunu bul
    current_dir_name = os.path.basename(os.path.dirname(__file__))
    source_program_path = os.path.join(base_path, current_dir_name)
    
    # 3. Hedef yol (ana EXE ile aynı dizin)
    target_base_path = os.path.dirname(sys.executable)
    target_program_path = os.path.join(target_base_path, current_dir_name)
    
    print(f"🎯 Source: {source_program_path}")
    print(f"🎯 Target: {target_program_path}")
    
    # 4. Eğer hedefte yoksa KOPYALA
    if not os.path.exists(target_program_path):
        print("📋 Copying program files...")
        import shutil
        
        try:
            shutil.copytree(source_program_path, target_program_path)
            print("✅ Copy successful")
        except Exception as e:
            print(f"❌ Copy failed: {e}")
    
    # 5. Çalışma dizinini AYNI SEVİYEDE olacak şekilde ayarla
    os.chdir(target_program_path)
    
else:
    # Normal mod
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"📂 Working directory: {os.getcwd()}")
print(f"📄 Files here: {os.listdir('.')}")
print("=" * 50)
time.sleep(1)  # Debug için bekle

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
