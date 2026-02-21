import time

class AircraftReady:
    def __init__(self, sim, logger):
        self.sim = sim
        self.log = logger

    def wait_for_sim_ready(self, timeout=90):
        """
        Gilt auch in Cold & Dark.
        Erst wenn Lat/Lon valide -> SIM READY
        """
        self.log.info("[READY] waiting for SIM READY (Lat/Lon valid)")
        start = time.time()

        while time.time() - start < timeout:
            self.sim.soft_reconnect_if_needed()

            lat = self.sim.get("PLANE LATITUDE")
            lon = self.sim.get("PLANE LONGITUDE")

            if lat is not None and lon is not None:
                self.log.info("[READY] SIM READY ✅ (Cold & Dark readable)")
                return True

            self.log.info("[READY] ...not yet (Lat/Lon NA) waiting")
            time.sleep(1.0)

        self.log.error("[READY] SIM READY timeout ❌")
        return False

    def wait_for_fbw_ready(self, timeout=120):
        """
        Optional: FBW/WASM/Variablen readiness.
        Wenn nicht ready: kein Abbruch, nur Warnung.
        """
        self.log.info("[READY] waiting for FBW READY (vars responding)")
        start = time.time()

        while time.time() - start < timeout:
            self.sim.soft_reconnect_if_needed()

            # Minimaler Plausibility-Check (ersetzbar durch echte FBW/WASIM Variable)
            on_ground = self.sim.get("SIM ON GROUND")
            if on_ground in (0, 1):
                self.log.info("[READY] FBW READY ✅ (vars plausible)")
                return True

            self.log.info("[READY] ...FBW not ready yet (still NA) waiting")
            time.sleep(1.0)

        self.log.warn("[READY] FBW not ready (continuing anyway) ⚠️")
        return False
