from PyQt5.QtWidgets import QPushButton, QLabel, QHBoxLayout, QCheckBox, QLineEdit, QSpacerItem, QSizePolicy, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator, QDesktopServices

from gui.style import *

from backend.core.event_manager import event_manager

from backend.robot_management  import save_robot


URL_HELP_PINS = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-pins-esp32/"
URL_HELP_MAX_MOVE = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-max-movement/"
URL_HELP_LIM_POS = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/limit-switch-position/"
URL_HELP_STEPS_SPEED = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-step-per-degree/"
URL_HELP_JOINT_DIR = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/joint-direction/"
URL_HELP_DH_PARAM = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/set-dh-parameters/"
URL_HOME_ORDER = "https://mikobots.com/mikobots-studio/help/robot/robot-settings/homing-order/"

class RobotSettings:
    def __init__(self,  parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QVBoxLayout(self.parent_frame)

        
        self.settings_name = [
            'Set_robot_name','Set_number_of_joints','Set_extra_joint','Set_motor_pin', 'Set_switch_pin', 'Set_tools', 
            'Set_io_pin','Set_max_pos', 'Set_lim_pos', 'Set_step_deg', 
            'Set_dir_joints', 'Set_speed', 'Set_home_settings', 'Set_dh_par'               
            ] 
        self.settings = [] 
     
        self.Extra_Linkage = 0
     
        self.GUI()
        self.subscribeToEvents()

        self.parent_frame.setLayout(self.layout)
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_robot_settings", self.LoadSettings)
        event_manager.subscribe("request_get_robot_settings", self.GetSettings)
        event_manager.subscribe("request_create_settings_fields", self.CreateSettingsFields)
        event_manager.subscribe("request_delete_settings_fields", self.DeleteSettingsFields)
        
    def LoadSettings(self, settings_file):
        # Add the logic to load robot settings here
                   
        for i, setting in enumerate(self.settings):
            settings = settings_file[self.settings_name[i+3]]
            setting.set_values(settings[0])
            setting.set_IOCheckbox(settings[1])
        
        self.robot_name.setText(str(settings_file[self.settings_name[0]][0]))
        self.entry_nr_joints.setText(str(settings_file[self.settings_name[1]][0]))
        


        if settings_file[self.settings_name[2]][0] == 1:
            self.checkbox.setChecked(True)
            self.Extra_Linkage = 1
            self.settings[10].DeleteFields()
            self.settings[10].CreateFieldsSettings(int(settings_file[self.settings_name[1]][0]) + self.Extra_Linkage)
            settings = settings_file[self.settings_name[i+3]]
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
            settings_file[self.settings_name[i + 3]] = settings


            
        settings_file[self.settings_name[0]] = [self.robot_name.text(), ""]
        settings_file[self.settings_name[1]] = [self.entry_nr_joints.text(), ""]
        settings_file[self.settings_name[2]] = [self.Extra_Linkage, ""]
        
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
        # create a scroll area
        scroll_area = QScrollArea(self.parent_frame)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget(scroll_area)
        scroll_widget.setStyleSheet(style_widget)
        layout_scroll = QVBoxLayout(scroll_widget)
        layout_scroll.setContentsMargins(0, 0, 0, 0)
        layout_scroll.setSpacing(0)
        layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area) 

    
        
        frame = QFrame()
        layout_scroll.addWidget(frame)
        layout_frame = QGridLayout()
        frame.setLayout(layout_frame)

        button = QPushButton("Save robot")
        button.setStyleSheet(style_button_menu)
        button.setFixedWidth(100)
        layout_frame.addWidget(button, 0, 0)
        button.clicked.connect(lambda: save_robot(True))  

        label = QLabel("Robot name:")
        label.setStyleSheet(style_label)
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
        layout_frame.addWidget(self.checkbox, 4, 0, 1, 2)
        
        
        ### settings
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
        
        setting_names = ["PUL pin J1: ","DIR pin J1: ","PUL pin J2: ","DIR pin J2: ", "PUL pin J3: ","DIR pin J3: ",
                    "PUL pin J4: ","DIR pin J4: ", "PUL pin J5: ","DIR pin J5: ", "PUL pin J6: ","DIR pin J6: "]
        self.settings.append(CreateFields(frame, rows=12, columns=1, row_names=setting_names, title="<b>Motor pin<b>", url = URL_HELP_PINS, times_nr_joints=2))
       
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)       
 
        setting_names = ["S1 pin: ","S2 pin: ","S3 pin: ","S4 pin: ","S5 pin: ","S6 pin: "]
        self.settings.append(CreateFields(frame, rows=6, columns=1, row_names=setting_names, title="<b>Switch pin<b>", url = URL_HELP_PINS,  times_nr_joints=1))
       
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame) 

        setting_names = ["Tool 1: ","Tool 2: ","Tool 3: ","Tool 4: ", "Tool 5: "]
        self.settings.append(CreateFields(frame, rows=5, columns=1, row_names=setting_names, title="<b>Tool pin<b>", url = URL_HELP_PINS, CheckBoxPin=True))

        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)   
        
        setting_names = ["IO 1: ","IO 2: ","IO 3: ","IO 4: ", "IO 5: ","IO 6: ","IO 7: ","IO 8: ","IO 9: ", "IO 10: "]
        self.settings.append(CreateFields(frame, rows=10, columns=1, row_names=setting_names, title="<b>IO pin<b>", url = URL_HELP_PINS, CheckBoxPin=True))
           
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
           
        setting_names = ["J1 min: ", "J1 max: ", "J2 min: ", "J2 max: ", "J3 min: ", "J3 max: ", 
                            "J4 min: ", "J4 max: ", "J5 min: ", "J5 max: ", "J6 min: ", "J6 max: ",]
        self.settings.append(CreateFields(frame, rows=12, columns=1, row_names=setting_names, title="<b>Max movement joints<b>", url = URL_HELP_MAX_MOVE, times_nr_joints=2))

        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
        
        setting_names = ["Pos S1: ", "Pos S2: ", "Pos S3: ", "Pos S4: ", "Pos S5: ", "Pos S6: "]
        self.settings.append(CreateFields(frame, rows=6, columns=1, row_names=setting_names, title="<b>Posistion switch<b>", url = URL_HELP_LIM_POS, times_nr_joints=1))

        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
        
        setting_names = ["step_deg_J1: ", "step_deg_J2: ", "step_deg_J3: ", "step_deg_J4: ", "step_deg_J5: ", "step_deg_J6: "]
        self.settings.append(CreateFields(frame, rows=6, columns=1, row_names=setting_names, title="<b>step deg<b>", url = URL_HELP_STEPS_SPEED, times_nr_joints=1))

        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)       
                
        setting_names = ["Direction J1: ", "Direction J2: ", "Direction J3: ", "Direction J4: ", "Direction J5: ", "Direction J6: ",]
        self.settings.append(CreateFields(frame, rows=6, columns=1, row_names=setting_names, title="direction of the joints<b>", url = URL_HELP_JOINT_DIR, times_nr_joints=1))
         
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
                        
        setting_names = ["J1 max vel (deg/s)", "J1 max acc","J2 max vel (deg/s)", "J2 max acc","J3 max vel (deg/s)", "J3 max acc",
                                 "J4 max vel (deg/s)", "J4 max acc","J5 max vel (deg/s)", "J5 max acc","J6 max vel (deg/s)", "J6 max acc",]
        self.settings.append(CreateFields(frame, rows=12, columns=1, row_names=setting_names, title="max speed/ acceleration", url = URL_HELP_STEPS_SPEED, times_nr_joints=2))
                   
        frame = QWidget()
        frame.setMaximumWidth(300)
        layout_scroll.addWidget(frame)
                        
        setting_names = ["Joint 1","Move to","Joint 2","Move to","Joint 3","Move to","Joint 4","Move to","Joint 5","Move to","Joint 6","Move to"] 
        self.settings.append(CreateFields(frame, rows=12, columns=1, row_names=setting_names, title="<b>Homing order<b>", url = URL_HOME_ORDER, times_nr_joints=2))
                       
                     
        frame = QWidget()
        frame.setMaximumWidth(600)
        layout_scroll.addWidget(frame)
                        
        setting_names_Y = ["Joint 1","Joint 2","Joint 3","Joint 4","Joint 5","Joint 6","Joint 7"] 
        setting_names_X = ["a", "alfpa", "d", "delta"]
        self.settings.append(CreateFields(frame, rows=6, columns=4, row_names=setting_names_Y, title="<b>DH - parameters<b>", url = URL_HELP_DH_PARAM, column_names=setting_names_X, times_nr_joints=1))

                          
        


    
