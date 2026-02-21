@echo off
title A380 AI Crew - RUN

set BASE=%USERPROFILE%\Documents\FBW_A380_Tools\A380_AI_Crew\A380-AI-Crew-main
cd /d "%BASE%"

echo ============================
echo   A380 AI Crew - START
echo ============================

python "app\main.py"
pause
