@echo off
setlocal EnableExtensions

:: Selbst-Relaunch, damit es nicht sofort schließt
if /i not "%~1"=="__RUN__" (
  start "A380 AI - Bridge Ports Check" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Bridge Ports Check (fixed)

echo =========================================
echo   A380 AI - Bridge Ports Check (fixed)
echo =========================================
echo.

set "PORTS=19784 19785 8380 5000 8080 3000 9000 9876 8777 8888 1337"

for %%P in (%PORTS%) do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$p=%%P; $ok=(Test-NetConnection -ComputerName '127.0.0.1' -Port $p -WarningAction SilentlyContinue).TcpTestSucceeded; if ($ok) { Write-Host ('Port ' + $p + ' : OPEN') } else { Write-Host ('Port ' + $p + ' : CLOSED') }"
)

echo.
echo Hinweis:
echo - Wenn mindestens ein Port OPEN ist, ist eine lokale Bridge/API erreichbar.
echo - Wenn alles CLOSED ist, ist das normal bei WASimCommander: es ist kein HTTP-Server.
echo.
pause
