import time

class StateMachine:
    def __init__(self, logger):
        self.log = logger
        self.state = "BOOT"
        self.state_since = time.time()

    def set_state(self, new_state):
        self.log.info(f"[SM] {self.state} -> {new_state}")
        self.state = new_state
        self.state_since = time.time()

    def tick(self, ctx):
        """
        ctx enthält z.B.
        ctx["sim"], ctx["cold_dark"], ctx["fbw_ready"], ctx["on_ground"], ...
        """
        if self.state == "BOOT":
            self.set_state("COLD_DARK_MONITOR")

        elif self.state == "COLD_DARK_MONITOR":
            # Cold & Dark lesen ist erlaubt. Wir warten, bis wir "ready to act" sind.
            if ctx.get("fbw_ready"):
                self.set_state("PREP")
            else:
                # weiter beobachten, aber noch nicht aggressiv steuern
                pass

        elif self.state == "PREP":
            # hier später: echte SOP-Checklisten, Batterie, ext power, IRS, etc.
            # erstmal nur placeholder
            if time.time() - self.state_since > 2:
                self.set_state("IDLE")

        elif self.state == "IDLE":
            # später: Gate-to-Gate Flow
            pass
