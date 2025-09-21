# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# TÜM DOSYALARI EKLE - KESİN ÇÖZÜM
datas = []

# TÜM ALT PROGRAM KLASÖRLERİNİ EKLE
modules = ['ISKONTO_HESABI', 'KARLILIK_ANALIZI', 'Musteri_Sayisi_Kontrolu', 'YASLANDIRMA']
for module in modules:
    datas.append((module, module))

# ICON KLASÖRÜNÜ EKLE
datas.append(('icon', 'icon'))

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[],  # BOŞ BIRAK
    binaries=[],
    datas=datas,
    hiddenimports=[
        # TÜM MODÜLLERİ EKLE
        'ISKONTO_HESABI.main', 'ISKONTO_HESABI.ui_components',
        'ISKONTO_HESABI.pdf_processor', 'ISKONTO_HESABI.export_manager',
        
        'KARLILIK_ANALIZI.gui', 'KARLILIK_ANALIZI.karlilik',
        'KARLILIK_ANALIZI.analiz_dashboard', 'KARLILIK_ANALIZI.dashboard_components',
        'KARLILIK_ANALIZI.data_operations', 'KARLILIK_ANALIZI.themes',
        'KARLILIK_ANALIZI.ui_components', 'KARLILIK_ANALIZI.veri_analizi',
        'KARLILIK_ANALIZI.zaman_analizi',
        
        'Musteri_Sayisi_Kontrolu.main', 'Musteri_Sayisi_Kontrolu.ui',
        'Musteri_Sayisi_Kontrolu.kurulum',
        
        'YASLANDIRMA.main', 'YASLANDIRMA.gui', 'YASLANDIRMA.excel_processor',
        'YASLANDIRMA.utils', 'YASLANDIRMA.setup',
        
        # KÜTÜPHANELER
        'pandas', 'numpy', 'matplotlib', 'customtkinter',
        'pdfplumber', 'PIL', 'openpyxl', 'seaborn',
        'tkcalendar', 'python-dateutil', 'psutil'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    name='BupiliC',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # DEBUG İÇİN TRUE
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # ICON'U KALDIR
)
