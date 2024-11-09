from backend.simulation.simulation_management import SimulationManagement
from backend.simulation.simulation_origin_window import SimulationOriginWindow
from backend.simulation.simulation_object_window import SimulationObjectWindow

simulation_management = SimulationManagement()
simulation_origin_window = SimulationOriginWindow()
simulation_object_window = SimulationObjectWindow()


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
    
    

####################
#   Simulation object
####################
def add_new_object_model():
    simulation_object_window.AddNewObjectModel()
    
def add_object_to_plotter(item):
    simulation_object_window.AddObjectToPlotter(item)
    
def delete_object_plotter(item):
    simulation_object_window.DeleteObjectPlotter(item)

def open_object_models():
    simulation_object_window.OpenObjectModels()
    
def show_pos_object(item):
    simulation_object_window.ShowPosObject(item)
    
def change_pos_object():
    simulation_object_window.ChangePosObject()
    
def show_origin_object(item):
    simulation_object_window.ShowOriginObject(item)
    
def change_origin_object():
    simulation_object_window.ChangeOriginObject()
    
def delete_stl_object_1(item):
    simulation_object_window.DeleteSTLObject1(item)
    
def change_color_object(color, color_code, item):
    simulation_object_window.ChangeColorObject(color, color_code, item)

    

####################
#   Simulation origin
####################
    
def add_origin():
    simulation_origin_window.AddOrigin()
    
def save_origin(item):
    simulation_origin_window.SaveOrigin(item)

def delete_origin(item):
    simulation_origin_window.DeleteOrigin(item)
