from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.run_program import run_single_line



class ControlAxis(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(5, 3, 5, 3)
        self.layout.setSpacing(5)

        self.setMinimumWidth(180)

        self.simulation = False
        self.frames = []

        self.FrameAxisJog()
        self.subscribeToEvents()

        self.setLayout(self.layout)

    def subscribeToEvents(self):
        event_manager.subscribe("request_label_pos_axis", self.ChangeAxisLabels)
        event_manager.subscribe("request_create_buttons_axis", self.CreateButtonsAxis)
        event_manager.subscribe("request_delete_buttons_axis", self.DeleteButtonsAxis)
       
    def FrameAxisJog(self):  
        self.title = QLabel("Jog Axis")
        self.title.setStyleSheet(style_label_title)
        self.title.setMaximumHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.title)
        
        # create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setMaximumWidth(200)
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet(style_scrollarea)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.scroll_widget = QWidget(scroll_area)
        self.scroll_widget.setStyleSheet(style_widget)
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.scroll_layout.setSpacing(0)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        
        scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(scroll_area) 

        
            
    def CreateButtonsAxis(self, nr):
        self.Buttons = []
        self.frames = []

        for i in range(nr):
            frame = QWidget(self.scroll_widget)
            layout_axis = QHBoxLayout()
            layout_axis.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_axis)
            self.scroll_layout.addWidget(frame) 
            self.frames.append(frame)

            button_minus = QPushButton("-")
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 0))
            button_minus.setMaximumWidth(30)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet(style_button)
            
            label = QLabel(f"{var.NAME_AXIS[i]} {var.POS_AXIS[i]} {var.UNIT_AXIS[i]}")
            label.setStyleSheet(style_label)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)
            
            button_plus = QPushButton("+")
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 1))
            button_plus.setMaximumWidth(30)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet(style_button)
            
            self.Buttons.append([button_minus,label,button_plus])

            layout_axis.addWidget(button_minus)
            layout_axis.addWidget(label) 
            layout_axis.addWidget(button_plus)

    def DeleteButtonsAxis(self):
        for frame in self.frames:
            self.scroll_layout.removeWidget(frame)
            frame.deleteLater() 
            frame = None
        

    def ChangeAxisLabels(self, pos, name, unit):
        number_of_joints = var.NUMBER_OF_JOINTS

        for i in range(number_of_joints):
            self.Buttons[i][1].setText(f"{name[i]}: {round(pos[i])} {unit[i]}")

    def ButtonAxisMove(self, axis, dir):
        number_of_joints = var.NUMBER_OF_JOINTS

        posAxis = [0]*number_of_joints
        
        if dir == 1:
            posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
        else:
            posAxis[axis] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
            
        run_single_line(f"robot.OffsetJ({posAxis}, {var.JOG_SPEED}, {var.JOG_ACCEL})")

