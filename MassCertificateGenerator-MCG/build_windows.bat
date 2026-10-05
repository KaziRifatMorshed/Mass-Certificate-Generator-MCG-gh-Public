@echo off
setlocal enabledelayedexpansion

echo ========================================================
echo   Mass Certificate Generator - Windows Build Script
echo ========================================================

:: 1. Extract Git Commit Hash
where git >nul 2>nul
if %errorlevel% equ 0 (
    for /f %%i in ('git rev-parse --short HEAD 2^>nul') do set MCG_GIT_HASH=%%i
)
if "%MCG_GIT_HASH%"=="" set MCG_GIT_HASH=unknown
echo [*] Git Commit Hash : %MCG_GIT_HASH%

:: 2. Extract Build Date and Time via PowerShell
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format 'yyyy-MM-dd_HH-mm-ss'"') do set MCG_BUILD_DATE_TIME=%%i
echo [*] Build Timestamp : %MCG_BUILD_DATE_TIME%

:: 3. Generate Windows Icon (.ico) if missing
if not exist "extra\MCG_logo.ico" (
    echo [*] Generating extra\MCG_logo.ico from PNG...
    python -c "from PIL import Image; img=Image.open('extra/MCG_logo.png'); img.save('extra/MCG_logo.ico', sizes=[(16,16),(24,24),(32,32),(48,48),(64,64),(128,128),(256,256)])"
)

:: 4. Run PyInstaller Build
echo [*] Building executable with PyInstaller...
pyinstaller MassCertificateGenerator.spec --noconfirm --clean
if %errorlevel% neq 0 (
    echo [ERROR] PyInstaller build failed.
    exit /b %errorlevel%
)

echo [*] Binary built: dist\MassCertificateGenerator.exe

:: 5. Compile Inno Setup Installer if ISCC is installed
set "ISCC_PATH="
if exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" set "ISCC_PATH=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if "%ISCC_PATH%"=="" (
    where ISCC.exe >nul 2>nul
    if %errorlevel% equ 0 set "ISCC_PATH=ISCC.exe"
)

if not "%ISCC_PATH%"=="" (
    echo [*] Building Inno Setup Installer with: "%ISCC_PATH%"
    "%ISCC_PATH%" winInstallationInnoScript.iss
    if %errorlevel% equ 0 (
        echo [SUCCESS] Windows installer generated in dist\installer\
    ) else (
        echo [WARNING] Inno Setup compilation encountered warnings or errors.
    )
) else (
    echo [*] Inno Setup 6 (ISCC.exe) not found on PATH or in Program Files.
    echo [*] To build the setup installer, install Inno Setup 6 and re-run this script.
)

echo ========================================================
echo   Build process completed successfully!
echo ========================================================
