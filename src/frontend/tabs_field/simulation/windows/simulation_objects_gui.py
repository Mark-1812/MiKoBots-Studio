from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QOpenGLWidget, QCheckBox, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QDoubleValidator, QIcon


import pyvista as pv
import pyvistaqt as pvt

from backend.core.event_manager import event_manager

from backend.core.api import open_object_models
from backend.core.api import show_origin_object
from backend.core.api import change_origin_object
from backend.core.api import delete_stl_object_1
from backend.core.api import add_new_object_model
from backend.core.api import add_object_to_plotter
from backend.core.api import show_pos_object
from backend.core.api import change_pos_object
from backend.core.api import delete_object_plotter
from backend.core.api import change_color_object


class SimulationObjectsGUI(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
    
        self.setWindowTitle("Add item")
        self.setWindowIcon(QIcon('mikobot.ico'))
        self.setFixedSize(1000, 700)

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.setStyleSheet(
            "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
            "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
            "QPushButton:hover { background-color: white; }"
            "QPushButton:pressed { background-color: darkorange; }"+
            "QCheckBox {  background-color: white; }"+
            "QLabel {font-size: 12px; font-family: Arial;}"+
            "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
            )

        self.stl_object_origin = [0] * 2
        
        self.Buttons2 = []
        self.Buttons1 = []
        
        self.origin_pos = []
        self.pos_entry = []
        
        
        self.subscribeToEvents()
        self.GUI()
        
        open_object_models()
          
    def subscribeToEvents(self):
        event_manager.subscribe("request_create_buttons_1_object", self.CreateButtons1)
        event_manager.subscribe("request_delete_buttons_1_object", self.DeleteButtons1)
        
        event_manager.subscribe("request_create_buttons_2_object", self.CreateButtons2)
        event_manager.subscribe("request_delete_buttons_2_object", self.DeleteButtons2)
        
        event_manager.subscribe("request_set_data_origin_object", self.SetDataOriginObject)
        event_manager.subscribe("request_get_data_origin_object", self.GetDataOriginObject)

        event_manager.subscribe("request_set_data_pos_object", self.SetDataPosObject)
        event_manager.subscribe("request_get_data_pos_object", self.GetDataPosObject)

        event_manager.subscribe("request_object_plotter_preview", self.AddModelToPlotter)
        event_manager.subscribe("request_clear_plotter_object", self.ClearPlotter)

    def CreatePlanes(self, plotter, size):
        origin = [0,0,0]
        normal_xy = [0,0,1]
        normal_xz = [0,1,0]
        normal_zy = [1,0,0]
        
        plane_xy = pv.Plane(center=origin, direction=normal_xy, i_size=size, j_size=size)
        plotter.add_mesh(plane_xy, opacity=0.5, color="blue") 
        
        plane_xz = pv.Plane(center=origin, direction=normal_xz, i_size=size, j_size=size)
        plotter.add_mesh(plane_xz, opacity=0.5, color="blue") 
        
        plane_zy = pv.Plane(center=origin, direction=normal_zy, i_size=size, j_size=size)
        plotter.add_mesh(plane_zy, opacity=0.5, color="blue") 
        
           
        self.plotter2.show()
    
    def ClearPlotter(self):
        if self.stl_object_origin[1] != 0:
            self.plotter2.remove_actor(self.stl_object_origin[1])

    def AddModelToPlotter(self, file_path):
        print(file_path)
        self.stl_object_origin[0] = pv.read(file_path)
        self.stl_object_origin[1] = self.plotter2.add_mesh(self.stl_object_origin[0], color="red", show_edges=False)   
        
    # set and get the origin data   
    def SetDataOriginObject(self, origin):
        for i in range(6):
            self.origin_pos[i].setText(str(origin[i]))
            
    def GetDataOriginObject(self):
        data = [0,0,0,0,0,0]
        for i in range(6):
            data[i] = float(self.origin_pos[i].text())
            
        return data

    # Set and get the position of the object
    def SetDataPosObject(self, pos):
        for i in range(6):
            self.pos_entry[i].setText(str(pos[i]))
   
    def GetDataPosObject(self):
        data = [0,0,0,0,0,0]
        for i in range(6):
            try:
                data[i] = float(self.pos_entry[i].text())
            except:
                data[i] = 0.0
            
        return data


    # Create the buttons for all the stl files that are saved in the mikobots studio
    def CreateButtons1(self, item, name):
        self.Buttons1.append([[],[],[],[]])
        
        label = QLabel(name)
        label.setMinimumWidth(60)
        self.scroll_area1.addWidget(label, item , 0)
        self.Buttons1[item][0] = label

        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_stl_object_1(idx))
        self.scroll_area1.addWidget(button, item, 1)
        self.Buttons1[item][1] = button
 
        button = QPushButton("+")
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: add_object_to_plotter(idx))
        self.scroll_area1.addWidget(button, item, 2)
        self.Buttons1[item][2] = button
        
        button = QPushButton("Origin")
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_origin_object(idx))
        self.scroll_area1.addWidget(button, item, 3)
        self.Buttons1[item][3] = button
        
        spacer_widget = QWidget()
        self.scroll_area1.addWidget(spacer_widget, self.scroll_area1.rowCount(), 0, 1, self.scroll_area1.columnCount())

    def DeleteButtons1(self):
        for i in range(len(self.Buttons1)):
            for j in range(4):
                self.Buttons1[i][j].setParent(None)
                self.Buttons1[i][j].deleteLater()
        
        self.Buttons1 = []        


    # create the buttons for the objects that are shown in the plotter
    def CreateButtons2(self, item, name):
        self.Buttons2.append([[],[],[],[],[],[]])
            
        label = QLabel(name)
        label.setMinimumWidth(60)
        self.scroll_area2.addWidget(label, item , 0)
        self.Buttons2[item][0] = label
        
        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_object_plotter(idx))
        self.scroll_area2.addWidget(button, item, 1)
        self.Buttons2[item][1] = button
               
        button = QPushButton("Position")
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_pos_object(idx))
        self.scroll_area2.addWidget(button, item, 2)
        self.Buttons2[item][2] = button
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        # for i in range(len(colors)):
        #     if colors[i] == self.Objects_stl2[item][2]:
        #         combo_nr = i
        
        self.combo = QComboBox()
        self.combo.addItems(colors)
        self.combo.setCurrentIndex(combo_nr)
        self.combo.currentIndexChanged.connect(lambda index, idx = item: self.ChangeColorCombo(idx))
        self.scroll_area2.addWidget(self.combo, item, 3)
        self.Buttons2[item][3] = self.combo
            
        spacer_widget = QWidget()
        self.scroll_area2.addWidget(spacer_widget, self.scroll_area2.rowCount(), 0, 1, self.scroll_area2.columnCount())

    def DeleteButtons2(self):
        # Delete all the buttons
        for i in range(len(self.Buttons2)):
            for j in range(4):
                self.Buttons2[i][j].setParent(None)
                self.Buttons2[i][j].deleteLater()
                
        self.Buttons2 = []

    def ChangeColorCombo(self, nr):
        if self.combo.currentText() == "red":
            color = [1,0,0]
        elif self.combo.currentText() == "blue":
            color = [0,0,1]
        elif self.combo.currentText() == "black":
            color = [0,0,0]
        elif self.combo.currentText() == "white":
            color = [1,1,1]
        elif self.combo.currentText() == "darkgray":
            color = [0.5,0.5,0.5]
            
        change_color_object(self.combo.currentText(), color, nr)
        


    # Create the plotter and load the list
    def openevent(self):
        self.plotter2 = pvt.QtInteractor()
        self.plotter2.setFixedHeight(300)
        self.plotter2.setFixedWidth(300)
        self.plotter2.add_axes()
          
        self.layout_plotter.addWidget(self.plotter2,0,0)   
        self.CreatePlanes(self.plotter2, 300)   
        
    def closeEvent(self, event):
        self.plotter2.close()
                  
    def GUI(self):
        column = 0
        
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        title = QLabel("Items")
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title, 0, column)
        
        # scroll area, where the files will be shown
        scroll_area2 = QScrollArea(self)
        scroll_area2.setWidgetResizable(True)
        self.scroll_area2 = QGridLayout(scroll_area2)
        
        self.layout.addWidget(scroll_area2, 1, column)

        frame_items = QFrame()
        scroll_area2.setWidget(frame_items)

        def ChangePosition():
            ## GUI for chancing the position of the objects
            layout_pos = QGridLayout()
            frame_pos = QFrame()
            self.layout.addWidget(frame_pos, 2, column)
            frame_pos.setLayout(layout_pos)
            
            title = QLabel("Change position:")
            title.setFixedHeight(30)
            title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            layout_pos.addWidget(title, 0, 0, 1, 2)
            
            
            labels = ["X:", "Y:", "Z:", "y", "p", "r"]
            for idx, label_text in enumerate(labels):
                label = QLabel(label_text)
                label.setFixedWidth(20)  # Set the width as needed

                entry = QLineEdit()
                entry.setFixedWidth(50)  # Set the width as needed
                entry.setValidator(validator)
                self.pos_entry.append(entry)

                row = idx + 1
                col = 0

                layout_pos.addWidget(label, row, col)
                layout_pos.addWidget(entry, row, col + 1)  # Put entry in the next column
                
            button_update_pos = QPushButton("Update")
            button_update_pos.clicked.connect(lambda: change_pos_object())
            layout_pos.addWidget(button_update_pos,7, 0, 1, 2)
        
        ChangePosition()

        ## make a frame where all the 3d files will be placed in
        column = 1
        title = QLabel("3D files:")
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title,0,column)
        
        scroll_area1 = QScrollArea(self)
        scroll_area1.setWidgetResizable(True)
        self.scroll_area1 = QGridLayout(scroll_area1)
        
        self.layout.addWidget(scroll_area1,1,column,2,1)
        
        frame_stl_items = QFrame()
        self.layout_stl_items = QGridLayout(frame_stl_items)
        scroll_area1.setWidget(frame_stl_items)
        
        spacer_widget = QWidget()
        self.layout_stl_items.addWidget(spacer_widget, self.layout_stl_items.rowCount(), 0, 1, self.layout_stl_items.columnCount())
         
        ## frame with the plotter
        column = 2
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        self.layout.addWidget(frame_plotter,0,column,2,1)
        frame_plotter.setLayout(self.layout_plotter)  
                 
        def changeOrigin():
            ## frame with the options
            layout_options = QGridLayout()
            frame_options = QFrame()
            self.layout.addWidget(frame_options,2,column)
            frame_options.setLayout(layout_options)
            
            title = QLabel("Change origin:")
            title.setFixedHeight(30)
            title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            layout_options.addWidget(title,0,0,1,2)
            
            labels = ["X:", "Y:", "Z:", "y", "p", "r"]
            for idx, label_text in enumerate(labels):
                label = QLabel(label_text)
                label.setFixedWidth(20)  # Set the width as needed

                entry = QLineEdit()
                entry.setFixedWidth(50)  # Set the width as needed
                entry.setValidator(validator)
                self.origin_pos.append(entry)

                row = idx + 1 
                col = 0

                layout_options.addWidget(label, row, col)
                layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
                
            button = QPushButton("Update")
            layout_options.addWidget(button,7, 0, 1, 2)
            button.clicked.connect(lambda: change_origin_object())
        
            
            button = QPushButton("Add new 3D model")
            layout_options.addWidget(button, 8, 0, 1, 2)
            button.clicked.connect(lambda: add_new_object_model())

        changeOrigin()


        
