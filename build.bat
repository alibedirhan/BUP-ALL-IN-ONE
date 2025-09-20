@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo =========================================
echo     BUPILIC - TEK EXE OLUSTURMA
echo =========================================
echo.

:: Python kontrolu
echo [1/6] Python kontrol ediliyor...
python --version >nul 2>&1
if errorlevel 1 (
    echo HATA: Python bulunamadi!
    echo Python 3.10+ yukleyin ve PATH'e ekleyin.
    pause
    exit /b 1
)
echo     Python bulundu.

:: Gerekli dosya kontrolu
echo [2/6] Gerekli dosyalar kontrol ediliyor...
if not exist "BUPILIC_ANA_PROGRAM.py" (
    echo HATA: BUPILIC_ANA_PROGRAM.py bulunamadi!
    pause
    exit /b 1
)
if not exist "bupilic.spec" (
    echo HATA: bupilic.spec bulunamadi!
    pause
    exit /b 1
)
if not exist "requirements.txt" (
    echo HATA: requirements.txt bulunamadi!
    pause
    exit /b 1
)
echo     Tum dosyalar mevcut.

:: Onceki build'leri temizle
echo [3/6] Onceki build'ler temizleniyor...
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
echo     Temizlik tamamlandi.

:: PyInstaller yukle
echo [4/6] PyInstaller kontrol ediliyor...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo     PyInstaller yukleniyor...
    pip install pyinstaller==6.3.0
    if errorlevel 1 (
        echo HATA: PyInstaller yuklenemedi!
        pause
        exit /b 1
    )
)
echo     PyInstaller hazir.

:: Kutuphaneleri yukle
echo [5/6] Kutuphaneler yukleniyor...
pip install -r requirements.txt
if errorlevel 1 (
    echo UYARI: Bazi kutuphaneler yuklenemedi, devam ediliyor...
)
echo     Kutuphaneler yuklendi.

:: Build islemi
echo [6/6] EXE dosyasi olusturuluyor...
echo     Bu islem birka dakika surebilir...
pyinstaller bupilic.spec --noconfirm --clean --log-level=WARN

:: Sonuc kontrolu
echo.
echo =========================================
if exist "dist\BupiliC.exe" (
    echo           BUILD BASARILI!
    echo =========================================
    echo.
    echo EXE Dosyasi: dist\BupiliC.exe
    
    :: Dosya boyutunu goster
    for %%I in ("dist\BupiliC.exe") do set filesize=%%~zI
    set /a "filesize_mb=!filesize!/1024/1024"
    echo Dosya Boyutu: !filesize_mb! MB
    
    echo.
    echo KULLANIM:
    echo 1. dist\BupiliC.exe dosyasini istediginiz yere kopyalayin
    echo 2. Cift tiklayarak calistirin
    echo 3. Sifre: bupilic2024
    echo 4. 4 alt programa erisebilirsiniz
    echo.
    echo DAGITIM:
    echo - Kullanicilar sadece BupiliC.exe dosyasini indirir
    echo - Python gerektirmez
    echo - Internet baglantisi gerektirmez
    echo - Hicbir sey yuklemez
    echo.
) else (
    echo           BUILD BASARISIZ!
    echo =========================================
    echo.
    echo HATA: EXE dosyasi olusturulamadi.
    echo Yukaridaki hata mesajlarini kontrol edin.
    echo.
    if exist build\BupiliC\warn-BupiliC.txt (
        echo UYARI DOSYASI:
        type build\BupiliC\warn-BupiliC.txt
    )
)

echo.
echo Test etmek icin: dist\BupiliC.exe
echo.
pause
