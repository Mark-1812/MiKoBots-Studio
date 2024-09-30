from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.core.api import send_pos_robot
from backend.core.api import simulation_move_gui
from backend.core.api import change_tool

class ControlField(QWidget):   
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        self.ButtonsJoint = []
        self.ButtonsAxis = []
        self.ButtonsMove = []
        
        self.simulation = False
        
        self.createFrames(frame_layout)
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_change_labels_control", self.ChangeTitles)
        
        event_manager.subscribe("request_label_pos_axis", self.ChangeAxisLabels)
        event_manager.subscribe("request_label_pos_joint", self.ChangeJointLabels)
        
        event_manager.subscribe("request_create_buttons_joint", self.CreateButtonsJoint)
        event_manager.subscribe("request_delete_buttons_joint", self.DeleteButtonsJoint)
       
        event_manager.subscribe("request_create_buttons_axis", self.CreateButtonsAxis)
        event_manager.subscribe("request_delete_buttons_axis", self.DeleteButtonsAxis)
        
        event_manager.subscribe("request_create_buttons_move", self.CreateButtonsMove)
        event_manager.subscribe("request_delete_buttons_move", self.DeleteButtonsMove)
  
        event_manager.subscribe("request_add_tool_combo", self.AddToolCombo)
        event_manager.subscribe("request_delete_tool_combo", self.DeleteToolsCombo)
        event_manager.subscribe("request_set_tool_combo", self.SetToolCombo)
        event_manager.subscribe("request_enable_tool_combo", self.EnableToolCombo)
        event_manager.subscribe("request_set_tool_pos", self.SetToolPos)
        event_manager.subscribe("request_set_tool_state", self.SetToolState)
        
        event_manager.subscribe("request_check_io_state", self.CheckIOState)
        event_manager.subscribe("request_set_io_state", self.SetIoState)
            
    def createFrames(self, layout):
        frame_joint_jog = QFrame()
        frame_joint_jog.setMaximumHeight(230)
        frame_joint_jog.setMinimumWidth(180)
        frame_joint_jog.setMaximumWidth(210)
        layout.addWidget(frame_joint_jog, 0, 1) 

        frame_axis_jog = QFrame()
        frame_axis_jog.setMaximumHeight(230)
        frame_axis_jog.setMinimumWidth(180)
        frame_axis_jog.setMaximumWidth(210)
        layout.addWidget(frame_axis_jog, 0, 2)  

        frame_move = QFrame()
        frame_move.setMaximumHeight(230)
        frame_move.setMinimumWidth(180)
        frame_move.setMaximumWidth(210)
        layout.addWidget(frame_move, 0, 3) 

        frame_tool = QFrame()
        frame_tool.setMaximumHeight(230)
        frame_tool.setMinimumWidth(180)
        frame_tool.setMaximumWidth(210)
        layout.addWidget(frame_tool, 0, 4) 

        frame_io = QFrame()
        frame_io.setMaximumHeight(230)
        frame_io.setMinimumWidth(180)
        frame_io.setMaximumWidth(210)
        layout.addWidget(frame_io, 0, 5) 
        
        self.frameMove(frame_move)
        self.FrameTool(frame_tool)
        self.FrameJointJog(frame_joint_jog)
        self.FrameAxisJog(frame_axis_jog)
        self.FrameIo(frame_io)    
 
    # Tool       
    def FrameTool(self, frame):
        layout = QGridLayout(frame)
        
        self.LABEL_TOOL = QLabel("Tool")
        self.LABEL_TOOL.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.LABEL_TOOL.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.LABEL_TOOL.setMaximumHeight(20)
        layout.addWidget(self.LABEL_TOOL, 0, 1, 1, 3)
               
        label = QLabel("Servo tool position:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        layout.addWidget(label, 1, 1, 1, 3)        

        Gripper_min_button = QPushButton("-")
        Gripper_min_button.setMaximumWidth(50)
        Gripper_min_button.setMinimumWidth(20)
        layout.addWidget(Gripper_min_button, 2, 1)
        Gripper_min_button.clicked.connect(lambda: self.MotionWidget.PosTool(0))

        self.LABEL_TOOL_POS = QLabel("pos: 0")
        self.LABEL_TOOL_POS.setAlignment(Qt.AlignCenter)
        self.LABEL_TOOL_POS.setFixedWidth(80)
        layout.addWidget(self.LABEL_TOOL_POS, 2, 2)

        Gripper_plus_button = QPushButton("+")
        Gripper_plus_button.setMinimumWidth(20)
        Gripper_plus_button.setMaximumWidth(50)
        layout.addWidget(Gripper_plus_button, 2, 3)
        Gripper_plus_button.clicked.connect(lambda: self.MotionWidget.PosTool(1))

        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout.addItem(spacer)

        label = QLabel("Relay tool state:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        layout.addWidget(label, 3, 1, 1, 3) 

        self.CHECKBOX_TOOL_OUTPUT = QCheckBox("ON / OFF")
        layout.addWidget(self.CHECKBOX_TOOL_OUTPUT, 4, 1, 1, 3)


        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 5, 0)
        
        label = QLabel("Current tool:")
        label.setStyleSheet("QLabel {font-size: 12px; font-weight: bold;}")
        layout.addWidget(label, 6, 1, 1, 3) 


        self.TOOL_COMBO = QComboBox()
        self.TOOL_COMBO.setStyleSheet("background-color: " + "white")
        self.TOOL_COMBO.setStyleSheet("QComboBox {text-align: center;}")
        self.TOOL_COMBO.setMaximumWidth(150)
        
        self.TOOL_COMBO.currentIndexChanged.connect(lambda index: change_tool(index))
        
        layout.addWidget(self.TOOL_COMBO, 7, 1, 1, 3)

        spacer_widget = QWidget()
        layout.addWidget(spacer_widget, 0, layout.columnCount(), layout.rowCount(), 1) 

    def AddToolCombo(self, tool):
        self.TOOL_COMBO.addItem(tool)  
        
    def DeleteToolsCombo(self):
        self.TOOL_COMBO.clear()

    def SetToolCombo(self, tool):
        self.TOOL_COMBO.setCurrentIndex(tool)
        
    def EnableToolCombo(self, enable):
        if enable:
            self.TOOL_COMBO.setEnabled(True)
        else:
            self.TOOL_COMBO.setEnabled(False)

    def SetToolPos(self, pos):
        self.LABEL_TOOL_POS.setText(f"Pos: {pos}")

    def SetToolState(self, state):
        self.CHECKBOX_TOOL_OUTPUT.setChecked(state) 
         
    # Frame move    
    def frameMove(self,frame):
        self.layout_move = QGridLayout(frame)
        
        self.LABEL_MOVE = QLabel("Move")
        self.LABEL_MOVE.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.LABEL_MOVE.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.LABEL_MOVE.setMaximumHeight(20)
        self.layout_move.addWidget(self.LABEL_MOVE, 0, 1, 1, 2)
                
        button = QPushButton("Go to pos")
        button.setMaximumWidth(95)
        button.clicked.connect(lambda: self.ButtonMove())
        self.layout_move.addWidget(button, 1,1,1,2) 
        
        self.CHECKBOX_MOVE = QCheckBox("Switch to joint")
        self.CHECKBOX_MOVE.setChecked(False)  # Set the initial state of the checkbox
        self.layout_move.addWidget(self.CHECKBOX_MOVE,2,1,1,2)
        self.CHECKBOX_MOVE.stateChanged.connect(lambda state: self.SwitchJointAxis(state))
 
 
        spacer_widget = QWidget()
        self.layout_move.addWidget(spacer_widget, 0, 0, self.layout_move.rowCount(), 1)
        
        spacer_widget = QWidget()
        self.layout_move.addWidget(spacer_widget, 0, self.layout_move.columnCount(), self.layout_move.rowCount(), 1) 
 
    def CreateButtonsMove(self, nr, name_joint, name_axis):
        self.ButtonsMove = []
        self.name_joint = name_joint
        self.name_axis = name_axis
        self.nr_of_joints = nr
        
        for i in range(self.nr_of_joints):
            label = QLabel(f"{self.name_joint[i]}:")
            label.setStyleSheet("font-weight: bold;")
            label.setMaximumWidth(20)
            
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            
            entry = QLineEdit()
            entry.setMaximumWidth(40)
            entry.setValidator(validator)
            entry.setText(str(round(var.POS_AXIS_SIM[i])))
            
            self.ButtonsMove.append([label,entry])
            
            self.layout_move.addWidget(label, i + 3, 1)
            self.layout_move.addWidget(entry, i + 3, 2)
    
    def DeleteButtonsMove(self):
        for i in range(len(self.ButtonsMove)):
            for j in range(2):
                self.ButtonsMove[i][j].setParent(None)
                self.ButtonsMove[i][j].deleteLater()
 
    def SwitchJointAxis(self, state):
        if state:
            self.CHECKBOX_MOVE.setText("Switch to axis")
            for i in range(self.nr_of_joints):
                self.ButtonsMove[i][0].setText(self.name_joint[i])
                if var.SIM:
                    # get the position of the sim axis 
                    pos = send_pos_robot(True)
                    self.ButtonsMove[i][1].setText(str(round(pos[0][i],2)))
                else:
                    # get the position of the axis 
                    pos = send_pos_robot(False)
                    self.ButtonsMove[i][1].setText(str(round(pos[0][i])))
                
        else:
            self.CHECKBOX_MOVE.setText("Switch to joint")
            for i in range(self.nr_of_joints):
                self.ButtonsMove[i][0].setText(self.name_axis[i])
                if var.SIM:
                    # get the position of the joint
                    pos = send_pos_robot(True)
                    self.ButtonsMove[i][1].setText(str(round(pos[1][i],2)))
                else:
                    # get the position of the joint
                    pos = send_pos_robot(False)
                    self.ButtonsMove[i][1].setText(str(round(pos[1][i])))        
    
    def ButtonMove(self):
        posJoint = [0]* self.nr_of_joints
        
        for i in range(self.nr_of_joints):
            posJoint[i] = self.ButtonsMove[i][1].text()
            
        print(posJoint)
        
        if self.simulation:
            if self.CHECKBOX_MOVE.isChecked():
                # joints
                simulation_move_gui(posJoint, "MoveJoint")
            else:
                # axis
                simulation_move_gui(posJoint, "MoveJ")
        else:
            
            pass  
    
    # Frame joint jog
    def FrameJointJog(self, frame):   
        self.layout_joint_jog = QGridLayout(frame)
        
        self.LABEL_JOG_JOINT = QLabel("Jog Joint")
        self.LABEL_JOG_JOINT.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.LABEL_JOG_JOINT.setMaximumHeight(20)
        self.LABEL_JOG_JOINT.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout_joint_jog.addWidget(self.LABEL_JOG_JOINT, 0, 0, 1, 3)

    def CreateButtonsJoint(self, nr):
        self.ButtonsJoint = []
        self.nr_of_joints = nr
        for i in range(nr):
            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 0))
            button_minus.setMaximumWidth(50)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet("font-weight: bold;")

            label = QLabel(f"{var.NAME_JOINTS[i]} {var.POS_JOINT[i]} {var.UNIT_JOINT[i]}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)

            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 1))
            button_plus.setMaximumWidth(50)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet("font-weight: bold;")
            
            self.ButtonsJoint.append([button_minus,label,button_plus])
            
            self.layout_joint_jog.addWidget(button_minus, i+1, 0)
            self.layout_joint_jog.addWidget(label, i+1, 1)
            self.layout_joint_jog.addWidget(button_plus, i+1, 2)
    
    def DeleteButtonsJoint(self):
        for i in range(len(self.ButtonsJoint)):
            for j in range(3):
                self.ButtonsJoint[i][j].setParent(None)
                self.ButtonsJoint[i][j].deleteLater()

    def ChangeJointLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.ButtonsJoint[i][1].setText(f"{name[i]}: {round(pos[i],2)} {unit[i]}")
 
    def ButtonJointMove(self, joint, dir):
        posJoint = [0] * self.nr_of_joints
        if self.simulation:
            if dir == 1:
                posJoint[joint] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posJoint[joint] = -1 * event_manager.publish("request_get_jog_distance")[0]
            simulation_move_gui(posJoint, "jogJ")
        else:
            pass
   
    # Frame axis jog             
    def FrameAxisJog(self, frame):  
        self.layout_axis_jog = QGridLayout(frame)
        
        self.LABEL_JOG_AXIS = QLabel("Jog Axis")
        self.LABEL_JOG_AXIS.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.LABEL_JOG_AXIS.setMaximumHeight(20)
        self.LABEL_JOG_AXIS.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout_axis_jog.addWidget(self.LABEL_JOG_AXIS, 0, 0, 1, 3)
            
    def CreateButtonsAxis(self, nr):
        self.ButtonsAxis = []
        for i in range(nr):
            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 0))
            button_minus.setMaximumWidth(50)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet("font-weight: bold;")
            
            label = QLabel(f"{var.NAME_AXIS[i]} {var.POS_AXIS[i]} {var.UNIT_AXIS[i]}")
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)
            
            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 1))
            button_plus.setMaximumWidth(50)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet("font-weight: bold;")
            
            self.ButtonsAxis.append([button_minus,label,button_plus])
            
            self.layout_axis_jog.addWidget(button_minus, i+1, 0)
            self.layout_axis_jog.addWidget(label, i+1, 1) 
            self.layout_axis_jog.addWidget(button_plus, i+1, 2)

    def DeleteButtonsAxis(self):
        for i in range(len(self.ButtonsAxis)):
            for j in range(3):
                self.ButtonsAxis[i][j].setParent(None)
                self.ButtonsAxis[i][j].deleteLater()

    def ChangeAxisLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.ButtonsAxis[i][1].setText(f"{name[i]}: {round(pos[i])} {unit[i]}")

    def ButtonAxisMove(self, axis, dir):
        posAxis = [0]*6
        if self.simulation:
            if dir == 1:
                posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posAxis[axis] = -1 * event_manager.publish("request_get_jog_distance")[0]
            print(posAxis)
            simulation_move_gui(posAxis, "OffsetJ")
        else:
            pass          

    # Frame IO 
    def FrameIo(self, frame):
        layout = QGridLayout(frame)
        
        self.LABEL_IO = QLabel("IO")
        self.LABEL_IO.setStyleSheet("QLabel {font-size: 16px; font-weight: bold;}")
        self.LABEL_IO.setMaximumHeight(20)
        self.LABEL_IO.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.LABEL_IO, 0, 0, 1, 2)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: lightgray;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget) 
        
        self.CHECKBOX_IO_INPUT = []
        self.CHECKBOX_IO_OUTPUT = []
        
        for i in range(10):
            label = QLabel(f"IO pin {i}")
            scroll_layout.addWidget(label, 1 + i, 0)
            
            checkbox = QCheckBox("IN")
            checkbox.setStyleSheet(            
                "QCheckBox { background-color: lightgray; }"
                "QCheckBox::indicator { border-radius: 5px; }"
                "QCheckBox::indicator:checked { background-color: green; }"
                "QCheckBox::indicator:unchecked { background-color: white; }"
                )
            scroll_layout.addWidget(checkbox, 1 + i, 2)
            self.CHECKBOX_IO_INPUT.append(checkbox)
            
            checkbox = QCheckBox("OUT")
            checkbox.setStyleSheet(            
                "QCheckBox { background-color: lightgray; }"
                "QCheckBox::indicator { border-radius: 5px; }"
                "QCheckBox::indicator:checked { background-color: green; }"
                "QCheckBox::indicator:unchecked { background-color: white; }"
                )
            scroll_layout.addWidget(checkbox, 1 + i, 3)
            self.CHECKBOX_IO_OUTPUT.append(checkbox)
          
        scroll.setWidget(scroll_widget)
            
        layout.addWidget(scroll)     
        #self.setLayout(layout)
      
    def CheckIOState(self, io_number):
        if self.CHECKBOX_IO_INPUT[io_number].isChecked():
            return True
        else:
            return False
        
    def SetIoState(self, io_number, state):
        self.CHECKBOX_IO_OUTPUT[io_number].setChecked(state)
            
            
      
      
    def ChangeTitles(self, sim):
        if sim:
            self.simulation = True
            self.LABEL_JOG_JOINT.setText("Jog Joint (sim)")
            self.LABEL_JOG_AXIS.setText("Jog Axis (sim)")
            self.LABEL_MOVE.setText("Move (sim)")
            self.LABEL_TOOL.setText("Tool (sim)")
            self.LABEL_IO.setText("IO (sim)")  
        else:
            self.simulation = False
            self.LABEL_JOG_JOINT.setText("Jog Joint")
            self.LABEL_JOG_AXIS.setText("Jog Axis")
            self.LABEL_MOVE.setText("Move")
            self.LABEL_TOOL.setText("Tool")
            self.LABEL_IO.setText("IO")      
            
