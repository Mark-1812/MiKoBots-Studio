from PyQt5.QtCore import QObject



from backend.core.event_manager import event_manager

class SimulationOriginWindow(QObject):
    def __init__(self):
        self.ORIGIN = []
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_open_doc_origins", self.OpenFile)
        event_manager.subscribe("request_close_doc_origins", self.CloseFile)
        event_manager.subscribe("request_get_origins_plotter", self.GetOriginsPlotter)
             
    def AddOrigin(self):
        item = len(self.ORIGIN)
        self.ORIGIN.append([[],[],[],[]])
        
        self.ORIGIN[item][0] = "New orign " + str(item)
        self.ORIGIN[item][1] = 0.0
        self.ORIGIN[item][2] = 0.0
        self.ORIGIN[item][3] = 0.0
        
        event_manager.publish("request_delete_space_origin")
        event_manager.publish("request_create_button_origin", item, self.ORIGIN[item])
        self.CreateAxes(item)
  
    def CreateAxes(self, item):
        event_manager.publish("request_add_axis_to_plotter", item)   
                     
    def SaveOrigin(self, item):      
        data = event_manager.publish("request_get_data_origin", item)

        self.ORIGIN[item] = data[0]

        #self.UpdateAxes(item, self.ORIGIN[item])
        event_manager.publish("request_change_pos_axis", item, self.ORIGIN[item])
        
        origins_new = []
        for i in range(len(self.ORIGIN)):
            if self.ORIGIN[i][0] is not None:
                origins_new.append(self.ORIGIN[i])
        
        self.ORIGIN = origins_new
        print(self.ORIGIN)
   
    def DeleteOrigin(self, item):
        # delete out of plotter
        event_manager.publish("request_delete_axis_plotter") 

        # delete the buttons
        event_manager.publish("request_delete_buttons_origin")  
        
        # Make a new list
        self.ORIGIN[item] = []
        origin_old = self.ORIGIN
        self.ORIGIN = []
        
        for i in range(len(origin_old)):
            if origin_old[i] != []:
                self.ORIGIN.append(origin_old[i])
                
        # Create new axis
        # Create new buttons
        for i in range(len(self.ORIGIN)):
            event_manager.publish("request_delete_space_origin")
            event_manager.publish("request_create_button_origin", i, self.ORIGIN[i])
            self.CreateAxes(i)   

    def OpenFile(self, origins):
        self.ORIGIN = origins
        
        for i in range(len(self.ORIGIN)):
            event_manager.publish("request_delete_space_origin")
            event_manager.publish("request_create_button_origin", i, self.ORIGIN[i])
            self.CreateAxes(i) 
               
    def CloseFile(self):
        # delete the buttons
        event_manager.publish("request_delete_buttons_origin") 

        # delete out of plotter
        event_manager.publish("request_delete_axis_plotter")
                
        self.ORIGIN = []
        
    def GetOriginsPlotter(self):
        return self.ORIGIN