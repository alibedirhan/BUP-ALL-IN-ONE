# ISKONTO_HESABI/main.py
# Tek pencere, modern UI. create_main_window'a gerek kalmadan direkt çalışır.

import sys
import os
import logging
from pathlib import Path
import tkinter as tk

# (Opsiyonel) Frozen modda log için basit ayar
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def _center_window(win: tk.Tk, w: int = 1400, h: int = 800):
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw // 2) - (w // 2)
    y = (sh // 2) - (h // 2)
    win.geometry(f"{w}x{h}+{x}+{y}")

def main():
    """
    Ana giriş: ModernPriceCalculatorUI ile çalış.
    """
    # UI bileşenlerini import et (paket içinden)
    try:
        from ISKONTO_HESABI.ui_components import ModernPriceCalculatorUI, create_main_window  # create_main_window yedek kalsın
    except Exception as e:
        logging.error(f"UI bileşenleri import edilemedi: {e}", exc_info=True)
        raise

    # TK kök pencere
    root = tk.Tk()
    root.title("Bupiliç İskontolu Fiyat Hesaplayıcı v3.0")
    _center_window(root, 1400, 800)

    # İkon (varsa)
    icon_candidates = [
        Path("icon.ico"),
        Path("icon") / "bupilic_logo.ico",
        Path("icon") / "bupilic_logo.ico".name,
    ]
    for ic in icon_candidates:
        if ic.exists():
            try:
                root.iconbitmap(str(ic))
                break
            except Exception:
                pass

    # Uygulama
    app = ModernPriceCalculatorUI(root)

    logging.info("İskonto Hesaplayıcı başlatıldı")
    root.mainloop()

def run_program():
    main()

if __name__ == "__main__":
    main()
