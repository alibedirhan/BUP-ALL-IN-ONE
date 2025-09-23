# -*- coding: utf-8 -*-
"""
ISKONTO_HESABI Ana Modül
Bu modül iskonto hesaplama uygulamasının giriş noktasıdır.
Güvenli başlatma ve hata yönetimi içerir.
"""

import tkinter as tk
from tkinter import messagebox
import logging
import sys
import traceback
import os
from datetime import datetime

# Import our UI component
try:
    from ISKONTO_HESABI.ui_components import ModernPriceCalculatorUI
except ImportError:
    try:
        from ui_components import ModernPriceCalculatorUI
    except ImportError as e:
        print(f"KRITIK HATA: UI bileşeni yüklenemedi: {e}")
        sys.exit(1)

def setup_logging():
    """
    Uygulama için loglama sistemini kur
    """
    try:
        # Log dizinini oluştur
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        
        # Log dosyası adı
        log_filename = os.path.join(log_dir, f"iskonto_hesabi_{datetime.now().strftime('%Y%m%d')}.log")
        
        # Logging konfigürasyonu
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        logger = logging.getLogger(__name__)
        logger.info("İskonto Hesaplama uygulaması başlatılıyor...")
        
        return logger
        
    except Exception as e:
        # Logging setup başarısız olursa bile uygulama çalışmalı
        print(f"UYARI: Loglama sistemi kurulamadı: {e}")
        # Fallback: Basic logging
        logging.basicConfig(level=logging.ERROR)
        return logging.getLogger(__name__)

def handle_critical_error(error, logger=None):
    """
    Kritik hataları yönet - kullanıcıya bilgi ver ve güvenli şekilde çık
    """
    error_msg = f"Kritik uygulama hatası: {str(error)}"
    
    if logger:
        logger.critical(error_msg)
        logger.critical(f"Stack trace: {traceback.format_exc()}")
    else:
        print(f"KRITIK HATA: {error_msg}")
        print(f"Detay: {traceback.format_exc()}")
    
    # Kullanıcıya hata mesajı göster
    try:
        # Tkinter window yoksa oluştur
        error_root = tk.Tk()
        error_root.withdraw()  # Ana pencereyi gizle
        
        messagebox.showerror(
            "Kritik Hata - İskonto Hesaplama", 
            f"Uygulama başlatılırken kritik bir hata oluştu:\n\n"
            f"{str(error)}\n\n"
            f"Program kapatılacak. Lütfen geliştirici ile iletişime geçin.\n"
            f"Hata detayları log dosyasına kaydedildi."
        )
        
        error_root.destroy()
        
    except Exception as display_error:
        print(f"Hata mesajı gösterilemedi: {display_error}")
    
    # Güvenli çıkış
    sys.exit(1)

def validate_system_requirements():
    """
    Sistem gereksinimlerini kontrol et
    """
    try:
        # Python versiyonu kontrolü
        if sys.version_info < (3, 8):
            raise RuntimeError(f"Python 3.8+ gerekli. Mevcut versiyon: {sys.version}")
        
        # Gerekli modüllerin yüklenip yüklenmediğini kontrol et
        required_modules = [
            'tkinter', 'pandas', 'openpyxl', 'pdfplumber', 
            'PIL', 'matplotlib', 'customtkinter'
        ]
        
        missing_modules = []
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                missing_modules.append(module)
        
        if missing_modules:
            raise RuntimeError(f"Eksik modüller: {', '.join(missing_modules)}")
            
        return True
        
    except Exception as e:
        raise RuntimeError(f"Sistem gereksinimleri kontrolü başarısız: {e}")

def create_main_window():
    try:
        if tk._default_root:
            root = tk.Toplevel(tk._default_root)
        else:
            root = tk.Tk()

        app = ModernPriceCalculatorUI(master=root)

        def on_closing():
            logging.info("Uygulama kullanıcı tarafından kapatılıyor...")
            root.quit()
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)

        return root, app  # ❗ Burası eksikti

    except Exception as e:
        raise RuntimeError(f"Ana pencere oluşturulamadı: {e}")



def main():
    """
    Ana uygulama fonksiyonu - Gelişmiş hata yönetimi ile
    """
    logger = None
    
    try:
        # 1. Loglama sistemini kur
        logger = setup_logging()
        logger.info("="*60)
        logger.info("İSKONTO HESAPLAMA UYGULAMASI BAŞLATILIYOR")
        logger.info("="*60)
        
        # 2. Sistem gereksinimlerini kontrol et
        logger.info("Sistem gereksinimleri kontrol ediliyor...")
        validate_system_requirements()
        logger.info("✓ Sistem gereksinimleri karşılandı")
        
        # 3. Ana pencereyi oluştur
        logger.info("Ana uygulama penceresi oluşturuluyor...")
        root, app = create_main_window()
        logger.info("✓ Ana pencere başarıyla oluşturuldu")
        
        # 4. Uygulamayı çalıştır
        logger.info("Uygulama kullanıcı arayüzü başlatılıyor...")
        #root.mainloop()
        
        # 5. Temizlik işlemleri
        logger.info("Uygulama normal şekilde sonlandırıldı")
        
    except KeyboardInterrupt:
        # Ctrl+C ile kapatma
        if logger:
            logger.info("Uygulama kullanıcı tarafından durduruldu (Ctrl+C)")
        print("\nUygulama kullanıcı tarafından durduruldu")
        
    except Exception as critical_error:
        # Kritik hatalar
        handle_critical_error(critical_error, logger)
        
    finally:
        # Her durumda çalışacak temizlik
        if logger:
            logger.info("Uygulama temizlik işlemleri tamamlandı")
            
        # Sistem kaynaklarını temizle
        try:
            if 'root' in locals():
                root.quit()
                root.destroy()
        except Exception:
            pass  # Zaten kapatılmış olabilir

def run_program():
    """
    Geriye uyumluluk için eski fonksiyon adı
    Bu fonksiyon ana programdan çağrılabilir
    """
    main()

# Doğrudan çalıştırma durumu
if __name__ == "__main__":
    try:
        main()
    except Exception as final_error:
        print(f"\nSON ÇARE HATA YÖNETİMİ:")
        print(f"Uygulama başlatılamadı: {final_error}")
        print("Lütfen sistem gereksinimlerini kontrol edin ve geliştirici ile iletişime geçin.")
        input("Çıkmak için Enter'a basın...")
        sys.exit(1)
