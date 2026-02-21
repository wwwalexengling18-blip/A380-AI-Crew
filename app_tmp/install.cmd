@echo off
cd /d "%~dp0"
cmd /k call :install
goto :eof

:install
setlocal EnableExtensions EnableDelayedExpansion
title A380-AI-Crew - INSTALL

echo ==========================================================
echo   A380-AI-Crew INSTALLATION (Fenster bleibt offen)
echo ==========================================================
echo.

rem ---- Tools Ordner ----
set "TOOLS=%USERPROFILE%\Documents\FBW_A380_Tools"
set "LOGS=%TOOLS%\logs"
set "VENV=%TOOLS%\venv"

if not exist "%TOOLS%" mkdir "%TOOLS%"
if not exist "%LOGS%"  mkdir "%LOGS%"

echo [1] Ordner OK
echo.

rem ---- Python finden ----
set "PYEXE="
for %%P in (py.exe python.exe) do (
  where %%P >nul 2>nul && (
    if "%%P"=="py.exe" (
      set "PYEXE=py"
    ) else (
      set "PYEXE=python"
    )
    goto :py_found
  )
)

:py_found
if "%PYEXE%"=="" (
  echo [FEHLER] Python nicht gefunden
  goto :end
)

echo [2] Python gefunden: %PYEXE%
echo.

rem ---- venv erstellen ----
if not exist "%VENV%\Scripts\python.exe" (
  echo [3] Erstelle venv...
  if "%PYEXE%"=="py" (
    py -3.11 -m venv "%VENV%" 2>nul || py -3.12 -m venv "%VENV%"
  ) else (
    python -m venv "%VENV%"
  )
)

if not exist "%VENV%\Scripts\python.exe" (
  echo [FEHLER] venv konnte nicht erstellt werden
  goto :end
)

set "VPY=%VENV%\Scripts\python.exe"
echo [4] venv OK
echo.

rem ---- pip upgrade ----
echo [5] pip upgrade...
"%VPY%" -m pip install --upgrade pip setuptools wheel

rem ---- Pakete ----
echo [6] Installiere Pakete...
"%VPY%" -m pip install colorama

echo.
echo [Optional] WASimCommander Versuch...
"%VPY%" -m pip install wasimcommander >nul 2>nul
if errorlevel 1 (
  echo   [WARN] WASim optional nicht installiert
) else (
  echo   [OK] WASim installiert
)

echo.
echo [7] Schnelltest...
"%VPY%" -c "import sys; print('Python OK:', sys.version)"

:end
echo.
echo ==========================================================
echo INSTALLATION FERTIG
echo Fenster bleibt offen fuer Logs / Fehleranalyse
echo ==========================================================
echo.
endlocal
