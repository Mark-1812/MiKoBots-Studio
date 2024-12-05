from PyQt5.QtWidgets import QHBoxLayout, QScrollArea, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

from backend.core.event_manager import event_manager

from .control_axis import ControlAxis
from .control_io import ControlIO
from .control_joint import ControlJoint
from .control_move import ControlMove
from .control_tool import ControlTool

class ControlField:   
    def __init__(self, parent_frame: QWidget):
        self.parent_frame = parent_frame
        self.layout = QHBoxLayout(self.parent_frame)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create a scroll area
        scroll_area = QScrollArea(self.parent_frame)
        scroll_area.setWidgetResizable(True) 

        # Create the child widget and layout
        scroll_widget = QWidget(scroll_area)
        scroll_widget.setStyleSheet(style_widget)
        self.scroll_layout = QHBoxLayout(scroll_widget)
        self.scroll_layout.setContentsMargins(5, 0, 5, 0)
        

        
        self.createFrames()
        self.subscribeToEvents()

        scroll_area.setWidget(scroll_widget)
        self.layout.addWidget(scroll_area)

        self.parent_frame.setLayout(self.layout)
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_change_labels_control", self.ChangeTitles)
            
    def createFrames(self):
        self.frame_joint_jog = QWidget()
        self.frame_joint_jog.setMinimumWidth(200)
        self.frame_joint_jog.setStyleSheet(style_frame)
        self.FrameJointJog  = ControlJoint(self.frame_joint_jog)
        self.scroll_layout.addWidget(self.frame_joint_jog) 
        

        self.frame_axis_jog = QWidget()
        self.frame_axis_jog.setMinimumWidth(200)
        self.frame_axis_jog.setStyleSheet(style_frame)
        self.FrameAxisJog = ControlAxis(self.frame_axis_jog)
        self.scroll_layout.addWidget(self.frame_axis_jog)  
        

        self.frame_move = QWidget()
        self.frame_move.setFixedWidth(110)
        self.frame_move.setStyleSheet(style_frame)
        self.frameMove = ControlMove(self.frame_move)
        self.scroll_layout.addWidget(self.frame_move) 
        

        self.frame_tool = QWidget()
        self.frame_tool.setMinimumWidth(180)
        self.frame_tool.setStyleSheet(style_frame)
        self.FrameTool = ControlTool(self.frame_tool)
        self.scroll_layout.addWidget(self.frame_tool) 
        

        self.frame_io = QWidget()
        self.frame_io.setMinimumWidth(180)
        self.frame_io.setStyleSheet(style_frame)
        self.FrameIo = ControlIO(self.frame_io) 
        self.scroll_layout.addWidget(self.frame_io)
        

    def ChangeTitles(self, sim):
        if sim:
            self.simulation = True
            self.FrameJointJog.title.setText("Jog Joint (sim)")
            self.FrameAxisJog.title.setText("Jog Axis (sim)")
            self.frameMove.title.setText("Move (sim)")
            self.FrameTool.title.setText("Tool (sim)")
            self.FrameIo.title.setText("IO (sim)")  

            self.FrameJointJog.simulation = True
            self.FrameAxisJog.simulation = True
            self.frameMove.simulation = True
            self.FrameTool.simulation = True
            self.FrameIo.simulation = True

        else:
            self.simulation = False
            
            self.FrameJointJog.title.setText("Jog Joint")
            self.FrameAxisJog.title.setText("Jog Axis")
            self.frameMove.title.setText("Move")
            self.FrameTool.title.setText("Tool")
            self.FrameIo.title.setText("IO")  

            self.FrameJointJog.simulation = False
            self.FrameAxisJog.simulation = False
            self.frameMove.simulation = False
            self.FrameTool.simulation = False
            self.FrameIo.simulation = False  
 