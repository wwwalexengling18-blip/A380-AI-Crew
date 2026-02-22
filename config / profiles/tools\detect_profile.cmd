@echo off
setlocal
title A380-AI-Crew - Detect Profile

set ROOT=%~dp0..
set VENV=%ROOT%\.venv

if not exist "%VENV%\Scripts\python.exe" (
  echo venv fehlt. Starte zuerst tools\phase1_setup.cmd
  echo (oder erstelle venv manuell)
  pause
  exit /b 1
)

"%VENV%\Scripts\python.exe" "%~dp0detect_profile.py"
echo.
echo Fertig. Schau in:
echo   %ROOT%\config\runtime_detected.json
echo   %ROOT%\config\active_profile.yaml
pause
