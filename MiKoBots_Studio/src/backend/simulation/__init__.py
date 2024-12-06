from backend.simulation.simulation_management import SimulationManagement

simulation_management = SimulationManagement()





####################
#   Simulation management
####################

def enable_simulation(state):
    simulation_management.EnableSimulation(state)

def check_simulation_on():
    return simulation_management.simulation_on
    
def simulate_program(command):
    simulation_management.SimulateProgram(command)
    
def simulation_not_busy():
    simulation_management.simulation_busy = False
    