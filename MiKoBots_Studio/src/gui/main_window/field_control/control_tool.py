from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QFrame, QPushButton, QLabel, QCheckBox, QComboBox,  QGridLayout,  QWidget
from PyQt5.QtCore import Qt

from gui.style import * 

import backend.core.variables as var

from backend.core.event_manager import event_manager

from backend.robot_management import change_tool

from backend.run_program import run_single_line      

class ControlTool(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(style_frame)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 3, 5, 3)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.setMinimumWidth(140)
        
        
        self.simulation = False

        self.FrameTool()
        self.subscribeToEvents()

        self.setLayout(self.layout)
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_add_tool_combo", self.AddToolCombo)
        event_manager.subscribe("request_delete_tool_combo", self.DeleteToolsCombo)
        event_manager.subscribe("request_set_tool_combo", self.SetToolCombo)
        event_manager.subscribe("request_enable_tool_combo", self.EnableToolCombo)
        event_manager.subscribe("request_set_tool_pos", self.SetToolPos)
        event_manager.subscribe("request_set_tool_state", self.SetToolState)

    # Tool       
    def FrameTool(self):
        self.title = QLabel("Tool")
        self.title.setStyleSheet(style_label_title)
        self.title.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.title.setMaximumHeight(20)
        self.layout.addWidget(self.title)
        
               
        label = QLabel("Servo tool position:")
        label.setStyleSheet(style_label_bold)
        self.layout.addWidget(label)       

        frame = QWidget()
        frame.setStyleSheet(style_widget)
        layout_buttons = QHBoxLayout()
        layout_buttons.setContentsMargins(5, 0, 5, 5)
        frame.setLayout(layout_buttons)
        self.layout.addWidget(frame) 

        button = QPushButton("-")
        button.setStyleSheet(style_button)
        button.setMaximumWidth(50)
        button.setMinimumWidth(20)
        layout_buttons.addWidget(button)
        button.clicked.connect(lambda: self.ButtonMoveTool(-1))

        self.LABEL_TOOL_POS = QLabel("pos: 0")
        self.LABEL_TOOL_POS.setStyleSheet(style_label)
        self.LABEL_TOOL_POS.setAlignment(Qt.AlignCenter)
        layout_buttons.addWidget(self.LABEL_TOOL_POS)

        button = QPushButton("+")
        button.setStyleSheet(style_button)
        button.setMinimumWidth(20)
        button.setMaximumWidth(50)
        layout_buttons.addWidget(button)
        button.clicked.connect(lambda: self.ButtonMoveTool(1))

        label = QLabel("Relay tool state:")
        label.setStyleSheet(style_label_bold)
        self.layout.addWidget(label) 

        self.CHECKBOX_TOOL_OUTPUT = QCheckBox("ON / OFF")
        self.CHECKBOX_TOOL_OUTPUT.setStyleSheet(style_checkbox)
        self.CHECKBOX_TOOL_OUTPUT.stateChanged.connect(self.ChangeStateTool)
        self.layout.addWidget(self.CHECKBOX_TOOL_OUTPUT)

        
        label = QLabel("Current tool:")
        label.setStyleSheet(style_label_bold)
        self.layout.addWidget(label) 

        self.TOOL_COMBO = QComboBox(self)
        self.TOOL_COMBO.setStyleSheet(style_combo)
        self.TOOL_COMBO.setMaximumWidth(150)
        self.layout.addWidget(self.TOOL_COMBO)
        
        self.TOOL_COMBO.currentIndexChanged.connect(lambda index: change_tool(index))
        
        

 
    def ChangeStateTool(self, state):
        if not self.simulation:
            tool = var.TOOL_NAME
            
            if state == 2:
                run_single_line(f"tool.SetTool('{tool}')\ntool.State('HIGH')")
            else:
                run_single_line(f"tool.SetTool('{tool}')\ntool.State('LOW')")

    def AddToolCombo(self, tool):
        self.TOOL_COMBO.blockSignals(True)
        self.TOOL_COMBO.addItem(tool)  
        self.TOOL_COMBO.blockSignals(False)
        

    def DeleteToolsCombo(self):
        self.TOOL_COMBO.blockSignals(True)
        self.TOOL_COMBO.clear()
        self.TOOL_COMBO.blockSignals(False)

    def SetToolCombo(self, tool):
        # self.TOOL_COMBO.blockSignals(True)
        self.TOOL_COMBO.setCurrentIndex(tool)
        # self.TOOL_COMBO.blockSignals(False)
        
    def EnableToolCombo(self, enable):
        if enable:
            self.TOOL_COMBO.setEnabled(True)
        else:
            self.TOOL_COMBO.setEnabled(False)

    def SetToolPos(self, pos):
        self.LABEL_TOOL_POS.setText(f"Pos: {pos}")

    def SetToolState(self, state):
        self.CHECKBOX_TOOL_OUTPUT.blockSignals(True)
        self.CHECKBOX_TOOL_OUTPUT.setChecked(state) 
        self.CHECKBOX_TOOL_OUTPUT.blockSignals(False)
         
    def ButtonMoveTool(self, dir):
        if dir == 1:
            pos = var.TOOL_POS + int(event_manager.publish("request_get_jog_distance")[0])
        else:
            pos = var.TOOL_POS - int(event_manager.publish("request_get_jog_distance")[0])
            
        tool = var.TOOL_NAME  
        
        if var.TOOL_TYPE == "Servo":
            line = f"""tool.SetTool("{tool}")\ntool.MoveTo({pos})"""
            run_single_line(line)
