@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: Immer in echtem CMD-Fenster laufen (nicht in PowerShell)
if /i not "%~1"=="__RUN__" (
  start "A380 AI - Phase 1 Install" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Phase 1 Install

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
cd /d "%ROOT%"

echo =========================================
echo   A380 AI - Phase 1 Installation
echo   Repo: %ROOT%
echo =========================================
echo.

echo [1/6] Python pruefen...
py -3 --version
if errorlevel 1 (
  echo FEHLER: Python Launcher "py" nicht gefunden.
  echo Loesung: Python installieren oder "python --version" testen.
  goto END
)

echo.
echo [2/6] Ordner anlegen...
if not exist "%ROOT%\logs" mkdir "%ROOT%\logs"
if not exist "%ROOT%\src\a380_ai" mkdir "%ROOT%\src\a380_ai"
if not exist "%ROOT%\third_party\wasim" mkdir "%ROOT%\third_party\wasim"

echo.
echo [3/6] Virtuelle Umgebung erstellen...
if not exist "%ROOT%\.venv\Scripts\python.exe" (
  py -3 -m venv "%ROOT%\.venv"
  if errorlevel 1 (
    echo FEHLER: venv konnte nicht erstellt werden.
    goto END
  )
)

echo.
echo [4/6] pip / Abhaengigkeiten installieren...
call "%ROOT%\.venv\Scripts\activate.bat"
python -m pip install --upgrade pip
python -m pip install pythonnet
if errorlevel 1 (
  echo FEHLER: pip install fehlgeschlagen.
  goto END
)

echo.
echo [5/6] Phase-1 Testscript schreiben (RPM States)...
set "PY=%ROOT%\src\a380_ai\main.py"
(
  echo import time, os
  echo from datetime import datetime
  echo import clr
  echo
  echo ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
  echo LOGDIR = os.path.join(ROOT, "logs")
  echo os.makedirs(LOGDIR, exist_ok=True)
  echo LOGFILE = os.path.join(LOGDIR, "phase1_rpm.log")
  echo
  echo DLL_DIR = os.path.join(ROOT, "third_party", "wasim")
  echo DLL_PATH = os.path.join(DLL_DIR, "WASimCommander.WASimClient.dll")
  echo if not os.path.isfile(DLL_PATH):
  echo     print("FEHLT DLL:", DLL_PATH)
  echo     print("Loesung: WASimCommander_SDK herunterladen und WASimCommander.WASimClient.dll nach third_party\\wasim kopieren.")
  echo     raise SystemExit(2)
  echo
  echo clr.AddReference(DLL_PATH)
  echo from WASimCommander import WASimClient
  echo
  echo def log(line: str):
  echo     ts = datetime.now().strftime("%%H:%%M:%%S")
  echo     out = f"[{ts}] {line}"
  echo     print(out, flush=True)
  echo     with open(LOGFILE, "a", encoding="utf-8") as f:
  echo         f.write(out + "\\n")
  echo
  echo def main():
  echo     log("Phase1 start - connecting to WASimCommander...")
  echo     c = WASimClient()
  echo     ok = c.connect()
  echo     if not ok:
  echo         log("FEHLER: connect() fehlgeschlagen. Ist MSFS gestartet + Flug geladen + WASimUI verbunden?")
  echo         return 3
  echo
  echo     vars_ = ["A380X_RPM_1_STATE", "A380X_RPM_2_STATE"]
  echo     log("Connected. Lese: " + ", ".join(vars_))
  echo
  echo     while True:
  echo         try:
  echo             v1 = c.getLvar(vars_[0])
  echo             v2 = c.getLvar(vars_[1])
  echo             log(f"RPM1_STATE={v1}  RPM2_STATE={v2}")
  echo         except Exception as e:
  echo             log("EXCEPTION: " + str(e))
  echo         time.sleep(1.0)
  echo
  echo if __name__ == "__main__":
  echo     raise SystemExit(main() or 0)
) > "%PY%"

echo.
echo [6/6] Naechster Schritt (DLL):
echo Kopiere WASimCommander.WASimClient.dll nach:
echo   %ROOT%\third_party\wasim\
echo.
echo Danach starten:
echo   installer\02_run_phase1.cmd
echo.

echo OK. Phase 1 installiert.

:END
echo.
echo Fertig. Fenster bleibt offen.
pause
