import time
import msvcrt

class StateMachine:
    def run(self):
        print("State Machine läuft (Q + Enter = Beenden)")
        while True:
            # Quit check
            if msvcrt.kbhit():
                key = msvcrt.getwch()
                if key.lower() == "q":
                    print("State Machine beendet")
                    return

            time.sleep(0.2)
