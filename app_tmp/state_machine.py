class StateMachine:
    def __init__(self):
        self.state = "COLD_DARK"

    def update(self, sim):

        if self.state == "COLD_DARK":
            if sim.get("ELECTRICAL MAIN BUS VOLTAGE") > 20:
                self.state = "POWERED"

        elif self.state == "POWERED":
            if sim.get("GENERAL ENG COMBUSTION:1"):
                self.state = "ENGINE_START"

        return self.state
