from simconnect_client import SimClient
import time

sim = SimClient()
sim.connect()

print("PROBE START")

tests = [
    "PLANE LATITUDE",
    "PLANE LONGITUDE",
    "SIMULATION TIME",
    "ZULU TIME",
    "GROUND VELOCITY"
]

for t in tests:
    v = sim.read(t, "NA")
    print(t, "=", v)

print("PROBE LOOP")
while True:
    v = sim.read("PLANE LATITUDE", "NA")
    print("LAT:", v)
    time.sleep(1)
