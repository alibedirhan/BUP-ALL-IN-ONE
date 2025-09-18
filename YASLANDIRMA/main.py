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
