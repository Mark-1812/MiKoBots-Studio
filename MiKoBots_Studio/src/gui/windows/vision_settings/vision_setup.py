from PyQt5.QtWidgets import QLineEdit, QLabel, QFrame, QSlider, QComboBox, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

from backend.core.event_manager import event_manager

from gui.style import *

from backend.vision import show_square, change_size_square, cam_tool_connected

from gui.windows.message_boxes import ErrorMessage

class VisionSetup(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self) 
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        self.image_HSV = None
        self.image_RGB = None
        self.PICTURE = False
        
        self.gui()
        self.subscribeToEvents()
    
    
    def subscribeToEvents(self):
        event_manager.subscribe("request_get_offset_cam", self.GetOffsetCam)
        event_manager.subscribe("request_get_square_size", self.GetSquareSize)
        
        event_manager.subscribe("request_set_vision_settings", self.SetVisionSettings)
        event_manager.subscribe("request_get_vision_settings", self.GetVisionSettings)
        
        
    def gui(self):
        label = QLabel("Camera settings")        
        label.setStyleSheet(style_label_bold)
        self.layout.addWidget(label) 

        frame = QFrame()
        frame.setFixedWidth(250)
        frame_layout = QGridLayout()
        frame_layout.setSpacing(5)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(frame_layout)
        self.layout.addWidget(frame)
        
        self.checkbox_cam_tool = QCheckBox("Camera connected to the tool")
        self.checkbox_cam_tool.stateChanged.connect(self.cam_connec_tool)
        self.checkbox_cam_tool.setStyleSheet(style_checkbox)
        frame_layout.addWidget(self.checkbox_cam_tool,0,0,1,2)
        
        self.checkbox_cal_square = QCheckBox("show calibration square")
        self.checkbox_cal_square.stateChanged.connect(self.show_square)
        self.checkbox_cal_square.setStyleSheet(style_checkbox)
        frame_layout.addWidget(self.checkbox_cal_square,1,0,1,2)

        label = QLabel("X postion (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        frame_layout.addWidget(label,2,0)
        self.entry_X_pos = QLineEdit()
        self.entry_X_pos.setStyleSheet(style_entry)
        frame_layout.addWidget(self.entry_X_pos,2,1)

        label = QLabel("Y position (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        frame_layout.addWidget(label,3,0)
        self.entry_Y_pos = QLineEdit()
        self.entry_Y_pos.setStyleSheet(style_entry)
        frame_layout.addWidget(self.entry_Y_pos,3,1)
        
        label = QLabel("Rotation camera (deg):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        frame_layout.addWidget(label,4,0)
        self.entry_rot = QLineEdit()
        self.entry_rot.setStyleSheet(style_entry)
        frame_layout.addWidget(self.entry_rot,4,1)
        
        label = QLabel("change the size of the calibration square")
        label.setStyleSheet(style_label)
        frame_layout.addWidget(label, 5,0,1,2)
        
        label = QLabel("Square size (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        frame_layout.addWidget(label,6,0)
        self.entry_square_size = QLineEdit("160")
        self.entry_square_size.setStyleSheet(style_entry)
        frame_layout.addWidget(self.entry_square_size,6,1)
        
        button = QPushButton("+")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: change_size_square(True))
        frame_layout.addWidget(button, 7, 0, 1, 2)

        button = QPushButton("-")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: change_size_square(False))
        frame_layout.addWidget(button, 8, 0, 1, 2)

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(space_widget)  


    def GetVisionSettings(self):
        x = float(self.entry_X_pos.text())
        y = float(self.entry_Y_pos.text())
        rot = float(self.entry_rot.text())
        square_size = int(self.entry_square_size.text())
        checkbox = self.checkbox_cam_tool.isChecked()
        
        data = [x, y, rot, square_size, checkbox]
        return data
    
    def SetVisionSettings(self, data):
        self.entry_X_pos.setText(str(data[0]))
        self.entry_Y_pos.setText(str(data[1]))
        self.entry_rot.setText(str(data[2]))
        self.entry_square_size.setText(str(data[3]))
        self.checkbox_cam_tool.setChecked(data[4])
        
    def GetOffsetCam(self):
        x = float(self.entry_X_pos.text())
        y = float(self.entry_Y_pos.text())
        rot = float(self.entry_rot.text())
        offset = [x,y, rot]
        
        return offset
  
    def GetSquareSize(self):
        square_size = int(self.entry_square_size.text())
        return square_size

    def SetOffsetCam(self, offset):
        print("set cam offset")
        
        x = str(offset[0])
        y = str(offset[1])
        rot = str(offset[2])
        
        self.entry_X_pos.setText(x)
        self.entry_Y_pos.setText(y)
        self.entry_rot.setText(rot)
        
        return offset
        
    def show_square(self, state):
        if state == 2:  # Checked (Qt.Checked)
            show_square(True)
        else:  # Unchecked (Qt.Unchecked)
            show_square(False)    
            
    def cam_connec_tool(self, state):
        if state == 2:  # Checked (Qt.Checked)
            cam_tool_connected(True)
        else:  # Unchecked (Qt.Unchecked)
            cam_tool_connected(False)               
            
 