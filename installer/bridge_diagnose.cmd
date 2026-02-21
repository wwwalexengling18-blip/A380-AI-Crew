@echo off
setlocal EnableExtensions
title A380 AI - Bridge Diagnose (stabil)

echo =========================================
echo   A380 AI - Bridge Diagnose
echo =========================================
echo.

echo [1/2] TCP-Port Check (localhost)
echo.

set PORTS=8380 5000 8080 3000 9000 9876 19784

for %%P in (%PORTS%) do (
    echo Pruefe Port %%P ...
    powershell -NoProfile -Command ^
    "if(Test-NetConnection -ComputerName 127.0.0.1 -Port %%P -WarningAction SilentlyContinue).TcpTestSucceeded {exit 0} else {exit 1}" >nul 2>&1

    if errorlevel 1 (
        echo Port %%P : CLOSED
    ) else (
        echo Port %%P : OPEN
    )
)

echo.
echo [2/2] HTTP Schnelltest
echo.

for %%P in (%PORTS%) do (
    powershell -NoProfile -Command ^
    "try{(Invoke-WebRequest -Uri http://127.0.0.1:%%P -TimeoutSec 2).StatusCode}catch{}"
)

echo.
echo =========================================
echo Fertig. Fenster bleibt offen.
echo =========================================
pause
cmd /k
