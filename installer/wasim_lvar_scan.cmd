@echo off
setlocal
title WASimCommander LVar Scan

set ROOT=%~dp0..
set VENV=%ROOT%\.venv

if exist "%VENV%\Scripts\python.exe" (
  "%VENV%\Scripts\python.exe" "%~dp0wasim_lvar_scan.py"
) else (
  py "%~dp0wasim_lvar_scan.py"
)

echo.
echo Fertig. Log im logs Ordner.
pause
