# -*- coding: utf-8 -*-
"""
ISKONTO_HESABI Ana Modül
Bu modül iskonto hesaplama uygulamasının giriş noktasıdır.
Güvenli başlatma ve hata yönetimi içerir. (Gömülü mod uyumlu)
"""

import tkinter as tk
from tkinter import messagebox
import logging
import sys
import traceback
import os
from datetime import datetime

# UI bileşeni
try:
    from ISKONTO_HESABI.ui_components import ModernPriceCalculatorUI
except ImportError:
    try:
        from ui_components import ModernPriceCalculatorUI
    except ImportError as e:
        # Gömülü modda sys.exit() KULLANMA!
        raise ImportError(f"UI bileşeni yüklenemedi: {e}") from e


def setup_logging():
    """Uygulama için loglama sistemini kur"""
    try:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_filename = os.path.join(log_dir, f"iskonto_hesabi_{datetime.now().strftime('%Y%m%d')}.log")

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.FileHandler(log_filename, encoding='utf-8'),
                      logging.StreamHandler(sys.stdout)]
        )
        logger = logging.getLogger(__name__)
        logger.info("İskonto Hesaplama uygulaması başlatılıyor...")
        return logger
    except Exception as e:
        print(f"UYARI: Loglama sistemi kurulamadı: {e}")
        logging.basicConfig(level=logging.ERROR)
        return logging.getLogger(__name__)


def handle_critical_error(error, logger=None):
    """Kritik hataları yönet (gömülü modda process'i öldürmeden!)"""
    error_msg = f"Kritik uygulama hatası: {str(error)}"

    if logger:
        logger.critical(error_msg)
        logger.critical("Stack trace:", exc_info=True)
    else:
        print(f"KRITIK HATA: {error_msg}")
        traceback.print_exc()

    # Kullanıcıya göster
    try:
        # Tk context varsa basit bir mesaj kutusu göster
        if tk._default_root:
            messagebox.showerror("Kritik Hata - İskonto Hesaplama",
                                 f"Uygulama başlatılırken hata oluştu:\n\n{error}\n\n"
                                 f"Detaylar log dosyasına kaydedildi.")
    except Exception:
        pass

    # Gömülü modda sys.exit() **YAPMA** – ana uygulamayı düşürür.
    # Bunun yerine exception fırlat ki ana program yakalasın.
    raise RuntimeError(error_msg)


def validate_system_requirements():
    """Sistem gereksinimlerini kontrol et"""
    if sys.version_info < (3, 8):
        raise RuntimeError(f"Python 3.8+ gerekli. Mevcut: {sys.version}")

    required = ['tkinter', 'pandas', 'openpyxl', 'pdfplumber', 'PIL', 'matplotlib', 'customtkinter']
    missing = []
    for m in required:
        try:
            __import__(m)
        except ImportError:
            missing.append(m)
    if missing:
        raise RuntimeError(f"Eksik modüller: {', '.join(missing)}")
    return True


def create_main_window():
    """
    Pencereyi oluştur.
    - Ana program (CTk) açıksa: Toplevel oluştur ve ana root’a bağla.
    - Tek başına çalıştırılıyorsa: Tk() root oluştur.
    """
    # Gömülü mü? (ana programda zaten bir Tk/CTk root var mı?)
    embedded = tk._default_root is not None

    if embedded:
        root = tk.Toplevel(tk._default_root)
        # Ana pencere üstüne otursun ve kapatırken sadece kendini kapatsın
        root.transient(tk._default_root)
        root.title("Bupiliç İskontolu Fiyat Hesaplayıcı")
    else:
        root = tk.Tk()
        root.title("Bupiliç İskontolu Fiyat Hesaplayıcı")

    app = ModernPriceCalculatorUI(master=root)

    def on_closing():
        logging.info("İskonto penceresi kapatılıyor...")
        # Sadece kendi penceresini kapat
        try:
            root.destroy()
        except Exception:
            pass

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # embedded flag'i de geri dön
    return root, app, embedded


def main():
    """Ana uygulama (gömülü mod uyumlu)"""
    logger = setup_logging()
    logger.info("=" * 60)
    logger.info("İSKONTO HESAPLAMA UYGULAMASI BAŞLATILIYOR")
    logger.info("=" * 60)

    root = None
    embedded = False
    try:
        logger.info("Sistem gereksinimleri kontrol ediliyor...")
        validate_system_requirements()
        logger.info("✓ Sistem gereksinimleri karşılandı")

        logger.info("Ana uygulama penceresi oluşturuluyor...")
        root, app, embedded = create_main_window()
        logger.info("✓ Ana pencere başarıyla oluşturuldu")
        logger.info("Uygulama kullanıcı arayüzü başlatılıyor...")

        # 🔴 DİKKAT: Gömülü moddaysak mainloop ÇAĞIRMAYACAĞIZ.
        if not embedded:
            root.mainloop()

        logger.info("Uygulama normal şekilde sonlandırıldı")

    except KeyboardInterrupt:
        logger.info("Uygulama kullanıcı tarafından durduruldu (Ctrl+C)")
    except Exception as e:
        handle_critical_error(e, logger)
    finally:
        # 🔒 SADECE bağımsız modda pencereyi biz kapatırız.
        if (root is not None) and (not embedded):
            try:
                root.destroy()
            except Exception:
                pass
        logger.info("Uygulama temizlik işlemleri tamamlandı")


def run_program():
    """Geriye uyumluluk için"""
    main()


if __name__ == "__main__":
    # Bağımsız çalıştırma (test)
    main()
