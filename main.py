import time

print("================================")
print(" A380 AI Crew gestartet")
print(" Status: Initialisierung")
print("================================")

phases = [
    "COLD_DARK",
    "POWER_UP",
    "COCKPIT_PREP",
    "ENGINE_START",
    "TAXI",
    "TAKEOFF",
    "CLIMB",
    "CRUISE",
    "DESCENT",
    "LANDING",
    "SHUTDOWN",
    "COLD_DARK_END"
]

for phase in phases:
    print(f"Phase: {phase}")
    time.sleep(1)

print("================================")
print(" A380 AI Crew Simulation Ende")
print("================================")
