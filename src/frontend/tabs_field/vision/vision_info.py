import json

from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QSizePolicy, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt

import backend.vision.vision_var as VD

from backend.file_managment.file_management import FileManagement



class VisionInfo():
    def __init__(self, frame):
        self.file_management = FileManagement()
        
        layout = QVBoxLayout(frame)
        
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
                "QLineEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
                "QTabBar::tab { background-color: orange; color: black;  height: 20px; width: 80px; font-size: 12px; font-family: Arial;}"
                "QTabBar::tab {border-top-left-radius: 5px;}"
                "QTabBar::tab {border-top-right-radius: 5px;}"
                "QTabBar::tab:selected {background-color: white;}"
                )
        scroll_layout = QVBoxLayout(scroll_widget)        
       
        label = QLabel("Import the vision library")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("from vision.functions import VisionFunctions")       
        scroll_layout.addWidget(entry)
        
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)
        
        label = QLabel("Vision functions")
        label.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        label = QLabel("Declare the vision function:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label)
        
        entry = QLineEdit()
        entry.setText("vision = VisionFunctions()")       
        scroll_layout.addWidget(entry)    
        
        # Find object 
        label = QLabel("<b>Find object</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("object_list = vision.find_object(color = str, size = [w,h])")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
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
        label = QLabel("<b>Move to object</b>")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        label.setMaximumWidth(150)
        scroll_layout.addWidget(label)     
        
        entry = QLineEdit("vision.move_to_object(list_objects = list, number = int, Zdistance = float)")
        scroll_layout.addWidget(entry)       
        
        label = QLabel()
        label.setText("Move to an object out of the list, from find objects<br>"
                "<b>list_objects:</b> the list from Move  to object.<br>"
                "<b>number:</b> which object out of the list usually 0.<br>"
                "<b>Zdistance:</b> Z height.<br>")
        label.setWordWrap(True)
        scroll_layout.addWidget(label)        
   

 
        # The colors that can be used, you can modify colors
        label = QLabel("Colors HSV")        
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        scroll_layout.addWidget(label) 
        
        data = VD.colors_options      
        formatted_string = "\n".join([f"{key}: {value}" for key, value in data.items()])
        
        self.colors_text = QTextEdit()
        self.colors_text.setPlainText(formatted_string)
        self.colors_text.textChanged.connect(self.update_text_content)
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
            VD.colors_options = json.loads(json_string)
        except:
            print("error")
        
    
        try:              
            settings_file = [VD.colors_options]
            file_path = self.file_management.GetFilePath("/settings/colors.json")
            
            with open(file_path, 'w') as file:
                json.dump(settings_file, file)
        except:
            pass
  