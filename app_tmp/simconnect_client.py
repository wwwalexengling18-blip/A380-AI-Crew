import time

from SimConnect import SimConnect, AircraftRequests


class SimClient:
    def __init__(self):
        self.sm = None
        self.aq = None

    def connect(self):
        self.sm = SimConnect()
        self.aq = AircraftRequests(self.sm, _time=2000)
        print("[SIM] Verbindung erfolgreich")

        # Warmup (optional)
        try:
            _ = self.aq.get("SIM ON GROUND")
        except Exception:
            pass

    def ensure_connected(self):
        if self.sm is None or self.aq is None:
            self.connect()

    def read(self, name: str, default=None, retries: int = 5, delay: float = 0.2):
        """
        Robust read: mehrmals versuchen, nur None als "nicht da" behandeln.
        """
        try:
            self.ensure_connected()

            last = None
            for _ in range(retries):
                last = self.aq.get(name)

                if last is not None:
                    return last

                time.sleep(delay)

            return default if last is None else last

        except Exception as e:
            print(f"[SIM] Read Fehler ({name}): {e} -> reconnect")
            self.sm = None
            self.aq = None
            time.sleep(1.0)
            return default
