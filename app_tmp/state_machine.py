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

            # --- TEST: liefert der Sim überhaupt Zeit/Status? ---
            sim_time = self.sim.read("SIMULATION TIME", -1)
            zulu = self.sim.read("ZULU TIME", -1)
            paused = self.sim.read("SIM IS PAUSED", -1)

            # --- LIVE: Basiswerte ---
            alt = self.sim.read("PLANE ALTITUDE", -1)
            ias = self.sim.read("AIRSPEED INDICATED", -1)
            hdg = self.sim.read("PLANE HEADING DEGREES TRUE", -1)
            gnd = self.sim.read("SIM ON GROUND", -1)

            up = int(time.time() - self.t0)
            print(
                f"[t+{up:>3}s] TIME={sim_time} ZULU={zulu} PAUSED={paused} | "
                f"ALT={alt} IAS={ias} HDG={hdg} GND={gnd}"
            )

            time.sleep(1.0)
