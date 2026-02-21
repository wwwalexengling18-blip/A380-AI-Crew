@echo off
title A380 AI - Variablen Diagnose

echo ================================
echo   Sim Variablen Test
echo ================================
echo.

echo from SimConnect import * > vars_test.py
echo import time >> vars_test.py
echo sm = SimConnect() >> vars_test.py
echo aq = AircraftRequests(sm, _time=2000) >> vars_test.py
echo. >> vars_test.py
echo print("Lese Variablen (10 Sekunden)...") >> vars_test.py
echo for i in range(10): >> vars_test.py
echo     try: >> vars_test.py
echo         ias = aq.get("AIRSPEED INDICATED") >> vars_test.py
echo         alt = aq.get("PLANE ALTITUDE") >> vars_test.py
echo         hdg = aq.get("PLANE HEADING DEGREES TRUE") >> vars_test.py
echo         print(f"IAS={ias} ALT={alt} HDG={hdg}") >> vars_test.py
echo     except Exception as e: >> vars_test.py
echo         print("Fehler:", e) >> vars_test.py
echo     time.sleep(1) >> vars_test.py
echo print("Test beendet") >> vars_test.py

python vars_test.py
pause
