import os
import sys
import time

print("=" * 50)
print(f"🚀 Starting {os.path.basename(os.path.dirname(__file__))}")
print("=" * 50)

# FROZEN DURUMU İÇİN KRİTİK AYAR
if getattr(sys, 'frozen', False):
    print("❄️ Frozen mode detected")
    
    # 1. MEIPASS yolunu al
    base_path = sys._MEIPASS
    print(f"📦 MEIPASS: {base_path}")
    
    # 2. Programın kendi yolunu bul
    current_dir_name = os.path.basename(os.path.dirname(__file__))
    source_program_path = os.path.join(base_path, current_dir_name)
    
    # 3. Hedef yol (ana EXE ile aynı dizin)
    target_base_path = os.path.dirname(sys.executable)
    target_program_path = os.path.join(target_base_path, current_dir_name)
    
    print(f"🎯 Source: {source_program_path}")
    print(f"🎯 Target: {target_program_path}")
    
    # 4. Eğer hedefte yoksa KOPYALA
    if not os.path.exists(target_program_path):
        print("📋 Copying program files...")
        import shutil
        
        try:
            shutil.copytree(source_program_path, target_program_path)
            print("✅ Copy successful")
        except Exception as e:
            print(f"❌ Copy failed: {e}")
    
    # 5. Çalışma dizinini AYNI SEVİYEDE olacak şekilde ayarla
    os.chdir(target_program_path)
    
else:
    # Normal mod
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"📂 Working directory: {os.getcwd()}")
print(f"📄 Files here: {os.listdir('.')}")
print("=" * 50)
time.sleep(1)  # Debug için bekle

# GERİ KALAN KODLARINIZ BURADAN SONRA GELMELİ

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import queue
import logging
import os
from datetime import datetime
from karlilik import KarlilikAnalizi


