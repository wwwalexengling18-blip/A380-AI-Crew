@echo off
title A380 AI Crew - RUN

set BASE=%USERPROFILE%\Documents\FBW_A380_Tools\A380_AI_Crew\A380-AI-Crew-main

echo ============================
echo   A380 AI Crew - START
echo ============================
echo.

if not exist "%BASE%\main.py" (
    echo Fehler: KI Core nicht gefunden
    echo Erwartet: %BASE%\main.py
    pause
    exit
)

echo Starte KI Core...
echo.

python "%BASE%\main.py"

echo.
echo KI beendet
pause
