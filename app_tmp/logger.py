from __future__ import annotations

import os
import sys
import time
import platform
from datetime import datetime
from pathlib import Path

_LOG_FILE = None

def _is_admin() -> bool:
    try:
        import ctypes  # type: ignore
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def init_logger(app_name: str = "A380_AI") -> Path:
    """
    Erstellt logs/ und öffnet eine Logdatei.
    """
    global _LOG_FILE

    base_dir = Path(__file__).resolve().parent  # app_tmp
    log_dir = base_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_path = log_dir / f"{app_name}_{ts}.log"

    _LOG_FILE = open(log_path, "a", encoding="utf-8")

    log("=" * 60)
    log(f"{app_name} Logger gestartet")
    log(f"Zeit: {datetime.now().isoformat(timespec='seconds')}")
    log(f"Python: {sys.version.replace(os.linesep, ' ')}")
    log(f"Executable: {sys.executable}")
    log(f"Platform: {platform.platform()}")
    log(f"CWD: {os.getcwd()}")
    log(f"Script Dir: {base_dir}")
    log(f"Admin: {_is_admin()}")
    log("=" * 60)

    return log_path

def log(msg: str) -> None:
    global _LOG_FILE
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line)
    if _LOG_FILE:
        try:
            _LOG_FILE.write(line + "\n")
            _LOG_FILE.flush()
        except Exception:
            pass

def log_exception(prefix: str, e: Exception) -> None:
    log(f"{prefix}: {type(e).__name__}: {e}")

def log_module_version(module_name: str) -> None:
    try:
        mod = __import__(module_name)
        ver = getattr(mod, "__version__", "unknown")
        log(f"Modul {module_name} import OK, version={ver}")
    except Exception as e:
        log_exception(f"Modul {module_name} import FAIL", e)
