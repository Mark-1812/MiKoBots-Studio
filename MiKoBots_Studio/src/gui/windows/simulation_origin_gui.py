from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QDialog, QCheckBox, QSlider, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5 import  QtGui

from backend.core.event_manager import event_manager

from backend.core.api import add_origin
from backend.core.api import delete_origin
from backend.core.api import save_origin

class SimulationOriginGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)       
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
        
        self.setWindowTitle("Add Origin")
        self.setWindowIcon(QtGui.QIcon('mikobot.ico'))
        self.setFixedSize(500,200)

        self.setStyleSheet(
            "QFrame { background-color: lightgray; border: 0px solid black; border-radius: 5px; }" +
            "QPushButton { background-color: orange; color: black; border: 0px solid black; border-radius: 3px; height: 20px; font-size: 12px;font-family: Arial;}"
            "QPushButton:hover { background-color: white; }"
            "QPushButton:pressed { background-color: darkorange; }"+
            "QCheckBox {  background-color: white; }"+
            "QLabel {font-size: 12px; font-family: Arial;}"+
            "QTextEdit { background-color: white; border-radius: 5px; font-size: 12px;}"
            )
        
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        self.layout.addWidget(scroll_area,0,0)

        self.button_add_new = QPushButton("Add new Origin")
        self.layout.addWidget(self.button_add_new, 1, 0)
        self.button_add_new.clicked.connect(lambda: add_origin())
        
        frame_origins = QFrame()
        self.layout_origins = QGridLayout(frame_origins)
        scroll_area.setWidget(frame_origins)
        
        print(self.layout)

    def GetData(self, item):
        data = [0,0,0,0]
        
        data[0] = self.widgets[item][0].text()
        data[1] = self.widgets[item][2].text()
        data[2] = self.widgets[item][4].text()
        data[3] = self.widgets[item][6].text()
        
        return data

    def CreateButtons(self, item, data):
        self.widgets.append([[],[],[],[],[],[],[],[],[]])
        
        entry = QLineEdit()
        entry.setText(data[0])
        entry.setFixedWidth(80)  # Set the width as needed
        self.layout_origins.addWidget(entry, item, 0)
        self.widgets[item][0] = entry
        
        label = QLabel("X:")
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        self.layout_origins.addWidget(label, item, 1)
        self.widgets[item][1] = label
        
        entry_X = QLineEdit()
        entry_X.setText(str(data[1]))
        entry_X.setFixedWidth(40)  # Set the width as needed
        self.layout_origins.addWidget(entry_X, item, 2)
        self.widgets[item][2] = entry_X
        
        label = QLabel("Y:")
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        self.layout_origins.addWidget(label, item, 3)
        self.widgets[item][3] = label
        
        entry_Y = QLineEdit()
        entry_Y.setText(str(data[2]))
        entry_Y.setFixedWidth(40)  # Set the width as needed
        self.layout_origins.addWidget(entry_Y, item, 4)
        self.widgets[item][4] = entry_Y
        
        label = QLabel("Z:")
        label.setAlignment(Qt.AlignRight | Qt.AlignCenter)
        label.setMinimumWidth(10)
        self.layout_origins.addWidget(label, item, 5)
        self.widgets[item][5] = label
        
        entry_Z = QLineEdit()
        entry_Z.setText(str(data[3]))
        entry_Z.setFixedWidth(40)  # Set the width as needed
        self.layout_origins.addWidget(entry_Z, item, 6)
        self.widgets[item][6] = entry_Z
        
        button_Save = QPushButton("Save")
        button_Save.setFixedSize(40,20)
        button_Save.pressed.connect(lambda idx = item: save_origin(idx))
        self.layout_origins.addWidget(button_Save, item, 7)
        self.widgets[item][7] = button_Save
        
        button_del = QPushButton("Delete")
        button_del.setFixedSize(40,20)
        button_del.pressed.connect(lambda idx = item: delete_origin(idx))
        self.layout_origins.addWidget(button_del, item, 8)
        self.widgets[item][8] = button_del
        
        self.spacer_widget = QWidget()
        self.layout_origins.addWidget(self.spacer_widget, self.layout_origins.rowCount(), 0, 1, self.layout_origins.columnCount())
    
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