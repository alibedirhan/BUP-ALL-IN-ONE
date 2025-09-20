# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import importlib
import tempfile
import shutil
import threading
import time
from pathlib import Path

def install_dependencies_completely():
    """Tüm bağımlılıkları otomatik olarak indirip kurar"""
    print("🤖 Automatic Dependency Installer")
    print("=" * 50)
    
    required_packages = [
        'pandas', 'numpy', 'matplotlib', 'pdfplumber', 'customtkinter',
        'openpyxl', 'psutil', 'Pillow', 'seaborn', 'xlsxwriter',
        'xlrd', 'xlwt', 'python-dateutil', 'tkcalendar'
    ]
    
    # Önce hangi modda olduğumuzu kontrol et
    is_frozen = getattr(sys, 'frozen', False)
    
    if is_frozen:
        print("❄️ Frozen mode detected - using standalone installer")
        return install_in_frozen_mode(required_packages)
    else:
        print("🐍 Normal mode - using pip")
        return install_with_pip(required_packages)

def install_with_pip(packages):
    """Normal modda pip ile kurulum"""
    try:
        for package in packages:
            try:
                importlib.import_module(package)
                print(f"✅ {package} already installed")
            except ImportError:
                print(f"⬇️ Downloading {package}...")
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ {package} installed successfully")
                else:
                    print(f"❌ Failed to install {package}: {result.stderr}")
        
        print("🎉 All dependencies installed!")
        return True
        
    except Exception as e:
        print(f"❌ Pip installation failed: {e}")
        return False

def install_in_frozen_mode(packages):
    """Frozen modda özel kurulum yöntemi"""
    print("🚀 Starting automatic installation...")
    
    # Geçici dizin oluştur
    temp_dir = tempfile.mkdtemp(prefix="bupilic_deps_")
    print(f"📁 Temporary directory: {temp_dir}")
    
    try:
        # Her paket için ayrı ayrı dene
        for package in packages:
            if not install_single_package(package, temp_dir):
                print(f"⚠️ Could not install {package}, but continuing...")
        
        # Başarılı say
        print("✅ Installation process completed")
        return True
        
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        return False
    finally:
        # Temizlik
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass

