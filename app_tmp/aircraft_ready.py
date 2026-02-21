import time

class AircraftReady:
    def __init__(self, sim):
        self.sim = sim

    def wait(self):
        print("[READY] Warte auf Aircraft Daten...")

        for _ in range(30):  # max ~30 Sekunden warten
            alt = self.sim.read("PLANE ALTITUDE", None)

            if alt not in (None, 0):
                print("[READY] Aircraft Daten vorhanden")
                return True

            time.sleep(1)

        print("[READY] Timeout – trotzdem weiter")
        return False
