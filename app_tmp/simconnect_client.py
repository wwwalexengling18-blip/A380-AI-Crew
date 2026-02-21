import time
import threading

class SimConnectClient:
    """
    Ziele:
    - get(var) liefert None statt Crash
    - NA/None-Reads werden toleriert (kein Reconnect-Spam)
    - Soft reconnect, wenn wirklich tot
    - Read-Rate wird gedrosselt
    """

    def __init__(self, logger, read_hz=10):
        self.log = logger
        self.read_interval = max(0.05, 1.0 / max(1, read_hz))
        self._lock = threading.Lock()

        self._sc = None  # <- hier hängt dein echtes SimConnect Objekt
        self._connected = False

        self._none_streak = 0
        self._last_ok = 0.0

    # ---- HIER: deine echte Connect-Logik rein ----
    def connect(self):
        with self._lock:
            try:
                # TODO: ersetze das mit deinem echten Connect
                # self._sc = SimConnect()
                # self._aq = AircraftRequests(self._sc, _time=2000)
                self._connected = True
                self._none_streak = 0
                self._last_ok = time.time()
                self.log.info("[SIM] connect OK")
                return True
            except Exception as e:
                self._connected = False
                self.log.error(f"[SIM] connect FAIL: {e}")
                return False

    def disconnect(self):
        with self._lock:
            try:
                self._connected = False
                self._sc = None
                self.log.warn("[SIM] disconnected")
            except Exception as e:
                self.log.error(f"[SIM] disconnect error: {e}")

    def is_connected(self):
        return self._connected

    # ---- Wichtig: NA/None safe get() ----
    def get(self, var_name):
        """
        Erwartung: du mapst var_name auf echte SimConnect Reads.
        Wenn du schon eine get()-Funktion hast, nutze diese Struktur:
        - try/except
        - None/NA -> streak erhöhen
        - OK -> streak reset
        """
        time.sleep(self.read_interval)

        try:
            # TODO: ersetze durch echten Read:
            # val = self._aq.get(var_name)
            val = self._fake_read(var_name)  # nur placeholder

            if val is None or val == "NA":
                self._none_streak += 1
                return None

            self._none_streak = 0
            self._last_ok = time.time()
            return val

        except Exception as e:
            self._none_streak += 1
            self.log.warn(f"[SIM] read error {var_name}: {e}")
            return None

    def soft_reconnect_if_needed(self, max_none_streak=50, max_silence_sec=10):
        """
        Reconnect nur, wenn:
        - lange Zeit kein gültiger Wert kam UND
        - none_streak hoch ist
        """
        if not self._connected:
            return self.connect()

        silence = time.time() - self._last_ok
        if self._none_streak >= max_none_streak and silence >= max_silence_sec:
            self.log.warn(f"[SIM] too many None reads ({self._none_streak}) -> soft reconnect")
            self.disconnect()
            time.sleep(1.0)
            return self.connect()

        return True

    # -------- placeholder --------
    def _fake_read(self, var_name):
        # Damit das Script nicht crasht, falls du es testest ohne echte Bindings.
        return None
