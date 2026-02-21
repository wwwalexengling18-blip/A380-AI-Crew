import time
import msvcrt

class StateMachine:
    def __init__(self, sim):
        self.sim = sim
        self.t0 = time.time()

    def run(self):
        print("State Machine läuft (Q = Beenden)")

        while True:
            # Q zum Beenden
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == "q":
                    print("State Machine beendet")
                    return

            alt = self.sim.read("INDICATED ALTITUDE", 0)
            ias = self.sim.read("AIRSPEED TRUE", 0)
            hdg = self.sim.read("PLANE HEADING DEGREES TRUE", 0)
            gnd = self.sim.read("SIM ON GROUND", 0)

            up = int(time.time() - self.t0)
            print(f"[LIVE t+{up:>3}s] ALT={alt}  IAS={ias}  HDG={hdg}  GND={gnd}")

            time.sleep(1.0)
