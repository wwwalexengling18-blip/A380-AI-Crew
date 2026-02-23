from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any, Dict, List

from .models import SOPPhase, SOPStep
from .sim_backend import SimBackendBase
from .state_machine import GateToGateStateMachine


class A380AICrewController:
    def __init__(
        self,
        backend: SimBackendBase,
        phases: List[SOPPhase],
        logger: logging.Logger,
        read_hz: int = 10,
        startup_delay_sec: int = 15,
        auto_complete_manual: bool = True,
    ) -> None:
        self.backend = backend
        self.log = logger
        self.read_hz = max(1, int(read_hz))
        self.startup_delay_sec = max(0, int(startup_delay_sec))
        self.sm = GateToGateStateMachine(phases=phases, logger=logger, auto_complete_manual=auto_complete_manual)
        self._started = time.time()
        self._last_action_step_id = None

    def _aircraft_ready(self, snapshot: Dict[str, Any]) -> bool:
        if (time.time() - self._started) < self.startup_delay_sec:
            return False
        return bool(snapshot.get("sim_connected")) and bool(snapshot.get("aircraft_loaded"))

    def _dispatch_step_action(self, step: SOPStep) -> None:
        if self._last_action_step_id == step.id:
            return
        action = step.action
        self.backend.execute_action(action.kind, action.name, action.value, unit=action.unit, **(action.args or {}))
        self._last_action_step_id = step.id

    def run(self, max_seconds: int = 0) -> int:
        if not self.backend.connect():
            self.log.error("Backend-Verbindung fehlgeschlagen.")
            return 2

        self.log.info("Controller gestartet (read_hz=%s, startup_delay=%ss)", self.read_hz, self.startup_delay_sec)
        dt = 1.0 / float(self.read_hz)
        end_at = (time.time() + max_seconds) if max_seconds and max_seconds > 0 else None

        try:
            while True:
                snap = self.backend.read_snapshot()

                if not self._aircraft_ready(snap):
                    remain = max(0, self.startup_delay_sec - int(time.time() - self._started))
                    self.log.info("Warte auf Aircraft Ready... (Delay/Init) %ss", remain)
                    time.sleep(dt)
                    continue

                phase, step = self.sm.current()
                if self.sm.finished:
                    self.log.info("Gate-to-Gate Ablauf beendet.")
                    return 0

                if step is not None:
                    self._dispatch_step_action(step)

                self.sm.tick(snap)

                if end_at and time.time() >= end_at:
                    self.log.info("Zeitlimit erreicht -> sauberer Stop.")
                    return 0

                time.sleep(dt)
        except KeyboardInterrupt:
            self.log.warning("Manuell abgebrochen.")
            return 130
        finally:
            self.backend.close()
