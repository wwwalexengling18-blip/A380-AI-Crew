@echo off
setlocal EnableExtensions
title A380 AI - Bridge Ports Check

echo =========================================
echo   A380 AI - Bridge Ports Check
echo =========================================
echo.

set PORTS=19784 19785 8380 5000 8080 3000 9000 9876 8777 8888 1337

for %%P in (%PORTS%) do (
  powershell -NoProfile -Command ^
    "if(Test-NetConnection -ComputerName 127.0.0.1 -Port %%P -WarningAction SilentlyContinue).TcpTestSucceeded { 'Port %%P : OPEN' } else { 'Port %%P : CLOSED' }"
)

echo.
echo Hinweis:
echo - Wenn ALLES CLOSED ist: Bridge ist nicht gestartet oder nicht installiert.
echo - Wenn ein Port OPEN ist: Schick mir den Port, dann bauen wir den LVar-Test.
echo.

pause
cmd /k
