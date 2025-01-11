from PyQt5.QtWidgets import QFormLayout, QTableWidget, QTableWidgetItem, QLabel, QSpinBox, QLabel, QApplication, QPushButton, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QTextCharFormat, QTextCursor, QColor, QDoubleValidator, QDesktopServices

from gui.style import *

from backend.core.event_manager import event_manager


class RobotSettings(QFrame):   
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QGridLayout(self) 

        self.Extra_Linkage = 0
        
        self.joint_frames = []
        
        self.json_data = {}
        self.nr_of_joints = 0
        
        self.subscribeToEvents()
     
        self.GUI()
    
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_set_robot_settings", self.SetSettings)
        event_manager.subscribe("request_get_robot_settings", self.extractDataToJson)

    def SetSettings(self, data):

        self.json_data = data
  
        robot_name = self.json_data.get("Set_robot_name")[0]
        self.robot_name.setText(robot_name)
        
        
        self.nr_of_joints = int(self.json_data.get("Set_number_of_joints")[0])
        self.combo_box_nr_joints.setCurrentText(str(self.nr_of_joints))

        self.changeNumberJoints(self.nr_of_joints)  
        
        # set the IO pins
        io_pins = self.json_data.get("Set_io_pin")[0]
        for row, value in enumerate(io_pins):
            if row < len(self.io_fields):
                self.io_fields[row].setText(value)
                
        if self.json_data.get("Set_io_pin")[1] == "IO":
            self.checkbox_enable_io.setChecked(True)
        else:
            self.checkbox_enable_io.setChecked(False)

   
        # set the tool pins
        tool_pins = self.json_data.get("Set_tools")[0]
        for row, value in enumerate(tool_pins):
            if row < len(self.tool_fields):
                self.tool_fields[row].setText(value)
                
        if self.json_data.get("Set_tools")[1] == "IO":
            self.checkbox_enable_tool.setChecked(True)
        else:
            self.checkbox_enable_tool.setChecked(False)
            

                
        # set extra linkage
        if self.nr_of_joints == 3 and self.json_data.get("Set_extra_joint")[0] == 1:
            self.checkbox_link.setChecked(True)
        else:
            self.checkbox_link.setChecked(False)
    
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
        
        self.combo_box_nr_joints = QComboBox(self)
        self.combo_box_nr_joints.addItems(["3", "5", "6"])  # Add items to the combo box
        self.combo_box_nr_joints.currentTextChanged.connect(lambda text: self.changeNumberJoints(int(text)))
        self.combo_box_nr_joints.setStyleSheet(style_combo)
        
        layout_frame.addWidget(self.combo_box_nr_joints, 2, 1)
        
        label = QLabel("At the moment the software only works with a robot with 6 joints")
        label.setStyleSheet(style_label)
        layout_frame.addWidget(label, 3, 0, 1, 3)    
           
        self.checkbox_link = QCheckBox('Extra linkage to keep the tool parrallel to the floor (only for 3 axis robot arm (RRR))', frame)                
        self.checkbox_link.setChecked(False)  # Set the initial state of the checkbox
        self.checkbox_link.stateChanged.connect(self.changeExtraLink)
        self.checkbox_link.setStyleSheet(style_checkbox)
        layout_frame.addWidget(self.checkbox_link, 4, 0, 1, 2)
        self.checkbox_link.hide()
        
        self.CreateIOPinsettings()
        self.CreateToolPinsettings()
        
        
    def changeExtraLink(self, state):
        if state:
            self.createDHTable(self.nr_of_joints + 1, self.json_data)
        else:
            self.createDHTable(self.nr_of_joints, self.json_data)
        
    def changeNumberJoints(self, number):
        self.nr_of_joints = number
                
        if number == 3:
            self.checkbox_link.show()
            # give an option for the extra linkage
        else:
            self.checkbox_link.hide()
                
                
        self.CreateJointFields(number, self.json_data)
        self.createDHTable(number, self.json_data)
        
        try:
            joint_types = self.json_data.get("Set_motor_type")[0]
            for i in range(self.nr_of_joints):
                if joint_types[i] == "1":
                    self.joint_frames[i].combo_box.setCurrentText("Servo")
                else: 
                    self.joint_frames[i].combo_box.setCurrentText("Stepper motor")
        except:
            pass
                    
        
    def CreateIOPinsettings(self):
        frame = QFrame(self.scroll_widget)
        self.layout_scroll.addWidget(frame)
        layout_frame = QGridLayout()  # Vertical layout for better organization
        frame.setLayout(layout_frame)
        
        self.checkbox_enable_io = QCheckBox("IO board", self)
        self.checkbox_enable_io.setStyleSheet(style_checkbox)
        layout_frame.addWidget(self.checkbox_enable_io)
        
        self.io_fields = []  # Store line edits for IO pins
        for row in range(10):
            label = QLabel(f"IO Pin {row + 1}:", self)
            label.setStyleSheet(style_label)
            label.setFixedWidth(140)
            line_edit = QLineEdit(self)
            line_edit.setFixedWidth(80)
            line_edit.setStyleSheet(style_entry)
            self.io_fields.append(line_edit)
            
            # Add label and line edit to grid layout
            layout_frame.addWidget(label, row+1, 0, alignment=Qt.AlignLeft)  
            layout_frame.addWidget(line_edit, row+1, 1, alignment=Qt.AlignLeft)  
            
        layout_frame.setColumnStretch(2, 1) 
        
    def CreateToolPinsettings(self):
        frame = QFrame(self.scroll_widget)
        self.layout_scroll.addWidget(frame)
        layout_frame = QGridLayout()  # Vertical layout for better organization
        frame.setLayout(layout_frame)
        
        self.checkbox_enable_tool = QCheckBox("IO board", self)
        self.checkbox_enable_tool.setStyleSheet(style_checkbox)
        layout_frame.addWidget(self.checkbox_enable_tool)
        
        self.tool_fields = []  # Store line edits for IO pins
        for row in range(5):
            label = QLabel(f"Tool Pin {row + 1}:", self)
            label.setStyleSheet(style_label)
            label.setFixedWidth(140)
            line_edit = QLineEdit(self)
            line_edit.setFixedWidth(80)
            line_edit.setStyleSheet(style_entry)
            self.tool_fields.append(line_edit)
            
            # Add label and line edit to grid layout
            layout_frame.addWidget(label, row+1, 0, alignment=Qt.AlignLeft)
            layout_frame.addWidget(line_edit, row+1, 1, alignment=Qt.AlignLeft)       
   
        layout_frame.setColumnStretch(2, 1) 
  

        
    def createDHTable(self, num_rows, json_data):
        # Remove the existing table frame if it exists
        if hasattr(self, "dh_table_frame"):
            self.layout_scroll.removeWidget(self.dh_table_frame)
            self.dh_table_frame.setParent(None)
            self.dh_table_frame.deleteLater()
            self.dh_table_frame = None

        # Create a new frame for the DH table
        self.dh_table_frame = QFrame(self)
        layout_frame = QVBoxLayout(self.dh_table_frame)

        # Add a label
        label = QLabel("DH Parameters (α, a, d, θ):")
        label.setStyleSheet(style_label_title)
        layout_frame.addWidget(label)

        # Create the table widget
        self.dh_table = QTableWidget(num_rows, 4)  # 4 columns for α, a, d, θ
        self.dh_table.setStyleSheet(style_table)
        self.dh_table.setHorizontalHeaderLabels(["α (alpha)", "a", "d", "θ (theta)"])
        
        self.dh_table.resizeColumnsToContents()
        self.dh_table.resizeRowsToContents()
        
        header_height = self.dh_table.horizontalHeader().height()
        row_height = sum(self.dh_table.rowHeight(row) for row in range(self.dh_table.rowCount()))
        vertical_scrollbar_width = self.dh_table.verticalScrollBar().width()
        
        total_height = header_height + row_height + 2  # Add 2 for borders
        total_width = (
            sum(self.dh_table.columnWidth(col) for col in range(self.dh_table.columnCount())) +
            vertical_scrollbar_width + 2  # Add 2 for borders
        )

        # Set the size of the table
        self.dh_table.setFixedHeight(total_height)
        self.dh_table.setFixedWidth(320)

        layout_frame.addWidget(self.dh_table)

        # Add the frame to the main layout
        self.layout_scroll.addWidget(self.dh_table_frame)
        
        dh_parameters = json_data.get("Set_dh_par")[0]
        
        for row, parameters in enumerate(dh_parameters):
            for col, value in enumerate(parameters):
                item = QTableWidgetItem(value)
                self.dh_table.setItem(row, col, item)

        self.dh_table.setColumnWidth(0, 80)
        self.dh_table.setColumnWidth(1, 80)
        self.dh_table.setColumnWidth(2, 80)
        self.dh_table.setColumnWidth(3, 80)
        
    def setupRowInput(self):
        self.row_input = QSpinBox(self)
        self.row_input.setMinimum(1)
        self.row_input.setMaximum(20)  # Adjust maximum as needed
        self.row_input.valueChanged.connect(lambda value: self.createDHTable(value))
        self.layout_scroll.addWidget(self.row_input)


        

    def CreateJointFields(self, number, json_data):
        # Delete all the current fields
        while self.joint_frames:
            frame = self.joint_frames.pop()
            self.layout_scroll.removeWidget(frame)
            frame.setParent(None)
            frame.deleteLater()
            
        width_line = 80
        width_text = 160

        # Create new frames
        for i in range(number):
            # Create a frame
            frame = QFrame(self.scroll_widget)
            self.layout_scroll.addWidget(frame)
            layout_frame = QVBoxLayout()  # Vertical layout for better organization
            frame.setLayout(layout_frame)
            
            title = QLabel(f"Joint {i+1}")
            title.setStyleSheet(style_label_title)
            

            # Create a ComboBox for joint type
            combo_box = QComboBox(self)
            combo_box.addItems(["Stepper motor", "Servo"])  # Add items to the combo box
            combo_box.setStyleSheet(style_combo)
            combo_box.setMaximumWidth(200)

            # Create a container for common settings
            common_layout = QFormLayout()
            layout_frame.addLayout(common_layout)

            # Add common settings (Max & min movement, Max Speed, Acceleration)
            dir_joint_input = QLineEdit()
            dir_joint_input.setMaximumWidth(width_line)
            dir_joint_input.setStyleSheet(style_entry)
            label = QLabel("Joint direction")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, dir_joint_input)
            
            max_movement_input = QLineEdit()
            max_movement_input.setMaximumWidth(width_line)
            max_movement_input.setStyleSheet(style_entry)
            label = QLabel("Max movement (deg)")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, max_movement_input)
            
            min_movement_input = QLineEdit()
            min_movement_input.setMaximumWidth(width_line)
            min_movement_input.setStyleSheet(style_entry)
            label = QLabel("Min movement (deg)")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, min_movement_input)
            
            max_speed_input = QLineEdit()
            max_speed_input.setMaximumWidth(width_line)
            max_speed_input.setStyleSheet(style_entry)
            label = QLabel("Max Speed (deg/s):")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, max_speed_input)

            max_acceleration_input = QLineEdit()
            max_acceleration_input.setMaximumWidth(width_line)
            max_acceleration_input.setStyleSheet(style_entry)
            label = QLabel("Max Acceleration (deg/s^2):")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, max_acceleration_input)
            
            home_order_input = QLineEdit()
            home_order_input.setMaximumWidth(width_line)
            home_order_input.setStyleSheet(style_entry)
            label = QLabel("Home order:")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, home_order_input)
            
            home_position_input = QLineEdit()
            home_position_input.setMaximumWidth(width_line)
            home_position_input.setStyleSheet(style_entry)
            label = QLabel("Move to .. after homing:")
            label.setFixedWidth(width_text)
            label.setStyleSheet(style_label)
            common_layout.addRow(label, home_position_input)
            
            label = QLabel("Motor type specific settings")
            label.setStyleSheet(style_label_bold)
            common_layout.addRow(label)
            
            
            try:
                joint_type = self.json_data.get("Set_motor_type", [""] * number)[0][i]
                if joint_type == "1" or joint_type == 1:
                    combo_box.setCurrentText("Servo")
                else: 
                    combo_box.setCurrentText("Stepper motor")

                # set the values out of the Json 
                dir_joint = json_data.get("Set_dir_joints", [""] * number)[0][i]
                dir_joint_input.setText(dir_joint)
                
                max_movement = json_data.get("Set_max_pos", [""] * number)[0][i*2 + 1]
                max_movement_input.setText(max_movement)
                
                min_movement = json_data.get("Set_max_pos", [""] * number)[0][i*2]
                min_movement_input.setText(min_movement)
                
                max_speed = json_data.get("Set_speed", [""] * number)[0][i*2]
                max_speed_input.setText(max_speed)
                
                max_acceleration = json_data.get("Set_speed", [""] * number)[0][i*2 + 1]
                max_acceleration_input.setText(max_acceleration)
                
                home_order = json_data.get("Set_home_settings", [""] * number)[0][i*2]
                home_order_input.setText(home_order)
                
                home_position = json_data.get("Set_home_settings", [""] * number)[0][i*2 + 1]
                home_position_input.setText(home_position)
            except:
                pass

            type_specific_container = QWidget()  # Use a QWidget as a container
            type_specific_layout = QFormLayout(type_specific_container)  # Set layout to the container

            # Add the type-specific layout to the frame, aligned to the left
            layout_frame.addWidget(type_specific_container, alignment=Qt.AlignLeft)
            
            # Connect the combo box to update the type-specific settings
            combo_box.currentTextChanged.connect(
                lambda text, layout=type_specific_layout, idx=i: self.updateTypeSpecificSettings(
                    text, layout, json_data, idx
                )
            )

            if joint_type == "1" or joint_type == 1:
                self.addServoSettings(type_specific_layout, json_data, i)
            else: 
                self.addStepperSettings(type_specific_layout, json_data, i)


            # Add ComboBox to layout
            layout_frame.insertWidget(0, title)
            layout_frame.insertWidget(1, combo_box)

            # Store references for future updates
            frame.combo_box = combo_box
            frame.type_specific_layout = type_specific_layout
            self.joint_frames.append(frame)

    def updateTypeSpecificSettings(self, joint_type, type_specific_layout, json_data, index):
        # save the settings first
        self.extractDataToJson()
        
        # Clear type-specific settings
        while type_specific_layout.count():
            item = type_specific_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Add joint-specific settings
        if joint_type == "Stepper motor":
            self.addStepperSettings(type_specific_layout, json_data, index)
        elif joint_type == "Servo":
            self.addServoSettings(type_specific_layout, json_data, index)

    def addStepperSettings(self, layout, json_data, index):
        width_line = 80
        width_text = 140
        
        # Add settings specific to stepper motors
        pul_pin_input = QLineEdit()
        pul_pin_input.setMaximumWidth(width_line)
        pul_pin_input.setStyleSheet(style_entry)
        label = QLabel("PUL pin:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, pul_pin_input)
        
        dir_pin_input = QLineEdit()
        dir_pin_input.setMaximumWidth(width_line)
        dir_pin_input.setStyleSheet(style_entry)
        label = QLabel("DIR pin:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, dir_pin_input)
        
        switch_pin_input = QLineEdit()
        switch_pin_input.setMaximumWidth(width_line)
        switch_pin_input.setStyleSheet(style_entry)
        label = QLabel("Switch pin:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, switch_pin_input)
        
        switch_position_input = QLineEdit()
        switch_position_input.setMaximumWidth(width_line)
        switch_position_input.setStyleSheet(style_entry)
        label = QLabel("Switch position:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, switch_position_input)
        
        steps_input = QLineEdit()
        steps_input.setMaximumWidth(width_line)
        steps_input.setStyleSheet(style_entry)
        label = QLabel("Steps per revolution:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, steps_input)
        
        try:
            pul_pin = json_data.get("Set_motor_pin", [[""] * 6] * len(self.joint_frames))[0][index*2]
            pul_pin_input.setText(pul_pin)
            dir_pin = json_data.get("Set_motor_pin", [[""] * 6] * len(self.joint_frames))[0][index*2 +1]
            dir_pin_input.setText(dir_pin)
            switch_pin = json_data.get("Set_switch_pin", [[""] * 6] * len(self.joint_frames))[0][index]
            switch_pin_input.setText(switch_pin)
            switch_position = json_data.get("Set_lim_pos", [[""] * 6] * len(self.joint_frames))[0][index]
            switch_position_input.setText(switch_position)
            steps = json_data.get("Set_step_deg", [[""] * 6] * len(self.joint_frames))[0][index]
            steps_input.setText(steps)  # Join values for display
        except:
            pass

    def addServoSettings(self, layout, json_data, index):
        width_line = 80
        width_text = 140
        
        # Add settings specific to servos
        servo_pin_input = QLineEdit()
        servo_pin_input.setMaximumWidth(width_line)
        servo_pin_input.setStyleSheet(style_entry)
        label = QLabel("Servo pin:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, servo_pin_input)
        
        pulse_range_min_input = QLineEdit()
        pulse_range_min_input.setMaximumWidth(width_line)
        pulse_range_min_input.setStyleSheet(style_entry)
        label = QLabel("Pulse range min:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, pulse_range_min_input)
        
        pulse_range_max_input = QLineEdit()
        pulse_range_max_input.setMaximumWidth(width_line)
        pulse_range_max_input.setStyleSheet(style_entry)
        label = QLabel("Pulse range max:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, pulse_range_max_input)
        
        servo_range_input = QLineEdit()
        servo_range_input.setMaximumWidth(width_line)
        servo_range_input.setStyleSheet(style_entry)
        label = QLabel("Range deg:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, servo_range_input)
        
        zero_position_input = QLineEdit()
        zero_position_input.setMaximumWidth(width_line)
        zero_position_input.setStyleSheet(style_entry)
        label = QLabel("Zero position servo:")
        label.setFixedWidth(width_text)
        label.setStyleSheet(style_label)
        layout.addRow(label, zero_position_input)
            
        try:
            servo_pin = json_data.get("Set_servo_pin", [[""] * 6] * len(self.joint_frames))[0][index]
            servo_pin_input.setText(servo_pin)
            pulse_range_min = json_data.get("Set_servo_pulse", [[""] * 6] * len(self.joint_frames))[0][index*3+1]
            pulse_range_min_input.setText(pulse_range_min)
            pulse_range_max = json_data.get("Set_servo_pulse", [[""] * 6] * len(self.joint_frames))[0][index*3]
            pulse_range_max_input.setText(pulse_range_max)
            servo_range = json_data.get("Set_servo_pulse", [[""] * 6] * len(self.joint_frames))[0][index*3+2]
            servo_range_input.setText(servo_range)
            zero_position = json_data.get("Set_servo_position", [[""] * 6] * len(self.joint_frames))[0][index]
            zero_position_input.setText(zero_position)
        except:
            pass 
       

        
    def extractDataToJson(self):
        # Extract data from GUI to JSON format
        data = {
            ## general settings joints
            "Set_dir_joints": [[0]*self.nr_of_joints,""],
            "Set_max_pos": [[0]*self.nr_of_joints * 2,""], # minimum and maximum position of the joint
            "Set_speed": [[0]*self.nr_of_joints * 2,""], # vel and acceleration
            "Set_home_settings": [[0]*self.nr_of_joints * 2,""], # home order and position
            "Set_motor_type": [[0]*self.nr_of_joints,""], 
            
            ## stepper motor settings
            "Set_motor_pin":  [[0]*self.nr_of_joints*2,""],
            "Set_switch_pin": [[0]*self.nr_of_joints,""],
            "Set_lim_pos": [[0]*self.nr_of_joints,""],
            "Set_step_deg": [[0]*self.nr_of_joints,""],
                
            ## Servo settings
            "Set_servo_pin": [[0]*self.nr_of_joints,""],
            "Set_servo_pulse": [[0]*self.nr_of_joints*3,""],
            "Set_servo_position": [[0]*self.nr_of_joints,""],
            
            
            # other settings
            "Set_dh_par": [[[0]*10,[0]*5],""],
            "Set_io_pin": [[0]*10,""],
            "Set_tools": [[0]*6,""],
            "Set_robot_name": ["", ""],
            "Set_number_of_joints": ["", ""],
            "Set_extra_joint": ["", ""]
        }

        joint_nr = 0
        for frame in self.joint_frames:
            common_layout = frame.layout().itemAt(2).layout()  # Common settings layout
            type_specific_layout = frame.type_specific_layout  # Type-specific settings
            
            

            # Extract common settings
            data["Set_dir_joints"][0][joint_nr] = common_layout.itemAt(1).widget().text()
            
            # set the maximum and miminumem position of the joint
            data["Set_max_pos"][0][joint_nr * 2 + 1] = common_layout.itemAt(3).widget().text()
            data["Set_max_pos"][0][joint_nr * 2] = common_layout.itemAt(5).widget().text()
            
            # set the speed settings of the joint
            data["Set_speed"][0][joint_nr * 2] = common_layout.itemAt(7).widget().text()
            data["Set_speed"][0][joint_nr * 2 + 1] = common_layout.itemAt(9).widget().text()
            
            # set the homing settings of the joint
            data["Set_home_settings"][0][joint_nr * 2] = common_layout.itemAt(11).widget().text()
            data["Set_home_settings"][0][joint_nr * 2 + 1] = common_layout.itemAt(13).widget().text()

            # Extract joint type
            if frame.combo_box.currentText() == "Stepper motor":
                data["Set_motor_type"][0][joint_nr] = "0"
            elif frame.combo_box.currentText() == "Servo":
                data["Set_motor_type"][0][joint_nr] = "1"

            # Extract type-specific settings
            if frame.combo_box.currentText() == "Stepper motor":
                ## set motor pin
                data["Set_motor_pin"][0][joint_nr * 2] = type_specific_layout.itemAt(1).widget().text()
                data["Set_motor_pin"][0][joint_nr * 2 + 1] = type_specific_layout.itemAt(3).widget().text()
                
                ## set switch pin
                data["Set_switch_pin"][0][joint_nr] = type_specific_layout.itemAt(5).widget().text()

                ## set switch pin
                data["Set_lim_pos"][0][joint_nr] = type_specific_layout.itemAt(7).widget().text()
                
                # set step per degree
                data["Set_step_deg"][0][joint_nr] = type_specific_layout.itemAt(9).widget().text()
                
                
            elif frame.combo_box.currentText() == "Servo":
                # servo pin
                data["Set_servo_pin"][0][joint_nr] = type_specific_layout.itemAt(1).widget().text()
                
                ## set pulse range of servo
                data["Set_servo_pulse"][0][joint_nr * 3] = type_specific_layout.itemAt(5).widget().text()
                data["Set_servo_pulse"][0][joint_nr * 3 + 1] = type_specific_layout.itemAt(3).widget().text()
                data["Set_servo_pulse"][0][joint_nr * 3 + 2] = type_specific_layout.itemAt(7).widget().text()
                
                # set servo position 
                data["Set_servo_position"][0][joint_nr] = type_specific_layout.itemAt(9).widget().text()

            joint_nr += 1
            
            
        # extract the dh parameters
        dh_parameters = []
        for row in range(self.dh_table.rowCount()):
            parameters = []
            for col in range(self.dh_table.columnCount()):
                item = self.dh_table.item(row, col)
                parameters.append(item.text() if item else "")
            dh_parameters.append(parameters)
        
        data["Set_dh_par"][0] = dh_parameters
        
        # extract the IO pins
        io_pins = []
        for line_edit in self.io_fields:
            io_pins.append(line_edit.text())
        data["Set_io_pin"][0] = io_pins
        
        if self.checkbox_enable_io.isChecked():
            data["Set_io_pin"][1] = "IO"
        else:
            data["Set_io_pin"][1] = ""
            
        # extract the tool pins
        
        tool_pins = []
        for line_edit in self.io_fields:
            tool_pins.append(line_edit.text())
        data["Set_tools"][0] = io_pins
        
        if self.checkbox_enable_tool.isChecked():
            data["Set_tools"][1] = "IO"
        else:
            data["Set_tools"][1] = ""
            
        # extract the robot name
        data["Set_robot_name"][0] = self.robot_name.text()
        
        # extract the number of joints
        data["Set_number_of_joints"][0] = self.combo_box_nr_joints.currentText()
        
        # extract axtra joint info
        if self.checkbox_link.isChecked and self.nr_of_joints ==3:
            data["Set_extra_joint"][0] = 1
        else:
            data["Set_extra_joint"][0] = 0
        
        
        return data