# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import importlib
import threading
import time
from pathlib import Path

# PyInstaller için path düzeltmeleri
def setup_paths():
    """PyInstaller bundle için path'leri düzelt"""
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
        print("Normal Python mode")

# Path'leri hemen ayarla
setup_paths()

def install_missing_dependencies():
    """Sadece eksik bağımlılıkları yükle"""
    print("Checking for missing dependencies...")
    
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
            print(f"✅ {package} already installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} missing")
    
    if not missing_packages:
        print("All dependencies are already installed!")
        return True
    
    print(f"Installing missing packages: {missing_packages}")
    
    # Python executable'ı bul
    python_exe = sys.executable
    
    for package in missing_packages:
        try:
            print(f"Installing {package}...")
            # Pillow için özel isim
            install_name = 'Pillow' if package == 'PIL' else package
            
            result = subprocess.run([
                python_exe, "-m", "pip", "install", install_name
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"❌ Failed to install {package}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error installing {package}: {e}")
    
    return True

def ensure_dependencies_async():
    """Bağımlılıkları arka planda kontrol et"""
    def install_thread():
        try:
            install_missing_dependencies()
        except Exception as e:
            print(f"❌ Dependency check error: {e}")
    
    thread = threading.Thread(target=install_thread, daemon=True)
    thread.start()
    return True

# HEMEN bağımlılıkları kontrol et (arka planda)
ensure_dependencies_async()

def run_embedded_program(program_name):
    """Gömülü programı çalıştır"""
    try:
        print(f"Starting {program_name}...")
        
        if program_name == "ISKONTO_HESABI":
            try:
                # Farklı import yollarını dene
                try:
                    from ISKONTO_HESABI import main as iskonto_main
                    if hasattr(iskonto_main, 'main'):
                        iskonto_main.main()
                    else:
                        print("main() function not found in ISKONTO_HESABI.main")
                    return True
                except ImportError:
                    # Alternatif import
                    import ISKONTO_HESABI.main
                    ISKONTO_HESABI.main.main()
                    return True
            except Exception as e:
                print(f"❌ ISKONTO_HESABI error: {e}")
                return False
                
        elif program_name == "KARLILIK_ANALIZI":
            try:
                try:
                    from KARLILIK_ANALIZI import gui as karlilik_gui
                    if hasattr(karlilik_gui, 'main'):
                        karlilik_gui.main()
                    else:
                        print("main() function not found in KARLILIK_ANALIZI.gui")
                    return True
                except ImportError:
                    import KARLILIK_ANALIZI.gui
                    KARLILIK_ANALIZI.gui.main()
                    return True
            except Exception as e:
                print(f"❌ KARLILIK_ANALIZI error: {e}")
                return False
                
        elif program_name == "Musteri_Sayisi_Kontrolu":
            try:
                try:
                    from Musteri_Sayisi_Kontrolu import main as musteri_main
                    if hasattr(musteri_main, 'main'):
                        musteri_main.main()
                    else:
                        print("main() function not found in Musteri_Sayisi_Kontrolu.main")
                    return True
                except ImportError:
                    import Musteri_Sayisi_Kontrolu.main
                    Musteri_Sayisi_Kontrolu.main.main()
                    return True
            except Exception as e:
                print(f"❌ Musteri_Sayisi_Kontrolu error: {e}")
                return False
                
        elif program_name == "YASLANDIRMA":
            try:
                try:
                    from YASLANDIRMA import main as yaslandirma_main
                    if hasattr(yaslandirma_main, 'main'):
                        yaslandirma_main.main()
                    else:
                        print("main() function not found in YASLANDIRMA.main")
                    return True
                except ImportError:
                    import YASLANDIRMA.main
                    YASLANDIRMA.main.main()
                    return True
            except Exception as e:
                print(f"❌ YASLANDIRMA error: {e}")
                return False
                
    except Exception as e:
        print(f"❌ General error starting {program_name}: {e}")
        return False

# Şimdi GUI kütüphanelerini import et
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
    print("✅ GUI libraries imported successfully")
except Exception as e:
    print(f"❌ GUI library import error: {e}")

class BupilicDashboard:
    def __init__(self):
        # Türkçe locale ayarlarını dene
        try:
            locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Turkish_Turkey.1254')
            except:
                print("Türkçe locale ayarlanamadı, İngilizce devam edilecek.")
        
        self.root = ctk.CTk()
        self.root.title("BupiliÇ İşletme Yönetim Sistemi")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # PyInstaller için resource path'i ayarla
        self.setup_resource_path()
        
        # Klasör yapısını oluştur
        self.setup_directories()
        
        # Loglama ayarla
        self.logger = self.setup_logging()
        self.logger.info("Uygulama başlatıldı. Klasör yapısı hazır.")
        
        # Kullanıcı verileri
        self.user_data = {
            "name": "Ali Yılmaz",
            "position": "Satış Yöneticisi",
            "password": "bupilic2024"
        }
        
        # Ayarları yükle
        self.load_settings()
        
        # Görünüm modu
        self.appearance_mode = self.user_data.get("theme", "light")
        ctk.set_appearance_mode(self.appearance_mode)
        ctk.set_default_color_theme("blue")
        
        # Merkezi renk yönetimi
        self.setup_color_palette()
        
        # Logo image referansını sakla
        self.logo_image = None
        
        # Önce login ekranı göster
        self.show_login_screen()
    
    def setup_resource_path(self):
        """PyInstaller için resource path'i ayarlar"""
        try:
            self.base_path = sys._MEIPASS
            self.is_frozen = True
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Frozen mode detected. Base path: {self.base_path}")
        except Exception:
            self.base_path = os.path.abspath(".")
            self.is_frozen = False
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Normal mode. Base path: {self.base_path}")
    
    def get_resource_path(self, relative_path):
        """Göreceli yolu absolute path'e çevirir"""
        if self.is_frozen:
            meipass_path = os.path.join(self.base_path, relative_path)
            if os.path.exists(meipass_path):
                return meipass_path
        return os.path.join(os.path.abspath("."), relative_path)
    
    def setup_directories(self):
        """Klasör yapısını oluşturur"""
        directories = [
            'data/input',
            'data/output',
            'config',
            'logs',
            'temp',
            'backups',
            'icon'
        ]
        
        for directory in directories:
            full_path = self.get_resource_path(directory)
            os.makedirs(full_path, exist_ok=True)
    
    def setup_logging(self):
        """Loglama sistemini kurar"""
        log_dir = self.get_resource_path("logs")
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def load_settings(self):
        """Kullanıcı ayarlarını yükler"""
        try:
            settings_path = self.get_resource_path("config/user_settings.json")
            if os.path.exists(settings_path):
                with open(settings_path, "r", encoding="utf-8") as f:
                    saved_data = json.load(f)
                    self.user_data.update(saved_data)
        except Exception as e:
            self.logger.error(f"Ayarlar yüklenirken hata: {str(e)}")
    
    def save_settings(self):
        """Kullanıcı ayarlarını kaydeder"""
        try:
            settings_path = self.get_resource_path("config/user_settings.json")
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            self.logger.error(f"Ayarlar kaydedilirken hata: {str(e)}")
    
    def setup_color_palette(self):
        self.colors = {
            "light": {
                "primary": "#2A9D8F",
                "secondary": "#264653",
                "background": "#F8F9FA",
                "text": "#000000",
                "text_secondary": "#6C757D",
                "card": "#FFFFFF",
                "button": "#E63946",
                "button_hover": "#C1121F",
                "sidebar_hover": "#1D7874",
            },
            "dark": {
                "primary": "#1D3557",
                "secondary": "#14213D",
                "background": "#121212",
                "text": "#FFFFFF",
                "text_secondary": "#ADB5BD",
                "card": "#1E1E1E",
                "button": "#E63946",
                "button_hover": "#C1121F",
                "sidebar_hover": "#2A9D8F",
            }
        }
    
    def get_color(self, color_key):
        return self.colors[self.appearance_mode][color_key]
    
    def load_logo(self):
        try:
            logo_path = self.get_resource_path("icon/bupilic_logo.png")
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                ctk_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(48, 48)
                )
                return ctk_image
        except Exception as e:
            self.logger.error(f"Logo yüklenirken hata: {e}")
        return None
    
    def show_login_screen(self):
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
        password = self.password_entry.get()
        if password == self.user_data["password"]:
            self.logger.info("Kullanıcı giriş yaptı.")
            self.setup_ui()
        else:
            self.login_error_label.configure(text="Hatalı şifre! Lütfen tekrar deneyin.")
    
    def setup_ui(self):
        self.clear_window()
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.logo_image = self.load_logo()
        
        self.setup_header()
        self.setup_sidebar()
        self.setup_main_content()
        self.update_datetime()
    
    def setup_header(self):
        self.header = ctk.CTkFrame(self.root, height=70, 
                                 fg_color=self.get_color("primary"), 
                                 corner_radius=0)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.header.grid_propagate(False)
        
        left_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        left_frame.pack(side="left", padx=20, pady=15)
        
        if self.logo_image:
            logo_label = ctk.CTkLabel(left_frame, image=self.logo_image, text="")
            logo_label.pack(side="left", padx=(0, 15))
        
        self.title_label = ctk.CTkLabel(left_frame, text="BUPİLİÇ", 
                           font=ctk.CTkFont(size=26, weight="bold"),
                           text_color="white")
        self.title_label.pack(side="left")
        
        right_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        right_frame.pack(side="right", padx=20, pady=15)
        
        self.theme_btn = ctk.CTkButton(right_frame, text="🌙", width=40, height=40,
                                     command=self.toggle_theme,
                                     fg_color="transparent", 
                                     hover_color="#FFFFFF",
                                     text_color="white")
        self.theme_btn.pack(side="right", padx=10)
        
        self.time_label = ctk.CTkLabel(right_frame, text="", 
                                     font=ctk.CTkFont(size=14), 
                                     text_color="white")
        self.time_label.pack(side="right", padx=10)
    
    def setup_sidebar(self):
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
        
        self.user_position_label = ctk.CTkLabel(user_frame, text=self.user_data["position"], 
                   font=ctk.CTkFont(size=12), 
                   text_color="#E9C46A")
        self.user_position_label.pack(pady=2)
        
        nav_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        nav_frame.pack(pady=20, padx=10, fill="x")
        
        nav_buttons = [
            ("Ana Sayfa", self.show_dashboard),
            ("İskonto Hesaplama", self.iskonto_ac),
            ("Karlılık Analizi", self.karlilik_ac),
            ("Müşteri Kayıp/Kaçak", self.musteri_kayip_ac),
            ("Yaşlandırma", self.yaslandirma_ac),
            ("Ayarlar", self.show_settings),
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
        self.main = ctk.CTkFrame(self.root, fg_color=self.get_color("background"))
        self.main.grid(row=1, column=1, sticky="nsew", padx=20, pady=20)
        
        self.setup_welcome_section()
        self.setup_quick_access()
    
    def setup_welcome_section(self):
        self.welcome_label = ctk.CTkLabel(self.main, 
                                   text="BupiliÇ İşletme Yönetim Sistemine Hoş Geldiniz",
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color=self.get_color("text"))
        self.welcome_label.pack(pady=(20, 10))
        
        self.desc_label = ctk.CTkLabel(self.main, 
                                text="Aşağıdaki butonlardan istediğiniz işlemi başlatabilirsiniz",
                                font=ctk.CTkFont(size=14),
                                text_color=self.get_color("text_secondary"))
        self.desc_label.pack(pady=(0, 30))
    
    def setup_quick_access(self):
        quick_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        quick_frame.pack(expand=True, pady=20)
        
        self.title_label = ctk.CTkLabel(quick_frame, text="Hızlı Erişim", 
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 text_color=self.get_color("text"))
        self.title_label.pack(pady=(0, 30))
        
        main_buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        main_buttons_frame.pack()
        
        main_buttons = [
            ("İskonto Hesaplama", self.iskonto_ac, "#E63946"),
            ("Karlılık Analizi", self.karlilik_ac, "#457B9D"),
            ("Müşteri Kayıp/Kaçak", self.musteri_kayip_ac, "#2A9D8F"),
            ("Yaşlandırma", self.yaslandirma_ac, "#F4A261")
        ]
        
        self.buttons = []
        
        for i, (text, command, color) in enumerate(main_buttons):
            row = i // 2
            col = i % 2
            
            btn_frame = ctk.CTkFrame(main_buttons_frame, fg_color="transparent")
            btn_frame.grid(row=row, column=col, padx=15, pady=15)
            
            btn = ctk.CTkButton(btn_frame, text=text, command=command,
                              height=60, 
                              width=220, 
                              fg_color=color,
                              hover_color=self.darken_color(color),
                              font=ctk.CTkFont(size=15, weight="bold"),
                              corner_radius=12,
                              text_color="white")
            btn.pack()
            self.buttons.append(btn)
    
    def show_settings(self):
        self.clear_main_content()
        
        settings_frame = ctk.CTkFrame(self.main, fg_color=self.get_color("background"))
        settings_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title_label = ctk.CTkLabel(settings_frame, text="Kullanıcı Ayarları", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(0, 30))
        
        back_btn = ctk.CTkButton(settings_frame, text="← Geri", 
                               command=self.setup_main_content,
                               height=40,
                               width=120,
                               fg_color="transparent",
                               font=ctk.CTkFont(size=13))
        back_btn.pack(pady=20)
    
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_main_content(self):
        for widget in self.main.winfo_children():
            widget.destroy()
    
    def darken_color(self, color):
        color_map = {
            "#E63946": "#C1121F",
            "#457B9D": "#1D3557",
            "#2A9D8F": "#1D7874",
            "#F4A261": "#E76F51"
        }
        return color_map.get(color, color)
    
    def toggle_theme(self):
        if self.appearance_mode == "light":
            self.appearance_mode = "dark"
            self.theme_btn.configure(text="☀️")
        else:
            self.appearance_mode = "light"
            self.theme_btn.configure(text="🌙")
        
        ctk.set_appearance_mode(self.appearance_mode)
        self.update_theme_colors()
        self.user_data["theme"] = self.appearance_mode
        self.save_settings()
    
    def update_theme_colors(self):
        self.header.configure(fg_color=self.get_color("primary"))
        self.sidebar.configure(fg_color=self.get_color("primary"))
        self.main.configure(fg_color=self.get_color("background"))
        
        self.welcome_label.configure(text_color=self.get_color("text"))
        self.desc_label.configure(text_color=self.get_color("text_secondary"))
        self.title_label.configure(text_color=self.get_color("text"))
    
    def get_turkish_date(self):
        now = datetime.now()
        turkish_months = [
            "Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran",
            "Temmuz", "Ağustos", "Eylül", "Ekim", "Kasım", "Aralık"
        ]
        
        day = now.day
        month = turkish_months[now.month - 1]
        year = now.year
        time_str = now.strftime("%H:%M:%S")
        
        return f"{day} {month} {year} - {time_str}"
    
    def update_datetime(self):
        def update():
            while True:
                try:
                    turkish_date = self.get_turkish_date()
                    self.time_label.configure(text=turkish_date)
                except:
                    english_date = datetime.now().strftime("%d %B %Y - %H:%M:%S")
                    self.time_label.configure(text=english_date)
                time.sleep(1)
        
        threading.Thread(target=update, daemon=True).start()
    
    def show_dashboard(self):
        self.clear_main_content()
        self.setup_welcome_section()
        self.setup_quick_access()
    
    def iskonto_ac(self):
        success = run_embedded_program("ISKONTO_HESABI")
        if not success:
            self.show_message("İskonto programı başlatılamadı!")

    def karlilik_ac(self):
        success = run_embedded_program("KARLILIK_ANALIZI")
        if not success:
            self.show_message("Karlılık analizi programı başlatılamadı!")

    def musteri_kayip_ac(self):
        success = run_embedded_program("Musteri_Sayisi_Kontrolu")
        if not success:
            self.show_message("Müşteri kayıp/kaçak programı başlatılamadı!")

    def yaslandirma_ac(self):
        success = run_embedded_program("YASLANDIRMA")
        if not success:
            self.show_message("Yaşlandırma programı başlatılamadı!")
    
    def show_message(self, message):
        print(f"INFO: {message}")
        # MessageBox göster
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
        dependencies = ['pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter', 
                       'PIL', 'python-dateutil', 'tkcalendar']
        
        for dep in dependencies:
            try:
                importlib.import_module(dep)
                info_text += f"\n  {dep}: ✅ AVAILABLE"
            except ImportError:
                info_text += f"\n  {dep}: ❌ MISSING"
        
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
        self.root.mainloop()

if __name__ == "__main__":
    app = BupilicDashboard()
    app.run()
