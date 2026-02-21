import os
import time

from logger import Logger
from simconnect_client import SimConnectClient
from aircraft_ready import AircraftReady
from state_machine import StateMachine

def main():
    tools_dir = os.path.join(os.path.expandvars("%USERPROFILE%"), "Documents", "FBW_A380_Tools")
    log_dir = os.path.join(tools_dir, "logs")

    log = Logger(log_dir=log_dir, prefix="diag")
    sim = SimConnectClient(log, read_hz=10)

    if not sim.connect():
        log.error("Could not connect to sim. Exiting.")
        return

    ready = AircraftReady(sim, log)

    # 1) SIM READY => Cold & Dark lesbar
    if not ready.wait_for_sim_ready(timeout=90):
        log.error("SIM never became ready.")
        return

    # 2) Optional: FBW READY
    fbw_ready = ready.wait_for_fbw_ready(timeout=120)

    sm = StateMachine(log)
    log.info("Starting main loop... (Ctrl+C to stop)")

    try:
        while True:
            sim.soft_reconnect_if_needed()

            # Minimal-Kontext (erweitern wir später)
            on_ground = sim.get("SIM ON GROUND")
            ctx = {
                "fbw_ready": fbw_ready,
                "on_ground": on_ground,
            }

            sm.tick(ctx)

            # Status alle ~2 Sekunden
            time.sleep(0.2)

    except KeyboardInterrupt:
        log.warn("Stopped by user.")
    finally:
        sim.disconnect()
        log.close()

if __name__ == "__main__":
    main()
