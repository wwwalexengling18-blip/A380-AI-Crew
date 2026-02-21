import time
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"a380_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def log(msg: str) -> None:
    print(msg, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("================================")
log(" A380 AI Crew gestartet")
log(" Status: Initialisierung")
log("================================")

phases = [
    "COLD_DARK",
    "POWER_UP",
    "COCKPIT_PREP",
    "ENGINE_START",
    "TAXI",
    "TAKEOFF",
    "CLIMB",
    "CRUISE",
    "DESCENT",
    "APPROACH",
    "LANDING",
    "TAXI_IN",
    "SHUTDOWN",
    "COLD_DARK_END",
]

for phase in phases:
    log(f"Phase: {phase}")
    time.sleep(1.5)

log("================================")
log(" A380 AI Crew Simulation Ende")
log("================================")
