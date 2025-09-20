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
        
        # DEBUG: Windows sorunlarını analiz et
        self.debug_windows_issue()
        
        # Klasör yapısını oluştur
        self.setup_directories()
        
        # Loglama ayarla
        self.logger = self.setup_logging()
        self.logger.info("Uygulama başlatıldı. Klasör yapısı hazır.")
        
        # Kullanıcı verileri
        self.user_data = {
            "name": "Ali Yılmaz",
            "position": "Satış Yöneticisi",
            "password": "bupilic2024"  # Varsayılan şifre
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
    
    def debug_windows_issue(self):
        """Windows spesifik sorunları debug et"""
        print("=" * 60)
        print("🐛 WINDOWS DEBUG INFORMATION")
        print("=" * 60)
        
        print(f"🏷️ Frozen Mode: {self.is_frozen}")
        print(f"📦 Base Path: {self.base_path}")
        print(f"📂 Current Directory: {os.getcwd()}")
        print(f"🐍 Python Executable: {sys.executable}")
        print(f"🔧 Operating System: {os.name}")
        
        # _internal klasörünü kontrol et
        if self.is_frozen:
            internal_path = os.path.join(self.base_path, '_internal')
            print(f"📁 _internal exists: {os.path.exists(internal_path)}")
            
            if os.path.exists(internal_path):
                print("📋 _internal contents:")
                try:
                    items = os.listdir(internal_path)
                    for item in items:
                        item_path = os.path.join(internal_path, item)
                        if os.path.isdir(item_path):
                            print(f"  📂 {item}/")
                        else:
                            print(f"  📄 {item}")
                except Exception as e:
                    print(f"❌ Error listing _internal: {e}")
        
        # Alt programları kontrol et
        programs = ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]
        print("\n🔍 Checking subprograms:")
        for program in programs:
            # Normal yol
            program_path = os.path.join(self.base_path, program)
            # _internal içindeki yol
            internal_program_path = os.path.join(self.base_path, '_internal', program)
            
            normal_exists = os.path.exists(program_path)
            internal_exists = os.path.exists(internal_program_path)
            
            print(f"  {program}:")
            print(f"    Normal: {'✅' if normal_exists else '❌'} {program_path}")
            print(f"    Internal: {'✅' if internal_exists else '❌'} {internal_program_path}")
            
            # Main.py kontrolü
            if internal_exists:
                main_path = os.path.join(internal_program_path, "main.py")
                print(f"    Main.py: {'✅' if os.path.exists(main_path) else '❌'} {main_path}")
        
        print("=" * 60)
    
    def setup_resource_path(self):
        """PyInstaller için resource path'i ayarlar"""
        try:
            # PyInstaller'ın oluşturduğu geçici klasör
            self.base_path = sys._MEIPASS
            self.is_frozen = True
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Frozen mode detected. Base path: {self.base_path}")
        except Exception:
            # Normal çalışma durumu
            self.base_path = os.path.abspath(".")
            self.is_frozen = False
            self.logger = logging.getLogger(__name__)
            self.logger.info(f"Normal mode. Base path: {self.base_path}")
    
    def get_resource_path(self, relative_path):
        """Göreceli yolu absolute path'e çevirir"""
        # Frozen durumunda önce MEIPASS'ta ara, sonra çalışma dizininde
        if self.is_frozen:
            meipass_path = os.path.join(self.base_path, relative_path)
            if os.path.exists(meipass_path):
                return meipass_path
        
        # Normal çalışma durumu veya MEIPASS'ta bulunamazsa
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
            self.logger.info(f"Klasör oluşturuldu/doğrulandı: {full_path}")
    
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
                    self.logger.info("Kullanıcı ayarları yüklendi.")
        except Exception as e:
            self.logger.error(f"Ayarlar yüklenirken hata: {str(e)}")
    
    def save_settings(self):
        """Kullanıcı ayarlarını kaydeder"""
        try:
            settings_path = self.get_resource_path("config/user_settings.json")
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=4)
            self.logger.info("Kullanıcı ayarları kaydedildi.")
        except Exception as e:
            self.logger.error(f"Ayarlar kaydedilirken hata: {str(e)}")
    
    def setup_color_palette(self):
        """Light ve dark mod için merkezi renk paleti"""
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
        """Mevcut temaya göre renk döndürür"""
        return self.colors[self.appearance_mode][color_key]
    
    def load_logo(self):
        """Logoyu yükler ve CTkImage olarak döndürür"""
        try:
            logo_path = self.get_resource_path("icon/bupilic_logo.png")
            if os.path.exists(logo_path):
                pil_image = Image.open(logo_path)
                # CTkImage kullanarak yükle (HighDPI desteği için)
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
        """Giriş ekranını gösterir"""
        self.clear_window()
        
        login_frame = ctk.CTkFrame(self.root, fg_color=self.get_color("background"))
        login_frame.pack(expand=True, fill="both", padx=100, pady=100)
        
        # Logo/Başlık
        title_label = ctk.CTkLabel(login_frame, text="BUPİLİÇ", 
                                 font=ctk.CTkFont(size=32, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(50, 20))
        
        subtitle_label = ctk.CTkLabel(login_frame, text="İşletme Yönetim Sistemi", 
                                    font=ctk.CTkFont(size=18),
                                    text_color=self.get_color("text_secondary"))
        subtitle_label.pack(pady=(0, 50))
        
        # Şifre girişi
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
        
        # Giriş butonu
        login_btn = ctk.CTkButton(password_frame, text="Giriş Yap", 
                                command=self.check_login,
                                height=40,
                                width=150,
                                fg_color=self.get_color("button"),
                                hover_color=self.get_color("button_hover"),
                                font=ctk.CTkFont(size=14, weight="bold"))
        login_btn.pack(pady=20)
        
        # Hata mesajı
        self.login_error_label = ctk.CTkLabel(password_frame, text="", 
                                            text_color="red",
                                            font=ctk.CTkFont(size=12))
        self.login_error_label.pack()
    
    def check_login(self):
        """Şifreyi kontrol eder"""
        password = self.password_entry.get()
        if password == self.user_data["password"]:
            self.logger.info("Kullanıcı giriş yaptı.")
            self.setup_ui()
        else:
            self.login_error_label.configure(text="Hatalı şifre! Lütfen tekrar deneyin.")
            self.logger.warning("Hatalı şifre girişimi.")
    
    def setup_ui(self):
        """Ana arayüzü kurar"""
        self.clear_window()
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        # Logoyu yükle
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
        
        # Logo ve başlık
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
            ("🐛 Debug", self.show_debug_info),
            ("🔄 Test All", self.test_all_subprograms)
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
        """Ayarlar panelini gösterir"""
        self.clear_main_content()
        
        settings_frame = ctk.CTkFrame(self.main, fg_color=self.get_color("background"))
        settings_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title_label = ctk.CTkLabel(settings_frame, text="⚙️ Kullanıcı Ayarları", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(0, 30))
        
        # Kullanıcı bilgileri formu
        form_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        form_frame.pack(pady=20)
        
        # İsim
        ctk.CTkLabel(form_frame, text="İsim:", 
                   font=ctk.CTkFont(size=14),
                   text_color=self.get_color("text")).grid(row=0, column=0, sticky="w", pady=10)
        
        self.name_entry = ctk.CTkEntry(form_frame, 
                                     width=250,
                                     height=40,
                                     font=ctk.CTkFont(size=14))
        self.name_entry.insert(0, self.user_data["name"])
        self.name_entry.grid(row=0, column=1, padx=20, pady=10)
        
        # Pozisyon
        ctk.CTkLabel(form_frame, text="Pozisyon:", 
                   font=ctk.CTkFont(size=14),
                   text_color=self.get_color("text")).grid(row=1, column=0, sticky="w", pady=10)
        
        self.position_entry = ctk.CTkEntry(form_frame, 
                                         width=250,
                                         height=40,
                                         font=ctk.CTkFont(size=14))
        self.position_entry.insert(0, self.user_data["position"])
        self.position_entry.grid(row=1, column=1, padx=20, pady=10)
        
        # Şifre değiştirme
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
        
        # Kaydet butonu
        save_btn = ctk.CTkButton(form_frame, text="Kaydet", 
                               command=self.save_user_settings,
                               height=45,
                               width=200,
                               fg_color=self.get_color("button"),
                               hover_color=self.get_color("button_hover"),
                               font=ctk.CTkFont(size=15, weight="bold"))
        save_btn.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Geri butonu
        back_btn = ctk.CTkButton(settings_frame, text="← Geri", 
                               command=self.setup_main_content,
                               height=40,
                               width=120,
                               fg_color="transparent",
                               font=ctk.CTkFont(size=13))
        back_btn.pack(pady=20)
    
    def save_user_settings(self):
        """Kullanıcı ayarlarını kaydeder"""
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
        
        # Tema ayarını da kaydet
        self.user_data["theme"] = self.appearance_mode
        
        self.save_settings()
        self.show_message("Ayarlar kaydedildi!")
        self.logger.info("Kullanıcı ayarları güncellendi.")
    
    def clear_window(self):
        """Pencereyi temizler"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_main_content(self):
        """Ana içeriği temizler"""
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
        
        # Tema ayarını kaydet
        self.user_data["theme"] = self.appearance_mode
        self.save_settings()
        self.logger.info(f"Tema değiştirildi: {self.appearance_mode}")
    
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
        """Türkçe tarih formatını döndürür"""
        now = datetime.now()
        
        # Türkçe ay isimları
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
                    # Fallback: İngilizce tarih formatı
                    english_date = datetime.now().strftime("%d %B %Y - %H:%M:%S")
                    self.time_label.configure(text=english_date)
                time.sleep(1)
        
        threading.Thread(target=update, daemon=True).start()
    
    def show_dashboard(self):
        self.clear_main_content()
        self.setup_welcome_section()
        self.setup_quick_access()
        self.logger.info("Ana sayfa gösterildi.")
    
    def run_subprogram(self, program_name, main_file="main.py"):
        """Alt programı çalıştır - KESİN ÇÖZÜM"""
        try:
            print(f"🚀 {program_name} başlatılıyor...")
            
            # 1. ÖNCE FROZEN MOD KONTROLÜ
            if self.is_frozen:
                print("❄️ Frozen modda çalışıyor")
                
                # CRITICAL FIX: MEIPASS yolunu kullan
                program_dir = os.path.join(self.base_path, program_name)
                print(f"📁 MEIPASS program_dir: {program_dir}")
                
                # Alternatif olarak executable dizinini de kontrol et
                exe_dir = os.path.join(os.path.dirname(sys.executable), program_name)
                print(f"📁 EXE program_dir: {exe_dir}")
                
                # Önce MEIPASS'ta ara, bulunamazsa EXE dizininde ara
                if os.path.exists(program_dir):
                    print("✅ MEIPASS'ta bulundu")
                elif os.path.exists(exe_dir):
                    print("✅ EXE dizininde bulundu")
                    program_dir = exe_dir
                else:
                    error_msg = f"❌ {program_name} hiçbir yerde bulunamadı!"
                    print(error_msg)
                    self.show_message(error_msg)
                    return False
                    
            else:
                print("🐍 Normal modda çalışıyor")
                # Normal modda - göreceli yolda
                program_dir = self.get_resource_path(program_name)
                print(f"📁 Normal program_dir: {program_dir}")
            
            # 2. DİZİN KONTROLÜ
            if not os.path.exists(program_dir):
                error_msg = f"❌ {program_name} dizini bulunamadı: {program_dir}"
                print(error_msg)
                self.show_message(error_msg)
                return False
            
            # 3. MAIN DOSYASINI KONTROL ET
            main_path = os.path.join(program_dir, main_file)
            print(f"📄 Main dosya yolu: {main_path}")
            
            if not os.path.exists(main_path):
                error_msg = f"❌ {main_file} bulunamadı: {main_path}"
                print(error_msg)
                
                # Main.py yerine farklı isimde olabilir mi diye kontrol et
                py_files = [f for f in os.listdir(program_dir) if f.endswith('.py')]
                print(f"🔍 Mevcut Python dosyaları: {py_files}")
                
                self.show_message(error_msg)
                return False
            
            # 4. DİZİN İÇERİĞİNİ GÖSTER (DEBUG)
            print(f"📋 Dizin içeriği: {os.listdir(program_dir)}")
            
            # 5. WINDOWS İÇİN KESİN ÇÖZÜM
            if os.name == 'nt':
                print("🪟 Windows işletim sistemi")
                
                # Python executable yolunu al
                python_exe = sys.executable
                print(f"🐍 Python executable: {python_exe}")
                
                # YENİ VE KESİN YÖNTEM: subprocess ile çalıştır
                try:
                    import subprocess
                    
                    # Çalışma dizinini ayarla
                    original_dir = os.getcwd()
                    os.chdir(program_dir)
                    print(f"📂 Çalışma dizini değiştirildi: {os.getcwd()}")
                    
                    # Process'i başlat
                    process = subprocess.Popen(
                        [python_exe, main_file],
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                    
                    print(f"✅ Process başlatıldı: PID {process.pid}")
                    
                    # Çalışma dizinini geri al
                    os.chdir(original_dir)
                    
                    return True
                    
                except Exception as e:
                    error_msg = f"❌ Subprocess hatası: {str(e)}"
                    print(error_msg)
                    
                    # FALLBACK: os.system ile dene
                    try:
                        cmd = f'cd /d "{program_dir}" && "{python_exe}" "{main_file}"'
                        print(f"⚡ Fallback komut: {cmd}")
                        result = os.system(cmd)
                        print(f"✅ Fallback sonuç: {result}")
                        return result == 0
                    except Exception as e2:
                        error_msg = f"❌ Fallback hatası: {str(e2)}"
                        print(error_msg)
                        self.show_message(f"{program_name} açılamadı: {str(e2)}")
                        return False
            else:
                # Linux/Mac
                import subprocess
                subprocess.Popen([sys.executable, main_path], cwd=program_dir)
                print(f"✅ {program_name} Linux/Mac'te başlatıldı")
                return True
                
        except Exception as e:
            error_msg = f"❌ GENEL HATA: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            self.show_message(f"Beklenmeyen hata: {str(e)}")
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
    
    def test_all_subprograms(self):
        """Tüm alt programları test et"""
        print("🧪 Testing all subprograms...")
        
        subprograms = [
            ("ISKONTO_HESABI", "main.py"),
            ("KARLILIK_ANALIZI", "main.py"),
            ("Musteri_Sayisi_Kontrolu", "main.py"),
            ("YASLANDIRMA", "main.py")
        ]
        
        results = []
        for program_name, main_file in subprograms:
            success = self.run_subprogram(program_name, main_file)
            results.append((program_name, success))
            print(f"  {program_name}: {'✅' if success else '❌'}")
            time.sleep(1)  # Her test arasında bekle
        
        print("📊 Test Results:")
        for program_name, success in results:
            print(f"  {program_name}: {'✅ PASS' if success else '❌ FAIL'}")
    
    def show_message(self, message):
        """Basit mesaj gösterimi"""
        print(f"INFO: {message}")
    
    def show_debug_info(self):
        """Debug bilgilerini göster"""
        debug_window = ctk.CTkToplevel(self.root)
        debug_window.title("🐛 Debug Information")
        debug_window.geometry("700x500")
        debug_window.transient(self.root)
        debug_window.grab_set()
        
        info_text = f"""=== BUPİLİÇ DEBUG BİLGİLERİ ===

Base Path: {self.base_path}
Frozen: {self.is_frozen}
Current Directory: {os.getcwd()}
Python Executable: {sys.executable}
Python Version: {sys.version}

Available Subprograms:
"""
        
        subprograms = ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]
        
        for program in subprograms:
            program_path = self.get_resource_path(program)
            exists = os.path.exists(program_path)
            main_file = "main.py"
            main_path = os.path.join(program_path, main_file) if exists else "N/A"
            main_exists = os.path.exists(main_path) if exists else False
            
            info_text += f"\n{program}:"
            info_text += f"\n  - Path: {program_path}"
            info_text += f"\n  - Exists: {'✅' if exists else '❌'}"
            if exists:
                info_text += f"\n  - Main file: {main_path}"
                info_text += f"\n  - Main exists: {'✅' if main_exists else '❌'}"
            
            info_text += "\n"
        
        # Mevcut dosyaları listele
        info_text += f"\nCurrent Directory Files:\n"
        try:
            for item in os.listdir('.'):
                if os.path.isdir(item):
                    info_text += f"📁 {item}/\n"
                else:
                    info_text += f"📄 {item}\n"
        except Exception as e:
            info_text += f"Error listing directory: {e}\n"
        
        textbox = ctk.CTkTextbox(debug_window, width=680, height=450)
        textbox.pack(padx=10, pady=10, fill="both", expand=True)
        textbox.insert("1.0", info_text)
        textbox.configure(state="disabled")
        
        # Kapatma butonu
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
