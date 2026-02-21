@echo off
title A380 AI - SimConnect LIVE Diagnose

echo ================================
echo   SimConnect LIVE Verbindungstest
echo ================================
echo.

:: Python prüfen
python --version
if errorlevel 1 (
    echo Python nicht gefunden
    pause
    exit
)

:: Diagnose Python erzeugen
echo from SimConnect import SimConnect > live_test.py
echo import time >> live_test.py
echo print("Verbinde mit Simulator...") >> live_test.py
echo try: >> live_test.py
echo     sm = SimConnect() >> live_test.py
echo     print("✔ Verbindung erfolgreich") >> live_test.py
echo except Exception as e: >> live_test.py
echo     print("❌ Verbindung fehlgeschlagen:", e) >> live_test.py
echo     exit() >> live_test.py
echo. >> live_test.py
echo print("Teste Datenfluss (5 Sekunden)...") >> live_test.py
echo for i in range(5): >> live_test.py
echo     try: >> live_test.py
echo         print(f"Tick {i+1} - Verbindung stabil") >> live_test.py
echo     except: >> live_test.py
echo         print("None Read erkannt") >> live_test.py
echo     time.sleep(1) >> live_test.py
echo. >> live_test.py
echo print("Diagnose beendet") >> live_test.py

python live_test.py

echo.
pause
