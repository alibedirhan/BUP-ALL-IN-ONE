# hooks/tkinter_hook.py (runtime hook)
# Keep it minimal: just pre-import common tkinter submodules so PyInstaller bundles them.
try:
    import tkinter
    import tkinter.filedialog  # file dialogs
    import tkinter.messagebox  # alerts
    import tkinter.ttk         # themed widgets
    import tkinter.commondialog
    print("[HOOK] Tkinter submodules imported successfully")
except Exception as e:
    print(f"[HOOK WARNING] Tkinter preload failed: {e}")
