from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from backend.core.event_manager import event_manager

class RobotSettings(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
     
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_robot_settings", self.LoadSettings)
        event_manager.subscribe("request_get_robot_settings", self.GetSettings)
        
    def LoadSettings(self, settings_file):
        print("load settings...")
        # Add the logic to load robot settings here
                   
        try:
            for i, setting in enumerate(self.settings):
                settings = settings_file[self.settings_name[i+1]]
                
                setting.set_values(settings[0])
                setting.set_IOCheckbox(settings[1])
            
            
            self.entry_nr_joints.setText(str(settings_file[self.settings_name[0]]))
                
        except FileNotFoundError:
            print("erro with setting the settings")
                
    def GetSettings(self):
        settings_file = {}

        for i, setting in enumerate(self.settings):
            settings = [None,None]
            settings[0] = setting.get_values()
            settings[1] = setting.get_IOCheckbox()
            settings_file[self.settings_name[i + 1]] = settings
            
        settings_file[self.settings_name[0]] = self.entry_nr_joints.text()
            
        print(settings_file)
            
        return settings_file    
        
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
    
        
        row1 = QFrame()
        layout.addWidget(row1, 0, 0, 1, 3)
        layout_row1 = QGridLayout()
        row1.setLayout(layout_row1)
        
        label = QLabel("Number of joints:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        layout_row1.addWidget(label, 0, 0)
        
        self.entry_nr_joints = QLineEdit()
        self.entry_nr_joints.setText("6")
        self.entry_nr_joints.setStyleSheet("background-color: white")        
        layout_row1.addWidget(self.entry_nr_joints, 0, 1)
        
        label = QLabel("At the moment the software only works with a robot with 6 joints")
        layout_row1.addWidget(label, 1, 0, 1, 2)    
        
        ### settings
        column1 = QFrame()
        column1.setMaximumWidth(230)
        layout.addWidget(column1, 1, 0)
        layout_column1 = QGridLayout()
        column1.setLayout(layout_column1)
        
        column2 = QFrame()
        column2.setMaximumWidth(230)
        layout.addWidget(column2, 1, 1)
        layout_column2 = QGridLayout()
        column2.setLayout(layout_column2)     

        column3 = QFrame()
        column3.setMaximumWidth(230)
        layout.addWidget(column3, 1, 2)
        layout_column3 = QGridLayout()
        column3.setLayout(layout_column3)
        
        column4 = QFrame()
        column4.setMaximumWidth(500)
        layout.addWidget(column4, 2, 0, 1, 3)
        layout_column4 = QGridLayout()
        column4.setLayout(layout_column4)
        
        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 0, 4, 3, 1)
                
        self.settings = []  
        

        self.settings_name = [
            'Set_number_of_joints','Set_motor_pin', 'Set_switch_pin', 'Set_tools', 
            'Set_io_pin','Set_max_pos', 'Set_lim_pos', 'Set_step_deg', 
            'Set_dir_joints','Set_speed', 'Set_dh_par'               
            ] 
        
        setting_names = ["PUL pin J1: ","DIR pin J1: ","PUL pin J2: ","DIR pin J2: ", "PUL pin J3: ","DIR pin J3: ",
                    "PUL pin J4: ","DIR pin J4: ", "PUL pin J5: ","DIR pin J5: ", "PUL pin J6: ","DIR pin J6: "]
        self.settings.append(CreateFields(layout_column1, start_row=0, rows=12, columns=1, row_names=setting_names, title="<b>Motor pin<b>"))
       
        setting_names = ["S1 pin: ","S2 pin: ","S3 pin: ","S4 pin: ","S5 pin: ","S6 pin: "]
        self.settings.append(CreateFields(layout_column1,14 ,6, 1,setting_names,"<b>Switch pin<b>",("")))

        setting_names = ["Tool 1: ","Tool 2: ","Tool 3: ","Tool 4: ", "Tool 5: "]
        self.settings.append(CreateFields(layout_column1, start_row=22, rows=5, columns=1, row_names=setting_names, title="<b>Tool pin<b>",CheckBoxPin=True))

        setting_names = ["IO 1: ","IO 2: ","IO 3: ","IO 4: ", "IO 5: ","IO 6: ","IO 7: ","IO 8: ","IO 9: ", "IO 10: "]
        self.settings.append(CreateFields(layout_column1, start_row=30, rows=10, columns=1, row_names=setting_names, title="<b>IO pin<b>",CheckBoxPin=True))

        setting_names = ["J1 min: ", "J1 max: ", "J2 min: ", "J2 max: ", "J3 min: ", "J3 max: ", 
                            "J4 min: ", "J4 max: ", "J5 min: ", "J5 max: ", "J6 min: ", "J6 max: ",]
        self.settings.append(CreateFields(layout_column2, 0, 12, 1, setting_names,"<b>Max movement joints<b>",("")))

        setting_names = ["Pos S1: ", "Pos S2: ", "Pos S3: ", "Pos S4: ", "Pos S5: ", "Pos S6: "]
        self.settings.append(CreateFields(layout_column2, 14, 6, 1,setting_names,"<b>Max movement joints<b>",("")))

        setting_names = ["step_deg_J1: ", "step_deg_J2: ", "step_deg_J3: ", "step_deg_J4: ", "step_deg_J5: ", "step_deg_J6: ",]
        self.settings.append(CreateFields(layout_column3, 0, 6, 1,setting_names,"<b>step deg<b>",("")))

        setting_names = ["Direction J1: ", "Direction J2: ", "Direction J3: ", "Direction J4: ", "Direction J5: ", "Direction J6: ",]
        self.settings.append(CreateFields(layout_column3,7 ,6, 1,setting_names,"<b>direction of the joints<b>",("")))

        setting_names = ["J1 max vel", "J1 max acc","J2 max vel", "J2 max acc","J3 max vel", "J3 max acc",
                                 "J4 max vel", "J4 max acc","J5 max vel", "J5 max acc","J6 max vel", "J6 max acc",]
        self.settings.append(CreateFields(layout_column3,15 ,12, 1,setting_names,"<b>max speed/ acceleration<b>",("")))

        setting_names_Y = ["Joint 1","Joint 2","Joint 3","Joint 4","Joint 5","Joint 6"] 
        setting_names_X = ["a", "alfpa", "d", "delta"]
        self.settings.append(CreateFields(layout_column4,14 ,6, 4,setting_names_Y,"<b>DH - parameters<b>",setting_names_X))

        spacer_widget = QWidget()
        layout_column1.addWidget(spacer_widget, layout_column1.rowCount(), 0, 1, layout_column1.columnCount())
        spacer_widget = QWidget()
        layout_column2.addWidget(spacer_widget, layout_column2.rowCount(), 0, 1, layout_column2.columnCount())
        spacer_widget = QWidget()
        layout_column3.addWidget(spacer_widget, layout_column3.rowCount(), 0, 1, layout_column3.columnCount())
        spacer_widget = QWidget()
        layout_column4.addWidget(spacer_widget, 0, layout_column4.columnCount(), layout_column4.rowCount(), 0)     
 
        main_layout.addWidget(scroll_area)
                          
        button = QPushButton("test")
        button.clicked.connect(lambda: self.CreateFields)
        


    
class CreateFields():
    def __init__ (self, layout, start_row, rows, columns, row_names,  title, column_names=None, default_values=None, CheckBoxPin=None):
        self.rows = rows
        self.columns = columns
        self.entry_boxes = []
        self.row_index = start_row
        self.row_names = row_names
        self.column_names = column_names
        self.IOCheckBox = False

        if title != "":
            label = QLabel(title)
            label.setFixedHeight(50)
            layout.addWidget(label, self.row_index,0)
            self.checkbox = QCheckBox('IO')
        
            if CheckBoxPin:                    
                self.checkbox.setChecked(False)  # Set the initial state of the checkbox
                self.checkbox.setStyleSheet("QCheckBox { background-color: lightgray}")
                layout.addWidget(self.checkbox, self.row_index, 1)
                
                
            self.row_index += 1             
        
        q = 0

        # Create entry boxes
        if column_names:
            rows = rows + 1

        for i in range(rows):
            row_entries = []
            col_index = 0
            
            if i == 0 and columns > 1:
                for j in range(columns):
                    col_index += 1
                    label = QLabel(column_names[j])
                    label.setFixedHeight(30)
                    label.setFixedWidth(80)
                    layout.addWidget(label, self.row_index,col_index)
                self.row_index += 1
            else:
                if columns == 1: 
                    label = QLabel(row_names[i])
                    label.setFixedWidth(80)
                    layout.addWidget(label, self.row_index,col_index)
                    col_index += 1

                    value = default_values[i] if default_values else ""
                    
                    entry = QLineEdit()
                    entry.setFixedWidth(80)
                    entry.setText(str(value))
                    entry.setStyleSheet("QLineEdit { background-color: white; font-size: 12px;}")
                    layout.addWidget(entry, self.row_index, col_index)
                    self.entry_boxes.append(entry)
        
                else:
                    label = QLabel(row_names[i-1])
                    layout.addWidget(label, self.row_index,col_index)
                    col_index += 1
                    
                    for j in range(columns):
                        value = default_values[i-1][j] if default_values else ""
                        
                        entry = QLineEdit()
                        entry.setFixedWidth(80)
                        entry.setText(str(value))
                        entry.setStyleSheet("QLineEdit { background-color: white; font-size: 12px;}")
                        layout.addWidget(entry, self.row_index, col_index)
                        row_entries.append(entry)
                        
                        col_index += 1                            
                    self.entry_boxes.append(row_entries)
                self.row_index += 1
                q += 1

    def get_values(self):
        # Retrieve values from entry boxes
        values = []
        for i in range(self.rows):
            if self.columns == 1:
                value = self.entry_boxes[i].text()
                values.append(value)
            else:
                value = self.entry_boxes[5][0].text()
                row_values = []
                for j in range(self.columns):
                    value = self.entry_boxes[i][j].text()
                    row_values.append(value) 
                values.append(row_values)
                
                
        return values

    def get_IOCheckbox(self):
        if self.checkbox.isChecked():
            return "IO"
        else:
            return ""

    def set_values(self, values):
        # Set values to entry boxes
        for i in range(self.rows):
            if self.columns == 1:
                self.entry_boxes[i].setText(values[i])
            else:
                for j in range(self.columns):
                    self.entry_boxes[i][j].setText(values[i][j])

    def set_IOCheckbox(self, value):
        if value == "IO":
            self.checkbox.setChecked(True)
    


'''
class RobotSettings(QWidget):
    
    def __init__(self, frame, event_manager):
        super().__init__()
        self.frame = frame
        
        #self.signals()
        event_manager.request_set_robot_settings.connect(self.load_settings)
        
        #self.GUI(frame) 
        
    def load_settings(self):   
        print("load settings...")   
        pass     

      
    def GUI(self, frame):
        main_layout = QVBoxLayout(frame)

        
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
        scroll_layout = QGridLayout(scroll_widget)
          
        row1 = QFrame()
        scroll_layout.addWidget(row1, 0, 0, 1, 3)
        layout_row1 = QGridLayout()
        row1.setLayout(layout_row1)
        
        label = QLabel("Number of joints:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        layout_row1.addWidget(label, 0, 0)
        
        entry = QLineEdit()
        entry.setText("6")
        entry.setStyleSheet("background-color: white")        
        layout_row1.addWidget(entry, 0, 1)
        
        label = QLabel("At the moment the software only works with a robot with 6 joints")
        layout_row1.addWidget(label, 1, 0, 1, 2)
          
        ### settings
        column1 = QFrame()
        column1.setMaximumWidth(230)
        scroll_layout.addWidget(column1, 1, 0)
        layout_column1 = QGridLayout()
        column1.setLayout(layout_column1)
        
        column2 = QFrame()
        column2.setMaximumWidth(230)
        scroll_layout.addWidget(column2, 1, 1)
        layout_column2 = QGridLayout()
        column2.setLayout(layout_column2)
        
        column3 = QFrame()
        column3.setMaximumWidth(230)
        scroll_layout.addWidget(column3, 1, 2)
        layout_column3 = QGridLayout()
        column3.setLayout(layout_column3)
        
        column4 = QFrame()
        column4.setMaximumWidth(500)
        scroll_layout.addWidget(column4, 2, 0, 1, 3)
        layout_column4 = QGridLayout()
        column4.setLayout(layout_column4)
        
        spacer_widget = QWidget()
        scroll_layout.addWidget(spacer_widget, 0, 4, 3, 1)
        
        

        self.settings = []
        self.settings_name = [
            'Set_motor_pin', 'Set_switch_pin', 'Set_tools', 'Set_io_pin',
            'Set_max_pos', 'Set_lim_pos', 'Set_step_deg', 
            'Set_dir_joints','Set_speed', 'Set_dh_par'               
            ]         

        setting_values = ["0" , "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        setting_names = ["PUL pin J1: ","DIR pin J1: ","PUL pin J2: ","DIR pin J2: ", "PUL pin J3: ","DIR pin J3: ",
                    "PUL pin J4: ","DIR pin J4: ", "PUL pin J5: ","DIR pin J5: ", "PUL pin J6: ","DIR pin J6: "]
        self.settings.append(self.create_fields(layout_column1, start_row=0, rows=12, columns=1, row_names=setting_names, title="<b>Motor pin<b>",default_values=setting_values))
        
        setting_values = ["0", "0", "0", "0", "0", "0"]
        setting_names = ["S1 pin: ","S2 pin: ","S3 pin: ","S4 pin: ","S5 pin: ","S6 pin: "]
        self.settings.append(self.create_fields(layout_column1,14 ,6, 1,setting_names,"<b>Switch pin<b>",(""), setting_values))
        
        setting_values = ["0" , "0", "0", "0", "0", "0"]
        setting_names = ["Tool 1: ","Tool 2: ","Tool 3: ","Tool 4: ", "Tool 5: "]
        self.settings.append(self.create_fields(layout_column1, start_row=22, rows=5, columns=1, row_names=setting_names, title="<b>Tool pin<b>",default_values=setting_values,CheckBoxPin=True))

        setting_values = ["0" , "0", "0", "0", "0", "0", "0" , "0", "0", "0", "0", "0"]
        setting_names = ["IO 1: ","IO 2: ","IO 3: ","IO 4: ", "IO 5: ","IO 6: ","IO 7: ","IO 8: ","IO 9: ", "IO 10: "]
        self.settings.append(self.create_fields(layout_column1, start_row=30, rows=10, columns=1, row_names=setting_names, title="<b>IO pin<b>",default_values=setting_values,CheckBoxPin=True))

        
        setting_values = ["0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]
        setting_names = ["J1 min: ", "J1 max: ", "J2 min: ", "J2 max: ", "J3 min: ", "J3 max: ", 
                            "J4 min: ", "J4 max: ", "J5 min: ", "J5 max: ", "J6 min: ", "J6 max: ",]
        self.settings.append(self.create_fields(layout_column2, 0, 12, 1, setting_names,"<b>Max movement joints<b>",(""), setting_values))
           
        setting_values = ["0", "0", "0", "0", "0", "0"]
        setting_names = ["Pos S1: ", "Pos S2: ", "Pos S3: ", "Pos S4: ", "Pos S5: ", "Pos S6: "]
        self.settings.append(self.create_fields(layout_column2, 14, 6, 1,setting_names,"<b>Max movement joints<b>",(""), setting_values))

        
        setting_values = ["0", "0", "0", "0", "0", "0"]
        setting_names = ["step_deg_J1: ", "step_deg_J2: ", "step_deg_J3: ", "step_deg_J4: ", "step_deg_J5: ", "step_deg_J6: ",]
        self.settings.append(self.create_fields(layout_column3, 0, 6, 1,setting_names,"<b>step deg<b>",(""), setting_values))

        setting_values = ["0", "0", "0", "0", "0", "0"]
        setting_names = ["Direction J1: ", "Direction J2: ", "Direction J3: ", "Direction J4: ", "Direction J5: ", "Direction J6: ",]
        self.settings.append(self.create_fields(layout_column3,7 ,6, 1,setting_names,"<b>direction of the joints<b>",(""), setting_values))
        
        
        setting_values = ["30", "1000","100", "1000","100", "1000", "100", "1000","100", "1000","200", "1000",]
        setting_names = ["J1 max vel", "J1 max acc","J2 max vel", "J2 max acc","J3 max vel", "J3 max acc",
                                 "J4 max vel", "J4 max acc","J5 max vel", "J5 max acc","J6 max vel", "J6 max acc",]
        self.settings.append(self.create_fields(layout_column3,15 ,12, 1,setting_names,"<b>max speed/ acceleration<b>",(""), setting_values))

        setting_values = [
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"],
            ["0", "0", "0", "0"]
        ]   
        setting_names_Y = ["Joint 1","Joint 2","Joint 3","Joint 4","Joint 5","Joint 6"] 
        setting_names_X = ["a", "alfpa", "d", "delta"]
        self.settings.append(self.create_fields(layout_column4,14 ,6, 4,setting_names_Y,"<b>DH - parameters<b>",setting_names_X,setting_values))
         
        spacer_widget = QWidget()
        layout_column1.addWidget(spacer_widget, layout_column1.rowCount(), 0, 1, layout_column1.columnCount())
        spacer_widget = QWidget()
        layout_column2.addWidget(spacer_widget, layout_column2.rowCount(), 0, 1, layout_column2.columnCount())
        spacer_widget = QWidget()
        layout_column3.addWidget(spacer_widget, layout_column3.rowCount(), 0, 1, layout_column3.columnCount())
        spacer_widget = QWidget()
        layout_column4.addWidget(spacer_widget, 0, layout_column4.columnCount(), layout_column4.rowCount(), 0)     
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout.addWidget(scroll_area)      
    
    def signals(self):
        self.event_manager.request_set_robot_settings.connect(self.load_settings)
        print(f"1 event_manager {self.event_manager.request_set_robot_settings}")
        print("signallllllls")

    def load_settings(self):
        print("load settings")
        # try:
        #     settings_file = var.SETTINGS
            
        #     # Set the dh paramerters
        #     settings = settings_file['Set_dh_par']
        #     var.DH_PARAM = settings[0]
            
        #     setting = settings_file['Set_max_pos']
        #     var.ROBOT_JOINT_MOVE = setting[0]
            
        #     print(var.DH_PARAM)
            
        #     for i, setting in enumerate(self.settings):
        #         settings = settings_file[self.settings_name[i]]
        #         setting.set_values(settings[0])
        #         setting.set_IOCheckbox(settings[1])

        # except FileNotFoundError:
        #     print("erro with setting the settings")

        


    def changeRobot(self):
        settings_file = var.SETTINGS

        for i, setting in enumerate(self.settings):
            settings = settings_file[self.settings_name[i]]
            setting.set_values(settings[0])
            setting.set_IOCheckbox(settings[1])

    def safe_settings(self):
        settings_file = {}

        for i, setting in enumerate(self.settings):
            settings = [None,None]
            settings[0] = setting.get_values()
            settings[1] = setting.get_IOCheckbox()
            settings_file[self.settings_name[i]] = settings
    
        var.SETTINGS = settings_file  
'''   