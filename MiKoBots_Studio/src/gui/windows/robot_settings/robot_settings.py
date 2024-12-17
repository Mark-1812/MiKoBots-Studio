from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator, QDesktopServices

from gui.style import *

from backend.core.event_manager import event_manager

URL_HELP_PINS = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-pins-esp32/"
URL_HELP_MAX_MOVE = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-max-movement/"
URL_HELP_LIM_POS = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/limit-switch-position/"
URL_HELP_STEPS_SPEED = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-step-per-degree/"
URL_HELP_JOINT_DIR = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/joint-direction/"
URL_HELP_DH_PARAM = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-dh-parameters/"
URL_HOME_ORDER = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/homing-order/"

class RobotSettings(QFrame):   
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self) 
        
        self.settings_name = [
            'Set_robot_name', 'Set_number_of_joints','Set_extra_joint','Set_motor_type','Set_motor_pin', 'Set_switch_pin', 'Set_tools', 
            'Set_io_pin','Set_servo_settings', 'Set_max_pos', 'Set_lim_pos', 'Set_step_deg',
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
        
    def LoadSettings(self, rows, settings_file):
        # Add the logic to load robot settings here
        if settings_file[self.settings_name[2]][0] == 1:
            self.Extra_Linkage = 1

        self.CreateSettingsFields(rows)
        
 
        for i, setting in enumerate(self.settings):
            settings = settings_file[self.settings_name[i+3]]
            setting.set_values(settings[0])
            setting.set_IOCheckbox(settings[1])
        
        self.robot_name.setText(str(settings_file[self.settings_name[0]][0]))
        self.entry_nr_joints.setText(str(settings_file[self.settings_name[1]][0]))
        


        if settings_file[self.settings_name[2]][0] == 1:
            self.checkbox.setChecked(True)
            
        else:
            self.checkbox.setChecked(False)
            self.Extra_Linkage = 0
                          
    def GetSettings(self):
        settings_file = {}

        for i, setting in enumerate(self.settings):
            settings = [None,None]
            settings[0] = setting.get_values()
            settings[1] = setting.get_IOCheckbox()
            settings_file[self.settings_name[i + 3]] = settings


            
        settings_file[self.settings_name[0]] = [self.robot_name.text(), ""]
        settings_file[self.settings_name[1]] = [self.entry_nr_joints.text(), ""]
        settings_file[self.settings_name[2]] = [self.Extra_Linkage, ""]
        
        return settings_file  
     
    def CreateSettingsFields(self, rows):
        for i in range(len(self.settings)):
            print(self.settings[i].title)
            if self.settings[i].times_nr_joints == 1:
                if self.settings[i].title == "DH - parameters":
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
        title = QLabel("Robot settings:")
        title.setStyleSheet(style_label_title)
        title.setFixedHeight(30)
        title.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.addWidget(title)

        # create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setContentsMargins(0, 0, 0, 0)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(self.scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)

        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area) 
        
        
        frame = QFrame(self.scroll_widget)
        self.layout_scroll.addWidget(frame)
        layout_frame = QGridLayout()
        frame.setLayout(layout_frame)

        label = QLabel("Robot name:")
        label.setStyleSheet(style_label_bold)
        layout_frame.addWidget(label, 1, 0)

        self.robot_name = QLineEdit()
        self.robot_name.setStyleSheet(style_entry)
        layout_frame.addWidget(self.robot_name, 1, 1)

        label = QLabel("Number of joints:")
        label.setStyleSheet(style_label_bold)
        layout_frame.addWidget(label, 2, 0)
        
        self.entry_nr_joints = QLineEdit()
        self.entry_nr_joints.setStyleSheet(style_entry)
        layout_frame.addWidget(self.entry_nr_joints, 2, 1)
        
        label = QLabel("At the moment the software only works with a robot with 6 joints")
        label.setStyleSheet(style_label)
        layout_frame.addWidget(label, 3, 0, 1, 3)    
           
        self.checkbox = QCheckBox('Extra linkage to keep the tool parrallel to the floor (only for 3 axis robot arm (RRR))', frame)                
        self.checkbox.setChecked(False)  # Set the initial state of the checkbox
        self.checkbox.setStyleSheet(style_checkbox)
        self.checkbox.toggled.connect(self.checkbox_toggled)
        layout_frame.addWidget(self.checkbox, 4, 0, 1, 2)
        
        
        ### settings
        setting_names = ["J1 type: ","J2 type: ","J3 type: ","J4 type: ","J5 type: ","J6 type: "]
        self.settings.append(CreateFields(rows=6, columns=1, row_names=setting_names, title="Motor type", url = URL_HELP_PINS,  times_nr_joints=1))
        
        setting_names = ["PUL pin J1: ","DIR pin J1: ","PUL pin J2: ","DIR pin J2: ", "PUL pin J3: ","DIR pin J3: ",
                    "PUL pin J4: ","DIR pin J4: ", "PUL pin J5: ","DIR pin J5: ", "PUL pin J6: ","DIR pin J6: "]
        self.settings.append(CreateFields(rows=12, columns=1, row_names=setting_names, title="Motor pin", url = URL_HELP_PINS, times_nr_joints=2))
           
 
        setting_names = ["S1 pin: ","S2 pin: ","S3 pin: ","S4 pin: ","S5 pin: ","S6 pin: "]
        self.settings.append(CreateFields(rows=6, columns=1, row_names=setting_names, title="Switch pin", url = URL_HELP_PINS,  times_nr_joints=1))
       

        setting_names = ["Tool 1: ","Tool 2: ","Tool 3: ","Tool 4: ", "Tool 5: "]
        self.settings.append(CreateFields(rows=5, columns=1, row_names=setting_names, title="Tool pin", url = URL_HELP_PINS, CheckBoxPin=True))

        
        setting_names = ["IO 1: ","IO 2: ","IO 3: ","IO 4: ", "IO 5: ","IO 6: ","IO 7: ","IO 8: ","IO 9: ", "IO 10: "]
        self.settings.append(CreateFields(rows=10, columns=1, row_names=setting_names, title="IO pin", url = URL_HELP_PINS, CheckBoxPin=True))

           
        setting_names = ["J1 Servo pin: ", "J1 Servo max: ", "J1 Servo min: ", "J1 Servo movement: ", 
                         "J2 Servo pin: ", "J2 Servo max: ", "J2 Servo min: ", "J2 Servo movement: ", 
                         "J3 Servo pin: ", "J3 Servo max: ", "J3 Servo min: ", "J3 Servo movement: ", 
                         "J4 Servo pin: ", "J4 Servo max: ", "J4 Servo min: ", "J4 Servo movement: ", 
                         "J5 Servo pin: ", "J5 Servo max: ", "J5 Servo min: ", "J5 Servo movement: ", 
                         "J6 Servo pin: ", "J6 Servo max: ", "J6 Servo min: ", "J6 Servo movement: "]
        self.settings.append(CreateFields(rows=24, columns=1, row_names=setting_names, title="Servo settings", url = URL_HELP_MAX_MOVE, times_nr_joints=4))
        
        setting_names = ["J1 min: ", "J1 max: ", "J2 min: ", "J2 max: ", "J3 min: ", "J3 max: ", 
                            "J4 min: ", "J4 max: ", "J5 min: ", "J5 max: ", "J6 min: ", "J6 max: ",]
        self.settings.append(CreateFields(rows=12, columns=1, row_names=setting_names, title="Max movement joints", url = URL_HELP_MAX_MOVE, times_nr_joints=2))
        
        
        
        setting_names = ["Pos S1: ", "Pos S2: ", "Pos S3: ", "Pos S4: ", "Pos S5: ", "Pos S6: "]
        self.settings.append(CreateFields(rows=6, columns=1, row_names=setting_names, title="Posistion switch", url = URL_HELP_LIM_POS, times_nr_joints=1))

        setting_names = ["step_deg_J1: ", "step_deg_J2: ", "step_deg_J3: ", "step_deg_J4: ", "step_deg_J5: ", "step_deg_J6: "]
        self.settings.append(CreateFields(rows=6, columns=1, row_names=setting_names, title="step deg", url = URL_HELP_STEPS_SPEED, times_nr_joints=1))

        setting_names = ["Direction J1: ", "Direction J2: ", "Direction J3: ", "Direction J4: ", "Direction J5: ", "Direction J6: ",]
        self.settings.append(CreateFields(rows=6, columns=1, row_names=setting_names, title="direction of the joints", url = URL_HELP_JOINT_DIR, times_nr_joints=1))
            
        setting_names = ["J1 max vel (deg/s)", "J1 max acc","J2 max vel (deg/s)", "J2 max acc","J3 max vel (deg/s)", "J3 max acc",
                                 "J4 max vel (deg/s)", "J4 max acc","J5 max vel (deg/s)", "J5 max acc","J6 max vel (deg/s)", "J6 max acc",]
        self.settings.append(CreateFields(rows=12, columns=1, row_names=setting_names, title="max speed/ acceleration", url = URL_HELP_STEPS_SPEED, times_nr_joints=2))
                   
        setting_names = ["Joint 1","Move to","Joint 2","Move to","Joint 3","Move to","Joint 4","Move to","Joint 5","Move to","Joint 6","Move to"] 
        self.settings.append(CreateFields(rows=12, columns=1, row_names=setting_names, title="Homing order", url = URL_HOME_ORDER, times_nr_joints=2))
                        
        setting_names_Y = ["Joint 1","Joint 2","Joint 3","Joint 4","Joint 5","Joint 6","Joint 7"] 
        setting_names_X = ["a", "alfpa", "d", "delta"]
        self.settings.append(CreateFields(rows=6, columns=4, row_names=setting_names_Y, title="DH - parameters", url = URL_HELP_DH_PARAM, column_names=setting_names_X, times_nr_joints=1))

        for setting in self.settings:
            self.layout_scroll.addWidget(setting)


        
    def checkbox_toggled(self):
        if self.entry_nr_joints.text() == "3" and self.checkbox.isChecked():
            self.Extra_Linkage = 1
        else:
            self.Extra_Linkage = 0
            self.checkbox.setChecked(False)
                          
        

    
