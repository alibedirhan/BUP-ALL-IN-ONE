REM setup_env.bat - Environment Setup Script
@echo off
echo ========================================
echo BupiliC Build Environment Setup
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo Found Python: 
python --version

REM Create virtual environment (optional but recommended)
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install build requirements
echo.
echo Installing build requirements...
python -m pip install pyinstaller==6.3.0 pillow>=10.1.0 upx-python

REM Install app requirements
echo.
echo Installing application requirements...
if exist "requirements.txt" (
    python -m pip install -r requirements.txt
) else (
    echo WARNING: requirements.txt not found
)

REM Install additional build requirements if they exist
if exist "requirements-build.txt" (
    echo Installing additional build requirements...
    python -m pip install -r requirements-build.txt
)

REM Create necessary directories
echo.
echo Creating build directories...
if not exist "build" mkdir build
if not exist "dist" mkdir dist
if not exist "logs" mkdir logs

echo.
echo ========================================
echo Environment setup completed!
echo ========================================
echo.
echo You can now run: scripts\test_build.bat
echo.
pause

REM ========================================
REM test_build.bat - Local Test Build Script  
REM ========================================
@echo off
echo ========================================
echo BupiliC Local Build Test
echo ========================================

REM Check if we're in virtual environment
if "%VIRTUAL_ENV%"=="" (
    echo Activating virtual environment...
    if exist "venv\Scripts\activate.bat" (
        call venv\Scripts\activate.bat
    ) else (
        echo WARNING: Virtual environment not found
        echo Run setup_env.bat first
    )
)

REM Check if build script exists
if not exist "build\build.py" (
    echo ERROR: build\build.py not found
    echo Please ensure all build files are in place
    pause
    exit /b 1
)

REM Run the build
echo.
echo Starting build process...
python build\build.py --version dev-test --debug

echo.
echo ========================================
echo Build test completed!
echo ========================================

REM Check if executable was created
if exist "dist\BupiliC.exe" (
    echo SUCCESS: Executable created at dist\BupiliC.exe
    set /p answer="Do you want to test the executable? (y/n): "
    if /i "%answer%"=="y" (
        echo Starting executable...
        start "" "dist\BupiliC.exe"
    )
) else (
    echo ERROR: Executable not found in dist folder
)

echo.
pause

REM ========================================
REM release_build.bat - Release Build Script
REM ========================================
@echo off
echo ========================================
echo BupiliC Release Build
echo ========================================

REM Get version from user
set /p version="Enter version (e.g., v1.0.0): "
if "%version%"=="" (
    echo ERROR: Version is required
    pause
    exit /b 1
)

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: Virtual environment not found
    echo Run setup_env.bat first
    pause
    exit /b 1
)

REM Clean previous builds
echo Cleaning previous builds...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Run release build
echo.
echo Starting release build for version %version%...
python build\build.py --version %version% --clean

REM Check result
if exist "dist\BupiliC.exe" (
    echo.
    echo ========================================
    echo RELEASE BUILD SUCCESSFUL!
    echo ========================================
    echo Executable: dist\BupiliC.exe
    
    REM Show file size
    for %%I in (dist\BupiliC.exe) do echo Size: %%~zI bytes
    
    echo.
    set /p answer="Create release package? (y/n): "
    if /i "%answer%"=="y" (
        echo Creating release package...
        if not exist "releases" mkdir releases
        
        REM Copy executable with version name
        copy "dist\BupiliC.exe" "releases\BupiliC-%version%-windows.exe"
        
        REM Create ZIP package
        if exist "C:\Program Files\7-Zip\7z.exe" (
            "C:\Program Files\7-Zip\7z.exe" a -tzip "releases\BupiliC-%version%-portable.zip" "releases\BupiliC-%version%-windows.exe"
            echo ZIP package created: releases\BupiliC-%version%-portable.zip
        ) else (
            echo 7-Zip not found, ZIP package not created
        )
        
        echo Release files ready in 'releases' folder
    )
    
) else (
    echo.
    echo ========================================
    echo BUILD FAILED!
    echo ========================================
    echo Check the error messages above
)

echo.
pause