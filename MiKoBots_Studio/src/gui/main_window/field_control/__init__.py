from PyQt5.QtWidgets import QScrollArea, QSpacerItem, QPushButton, QLabel, QCheckBox, QComboBox, QSizePolicy, QApplication, QFileDialog, QFrame, QGridLayout, QTextEdit, QScrollBar, QLineEdit, QWidget

from gui.style import * 

from backend.core.event_manager import event_manager

from .control_axis import ControlAxis
from .control_io import ControlIO
from .control_joint import ControlJoint
from .control_move import ControlMove
from .control_tool import ControlTool

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
        frame_move.setFixedWidth(110)
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
        
        self.frameMove = ControlMove(frame_move)
        self.FrameTool = ControlTool(frame_tool)
        self.FrameJointJog  = ControlJoint(frame_joint_jog)
        self.FrameAxisJog = ControlAxis(frame_axis_jog)
        self.FrameIo = ControlIO(frame_io)    
 
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
 