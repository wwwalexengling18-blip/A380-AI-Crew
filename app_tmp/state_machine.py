import time

class StateMachine:
    def run(self):
        print("State Machine läuft (STRG+C zum Beenden)")
        try:
            while True:
                # später kommen hier: Aircraft Ready, ECAM, SOP Steps, GSX, usw.
                time.sleep(1.0)
        except KeyboardInterrupt:
            print("State Machine beendet")
