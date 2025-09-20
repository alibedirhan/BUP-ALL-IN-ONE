import os
import sys

# FROZEN DURUMU İÇİN KRİTİK AYAR
if getattr(sys, 'frozen', False):
    # PyInstaller ile paketlenmişse
    base_path = sys._MEIPASS
    program_path = os.path.join(base_path, os.path.basename(os.path.dirname(__file__)))
    
    # Çalışma dizinini AYNI SEVİYEDE olacak şekilde ayarla
    target_dir = os.path.dirname(sys.executable)
    target_program_dir = os.path.join(target_dir, os.path.basename(os.path.dirname(__file__)))
    
    # Eğer hedef dizin yoksa oluştur ve kopyala
    if not os.path.exists(target_program_dir):
        import shutil
        shutil.copytree(program_path, target_program_dir)
    
    os.chdir(target_program_dir)
else:
    # Normal Python ortamında çalışıyorsa
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Çalışma dizini: {os.getcwd()}")
print(f"Mevcut dosyalar: {os.listdir('.')}")

# GERİ KALAN KODLARINIZ BURADAN SONRA GELMELİ

import customtkinter as ctk
import sys
import os

class Program:
    def __init__(self, title):
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("600x400")
        
        # Ana frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Başlık
        title_label = ctk.CTkLabel(main_frame, text=title, 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=20)
        
        # İçerik
        info_label = ctk.CTkLabel(main_frame, 
                                 text="Bu modül henüz geliştirilme aşamasındadır.",
                                 font=ctk.CTkFont(size=14))
        info_label.pack(pady=10)
        
        # Kapat butonu
        close_btn = ctk.CTkButton(main_frame, text="Kapat", 
                                 command=self.root.quit,
                                 width=200, height=40)
        close_btn.pack(pady=30)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Program("Yaşlandırma Raporları")
    app.run()
