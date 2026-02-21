class AircraftReady:
    def __init__(self, sim):
        self.sim = sim

    def is_ready(self):
        bus = self.sim.get("ELECTRICAL MAIN BUS VOLTAGE")
        return bus is not None
