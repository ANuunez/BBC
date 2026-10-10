@echo off
setlocal

echo =============================================
echo Best BongoCat Clicker (BBC) - build script
echo =============================================
echo.

echo This script is for building the developer version.
echo End users do NOT need Python or these libraries.
echo.

py -m pip install -r requirements.txt
if errorlevel 1 exit /b 1

py -m pip install pyinstaller
if errorlevel 1 exit /b 1

pyinstaller --noconfirm --clean --onefile --windowed ^
  --name "BBC" ^
  --icon "assets\BBC.ico" ^
  --add-data "assets\BBC.ico;assets" ^
  --version-file "version_info.txt" ^
  "src\bbc_clicker.py"

if errorlevel 1 exit /b 1

echo.
echo Build complete: dist\BBC.exe
endlocal
