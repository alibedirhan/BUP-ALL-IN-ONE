# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import importlib
import threading
import time
from pathlib import Path

# ===== PyInstaller PATH DÜZELTMELERİ =====
def setup_pyinstaller_paths():
    """PyInstaller bundle için path'leri otomatik düzelt"""
    if getattr(sys, 'frozen', False):
        # PyInstaller bundle modunda
        bundle_dir = sys._MEIPASS
        print(f"PyInstaller mode detected. Bundle dir: {bundle_dir}")
        
        # Alt modül klasörlerini sys.path'e ekle
        module_dirs = [
            'ISKONTO_HESABI',
            'KARLILIK_ANALIZI', 
            'Musteri_Sayisi_Kontrolu',
            'YASLANDIRMA',
            'YASLANDIRMA/gui',
            'YASLANDIRMA/modules'
        ]
        
        for module_dir in module_dirs:
            full_path = os.path.join(bundle_dir, module_dir)
            if os.path.exists(full_path) and full_path not in sys.path:
                sys.path.insert(0, full_path)
                print(f"Added to path: {full_path}")
    else:
        print("Normal Python mode - development environment")

# Path'leri hemen ayarla
setup_pyinstaller_paths()

# ===== BAĞIMLILIK YÖNETİMİ =====
def check_and_install_dependencies():
    """SADECE PyInstaller dışında bağımlılıkları kontrol et"""
    # PyInstaller modunda bağımlılık yükleme yapma
    if getattr(sys, 'frozen', False):
        print("PyInstaller mode - all dependencies included")
        return True
    
    print("Development mode - checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'PIL', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'python-dateutil', 'tkcalendar'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"OK: {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"MISSING: {package}")
    
    if missing_packages:
        print(f"Installing missing packages: {missing_packages}")
        python_exe = sys.executable
        
        for package in missing_packages:
            try:
                install_name = 'Pillow' if package == 'PIL' else package
                result = subprocess.run([
                    python_exe, "-m", "pip", "install", install_name
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"Installed: {package}")
                else:
                    print(f"Failed to install {package}")
            except Exception as e:
                print(f"Error installing {package}: {e}")
    
    return True

# ===== PROGRAM ÇALIŞTIRMA =====
def run_subprogram(program_name):
    """Alt programları çalıştır - garantili yöntem"""
    try:
        print(f"Starting {program_name}...")
        
        if program_name == "ISKONTO_HESABI":
            try:
                # Method 1: Direct import
                from ISKONTO_HESABI import main as iskonto_main
                if hasattr(iskonto_main, 'main'):
                    iskonto_main.main()
                    return True
            except ImportError:
                try:
                    # Method 2: Module path import
                    import sys
                    iskonto_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else '.', 'ISKONTO_HESABI')
                    sys.path.insert(0, iskonto_path)
                    import main as iskonto_main
                    iskonto_main.main()
                    return True
                except Exception as e:
                    print(f"ISKONTO_HESABI import error: {e}")
                    return False
                    
        elif program_name == "KARLILIK_ANALIZI":
            try:
                from KARLILIK_ANALIZI import gui as karlilik_gui
                if hasattr(karlilik_gui, 'main'):
                    karlilik_gui.main()
                    return True
            except ImportError:
                try:
                    karlilik_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else '.', 'KARLILIK_ANALIZI')
                    sys.path.insert(0, karlilik_path)
                    import gui as karlilik_gui
                    karlilik_gui.main()
                    return True
                except Exception as e:
                    print(f"KARLILIK_ANALIZI import error: {e}")
                    return False
                    
        elif program_name == "Musteri_Sayisi_Kontrolu":
            try:
                from Musteri_Sayisi_Kontrolu import main as musteri_main
                if hasattr(musteri_main, 'main'):
                    musteri_main.main()
                    return True
            except ImportError:
                try:
                    musteri_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else '.', 'Musteri_Sayisi_Kontrolu')
                    sys.path.insert(0, musteri_path)
                    import main as musteri_main
                    musteri_main.main()
                    return True
                except Exception as e:
                    print(f"Musteri_Sayisi_Kontrolu import error: {e}")
                    return False
                    
        elif program_name == "YASLANDIRMA":
            try:
                from YASLANDIRMA import main as yaslandirma_main
                if hasattr(yaslandirma_main, 'main'):
                    yaslandirma_main.main()
                    return True
            except ImportError:
                try:
                    yaslandirma_path = os.path.join(sys._MEIPASS if getattr(sys, 'frozen', False) else '.', 'YASLANDIRMA')
                    sys.path.insert(0, yaslandirma_path)
                    import main as yaslandirma_main
                    yaslandirma_main.main()
                    return True
                except Exception as e:
                    print(f"YASLANDIRMA import error: {e}")
                    return False
                    
    except Exception as e:
        print(f"General error starting {program_name}: {e}")
        return False

