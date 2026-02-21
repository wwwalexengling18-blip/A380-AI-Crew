@echo off
setlocal EnableExtensions EnableDelayedExpansion
title A380-AI-Crew - INSTALL (MSFS 2024)
cd /d "%~dp0"

echo ==========================================================
echo   A380-AI-Crew - GROSSES INSTALL UPDATE
echo   Ziel: stabile Installation + Logs + venv + Tests
echo ==========================================================
echo.

rem ---- Tools Ordner (dein Standard) ----
set "TOOLS=%USERPROFILE%\Documents\FBW_A380_Tools"
set "LOGS=%TOOLS%\logs"
set "VENV=%TOOLS%\venv"

if not exist "%TOOLS%" mkdir "%TOOLS%"
if not exist "%LOGS%"  mkdir "%LOGS%"

echo [1/8] Ordnerstruktur:
echo   TOOLS = "%TOOLS%"
echo   LOGS  = "%LOGS%"
echo   VENV  = "%VENV%"
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
  echo [FEHLER] Python nicht gefunden.
  echo Installiere Python (3.11 oder 3.12) und versuche es erneut.
  goto :end
)

echo [2/8] Python Launcher:
echo   PY = %PYEXE%
echo.

rem ---- venv erstellen (einmalig) ----
if not exist "%VENV%\Scripts\python.exe" (
  echo [3/8] Erstelle venv...
  if "%PYEXE%"=="py" (
    py -3.11 -m venv "%VENV%" 2>nul || py -3.12 -m venv "%VENV%"
  ) else (
    python -m venv "%VENV%"
  )
)

if not exist "%VENV%\Scripts\python.exe" (
  echo [FEHLER] venv konnte nicht erstellt werden.
  goto :end
)

set "VPY=%VENV%\Scripts\python.exe"
echo [4/8] venv OK:
echo   VPY = "%VPY%"
echo.

rem ---- pip aktualisieren ----
echo [5/8] pip upgrade...
"%VPY%" -m pip install --upgrade pip setuptools wheel

rem ---- Requirements installieren ----
echo [6/8] Installiere Pakete...
rem Minimal: SimConnect libs sind je nach Setup verschieden,
rem wir installieren "requests" etc. + wasimcommander optional.
"%VPY%" -m pip install --upgrade colorama

rem optional WASimCommander (wenn verfügbar)
echo.
echo [Optional] WASimCommander installieren (wenn moeglich)...
"%VPY%" -m pip install wasimcommander >nul 2>nul
if errorlevel 1 (
  echo   [WARN] wasimcommander konnte nicht installiert werden (ok, optional).
) else (
  echo   [OK] wasimcommander installiert.
)

rem ---- Quick Self Test ----
echo.
echo [7/8] Schnelltest: Python + Imports
"%VPY%" -c "import sys; print('Python OK:', sys.version)"
"%VPY%" -c "import colorama; print('colorama OK')"

echo.
echo [8/8] Fertig.
echo - Naechster Schritt: run.cmd starten
echo - Logs: "%LOGS%"
echo.

:end
echo.
pause
endlocal
