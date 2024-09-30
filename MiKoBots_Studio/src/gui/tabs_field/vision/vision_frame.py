from PyQt5.QtWidgets import QLineEdit, QLabel, QTabWidget, QFrame, QScrollArea, QVBoxLayout, QSpacerItem, QPushButton, QWidget, QGridLayout, QCheckBox, QTextEdit
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QPixmap, QImage, QDoubleValidator

from backend.core.event_manager import event_manager

from gui.tabs_field.vision.vision_info import VisionInfo
from gui.tabs_field.vision.vision_connec4 import Connect4
from gui.tabs_field.vision.vision_tictactoe import TicTacToe
from gui.tabs_field.vision.vision_setup import VisionSetup

from gui.style import *

class VisionFrame():
    def __init__(self, frame):
        frame_layout = QGridLayout()
        frame.setLayout(frame_layout)
        
        title = QLabel("Setup vision")
        title.setStyleSheet(style_label_bold)
        title.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        title.setFixedHeight(20)
        frame_layout.addWidget(title, 0, 0,1,2)
        
        tabs = QTabWidget()
        tabs.setMaximumWidth(500)
        frame_layout.addWidget(tabs, 1, 0,2,1)
        
        # Create the label to display the frame
        self.label_Image = QLabel()
        self.label_Image.setMinimumWidth(300)
        self.label_Image.setMaximumHeight(400)
        self.label_Image.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        frame_layout.addWidget(self.label_Image, 1, 1)

        
        self.label_video = QLabel()
        self.label_video.setMinimumWidth(300)
        self.label_video.setMaximumHeight(200)
        self.label_video.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        frame_layout.addWidget(self.label_video, 2, 1)
        
        tabs.setStyleSheet(style_tabs)
        
        tab1 = QFrame()
        tab2 = QFrame()
        tab3 = QFrame()
        tab4 = QFrame()

        tabs.addTab(tab1, "Info")        
        tabs.addTab(tab2, "Set-up")
        tabs.addTab(tab3, "Tic-Tac-Toe")
        tabs.addTab(tab4, "Connect 4")
        
        VisionInfo(tab1)
        VisionSetup(tab2)
        TicTacToe(tab3)
        Connect4(tab4)
        
        self.subscribeToEvents()
        
    def subscribeToEvents(self):
        event_manager.subscribe("request_label_width_video", self.GetLabelWidthVideo)
        event_manager.subscribe("request_label_height_video", self.GetLabelHeightVideo)
        event_manager.subscribe("request_set_pixmap_video", self.LabelVideoSetPixmap)
        
        event_manager.subscribe("request_label_width_image", self.GetLabelWidthImage)
        event_manager.subscribe("request_label_height_image", self.GetLabelHeightImage)
        event_manager.subscribe("request_set_pixmap_image", self.LabelImageSetPixmap)

        
    def GetLabelWidthVideo(self):
        label_width = self.label_video.width()
        return label_width
    
    def GetLabelHeightVideo(self):
        label_height = self.label_video.height()
        return label_height
        
    def LabelVideoSetPixmap(self, image_RGB):
        height, width, ch = image_RGB.shape        
        q_image = QImage(image_RGB.data, width, height, ch * width, QImage.Format_RGB888)
        
        label_height = self.label_video.height()
        label_width = self.label_video.width()
        
        image_aspect_ratio = q_image.width() / q_image.height()
        scaled_width = label_width
        scaled_height = int(scaled_width / image_aspect_ratio)
        if scaled_height > label_height:
            scaled_height = label_height
            scaled_width = int(scaled_height * image_aspect_ratio)
        scaled_image = q_image.scaled(scaled_width, scaled_height, aspectRatioMode=Qt.KeepAspectRatio) 
          
        self.label_video.setPixmap(QPixmap.fromImage(scaled_image))
     
    def GetLabelWidthImage(self):
        label_width = self.label_Image.width()
        return label_width
    
    def GetLabelHeightImage(self):
        label_height = self.label_Image.height()
        return label_height

        
    def LabelImageSetPixmap(self, image_RGB):
        height, width, ch = image_RGB.shape        
        q_image = QImage(image_RGB.data, width, height, ch * width, QImage.Format_RGB888)


        label_height = self.label_Image.height()
        label_width = self.label_Image.width()
        
        
        image_aspect_ratio = q_image.width() / q_image.height()
        scaled_width = label_width
        scaled_height = int(scaled_width / image_aspect_ratio)
        if scaled_height > label_height:
            scaled_height = label_height
            scaled_width = int(scaled_height * image_aspect_ratio)
        scaled_image = q_image.scaled(scaled_width, scaled_height, aspectRatioMode=Qt.KeepAspectRatio)    
         
         
         
        self.label_Image.setPixmap(QPixmap.fromImage(scaled_image))