class CreateFields(QWidget):
    def __init__ (self, rows = None, columns = None, row_names = None,  title=None, url=None ,column_names=None, CheckBoxPin=None, times_nr_joints=None):
        super().__init__()
        self.layout = QGridLayout(self)
        self.setStyleSheet(style_widget)

        self.rows = rows
        self.columns = columns
        self.title = title
        
        self.entry_boxes = []
        self.frames = []
        self.labels = []
        self.times_nr_joints = times_nr_joints
        
        self.row_names = row_names
        self.column_names = column_names
        self.IOCheckBox = False

        if title != "":
            frame = QWidget(self)
            layout_title = QHBoxLayout()
            layout_title.setAlignment(Qt.AlignLeft)
            frame.setLayout(layout_title)
            self.layout.addWidget(frame)

            button = QPushButton("?")
            button.setStyleSheet(style_button_help)
            button.setFixedSize(20,20)
            button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
            layout_title.addWidget(button)
        
            label = QLabel(title)
            label.setStyleSheet(style_label_bold)
            layout_title.addWidget(label)

            self.checkbox = QCheckBox('IO')
        
            if CheckBoxPin:       
                self.checkbox.setStyleSheet(style_checkbox)             
                self.checkbox.setChecked(False)  # Set the initial state of the checkbox
                layout_title.addWidget(self.checkbox)   

        self.setLayout(self.layout)    

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
        self.frames = []
        self.entry_boxes = []
        self.labels = []
        
        # Create entry boxes
        if self.column_names:
            self.rows = self.rows + 1
            
        for i in range(self.rows):     
            frame = QWidget(self)
            layout_frame = QHBoxLayout()
            layout_frame.setContentsMargins(0,0,0,0)
            layout_frame.setAlignment(Qt.AlignLeft)
            frame.setLayout(layout_frame)
            self.layout.addWidget(frame) 
            self.frames.append(frame)

            row_entries = []
            
            if i == 0 and self.columns > 1:
                label = QLabel(" ")
                label.setStyleSheet(style_label)
                label.setFixedWidth(120)
                layout_frame.addWidget(label)
                for j in range(self.columns):
                    label = QLabel(self.column_names[j])
                    label.setStyleSheet(style_label)
                    label.setFixedWidth(80)
                    layout_frame.addWidget(label)
                    self.labels.append(label)
            else:
                if self.columns == 1: 
                    label = QLabel(self.row_names[i])
                    label.setStyleSheet(style_label)
                    label.setFixedWidth(120)
                    self.labels.append(label)
                    layout_frame.addWidget(label)
                    
                    entry = QLineEdit()
                    entry.setFixedWidth(80)
                    entry.setStyleSheet(style_entry)
                    layout_frame.addWidget(entry)
                    
                    self.entry_boxes.append(entry)
        
                else:
                    label = QLabel(self.row_names[i-1])
                    label.setFixedWidth(120)
                    label.setStyleSheet(style_label)
                    layout_frame.addWidget(label)
                    self.labels.append(label)
                    
                    for j in range(self.columns):
                        entry = QLineEdit()
                        entry.setFixedWidth(80)
                        entry.setStyleSheet(style_entry)
                        layout_frame.addWidget(entry)
                        row_entries.append(entry)   

                    self.entry_boxes.append(row_entries)
        
        if self.column_names:
            self.rows = self.rows - 1


 
    def DeleteFields(self):   
        for frame in self.frames:
            self.layout.removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater()
            frame = None

        self.frames = []
        self.frames_layout = []
        
