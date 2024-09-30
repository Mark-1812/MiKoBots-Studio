from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QCursor, QPixmap, QIcon, QDoubleValidator, QSyntaxHighlighter, QTextCharFormat, QColor, QTextCursor, QFont
from PyQt5.QtCore import Qt, QRegularExpression, QUrl, pyqtSignal
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.core.api import send_pos_robot
from backend.core.api import simulation_move_gui
from backend.core.api import change_tool
from backend.core.api import jog_joint
from backend.core.api import move_j
from backend.core.api import offset_j
from backend.core.api import get_tool_info
from backend.core.api import move_joint_pos

class ControlField(QWidget):   
    def __init__(self, frame):
        super().__init__()
        
        frame_layout = QGridLayout()
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        frame.setLayout(frame_layout)
        
        self.ButtonsJoint = []
        self.ButtonsAxis = []
        self.ButtonsMove = []
        
        self.space_widget_joint = None
        self.space_widget_axis = None
        self.space_widget_move = None
        
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
        event_manager.subscribe("request_set_io_state", self.SetIoStateOutput)
        event_manager.subscribe("request_set_io_state_input", self.SetIoStateInput)
            
    def createFrames(self, layout):
        frame_joint_jog = QFrame()
        frame_joint_jog.setMinimumWidth(200)
        frame_joint_jog.setStyleSheet(style_frame)
        layout.addWidget(frame_joint_jog, 0, 0) 
        
        space = QFrame()
        space.setFixedWidth(5)
        space.setStyleSheet("background-color: #E8E8E8;")
        layout.addWidget(space, 0, 1) 

        frame_axis_jog = QFrame()
        frame_axis_jog.setMinimumWidth(200)
        frame_axis_jog.setStyleSheet(style_frame)
        layout.addWidget(frame_axis_jog, 0, 2)  
        
        space = QFrame()
        space.setFixedWidth(5)
        space.setStyleSheet("background-color: #E8E8E8;")
        layout.addWidget(space, 0, 3) 

        frame_move = QFrame()
        frame_move.setMinimumWidth(100)
        frame_move.setStyleSheet(style_frame)
        layout.addWidget(frame_move, 0, 4) 
        
        space = QFrame()
        space.setFixedWidth(5)
        space.setStyleSheet("background-color: #E8E8E8;")
        layout.addWidget(space, 0, 5) 

        frame_tool = QFrame()
        frame_tool.setMinimumWidth(180)
        frame_tool.setStyleSheet(style_frame)
        layout.addWidget(frame_tool, 0, 6) 
        
        space = QFrame()
        space.setFixedWidth(5)
        space.setStyleSheet("background-color: #E8E8E8;")
        layout.addWidget(space, 0, 7) 

        frame_io = QFrame()
        frame_io.setMinimumWidth(180)
        frame_io.setStyleSheet(style_frame)
        layout.addWidget(frame_io, 0, 8) 
        
        self.frameMove(frame_move)
        self.FrameTool(frame_tool)
        self.FrameJointJog(frame_joint_jog)
        self.FrameAxisJog(frame_axis_jog)
        self.FrameIo(frame_io)    
 
    # Tool       
    def FrameTool(self, frame):
        layout = QGridLayout(frame)
        
        self.LABEL_TOOL = QLabel("Tool")
        self.LABEL_TOOL.setStyleSheet(style_label_title)
        self.LABEL_TOOL.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.LABEL_TOOL.setMaximumHeight(20)
        layout.addWidget(self.LABEL_TOOL, 0, 0)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
    
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QGridLayout(scroll_widget) 
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, 1, 0) 
               
        label = QLabel("Servo tool position:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label, 0, 0, 1, 3)        

        button = QPushButton("-")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(50)
        button.setMinimumWidth(20)
        scroll_layout.addWidget(button, 1, 0)
        button.clicked.connect(lambda: self.ButtonMoveTool(-1))

        self.LABEL_TOOL_POS = QLabel("pos: 0")
        self.LABEL_TOOL_POS.setStyleSheet(style_label)
        self.LABEL_TOOL_POS.setAlignment(Qt.AlignCenter)
        self.LABEL_TOOL_POS.setFixedWidth(80)
        scroll_layout.addWidget(self.LABEL_TOOL_POS, 1, 1)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMinimumWidth(20)
        button.setMaximumWidth(50)
        scroll_layout.addWidget(button, 1, 2)
        button.clicked.connect(lambda: self.ButtonMoveTool(1))

        spacer = QSpacerItem(10, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        scroll_layout.addItem(spacer)

        label = QLabel("Relay tool state:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label, 2, 0, 1, 3) 

        self.CHECKBOX_TOOL_OUTPUT = QCheckBox("ON / OFF")
        self.CHECKBOX_TOOL_OUTPUT.setStyleSheet(style_checkbox)
        scroll_layout.addWidget(self.CHECKBOX_TOOL_OUTPUT, 3, 0, 1, 3)

        spacer_widget = QWidget()
        scroll_layout.addWidget(spacer_widget, 4, 0)
        
        label = QLabel("Current tool:")
        label.setStyleSheet(style_label_bold)
        scroll_layout.addWidget(label, 5, 0, 1, 3) 

        self.TOOL_COMBO = QComboBox()
        self.TOOL_COMBO.setStyleSheet(style_combo)
        self.TOOL_COMBO.setMaximumWidth(150)
        
        self.TOOL_COMBO.currentIndexChanged.connect(lambda index: change_tool(index))
        
        scroll_layout.addWidget(self.TOOL_COMBO, 6, 0, 1, 3)


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
         
    def ButtonMoveTool(self, dir):
        # chack if thye tool is a servo
        if get_tool_info() != "Servo":
            return
        
        if self.simulation:
            if dir == 1:
                pos = event_manager.publish("request_get_jog_distance")[0]
            else:
                pos = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            
            print(pos)
            simulation_move_gui(pos, "Tool_MoveTo")
        else:
            if dir == 1:
                pos = event_manager.publish("request_get_jog_distance")[0]
            else:
                pos = -1 * int(event_manager.publish("request_get_jog_distance")[0])
                
            #offset_j(posAxis)

 
         
    # Frame move    
    def frameMove(self,frame):
        layout = QGridLayout(frame)
        
        self.LABEL_MOVE = QLabel("Move")
        self.LABEL_MOVE.setStyleSheet(style_label_title)
        self.LABEL_MOVE.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.LABEL_MOVE.setMaximumHeight(20)
        layout.addWidget(self.LABEL_MOVE, 0, 0)
 
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout_move = QGridLayout(scroll_widget) 
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll, 3, 0) 
         
        
        button = QPushButton("Go to pos")
        button.setStyleSheet(style_button)
        button.clicked.connect(lambda: self.ButtonMove())
        layout.addWidget(button, 1, 0) 
        
        self.CHECKBOX_MOVE = QCheckBox("Switch to joint")
        self.CHECKBOX_MOVE.setStyleSheet(style_checkbox)
        self.CHECKBOX_MOVE.setChecked(False)  # Set the initial state of the checkbox
        
        layout.addWidget(self.CHECKBOX_MOVE, 2, 0)
        self.CHECKBOX_MOVE.stateChanged.connect(lambda state: self.SwitchJointAxis(state))
        
    def CreateButtonsMove(self, nr, name_joint, name_axis):
        self.ButtonsMove = []
        self.name_joint = name_joint
        self.name_axis = name_axis
        self.nr_of_joints = nr
        
        for i in range(self.nr_of_joints):
            label = QLabel(f"{self.name_axis[i]}:")
            label.setStyleSheet(style_label)
            label.setMaximumWidth(20)
            
            validator = QDoubleValidator()
            validator.setNotation(QDoubleValidator.StandardNotation)
            
            entry = QLineEdit()
            entry.setMaximumWidth(40)
            entry.setStyleSheet(style_entry)
            entry.setValidator(validator)
            entry.setText(str(round(var.POS_AXIS_SIM[i])))
            
            self.ButtonsMove.append([label,entry])
            
            self.layout_move.addWidget(label, i, 0)
            self.layout_move.addWidget(entry, i, 1)
            
        self.space_widget_move = QWidget()
        self.layout_move.addWidget(self.space_widget_move, self.layout_move.rowCount(), 0, 1, self.layout_move.columnCount())              

    def DeleteButtonsMove(self):
        for i in range(len(self.ButtonsMove)):
            for j in range(2):
                self.ButtonsMove[i][j].setParent(None)
                self.ButtonsMove[i][j].deleteLater()
 
        if self.space_widget_move:
            self.space_widget_move.setParent(None)
            self.space_widget_move.deleteLater()
 
    def SwitchJointAxis(self, state):
        if state:
            self.CHECKBOX_MOVE.setText("Switch to axis")
            for i in range(self.nr_of_joints):
                self.ButtonsMove[i][0].setText(self.name_joint[i])
                if var.SIM:
                    # get the position of the sim axis 
                    pos = send_pos_robot(True)
                    self.ButtonsMove[i][1].setText(str(round(pos[1][i],2)))
                    
                else:
                    # get the position of the axis 
                    pos = send_pos_robot(False)
                    self.ButtonsMove[i][1].setText(str(round(pos[1][i])))
                
        else:
            self.CHECKBOX_MOVE.setText("Switch to joint")
            for i in range(self.nr_of_joints):
                self.ButtonsMove[i][0].setText(self.name_axis[i])
                if var.SIM:
                    # get the position of the joint
                    pos = send_pos_robot(True)  # TRUE IS SIM
                    self.ButtonsMove[i][1].setText(str(round(pos[0][i],2)))
                else:
                    # get the position of the joint
                    pos = send_pos_robot(False)
                    self.ButtonsMove[i][1].setText(str(round(pos[0][i])))        
    
    def ButtonMove(self):
        posJoint = [0]* self.nr_of_joints
        
        for i in range(self.nr_of_joints):
            posJoint[i] = self.ButtonsMove[i][1].text()
            
        if self.simulation:
            if self.CHECKBOX_MOVE.isChecked():
                # joints
                print("Move joint")
                simulation_move_gui(posJoint, "MoveJoint")
            else:
                # axis
                print("MoveJ axis")
                simulation_move_gui(posJoint, "MoveJ")
        else:
            if self.CHECKBOX_MOVE.isChecked():
                # joints
                move_joint_pos(posJoint)
            else:
                # axis
                move_j(posJoint)
            
            
    
    # Frame joint jog
    def FrameJointJog(self, frame):   
        layout = QGridLayout(frame)
        
        self.LABEL_JOG_JOINT = QLabel("Jog Joint")
        self.LABEL_JOG_JOINT.setStyleSheet(style_label_title)
        self.LABEL_JOG_JOINT.setMaximumHeight(20)
        self.LABEL_JOG_JOINT.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.LABEL_JOG_JOINT, 0, 0, 1, 3)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout_joint_jog = QGridLayout(scroll_widget) 
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll) 

    def CreateButtonsJoint(self, nr):
        self.ButtonsJoint = []
        self.nr_of_joints = nr
        for i in range(nr):
            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 0))
            button_minus.setMaximumWidth(50)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet(style_button)

            label = QLabel(f"{var.NAME_JOINTS[i]} {var.POS_JOINT[i]} {var.UNIT_JOINT[i]}")
            label.setStyleSheet(style_label)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)

            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 1))
            button_plus.setMaximumWidth(50)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet(style_button)
            
            self.ButtonsJoint.append([button_minus,label,button_plus])
            
            self.layout_joint_jog.addWidget(button_minus, i+1, 0)
            self.layout_joint_jog.addWidget(label, i+1, 1)
            self.layout_joint_jog.addWidget(button_plus, i+1, 2)
            
        self.space_widget_joint = QWidget()
        self.layout_joint_jog.addWidget(self.space_widget_joint, self.layout_joint_jog.rowCount(), 0, 1, self.layout_joint_jog.columnCount())
    
    def DeleteButtonsJoint(self):
        for i in range(len(self.ButtonsJoint)):
            for j in range(3):
                self.ButtonsJoint[i][j].setParent(None)
                self.ButtonsJoint[i][j].deleteLater()
                
        if self.space_widget_joint:
            self.space_widget_joint.setParent(None)
            self.space_widget_joint.deleteLater()

    def ChangeJointLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.ButtonsJoint[i][1].setText(f"{name[i]}: {round(pos[i],2)} {unit[i]}")
 
    def ButtonJointMove(self, joint, dir):
        posJoint = [0] * self.nr_of_joints
        if self.simulation:
            if dir == 1:
                posJoint[joint] = int(event_manager.publish("request_get_jog_distance")[0])
            else:
                posJoint[joint] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            
            simulation_move_gui(posJoint, "jogJ")
        else:
            if dir == 1:
                posJoint[joint] = int(event_manager.publish("request_get_jog_distance")[0])
            else:
                posJoint[joint] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            
            jog_joint(posJoint)
   
    # Frame axis jog             
    def FrameAxisJog(self, frame):  
        layout = QGridLayout(frame)
        
        self.LABEL_JOG_AXIS = QLabel("Jog Axis")
        self.LABEL_JOG_AXIS.setStyleSheet(style_label_title)
        self.LABEL_JOG_AXIS.setMaximumHeight(20)
        self.LABEL_JOG_AXIS.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.LABEL_JOG_AXIS, 0, 0, 1, 3)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout_axis_jog = QGridLayout(scroll_widget) 
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll) 
            
    def CreateButtonsAxis(self, nr):
        self.ButtonsAxis = []
        for i in range(nr):
            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 0))
            button_minus.setMaximumWidth(50)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet(style_button)
            
            label = QLabel(f"{var.NAME_AXIS[i]} {var.POS_AXIS[i]} {var.UNIT_AXIS[i]}")
            label.setStyleSheet(style_label)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)
            
            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 1))
            button_plus.setMaximumWidth(50)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet(style_button)
            
            self.ButtonsAxis.append([button_minus,label,button_plus])
            
            self.layout_axis_jog.addWidget(button_minus, i+1, 0)
            self.layout_axis_jog.addWidget(label, i+1, 1) 
            self.layout_axis_jog.addWidget(button_plus, i+1, 2)
            
        self.space_widget_axis = QWidget()
        self.layout_axis_jog.addWidget(self.space_widget_axis, self.layout_axis_jog.rowCount(), 0, 1, self.layout_axis_jog.columnCount())

    def DeleteButtonsAxis(self):
        for i in range(len(self.ButtonsAxis)):
            for j in range(3):
                self.ButtonsAxis[i][j].setParent(None)
                self.ButtonsAxis[i][j].deleteLater()
                
        if self.space_widget_axis:
            self.space_widget_axis.setParent(None)
            self.space_widget_axis.deleteLater()

    def ChangeAxisLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.ButtonsAxis[i][1].setText(f"{name[i]}: {round(pos[i])} {unit[i]}")

    def ButtonAxisMove(self, axis, dir):
        posAxis = [0]*6
        if self.simulation:
            if dir == 1:
                posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posAxis[axis] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            print(posAxis)
            simulation_move_gui(posAxis, "OffsetJ")
        else:
            if dir == 1:
                posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posAxis[axis] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            offset_j(posAxis)

    # Frame IO 
    def FrameIo(self, frame):
        layout = QGridLayout(frame)
        
        self.LABEL_IO = QLabel("IO")
        self.LABEL_IO.setStyleSheet(style_label_title)
        self.LABEL_IO.setMaximumHeight(20)
        self.LABEL_IO.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        layout.addWidget(self.LABEL_IO, 0, 0, 1, 2)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        scroll_layout = QGridLayout(scroll_widget) 
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll) 
        
        self.CHECKBOX_IO_INPUT = []
        self.CHECKBOX_IO_OUTPUT = []
        
        for i in range(10):
            label = QLabel(f"IO pin {i}")
            label.setStyleSheet(style_label)
            scroll_layout.addWidget(label, 1 + i, 0)
            
            checkbox = QCheckBox("IN")
            checkbox.setStyleSheet(style_checkbox_io)
            scroll_layout.addWidget(checkbox, 1 + i, 2)
            self.CHECKBOX_IO_INPUT.append(checkbox)
            
            checkbox = QCheckBox("OUT")
            checkbox.setStyleSheet(style_checkbox_io)
            scroll_layout.addWidget(checkbox, 1 + i, 3)
            self.CHECKBOX_IO_OUTPUT.append(checkbox)
           
    def CheckIOState(self, io_number):
        if self.CHECKBOX_IO_INPUT[io_number].isChecked():
            return True
        else:
            return False
           
    def SetIoStateInput(self, io_number, state):
        self.CHECKBOX_IO_INPUT[io_number].setChecked(state)
        
    def SetIoStateOutput(self, io_number, state):
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
            
