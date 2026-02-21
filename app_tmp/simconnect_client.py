import time

class SimClient:
    def __init__(self):
        self.sm = None
        self.aq = None

    def connect(self):
        # Lazy import, damit Fehlermeldungen sauberer sind
        from SimConnect import SimConnect, AircraftRequests

        self.sm = SimConnect()
        self.aq = AircraftRequests(self.sm, _time=2000)
        print("[SIM] Verbindung erfolgreich")

    def ensure_connected(self):
        if self.sm is None or self.aq is None:
            self.connect()

    def read(self, name: str, default=None):
        """
        Liest eine SimVar über AircraftRequests.
        Wenn etwas schiefgeht (z.B. None/Disconnect), geben wir default zurück.
        """
        try:
            self.ensure_connected()
            val = self.aq.get(name)
            if val is None:
                return default
            return val
        except Exception as e:
            print(f"[SIM] Read Fehler ({name}): {e} -> reconnect")
            self.sm = None
            self.aq = None
            time.sleep(1.0)
            return default
