@echo off
setlocal enabledelayedexpansion
title A380-AI-Crew - SimCommander / SimConnect Check

REM ====== ANPASSEN (falls du einen anderen Port nutzt) ======
set HOST=127.0.0.1
set PORT=8383
REM ==========================================================

echo ==============================================
echo  A380-AI-Crew - Verbindungstest
echo ==============================================
echo Host: %HOST%
echo Port: %PORT%
echo.

REM --- 1) SimConnect Live Test (wenn vorhanden) ---
if exist "%~dp0check_simconnect_live.cmd" (
  echo [1/3] SimConnect Live Test...
  call "%~dp0check_simconnect_live.cmd"
) else (
  echo [1/3] WARN: check_simconnect_live.cmd nicht gefunden.
)

echo.
echo [2/3] Port-Test (SimCommander/Bridge)...
powershell -NoProfile -Command ^
  "$h='%HOST%'; $p=%PORT%;" ^
  "try { $c=Test-NetConnection -ComputerName $h -Port $p -WarningAction SilentlyContinue; " ^
  "if($c.TcpTestSucceeded){ 'OK: Port offen (Bridge erreichbar)'} else { 'FAIL: Port zu (Bridge nicht erreichbar)' } }" ^
  "catch { 'FAIL: Test-NetConnection Fehler: ' + $_.Exception.Message }"

echo.
echo [3/3] Optional: HTTP Ping (falls Bridge HTTP spricht)...
powershell -NoProfile -Command ^
  "$u='http://%HOST%:%PORT%/';" ^
  "try { $r=Invoke-WebRequest -Uri $u -UseBasicParsing -TimeoutSec 2; 'OK: HTTP Antwort: ' + $r.StatusCode }" ^
  "catch { 'INFO: Kein HTTP oder keine Antwort (ist ok, wenn Bridge kein HTTP nutzt).' }"

echo.
echo ==============================================
echo Fertig.
echo Wenn SimConnect OK ist, aber Port FAIL:
echo   -> Bridge/SimCommander nicht gestartet oder anderer Port.
echo ==============================================
pause
