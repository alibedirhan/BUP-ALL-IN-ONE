# hooks/tkinter_hook.py
import os
import sys

def hook_tkinter():
    """
    Tkinter modülleri için runtime hook.
    commondialog ImportError hatasını çözer.
    """
    try:
        # Tkinter modüllerini manuel olarak yükle
        import tkinter
        import tkinter.filedialog
        import tkinter.messagebox
        import tkinter.ttk
        
        # commondialog için özel yükleme
        try:
            from tkinter import commondialog
            print("[HOOK] tkinter.commondialog successfully imported")
        except ImportError:
            try:
                # Alternatif import yolu
                import tkinter.commondialog as commondialog
                print("[HOOK] tkinter.commondialog imported via alternative path")
            except ImportError:
                # Eğer modül gerçekten yoksa, basit bir implementasyon
                print("[HOOK] Creating dummy commondialog module")
                class Commondialog:
                    """Dummy commondialog class for compatibility"""
                    pass
                
                # Fake module oluştur
                class DummyModule:
                    def __init__(self):
                        self.Dialog = Commondialog
                    
                    def __getattr__(self, name):
                        return Commondialog
                
                sys.modules['tkinter.commondialog'] = DummyModule()
                print("[HOOK] Dummy commondialog module created")
                
    except Exception as e:
        print(f"[HOOK ERROR] Tkinter hook failed: {e}")

# Hook'u çalıştır
hook_tkinter()