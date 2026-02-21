from SimConnect import SimConnect, AircraftRequests
import time, datetime, sys

def ts():
    return datetime.datetime.now().strftime("%H:%M:%S")

print(f"[{ts()}] Verbinde mit Simulator...", flush=True)

try:
    sm = SimConnect()
    aq = AircraftRequests(sm, _time=1000)
    print(f"[{ts()}] ✔ Verbindung OK", flush=True)
except Exception as e:
    print(f"[{ts()}] ❌ Verbindung fehlgeschlagen: {e}", flush=True)
    input("ENTER zum Schliessen...")
    sys.exit(1)

print(f"[{ts()}] Warte 10 Sekunden (FBW/WASM Ready)...", flush=True)
time.sleep(10)

vars_ = [
    ("SIM ON GROUND","ONGROUND"),
    ("PLANE ALTITUDE","ALT"),
    ("AIRSPEED INDICATED","IAS"),
    ("GENERAL ENG RPM:1","N1_1"),
    ("GENERAL ENG RPM:2","N1_2"),
    ("PLANE HEADING DEGREES TRUE","HDG"),
]

none_streak = 0
print(f"[{ts()}] Lese Variablen (20 Sekunden)...", flush=True)

for i in range(20):
    row = {}
    for vname, key in vars_:
        try:
            row[key] = aq.get(vname)
        except Exception as e:
            row[key] = f"ERR:{e}"

    any_none = any(row[k] is None for k in row)
    none_streak = none_streak + 1 if any_none else 0

    print(f"[{ts()}] Tick {i+1:02d} " + " ".join([f"{k}={row[k]}" for k in row]), flush=True)

    if none_streak >= 5:
        print(f"[{ts()}] ⚠ 5x NONE in Folge -> Aircraft nicht ready oder FBW braucht Bridge", flush=True)

    time.sleep(1)

print(f"[{ts()}] Test beendet.", flush=True)
input("ENTER zum Schliessen...")
