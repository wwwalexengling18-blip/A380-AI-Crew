import os
import time
from datetime import datetime

class Logger:
    def __init__(self, log_dir=None, prefix="A380_AI"):
        self.log_dir = log_dir
        self.prefix = prefix
        self._file = None

        if self.log_dir:
            os.makedirs(self.log_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            path = os.path.join(self.log_dir, f"{self.prefix}_{ts}.log")
            self._file = open(path, "a", encoding="utf-8")

        self.info("Logger init")

    def _write(self, level, msg):
        line = f"[{level}] {time.strftime('%H:%M:%S')} {msg}"
        print(line)
        if self._file:
            self._file.write(line + "\n")
            self._file.flush()

    def info(self, msg): self._write("INFO", msg)
    def warn(self, msg): self._write("WARN", msg)
    def error(self, msg): self._write("ERROR", msg)

    def close(self):
        if self._file:
            self.info("Logger close")
            self._file.close()
            self._file = None
