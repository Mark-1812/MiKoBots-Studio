from PyQt5.QtWidgets import QPushButton, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator

from gui.style import *

from backend.core.event_manager import event_manager

from backend.robot_management  import save_robot

class RobotSettings(QWidget):
    def __init__(self, frame):
        super().__init__()
        self.frame = frame
        
        self.settings_name = [
            'Set_number_of_joints','Set_extra_joint','Set_motor_pin', 'Set_switch_pin', 'Set_tools', 
            'Set_io_pin','Set_max_pos', 'Set_lim_pos', 'Set_step_deg', 
            'Set_dir_joints', 'Set_speed', 'Set_home_settings', 'Set_dh_par'               
            ] 
        self.settings = [] 
     
        self.Extra_Linkage = 0
     
        self.GUI()
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_robot_settings", self.LoadSettings)
        event_manager.subscribe("request_get_robot_settings", self.GetSettings)
        event_manager.subscribe("request_create_settings_fields", self.CreateSettingsFields)
        event_manager.subscribe("request_delete_settings_fields", self.DeleteSettingsFields)
        
    def LoadSettings(self, settings_file):
        # Add the logic to load robot settings here
                   
        for i, setting in enumerate(self.settings):
            settings = settings_file[self.settings_name[i+2]]
            setting.set_values(settings[0])
            setting.set_IOCheckbox(settings[1])
        
        
        self.entry_nr_joints.setText(str(settings_file[self.settings_name[0]][0]))
        
        if settings_file[self.settings_name[1]][0] == 1:
            self.checkbox.setChecked(True)
            self.Extra_Linkage = 1
            self.settings[10].DeleteFields()
            self.settings[10].CreateFieldsSettings(int(settings_file[self.settings_name[0]][0]) + self.Extra_Linkage)
            settings = settings_file[self.settings_name[i+2]]
            setting.set_values(settings[0])
            
        else:
            self.checkbox.setChecked(False)
            self.Extra_Linkage = 0
                          
    def GetSettings(self):
        settings_file = {}

        for i, setting in enumerate(self.settings):
            settings = [None,None]
            settings[0] = setting.get_values()
            settings[1] = setting.get_IOCheckbox()
            settings_file[self.settings_name[i + 2]] = settings
            
            
        settings_file[self.settings_name[0]] = [self.entry_nr_joints.text(), ""]
        settings_file[self.settings_name[1]] = [self.Extra_Linkage, ""]
        
        return settings_file    
     
    def CreateSettingsFields(self, rows):
        for i in range(len(self.settings)):
            if self.settings[i].times_nr_joints == 1:
                if self.settings[i].title == "<b>DH - parameters<b>":
                    self.settings[i].CreateFieldsSettings(rows + self.Extra_Linkage)
                else:
                    self.settings[i].CreateFieldsSettings(rows)
            elif self.settings[i].times_nr_joints == 2:
                self.settings[i].CreateFieldsSettings(rows * 2)
            else: 
                self.settings[i].CreateFieldsSettings(self.settings[i].rows)
                
    def DeleteSettingsFields(self):
        self.checkbox.setChecked(False)
        self.Extra_Linkage = 0
                
        for i in range(len(self.settings)):
            self.settings[i].DeleteFields()
    
    def GUI(self):
        main_layout = QVBoxLayout(self.frame)
        
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        
        layout = QGridLayout(scroll_widget)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
    
        
        row1 = QFrame()
        layout.addWidget(row1, 0, 0, 1, 3)
        layout_row1 = QGridLayout()
        row1.setLayout(layout_row1)
        
        label = QLabel("Number of joints:")
        label.setStyleSheet(style_label_bold)
        layout_row1.addWidget(label, 0, 0)
        
        self.entry_nr_joints = QLineEdit()
        self.entry_nr_joints.setStyleSheet(style_entry)
        self.entry_nr_joints.setText("6")    
        layout_row1.addWidget(self.entry_nr_joints, 0, 1)
        
        button = QPushButton("Save robot")
        button.setStyleSheet(style_button)
        button.setFixedWidth(100)
        layout_row1.addWidget(button, 0, 2)
        button.clicked.connect(lambda: save_robot(True))          
        
        label = QLabel("At the moment the software only works with a robot with 6 joints")
        label.setStyleSheet(style_label)
        layout_row1.addWidget(label, 1, 0, 1, 3)    
           
        def checkbox_toggled():
            if self.entry_nr_joints.text() == "3" and self.checkbox.isChecked():
                self.Extra_Linkage = 1
            else:
                self.Extra_Linkage = 0
                self.checkbox.setChecked(False)
           
        self.checkbox = QCheckBox('Extra linkage to keep the tool parrallel to the floor (only for 3 axis robot arm (RRR))')                
        self.checkbox.setChecked(False)  # Set the initial state of the checkbox
        self.checkbox.setStyleSheet(style_checkbox)
        self.checkbox.toggled.connect(checkbox_toggled)
        layout_row1.addWidget(self.checkbox, 2, 0, 1, 2)
        
        
        ### settings
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 1, 0)
        layout_motor_pin = QGridLayout()
        frame.setLayout(layout_motor_pin)
        
        setting_names = ["PUL pin J1: ","DIR pin J1: ","PUL pin J2: ","DIR pin J2: ", "PUL pin J3: ","DIR pin J3: ",
                    "PUL pin J4: ","DIR pin J4: ", "PUL pin J5: ","DIR pin J5: ", "PUL pin J6: ","DIR pin J6: "]
        self.settings.append(CreateFields(layout_motor_pin, rows=12, columns=1, row_names=setting_names, title="<b>Motor pin<b>", times_nr_joints=2))
 
        spacer_widget = QWidget()
        layout_motor_pin.addWidget(spacer_widget, layout_motor_pin.rowCount(), 0, 1, layout_motor_pin.columnCount())
 
       
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 2, 0)
        layout_switch_pin = QGridLayout()
        frame.setLayout(layout_switch_pin)        
 
        setting_names = ["S1 pin: ","S2 pin: ","S3 pin: ","S4 pin: ","S5 pin: ","S6 pin: "]
        self.settings.append(CreateFields(layout_switch_pin, rows=6, columns=1, row_names=setting_names, title="<b>Switch pin<b>", times_nr_joints=1))
       
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 3, 0)
        layout_tool_pin = QGridLayout()
        frame.setLayout(layout_tool_pin)   

        setting_names = ["Tool 1: ","Tool 2: ","Tool 3: ","Tool 4: ", "Tool 5: "]
        self.settings.append(CreateFields(layout_tool_pin, rows=5, columns=1, row_names=setting_names, title="<b>Tool pin<b>",CheckBoxPin=True))

        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 4, 0)
        layout_io_pin = QGridLayout()
        frame.setLayout(layout_io_pin)   
        
        setting_names = ["IO 1: ","IO 2: ","IO 3: ","IO 4: ", "IO 5: ","IO 6: ","IO 7: ","IO 8: ","IO 9: ", "IO 10: "]
        self.settings.append(CreateFields(layout_io_pin, rows=10, columns=1, row_names=setting_names, title="<b>IO pin<b>",CheckBoxPin=True))
           
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 5, 0)
        layout_max_movement = QGridLayout()
        frame.setLayout(layout_max_movement)  
           
        setting_names = ["J1 min: ", "J1 max: ", "J2 min: ", "J2 max: ", "J3 min: ", "J3 max: ", 
                            "J4 min: ", "J4 max: ", "J5 min: ", "J5 max: ", "J6 min: ", "J6 max: ",]
        self.settings.append(CreateFields(layout_max_movement, rows=12, columns=1, row_names=setting_names, title="<b>Max movement joints<b>", times_nr_joints=2))

        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 6, 0)
        layout_pos_switch = QGridLayout()
        frame.setLayout(layout_pos_switch)  
        
        setting_names = ["Pos S1: ", "Pos S2: ", "Pos S3: ", "Pos S4: ", "Pos S5: ", "Pos S6: "]
        self.settings.append(CreateFields(layout_pos_switch, rows=6, columns=1, row_names=setting_names, title="<b>Posistion switch<b>", times_nr_joints=1))

        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 7, 0)
        layout_step_deg = QGridLayout()
        frame.setLayout(layout_step_deg)
        
        setting_names = ["step_deg_J1: ", "step_deg_J2: ", "step_deg_J3: ", "step_deg_J4: ", "step_deg_J5: ", "step_deg_J6: "]
        self.settings.append(CreateFields(layout_step_deg, rows=6, columns=1, row_names=setting_names, title="<b>step deg<b>", times_nr_joints=1))

        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 8, 0)
        layout_dir_joint = QGridLayout()
        frame.setLayout(layout_dir_joint)          
                
        setting_names = ["Direction J1: ", "Direction J2: ", "Direction J3: ", "Direction J4: ", "Direction J5: ", "Direction J6: ",]
        self.settings.append(CreateFields(layout_dir_joint, rows=6, columns=1, row_names=setting_names, title="<b>direction of the joints<b>", times_nr_joints=1))
         
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 9, 0)
        layout_max_speed = QGridLayout()
        frame.setLayout(layout_max_speed)  
                        
        setting_names = ["J1 max vel (deg/s)", "J1 max acc","J2 max vel (deg/s)", "J2 max acc","J3 max vel (deg/s)", "J3 max acc",
                                 "J4 max vel (deg/s)", "J4 max acc","J5 max vel (deg/s)", "J5 max acc","J6 max vel (deg/s)", "J6 max acc",]
        self.settings.append(CreateFields(layout_max_speed, rows=12, columns=1, row_names=setting_names, title="<b>max speed/ acceleration<b>", times_nr_joints=2))
                   
        frame = QFrame()
        frame.setMaximumWidth(300)
        layout.addWidget(frame, 10, 0)
        layout_home = QGridLayout()
        frame.setLayout(layout_home)  
                        
        setting_names = ["Joint 1","Move to","Joint 2","Move to","Joint 3","Move to","Joint 4","Move to","Joint 5","Move to","Joint 6","Move to"] 
        self.settings.append(CreateFields(layout_home, rows=12, columns=1, row_names=setting_names, title="<b>Homing order<b>", times_nr_joints=2))
                       
                     
        frame = QFrame()
        frame.setMaximumWidth(600)
        layout.addWidget(frame, 11, 0)
        layout_dh_param = QGridLayout()
        frame.setLayout(layout_dh_param)  
                        
        setting_names_Y = ["Joint 1","Joint 2","Joint 3","Joint 4","Joint 5","Joint 6","Joint 7"] 
        setting_names_X = ["a", "alfpa", "d", "delta"]
        self.settings.append(CreateFields(layout_dh_param, rows=6, columns=4, row_names=setting_names_Y, title="<b>DH - parameters<b>", column_names=setting_names_X, times_nr_joints=1))
                
        main_layout.addWidget(scroll_area)
                          
        


    
