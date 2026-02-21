sim_time = self.sim.read("SIMULATION TIME", -1)
zulu = self.sim.read("ZULU TIME", -1)
paused = self.sim.read("SIM IS PAUSED", -1)
print(f"[TEST] SIM_TIME={sim_time} ZULU={zulu} PAUSED={paused}")
