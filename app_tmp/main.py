from state_machine import StateMachine
from logger import log

if __name__ == "__main__":
    log("A380 AI Crew gestartet")
    sm = StateMachine()
    sm.run()