class CreateFields():
    def __init__ (self, layout, rows, columns, row_names,  title, column_names=None, CheckBoxPin=None, times_nr_joints=None):
        self.layout = layout
        self.title = title
        self.rows = rows
        self.columns = columns
        
        self.times_nr_joints = times_nr_joints
        
        self.entry_boxes = []
        self.labels_row = []
        self.labels_col = []
        
        self.spacer_widget = None
        
        self.row_index = 0
        self.row_names = row_names
        self.column_names = column_names
        self.IOCheckBox = False

        if title != "":
            label = QLabel(title)
            label.setStyleSheet(style_label_bold)
            self.layout.addWidget(label, self.row_index, 0, 1 ,2)
            self.checkbox = QCheckBox('IO')
            self.checkbox.setStyleSheet(style_checkbox)
        
            if CheckBoxPin:                    
                self.checkbox.setChecked(False)  # Set the initial state of the checkbox
                self.checkbox.setStyleSheet("QCheckBox { background-color: lightgray}")
                self.layout.addWidget(self.checkbox, self.row_index, 1)
                
                
            self.row_index += 1             

    def get_values(self):
        # Retrieve values from entry boxes
        values = []
        for i in range(self.rows):
            if self.columns == 1:
                try:
                    value = self.entry_boxes[i].text()
                except:
                    value = "0"
                values.append(value)
            else:
                #value = self.entry_boxes[5][0].text()
                row_values = []
                for j in range(self.columns):
                    try:
                        value = self.entry_boxes[i][j].text()
                    except:
                        value = "0"
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
                try:
                    self.entry_boxes[i].setText(values[i])
                except:
                    self.entry_boxes[i].setText("0")
            else:
                for j in range(self.columns):
                    try:
                        self.entry_boxes[i][j].setText(values[i][j])
                    except:
                        self.entry_boxes[i][j].setText("0")

    def set_IOCheckbox(self, value):
        if value == "IO":
            self.checkbox.setChecked(True)
    
    def CreateFieldsSettings(self, rows):   
        self.rows = rows
        
        # Create entry boxes
        if self.column_names:
            self.rows = self.rows + 1
            
        for i in range(self.rows):           
            col_index = 0
            row_entries = []
            
            if i == 0 and self.columns > 1:
                for j in range(self.columns):
                    col_index += 1
                    label = QLabel(self.column_names[j])
                    label.setStyleSheet(style_label)
                    label.setFixedHeight(30)
                    label.setFixedWidth(120)
                    self.layout.addWidget(label, self.row_index, col_index)
                    self.labels_col.append(label)
                self.row_index += 1
            else:
                if self.columns == 1: 
                    label = QLabel(self.row_names[i])
                    label.setStyleSheet(style_label)
                    label.setFixedWidth(120)
                    self.layout.addWidget(label, self.row_index,col_index)
                    self.labels_row.append(label)
                    
                    col_index += 1
                    
                    entry = QLineEdit("0")
                    entry.setFixedWidth(80)
                    entry.setStyleSheet(style_entry)
                    self.layout.addWidget(entry, self.row_index, col_index)
                    
                    self.entry_boxes.append(entry)
        
                else:
                    label = QLabel(self.row_names[i-1])
                    label.setStyleSheet(style_label)
                    self.labels_row.append(label)
                    self.layout.addWidget(label, self.row_index,col_index)
                    col_index += 1
                    
                    for j in range(self.columns):
                        entry = QLineEdit("0")
                        entry.setFixedWidth(80)
                        entry.setStyleSheet(style_entry)
                        self.layout.addWidget(entry, self.row_index, col_index)
                        row_entries.append(entry)
                        
                        col_index += 1                            
                    self.entry_boxes.append(row_entries)
                self.row_index += 1
        
        if self.column_names:
            self.rows = self.rows - 1
        
        self.spacer_widget = QWidget()
        self.spacer_widget.setStyleSheet(style_widget)
        self.layout.addWidget(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())
 
    def DeleteFields(self): 
        if self.columns == 1:      
            for i in range(len(self.entry_boxes)):
                self.entry_boxes[i].setParent(None)
                self.entry_boxes[i].deleteLater()
        else:
            for i in range(len(self.entry_boxes)):
                for j in range(4):
                    self.entry_boxes[i][j].setParent(None)
                    self.entry_boxes[i][j].deleteLater()       
               
                
        for i in range(len(self.labels_row)):
            self.labels_row[i].setParent(None)
            self.labels_row[i].deleteLater()
            
        for i in range(len(self.labels_col)):
            self.labels_col[i].setParent(None)
            self.labels_col[i].deleteLater()
            
        if self.spacer_widget:  
            self.spacer_widget.setParent(None)
            self.spacer_widget.deleteLater()

            

        self.entry_boxes = []
        self.labels_row = []
        self.labels_col = []