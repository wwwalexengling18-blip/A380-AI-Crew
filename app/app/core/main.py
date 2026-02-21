import os
import time
import yaml
from datetime import datetime

from core.simconnect_client import SimClient
from core.aircraft_ready import wait_for_ready
from core.ecam_monitor import EcamMonitor
from core.gsx_adapter import GsxAdapter
from core.state_machine import StateMachine
from core.input_controller import InputController


def make_logger():
    base = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(base, "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"a380_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")

    def log(msg: str):
        print(msg, flush=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(msg + "\n")

    log(f"[BOOT] Logfile: {log_file}")
    return log


def load_yaml(path: str) -> dict:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def main():
    log = make_logger()
    root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")

    settings = load_yaml(os.path.join(root, "config", "settings.yaml"))
    sop = load_yaml(os.path.join(root, "config", "sop_gate_to_gate.yaml"))

    sim = SimClient(log, read_hz=float(settings.get("read_hz", 10)))
    sim.connect()

    ready_ok = wait_for_ready(sim.snapshot, log, timeout_s=int(settings.get("ready_timeout_s", 180)))
    if not ready_ok:
        log("[BOOT] Aircraft nicht ready → Abbruch")
        return

    ecam = EcamMonitor(log)
    gsx = GsxAdapter(log, enabled=bool(settings.get("gsx_enabled", False)))
    ctrl = InputController(log, mode=str(settings.get("control_mode", "OFF")))

    sm = StateMachine(log, sop, ecam, gsx, settings)
    sm.run(sim)

    log("[END] Done")
    time.sleep(0.5)


if __name__ == "__main__":
    main()
