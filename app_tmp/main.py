import time
from logger import setup_logger
from simconnect_client import SimConnectClient
from aircraft_ready import AircraftReady
from state_machine import StateMachine

setup_logger()

print("A380 AI startet...")

sim = SimConnectClient()
sim.connect()

ready = AircraftReady(sim)
sm = StateMachine()

while True:
    if not ready.is_ready():
        print("Warte auf Aircraft Ready...")
        time.sleep(1)
        continue

    state = sm.update(sim)

    print(f"State: {state}")

    time.sleep(0.2)

from aircraft_ready import AircraftReadyDetector

ready = AircraftReadyDetector(sim)

ready.wait_for_sim_ready()
ready.wait_for_fbw_ready()   # optional
