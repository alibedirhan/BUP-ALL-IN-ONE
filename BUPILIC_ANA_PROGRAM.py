# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import importlib
import threading
import time
from pathlib import Path

# ===== KESİN ÇÖZÜM: TÜM BAĞIMLILIKLAR =====
def install_missing_dependencies():
    """Sadece eksik bağımlılıkları yükle"""
    print("🔧 Checking for missing dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'PIL', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'python-dateutil', 'tkcalendar'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package} already installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} missing")
    
    if not missing_packages:
        print("🎉 All dependencies are already installed!")
        return True
    
    print(f"⬇️ Installing missing packages: {missing_packages}")
    
    # Python executable'ı bul
    python_exe = sys.executable
    
    for package in missing_packages:
        try:
            print(f"📦 Installing {package}...")
            result = subprocess.run([
                python_exe, "-m", "pip", "install", package
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

# ===== TÜM ALT PROGRAMLARI ÇALIŞTIRMA =====
def run_embedded_program(program_name):
    """Gömülü programı çalıştır - KESİN ÇÖZÜM"""
    print(f"🚀 Starting {program_name}...")
    
    # PyInstaller modunda çalışıyorsak
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
        print(f"Frozen mode. Base path: {base_path}")
        
        # ALT PROGRAMIN YOLUNU EKLE
        program_path = os.path.join(base_path, program_name)
        if program_path not in sys.path:
            sys.path.insert(0, program_path)
            print(f"Added program path: {program_path}")
    
    try:
        # DOĞRUDAN IMPORT ET VE ÇALIŞTIR
        if program_name == "ISKONTO_HESABI":
            from ISKONTO_HESABI.main import main
            main()
            return True
            
        elif program_name == "KARLILIK_ANALIZI":
            from KARLILIK_ANALIZI.gui import main
            main()
            return True
            
        elif program_name == "Musteri_Sayisi_Kontrolu":
            from Musteri_Sayisi_Kontrolu.main import main
            main()
            return True
            
        elif program_name == "YASLANDIRMA":
            from YASLANDIRMA.main import main
            main()
            return True
            
    except Exception as e:
        print(f"❌ Error running {program_name}: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return False

# GERI KALAN IMPORTLAR
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

# ... (BUPILIC_ANA_PROGRAM.py'nin geri kalanı AYNI KALACAK)
# class BupilicDashboard: ... etc.

# GERI KALAN IMPORTLAR
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
        self.root.title("Bupiliç İşletme Yönetim Sistemi")
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
        else:
            ctk.CTkLabel(left_frame, text="🐔", 
                       font=ctk.CTkFont(size=28)).pack(side="left", padx=(0, 15))
        
            ctk.CTkLabel(left_frame, text="BUPİLİÇ", 
                       font=ctk.CTkFont(size=26, weight="bold"),
                       text_color="white").pack(side="left")
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
        
        ctk.CTkLabel(user_frame, text="Kullanıcı", 
                   font=ctk.CTkFont(size=32),
                   text_color="white").pack(pady=5)
        
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
        
        # Tüm emojileri Unicode escape ile yazın:
        nav_buttons = [
            ("\U0001F4CA Ana Sayfa", self.show_dashboard),
            ("\U0001F4B0 İskonto Hesaplama", self.iskonto_ac),
            ("\U0001F4C8 Karlılık Analizi", self.karlilik_ac),
            ("\U0001F465 Müşteri Kayıp/Kaçak", self.musteri_kayip_ac),
            ("\U0001F4CA Yaşlandırma", self.yaslandirma_ac),
            ("\U00002699 Ayarlar", self.show_settings),
            ("\U0001F41B Debug", self.show_debug_info)
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
                                   text="Bupiliç İşletme Yönetim Sistemine Hoş Geldiniz",
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
        
        self.title_label = ctk.CTkLabel(quick_frame, text="🚀 Hızlı Erişim", 
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
        self.desc_labels = []
        
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
            
            descriptions = {
                "💰 İskonto Hesaplama": "İskontolarını hesapla",
                "📈 Karlılık Analizi": "Şube karlılık analizleri",
                "👥 Müşteri Kayıp/Kaçak": "Müşteri kayıp/kaçak analizleri",
                "📊 Yaşlandırma": "Yaşlandırma raporları"
            }
            
            desc_label = ctk.CTkLabel(btn_frame, 
                                    text=descriptions[text],
                                    font=ctk.CTkFont(size=12),
                                    text_color=self.get_color("text_secondary"))
            desc_label.pack(pady=(5, 0))
            self.desc_labels.append(desc_label)
    
    def show_settings(self):
        self.clear_main_content()
        
        settings_frame = ctk.CTkFrame(self.main, fg_color=self.get_color("background"))
        settings_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title_label = ctk.CTkLabel(settings_frame, text="⚙️ Kullanıcı Ayarları", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(0, 30))
        
        form_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        form_frame.pack(pady=20)
        
        ctk.CTkLabel(form_frame, text="İsim:", 
                   font=ctk.CTkFont(size=14),
                   text_color=self.get_color("text")).grid(row=0, column=0, sticky="w", pady=10)
        
        self.name_entry = ctk.CTkEntry(form_frame, 
                                     width=250,
                                     height=40,
                                     font=ctk.CTkFont(size=14))
        self.name_entry.insert(0, self.user_data["name"])
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Pozisyon:", 
                   font=ctk.CTkFont(size=14),
                   text_color=self.get_color("text")).grid(row=1, column=0, sticky="w", pady=10)
        
        self.position_entry = ctk.CTkEntry(form_frame, 
                                         width=250,
                                         height=40,
                                         font=ctk.CTkFont(size=14))
        self.position_entry.insert(0, self.user_data["position"])
        self.position_entry.grid(row=1, column=1, padx=20, pady=10)
        
        ctk.CTkLabel(form_frame, text="Yeni Şifre:", 
                   font=ctk.CTkFont(size=14),
                   text_color=self.get_color("text")).grid(row=2, column=0, sticky="w", pady=10)
        
        self.new_password_entry = ctk.CTkEntry(form_frame, 
                                             width=250,
                                             height=40,
                                             show="*",
                                             font=ctk.CTkFont(size=14),
                                             placeholder_text="Yeni şifre (boş bırakılırsa değişmez)")
        self.new_password_entry.grid(row=2, column=1, padx=20, pady=10)
        
        save_btn = ctk.CTkButton(form_frame, text="Kaydet", 
                               command=self.save_user_settings,
                               height=45,
                               width=200,
                               fg_color=self.get_color("button"),
                               hover_color=self.get_color("button_hover"),
                               font=ctk.CTkFont(size=15, weight="bold"))
        save_btn.grid(row=3, column=0, columnspan=2, pady=30)
        
        back_btn = ctk.CTkButton(settings_frame, text="← Geri", 
                               command=self.setup_main_content,
                               height=40,
                               width=120,
                               fg_color="transparent",
                               font=ctk.CTkFont(size=13))
        back_btn.pack(pady=20)
    
    def save_user_settings(self):
        new_name = self.name_entry.get()
        new_position = self.position_entry.get()
        new_password = self.new_password_entry.get()
        
        if new_name:
            self.user_data["name"] = new_name
            self.user_name_label.configure(text=new_name)
        
        if new_position:
            self.user_data["position"] = new_position
            self.user_position_label.configure(text=new_position)
        
        if new_password:
            self.user_data["password"] = new_password
        
        self.user_data["theme"] = self.appearance_mode
        self.save_settings()
        self.show_message("Ayarlar kaydedildi!")
    
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
        
        for label in self.desc_labels:
            label.configure(text_color=self.get_color("text_secondary"))
    
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
        print("=== DEBUG ISKONTO ===")
        print(f"Current directory: {os.getcwd()}")
        print(f"Python path: {sys.path}")
        print(f"Frozen: {getattr(sys, 'frozen', False)}")
        if getattr(sys, 'frozen', False):
            print(f"MEIPASS: {sys._MEIPASS}")
            print(f"Files in MEIPASS: {os.listdir(sys._MEIPASS)}")
        
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
    
    def show_debug_info(self):
        """Debug bilgilerini göster"""
        debug_info = f"""
        DEBUG INFORMATION:
        Current dir: {os.getcwd()}
        Python path: {sys.path}
        Frozen: {getattr(sys, 'frozen', False)}
        """
        
        if getattr(sys, 'frozen', False):
            debug_info += f"MEIPASS: {sys._MEIPASS}\n"
            try:
                debug_info += f"Files in MEIPASS: {os.listdir(sys._MEIPASS)}\n"
            except:
                debug_info += "Cannot list MEIPASS files\n"
        
        # Her alt programın varlığını kontrol et
        for program in ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]:
            debug_info += f"\n{program}:\n"
            if getattr(sys, 'frozen', False):
                program_path = os.path.join(sys._MEIPASS, program)
                debug_info += f"  In MEIPASS: {os.path.exists(program_path)}\n"
            
            # Current dir'de kontrol et
            current_program_path = os.path.join(os.getcwd(), program)
            debug_info += f"  In current dir: {os.path.exists(current_program_path)}\n"
        
        print(debug_info)
        self.show_message(debug_info)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = BupilicDashboard()
    app.run()
