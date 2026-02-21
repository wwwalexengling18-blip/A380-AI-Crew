@echo off
title A380 AI Crew - RUN

set "BASE=%USERPROFILE%\Documents\FBW_A380_Tools\A380_AI_Crew"

echo ============================
echo   A380 AI Crew - START
echo ============================
echo.

REM Kandidaten (verschiedene Layouts abdecken)
set "CAND1=%BASE%\A380-AI-Crew-main\app\main.py"
set "CAND2=%BASE%\A380-AI-Crew-main\main.py"
set "CAND3=%BASE%\A380-AI-Crew-main\app\core\main.py"
set "CAND4=%BASE%\app\main.py"
set "CAND5=%BASE%\main.py"

set "PY="

if exist "%CAND1%" set "PY=%CAND1%"
if not defined PY if exist "%CAND2%" set "PY=%CAND2%"
if not defined PY if exist "%CAND3%" set "PY=%CAND3%"
if not defined PY if exist "%CAND4%" set "PY=%CAND4%"
if not defined PY if exist "%CAND5%" set "PY=%CAND5%"

REM Notfall: Suche rekursiv nach app\main.py oder main.py
if not defined PY (
  echo Suche main.py automatisch...
  for /r "%BASE%" %%F in (main.py) do (
    set "PY=%%F"
    goto :FOUND
  )
)

:FOUND
if not defined PY (
  echo FEHLER: Keine main.py gefunden unter:
  echo %BASE%
  echo.
  echo Inhalte des Ordners:
  dir "%BASE%"
  echo.
  pause
  exit /b 1
)

echo Gefunden: %PY%
echo.

REM Arbeitsordner auf Projekt-Root setzen (Ordner der main.py)
for %%D in ("%PY%") do set "WORK=%%~dpD"
cd /d "%WORK%"

python "%PY%"

echo.
echo Fertig.
pause
