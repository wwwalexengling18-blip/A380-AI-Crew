@echo off
setlocal
title A380-AI-Crew - Phase1 Setup

set ROOT=%~dp0..
set VENV=%ROOT%\.venv
set LOGDIR=%ROOT%\logs

mkdir "%LOGDIR%" 2>nul

echo [Phase1] ROOT=%ROOT%
echo [Phase1] LOGDIR=%LOGDIR%

py -V || (echo Python fehlt. Installiere Python 3.11+ und starte neu. & pause & exit /b 1)

if not exist "%VENV%\Scripts\python.exe" (
  echo [Phase1] Erstelle venv...
  py -m venv "%VENV%" || (echo venv Fehler & pause & exit /b 1)
)

echo [Phase1] Upgrade pip...
"%VENV%\Scripts\python.exe" -m pip install --upgrade pip

if exist "%ROOT%\requirements.txt" (
  echo [Phase1] Installiere requirements...
  "%VENV%\Scripts\python.exe" -m pip install -r "%ROOT%\requirements.txt"
) else (
  echo [Phase1] requirements.txt fehlt - überspringe.
)

echo [Phase1] Fertig.
echo Log-Ordner: %LOGDIR%
pause
