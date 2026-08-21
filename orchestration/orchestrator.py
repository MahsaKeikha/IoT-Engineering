from AGENTS import device_agent,connectivity_agent,data_agent,security_agent,operations_agent
def run(ctx): return [a.run(ctx) for a in [device_agent,connectivity_agent,data_agent,security_agent,operations_agent]]