class BupilicKarlilikGUI:
    def __init__(self):
        # Ana pencere oluştur
        self.root = tk.Tk()
        self.root.title("Bupiliç Karlılık Analizi - CAL")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        self.root.resizable(True, True)
        
        # Logging setup
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Thread-safe communication için queue
        self.result_queue = queue.Queue()
        self.is_processing = False
        self._closing = False
        
        # GUI state variables - ÖNCELİKLE TANIMLA
        self.karlilik_path = tk.StringVar()
        self.iskonto_path = tk.StringVar()
        
        # Widget references - ÖNCELİKLE TANIMLA
        self.karlilik_display = None
        self.iskonto_display = None
        self.process_btn = None
        self.result_text = None
        self.notebook = None
        self.main_tab = None
        
        # Karlılık analizi instance
        self.analiz = KarlilikAnalizi(
            progress_callback=self.thread_safe_update_progress,
            log_callback=self.thread_safe_log_message
        )
        
        # Dashboard ve analiz sonucu referansları
        self.analiz_sonucu = None
        self.dashboard = None
        self.zaman_analizi = None
        
        # Modern stil kurulumu
        self.setup_style()
        
        # UI bileşenlerini oluştur
        self.setup_ui()
        
        # Queue kontrol timer'ını başlat
        self.check_queue()
        
        # Graceful shutdown setup
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def thread_safe_update_progress(self, value, status):
        """Thread-safe progress güncelleme"""
        if not self._closing:
            try:
                # Thread-safe queue put
                self.result_queue.put(('progress', {'value': value, 'status': status}))
            except Exception as e:
                self.logger.debug(f"Progress queue error: {e}")
    
    def thread_safe_log_message(self, message, msg_type='info'):
        """Thread-safe log mesajı"""
        if not self._closing:
            try:
                # Thread-safe queue put
                self.result_queue.put(('log', {'message': message, 'type': msg_type}))
            except Exception as e:
                self.logger.debug(f"Log queue error: {e}")
    
    def check_queue(self):
        """Thread'den gelen mesajları kontrol et ve işle"""
        if self._closing:
            return
        
        try:
            processed = 0
            while processed < 10:  # Batch processing
                try:
                    message_type, data = self.result_queue.get_nowait()
                    
                    if message_type == 'analysis_complete':
                        self.on_analysis_complete(data)
                    elif message_type == 'analysis_error':
                        self.on_analysis_error(data)
                    elif message_type == 'analysis_cancelled':
                        self.on_analysis_cancelled()
                    elif message_type == 'progress':
                        self.update_progress(data['value'], data['status'])
                    elif message_type == 'log':
                        self.log_message(data['message'], data.get('type', 'info'))
                    
                    processed += 1
                    
                except queue.Empty:
                    break
                except Exception as e:
                    self.logger.error(f"Queue message processing error: {e}")
                    break
                    
        except Exception as e:
            self.logger.error(f"Queue check error: {e}")
        
        # Schedule next check
        if not self._closing:
            try:
                self.root.after(100, self.check_queue)
            except tk.TclError:
                pass
    
    def on_analysis_complete(self, result_data):
        """Analiz tamamlandığında çağrılır"""
        try:
            self.is_processing = False
            self.analiz_sonucu = result_data
            
            self.log_message("✓ Karlılık analizi başarıyla tamamlandı!", 'success')
            
            # Dashboard oluştur
            self.safe_after(lambda: self.create_dashboard_tab())
            
            # Success message
            self.safe_after(lambda: messagebox.showinfo(
                "Başarılı! 🎉",
                "Karlılık analizi tamamlandı!\nSonuç dosyası başarıyla kaydedildi.\n\n📊 Dashboard sekmesinde detaylı analizi görebilirsiniz."
            ))
            
            self.reset_process_button()
            
        except Exception as e:
            self.logger.error(f"Analysis complete handler error: {e}")
            self.on_analysis_error(str(e))
    
    def on_analysis_error(self, error_msg):
        """Analiz hatası oluştuğunda çağrılır"""
        try:
            self.is_processing = False
            self.update_progress(0, f"Hata: {str(error_msg)}")
            self.log_message(f"✗ HATA: {str(error_msg)}", 'error')
            
            # Error message
            self.safe_after(lambda: messagebox.showerror(
                "Hata", f"İşlem sırasında hata oluştu:\n{str(error_msg)}"
            ))
            
            self.reset_process_button()
            
        except Exception as e:
            self.logger.error(f"Error handler error: {e}")
    
    def on_analysis_cancelled(self):
        """Analiz iptal edildiğinde çağrılır"""
        try:
            self.is_processing = False
            self.update_progress(0, "İşlem iptal edildi")
            self.reset_process_button()
            
        except Exception as e:
            self.logger.error(f"Analysis cancelled handler error: {e}")
    
    def safe_after(self, func):
        """Thread-safe after call"""
        try:
            if not self._closing and self.root:
                self.root.after_idle(func)
        except (tk.TclError, AttributeError):
            pass
    
    def reset_process_button(self):
        """Process butonunu varsayılan haline getir"""
        def _reset():
            try:
                if self.process_btn and self.process_btn.winfo_exists():
                    self.process_btn.config(
                        state='normal',
                        text="✨ Analizi Başlat",
                        bg='#fd7e14',
                        cursor='hand2'
                    )
            except (tk.TclError, AttributeError):
                pass
        
        self.safe_after(_reset)
    
    def setup_style(self):
        """TTK stillerini ayarla"""
        try:
            style = ttk.Style()
            
            # Theme selection - güvenli
            try:
                available_themes = style.theme_names()
                if 'clam' in available_themes:
                    style.theme_use('clam')
                elif 'vista' in available_themes:
                    style.theme_use('vista')
                elif 'default' in available_themes:
                    style.theme_use('default')
            except tk.TclError as e:
                self.logger.debug(f"Theme setting warning: {e}")
            
            # Style configuration - güvenli
            try:
                style.configure(
                    'Modern.TButton',
                    font=('Segoe UI', 11),
                    relief='flat',
                    borderwidth=0,
                    focuscolor='none'
                )
                
                style.map('Modern.TButton',
                         background=[('active', '#005a9e'),
                                   ('pressed', '#004080')])
                
                style.configure(
                    'Modern.Horizontal.TProgressbar',
                    background='#007acc',
                    troughcolor='#e1e5e9',
                    borderwidth=0,
                    lightcolor='#007acc',
                    darkcolor='#005a9e'
                )
                
                style.configure(
                    'Modern.TFrame',
                    background='#ffffff',
                    relief='flat',
                    borderwidth=1
                )
                
            except tk.TclError as e:
                self.logger.warning(f"Style configuration warning: {e}")
                
        except Exception as e:
            self.logger.error(f"Style setup error: {e}")
    
    def setup_ui(self):
        """Ana UI bileşenlerini oluştur"""
        try:
            main_container = tk.Frame(self.root, bg='#f8f9fa')
            main_container.pack(fill='both', expand=True, padx=15, pady=15)
            
            self.create_header(main_container)
            
            self.notebook = ttk.Notebook(main_container)
            self.notebook.pack(fill='both', expand=True, pady=(20, 0))
            
            self.main_tab = tk.Frame(self.notebook, bg='#f8f9fa')
            self.notebook.add(self.main_tab, text="🔧 Ana İşlemler")
            
            self.setup_main_tab()
            self.create_time_analysis_tab()
            
        except Exception as e:
            self.logger.error(f"UI setup error: {e}")
            messagebox.showerror("Hata", f"UI oluşturma hatası: {e}")
    
    def create_header(self, parent):
        """Modern header oluştur"""
        try:
            header_frame = tk.Frame(parent, bg='#f8f9fa')
            header_frame.pack(fill='x', pady=(0, 10))
            
            title_canvas = tk.Canvas(
                header_frame, 
                height=100, 
                bg='#f8f9fa', 
                highlightthickness=0
            )
            title_canvas.pack(fill='x')
            
            def draw_header():
                try:
                    if not self._closing and title_canvas.winfo_exists():
                        title_canvas.delete("all")
                        width = title_canvas.winfo_width()
                        height = 100
                        
                        if width > 1:  # Valid width check
                            title_canvas.create_rectangle(0, 0, width, height, fill='#007acc', outline='')
                            title_canvas.create_rectangle(0, 0, width, height, fill='#005a9e', stipple='gray25', outline='')
                            
                            title_canvas.create_text(
                                width//2, 30, 
                                text="🚀 Bupiliç Karlılık Analizi", 
                                font=('Segoe UI', 20, 'bold'), 
                                fill='white', 
                                anchor='center'
                            )
                            title_canvas.create_text(
                                width//2, 60, 
                                text="Karlılık ve İskonto Raporları Eşleştirme Sistemi",
                                font=('Segoe UI', 12), 
                                fill='#b3d9ff', 
                                anchor='center'
                            )
                        
                except (tk.TclError, AttributeError):
                    pass
            
            def resize_canvas(event):
                if not self._closing:
                    try:
                        self.root.after_idle(draw_header)
                    except (tk.TclError, AttributeError):
                        pass
            
            title_canvas.bind('<Configure>', resize_canvas)
            self.safe_after(lambda: self.root.after(100, draw_header))
            
        except Exception as e:
            self.logger.error(f"Header creation error: {e}")
    
    def setup_main_tab(self):
        """Ana sekme içeriğini oluştur"""
        try:
            content_frame = tk.Frame(self.main_tab, bg='#f8f9fa')
            content_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            left_frame = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1)
            left_frame.pack(side='left', fill='y', padx=(0, 15))
            left_frame.config(width=400)
            left_frame.pack_propagate(False)
            
            right_frame = tk.Frame(content_frame, bg='#ffffff', relief='solid', bd=1)
            right_frame.pack(side='right', fill='both', expand=True)
            
            self.create_left_panel(left_frame)
            self.create_right_panel(right_frame)
            
        except Exception as e:
            self.logger.error(f"Main tab setup error: {e}")
    
    def create_left_panel(self, parent):
        """Sol panel (dosya seçimi) oluştur"""
        try:
            panel_header = tk.Frame(parent, bg='#007acc', height=50)
            panel_header.pack(fill='x')
            panel_header.pack_propagate(False)
            
            tk.Label(
                panel_header,
                text="📁 Dosya Seçimi ve İşlemler",
                font=('Segoe UI', 14, 'bold'),
                fg='white',
                bg='#007acc'
            ).pack(expand=True)
            
            content = tk.Frame(parent, bg='#ffffff')
            content.pack(fill='both', expand=True, padx=25, pady=25)
            
            self.create_file_section(content)
            self.create_action_button(content)
            
        except Exception as e:
            self.logger.error(f"Left panel creation error: {e}")
    
    def create_file_section(self, parent):
        """Dosya seçim bölümünü oluştur"""
        try:
            # Karlılık dosyası bölümü
            karlilik_section = tk.LabelFrame(
                parent,
                text="📊 Karlılık Analizi Dosyası",
                font=('Segoe UI', 11, 'bold'),
                fg='#2c3e50',
                bg='#ffffff',
                relief='groove',
                bd=2
            )
            karlilik_section.pack(fill='x', pady=(0, 20))
            
            self.create_file_widget(karlilik_section, 'karlilik', "📂 Karlılık Dosyası Seç", '#007acc')
            
            # İskonto dosyası bölümü
            iskonto_section = tk.LabelFrame(
                parent,
                text="💰 Bupiliç İskonto Raporu",
                font=('Segoe UI', 11, 'bold'),
                fg='#2c3e50',
                bg='#ffffff',
                relief='groove',
                bd=2
            )
            iskonto_section.pack(fill='x', pady=(0, 30))
            
            self.create_file_widget(iskonto_section, 'iskonto', "📂 İskonto Dosyası Seç", '#28a745')
            
        except Exception as e:
            self.logger.error(f"File section creation error: {e}")
    
    def create_file_widget(self, parent, file_type, button_text, button_color):
        """Dosya seçim widget'ını oluştur"""
        try:
            path_frame = tk.Frame(parent, bg='#ffffff')
            path_frame.pack(fill='x', padx=15, pady=15)
            
            file_display = tk.Text(
                path_frame,
                height=3,
                font=('Segoe UI', 9),
                bg='#f8f9fa',
                fg='#555555',
                relief='solid',
                bd=1,
                wrap='word'
            )
            file_display.pack(fill='x', pady=(0, 10))
            file_display.insert('1.0', "Henüz dosya seçilmedi...")
            file_display.config(state='disabled')
            
            # Widget reference'ını sakla
            if file_type == 'karlilik':
                self.karlilik_display = file_display
            else:
                self.iskonto_display = file_display
            
            file_btn = tk.Button(
                path_frame,
                text=button_text,
                command=lambda: self.select_file(file_type),
                bg=button_color,
                fg='white',
                font=('Segoe UI', 10, 'bold'),
                relief='flat',
                bd=0,
                cursor='hand2',
                padx=20,
                pady=10
            )
            file_btn.pack(fill='x')
            
            self.create_button_hover_effect(file_btn, button_color)
            
        except Exception as e:
            self.logger.error(f"File widget creation error: {e}")
    
    def create_button_hover_effect(self, button, normal_color):
        """Buton hover efekti oluştur"""
        try:
            hover_colors = {
                '#007acc': '#005a9e',
                '#28a745': '#218838',
                '#fd7e14': '#e8630e'
            }
            hover_color = hover_colors.get(normal_color, normal_color)
            
            def on_enter(e):
                try:
                    if button.winfo_exists() and not self.is_processing:
                        button.config(bg=hover_color)
                except tk.TclError:
                    pass
            
            def on_leave(e):
                try:
                    if button.winfo_exists() and not self.is_processing:
                        button.config(bg=normal_color)
                except tk.TclError:
                    pass
            
            button.bind("<Enter>", on_enter)
            button.bind("<Leave>", on_leave)
            
        except Exception as e:
            self.logger.debug(f"Button hover effect error: {e}")
    
    def create_action_button(self, parent):
        """Ana işlem butonunu oluştur"""
        try:
            button_frame = tk.Frame(parent, bg='#ffffff')
            button_frame.pack(fill='x', pady=(0, 30))
            
            self.process_btn = tk.Button(
                button_frame,
                text="✨ Analizi Başlat",
                command=self.start_analysis,
                bg='#fd7e14',
                fg='white',
                font=('Segoe UI', 14, 'bold'),
                relief='flat',
                bd=0,
                cursor='hand2',
                pady=15
            )
            self.process_btn.pack(fill='x')
            
            self.create_button_hover_effect(self.process_btn, '#fd7e14')
            
        except Exception as e:
            self.logger.error(f"Action button creation error: {e}")
    
    def create_right_panel(self, parent):
        """Sağ panel (sonuçlar) oluştur"""
        try:
            panel_header = tk.Frame(parent, bg='#007acc', height=50)
            panel_header.pack(fill='x')
            panel_header.pack_propagate(False)
            
            tk.Label(
                panel_header,
                text="📝 İşlem Sonuçları ve Loglar",
                font=('Segoe UI', 14, 'bold'),
                fg='white',
                bg='#007acc'
            ).pack(expand=True)
            
            log_frame = tk.Frame(parent, bg='#ffffff')
            log_frame.pack(fill='both', expand=True, padx=20, pady=20)
            
            text_container = tk.Frame(log_frame, bg='#ffffff')
            text_container.pack(fill='both', expand=True)
            
            self.result_text = tk.Text(
                text_container,
                font=('Consolas', 10),
                bg='#2c3e50',
                fg='#ecf0f1',
                relief='flat',
                bd=0,
                wrap='word',
                padx=15,
                pady=15
            )
            
            scrollbar = tk.Scrollbar(text_container, orient='vertical', command=self.result_text.yview)
            self.result_text.configure(yscrollcommand=scrollbar.set)
            
            self.result_text.pack(side='left', fill='both', expand=True)
            scrollbar.pack(side='right', fill='y')
            
            self.setup_welcome_message()
            self.setup_text_tags()
            
        except Exception as e:
            self.logger.error(f"Right panel creation error: {e}")
    
    def setup_welcome_message(self):
        """Hoşgeldin mesajını ayarla"""
        try:
            welcome_msg = """🚀 Bupiliç Karlılık Analizi Sistemine Hoşgeldiniz!

✨ Bu sistem karlılık analizi ve iskonto raporlarınızı eşleştirerek:
   • Birim maliyetleri hesaplar
   • Kar marjlarını analiz eder  
   • En karlı ürünleri belirler
   • Detaylı Excel raporları oluşturur

📋 Kullanım Adımları:
   1. Sol panelden karlılık analizi Excel dosyasını seçin
   2. Bupiliç iskonto raporu dosyasını seçin
   3. "Analizi Başlat" butonuna tıklayın
   4. İşlem tamamlandığında sonuç dosyasını kaydedin

🎯 Sistem hazır. Dosyalarınızı seçerek başlayabilirsiniz.

📅 YENİ: Dönem analizi özelliği eklendi! 
   • Tarih aralıkları ile analiz kaydetme
   • Dönemsel karşılaştırma 
   • Trend analizi
   "Dönem Analizi" sekmesini kontrol edin!
"""
            
            self.result_text.insert('1.0', welcome_msg)
            self.result_text.config(state='disabled')
            
        except Exception as e:
            self.logger.error(f"Welcome message setup error: {e}")
    
    def setup_text_tags(self):
        """Text widget için renk etiketlerini ayarla"""
        try:
            self.result_text.tag_config('success', foreground='#2ecc71', font=('Consolas', 10, 'bold'))
            self.result_text.tag_config('error', foreground='#e74c3c', font=('Consolas', 10, 'bold'))
            self.result_text.tag_config('warning', foreground='#f39c12', font=('Consolas', 10, 'bold'))
            self.result_text.tag_config('info', foreground='#3498db', font=('Consolas', 10))
            
        except Exception as e:
            self.logger.error(f"Text tags setup error: {e}")
    
    def create_time_analysis_tab(self):
        """Zaman analizi sekmesini oluştur"""
        try:
            from zaman_analizi import ZamanAnalizi
            
            self.zaman_analizi = ZamanAnalizi(self.notebook)
            self.log_message("✓ Dönem analizi modülü başarıyla yüklendi!", 'success')
            
        except ImportError as e:
            self.logger.warning(f"Time analysis module import error: {e}")
            self.log_message(f"✗ Dönem analizi modülü yüklenemedi: {str(e)}", 'error')
            self.create_error_tab("📅 Dönem Analizi (Hata)", str(e))
            
        except Exception as e:
            self.logger.error(f"Time analysis creation error: {e}")
            self.log_message(f"✗ Dönem analizi oluşturma hatası: {str(e)}", 'error')
    
    def create_error_tab(self, tab_title, error_message):
        """Hata sekmesi oluştur"""
        try:
            error_frame = ttk.Frame(self.notebook)
            self.notebook.add(error_frame, text=tab_title)
            
            error_container = tk.Frame(error_frame, bg='#f8fafc')
            error_container.pack(fill='both', expand=True, padx=20, pady=20)
            
            tk.Label(
                error_container,
                text="❌ Modül Yüklenemedi",
                font=('Segoe UI', 16, 'bold'),
                fg='#ef4444',
                bg='#f8fafc'
            ).pack(pady=(50, 20))
            
            tk.Label(
                error_container,
                text=f"Hata detayı: {error_message}",
                font=('Segoe UI', 12),
                fg='#6b7280',
                bg='#f8fafc'
            ).pack()
            
            tk.Label(
                error_container,
                text="Lütfen gerekli dosyaların mevcut olduğundan\nve kütüphanelerin yüklü olduğundan emin olun.",
                font=('Segoe UI', 11),
                fg='#6b7280',
                bg='#f8fafc',
                justify='center'
            ).pack(pady=20)
            
        except Exception as e:
            self.logger.error(f"Error tab creation error: {e}")
    
    def select_file(self, file_type):
        """Dosya seçimi işlemi"""
        try:
            title = "Karlılık Analizi Dosyasını Seçin" if file_type == 'karlilik' else "Bupiliç İskonto Raporu Dosyasını Seçin"
            
            filename = filedialog.askopenfilename(
                title=title,
                filetypes=[("Excel dosyaları", "*.xlsx *.xls"), ("Tüm dosyalar", "*.*")]
            )
            
            if filename:
                # Path variable'ını güncelle
                if file_type == 'karlilik':
                    self.karlilik_path.set(filename)
                    display_widget = self.karlilik_display
                else:
                    self.iskonto_path.set(filename)
                    display_widget = self.iskonto_display
                
                # Display widget'ını güvenli şekilde güncelle
                if display_widget is not None:
                    try:
                        if display_widget.winfo_exists():
                            display_widget.config(state='normal')
                            display_widget.delete('1.0', 'end')
                            
                            # Dosya yolunu güvenli şekilde kısalt
                            filename_display = os.path.basename(filename)
                            if len(filename) > 80:
                                path_display = f"{filename[:40]}...{filename[-40:]}"
                            else:
                                path_display = filename
                            
                            display_widget.insert('1.0', f"✅ Seçilen dosya:\n{filename_display}\n\n📍 Tam yol: {path_display}")
                            display_widget.config(state='disabled')
                            
                            self.log_message(f"✓ {file_type.title()} dosyası seçildi: {filename_display}", 'success')
                        else:
                            self.logger.warning(f"Display widget does not exist for {file_type}")
                            
                    except tk.TclError as e:
                        self.logger.error(f"Display update error for {file_type}: {e}")
                else:
                    self.logger.warning(f"Display widget is None for {file_type}")
                    
        except Exception as e:
            self.logger.error(f"File selection error: {e}")
            messagebox.showerror("Hata", f"Dosya seçim hatası: {e}")
    
    def log_message(self, message, msg_type='info'):
        """Log mesajı ekle"""
        try:
            if self._closing or not self.result_text:
                return
            
            # Widget existence check
            if not self.result_text.winfo_exists():
                return
                
            self.result_text.config(state='normal')
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            icons = {
                'success': '✅',
                'error': '❌',
                'warning': '⚠️',
                'info': 'ℹ️'
            }
            
            icon = icons.get(msg_type, 'ℹ️')
            formatted_message = f"\n[{timestamp}] {icon} {message}"
            
            start_pos = self.result_text.index('end-1c')
            self.result_text.insert('end', formatted_message)
            end_pos = self.result_text.index('end-1c')
            
            self.result_text.tag_add(msg_type, start_pos, end_pos)
            
            self.result_text.see('end')
            self.result_text.config(state='disabled')
            
        except tk.TclError:
            pass
        except Exception as e:
            self.logger.error(f"Log message error: {e}")
    
    def update_progress(self, value, status):
        """Progress durumunu güncelle"""
        try:
            if status and not self._closing:
                self.log_message(f"İlerleme %{value:.0f}: {status}", 'info')
        except Exception as e:
            self.logger.debug(f"Progress update error: {e}")
    
    def start_analysis(self):
        """Analizi başlat"""
        try:
            if self.is_processing:
                return
            
            # File validation
            karlilik_path = self.karlilik_path.get()
            iskonto_path = self.iskonto_path.get()
            
            if not karlilik_path or not iskonto_path:
                messagebox.showwarning(
                    "Eksik Dosya",
                    "Lütfen hem karlılık analizi hem de iskonto raporu dosyalarını seçin!"
                )
                return
            
            if not os.path.exists(karlilik_path):
                messagebox.showerror("Hata", "Karlılık dosyası bulunamadı!")
                return
            
            if not os.path.exists(iskonto_path):
                messagebox.showerror("Hata", "İskonto dosyası bulunamadı!")
                return
            
            self.is_processing = True
            
            # Update button state
            try:
                if self.process_btn and self.process_btn.winfo_exists():
                    self.process_btn.config(
                        state='disabled',
                        text="⏳ İşlem Devam Ediyor...",
                        bg='#6c757d',
                        cursor='arrow'
                    )
            except (tk.TclError, AttributeError):
                pass
            
            # Start analysis in separate thread
            analysis_thread = threading.Thread(
                target=self.run_analysis,
                daemon=True,
                name="AnalysisThread"
            )
            analysis_thread.start()
            
        except Exception as e:
            self.logger.error(f"Start analysis error: {e}")
            self.is_processing = False
            self.reset_process_button()
            messagebox.showerror("Hata", f"Analiz başlatma hatası: {e}")
    
    def run_analysis(self):
        """Thread-safe analiz fonksiyonu"""
        try:
            self.logger.info("Analysis thread started")
            
            # Get file paths
            karlilik_path = self.karlilik_path.get()
            iskonto_path = self.iskonto_path.get()
            
            if not karlilik_path or not iskonto_path:
                self.result_queue.put(('analysis_error', "Dosya yolları bulunamadı"))
                return
            
            # Run analysis
            analiz_sonucu = self.analiz.analyze(karlilik_path, iskonto_path)
            
            if analiz_sonucu is not None and not analiz_sonucu.empty:
                self.result_queue.put(('analysis_complete', analiz_sonucu))
                self.logger.info("Analysis completed successfully")
            else:
                self.result_queue.put(('analysis_cancelled', None))
                self.logger.warning("Analysis cancelled or returned empty result")
                
        except Exception as e:
            self.logger.error(f"Analysis thread error: {e}")
            self.result_queue.put(('analysis_error', str(e)))
        finally:
            self.logger.info("Analysis thread finished")
    
    def create_dashboard_tab(self):
        """Dashboard sekmesini oluştur"""
        try:
            try:
                from analiz_dashboard import AnalyzDashboard
            except ImportError as e:
                self.log_message(f"✗ Dashboard modülü bulunamadı: {str(e)}", 'error')
                return
            
            if self.analiz_sonucu is None or self.analiz_sonucu.empty:
                self.log_message("✗ Dashboard için analiz sonucu bulunamadı!", 'error')
                return
            
            # Remove existing dashboard
            self.remove_existing_dashboard()
            
            # Create new dashboard
            self.dashboard = AnalyzDashboard(self.notebook, self.analiz_sonucu)
            
            dashboard_frame = self.dashboard.get_frame()
            if dashboard_frame:
                self.notebook.add(dashboard_frame, text="📊 Analiz Dashboard")
                
                # Select dashboard tab
                try:
                    self.notebook.select(dashboard_frame)
                except tk.TclError:
                    pass
                
                self.log_message("✓ Dashboard gerçek verilerle oluşturuldu!", 'success')
                self.log_message(f"📊 {len(self.analiz_sonucu)} ürün analiz edildi", 'info')
            else:
                self.log_message("✗ Dashboard frame oluşturulamadı!", 'error')
            
        except Exception as e:
            self.logger.error(f"Dashboard creation error: {e}")
            self.log_message(f"✗ Dashboard oluşturma hatası: {str(e)}", 'error')
    
    def remove_existing_dashboard(self):
        """Mevcut dashboard sekmesini kaldır"""
        try:
            if self.dashboard:
                # Find and remove dashboard tab
                tab_list = self.notebook.tabs()
                for tab_id in tab_list:
                    try:
                        tab_text = self.notebook.tab(tab_id, "text")
                        if tab_text == "📊 Analiz Dashboard":
                            self.notebook.forget(tab_id)
                            break
                    except tk.TclError:
                        continue
                
                # Cleanup dashboard
                if hasattr(self.dashboard, 'cleanup'):
                    try:
                        self.dashboard.cleanup()
                    except Exception as e:
                        self.logger.debug(f"Dashboard cleanup error: {e}")
                
                self.dashboard = None
                
        except Exception as e:
            self.logger.debug(f"Dashboard removal error (expected): {e}")
    
    def on_closing(self):
        """Uygulama kapanış işlemi"""
        try:
            self.logger.info("Application closing...")
            self._closing = True
            self.is_processing = False
            
            # Wait for analysis threads to finish
            active_threads = [t for t in threading.enumerate() if t.name == "AnalysisThread" and t.is_alive()]
            for thread in active_threads:
                if thread.is_alive():
                    self.logger.info(f"Waiting for thread {thread.name} to finish...")
                    thread.join(timeout=2.0)
                    if thread.is_alive():
                        self.logger.warning(f"Thread {thread.name} did not finish in time")
            
            # Cleanup dashboard
            try:
                if self.dashboard and hasattr(self.dashboard, 'cleanup'):
                    self.dashboard.cleanup()
            except Exception as e:
                self.logger.debug(f"Dashboard cleanup error: {e}")
            
            # Cleanup zaman analizi
            try:
                if self.zaman_analizi and hasattr(self.zaman_analizi, 'cleanup'):
                    self.zaman_analizi.cleanup()
            except Exception as e:
                self.logger.debug(f"ZamanAnalizi cleanup error: {e}")
            
            # Destroy GUI
            try:
                self.root.quit()
                self.root.destroy()
            except tk.TclError:
                pass
                
        except Exception as e:
            self.logger.error(f"Closing error: {e}")
        finally:
            import sys
            sys.exit(0)
    
    def run(self):
        """Ana uygulama döngüsünü başlat"""
        try:
            self.logger.info("Starting GUI application...")
            self.root.mainloop()
        except KeyboardInterrupt:
            self.logger.info("Keyboard interrupt received")
            self.on_closing()
        except Exception as e:
            self.logger.error(f"Main loop error: {e}")
            self.on_closing()


def main():
    app = BupilicKarlilikGUI()  # doğru sınıf adı bu
    app.run()

if __name__ == "__main__":
    main()
