from PyQt5.QtWidgets import QLineEdit, QLabel, QFrame, QSlider, QComboBox, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator
from PyQt5.QtWidgets import QSpacerItem, QSizePolicy

from backend.vision.vision_management import VisionManagement
import cv2
from backend.core.event_manager import event_manager

from gui.style import *

import numpy as np

import backend.core.variables as var

from backend.vision import get_image_frame, cam_connected, show_square, change_size_square, cam_tool_connected

from gui.windows.message_boxes import ErrorMessage

class VisionSetup(QWidget):
    def __init__(self, frame):     
        super().__init__()  
        self.frame = frame
        self.layout = QVBoxLayout(self.frame)
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
        
        self.CamSettingsGUI(frame_layout)
        
        frame = QFrame()
        frame_layout = QGridLayout()
        frame_layout.setSpacing(5)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(frame_layout)
        self.layout.addWidget(frame)
        
        self.ColorsSettingsGUI(frame_layout)

        space_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(space_widget)  


                     
        
    def ColorsSettingsGUI(self, layout):
        label = QLabel("Colors HSV")        
        label.setStyleSheet(style_label_bold)
        layout.addWidget(label, 0, 0) 
        
        self.image_label = QLabel(self)
        self.image_label.setFixedWidth(300)
        layout.addWidget(self.image_label, 0, 1, 11, 1)
        
        
        
        self.color_ranges_init = {
            "RED": [[0, 50, 100], [25, 255, 255]],  #0, 10, 100, 255, 100, 255
            "GREEN": [[35, 100, 100], [85, 255, 255]],
            "BLUE": [[100, 100, 100], [130, 255, 255]],
            "YELLOW": [[20, 100, 100], [30, 255, 255]],
            "ORANGE": [[10, 100, 100], [20, 255, 255]],
            "BLACK": [[0, 0, 0], [180, 255, 50]],
            "GRAY": [[0, 0, 50], [180, 50, 200]],     
            "WHITE": [[0, 0, 200], [180, 50, 255]],    
        }
        
        
        self.colors_combo = QComboBox()
        self.colors_combo.setStyleSheet(style_combo)
        layout.addWidget(self.colors_combo, 2 , 0)
        
        
        button_show_image = QPushButton("Show image")
        button_show_image.clicked.connect(self.ShowImage)
        button_show_image.setStyleSheet(style_button_menu)
        layout.addWidget(button_show_image, 1, 0)
        
        button_show_image = QPushButton("Update image")
        button_show_image.clicked.connect(self.UpdateImage)
        button_show_image.setStyleSheet(style_button_menu)
        layout.addWidget(button_show_image, 3, 0)
        
        button_save_color = QPushButton("Save color")
        button_save_color.clicked.connect(self.SaveColor)
        button_save_color.setStyleSheet(style_button_menu)
        layout.addWidget(button_save_color, 4, 0)
        
        button_restore_color = QPushButton("restore color")
        button_restore_color.clicked.connect(self.RestoreColor)
        button_restore_color.setStyleSheet(style_button_menu)
        layout.addWidget(button_restore_color, 5, 0)
        
        
        # Create sliders for HSV ranges
        self.lower_hue_slider = CreateSlider(layout, 6, 'Lower Hue', 0, 179)
        self.upper_hue_slider = CreateSlider(layout, 7, 'Upper Hue', 0, 179)
        self.lower_sat_slider = CreateSlider(layout, 8, 'Lower Sat', 0, 255)
        self.upper_sat_slider = CreateSlider(layout, 9, 'Upper Sat', 0, 255)
        self.lower_val_slider = CreateSlider(layout, 10, 'Lower Val', 0, 255)
        self.upper_val_slider = CreateSlider(layout, 11, 'Upper Val', 0, 255)
        
    def CamSettingsGUI(self, layout):
        self.checkbox_cam_tool = QCheckBox("Camera connected to the tool")
        self.checkbox_cam_tool.stateChanged.connect(self.cam_connec_tool)
        self.checkbox_cam_tool.setStyleSheet(style_checkbox)
        layout.addWidget(self.checkbox_cam_tool,0,0,1,2)
        
        self.checkbox_cal_square = QCheckBox("show calibration square")
        self.checkbox_cal_square.stateChanged.connect(self.show_square)
        self.checkbox_cal_square.setStyleSheet(style_checkbox)
        layout.addWidget(self.checkbox_cal_square,1,0,1,2)

        label = QLabel("X postion (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        layout.addWidget(label,2,0)
        self.entry_X_pos = QLineEdit()
        self.entry_X_pos.setStyleSheet(style_entry)
        layout.addWidget(self.entry_X_pos,2,1)

        label = QLabel("Y position (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        layout.addWidget(label,3,0)
        self.entry_Y_pos = QLineEdit()
        self.entry_Y_pos.setStyleSheet(style_entry)
        layout.addWidget(self.entry_Y_pos,3,1)
        
        label = QLabel("Rotation camera (deg):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        layout.addWidget(label,4,0)
        self.entry_rot = QLineEdit()
        self.entry_rot.setStyleSheet(style_entry)
        layout.addWidget(self.entry_rot,4,1)
        
        label = QLabel("change the size of the calibration square")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 5,0,1,2)
        
        label = QLabel("Square size (mm):")
        label.setStyleSheet(style_label)
        label.setFixedWidth(150)
        layout.addWidget(label,6,0)
        self.entry_square_size = QLineEdit("160")
        self.entry_square_size.setStyleSheet(style_entry)
        layout.addWidget(self.entry_square_size,6,1)
        
        button = QPushButton("+")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: change_size_square(True))
        layout.addWidget(button, 7, 0, 1, 2)

        button = QPushButton("-")
        button.setStyleSheet(style_button_menu)
        button.clicked.connect(lambda: change_size_square(False))
        layout.addWidget(button, 8, 0, 1, 2)


    def GetVisionSettings(self):
        x = float(self.entry_X_pos.text())
        y = float(self.entry_Y_pos.text())
        rot = float(self.entry_rot.text())
        square_size = int(self.entry_square_size.text())
        checkbox = self.checkbox_cam_tool.isChecked()
        colors = var.COLOR_RANGE
        
        data = [x, y, rot, square_size, checkbox, colors]
        print(data)
        return data
    
    def SetVisionSettings(self, data):
        self.entry_X_pos.setText(str(data[0]))
        self.entry_Y_pos.setText(str(data[1]))
        self.entry_rot.setText(str(data[2]))
        self.entry_square_size.setText(str(data[3]))
        self.checkbox_cam_tool.setChecked(data[4])
        self.colors_combo.addItems(data[5].keys())
        self.colors_combo.currentIndexChanged.connect(self.ChangeColor)
        

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


    def SaveColor(self):
        lower_hue = self.lower_hue_slider.current_val
        upper_hue = self.upper_hue_slider.current_val
        lower_sat = self.lower_sat_slider.current_val
        upper_sat = self.upper_sat_slider.current_val
        lower_val = self.lower_val_slider.current_val
        upper_val = self.upper_val_slider.current_val
        
        HSV_range = [[lower_hue, lower_sat, lower_val], [upper_hue, upper_sat, upper_val]]
    
        color = self.colors_combo.currentText()
    
        var.COLOR_RANGE[color] = HSV_range
    
    def RestoreColor(self):
        color = self.colors_combo.currentText()
        
        var.COLOR_RANGE[color] = self.color_ranges_init[color]
        
        initial_hsv_ranges = var.COLOR_RANGE.get(color)
        
        
        self.lower_hue_slider.slider.setValue(initial_hsv_ranges[0][0])
        self.lower_sat_slider.slider.setValue(initial_hsv_ranges[0][1])
        self.lower_val_slider.slider.setValue(initial_hsv_ranges[0][2])
        
        self.upper_hue_slider.slider.setValue(initial_hsv_ranges[1][0])
        self.upper_sat_slider.slider.setValue(initial_hsv_ranges[1][1])
        self.upper_val_slider.slider.setValue(initial_hsv_ranges[1][2])
            
    def ChangeColor(self):
        if not self.PICTURE:
            return
        
        color = self.colors_combo.currentText()
        
        initial_hsv_ranges = var.COLOR_RANGE.get(color)
        
        self.lower_hue_slider.slider.setValue(initial_hsv_ranges[0][0])
        self.lower_sat_slider.slider.setValue(initial_hsv_ranges[0][1])
        self.lower_val_slider.slider.setValue(initial_hsv_ranges[0][2])
        
        self.upper_hue_slider.slider.setValue(initial_hsv_ranges[1][0])
        self.upper_sat_slider.slider.setValue(initial_hsv_ranges[1][1])
        self.upper_val_slider.slider.setValue(initial_hsv_ranges[1][2])
        
        # Define the lower and upper bounds as arrays
        lower_bound = np.array(initial_hsv_ranges[0])
        upper_bound = np.array(initial_hsv_ranges[1])

        # Create the mask and apply it to the image
        mask = cv2.inRange(self.image_HSV, lower_bound, upper_bound)
        masked_image = cv2.bitwise_and(self.image_RGB, self.image_RGB, mask=mask)

        # Convert the masked image to QImage format
        height, width, channel = masked_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(masked_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert QImage to QPixmap and scale it to a max width of 200 pixels, keeping aspect ratio
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(300, height, Qt.KeepAspectRatio)
        
        # Display the scaled image in the QLabel
        self.image_label.setPixmap(scaled_pixmap)
    
    def ShowImage(self):
        print(f"check connection cam {cam_connected()}")
        
        
        
        if not cam_connected():
            ErrorMessage(var.LANGUAGE_DATA.get("message_cam_not_connect"))
            return
        
        color = self.colors_combo.currentText()
        
        initial_hsv_ranges = var.COLOR_RANGE.get(color)
        
        
        self.lower_hue_slider.slider.setValue(initial_hsv_ranges[0][0])
        self.lower_sat_slider.slider.setValue(initial_hsv_ranges[0][1])
        self.lower_val_slider.slider.setValue(initial_hsv_ranges[0][2])
        
        self.upper_hue_slider.slider.setValue(initial_hsv_ranges[1][0])
        self.upper_sat_slider.slider.setValue(initial_hsv_ranges[1][1])
        self.upper_val_slider.slider.setValue(initial_hsv_ranges[1][2])
        
        frame = get_image_frame()
        self.image_RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        self.image_HSV = cv2.cvtColor(self.image_RGB, cv2.COLOR_RGB2HSV)
        
        self.PICTURE = True
        
        
        # Define the lower and upper bounds as arrays
        lower_bound = np.array(initial_hsv_ranges[0])
        upper_bound = np.array(initial_hsv_ranges[1])
        
        # Create the mask and apply it to the image
        mask_HSV = cv2.inRange(self.image_HSV, lower_bound, upper_bound)
        masked_image = cv2.bitwise_and(self.image_RGB, self.image_RGB, mask=mask_HSV)
        
        # Convert the masked image to QImage format
        height, width, channel = masked_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(masked_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        
        # Convert QImage to QPixmap and scale it to a max width of 200 pixels, keeping aspect ratio
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(300, height, Qt.KeepAspectRatio)
        
        # Display the scaled image in the QLabel
        self.image_label.setPixmap(scaled_pixmap)
        
    def show_square(self, state):
        if state == 2:  # Checked (Qt.Checked)
            show_square(True)
        else:  # Unchecked (Qt.Unchecked)
            show_square(False)    
            
    def cam_connec_tool(self, state):
        if state == 2:  # Checked (Qt.Checked)
            cam_tool_connected(False)
        else:  # Unchecked (Qt.Unchecked)
            cam_tool_connected(True)               
            
      
    def UpdateImage(self):
        if not self.PICTURE:
            return
        
        
        
        """Update the displayed image based on the current HSV slider values."""
        # Get HSV ranges from sliders
        lower_hue = self.lower_hue_slider.current_val
        upper_hue = self.upper_hue_slider.current_val
        lower_sat = self.lower_sat_slider.current_val
        upper_sat = self.upper_sat_slider.current_val
        lower_val = self.lower_val_slider.current_val
        upper_val = self.upper_val_slider.current_val
        

        # Define the lower and upper bounds as arrays
        lower_bound = np.array([lower_hue, lower_sat, lower_val])
        upper_bound = np.array([upper_hue, upper_sat, upper_val])

        # Create the mask and apply it to the image
        mask = cv2.inRange(self.image_HSV, lower_bound, upper_bound)
        masked_image = cv2.bitwise_and(self.image_RGB, self.image_RGB, mask=mask)

        # Convert the masked image to QImage format
        height, width, channel = masked_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(masked_image.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # Convert QImage to QPixmap and scale it to a max width of 200 pixels, keeping aspect ratio
        pixmap = QPixmap.fromImage(q_image)
        scaled_pixmap = pixmap.scaled(300, height, Qt.KeepAspectRatio)
        
        # Display the scaled image in the QLabel
        self.image_label.setPixmap(scaled_pixmap)
        
            
        
class CreateSlider():
    def __init__(self, layout, row, name, min_val, max_val):
        slider_layout = QGridLayout()
        
        self.current_val = 0
        self.name = name
        
        # Label for the minimum value
        min_label = QLabel(str(min_val))
        min_label.setStyleSheet(style_label)
        min_label.setFixedWidth(10)
        slider_layout.addWidget(min_label, 0, 2)
        
        # Create a slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setStyleSheet(style_slider)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(10)
        self.slider.valueChanged.connect(self.updateLabel)
        self.slider.setObjectName(name)
        slider_layout.addWidget(self.slider, 0, 3)        

        # Label for the maximum value
        max_label = QLabel(str(max_val))
        max_label.setStyleSheet(style_label)
        max_label.setFixedWidth(20)
        slider_layout.addWidget(max_label, 0, 4) 
        
        self.value_label = QLabel(f"{name}: 0")
        self.value_label.setObjectName(f"{name}_label")
        self.value_label.setStyleSheet(style_label)
        self.value_label.setFixedWidth(90)
        slider_layout.addWidget(self.value_label, 0, 1)        

        layout.addLayout(slider_layout, row, 0)
    
    def updateLabel(self, value):
        self.current_val = value
        self.value_label.setText(f"{self.name}: {value}")                   


        
        
 
                  

    
        
        