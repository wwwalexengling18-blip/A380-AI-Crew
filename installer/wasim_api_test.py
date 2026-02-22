import os
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
LIBDIR = Path(__file__).resolve().parent / "wasim" / "lib"
LOGDIR = ROOT / "logs"
LOGDIR.mkdir(exist_ok=True)

LOG = LOGDIR / f"wasim_api_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg: str):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def fail(msg: str, code: int = 1):
    log("FATAL: " + msg)
    log(f"LOG: {LOG.resolve()}")
    raise SystemExit(code)

dll = LIBDIR / "WASimCommander.WASimClient.dll"
ijw = LIBDIR / "Ijwhost.dll"
ini = LIBDIR / "client_conf.ini"

log("=== WASimCommander API Test ===")
log(f"LIBDIR: {LIBDIR}")
log(f"LOG:    {LOG.resolve()}")

if not dll.exists():
    fail("WASimCommander.WASimClient.dll fehlt. Kopiere sie nach installer\\wasim\\lib\\")
if not ijw.exists():
    fail("Ijwhost.dll fehlt. Kopiere sie nach installer\\wasim\\lib\\ (sonst DLL-Load kann scheitern).")

# pythonnet laden
try:
    import clr  # pythonnet
except Exception as e:
    fail(f"pythonnet fehlt: {e}\nInstalliere es im venv: pip install pythonnet")

# Damit die DLLs gefunden werden:
os.add_dll_directory(str(LIBDIR))
sys.path.insert(0, str(LIBDIR))

try:
    clr.AddReference(str(dll))
except Exception as e:
    fail(f"Konnte WASimClient DLL nicht laden: {e}")

try:
    # Namespace laut Doku: WASimCommander::Client::WASimClient
    from WASimCommander.Client import WASimClient
except Exception as e:
    fail(f"Namespace/Class nicht gefunden (Assembly geladen, aber API anders?): {e}")

# ClientId frei wählbar (muss nur eindeutig pro Client sein)
client_id = 0xA3802024
config_path = str(ini) if ini.exists() else ""

log(f"ClientId: {hex(client_id)}")
log(f"Config:   {config_path if config_path else '(none)'}")

try:
    c = WASimClient(client_id, config_path)
except Exception as e:
    fail(f"WASimClient() Konstruktor fehlgeschlagen: {e}")

# 1) SimConnect Link initialisieren
log("\n[1/4] connectSimulator() ...")
hr = c.connectSimulator(3000)  # timeout ms
log(f"HR: {hr} | isInitialized={c.isInitialized()} status={c.status()}")

# 2) Server ping
log("\n[2/4] pingServer() ...")
ver = c.pingServer(2000)
log(f"ServerVersion(BCD): {ver} | isConnected={c.isConnected()}")

if ver == 0:
    fail("Ping = 0. WASimModule nicht erreichbar. Prüfe: wasimcommander-module im Community-Ordner + MSFS neu starten.")

# 3) connectServer
log("\n[3/4] connectServer() ...")
hr = c.connectServer(3000)
log(f"HR: {hr} | isConnected={c.isConnected()} serverVersion={c.serverVersion()}")

if not c.isConnected():
    fail("connectServer() hat keine Verbindung hergestellt (isConnected=false).")

# 4) LVars listen + filtern + lesen
log("\n[4/4] List Local Variables + Filter 'A380X_' ...")
# Doku: "List Local Variables" Feature vorhanden; UI macht das auch.
# In der API gibt es Lookup/List-Funktionen – wenn bei dir eine Methode anders heißt,
# sehen wir das sofort im Log und passen an.

# Versuch: viele Builds haben eine Methode, die LVars listet. Falls dein Build anders heißt,
# kommt eine Exception -> dann sag ich dir die 2 Alternativen.
try:
    # Häufiger Name in den Libs: listLocalVariables()
    lvars = c.listLocalVariables()
    # listLocalVariables() gibt typischerweise eine Liste/Vector mit Records oder Strings
    # Wir behandeln beides robust:
    names = []
    for item in lvars:
        s = str(item)
        names.append(s)
except Exception as e:
    fail(f"Konnte LVar-Liste nicht abrufen (listLocalVariables): {e}")

filtered = [n for n in names if "A380X_" in n]
log(f"Total LVars: {len(names)}")
log(f"Filtered A380X_: {len(filtered)}")
log("Top 30 A380X_ Treffer:")
for n in filtered[:30]:
    log("  " + n)

# Optional: 3 konkrete Reads via getLocalVariable()
# (Achtung: getLocalVariable erwartet den Namen ohne 'L:' in vielen APIs)
test_names = []
for raw in filtered[:3]:
    # raw kann "A380X_SOMETHING" oder "A380X_SOMETHING (id=123)" sein -> nur Name rausziehen
    name = raw.split()[0]
    test_names.append(name)

log("\nRead 3 LVars (getLocalVariable):")
for name in test_names:
    try:
        # double* wird in pythonnet als byref gehandhabt: wir nutzen ein Python float container pattern
        # Viele pythonnet-Bindings akzeptieren "None" und geben tuple zurück; wenn nicht, Exception -> Log.
        val = c.getLocalVariable(name)
        log(f"  {name} = {val}")
    except Exception as e:
        log(f"  {name} = (ERROR) {e}")

log("\nOK: WASimCommander API Test abgeschlossen.")
log(f"LOG: {LOG.resolve()}")
