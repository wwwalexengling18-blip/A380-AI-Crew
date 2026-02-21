from state_machine import StateMachine
from logger import log
from simconnect_client import SimClient

if __name__ == "__main__":
    log("A380 AI Crew gestartet")

    sim = SimClient()
    sim.connect()

    sm = StateMachine()
    sm.run()
