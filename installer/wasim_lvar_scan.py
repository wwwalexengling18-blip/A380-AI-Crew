import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGDIR = ROOT / "logs"
LOGDIR.mkdir(exist_ok=True)

LOG = LOGDIR / f"wasim_lvar_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

def log(msg):
    print(msg)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("=== WASim LVar Scan ===")

try:
    from SimConnect import SimConnect
except Exception as e:
    log(f"SimConnect fehlt: {e}")
    raise

sm = SimConnect()
log("SimConnect OK")

# Beispiel LVars zum Testen (A380)
lvars = [
    "L:A380X_ELEC_EXT_PWR_ON",
    "L:A380X_APU_MASTER_SW",
    "L:A380X_APU_START_PB",
    "L:A380X_ENGINE_1_MASTER",
]

log(f"LVars: {len(lvars)}")

for l in lvars:
    code = f"{l}"
    try:
        # Calculator Code über Sim (WASM)
        val = sm.execute_calculator_code(code)
    except Exception as e:
        val = None

    log(f"{l} = {val}")
    time.sleep(0.2)

log(f"LOG: {LOG}")
