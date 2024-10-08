from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QOpenGLWidget, QCheckBox, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QDoubleValidator, QIcon

from gui.style import *

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
        
        self.setStyleSheet("background-color: #E8E8E8;")

        self.stl_object_origin = [0] * 2
        
        self.Buttons2 = []
        self.Buttons1 = []
        
        self.origin_pos = []
        self.pos_entry = []
        
        self.spacer_widget_2 = None
        
        
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
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        self.scroll_area1.addWidget(label, item , 0)
        self.Buttons1[item][0] = label

        button = QPushButton("X")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_stl_object_1(idx))
        self.scroll_area1.addWidget(button, item, 1)
        self.Buttons1[item][1] = button
 
        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: add_object_to_plotter(idx))
        self.scroll_area1.addWidget(button, item, 2)
        self.Buttons1[item][2] = button
        
        button = QPushButton("Origin")
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_origin_object(idx))
        self.scroll_area1.addWidget(button, item, 3)
        self.Buttons1[item][3] = button
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        self.scroll_area1.addWidget(spacer_widget, self.scroll_area1.rowCount(), 0, 1, self.scroll_area1.columnCount())

    def DeleteButtons1(self):
        for i in range(len(self.Buttons1)):
            for j in range(4):
                self.Buttons1[i][j].setParent(None)
                self.Buttons1[i][j].deleteLater()
        
        self.Buttons1 = []        


    # create the buttons for the objects that are shown in the plotter
    def CreateButtons2(self, item, name):
        if self.spacer_widget_2:
            self.spacer_widget_2.setParent(None)
            self.spacer_widget_2.deleteLater()
        
        self.Buttons2.append([[],[],[],[],[],[]])
            
        label = QLabel(name)
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        self.scroll_area2.addWidget(label, item , 0)
        self.Buttons2[item][0] = label
        
        button = QPushButton("X")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_object_plotter(idx))
        self.scroll_area2.addWidget(button, item, 1)
        self.Buttons2[item][1] = button
               
        button = QPushButton("Position")
        button.setStyleSheet(style_button)
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_pos_object(idx))
        self.scroll_area2.addWidget(button, item, 2)
        self.Buttons2[item][2] = button
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        
        self.combo = QComboBox()
        self.combo.setStyleSheet(style_combo)
        self.combo.addItems(colors)
        self.combo.setCurrentIndex(combo_nr)
        self.combo.currentIndexChanged.connect(lambda index, idx = item: self.ChangeColorCombo(idx))
        self.scroll_area2.addWidget(self.combo, item, 3)
        self.Buttons2[item][3] = self.combo
            
        self.spacer_widget_2 = QWidget()
        self.spacer_widget_2.setStyleSheet(style_widget)
        self.scroll_area2.addWidget(self.spacer_widget_2, self.scroll_area2.rowCount(), 0, 1, self.scroll_area2.columnCount())

    def DeleteButtons2(self):
        # Delete all the buttons
        for i in range(len(self.Buttons2)):
            for j in range(4):
                self.Buttons2[i][j].setParent(None)
                self.Buttons2[i][j].deleteLater()
                
        self.Buttons2 = []
        
        if self.spacer_widget_2:
            self.spacer_widget_2.setParent(None)
            self.spacer_widget_2.deleteLater()       
            self.spacer_widget_2 = None
        

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
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        
        frame_1_layout = QGridLayout()
        frame_1_items = QFrame()
        frame_1_items.setStyleSheet(style_frame)
        frame_1_items.setLayout(frame_1_layout)
        
        frame_2_layout = QGridLayout()
        frame_2_position = QFrame()
        frame_2_position.setStyleSheet(style_frame)
        frame_2_position.setLayout(frame_2_layout)
        
        frame_3_layout = QGridLayout()
        frame_3_3dfiles = QFrame()
        frame_3_3dfiles.setStyleSheet(style_frame)
        frame_3_3dfiles.setLayout(frame_3_layout)
        
        frame_4_layout = QGridLayout()
        frame_4_plotter = QFrame()
        frame_4_plotter.setStyleSheet(style_frame)
        frame_4_plotter.setLayout(frame_4_layout)
        
        frame_5_layout = QGridLayout()
        frame_5_origin = QFrame()
        frame_5_origin.setStyleSheet(style_frame)
        frame_5_origin.setLayout(frame_5_layout)
        
        self.layout.addWidget(frame_1_items, 0, 0)
        self.layout.addWidget(frame_2_position, 1, 0)
        self.layout.addWidget(frame_3_3dfiles, 0, 1, 2, 1)
        self.layout.addWidget(frame_4_plotter, 0, 2)
        self.layout.addWidget(frame_5_origin, 1, 2)
  
  
        #### frame 1
        title = QLabel("Items")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_1_layout.addWidget(title, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_area2 = QGridLayout(scroll_widget) 
        
        scroll_area.setWidget(scroll_widget)
        frame_1_layout.addWidget(scroll_area) 


        #### frame 2   
        title = QLabel("Change position:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_2_layout.addWidget(title, 0, 0, 1, 2)
        
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.pos_entry.append(entry)

            row = idx + 1
            col = 0

            frame_2_layout.addWidget(label, row, col)
            frame_2_layout.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        button_update_pos = QPushButton("Update")
        button_update_pos.setStyleSheet(style_button)
        button_update_pos.clicked.connect(lambda: change_pos_object())
        frame_2_layout.addWidget(button_update_pos,7, 0, 1, 2)


        ## frame 3
        title = QLabel("3D files:")
        title.setFixedHeight(30)
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_3_layout.addWidget(title, 0 , 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_area1 = QGridLayout(scroll_widget) 
        
        scroll_area.setWidget(scroll_widget)
        frame_3_layout.addWidget(scroll_area) 
               
         
        ## frame 4
        self.layout_plotter = QGridLayout()
        frame_plotter = QFrame()
        frame_4_layout.addWidget(frame_plotter, 0, 0)
        frame_plotter.setLayout(self.layout_plotter)  
                
                
                
        ## frame 5 
        title = QLabel("Change origin:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        frame_5_layout.addWidget(title,0,0,1,2)
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            row = idx + 1 
            col = 0

            frame_5_layout.addWidget(label, row, col)
            frame_5_layout.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        button = QPushButton("Update")
        button.setStyleSheet(style_button)
        frame_5_layout.addWidget(button,7, 0, 1, 2)
        button.clicked.connect(lambda: change_origin_object())
    
        
        button = QPushButton("Add new 3D model")
        button.setStyleSheet(style_button)
        frame_5_layout.addWidget(button, 8, 0, 1, 2)
        button.clicked.connect(lambda: add_new_object_model())




        
