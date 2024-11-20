from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.simulation import simulation_move_gui
from backend.run_program import run_single_line

class ControlAxis(QWidget):
    def __init__(self, frame, parent = None):
        super().__init__(parent)
        self.layout = QGridLayout(frame)
        self.layout.setContentsMargins(3, 3, 3, 3)

        self.simulation = False

        self.FrameAxisJog()
        self.subscribeToEvents()
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_label_pos_axis", self.ChangeAxisLabels)
        event_manager.subscribe("request_create_buttons_axis", self.CreateButtonsAxis)
        event_manager.subscribe("request_delete_buttons_axis", self.DeleteButtonsAxis)
       
    def FrameAxisJog(self):  
        self.title = QLabel("Jog Axis")
        self.title.setStyleSheet(style_label_title)
        self.title.setMaximumHeight(20)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignVCenter)
        self.layout.addWidget(self.title, 0, 0)
        
        # create a scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(style_scrollarea)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_widget = QWidget()
        scroll_widget.setStyleSheet(style_widget)
        self.layout_scroll = QVBoxLayout(scroll_widget)
        self.layout_scroll.setContentsMargins(0, 0, 0, 0)
        self.layout_scroll.setSpacing(0)
        self.layout_scroll.setAlignment(Qt.AlignTop)
        
        scroll.setWidget(scroll_widget)
        self.layout.addWidget(scroll) 
            
    def CreateButtonsAxis(self, nr):
        self.Buttons = []

        if not hasattr(self, 'layout_scroll') or self.layout_scroll is None:
        # Recreate the layout if it doesn't exist
            self.layout_scroll = QGridLayout(self)

        for i in range(nr):
            frame = QFrame()
            layout_axis = QHBoxLayout()
            layout_axis.setContentsMargins(5,0,5,5)
            frame.setLayout(layout_axis)
            self.layout_scroll.addWidget(frame) 

            button_minus = QPushButton("-", self)
            button_minus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 0))
            button_minus.setMaximumWidth(50)
            button_minus.setMinimumWidth(20)
            button_minus.setStyleSheet(style_button)
            
            label = QLabel(f"{var.NAME_AXIS[i]} {var.POS_AXIS[i]} {var.UNIT_AXIS[i]}", self)
            label.setStyleSheet(style_label)
            label.setAlignment(QtCore.Qt.AlignCenter)
            label.setMinimumWidth(90)
            
            button_plus = QPushButton("+", self)
            button_plus.clicked.connect(lambda state, idx=i: self.ButtonAxisMove(idx, 1))
            button_plus.setMaximumWidth(50)
            button_plus.setMinimumWidth(20)
            button_plus.setStyleSheet(style_button)
            
            self.Buttons.append([button_minus,label,button_plus])

            layout_axis.addWidget(button_minus)
            layout_axis.addWidget(label) 
            layout_axis.addWidget(button_plus)

    def DeleteButtonsAxis(self):
        while self.layout_scroll.count():
            item = self.layout_scroll.takeAt(0)  # Take the first item from the layout
            widget = item.widget()   # If it's a widget, delete it
            if widget is not None:
                widget.deleteLater()  # This ensures the widget is properly deleted
            else:
                self.layout_scroll.removeItem(item)  # If it's not a widget, just remove it (e.g., a spacer item)
        

    def ChangeAxisLabels(self, pos, name, unit):
        for i in range(var.NUMBER_OF_JOINTS):
            self.Buttons[i][1].setText(f"{name[i]}: {round(pos[i])} {unit[i]}")

    def ButtonAxisMove(self, axis, dir):
        posAxis = [0]*var.NUMBER_OF_JOINTS
        if self.simulation:
            if dir == 1:
                posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posAxis[axis] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
                
            simulation_move_gui(posAxis, "OffsetJ")
        else:
            if dir == 1:
                posAxis[axis] = event_manager.publish("request_get_jog_distance")[0]
            else:
                posAxis[axis] = -1 * int(event_manager.publish("request_get_jog_distance")[0])
                
            run_single_line(f"robot.OffsetJ({posAxis}, {var.JOG_SPEED}, {var.JOG_ACCEL})")

