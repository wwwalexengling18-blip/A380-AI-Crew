@echo off
title A380 AI - Variablen Diagnose V3 (Wrapper-kompatibel)

setlocal EnableExtensions
set LOGDIR=%~dp0logs
if not exist "%LOGDIR%" mkdir "%LOGDIR%"

echo ================================ 
echo   Sim Variablen Test V3
echo ================================
echo.

python --version
if errorlevel 1 (
  echo ❌ Python nicht gefunden
  pause
  exit /b 1
)

:: Python Diagnose schreiben
set PY=%~dp0vars_test_v3.py
(
  echo from SimConnect import SimConnect, AircraftRequests
  echo import time, datetime, os, sys
  echo
  echo def ts(): 
  echo ^    return datetime.datetime.now().strftime("%%H:%%M:%%S")
  echo
  echo print(f"[{ts()}] Verbinde mit Simulator...")
  echo try:
  echo ^    sm = SimConnect()
  echo ^    aq = AircraftRequests(sm, _time=1000)
  echo ^    print(f"[{ts()}] ✔ Verbindung OK")
  echo except Exception as e:
  echo ^    print(f"[{ts()}] ❌ Verbindung fehlgeschlagen: {e}")
  echo ^    sys.exit(1)
  echo
  echo print(f"[{ts()}] Warte 8 Sekunden (FBW/WASM Ready)...")
  echo time.sleep(8)
  echo
  echo vars_ = [
  echo ^    ("AIRSPEED INDICATED","IAS"),
  echo ^    ("PLANE ALTITUDE","ALT"),
  echo ^    ("PLANE HEADING DEGREES TRUE","HDG"),
  echo ^    ("SIM ON GROUND","ONGROUND"),
  echo ^    ("GENERAL ENG RPM:1","N1_1"),
  echo ^    ("GENERAL ENG RPM:2","N1_2"),
  echo ]
  echo
  echo none_streak = 0
  echo print(f"[{ts()}] Lese Variablen (20 Sekunden)...")
  echo for i in range(20):
  echo ^    row = {}
  echo ^    for vname, key in vars_:
  echo ^        try:
  echo ^            val = aq.get(vname)
  echo ^        except Exception as e:
  echo ^            val = f"ERR:{e}"
  echo ^        row[key] = val
  echo ^    # NONE-Erkennung
  echo ^    any_none = any(row[k] is None for k in row)
  echo ^    none_streak = none_streak + 1 if any_none else 0
  echo ^    print(f"[{ts()}] Tick {i+1:02d}  " +
  echo ^          " ".join([f"{k}={row[k]}" for k in row]))
  echo ^    if none_streak >= 5:
  echo ^        print(f"[{ts()}] ⚠ 5x NONE in Folge -> Aircraft/SimVars noch nicht bereit oder FBW-Var Zugriff fehlt")
  echo ^    time.sleep(1)
  echo
  echo print(f"[{ts()}] Test beendet.")
) > "%PY%"

python "%PY%"

echo.
echo Logs-Ordner: "%LOGDIR%"
pause
