@echo off
echo ========================================
echo    BUPiLiC - TEK EXE OLUSTURMA
echo ========================================

:: Onceki build'leri temizle
echo Cleaning previous builds...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

:: PyInstaller kontrolu
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller not found! Installing...
    pip install pyinstaller
)

:: Gerekli kutuphaneleri yukle
echo Installing dependencies...
pip install -r requirements.txt

:: Spec dosyasi ile build
echo Building executable...
pyinstaller bupilic.spec --noconfirm --clean

:: Sonuc kontrolu
if exist "dist\BupiliC.exe" (
    echo.
    echo ========================================
    echo ✅ BUILD SUCCESSFUL!
    echo ========================================
    echo EXE file: dist\BupiliC.exe
    dir dist\BupiliC.exe
    echo.
    echo You can now run: dist\BupiliC.exe
) else (
    echo.
    echo ========================================
    echo ❌ BUILD FAILED!
    echo ========================================
    echo Check error messages above.
)

echo.
pause
