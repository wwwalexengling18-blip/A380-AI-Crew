import time
import os
from datetime import datetime

LOGDIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOGDIR, exist_ok=True)
log_path = os.path.join(LOGDIR, f"phase1_live_read_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

def log(msg: str):
    line = f"{datetime.now().strftime('%H:%M:%S')} | {msg}"
    print(line)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(line + "\n")

log("Starte Phase1 Live Read...")

try:
    # pip package: SimConnect (bekannt aus MSFS Python Beispielen)
    from SimConnect import SimConnect, AircraftRequests
except Exception as e:
    log(f"ERROR: SimConnect Python Lib fehlt/kaputt: {e}")
    log("Tipp: requirements.txt muss SimConnect enthalten.")
    raise

sm = None
aq = None

for attempt in range(1, 6):
    try:
        log(f"Verbinde SimConnect (Attempt {attempt}/5)...")
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=2000)
        log("OK: SimConnect verbunden.")
        break
    except Exception as e:
        log(f"WARN: Verbindung fehlgeschlagen: {e}")
        time.sleep(2)

if not aq:
    log("FATAL: Keine Verbindung möglich. Starte MSFS und probiere erneut.")
    raise SystemExit(1)

# Werte, die fast immer funktionieren
vars_to_read = [
    ("PLANE LATITUDE", "degrees"),
    ("PLANE LONGITUDE", "degrees"),
    ("PLANE ALTITUDE", "feet"),
    ("AIRSPEED INDICATED", "knots"),
    ("HEADING INDICATOR", "degrees"),
]

none_streak = 0

log("Beginne Reads (10 Sekunden)...")
t_end = time.time() + 10

while time.time() < t_end:
    values = []
    for name, unit in vars_to_read:
        try:
            val = aq.get(name)
        except Exception as e:
            val = None
        values.append((name, val))

    if all(v is None for _, v in values):
        none_streak += 1
    else:
        none_streak = 0

    line = " | ".join([f"{n}={v}" for n, v in values])
    log(line)

    if none_streak >= 5:
        log("WARN: 5x hintereinander nur None → Sim nicht ready oder SimConnect liefert nichts.")
        none_streak = 0

    time.sleep(0.5)

log("Phase1 Live Read beendet.")
log(f"LOGFILE: {os.path.abspath(log_path)}")