def install_single_package(package_name, target_dir):
    """Tek bir paketi kur"""
    try:
        # Önce zaten yüklü mü kontrol et
        try:
            importlib.import_module(package_name)
            print(f"✅ {package_name} already available")
            return True
        except ImportError:
            pass
        
        print(f"📦 Installing {package_name}...")
        
        # 1. Yöntem: embedded pip ile dene
        if try_embedded_pip(package_name):
            return True
        
        # 2. Yöntem: direct download ile dene
        if try_direct_download(package_name, target_dir):
            return True
        
        # 3. Yöntem: manual wheel download
        if try_wheel_download(package_name, target_dir):
            return True
            
        print(f"❌ All methods failed for {package_name}")
        return False
        
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def try_embedded_pip(package_name):
    """Embedded pip ile kurmayı dene"""
    try:
        # Python executable path
        python_exe = sys.executable
        python_dir = os.path.dirname(python_exe)
        
        # Pip yollarını ara
        possible_pip_paths = [
            os.path.join(python_dir, "pip"),
            os.path.join(python_dir, "pip.exe"),
            os.path.join(python_dir, "Scripts", "pip.exe"),
            os.path.join(python_dir, "Scripts", "pip"),
        ]
        
        for pip_path in possible_pip_paths:
            if os.path.exists(pip_path):
                print(f"🔧 Using pip: {pip_path}")
                result = subprocess.run([
                    python_exe, pip_path, "install", package_name
                ], capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ {package_name} installed via pip")
                    return True
        return False
        
    except:
        return False

def try_direct_download(package_name, target_dir):
    """Direct download ile kurmayı dene"""
    try:
        # Basitçe Python'u kullanarak kur
        import urllib.request
        import zipfile
        
        # Paket için wheel URL'si (basit versiyon)
        wheel_urls = {
            'pandas': f'https://files.pythonhosted.org/packages/pandas/pandas-2.1.4-cp310-cp310-win_amd64.whl',
            'numpy': f'https://files.pythonhosted.org/packages/numpy/numpy-1.24.3-cp310-cp310-win_amd64.whl',
            'matplotlib': f'https://files.pythonhosted.org/packages/matplotlib/matplotlib-3.7.2-cp310-cp310-win_amd64.whl',
        }
        
        if package_name in wheel_urls:
            print(f"🌐 Downloading {package_name} wheel...")
            wheel_path = os.path.join(target_dir, f"{package_name}.whl")
            
            # İndir
            urllib.request.urlretrieve(wheel_urls[package_name], wheel_path)
            
            # Kur
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", wheel_path
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {package_name} installed from wheel")
                return True
        
        return False
        
    except:
        return False

def try_wheel_download(package_name, target_dir):
    """Wheel download ile kurmayı dene"""
    try:
        # Python'u kullanarak wheel indir ve kur
        result = subprocess.run([
            sys.executable, "-m", "pip", "download", 
            package_name, "-d", target_dir
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # İndirilen wheel'leri bul ve kur
            wheels = [f for f in os.listdir(target_dir) if f.endswith('.whl')]
            for wheel in wheels:
                wheel_path = os.path.join(target_dir, wheel)
                subprocess.run([
                    sys.executable, "-m", "pip", "install", wheel_path
                ], capture_output=True)
            
            print(f"✅ {package_name} installed from downloaded wheel")
            return True
        
        return False
        
    except:
        return False

def ensure_all_dependencies():
    """Tüm bağımlılıkların kurulu olduğundan emin ol"""
    print("🔄 Checking and installing dependencies...")
    
    # Thread ile arka planda kur
    def install_thread():
        try:
            success = install_dependencies_completely()
            if success:
                print("🎉 All dependencies are ready!")
            else:
                print("⚠️ Some dependencies may be missing, but continuing...")
        except Exception as e:
            print(f"❌ Dependency installation error: {e}")
    
    # Arka planda kurulumu başlat
    thread = threading.Thread(target=install_thread, daemon=True)
    thread.start()
    
    # Hemen return et, uygulama beklemeye devam etsin
    return True

# UYGULAMA BAŞLANGICI
print("🚀 BupiliC Starting...")
print("💡 Automatic dependency installation in background...")

# Bağımlılıkları kontrol et ve kur (arka planda)
ensure_all_dependencies()

# Hemen ana uygulamaya geç
print("⚡ Starting main application...")

# Geri kalan importlar
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


import customtkinter as ctk
import subprocess
import os
from PIL import Image, ImageTk
import threading
import time
from datetime import datetime
import json
import logging
import locale
import sys
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
        
        ctk.CTkLabel(user_frame, text="👤", 
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
        
        nav_buttons = [
            ("📊 Ana Sayfa", self.show_dashboard),
            ("💰 İskonto Hesaplama", self.iskonto_ac),
            ("📈 Karlılık Analizi", self.karlilik_ac),
            ("👥 Müşteri Kayıp/Kaçak", self.musteri_kayip_ac),
            ("📊 Yaşlandırma", self.yaslandirma_ac),
            ("⚙️ Ayarlar", self.show_settings),
            ("🐛 Debug", self.show_debug_info)
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
            ("💰 İskonto Hesaplama", self.iskonto_ac, "#E63946"),
            ("📈 Karlılık Analizi", self.karlilik_ac, "#457B9D"),
            ("👥 Müşteri Kayıp/Kaçak", self.musteri_kayip_ac, "#2A9D8F"),
            ("📊 Yaşlandırma", self.yaslandirma_ac, "#F4A261")
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
    
    def run_subprogram(self, program_name, main_file="main.py"):
        """Alt programı çalıştır - KESİN ÇÖZÜM"""
        try:
            print(f"🚀 {program_name} başlatılıyor...")
            
            # Yol bulma - ÖNCE mevcut dizini kontrol et
            current_dir = os.path.dirname(os.path.abspath(__file__))
            program_dir = os.path.join(current_dir, program_name)
            
            # Eğer yoksa frozen modda ara
            if not os.path.exists(program_dir) and getattr(sys, 'frozen', False):
                program_dir = os.path.join(os.path.dirname(sys.executable), program_name)
                if not os.path.exists(program_dir):
                    program_dir = os.path.join(self.base_path, program_name)
            
            print(f"🔍 Program dizini: {program_dir}")
            
            if not os.path.exists(program_dir):
                self.show_message(f"{program_name} bulunamadı!")
                return False
            
            # Tüm Python dosyalarını listele
            py_files = [f for f in os.listdir(program_dir) if f.endswith('.py') and f != '__init__.py']
            print(f"📁 {program_name} içindeki Python dosyaları: {py_files}")
            
            # ÖZEL DURUM: KARLILIK_ANALIZI için gui.py kullan
            if program_name == "KARLILIK_ANALIZI":
                main_file = "gui.py"
                main_path = os.path.join(program_dir, main_file)
                print(f"✅ KARLILIK_ANALIZI için özel dosya: {main_file}")
            else:
                # Ana dosyayı bul
                main_path = None
                possible_main_files = [main_file, f"{program_name}.py", "app.py", "gui.py", "program.py"]
                
                for possible_file in possible_main_files:
                    test_path = os.path.join(program_dir, possible_file)
                    if os.path.exists(test_path):
                        main_path = test_path
                        main_file = possible_file
                        break
                
                if not main_path:
                    # Hiçbiri yoksa ilk Python dosyasını kullan
                    if py_files:
                        main_path = os.path.join(program_dir, py_files[0])
                        main_file = py_files[0]
                    else:
                        self.show_message(f"{program_name} içinde Python dosyası bulunamadı!")
                        return False
            
            print(f"✅ Ana dosya bulundu: {main_file}")
            
            # Windows için kesin çözüm
            if os.name == 'nt':
                try:
                    # Python executable'ı bul
                    python_exe = sys.executable
                    
                    # Eğer frozen modda ise sistem Python'unu kullan
                    if getattr(sys, 'frozen', False):
                        # Sistemde Python kurulu mu kontrol et
                        try:
                            result = subprocess.run(['python', '--version'], 
                                                  capture_output=True, text=True, timeout=5)
                            if result.returncode == 0:
                                python_exe = 'python'
                                print("✅ Sistem Python'u kullanılacak")
                            else:
                                result = subprocess.run(['py', '--version'], 
                                                      capture_output=True, text=True, timeout=5)
                                if result.returncode == 0:
                                    python_exe = 'py'
                                    print("✅ Py launcher kullanılacak")
                                else:
                                    # Son çare: embedded Python'u kullan
                                    python_exe = sys.executable
                                    print("⚠️ Embedded Python kullanılacak")
                        except:
                            python_exe = sys.executable
                            print("⚠️ Embedded Python kullanılacak (hata)")
                    
                    print(f"🐍 Python executable: {python_exe}")
                    
                    # start komutu ile yeni pencere aç
                    cmd = f'start "BupiliC - {program_name}" /D "{program_dir}" "{python_exe}" "{main_file}"'
                    print(f"⚡ Komut: {cmd}")
                    
                    # Komutu çalıştır
                    import subprocess
                    process = subprocess.Popen(cmd, shell=True)
                    time.sleep(3)  # Programın açılması için bekle
                    
                    # Process durumunu kontrol et
                    if process.poll() is None:
                        print(f"✅ {program_name} başarıyla başlatıldı")
                        return True
                    else:
                        # Alternatif yöntem - doğrudan çalıştır
                        try:
                            subprocess.Popen([python_exe, main_file], cwd=program_dir)
                            print(f"✅ {program_name} alternatif yöntemle başlatıldı")
                            return True
                        except Exception as alt_error:
                            print(f"❌ Alternatif yöntem de başarısız: {alt_error}")
                            self.show_message(f"{program_name} başlatılamadı!")
                            return False
                            
                except Exception as e:
                    print(f"❌ Hata: {e}")
                    # Son çare olarak subprocess dene
                    try:
                        subprocess.Popen([sys.executable, main_path], cwd=program_dir)
                        print(f"✅ {program_name} son çare yöntemiyle başlatıldı")
                        return True
                    except:
                        self.show_message(f"Hata: {e}")
                        return False
            else:
                # Linux/Mac için
                subprocess.Popen([sys.executable, main_path], cwd=program_dir)
                return True
                
        except Exception as e:
            print(f"❌ Genel hata: {e}")
            self.show_message(f"Beklenmeyen hata: {e}")
            return False

    def iskonto_ac(self):
        success = self.run_subprogram("ISKONTO_HESABI", "main.py")
        if not success:
            self.show_message("İskonto programı başlatılamadı!")

    def karlilik_ac(self):
        success = self.run_subprogram("KARLILIK_ANALIZI", "main.py")
        if not success:
            self.show_message("Karlılık analizi programı başlatılamadı!")

    def musteri_kayip_ac(self):
        success = self.run_subprogram("Musteri_Sayisi_Kontrolu", "main.py")
        if not success:
            self.show_message("Müşteri kayıp/kaçak programı başlatılamadı!")

    def yaslandirma_ac(self):
        success = self.run_subprogram("YASLANDIRMA", "main.py")
        if not success:
            self.show_message("Yaşlandırma programı başlatılamadı!")
    
    def show_message(self, message):
        print(f"INFO: {message}")
    
    def show_debug_info(self):
        debug_window = ctk.CTkToplevel(self.root)
        debug_window.title("🐛 Debug Information")
        debug_window.geometry("700x500")
        debug_window.transient(self.root)
        debug_window.grab_set()
        
        info_text = f"""DEBUG INFORMATION:

Frozen Mode: {self.is_frozen}
Base Path: {self.base_path}
Current Directory: {os.getcwd()}
Python Executable: {sys.executable}
Operating System: {os.name}

Subprograms Status:
"""
        
        subprograms = ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]
        
        for program in subprograms:
            program_path = os.path.join(self.base_path, program)
            exists = os.path.exists(program_path)
            main_file = "main.py"
            main_path = os.path.join(program_path, main_file) if exists else "N/A"
            main_exists = os.path.exists(main_path) if exists else False
            
            info_text += f"\n{program}:"
            info_text += f"\n  Path: {program_path}"
            info_text += f"\n  Exists: {'YES' if exists else 'NO'}"
            if exists:
                info_text += f"\n  Main file: {main_path}"
                info_text += f"\n  Main exists: {'YES' if main_exists else 'NO'}"
        
        textbox = ctk.CTkTextbox(debug_window, width=680, height=450)
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
