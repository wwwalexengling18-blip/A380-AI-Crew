@echo off
title A380 AI - SimConnect Diagnose

echo ================================
echo   A380 AI SimConnect Check
echo ================================
echo.

:: Python vorhanden?
python --version
if errorlevel 1 (
    echo.
    echo ❌ Python nicht gefunden!
    pause
    exit
)

echo.
echo ✔ Python erkannt
echo.

:: Temporäres Diagnose-Skript erzeugen
echo import importlib > simconnect_check.py
echo libs = ["SimConnect","simconnect","pymSimConnect","msfs","pySimConnect"] >> simconnect_check.py
echo print("---- SimConnect Bibliotheken ----") >> simconnect_check.py
echo for lib in libs: >> simconnect_check.py
echo     try: >> simconnect_check.py
echo         importlib.import_module(lib) >> simconnect_check.py
echo         print(f"✔ Gefunden: {lib}") >> simconnect_check.py
echo     except: >> simconnect_check.py
echo         print(f"- Nicht vorhanden: {lib}") >> simconnect_check.py

echo.
python simconnect_check.py

echo.
echo ================================
echo Check beendet
echo ================================
pause
