from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator

import cv2

import backend.vision.vision_var as VD
from backend.vision.vision_management import VisionManagement

from backend.core.event_manager import event_manager

from gui.style import *

from backend.core.api import calibrate_vision

class VisionSetup():
    def __init__(self, frame):       
        self.Origins = []
        self.widgets = []
        self.axes_lines = []
        
        self.mm_per_pixel = 1
        self.width_picture = 100
        self.height_picture = 100
        
        self.turncam = 0

        self.CAM_area = [100,100]
        
        self.frame = frame
        self.GUI()
        
        self.cam = VisionManagement()
        
    def GUI(self):
        self.layout = QGridLayout(self.frame)
     
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
     
        button = QPushButton("Calibration square")
        button.setStyleSheet(style_button)
        self.layout.addWidget(button, 0, 0, 1, 2)
        button.clicked.connect(self.display_frame)
        
        button = QPushButton("Calibrate")
        button.setStyleSheet(style_button)
        self.layout.addWidget(button, 1, 0, 1, 2)
        button.clicked.connect(lambda: self.CalibrateVision())
        
        # Calibration squars
        label = QLabel("Z height squars")
        label.setFixedSize(125,25)
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        self.layout.addWidget(label, 2, 0, 1, 2)
        
        self.entry_Z1 = QLineEdit()
        self.entry_Z1.setStyleSheet(style_entry)
        self.entry_Z1.setFixedWidth(50)  # Set the width as needed
        self.entry_Z1.setText("0")
        self.entry_Z1.setValidator(validator)
        self.layout.addWidget(self.entry_Z1, 4, 0)
        
        label = QLabel("mm (biggest square)")
        self.layout.addWidget(label, 4, 1)

        self.entry_Z2 = QLineEdit()
        self.entry_Z2.setStyleSheet(style_entry)
        self.entry_Z2.setFixedWidth(50)  # Set the width as needed
        self.entry_Z2.setText("0")
        self.entry_Z2.setValidator(validator)
        self.layout.addWidget(self.entry_Z2, 5, 0)
        
        label = QLabel(f"mm (smallest square)")
        label.setMaximumWidth(100)
        self.layout.addWidget(label, 5, 1)
        
        # sizeof the tow squares                   
        row = self.layout.rowCount()
        label = QLabel("Square sizes")
        label.setFixedSize(125,25)
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        self.layout.addWidget(label, row, 0)
           
        self.entry_size_1 = QLineEdit()
        self.entry_size_1.setStyleSheet(style_entry)
        self.entry_size_1.setFixedWidth(50) 
        self.entry_size_1.setText("160")
        self.entry_size_1.setValidator(validator)
        self.layout.addWidget(self.entry_size_1, row + 1, 0) 
        
        label = QLabel("mm (square 1)")
        self.layout.addWidget(label, row + 1, 1)     
                       
        self.entry_size_2 = QLineEdit()
        self.entry_size_2.setStyleSheet(style_entry)
        self.entry_size_2.setText("120")
        self.entry_size_2.setFixedWidth(50)
        self.entry_size_2.setValidator(validator)
        self.layout.addWidget(self.entry_size_2, row + 2, 0) 
        
        label = QLabel("mm (square 2)")
        self.layout.addWidget(label, row + 2, 1)   
        
        self.spacer_widget = QWidget()
        self.spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())
                   
    def CalibrateVision(self):
        print("test vison cal")
        TOOL_SETTINGS_CAM = [0,0,0,0,0]
        TOOL_SETTINGS_CAM[0] = float(self.entry_Z1.text())
        TOOL_SETTINGS_CAM[1] = float(self.entry_Z2.text())
        
        TOOL_SETTINGS_CAM[2] = float(self.entry_size_1.text())
        TOOL_SETTINGS_CAM[3] = float(self.entry_size_2.text())
        
        calibrate_vision(TOOL_SETTINGS_CAM)
                             
    def display_frame(self):
        image = VD.image_RGB

        if image is not None:
            self.height_picture, self.width_picture, ch = image.shape 
            
            print(f"{self.height_picture} x {self.width_picture}")
            
            y_1 = int(0.1 * self.height_picture)
            h_1 = int(0.8 * self.height_picture)
            
            w_1 = int(0.8 * self.height_picture)
            x_1 = int((self.width_picture - w_1) / 2)
            
            self.square_size_pixel = 0.8 * self.height_picture
            
            cv2.rectangle(image, (x_1, y_1), (x_1+w_1, y_1+h_1), (0, 255, 0), 2)
            
            event_manager.publish("request_set_pixmap_image", image)
                  

    
        
        