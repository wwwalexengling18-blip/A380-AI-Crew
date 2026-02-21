import time
from logger import log, log_exception, log_module_version

def simconnect_probe(sim):
    log("[DIAG] SimConnect Probe startet...")
    tests = [
        "PLANE LATITUDE",
        "PLANE LONGITUDE",
        "SIMULATION TIME",
        "ZULU TIME",
        "SIM IS PAUSED",
        "PLANE ALTITUDE",
        "AIRSPEED INDICATED",
        "SIM ON GROUND",
    ]
    for t in tests:
        v = sim.read(t, "NA")
        log(f"[SIMVAR] {t} = {v}")

def wasim_probe():
    log("[DIAG] WASim Probe startet...")
    try:
        from wasimcommander import WASimCommander  # type: ignore
    except Exception as e:
        log_exception("[DIAG] wasimcommander import FAIL", e)
        return

    try:
        w = WASimCommander()
        w.connect()
        log("[WASIM] verbunden")
        for _ in range(5):
            lat = w.get("PLANE LATITUDE")
            lon = w.get("PLANE LONGITUDE")
            alt = w.get("PLANE ALTITUDE")
            log(f"[WASIM] LAT={lat} LON={lon} ALT={alt}")
            time.sleep(1)
    except Exception as e:
        log_exception("[DIAG] WASim Probe FAIL", e)

def run_all(sim):
    # Module check
    log_module_version("SimConnect")
    log_module_version("wasimcommander")

    # SimConnect probe
    try:
        simconnect_probe(sim)
    except Exception as e:
        log_exception("[DIAG] SimConnect Probe FAIL", e)

    # WASim probe (optional)
    wasim_probe()
