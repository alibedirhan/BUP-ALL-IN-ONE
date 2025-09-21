# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# EN BASİT ve ETKİLİ YOL - TÜM DOSYALARI EKLE
datas = [
    ('ISKONTO_HESABI', 'ISKONTO_HESABI'),
    ('KARLILIK_ANALIZI', 'KARLILIK_ANALIZI'),
    ('Musteri_Sayisi_Kontrolu', 'Musteri_Sayisi_Kontrolu'),
    ('YASLANDIRMA', 'YASLANDIRMA'),
    ('icon', 'icon'),
]

a = Analysis(
    ['BUPILIC_ANA_PROGRAM.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # SADECE ANA MODÜLLER
        'ISKONTO_HESABI.main',
        'KARLILIK_ANALIZI.gui',
        'Musteri_Sayisi_Kontrolu.main', 
        'YASLANDIRMA.main',
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
    icon='icon/bupilic_logo.ico',
)
