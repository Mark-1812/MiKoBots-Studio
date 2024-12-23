from PyQt5 import  QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QSizePolicy,  QGridLayout,  QLineEdit, QWidget

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.robot_management import get_pos_robot


from backend.simulation import check_simulation_on
from backend.run_program import run_single_line

class ControlMove(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 3, 5, 3)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setMinimumWidth(150)

        self.simulation = False

        self.frameMove()
        self.subscribeToEvents()
        self.frames = []

        self.setLayout(self.layout) 
           
    def subscribeToEvents(self):       
        event_manager.subscribe("request_create_buttons_move", self.CreateButtonsMove)
        event_manager.subscribe("request_delete_buttons_move", self.DeleteButtonsMove)
  
    def frameMove(self):
        self.title = QLabel("Move")
        self.title.setStyleSheet(style_label_title)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.title.setMaximumHeight(20)
        self.layout.addWidget(self.title)

        button = QPushButton("Go to pos")
        button.setStyleSheet(style_button)
        button.clicked.connect(lambda: self.ButtonMove())
        self.layout.addWidget(button) 

        self.CHECKBOX_MOVE = QCheckBox("Switch to joint")
        self.CHECKBOX_MOVE.setStyleSheet(style_checkbox)
        self.CHECKBOX_MOVE.setChecked(False)  # Set the initial state of the checkbox
        
        self.layout.addWidget(self.CHECKBOX_MOVE)
        self.CHECKBOX_MOVE.stateChanged.connect(lambda state: self.SwitchJointAxis(state))
 
        # create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setMaximumWidth(150)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_widget = QWidget(scroll_area)
        self.scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(self.scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area) 
         
        

        

        
    def CreateButtonsMove(self, nr, name_joint, name_axis):
        self.Buttons = []
        self.name_joint = name_joint
        self.name_axis = name_axis
        self.nr_of_joints = nr
        self.frames = []

        for i in range(self.nr_of_joints):
            frame = QWidget(self.scroll_widget)
            layout_move = QHBoxLayout()
            layout_move.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_move)
            self.layout_scroll.addWidget(frame) 
            self.frames.append(frame)

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
            
            self.Buttons.append([label,entry])

            layout_move.addWidget(label)
            layout_move.addWidget(entry)

    def DeleteButtonsMove(self):
        for frame in self.frames:
            self.layout_scroll.removeWidget(frame)
            frame.deleteLater() 
            frame = None
 
    def SwitchJointAxis(self, state):
        if state:
            self.CHECKBOX_MOVE.setText("Switch to axis")
            for i in range(self.nr_of_joints):
                self.Buttons[i][0].setText(self.name_joint[i])
                if check_simulation_on():
                    pos = var.POS_JOINT_SIM
                    self.Buttons[i][1].setText(str(round(pos[i],2)))
                else:
                    pos = var.POS_JOINT
                    self.Buttons[i][1].setText(str(round(pos[i],2)))
                
        else:
            self.CHECKBOX_MOVE.setText("Switch to joint")
            for i in range(self.nr_of_joints):
                self.Buttons[i][0].setText(self.name_axis[i])
                if check_simulation_on():
                    pos = var.POS_AXIS_SIM
                    self.Buttons[i][1].setText(str(round(pos[i],2)))
                else:
                    pos = var.POS_AXIS
                    self.Buttons[i][1].setText(str(round(pos[i],2)))        
    
    def ButtonMove(self):
        posJoint = [0]* self.nr_of_joints
        
        for i in range(self.nr_of_joints):
            posJoint[i] = self.Buttons[i][1].text()
            
        if self.CHECKBOX_MOVE.isChecked():
            # joints
            run_single_line(f"robot.MoveJointPos({posJoint}, {var.JOG_SPEED}, {var.JOG_ACCEL})")
        else:
            # axis
            run_single_line(f"robot.MoveJ({posJoint}, {var.JOG_SPEED}, {var.JOG_ACCEL})")

