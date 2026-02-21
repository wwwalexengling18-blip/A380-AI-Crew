@echo off
setlocal EnableExtensions
title A380-AI-Crew - RUN
cd /d "%~dp0"

set "TOOLS=%USERPROFILE%\Documents\FBW_A380_Tools"
set "VENV=%TOOLS%\venv"
set "VPY=%VENV%\Scripts\python.exe"

if not exist "%VPY%" (
  echo [FEHLER] venv fehlt. Bitte zuerst install.cmd ausfuehren.
  echo.
  pause
  exit /b 1
)

echo Starte A380-AI-Crew...
echo Python: "%VPY%"
echo.

rem /k = Fenster bleibt offen (dein Wunsch)
cmd /k "%VPY%" main.py
endlocal
