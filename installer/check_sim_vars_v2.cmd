@echo off
title A380 AI - Variablen Diagnose V2

echo ================================
echo   Sim Variablen Test V2
echo ================================
echo.

echo from SimConnect import * > vars_test_v2.py
echo import time >> vars_test_v2.py
echo. >> vars_test_v2.py
echo sm = SimConnect() >> vars_test_v2.py
echo aq = AircraftRequests(sm, _time=1000) >> vars_test_v2.py
echo. >> vars_test_v2.py
echo print("Warte 5 Sekunden (Aircraft Ready)...") >> vars_test_v2.py
echo time.sleep(5) >> vars_test_v2.py
echo. >> vars_test_v2.py
echo print("Lese Variablen (15 Sekunden)...") >> vars_test_v2.py
echo for i in range(15): >> vars_test_v2.py
echo     try: >> vars_test_v2.py
echo         ias = aq.get("AIRSPEED INDICATED", True) >> vars_test_v2.py
echo         alt = aq.get("PLANE ALTITUDE", True) >> vars_test_v2.py
echo         hdg = aq.get("PLANE HEADING DEGREES TRUE", True) >> vars_test_v2.py
echo. >> vars_test_v2.py
echo         if None in (ias, alt, hdg): >> vars_test_v2.py
echo             print(f"Tick {i+1}: NONE READ -> IAS={ias} ALT={alt} HDG={hdg}") >> vars_test_v2.py
echo         else: >> vars_test_v2.py
echo             print(f"Tick {i+1}: IAS={ias:.1f} ALT={alt:.1f} HDG={hdg:.1f}") >> vars_test_v2.py
echo. >> vars_test_v2.py
echo     except Exception as e: >> vars_test_v2.py
echo         print("Fehler:", e) >> vars_test_v2.py
echo. >> vars_test_v2.py
echo     time.sleep(1) >> vars_test_v2.py
echo. >> vars_test_v2.py
echo print("Test beendet") >> vars_test_v2.py

python vars_test_v2.py
pause
