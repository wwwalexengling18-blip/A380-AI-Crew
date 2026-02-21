@echo off
title A380 AI Crew Installer

echo ============================
echo   A380 AI Crew Installer
echo ============================

set TARGET=%USERPROFILE%\Documents\FBW_A380_Tools\A380_AI_Crew
echo Installationspfad: %TARGET%

if not exist "%TARGET%" mkdir "%TARGET%"

echo.
echo Lade neueste Version von GitHub...
powershell -Command "Invoke-WebRequest -Uri https://github.com/wwwalexengling18-blip/A380-AI-Crew/archive/refs/heads/main.zip -OutFile %TEMP%\A380.zip"

echo Entpacke Dateien...
powershell -Command "Expand-Archive -Path %TEMP%\A380.zip -DestinationPath %TARGET% -Force"

echo.
echo Installation abgeschlossen
pause

echo.
echo Python Pakete installieren...
cd /d "%TARGET%\A380-AI-Crew-main"

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Abhaengigkeiten fertig.
