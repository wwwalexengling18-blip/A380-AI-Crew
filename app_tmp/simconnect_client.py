import time

def read(self, name: str, default=None, retries: int = 5, delay: float = 0.2):
    """
    Robust read:
    - probiert mehrfach
    - akzeptiert Werte ungleich None
    - wartet kurz zwischen Versuchen
    """
    try:
        self.ensure_connected()

        last = None
        for _ in range(retries):
            last = self.aq.get(name)

            # Einige Wrapper geben None/0 bei "noch nicht ready" zurück.
            # Wir akzeptieren alles, was nicht None ist.
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
