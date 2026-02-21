import os
import sys
import time
from pathlib import Path
from datetime import datetime

def write_log(line: str, log_path: Path):
    print(line)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")

def is_admin() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def main():
    base = Path(__file__).resolve().parent  # app_tmp
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = base / "logs" / f"diag_{ts}.log"

    write_log("="*60, log_path)
    write_log("[DIAG] START", log_path)
    write_log(f"[DIAG] CWD={os.getcwd()}", log_path)
    write_log(f"[DIAG] FILE_DIR={base}", log_path)
    write_log(f"[DIAG] PY_EXE={sys.executable}", log_path)
    write_log(f"[DIAG] PY_VER={sys.version.replace(os.linesep,' ')}", log_path)
    write_log(f"[DIAG] ADMIN={is_admin()}", log_path)

    # --- SimConnect check ---
    try:
        from simconnect_client import SimClient
        sim = SimClient()
        sim.connect()
        write_log("[SIM] connect OK", log_path)

        tests = [
            "PLANE LATITUDE",
            "PLANE LONGITUDE",
            "SIMULATION TIME",
            "ZULU TIME",
            "SIM IS PAUSED",
            "PLANE ALTITUDE",
            "AIRSPEED INDICATED",
            "SIM ON GROUND",
        ]
        for t in tests:
            v = sim.read(t, "NA")
            write_log(f"[SIMVAR] {t} = {v}", log_path)

    except Exception as e:
        write_log(f"[SIM] ERROR: {type(e).__name__}: {e}", log_path)

    # --- WASimCommander check (optional) ---
    try:
        from wasimcommander import WASimCommander
        w = WASimCommander()
        w.connect()
        write_log("[WASIM] connect OK", log_path)
        for _ in range(3):
            lat = w.get("PLANE LATITUDE")
            lon = w.get("PLANE LONGITUDE")
            alt = w.get("PLANE ALTITUDE")
            write_log(f"[WASIM] LAT={lat} LON={lon} ALT={alt}", log_path)
            time.sleep(1)
    except Exception as e:
        write_log(f"[WASIM] SKIP/ERROR: {type(e).__name__}: {e}", log_path)

    write_log(f"[DIAG] DONE -> {log_path}", log_path)
    write_log("="*60, log_path)

if __name__ == "__main__":
    main()
