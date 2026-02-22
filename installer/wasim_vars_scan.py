import os, time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGDIR = ROOT / "logs"
LOGDIR.mkdir(exist_ok=True)

LIST_PATH = Path(__file__).resolve().parent / "wasim_vars_list.txt"
LOG_PATH = LOGDIR / f"wasim_vars_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg: str):
    line = f"{datetime.now().strftime('%H:%M:%S')} | {msg}"
    print(line)
    LOG_PATH.open("a", encoding="utf-8").write(line + "\n")

def load_vars():
    if not LIST_PATH.exists():
        raise FileNotFoundError(f"Fehlt: {LIST_PATH}")
    out = []
    for raw in LIST_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
        s = raw.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out

log("Starte Vars Scan...")

try:
    from SimConnect import SimConnect, AircraftRequests
except Exception as e:
    log(f"ERROR: SimConnect Python Lib fehlt: {e}")
    raise

# Connect
aq = None
for attempt in range(1, 6):
    try:
        log(f"Verbinde SimConnect (Attempt {attempt}/5)...")
        sm = SimConnect()
        aq = AircraftRequests(sm, _time=2000)
        log("OK: SimConnect verbunden.")
        break
    except Exception as e:
        log(f"WARN: Connect failed: {e}")
        time.sleep(2)

if not aq:
    log("FATAL: Keine SimConnect Verbindung möglich.")
    raise SystemExit(1)

vars_list = load_vars()
log(f"Variablen geladen: {len(vars_list)}")

ok = 0
none = 0

# 3 Runden lesen, damit “zu früh” weniger stört
rounds = 3
for r in range(1, rounds + 1):
    log(f"--- Runde {r}/{rounds} ---")
    for name in vars_list:
        try:
            val = aq.get(name)
        except Exception as e:
            val = None
        if val is None:
            none += 1
            log(f"FAIL | {name} = None")
        else:
            ok += 1
            log(f"OK   | {name} = {val}")
    time.sleep(0.5)

log("=== Ergebnis ===")
log(f"OK Reads:   {ok}")
log(f"None Reads: {none}")
log(f"LOGFILE: {LOG_PATH.resolve()}")
