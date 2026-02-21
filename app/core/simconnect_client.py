
import time

class SimClient:
    """
    SimClient mit optionaler SimConnect-Unterstützung.
    Wenn SimConnect nicht installiert/verfügbar ist, läuft es als Stub weiter.
    """

    def __init__(self, log, read_hz: float = 10.0):
        self.log = log
        self.read_interval = 1.0 / max(1.0, float(read_hz))
        self._last_read_t = 0.0
        self._cache = {}
        self.connected = False

        self._sc = None
        self._aq = None
        self._use_stub = True

    def connect(self):
        # Versuche SimConnect dynamisch zu importieren
        try:
            # Häufig genutzte Python-Lib: "SimConnect"
            from SimConnect import SimConnect, AircraftRequests  # type: ignore

            self._sc = SimConnect()
            self._aq = AircraftRequests(self._sc, _time=2000)  # ms timeout
            self._use_stub = False
            self.connected = True
            self.log("[SIM] SimConnect verbunden.")
            return
        except Exception as e:
            self._use_stub = True
            self.connected = True  # wir laufen im Stub weiter
            self.log(f"[SIM] SimConnect NICHT aktiv (Fallback Stub). Grund: {e}")

    def disconnect(self):
        self.connected = False
        try:
            if self._sc:
                self._sc.exit()
        except Exception:
            pass
        self.log("[SIM] Getrennt.")

    def _read_simconnect_snapshot(self) -> dict:
        # Wenn irgendwas schiefgeht, fallen wir zurück auf Stub
        try:
            aq = self._aq
            if aq is None:
                raise RuntimeError("AircraftRequests not ready")

            # Diese Variablen sind sehr basic und stabil:
            title = aq.get("TITLE")
            lat = aq.get("PLANE_LATITUDE")
            lon = aq.get("PLANE_LONGITUDE")
            alt = aq.get("PLANE_ALTITUDE")
            on_ground = aq.get("SIM_ON_GROUND")
            airspeed = aq.get("AIRSPEED_INDICATED")

            position_ok = (lat is not None and lon is not None)

            return {
                "title": title,
                "lat": lat,
                "lon": lon,
                "altitude_ft": alt,
                "on_ground": bool(on_ground) if on_ground is not None else None,
                "airspeed_kt": airspeed,
                "position_ok": bool(position_ok),
                "sim_time_ok": True,  # kann man später erweitern
                "source": "simconnect",
            }
        except Exception as e:
            self.log(f"[SIM] SimConnect Read Fehler -> Stub Snapshot. Grund: {e}")
            return self._read_stub_snapshot()

    def _read_stub_snapshot(self) -> dict:
        # Fallback (läuft immer)
        return {
            "title": "FBW A380X (Stub)",
            "lat": 0.0,
            "lon": 0.0,
            "altitude_ft": 0.0,
            "on_ground": True,
            "airspeed_kt": 0.0,
            "position_ok": True,
            "sim_time_ok": True,
            "source": "stub",
        }

    def snapshot(self) -> dict:
        now = time.time()
        if now - self._last_read_t < self.read_interval and self._cache:
            return self._cache

        self._last_read_t = now

        if self._use_stub:
            snap = self._read_stub_snapshot()
        else:
            snap = self._read_simconnect_snapshot()

        self._cache = snap
        return snap