# Bağımlılıkları kontrol et (sadece dev mode'da)
check_and_install_dependencies()

# ===== GUI KÜTÜPHANELER =====
try:
    import customtkinter as ctk
    from PIL import Image, ImageTk
    import threading
    import time
    from datetime import datetime
    import json
    import logging
    import locale
    from pathlib import Path
    import tempfile
    import shutil
    print("GUI libraries loaded successfully")
except Exception as e:
    print(f"GUI library error: {e}")
    sys.exit(1)

# ===== ANA UYGULAMA SINIFI =====
class BupilicDashboard:
    def __init__(self):
        # Locale ayarları
        try:
            locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Turkish_Turkey.1254')
            except:
                pass
        
        # Ana pencere
        self.root = ctk.CTk()
        self.root.title("BupiliC İşletme Yönetim Sistemi")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # PyInstaller resource path
        self.setup_resource_path()
        self.setup_directories()
        self.logger = self.setup_logging()
        
        # Kullanıcı verileri
        self.user_data = {
            "name": "Ali Yılmaz",
            "position": "Satış Yöneticisi",
            "password": "bupilic2024"
        }
        
        # Ayarları yükle
        self.load_settings()
        
        # Tema
        self.appearance_mode = self.user_data.get("theme", "light")
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("blue")
        
        # Renk paleti
        self.setup_color_palette()
        
        # Login ekranı
        self.show_login_screen()
    
    def setup_resource_path(self):
        """Resource path ayarları"""
        try:
            self.base_path = sys._MEIPASS
            self.is_frozen = True
        except:
            self.base_path = os.path.abspath(".")
            self.is_frozen = False
    
    def get_resource_path(self, relative_path):
        """Resource dosya yolu"""
        if self.is_frozen:
            return os.path.join(self.base_path, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)
    
    def setup_directories(self):
        """Klasörleri oluştur"""
        directories = ['data/input', 'data/output', 'config', 'logs', 'temp', 'backups']
        for directory in directories:
            os.makedirs(self.get_resource_path(directory), exist_ok=True)
    
    def setup_logging(self):
        """Logging ayarları"""
        log_dir = self.get_resource_path("logs")
        log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_settings(self):
        """Ayarları yükle"""
        try:
            settings_path = self.get_resource_path("config/user_settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self.user_data.update(saved_data)
        except:
            pass
    
    def save_settings(self):
        """Ayarları kaydet"""
        try:
            settings_path = self.get_resource_path("config/user_settings.json")
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
        except:
            pass
    
    def setup_color_palette(self):
        """Renk paleti"""
        self.colors = {
            "light": {
                "primary": "#2A9D8F",
                "background": "#F8F9FA",
                "text": "#000000",
                "text_secondary": "#6C757D",
                "button": "#E63946",
                "button_hover": "#C1121F",
                "sidebar_hover": "#1D7874",
            },
            "dark": {
                "primary": "#1D3557",
                "background": "#121212",
                "text": "#FFFFFF",
                "text_secondary": "#ADB5BD",
                "button": "#E63946",
                "button_hover": "#C1121F",
                "sidebar_hover": "#2A9D8F",
            }
        }
    
    def get_color(self, color_key):
        return self.colors[self.appearance_mode][color_key]
    
    def show_login_screen(self):
        """Login ekranı"""
        self.clear_window()
        
        login_frame = ctk.CTkFrame(self.root, fg_color=self.get_color("background"))
        login_frame.pack(expand=True, fill="both", padx=100, pady=100)
        
        title_label = ctk.CTkLabel(login_frame, text="BUPİLİÇ", 
                                 font=ctk.CTkFont(size=32, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(50, 20))
        
        subtitle_label = ctk.CTkLabel(login_frame, text="İşletme Yönetim Sistemi", 
                                    font=ctk.CTkFont(size=18),
                                    text_color=self.get_color("text_secondary"))
        subtitle_label.pack(pady=(0, 50))
        
        password_frame = ctk.CTkFrame(login_frame, fg_color="transparent")
        password_frame.pack(pady=20)
        
        password_label = ctk.CTkLabel(password_frame, text="Şifre:", 
                                    font=ctk.CTkFont(size=14),
                                    text_color=self.get_color("text"))
        password_label.pack()
        
        self.password_entry = ctk.CTkEntry(password_frame, 
                                         placeholder_text="Şifrenizi giriniz",
                                         show="*",
                                         width=250,
                                         height=40,
                                         font=ctk.CTkFont(size=14))
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda e: self.check_login())
        
        login_btn = ctk.CTkButton(password_frame, text="Giriş Yap", 
                                command=self.check_login,
                                height=40,
                                width=150,
                                fg_color=self.get_color("button"),
                                hover_color=self.get_color("button_hover"),
                                font=ctk.CTkFont(size=14, weight="bold"))
        login_btn.pack(pady=20)
        
        self.login_error_label = ctk.CTkLabel(password_frame, text="", 
                                            text_color="red",
                                            font=ctk.CTkFont(size=12))
        self.login_error_label.pack()
    
    def check_login(self):
        """Login kontrolü"""
        password = self.password_entry.get()
        if password == self.user_data["password"]:
            self.logger.info("Kullanıcı giriş yaptı.")
            self.setup_ui()
        else:
            self.login_error_label.configure(text="Hatalı şifre! Lütfen tekrar deneyin.")
    
    def setup_ui(self):
        """Ana UI"""
        self.clear_window()
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.setup_header()
        self.setup_sidebar()
        self.setup_main_content()
        self.update_datetime()
    
    def setup_header(self):
        """Header"""
        self.header = ctk.CTkFrame(self.root, height=70, 
                                 fg_color=self.get_color("primary"), 
                                 corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_propagate(False)
        
        left_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=15)
        
        self.title_label = ctk.CTkLabel(left_frame, text="BUPİLİÇ", 
                           font=ctk.CTkFont(size=26, weight="bold"),
                           text_color="white")
        self.title_label.pack(side="left")
        
        right_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=15)
        
        self.theme_btn = ctk.CTkButton(right_frame, text="🌙", width=40, height=40,
                                     command=self.toggle_theme,
                                     fg_color="transparent", 
                                     text_color="white")
        self.theme_btn.pack(side="right", padx=10)
        
        self.time_label = ctk.CTkLabel(right_frame, text="", 
                                     font=ctk.CTkFont(size=14), 
                                     text_color="white")
        self.time_label.pack(side="right", padx=10)
    
    def setup_sidebar(self):
        """Sidebar"""
        self.sidebar = ctk.CTkFrame(self.root, width=220, 
                                  fg_color=self.get_color("primary"), 
                                  corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(pady=30, padx=10, fill="x")
        
        self.user_name_label = ctk.CTkLabel(user_frame, text=self.user_data["name"], 
                   font=ctk.CTkFont(size=16, weight="bold"), 
                   text_color="white")
        self.user_name_label.pack()
        
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(pady=20, padx=10, fill="x")
        
        nav_buttons = [
            ("Ana Sayfa", self.show_dashboard),
            ("İskonto Hesaplama", self.iskonto_ac),
            ("Karlılık Analizi", self.karlilik_ac),
            ("Müşteri Kayıp/Kaçak", self.musteri_kayip_ac),
            ("Yaşlandırma", self.yaslandirma_ac),
            ("Debug", self.show_debug_info)
        ]
        
        for text, command in nav_buttons:
            btn = ctk.CTkButton(nav_frame, text=text, command=command,
                              fg_color="transparent", 
                              hover_color=self.get_color("sidebar_hover"),
                              anchor="w", 
                              height=40,
                              font=ctk.CTkFont(size=14),
                              text_color="white")
            btn.pack(fill="x", pady=3)
    
    def setup_main_content(self):
        """Ana içerik"""
        self.main = ctk.CTkFrame(self.root, fg_color=self.get_color("background"))
        self.main.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        welcome_label = ctk.CTkLabel(self.main, 
                               text="BupiliÇ İşletme Yönetim Sistemine Hoş Geldiniz",
                               font=ctk.CTkFont(size=18, weight="bold"),
                               text_color=self.get_color("text"))
        welcome_label.pack(pady=(20, 30))
        
        # Ana butonlar
        buttons_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        buttons_frame.pack(expand=True)
        
        main_buttons = [
            ("İskonto Hesaplama", self.iskonto_ac, "#E63946"),
            ("Karlılık Analizi", self.karlilik_ac, "#457B9D"),
            ("Müşteri Kayıp/Kaçak", self.musteri_kayip_ac, "#2A9D8F"),
            ("Yaşlandırma", self.yaslandirma_ac, "#F4A261")
        ]
        
        for i, (text, command, color) in enumerate(main_buttons):
            row = i // 2
            col = i % 2
            
            btn_frame = ctk.CTkFrame(buttons_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=col, padx=15, pady=15)
            
            btn = ctk.CTkButton(btn_frame, text=text, command=command,
                              height=60, 
                              width=220, 
                              fg_color=color,
                              font=ctk.CTkFont(size=15, weight="bold"),
                              corner_radius=12,
                              text_color="white")
            btn.pack()
    
    def clear_window(self):
        """Pencereyi temizle"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def toggle_theme(self):
        """Tema değiştir"""
        if self.appearance_mode == "light":
            self.appearance_mode = "dark"
            self.theme_btn.configure(text="☀️")
        else:
            self.appearance_mode = "light"
            self.theme_btn.configure(text="🌙")
        
        ctk.set_appearance_mode(self.appearance_mode)
        self.user_data["theme"] = self.appearance_mode
        self.save_settings()
    
    def update_datetime(self):
        """Tarih/saat güncelleme"""
        def update():
            while True:
                try:
                    now = datetime.now()
                    date_str = now.strftime("%d/%m/%Y - %H:%M:%S")
                    self.time_label.configure(text=date_str)
                except:
                    pass
                time.sleep(1)
        
        threading.Thread(target=update, daemon=True).start()
    
    def show_dashboard(self):
        """Ana sayfa"""
        self.clear_main_content()
        self.setup_main_content()
    
    def clear_main_content(self):
        """Ana içeriği temizle"""
        try:
            for widget in self.main.winfo_children():
                widget.destroy()
        except:
            pass
    
    # ===== ALT PROGRAM ÇALIŞTIRMA FONKSİYONLARI =====
    def iskonto_ac(self):
        """İskonto hesaplama programını aç"""
        success = run_subprogram("ISKONTO_HESABI")
        if not success:
            self.show_message("İskonto programı başlatılamadı!")

    def karlilik_ac(self):
        """Karlılık analizi programını aç"""
        success = run_subprogram("KARLILIK_ANALIZI")
        if not success:
            self.show_message("Karlılık analizi programı başlatılamadı!")

    def musteri_kayip_ac(self):
        """Müşteri kayıp/kaçak programını aç"""
        success = run_subprogram("Musteri_Sayisi_Kontrolu")
        if not success:
            self.show_message("Müşteri kayıp/kaçak programı başlatılamadı!")

    def yaslandirma_ac(self):
        """Yaşlandırma programını aç"""
        success = run_subprogram("YASLANDIRMA")
        if not success:
            self.show_message("Yaşlandırma programı başlatılamadı!")
    
    def show_message(self, message):
        """Mesaj göster"""
        print(f"INFO: {message}")
        try:
            import tkinter.messagebox as msgbox
            msgbox.showinfo("Bilgi", message)
        except:
            print(f"GUI Message: {message}")
    
    def show_debug_info(self):
        """Debug bilgilerini göster"""
        debug_window = ctk.CTkToplevel(self.root)
        debug_window.title("Debug Information")
        debug_window.geometry("800x600")
        debug_window.transient(self.root)
        debug_window.grab_set()
        
        # Debug bilgilerini topla
        info_text = f"""DEBUG INFORMATION:

Frozen Mode: {getattr(sys, 'frozen', False)}
Base Path: {getattr(sys, '_MEIPASS', 'Not frozen')}
Current Directory: {os.getcwd()}
Python Executable: {sys.executable}
Operating System: {os.name}

SUBPROGRAMS STATUS:
"""
        
        subprograms = ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]
        
        for program in subprograms:
            if hasattr(self, 'base_path'):
                program_path = os.path.join(self.base_path, program)
            else:
                program_path = program
            exists = os.path.exists(program_path)
            
            info_text += f"\n{program}:"
            info_text += f"\n  Path: {program_path}"
            info_text += f"\n  Exists: {'YES' if exists else 'NO'}"
            
            if exists:
                try:
                    py_files = [f for f in os.listdir(program_path) if f.endswith('.py')]
                    info_text += f"\n  Python Files: {py_files}"
                except:
                    info_text += f"\n  Files: Cannot read directory"
        
        info_text += f"\n\nDEPENDENCIES STATUS:"
        dependencies = ['pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter', 'PIL']
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                info_text += f"\n  {dep}: OK"
            except ImportError:
                info_text += f"\n  {dep}: MISSING"
        
        textbox = ctk.CTkTextbox(debug_window, width=780, height=550)
        textbox.pack(padx=10, pady=10, fill="both", expand=True)
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")
        
        close_btn = ctk.CTkButton(debug_window, text="Kapat", 
                                command=debug_window.destroy,
                                height=40,
                                fg_color="#E63946")
        close_btn.pack(pady=10)
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

# ===== ANA PROGRAM BAŞLATMA =====
if __name__ == "__main__":
    try:
        app = BupilicDashboard()
        app.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        sys.exit(1)
