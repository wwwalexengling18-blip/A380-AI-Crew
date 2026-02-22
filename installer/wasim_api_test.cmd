@echo off
setlocal
title A380-AI-Crew - WASimCommander API Test

set ROOT=%~dp0..
set VENV=%ROOT%\.venv

echo ==========================================
echo WASimCommander API Test (Ping + LVar List)
echo ==========================================
echo.

if exist "%VENV%\Scripts\python.exe" (
  "%VENV%\Scripts\python.exe" -m pip show pythonnet >nul 2>nul || (
    echo Installiere pythonnet...
    "%VENV%\Scripts\python.exe" -m pip install pythonnet
  )
  "%VENV%\Scripts\python.exe" "%~dp0wasim_api_test.py"
) else (
  py -m pip show pythonnet >nul 2>nul || (
    echo Installiere pythonnet...
    py -m pip install pythonnet
  )
  py "%~dp0wasim_api_test.py"
)

echo.
echo Fertig. Schau in logs\wasim_api_test_*.log
pause
