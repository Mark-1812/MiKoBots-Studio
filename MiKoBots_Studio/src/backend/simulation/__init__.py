from backend.simulation.simulation_management import SimulationManagement

simulation_management = SimulationManagement()





####################
#   Simulation management
####################

def enable_simulation(state):
    simulation_management.EnableSimulation(state)

def simulation_move_gui(pos, move):
    simulation_management.SimulationMoveGUI(pos, move)
    
def simulate_program(command):
    simulation_management.SimulateProgram(command)
    
def simulation_not_busy():
    simulation_management.SetNotBusy()
    
    



    
