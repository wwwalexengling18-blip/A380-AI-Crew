@echo off
setlocal
title A380-AI-Crew - WASim Vars Scan (CMD)

set ROOT=%~dp0..
set VENV=%ROOT%\.venv

echo ==========================================
echo WASimCommander-Style Vars Scan
echo Datei: installer\wasim_vars_list.txt
echo Log:   logs\
echo ==========================================
echo.

if exist "%VENV%\Scripts\python.exe" (
  "%VENV%\Scripts\python.exe" "%~dp0wasim_vars_scan.py"
) else (
  py "%~dp0wasim_vars_scan.py"
)

echo.
echo Fertig. Schau in den logs Ordner.
pause
