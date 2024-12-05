from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QScrollArea, QSpacerItem, QPushButton, QLabel,  QSizePolicy, QGridLayout, QWidget

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.run_program import run_single_line

class ControlJoint:
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QGridLayout(self.parent_frame)


        self.layout.setContentsMargins(3, 3, 3, 3)
        self.simulation = False

        self.FrameJointJog()
        self.subscribeToEvents()

        self.parent_frame.setLayout(self.layout)
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_label_pos_joint", self.ChangeJointLabels)    
        event_manager.subscribe("request_create_buttons_joint", self.CreateButtonsJoint)
        event_manager.subscribe("request_delete_buttons_joint", self.DeleteButtonsJoint)

    def FrameJointJog(self):   
        self.title = QLabel("Jog Joint")
        self.title.setStyleSheet(style_label_title)
        self.title.setMaximumHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.title, 0, 0)
        
        # create a scroll area
        scroll_area = QScrollArea(self.parent_frame)
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

        self.parent_frame.setLayout(self.layout)

    def CreateButtonsJoint(self, nr):
        self.Buttons = []
        self.frames = []

        self.nr_of_joints = nr

        for i in range(nr):
            frame = QWidget(self.scroll_widget)
            layout_axis = QHBoxLayout()
            layout_axis.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_axis)
            self.layout_scroll.addWidget(frame) 
            self.frames.append(frame)

            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 0))
            button_minus.setMaximumWidth(30)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet(style_button)

            label = QLabel(f"{var.NAME_JOINTS[i]} {var.POS_JOINT[i]} {var.UNIT_JOINT[i]}")
            label.setStyleSheet(style_label)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(80)

            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonJointMove(idx, 1))
            button_plus.setMaximumWidth(30)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet(style_button)
            
            self.Buttons.append([button_minus,label,button_plus])
            
            layout_axis.addWidget(button_minus)
            layout_axis.addWidget(label)
            layout_axis.addWidget(button_plus)
            

    def DeleteButtonsJoint(self):
        for frame in self.frames:
            self.layout_scroll.removeWidget(frame)
            frame.deleteLater() 
            frame = None
            
    def ChangeJointLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.Buttons[i][1].setText(f"{name[i]}: {round(pos[i],2)} {unit[i]}")
 
    def ButtonJointMove(self, joint, dir):
        posJoint = [0] * self.nr_of_joints

        if dir == 1:
            posJoint[joint] = int(event_manager.publish("request_get_jog_distance")[0])
        else:
            posJoint[joint] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            
        run_single_line(f"robot.JogJoint({posJoint}, {var.JOG_SPEED}, {var.JOG_ACCEL})")

