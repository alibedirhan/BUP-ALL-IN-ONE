# -*- coding: utf-8 -*-
import os
import sys
import subprocess
import importlib
import threading
import time
from pathlib import Path

# PyInstaller için path ayarları
if getattr(sys, 'frozen', False):
    # Frozen modda çalışıyoruz
    base_path = sys._MEIPASS
    # Alt modülleri path'e ekle
    for module in ["ISKONTO_HESABI", "KARLILIK_ANALIZI", "Musteri_Sayisi_Kontrolu", "YASLANDIRMA"]:
        module_path = os.path.join(base_path, module)
        if os.path.exists(module_path) and module_path not in sys.path:
            sys.path.insert(0, module_path)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

# GUI imports
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

def run_embedded_program(program_name):
    """Alt programı çalıştır"""
    print(f"[START] Starting {program_name}...")
    print(f"[DEBUG] sys.path = {sys.path}")

    try:
        if program_name == "ISKONTO_HESABI":
            print("[DEBUG] importing ISKONTO_HESABI.main")
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
        print(f"[ERROR] Error running {program_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

    return False


class BupilicDashboard:
    def __init__(self):
        # Türkçe locale ayarları
        try:
            locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
        except:
            try:
                locale.setlocale(locale.LC_TIME, 'Turkish_Turkey.1254')
            except:
                pass
        
        self.root = ctk.CTk()
        self.root.title("BupiliÇ İşletme Yönetim Sistemi")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # PyInstaller için resource path
        self.setup_resource_path()
        
        # Klasör yapısını oluştur
        self.setup_directories()
        
        # Loglama
        self.logger = self.setup_logging()
        self.logger.info("Uygulama başlatıldı")
        
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
        
        # Renk paleti
        self.setup_color_palette()
        
        # Logo referansı
        self.logo_image = None
        
        # Login ekranını göster
        self.show_login_screen()
    
    def setup_resource_path(self):
        """PyInstaller için resource path ayarları"""
        try:
            self.base_path = sys._MEIPASS
            self.is_frozen = True
        except:
            self.base_path = os.path.abspath(".")
            self.is_frozen = False
    
    def get_resource_path(self, relative_path):
        """Resource path'i döndür"""
        if self.is_frozen:
            path = os.path.join(self.base_path, relative_path)
            if os.path.exists(path):
                return path
        return os.path.join(os.path.abspath("."), relative_path)
    
    def setup_directories(self):
        """Gerekli klasörleri oluştur"""
        directories = ['data/input', 'data/output', 'config', 'logs', 'temp']
        for directory in directories:
            os.makedirs(self.get_resource_path(directory), exist_ok=True)
    
    def setup_logging(self):
        """Loglama sistemi"""
        log_dir = self.get_resource_path("logs")
        os.makedirs(log_dir, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
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
        """Renk döndür"""
        return self.colors[self.appearance_mode][color_key]
    
    def load_logo(self):
        """Logo yükle"""
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
        except:
            pass
        return None
    
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
            self.logger.info("Giriş başarılı")
            self.setup_ui()
        else:
            self.login_error_label.configure(text="Hatalı şifre!")
    
    def setup_ui(self):
        """Ana UI"""
        self.clear_window()
        
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.logo_image = self.load_logo()
        
        self.setup_header()
        self.setup_sidebar()
        self.setup_main_content()
    
    def setup_header(self):
        """Üst başlık"""
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
        
        title_label = ctk.CTkLabel(left_frame, text="BUPİLİÇ", 
                                   font=ctk.CTkFont(size=26, weight="bold"),
                                   text_color="white")
        title_label.pack(side="left")
    
    def setup_sidebar(self):
        """Sol menü"""
        self.sidebar = ctk.CTkFrame(self.root, width=220, 
                                  fg_color=self.get_color("primary"), 
                                  corner_radius=0)
        self.sidebar.grid(row=1, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        user_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        user_frame.pack(pady=30, padx=10, fill="x")
        
        ctk.CTkLabel(user_frame, text="Kullanıcı", 
                   font=ctk.CTkFont(size=14),
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
            ("Ana Sayfa", self.show_dashboard),
            ("İskonto Hesaplama", self.iskonto_ac),
            ("Karlılık Analizi", self.karlilik_ac),
            ("Müşteri Kayıp/Kaçak", self.musteri_kayip_ac),
            ("Yaşlandırma", self.yaslandirma_ac),
            ("Ayarlar", self.show_settings),
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
        
        self.setup_welcome_section()
        self.setup_quick_access()
    
    def setup_welcome_section(self):
        """Hoşgeldin bölümü"""
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
        """Hızlı erişim butonları - TÜM 4 PROGRAM"""
        quick_frame = ctk.CTkFrame(self.main, fg_color="transparent")
        quick_frame.pack(expand=True, pady=20)
        
        self.title_label = ctk.CTkLabel(quick_frame, text="Hızlı Erişim", 
                                 font=ctk.CTkFont(size=20, weight="bold"),
                                 text_color=self.get_color("text"))
        self.title_label.pack(pady=(0, 30))
        
        main_buttons_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        main_buttons_frame.pack()
        
        # TÜM 4 PROGRAM İÇİN BUTONLAR
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
                "İskonto Hesaplama": "İskontolarınızı hesapla",
                "Karlılık Analizi": "Şube karlılık analizleri",
                "Müşteri Kayıp/Kaçak": "Müşteri kayıp/kaçak analizleri",
                "Yaşlandırma": "Yaşlandırma raporları"
            }
            
            desc_label = ctk.CTkLabel(btn_frame, 
                                    text=descriptions.get(text, ""),
                                    font=ctk.CTkFont(size=12),
                                    text_color=self.get_color("text_secondary"))
            desc_label.pack(pady=(5, 0))
            self.desc_labels.append(desc_label)
    
    def show_settings(self):
        """Ayarlar ekranı"""
        self.clear_main_content()
        
        settings_frame = ctk.CTkFrame(self.main, fg_color=self.get_color("background"))
        settings_frame.pack(expand=True, fill="both", padx=50, pady=50)
        
        title_label = ctk.CTkLabel(settings_frame, text="Kullanıcı Ayarları", 
                                 font=ctk.CTkFont(size=24, weight="bold"),
                                 text_color=self.get_color("text"))
        title_label.pack(pady=(0, 30))
        
        back_btn = ctk.CTkButton(settings_frame, text="Geri", 
                               command=self.setup_main_content,
                               height=40,
                               width=120,
                               fg_color="transparent",
                               font=ctk.CTkFont(size=13))
        back_btn.pack(pady=20)
    
    def clear_window(self):
        """Pencereyi temizle"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def clear_main_content(self):
        """Ana içeriği temizle"""
        for widget in self.main.winfo_children():
            widget.destroy()
    
    def darken_color(self, color):
        """Rengi koyulaştır"""
        color_map = {
            "#E63946": "#C1121F",
            "#457B9D": "#1D3557",
            "#2A9D8F": "#1D7874",
            "#F4A261": "#E76F51"
        }
        return color_map.get(color, color)
    
    def show_dashboard(self):
        """Ana sayfaya dön"""
        self.clear_main_content()
        self.setup_welcome_section()
        self.setup_quick_access()
    
    def iskonto_ac(self):
        """İskonto programını aç"""
        print("[INFO] İskonto programı başlatılıyor...")
        success = run_embedded_program("ISKONTO_HESABI")
        if not success:
            self.show_message("İskonto programı başlatılamadı!")
    
    def karlilik_ac(self):
        """Karlılık programını aç"""
        print("[INFO] Karlılık analizi başlatılıyor...")
        success = run_embedded_program("KARLILIK_ANALIZI")
        if not success:
            self.show_message("Karlılık analizi başlatılamadı!")
    
    def musteri_kayip_ac(self):
        """Müşteri kayıp programını aç"""
        print("[INFO] Müşteri kayıp/kaçak programı başlatılıyor...")
        success = run_embedded_program("Musteri_Sayisi_Kontrolu")
        if not success:
            self.show_message("Müşteri programı başlatılamadı!")
    
    def yaslandirma_ac(self):
        """Yaşlandırma programını aç"""
        print("[INFO] Yaşlandırma programı başlatılıyor...")
        success = run_embedded_program("YASLANDIRMA")
        if not success:
            self.show_message("Yaşlandırma programı başlatılamadı!")
    
    def show_message(self, message):
        """Mesaj göster"""
        print(f"[MSG] {message}")
        # Popup mesaj göster
        popup = ctk.CTkToplevel(self.root)
        popup.title("Bilgi")
        popup.geometry("300x150")
        
        ctk.CTkLabel(popup, text=message, 
                    font=ctk.CTkFont(size=14)).pack(pady=30)
        
        ctk.CTkButton(popup, text="Tamam", 
                     command=popup.destroy).pack()
    
    def run(self):
        """Uygulamayı çalıştır"""
        self.root.mainloop()

if __name__ == "__main__":
    app = BupilicDashboard()
    app.run()
