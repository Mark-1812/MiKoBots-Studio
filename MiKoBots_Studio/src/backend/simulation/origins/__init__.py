from .simulation_origin_window import SimulationOriginWindow

simulation_origin_window = SimulationOriginWindow()


####################
#   Simulation origin
####################
def setup_renderer_origin(renderer, plotter, interactor):
    simulation_origin_window.SetupRenderer(renderer, plotter, interactor)

def add_origin():
    simulation_origin_window.AddOrigin()
    
def save_origin(item):
    simulation_origin_window.SaveOrigin(item)

def delete_origin(item):
    simulation_origin_window.DeleteOrigin(item)

def open_origins_file(origins):
    simulation_origin_window.OpenFile(origins)

def close_origins_file():
    simulation_origin_window.CloseFile()

def get_origins_file():
    origins = simulation_origin_window.GetOriginsPlotter()
    return origins
    
