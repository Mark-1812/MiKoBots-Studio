from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

import pyvistaqt as pvt
import pyvista as pv

from backend.core.event_manager import event_manager

from backend.core.api import add_new_tool
from backend.core.api import delete_tool
from backend.core.api import show_tool_settings
from backend.core.api import update_tool_settings

class RobotTools(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
                
        self.Tools_robot_buttons = []
        self.stl_object = [0] * 2
  
        self.GUI()
        self.CreatePlanes(100)
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_create_buttons_tool", self.CreateButtons)
        event_manager.subscribe("request_new_buttons", self.CreateButtons)
        event_manager.subscribe("request_delete_buttons_tool", self.DeleteButtons)
        event_manager.subscribe("request_show_tool_settings", self.ShowSettings)
        event_manager.subscribe("request_get_tool_data", self.GetToolData)
        event_manager.subscribe("request_show_tool", self.ShowModel)
        event_manager.subscribe("request_clear_plotter_tool", self.ClearPlotter) 
        event_manager.subscribe("request_close_plotter_tool", self.ClosePlotter)     
    
    def GUI(self):
        main_layout = QVBoxLayout(self.frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(
                "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
                "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
                "QPushButton:hover { background-color: white; }"
                "QPushButton:pressed { background-color: darkorange; }"+
                "QCheckBox {  background-color: white; }"+
                "QLabel {font-size: 12px; font-family: Arial;}"+
                "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QComboBox { background-color: white; }"
                "QLineEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        
        layout = QGridLayout(scroll_widget)
        
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout.addWidget(scroll_area)

        # Frame with the stl files
        title = QLabel("Tools:")
        title.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        title.setFixedHeight(30)
        
        layout.addWidget(title,0,0)
        
        
        # create an area where the parts will be placed
        scroll_area2 = QScrollArea()
        scroll_area2.setWidgetResizable(True)
        scroll_area2.setFixedWidth(330)
        self.layout = QGridLayout(scroll_area2)
        
        layout.addWidget(scroll_area2,1,0)    

        # frame with change origin
        layout_options = QGridLayout()
        frame_options = QFrame()
        frame_options.setMaximumWidth(250)
        layout.addWidget(frame_options,0,1,4,1)
        frame_options.setLayout(layout_options)
        
        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 2, 0) 
        
        ## frame with the plotter
        self.PLOTTER_ORIGIN_TOOL = pvt.QtInteractor()
        self.PLOTTER_ORIGIN_TOOL.setFixedHeight(200)
        self.PLOTTER_ORIGIN_TOOL.setFixedWidth(330)
        #self.PLOTTER_ORIGIN_TOOL.add_axes()
        
        layout.addWidget(self.PLOTTER_ORIGIN_TOOL,3,0)
        
        # put everything on the left side of the screen
        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, layout.rowCount(), 4)
        
        title = QLabel("<b>Tool settings</b>")
        title.setFixedSize(250,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,0,0,1,4)
        
        title = QLabel("Change origin:")
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,0,1,2)
        
        title = QLabel("Tool frame:")
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title,1,2,1,2)
        
        labels = ["X:", "Y:", "Z:", "y", "p", "r"]
        self.entry_origin_pos = []
        self.ToolFrame = []
        
        for idx, label_text in enumerate(labels):
            label = QLabel(label_text)
            label.setFixedWidth(20)  # Set the width as needed

            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)

            entry = QLineEdit()
            entry.setFixedWidth(50)  # Set the width as needed
            entry.setValidator(validator)
            self.entry_origin_pos.append(entry)

            row = idx + 2
            col = 0

            layout_options.addWidget(label, row, col)
            layout_options.addWidget(entry, row, col + 1)  # Put entry in the next column
                       
            label = QLabel(label_text)
            label.setFixedWidth(20)
            
            entry = QLineEdit()
            entry.setFixedWidth(50)
            entry.setValidator(validator)
            self.ToolFrame.append(entry)
            
            layout_options.addWidget(label, row, col + 2)
            layout_options.addWidget(entry, row, col + 3)  # Put entry in the next column
            
        # Pin settings tool
        row = layout_options.rowCount()
            
        title = QLabel("Pin settings tool:")
        title.setFixedSize(125,25)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        layout_options.addWidget(title, row, 0, 1, 4)    
            
        tools = ["Tool pin 1", "Tool pin 2", "Tool pin 3", "Tool pin 4", "Tool pin 5"]
        self.combobox_tool_pin = QComboBox() 
        self.combobox_tool_pin.setStyleSheet("background-color: " + "white")
        self.combobox_tool_pin.setStyleSheet("QComboBox {text-align: center;}")
        layout_options.addWidget(self.combobox_tool_pin, row + 1, 0, 1, 4)
        self.combobox_tool_pin.addItems(tools)

        ## define the type of tool, what is connected to the pin
        # Relay
        self.radio_button_relay = QRadioButton()
        self.radio_button_relay.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_relay.setStyleSheet("QCheckBox { background-color: lightgray}")
        layout_options.addWidget(self.radio_button_relay,  row + 2,0)
        
        label = QLabel("ON/OFF relay")
        layout_options.addWidget(label, row + 2,1,1,3)
        
        # Servo
        self.radio_button_servo = QRadioButton()
        self.radio_button_servo.setChecked(False)  # Set the initial state of the radio_button
        self.radio_button_servo.setStyleSheet("QCheckBox { background-color: lightgray}")
        layout_options.addWidget(self.radio_button_servo, row + 3,0)

        self.entry_servo_min = QLineEdit()
        self.entry_servo_min.setPlaceholderText("Min")
        self.entry_servo_min.setFixedWidth(50)
        self.entry_servo_min.setValidator(validator)
        layout_options.addWidget(self.entry_servo_min, row + 3, 1)
        
        self.entry_servo_max = QLineEdit()
        self.entry_servo_max.setPlaceholderText("Max")
        self.entry_servo_max.setFixedWidth(50)
        self.entry_servo_max.setValidator(validator)
        layout_options.addWidget(self.entry_servo_max, row + 3, 2)

        label = QLabel("Servo")
        layout_options.addWidget(label, row + 3, 3)        
                       
        ## camera offset
        row = layout_options.rowCount()
        
        title = QLabel("Camera offset:")
        title.setFixedSize(250,25)
        layout_options.addWidget(title, row, 0, 1, 4)
        
        label = QLabel("XYZ:")
        layout_options.addWidget(label, row + 1, 0)
        
        self.cam_offset = []
        for i in range(3):
            entry_cam = QLineEdit()
            entry_cam.setFixedWidth(50)
            entry_cam.setValidator(validator)
            layout_options.addWidget(entry_cam, row + 1, i + 1)
            
            self.cam_offset.append(entry_cam)
        
        # Camera turn 180 degrees        
        self.checkbox_cam = QCheckBox('turn camera 180°')
        self.checkbox_cam.setStyleSheet("background-color: lightgray")
        layout_options.addWidget(self.checkbox_cam, row + 2, 0, 1, 4)       
                       
        self.button_update = QPushButton("Update")
        layout_options.addWidget(self.button_update, row + 3, 0, 1, 4)
        self.button_update.clicked.connect(lambda: update_tool_settings())
        
        self.button_add_new = QPushButton("Add new 3D model")
        layout_options.addWidget(self.button_add_new, row + 4, 0, 1, 4)
        self.button_add_new.clicked.connect(lambda: add_new_tool())      
        
        spacer_widget = QWidget()
        layout_options.addWidget(spacer_widget, layout_options.rowCount(), 4)

    def CreateButtons(self, item, tool_data):
        self.Tools_robot_buttons.append([[],[],[],[]])
            
        label = QLabel(tool_data[item][0])
        label.setMinimumWidth(60)
        self.layout.addWidget(label, item, 0)
        self.Tools_robot_buttons[item][0] = label
        
        button = QPushButton("X")
        button.setFixedSize(25,25)
        button.pressed.connect(lambda idx = item: delete_tool(idx))
        self.layout.addWidget(button, item, 1)
        self.Tools_robot_buttons[item][1] = button
        
        button = QPushButton("Settings")
        button.setFixedSize(75,25)
        button.pressed.connect(lambda idx = item: show_tool_settings(idx))
        self.layout.addWidget(button, item, 2)
        self.Tools_robot_buttons[item][2] = button
        
        def on_combobox_change(nr):
            tool_data[nr][3] = combo.currentText()
       
        colors = ['red', 'blue', 'black', 'white', 'darkgray']
        combo_nr = 0
        for i in range(len(colors)):
            if colors[i] == tool_data[item][3]:
                combo_nr = i
        
        combo = QComboBox()
        combo.addItems(colors)
        combo.setCurrentIndex(combo_nr)
        combo.currentIndexChanged.connect(lambda index, idx = item: on_combobox_change(idx))
        self.layout.addWidget(combo, item, 3)
        self.Tools_robot_buttons[item][3] = combo
            
        spacer_widget = QWidget()
        self.layout.addWidget(spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

    def DeleteButtons(self):
        for i in range(len(self.Tools_robot_buttons)):
            for j in range(4):
                self.Tools_robot_buttons[i][j].setParent(None)
                self.Tools_robot_buttons[i][j].deleteLater()
                
        self.Tools_robot_buttons = []

    def CreatePlanes(self, size):
        origin = [0,0,0]
        normal_xy = [0,0,1]
        normal_xz = [0,1,0]
        normal_zy = [1,0,0]
        
        plane_xy = pv.Plane(center=origin, direction=normal_xy, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_TOOL.add_mesh(plane_xy, opacity=0.5, color="blue") 
        
        plane_xz = pv.Plane(center=origin, direction=normal_xz, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_TOOL.add_mesh(plane_xz, opacity=0.5, color="blue") 
        
        plane_zy = pv.Plane(center=origin, direction=normal_zy, i_size=size, j_size=size)
        self.PLOTTER_ORIGIN_TOOL.add_mesh(plane_zy, opacity=0.5, color="blue")

    def DeleteTool(self,item):
        self.send_signal_delete_tool.emit(item)
    
    def ShowSettings(self, tool_settings): 
        print("show settings")

        if self.stl_object[1] != 0:
            self.PLOTTER_ORIGIN_TOOL.remove_actor(self.stl_object[1])
        
        # Set the settings
        for i in range(6):
            self.entry_origin_pos[i].setText(str(tool_settings[4][i]))
            self.ToolFrame[i].setText(str(tool_settings[5][i]))
        
        # Set the combo box
        self.combobox_tool_pin.setCurrentText(tool_settings[6]) 
              
        if tool_settings[7] == "Servo":
            self.radio_button_servo.setChecked(True)
            self.radio_button_relay.setChecked(False)
        elif tool_settings[7] == "Relay":
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(True)
        else:
            self.radio_button_servo.setChecked(False)
            self.radio_button_relay.setChecked(False)
            
        value = tool_settings[8]
        self.entry_servo_min.setText(str(value[0]))
        self.entry_servo_max.setText(str(value[1]))
        
        offset = tool_settings[9]
        for i in range(3):
            self.cam_offset[i].setText(str(offset[i]))
            
        if tool_settings[10] == 1:
            self.checkbox_cam.setChecked(True)
        else:
            self.checkbox_cam.setChecked(False)

    def ClearPlotter(self):
        if self.stl_object[1] != 0:
            self.PLOTTER_ORIGIN_TOOL.remove_actor(self.stl_object[1])

    def ClosePlotter(self):
        self.PLOTTER_ORIGIN_TOOL.close()

    def ShowModel(self, path):
        self.stl_object[0] = pv.read(path)
        self.stl_object[1] = self.PLOTTER_ORIGIN_TOOL.add_mesh(self.stl_object[0], color="red", show_edges=False)            
   
    def GetToolData(self, data_tool):
        if self.stl_object[0] == 0:
            return
        
        for i in range(6):
            try:
                data_tool[4][i] = float(self.entry_origin_pos[i].text())
            except:
                data_tool[4][i] = 0
                self.entry_origin_pos[i].setText("0.0")
            
            try:
                data_tool[5][i] = float(self.ToolFrame[i].text())
            except:
                data_tool[5][i] = 0
                self.ToolFrame[i].setText("0.0")       
        
        data_tool[6] = self.combobox_tool_pin.currentText() 
           
        if self.radio_button_relay.isChecked():
            data_tool[7] = "Relay"
        elif self.radio_button_servo.isChecked():
            data_tool[7] = "Servo"
            value = ["0","0"]
            try:
                value[0] = float(self.entry_servo_min.text())
            except:
                value[0] = 0.0
                self.entry_servo_min.setText("0.0")
            
            try:
                value[1] = float(self.entry_servo_max.text())
            except:
                value[1] = 0.0
                self.entry_servo_max.setText("0.0")
                
            data_tool[8] = value
        
        offset = []
        for i in range(3):
            try:
                value = float(self.cam_offset.text())
                offset.append(value)
            except:
                offset.append(0.0)
            
        data_tool[9] = offset
        
        if self.checkbox_cam.isChecked:
            data_tool[10] = 1
        else:
            data_tool[10] = 0
        
        return data_tool

