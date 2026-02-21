import time
import os
from datetime import datetime

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)

log_file = os.path.join(log_dir, f"a380_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

def log(msg):
    print(msg)
    with open(log_file, "a", encoding="utf-8") as f:
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
    "LANDING",
    "SHUTDOWN",
    "COLD_DARK_END"
]

for phase in phases:
    log(f"Phase: {phase}")
    time.sleep(1.5)

log("================================")
log(" A380 AI Crew Simulation Ende")
log("================================")
