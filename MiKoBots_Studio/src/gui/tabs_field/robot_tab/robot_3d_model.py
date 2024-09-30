from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

import pyvistaqt as pvt
import pyvista as pv

from backend.core.event_manager import event_manager

from backend.core.api import move_robot_model
from backend.core.api import show_3d_model_settings
from backend.core.api import delete_robot_model
from backend.core.api import change_origin_3d_model
from backend.core.api import add_new_3d_model
from backend.core.api import save_robot

class Robot3DModel(QWidget): 
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
                
        self.Robot_buttons = []
        self.stl_object = [0] * 2
        
        self.spacer_widget = None
        
        self.GUI()
        self.CreatePlanes(100)
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_delete_buttons_3d_model", self.DeleteButtons)
        event_manager.subscribe("request_clear_plotter_3d_model", self.ClearPlotter)
        event_manager.subscribe("request_create_buttons_3d_model", self.CreateButtons)
        event_manager.subscribe("request_show_3d_model", self.ShowModelPlotter)
        event_manager.subscribe("request_show_origin_3d_model", self.SetOriginfields)
        event_manager.subscribe("request_get_origin_3d_model", self.GetOriginData)
        event_manager.subscribe("request_close_plotter_3d_model", self.ClosePlotter)
    
    def GUI(self):
        main_layout = QVBoxLayout(self.frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        
        layout = QGridLayout(scroll_widget)
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout.addWidget(scroll_area)

        # Frame with the stl files
        title = QLabel("3D files:")
        title.setStyleSheet(style_label_bold)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout.addWidget(title,0,0)
        
        
        # create an area where the parts will be placed
        scroll_area2 = QScrollArea()
        scroll_area2.setWidgetResizable(True)
        scroll_area2.setFixedWidth(400)
        self.layout = QGridLayout(scroll_area2)
        
        layout.addWidget(scroll_area2,1,0)    
        
        # frame with change origin
        layout_options = QGridLayout()
        frame_options = QFrame()
        frame_options.setMaximumWidth(250)
        layout.addWidget(frame_options,0,1,2,1)
        frame_options.setLayout(layout_options)
        
        ## frame with the plotter
        self.PLOTTER_ORIGIN_ROBOT = pvt.QtInteractor()
        self.PLOTTER_ORIGIN_ROBOT.setFixedHeight(200)
        self.PLOTTER_ORIGIN_ROBOT.setFixedWidth(220)
        self.PLOTTER_ORIGIN_ROBOT.add_axes()
        #self.PLOTTER_ORIGIN_ROBOT.add_axes()
        
        layout_options.addWidget(self.PLOTTER_ORIGIN_ROBOT,0,0)
        
        title = QLabel("Change origin:")
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,0)
        
        labels = ["X:", "Y:", "Z:", "y:", "p:", "r:"]
        self.origin_pos = []
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setStyleSheet(style_label)
            label.setFixedWidth(20)  # Set the width as needed

            # make sure only int and float numbers are filled in
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setStyleSheet(style_entry)
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.origin_pos.append(entry)

            row = idx + 2
            col = 0

            layout_options.addWidget(label, row, col)
            layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
            
        self.button_update = QPushButton("Update")
        self.button_update.setStyleSheet(style_button)
        layout_options.addWidget(self.button_update,8, 0, 1, 2)
        self.button_update.clicked.connect(lambda: change_origin_3d_model())
        
        self.button_add_new = QPushButton("Add new 3D model")
        self.button_add_new.setStyleSheet(style_button)
        layout_options.addWidget(self.button_add_new, 9, 0, 1, 2)
        self.button_add_new.clicked.connect(lambda: add_new_3d_model())  
        
        button = QPushButton("Save robot")
        button.setStyleSheet(style_button)
        layout_options.addWidget(button, 10, 0, 1, 2)
        button.clicked.connect(lambda: save_robot(True))        
        
        spacer_widget = QWidget()
        spacer_widget.setStyleSheet(style_widget)
        layout.addWidget(spacer_widget, layout.rowCount(), 3)                          

    def ShowModelPlotter(self, path):
        self.stl_object[0] = pv.read(path)
        self.stl_object[1] = self.PLOTTER_ORIGIN_ROBOT.add_mesh(self.stl_object[0], color="red", show_edges=False)            
            
    def ClearPlotter(self):
        if self.stl_object[1]:
            self.PLOTTER_ORIGIN_ROBOT.remove_actor(self.stl_object[1])

    def ClosePlotter(self):
        self.PLOTTER_ORIGIN_ROBOT.close()

    def CreateButtons(self, item, robot_3d_data):
        if self.spacer_widget:
            self.spacer_widget.deleteLater()    
            self.spacer_widget.setParent(None)
            self.spacer_widget = None
            
        self.Robot_buttons.append([[],[],[],[],[],[],[]])
            
        label = QLabel(robot_3d_data[item][0])
        label.setStyleSheet(style_label)
        label.setMinimumWidth(60)
        self.layout.addWidget(label, item * 2, 0, 2, 1)
        self.Robot_buttons[item][0] = label
        
        button = QPushButton("▲")
        button.setStyleSheet(style_button)
        button.setFixedSize(25,10)
        button.pressed.connect(lambda idx = item: move_robot_model(idx, 1))
        self.layout.addWidget(button, item * 2, 1)
        self.Robot_buttons[item][1] = button
        
        button = QPushButton("▼")
        button.setFixedSize(25,10)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: move_robot_model(idx, 0))
        self.layout.addWidget(button, item*2+1, 1)
        self.Robot_buttons[item][2] = button
        
        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: delete_robot_model(idx))
        self.layout.addWidget(button, item*2, 2, 2, 1)
        self.Robot_buttons[item][3] = button
        
        button = QPushButton("Origin")
        button.setFixedSize(75,25)
        button.setStyleSheet(style_button)
        button.pressed.connect(lambda idx = item: show_3d_model_settings(idx))
        self.layout.addWidget(button, item*2, 3, 2, 1)
        self.Robot_buttons[item][4] = button
        
        def on_combobox_change(nr):
            robot_3d_data[nr][3] = combo_color.currentText()
            
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        for i in range(len(colors)):
            if colors[i] == robot_3d_data[item][3]:
                combo_nr = i
        
        combo_color = QComboBox()
        combo_color.addItems(colors)
        combo_color.setStyleSheet(style_combo)
        combo_color.setCurrentIndex(combo_nr)
        combo_color.currentIndexChanged.connect(lambda index, idx = item: on_combobox_change(idx))
        self.layout.addWidget(combo_color, item*2, 4, 2, 1)
        self.Robot_buttons[item][5] = combo_color
        
                        
        def on_linkage_change(nr):
            robot_3d_data[nr][5] = combo.currentText()
            print(combo.currentText()) 
        
        linkages = ['Link 1', 'Link 2', 'Link 3', 'Link 4', 'Link 5', 'Link 6', 'Base']
        combo_nr = 0
        for i in range(len(linkages)):
            if linkages[i] == robot_3d_data[item][5]:
                combo_nr = i

        
        combo = QComboBox()
        combo.setStyleSheet(style_combo)
        combo.addItems(linkages)
        combo.setCurrentIndex(combo_nr)
        combo.currentIndexChanged.connect(lambda index, idx = item: on_linkage_change(idx))
        self.layout.addWidget(combo, item*2, 5, 2, 1)
        self.Robot_buttons[item][6] = combo
        
            
        self.spacer_widget = QWidget()
        self.spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def DeleteButtons(self):
        for i in range(len(self.Robot_buttons)):
            for j in range(len(self.Robot_buttons[i])):
                self.Robot_buttons[i][j].setParent(None)
                self.Robot_buttons[i][j].deleteLater()
                
        self.Robot_buttons = []    
        
        if self.spacer_widget:
            self.spacer_widget.deleteLater()    
            self.spacer_widget.setParent(None)
            self.spacer_widget = None


    def SetOriginfields(self, data):
        for i in range(6):
            self.origin_pos[i].setText(str(data[i]))
            
    def GetOriginData(self, data):
        for i in range(6):
            try:
                data[i] = float(self.origin_pos[i].text())
            except:
                data[i] = 0.0
                self.origin_pos[i].setText("0.0")
                
        return data
            
    def CreatePlanes(self, size):
        origin = [0,0,0]
        normal_xy = [0,0,1]
        normal_xz = [0,1,0]
        normal_zy = [1,0,0]
        
        plane_xy = pv.Plane(center=origin, direction=normal_xy, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_ROBOT.add_mesh(plane_xy, opacity=0.5, color="blue") 
        
        plane_xz = pv.Plane(center=origin, direction=normal_xz, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_ROBOT.add_mesh(plane_xz, opacity=0.5, color="blue") 
        
        plane_zy = pv.Plane(center=origin, direction=normal_zy, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_ROBOT.add_mesh(plane_zy, opacity=0.5, color="blue") 
    
    