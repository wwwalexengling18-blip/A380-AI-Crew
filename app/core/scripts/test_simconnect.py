from time import sleep

print("Starte SimConnect Test... (MSFS muss laufen)")
try:
    from SimConnect import SimConnect, AircraftRequests
except Exception as e:
    print("IMPORT FEHLER:", e)
    raise

sm = SimConnect()
aq = AircraftRequests(sm, _time=2000)

for i in range(10):
    title = aq.get("TITLE")
    lat = aq.get("PLANE_LATITUDE")
    lon = aq.get("PLANE_LONGITUDE")
    on_ground = aq.get("SIM_ON_GROUND")
    ias = aq.get("AIRSPEED_INDICATED")
    print(f"[{i+1}/10] TITLE={title} LAT={lat} LON={lon} GND={on_ground} IAS={ias}")
    sleep(1)

print("SimConnect Test fertig.")
