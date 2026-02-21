
from SimConnect import SimConnect

class SimClient:
    def __init__(self):
        self.sm = None

    def connect(self):
        try:
            self.sm = SimConnect()
            print("[SIM] Verbindung erfolgreich")
        except Exception as e:
            print(f"[SIM] Fehler: {e}")
