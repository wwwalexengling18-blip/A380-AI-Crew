@echo off
setlocal EnableExtensions
title A380 AI - Variablen Diagnose V3 (sichtbar + bleibt offen)

echo ================================
echo   Sim Variablen Test V3
echo ================================
echo.

echo [1/3] Python pruefen...
python --version
if errorlevel 1 (
  echo.
  echo ❌ Python nicht gefunden.
  echo.
  pause
  cmd /k
)

echo.
echo [2/3] Diagnose-Skript erstellen...

set "PY=%~dp0vars_test_v3.py"
(
  echo from SimConnect import SimConnect, AircraftRequests
  echo import time, datetime, sys
  echo
  echo def ts():
  echo ^    return datetime.datetime.now().strftime("%%H:%%M:%%S")
  echo
  echo print(f"[{ts()}] Verbinde mit Simulator...", flush=True)
  echo try:
  echo ^    sm = SimConnect()
  echo ^    aq = AircraftRequests(sm, _time=1000)
  echo ^    print(f"[{ts()}] ✔ Verbindung OK", flush=True)
  echo except Exception as e:
  echo ^    print(f"[{ts()}] ❌ Verbindung fehlgeschlagen: {e}", flush=True)
  echo ^    input("ENTER zum Schliessen...")
  echo ^    sys.exit(1)
  echo
  echo print(f"[{ts()}] Warte 10 Sekunden (FBW/WASM Ready)...", flush=True)
  echo time.sleep(10)
  echo
  echo vars_ = [
  echo ^    ("SIM ON GROUND","ONGROUND"),
  echo ^    ("PLANE ALTITUDE","ALT"),
  echo ^    ("AIRSPEED INDICATED","IAS"),
  echo ^    ("GENERAL ENG RPM:1","N1_1"),
  echo ^    ("GENERAL ENG RPM:2","N1_2"),
  echo ^    ("PLANE HEADING DEGREES TRUE","HDG"),
  echo ]
  echo
  echo none_streak = 0
  echo print(f"[{ts()}] Lese Variablen (20 Sekunden)...", flush=True)
  echo for i in range(20):
  echo ^    row = {}
  echo ^    for vname, key in vars_:
  echo ^        try:
  echo ^            row[key] = aq.get(vname)
  echo ^        except Exception as e:
  echo ^            row[key] = f"ERR:{e}"
  echo ^    any_none = any(row[k] is None for k in row)
  echo ^    none_streak = none_streak + 1 if any_none else 0
  echo ^    print(f"[{ts()}] Tick {i+1:02d} " + " ".join([f"{k}={row[k]}" for k in row]), flush=True)
  echo ^    if none_streak ^>= 5:
  echo ^        print(f"[{ts()}] ⚠ 5x NONE in Folge -> Aircraft/SimVars noch nicht bereit ODER FBW braucht Bridge", flush=True)
  echo ^    time.sleep(1)
  echo
  echo print(f"[{ts()}] Test beendet.", flush=True)
  echo input("ENTER zum Schliessen...")
) > "%PY%"

echo OK: %PY%
echo.
echo [3/3] Starte Test...
echo.

python -u "%PY%"

echo.
echo ================================
echo Fertig. Fenster bleibt offen.
echo ================================
pause
cmd /k
