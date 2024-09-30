import json

from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

import backend.core.variables as var

from backend.file_managment.file_management import FileManagement

from gui.style import *

class VisionInfo():
    def __init__(self, frame):
        self.file_management = FileManagement()
        
        layout = QVBoxLayout(frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("background-color: lightGray;")
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QVBoxLayout(scroll_widget)        
       
        label = QLabel("Import the vision library")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("from robot_library import Vision")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Vision functions")
        label.setStyleSheet(style_label_title)
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the vision function:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        entry.setText("vision = VisionFunctions()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("<b>Find object</b>")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("object_list = vision.find_object(color = str, size = [w,h])")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("find object is used to find specified by the color or size of the object<br>"
                "<b>color:</b> color of the object<br>"
                "<b>size:</b> size of the object in mm, does not need be specified<br><br>"
                "<b>object_list:</b> is a list that contains the following information of each object:<br>"
                "<b>color:</b> [[Xobject_place, Yobject_place, width, height, angle, color],.....]<br>"
                "<b>Xobject_place:</b> Place of the object in x coordinate<br>"
                "<b>Yobject_place:</b> Place of the object in y coordinate<br>"
                "<b>width:</b> The width of the object<br>"
                "<b>height:</b> The height of the object<br>"
                "<b>angle:</b> The angle of the object<br>"
                "<b>color:</b> The input color<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)
        
        # Move to object
        label = QLabel("Move to object")
        label.setStyleSheet(style_label_bold)
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("vision.move_to_object(list_objects = list, number = int, Zdistance = float)")
        entry.setReadOnly(True)
        entry.setStyleSheet(style_entry)
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setStyleSheet(style_label)
        label.setText("Move to an object out of the list, from find objects<br>"
                "<b>list_objects:</b> the list from Move  to object.<br>"
                "<b>number:</b> which object out of the list usually 0.<br>"
                "<b>Zdistance:</b> Z height.<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)        
   

 
        # The colors that can be used, you can modify colors
        label = QLabel("Colors HSV")        
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label) 
        
        data = var.colors_options      
        formatted_string = "\n".join([f"{key}: {value}" for key, value in data.items()])
        
        self.colors_text = QTextEdit()
        self.colors_text.setReadOnly(True)
        self.colors_text.setStyleSheet(style_textedit)
        self.colors_text.setPlainText(formatted_string)
        #self.colors_text.textChanged.connect(self.update_text_content)
        scroll_layout.addWidget(self.colors_text)   
            
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        
        layout.addWidget(scroll_area)
      
    def update_text_content(self):
        json_string = '{"'
        json_string += self.colors_text.toPlainText()
        json_string = json_string.replace('\n', ',"')
        json_string = json_string.replace(':', '":')
        json_string += '}'
    
        try:  
            var.colors_options = json.loads(json_string)
        except:
            print("error")
        
    
        try:              
            settings_file = [VD.colors_options]
            file_path = self.file_management.GetFilePath("/settings/colors.json")
            
            with open(file_path, 'w') as file:
                json.dump(settings_file, file, indent=4)
        except:
            pass
  