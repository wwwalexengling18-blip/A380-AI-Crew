from logger import log
from simconnect_client import SimClient
from state_machine import StateMachine

if __name__ == "__main__":
    log("A380 AI Crew gestartet")

    sim = SimClient()
    sim.connect()

    sm = StateMachine(sim)
    sm.run()
