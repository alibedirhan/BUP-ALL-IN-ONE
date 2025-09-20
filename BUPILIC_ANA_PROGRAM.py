#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
from pathlib import Path

# PyInstaller bundle path fix
def get_resource_path(relative_path=""):
    """PyInstaller ile paketlenmiş uygulamada kaynak dosyalarının yolunu bulur"""
    try:
        # PyInstaller bundle içinde geçici klasör
        base_path = sys._MEIPASS
    except AttributeError:
        # Normal Python çalışma ortamı
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

# Python path'ine modül klasörlerini ekle
def add_module_paths():
    """Alt modül klasörlerini Python path'ine ekler"""
    base_path = get_resource_path()
    
    module_dirs = [
        'ISKONTO_HESABI',
        'KARLILIK_ANALIZI', 
        'Musteri_Sayisi_Kontrolu',
        'YASLANDIRMA',
        'YASLANDIRMA/gui',
        'YASLANDIRMA/modules'
    ]
    
    for module_dir in module_dirs:
        full_path = os.path.join(base_path, module_dir)
        if os.path.exists(full_path) and full_path not in sys.path:
            sys.path.insert(0, full_path)
            print(f"✅ Added to path: {full_path}")

# Logging setup
def setup_logging():
    """Loglama ayarlarını yapar"""
    log_file = os.path.join(get_resource_path(), 'bupilic_app.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def install_dependencies():
    """Gerekli kütüphaneleri yükler"""
    import subprocess
    import importlib
    
    dependencies = [
        'pandas', 'numpy', 'matplotlib', 'customtkinter', 
        'openpyxl', 'pdfplumber', 'Pillow', 'seaborn',
        'xlsxwriter', 'xlrd', 'xlwt', 'psutil'
    ]
    
    for dep in dependencies:
        try:
            importlib.import_module(dep.lower().replace('-', '_'))
            print(f"✅ {dep} already installed")
        except ImportError:
            print(f"⬇️ Installing {dep}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
                print(f"✅ {dep} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {dep}")

def show_main_menu():
    """Ana menü arayüzünü gösterir"""
    import tkinter as tk
    from tkinter import ttk, messagebox
    
    class MainApp:
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Bupiliç Yönetim Sistemi")
            self.root.geometry("800x600")
            self.root.configure(bg='#2b2b2b')
            
            # Ana başlık
            title_label = tk.Label(
                self.root, 
                text="🐔 BUPİLİÇ YÖNETİM SİSTEMİ",
                font=('Arial', 24, 'bold'),
                fg='white',
                bg='#2b2b2b'
            )
            title_label.pack(pady=30)
            
            # Alt başlık
            subtitle_label = tk.Label(
                self.root,
                text="Tavukçuluk Sektörü İçin Tümleşik İşletme Yönetim Sistemi",
                font=('Arial', 12),
                fg='#cccccc',
                bg='#2b2b2b'
            )
            subtitle_label.pack(pady=10)
            
            # Buton frame
            button_frame = tk.Frame(self.root, bg='#2b2b2b')
            button_frame.pack(expand=True, fill='both', padx=50, pady=50)
            
            # Modül butonları
            self.create_module_button(button_frame, "💰 İskonto Hesaplama", self.open_iskonto, 0, 0)
            self.create_module_button(button_frame, "📊 Karlılık Analizi", self.open_karlilik, 0, 1)
            self.create_module_button(button_frame, "👥 Müşteri Sayısı Kontrolü", self.open_musteri, 1, 0)
            self.create_module_button(button_frame, "📅 Yaşlandırma Raporları", self.open_yaslandirma, 1, 1)
            
            # Çıkış butonu
            exit_btn = tk.Button(
                self.root,
                text="🚪 Çıkış",
                font=('Arial', 12, 'bold'),
                bg='#ff4444',
                fg='white',
                width=15,
                height=2,
                command=self.root.quit
            )
            exit_btn.pack(pady=20)
            
        def create_module_button(self, parent, text, command, row, col):
            """Modül butonu oluşturur"""
            btn = tk.Button(
                parent,
                text=text,
                font=('Arial', 14, 'bold'),
                bg='#4CAF50',
                fg='white',
                width=25,
                height=3,
                command=command,
                relief='raised',
                bd=3
            )
            btn.grid(row=row, column=col, padx=20, pady=20, sticky='nsew')
            
            # Grid weight ayarları
            parent.grid_rowconfigure(row, weight=1)
            parent.grid_columnconfigure(col, weight=1)
            
        def open_iskonto(self):
            """İskonto hesaplama modülünü açar"""
            try:
                print("🚀 Starting ISKONTO_HESABI...")
                # Import path fix
                sys.path.insert(0, get_resource_path('ISKONTO_HESABI'))
                
                from ISKONTO_HESABI.main import main as iskonto_main
                iskonto_main()
            except Exception as e:
                messagebox.showerror("Hata", f"İskonto modülü açılamadı:\n{str(e)}")
                logging.error(f"İskonto modülü hatası: {e}")
                
        def open_karlilik(self):
            """Karlılık analizi modülünü açar"""
            try:
                print("🚀 Starting KARLILIK_ANALIZI...")
                sys.path.insert(0, get_resource_path('KARLILIK_ANALIZI'))
                
                from KARLILIK_ANALIZI.gui import main as karlilik_main
                karlilik_main()
            except Exception as e:
                messagebox.showerror("Hata", f"Karlılık modülü açılamadı:\n{str(e)}")
                logging.error(f"Karlılık modülü hatası: {e}")
                
        def open_musteri(self):
            """Müşteri kontrolü modülünü açar"""
            try:
                print("🚀 Starting Musteri_Sayisi_Kontrolu...")
                sys.path.insert(0, get_resource_path('Musteri_Sayisi_Kontrolu'))
                
                from Musteri_Sayisi_Kontrolu.main import main as musteri_main
                musteri_main()
            except Exception as e:
                messagebox.showerror("Hata", f"Müşteri modülü açılamadı:\n{str(e)}")
                logging.error(f"Müşteri modülü hatası: {e}")
                
        def open_yaslandirma(self):
            """Yaşlandırma modülünü açar"""
            try:
                print("🚀 Starting YASLANDIRMA...")
                sys.path.insert(0, get_resource_path('YASLANDIRMA'))
                
                from YASLANDIRMA.main import main as yaslandirma_main
                yaslandirma_main()
            except Exception as e:
                messagebox.showerror("Hata", f"Yaşlandırma modülü açılamadı:\n{str(e)}")
                logging.error(f"Yaşlandırma modülü hatası: {e}")
                
        def run(self):
            """Uygulamayı çalıştırır"""
            self.root.mainloop()
    
    app = MainApp()
    return app

def main():
    """Ana fonksiyon"""
    print("🔄 Ensuring dependencies...")
    
    # Logging setup
    setup_logging()
    logging.info("Uygulama başlatıldı. Klasör yapısı hazır.")
    
    # Module paths'leri ekle
    add_module_paths()
    
    # Dependencies kontrolü
    print("🔧 Installing ALL dependencies...")
    install_dependencies()
    
    # Giriş kontrolü (istege bağlı)
    print("🔐 User authentication...")
    
    import tkinter as tk
    from tkinter import simpledialog, messagebox
    
    root = tk.Tk()
    root.withdraw()  # Ana pencereyi gizle
    
    password = simpledialog.askstring("Giriş", "Şifre girin:", show='*')
    
    if password == "bupilic2024":  # Varsayılan şifre
        root.destroy()
        logging.info("Kullanıcı giriş yaptı.")
        
        # Ana menüyü göster
        app = show_main_menu()
        app.run()
    else:
        messagebox.showerror("Hata", "Yanlış şifre!")
        root.destroy()
        sys.exit(1)

if __name__ == "__main__":
    main()
