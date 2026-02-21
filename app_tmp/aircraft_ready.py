import time

class AircraftReadyDetector:
    def __init__(self, sim):
        self.sim = sim

    def wait_for_sim_ready(self, timeout=60):
        start = time.time()

        while time.time() - start < timeout:
            lat = self.sim.get("PLANE LATITUDE")
            lon = self.sim.get("PLANE LONGITUDE")

            if lat not in [None, "NA"] and lon not in [None, "NA"]:
                print("[READY] SIM READY (Cold & Dark ok)")
                return True

            print("[WAIT] Sim not ready yet...")
            time.sleep(1)

        print("[ERROR] Sim never became ready")
        return False

    def wait_for_fbw_ready(self, timeout=60):
        start = time.time()

        while time.time() - start < timeout:
            val = self.sim.get("AIRSPEED INDICATED")

            if val not in [None, "NA"]:
                print("[READY] FBW/Vars responding")
                return True

            print("[WAIT] FBW not ready yet...")
            time.sleep(1)

        print("[WARN] FBW not ready (Cold & Dark allowed)")
        return False
