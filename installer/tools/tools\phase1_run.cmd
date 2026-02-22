@echo off
setlocal
title A380-AI-Crew - Phase1 Run

set ROOT=%~dp0..
set VENV=%ROOT%\.venv

if not exist "%VENV%\Scripts\python.exe" (
  echo venv fehlt. Starte zuerst tools\phase1_setup.cmd
  pause
  exit /b 1
)

"%VENV%\Scripts\python.exe" "%~dp0phase1_live_read.py"
echo.
echo Fertig. Log liegt in: %ROOT%\logs
pause
