@echo off
title A380 AI Crew - SimConnect Test

set "BASE=%USERPROFILE%\Documents\FBW_A380_Tools\A380_AI_Crew\A380-AI-Crew-main"
cd /d "%BASE%"

python "scripts\test_simconnect.py"
pause
