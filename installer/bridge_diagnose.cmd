@echo off
setlocal EnableExtensions EnableDelayedExpansion

:: =========================================================
:: Selbst-Relaunch: Immer in eigenem CMD-Fenster mit /k laufen
:: =========================================================
if /i not "%~1"=="__RUN__" (
  start "A380 AI - Bridge Diagnose" cmd /k ""%~f0" __RUN__"
  exit /b
)

title A380 AI - Bridge Diagnose (bleibt offen)

echo ==================================================
echo   A380 AI - Bridge Diagnose (SimBridge / WASM etc.)
echo ==================================================
echo.

:: --------- BASIC: Python vorhanden? (optional) ----------
python --version >nul 2>&1
if errorlevel 1 ( set HASPY=0 ) else ( set HASPY=1 )

:: --------- Prozesse (nur Hinweis) ----------
echo [1/5] Prozesse (Hinweis):
tasklist | findstr /i "SimBridge node.exe python.exe msfs" >nul
if errorlevel 1 (
  echo - Keine typischen Prozesse gefunden (kann trotzdem laufen).
) else (
  echo - Gefundene passende Prozesse:
  tasklist | findstr /i "SimBridge node.exe python.exe msfs"
)
echo.

:: --------- Port-Checks (TCP) ----------
echo [2/5] TCP-Port Check (localhost):
echo.

set "PORTS=8380 5000 8080 3000 9000 9876 19784"
for %%P in (%PORTS%) do call :CHECKPORT %%P
echo.

:: --------- HTTP Endpoints (wenn Port offen) ----------
echo [3/5] HTTP-Check auf typische URLs (nur wenn Port offen):
echo.

for %%P in (%PORTS%) do (
  if exist "%TEMP%\port_%%P.open" call :CHECKHTTP %%P
)
echo.

:: --------- Optionale Python-HTTP Probe ----------
echo [4/5] Optional: Python HTTP Probe (mehr Details)
if "%HASPY%"=="1" (
  echo - Python gefunden, starte Probe...
  call :PYPROBE
) else (
  echo - Python nicht im PATH -> uebersprungen.
)
echo.

echo [5/5] Ergebnis-Hinweis:
echo - OPEN bei TCP bedeutet: Da lauscht etwas auf dem Port.
echo - HTTP 200/3xx bedeutet: Web-API antwortet.
echo - Wenn alles CLOSED ist: Bridge laeuft nicht oder anderer Port.
echo.

echo ==================================================
echo Fertig. Dieses Fenster bleibt offen.
echo ==================================================
echo.
pause
goto :EOF

:CHECKPORT
set "P=%~1"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$p=%P%; $r = Test-NetConnection -ComputerName 127.0.0.1 -Port $p -WarningAction SilentlyContinue; if($r.TcpTestSucceeded){ exit 0 } else { exit 1 }" >nul 2>&1
if errorlevel 1 (
  echo Port %P% : CLOSED
  if exist "%TEMP%\port_%P%.open" del /q "%TEMP%\port_%P%.open" >nul 2>&1
) else (
  echo Port %P% : OPEN
  echo open>"%TEMP%\port_%P%.open"
)
exit /b 0

:CHECKHTTP
set "P=%~1"
for %%U in ("/" "/api" "/status" "/health" "/v1" "/sim" "/metrics") do (
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$u='http://127.0.0.1:%P%%%U'; try { $resp = Invoke-WebRequest -UseBasicParsing -TimeoutSec 2 -Uri $u; $code=$resp.StatusCode; Write-Host ('HTTP ' + $code + '  ' + $u) } catch { }"
)
exit /b 0

:PYPROBE
set "PY=%TEMP%\bridge_probe.py"
(
  echo import urllib.request
  echo ports = [8380,5000,8080,3000,9000,9876,19784]
  echo paths = ["/","/api","/status","/health","/v1","/sim","/metrics"]
  echo def try_url(url):
  echo ^    try:
  echo ^        req = urllib.request.Request(url, headers={"User-Agent":"A380-AI-BridgeProbe"})
  echo ^        with urllib.request.urlopen(req, timeout=2) as r:
  echo ^            return r.status
  echo ^    except Exception:
  echo ^        return None
  echo print("---- Python Probe ----", flush=True)
  echo for p in ports:
  echo ^    base = f"http://127.0.0.1:{p}"
  echo ^    for path in paths:
  echo ^        url = base + path
  echo ^        code = try_url(url)
  echo ^        if code is not None:
  echo ^            print(f"Port {p}  HTTP {code}  {url}", flush=True)
  echo print("---- Ende ----", flush=True)
) > "%PY%"
python -u "%PY%"
exit /b 0
