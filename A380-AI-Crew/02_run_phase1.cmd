@echo off
setlocal EnableExtensions

if /i not "%~1"=="__RUN__" (
  start "A380 AI - Phase 1 Run" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Phase 1 Run

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
cd /d "%ROOT%"

call "%ROOT%\.venv\Scripts\activate.bat" || (echo FEHLER: venv fehlt. Erst 01_install_phase1.cmd ausfuehren. & goto :END)

echo Starte Phase 1...
py -3 "%ROOT%\src\a380_ai\main.py"

:END
echo.
echo Fertig. Fenster bleibt offen.
pause
