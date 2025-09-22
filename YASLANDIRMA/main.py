# YASLANDIRMA/main.py
# ExcelProcessorGUI’yi başlatan net bir main() sağlanır.

import logging
logging.basicConfig(level=logging.INFO)

def main():
    """
    Ana giriş: ExcelProcessorGUI’yi çalıştır.
    YASLANDIRMA/gui.py içindeki run() zaten ExcelProcessorGUI'yi çağırıyor.
    """
    try:
        # 1) Doğrudan run() ile
        from YASLANDIRMA.gui import run as gui_run
        gui_run()
    except Exception:
        # 2) Yedek: sınıfı doğrudan çağır
        from YASLANDIRMA.gui import ExcelProcessorGUI
        app = ExcelProcessorGUI()
        app.run()

def run_program():
    main()

if __name__ == "__main__":
    main()
