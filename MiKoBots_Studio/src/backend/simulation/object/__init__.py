from backend.file_managment.file_management import FileManagement
from .simulation_object_window import SimulationObjectWindow


sim_object_window = SimulationObjectWindow()





####################
#   Simulation object
####################
def setup_renderer_object(renderer, plotter, interactor):
    sim_object_window.SetupRenderer(renderer, plotter, interactor)

def add_new_object_model():
    sim_object_window.AddNewObjectModel()
    
def add_object_to_plotter(item):
    sim_object_window.AddObjectToPlotter(item)
    
def delete_object_plotter(item):
    sim_object_window.DeleteObjectPlotter(item)

def open_object_models():
    sim_object_window.OpenObjectModels()
    
def show_pos_object(item):
    sim_object_window.ShowPosObject(item)
    
def change_pos_object():
    sim_object_window.ChangePosObject()
    
def show_origin_object(item):
    sim_object_window.ShowOriginObject(item)
    
def change_origin_object():
    sim_object_window.ChangeOriginObject()
    
def delete_stl_object_1(item):
    sim_object_window.DeleteSTLObject1(item)
    
def change_color_object(color, color_code, item):
    sim_object_window.ChangeColorObject(color, color_code ,item)


def open_object_file(objects):
    sim_object_window.OpenFile(objects)

def close_object_file():
    sim_object_window.CloseFile()

def get_objects_sim():
    objects = sim_object_window.GetObjectsPlotter()
    return objects