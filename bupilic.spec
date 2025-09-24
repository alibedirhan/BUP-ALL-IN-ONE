# -*- mode: python ; coding: utf-8 -*-
import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

project_root = Path(os.getcwd()).resolve()
block_cipher = None

datas = [
    ('icon/bupilic_logo.png', 'icon'),
]
# Kütüphane assetleri
datas += collect_data_files('customtkinter')
datas += collect_data_files('PIL')

hiddenimports = [
    'tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk', 'tkinter.commondialog',
    'PIL.ImageTk',
]

# .py modülleri göm (importlar için)
for pkg in ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']:
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception:
        pass

# MEIPASS altına klasör ağacı koy (bazı modüller klasörü kopyalıyor)
def add_tree(src_dir: Path, dest_prefix: str):
    if not src_dir.exists():
        return
    for root, _, files in os.walk(src_dir):
        for fname in files:
            full = Path(root) / fname
            rel = full.relative_to(src_dir)
            datas.append((str(full), str(Path(dest_prefix) / rel)))

for sub in ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']:
    add_tree(project_root / sub, sub)

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=['hooks'] if (project_root / 'hooks').exists() else [],
    runtime_hooks=['runtime_hook.py'],
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas,
    name='BupiliC',
    console=True,  # ilk testlerde açık kalsın
    icon=str(project_root/'build'/'app_icon.ico') if (project_root/'build'/'app_icon.ico').exists() else None,
)
