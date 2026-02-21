import time
import msvcrt

class StateMachine:
    def __init__(self, sim):
        self.sim = sim
        self.t0 = time.time()

    def run(self):
        print("State Machine läuft (Q = Beenden)")

        while True:
            # Q zum Beenden (keine Batch J/N Nachfrage)
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == "q":
                    print("State Machine beendet")
                    return

            # Live Werte lesen (ein paar Beispiele)
            alt = self.sim.read("PLANE ALTITUDE", default=0)
            ias = self.sim.read("AIRSPEED INDICATED", default=0)
            hdg = self.sim.read("PLANE HEADING DEGREES MAGNETIC", default=0)
            on_ground = self.sim.read("SIM ON GROUND", default=0)

            # hübsche Ausgabe (läuft jede Sekunde)
            up = int(time.time() - self.t0)
            print(f"[LIVE t+{up:>3}s] ALT={alt}  IAS={ias}  HDG={hdg}  GND={on_ground}")

            time.sleep(1.0)
