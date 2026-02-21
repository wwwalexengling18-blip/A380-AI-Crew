@echo off
setlocal EnableExtensions EnableDelayedExpansion

if /i not "%~1"=="__RUN__" (
  start "A380 AI - Phase 1 Run" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Phase 1 Run

set "ROOT=%~dp0.."
for %%I in ("%ROOT%") do set "ROOT=%%~fI"
cd /d "%ROOT%"

echo =========================================
echo   A380 AI - Phase 1 Run
echo   Repo: %ROOT%
echo =========================================
echo.

echo [1/5] venv pruefen/aktivieren...
if not exist "%ROOT%\.venv\Scripts\activate.bat" (
  echo FEHLT: .venv
  echo Starte zuerst: installer\01_install_phase1.cmd
  goto END
)
call "%ROOT%\.venv\Scripts\activate.bat"

echo.
echo [2/5] Ordner pruefen...
if not exist "%ROOT%\src\a380_ai" mkdir "%ROOT%\src\a380_ai"
if not exist "%ROOT%\logs" mkdir "%ROOT%\logs"
if not exist "%ROOT%\third_party\wasim" mkdir "%ROOT%\third_party\wasim"

echo.
echo [3/5] main.py pruefen...
set "PY=%ROOT%\src\a380_ai\main.py"
if not exist "%PY%" (
  echo main.py fehlt - wird erstellt...
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
    echo     print("Loesung: WASimCommander_SDK laden und WASimCommander.WASimClient.dll nach third_party\\wasim kopieren.")
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
    echo         log("FEHLER: connect() fehlgeschlagen. MSFS gestartet + Flug geladen + WASimUI 'Server Connected'?")
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
)

echo.
echo [4/5] DLL pruefen...
if not exist "%ROOT%\third_party\wasim\WASimCommander.WASimClient.dll" (
  echo FEHLT DLL: %ROOT%\third_party\wasim\WASimCommander.WASimClient.dll
  echo Bitte aus WASimCommander_SDK kopieren.
  goto END
)

echo.
echo [5/5] Starte Script...
py -3 "%PY%"

:END
echo.
echo Fertig. Fenster bleibt offen.
pause
