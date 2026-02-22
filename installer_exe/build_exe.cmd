@echo off
setlocal
title Build A380 AI Installer EXE
cd /d "%~dp0"

echo === Python prüfen ===
python --version || (echo Python fehlt. Installiere Python 3.11+ & versuche erneut. & pause & exit /b 1)

echo === venv erstellen ===
if not exist ".venv" (
  python -m venv .venv || (echo venv failed & pause & exit /b 1)
)

call ".venv\Scripts\activate.bat" || (echo activate failed & pause & exit /b 1)

echo === Requirements installieren ===
python -m pip install --upgrade pip
pip install -r requirements.txt || (echo pip failed & pause & exit /b 1)

echo === PyInstaller Build ===
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

pyinstaller ^
  --noconfirm ^
  --onefile ^
  --name "A380_AI_Installer" ^
  --add-data "payload;payload" ^
  --add-data "lib;lib" ^
  installer_app.py || (echo pyinstaller failed & pause & exit /b 1)

echo.
echo ✅ Fertig! EXE liegt hier:
echo %cd%\dist\A380_AI_Installer.exe
echo.
echo Starte die EXE als normaler User (kein Admin noetig).
echo.
cmd /k