class CreateFields:
    def __init__ (self, parent_frame: QWidget, rows, columns, row_names,  title, url=None ,column_names=None, CheckBoxPin=None, times_nr_joints=None):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)

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
            frame = QWidget(self.parent_frame)
            layout_title = QHBoxLayout()
            frame.setLayout(layout_title)
            self.layout.addWidget(frame, 0, 0, 1, 2)

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
                
            self.row_index += 1     

        self.parent_frame.setLayout(self.layout)        

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

        self.spacer_widget = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.layout.addItem(self.spacer_widget, self.layout.rowCount(), 0, 1, self.layout.columnCount())

 
    def DeleteFields(self): 
        if self.columns == 1:      
            for i in range(len(self.entry_boxes)):
                self.layout.removeWidget(self.entry_boxes[i])
                self.entry_boxes[i].deleteLater()
                self.entry_boxes[i].setParent(None)
        else:
            for i in range(len(self.entry_boxes)):
                for j in range(4):
                    self.layout.removeWidget(self.entry_boxes[i][j])
                    self.entry_boxes[i][j].deleteLater()       
                    self.entry_boxes[i][j].setParent(None)
               
                
        for i in range(len(self.labels_row)):
            self.layout.removeWidget(self.labels_row[i])
            self.labels_row[i].deleteLater()
            self.labels_row[i].setParent(None)
            
        for i in range(len(self.labels_col)):
            self.layout.removeWidget(self.labels_col[i])
            self.labels_col[i].deleteLater()
            self.labels_col[i].setParent(None)
            
        if self.spacer_widget:  
            self.layout.removeItem(self.spacer_widget)

            

        self.entry_boxes = []
        self.labels_row = []
        self.labels_col = []