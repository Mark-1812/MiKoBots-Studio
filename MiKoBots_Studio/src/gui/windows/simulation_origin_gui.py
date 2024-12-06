from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

from backend.core.event_manager import event_manager
from backend.file_managment.file_management import FileManagement

from backend.simulation.origins import add_origin
from backend.simulation.origins import delete_origin
from backend.simulation.origins import save_origin

from gui.style import *

class SimulationOriginGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)    
        self.setWindowTitle("Add Origin")
        self.setFixedSize(500,200)
        self.setStyleSheet("background-color: #E8E8E8;")
        
        file_management = FileManagement()
        image_path = file_management.resource_path('mikobot.ico')
        self.setWindowIcon(QIcon(image_path))
           
        self.Origins = []
        self.widgets = []
        self.axes_lines = []
        
        self.spacer_widget = None
        
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_create_button_origin", self.CreateButtons)
        event_manager.subscribe("request_delete_buttons_origin", self.DeleteButtons)
        event_manager.subscribe("request_delete_space_origin", self.DeleteSpacerWidget)
        event_manager.subscribe("request_get_data_origin", self.GetData)
    
    def GUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)
        


            
        frame = QFrame()
        frame.setStyleSheet(style_frame)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(5, 5, 5, 5)
        frame.setLayout(main_layout)
        self.layout.addWidget(frame) 
        
        scroll = QScrollArea()
        scroll.setStyleSheet(style_scrollarea)
        scroll.setWidgetResizable(True)

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_layout = QVBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setAlignment(Qt.AlignTop)

        scroll.setWidget(scroll_widget)
        main_layout.addWidget(scroll)

        self.button_add_new = QPushButton("Add new Origin")
        self.button_add_new.setStyleSheet(style_button_menu)
        main_layout.addWidget(self.button_add_new)
        self.button_add_new.clicked.connect(lambda: add_origin())



    def GetData(self, item):
        data = [0,0,0,0]
        
        data[0] = self.widgets[item][0].text()
        data[1] = self.widgets[item][2].text()
        data[2] = self.widgets[item][4].text()
        data[3] = self.widgets[item][6].text()
        
        return data

    def CreateButtons(self, item, data):
        self.widgets.append([[],[],[],[],[],[],[],[],[]])

        frame = QFrame()
        layout = QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 5)
        frame.setLayout(layout)
        self.scroll_layout.addWidget(frame) 

        entry = QLineEdit()
        entry.setStyleSheet(style_entry)
        entry.setText(data[0])
        entry.setFixedWidth(80)  # Set the width as needed
        layout.addWidget(entry)
        self.widgets[item][0] = entry
        
        label = QLabel("X:")
        label.setStyleSheet(style_label)
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        layout.addWidget(label)
        self.widgets[item][1] = label
        
        entry_X = QLineEdit()
        entry_X.setStyleSheet(style_entry)
        entry_X.setText(str(data[1]))
        entry_X.setFixedWidth(40)  # Set the width as needed
        layout.addWidget(entry_X)
        self.widgets[item][2] = entry_X
        
        label = QLabel("Y:")
        label.setStyleSheet(style_label)
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        layout.addWidget(label)
        self.widgets[item][3] = label
        
        entry_Y = QLineEdit()
        entry_Y.setStyleSheet(style_entry)
        entry_Y.setText(str(data[2]))
        entry_Y.setFixedWidth(40)  # Set the width as needed
        layout.addWidget(entry_Y)
        self.widgets[item][4] = entry_Y
        
        label = QLabel("Z:")
        label.setStyleSheet(style_label)
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        layout.addWidget(label)
        self.widgets[item][5] = label
        
        entry_Z = QLineEdit()
        entry_Z.setStyleSheet(style_entry)
        entry_Z.setText(str(data[3]))
        entry_Z.setFixedWidth(40)  # Set the width as needed
        layout.addWidget(entry_Z)
        self.widgets[item][6] = entry_Z
        
        button_Save = QPushButton("Save")
        button_Save.setStyleSheet(style_button)
        button_Save.setFixedSize(40,20)
        button_Save.pressed.connect(lambda idx = item: save_origin(idx))
        layout.addWidget(button_Save)
        self.widgets[item][7] = button_Save
        
        button_del = QPushButton("Delete")
        button_del.setStyleSheet(style_button)
        button_del.setFixedSize(40,20)
        button_del.pressed.connect(lambda idx = item: delete_origin(idx))
        layout.addWidget(button_del)
        self.widgets[item][8] = button_del
        

    def DeleteSpacerWidget(self):
        # delete the spacer under rhe buttons
        if self.spacer_widget:
            self.spacer_widget.setParent(None)
            self.spacer_widget.deleteLater()    
            self.spacer_widget = None    
        
    def DeleteButtons(self):
        for j in range(len(self.widgets)):
            for i in range(9):
                self.widgets[j][i].setParent(None)
                self.widgets[j][i].deleteLater() 
                
        self.widgets = []