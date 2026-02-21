from simconnect_client import SimClient
import time

sim = SimClient()
sim.connect()

print("PROBE START")

tests = [
    "PLANE LATITUDE",
    "PLANE LONGITUDE",
    "SIMULATION TIME",
    "ZULU TIME",
    "GROUND VELOCITY"
]

for t in tests:
    v = sim.read(t, "NA")
    print(t, "=", v)

print("PROBE LOOP")
while True:
    v = sim.read("PLANE LATITUDE", "NA")
    print("LAT:", v)
    time.sleep(1)

from logger import init_logger, log
from simconnect_client import SimClient
from diagnose import run_all

if __name__ == "__main__":
    log_path = init_logger("A380_AI_DIAG")
    log(f"Logfile: {log_path}")

    sim = SimClient()
    try:
        sim.connect()
    except Exception as e:
        log(f"[SIM] Connect FAIL: {e}")

    # Diagnose laufen lassen (SimConnect + ggf. WASim)
    run_all(sim)

    log("Diagnose fertig. Du kannst die Logdatei öffnen und hier posten.")
