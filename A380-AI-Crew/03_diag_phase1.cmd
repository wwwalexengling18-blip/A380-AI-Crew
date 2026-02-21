@echo off
setlocal EnableExtensions

if /i not "%~1"=="__RUN__" (
  start "A380 AI - Phase 1 Diagnose" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Phase 1 Diagnose

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
cd /d "%ROOT%"

echo =========================================
echo   A380 AI - Phase 1 Diagnose
echo =========================================

echo.
echo [1] Python:
py -3 --version

echo.
echo [2] venv:
if exist "%ROOT%\.venv\Scripts\python.exe" (echo OK: .venv vorhanden) else (echo FEHLT: .venv)

echo.
echo [3] WASim DLL:
if exist "%ROOT%\third_party\wasim\WASimCommander.WASimClient.dll" (
  echo OK: DLL gefunden
) else (
  echo FEHLT: %ROOT%\third_party\wasim\WASimCommander.WASimClient.dll
)

echo.
echo [4] Logfile:
if exist "%ROOT%\logs\phase1_rpm.log" (echo OK: logs\phase1_rpm.log) else (echo Noch kein Log geschrieben)

echo.
pause
