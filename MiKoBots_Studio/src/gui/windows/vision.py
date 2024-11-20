from PyQt5.QtWidgets import QMessageBox, QLabel, QSizePolicy, QCheckBox, QLineEdit, QSpacerItem, QTabWidget, QWidget, QRadioButton, QGridLayout, QScrollArea, QVBoxLayout, QFrame, QComboBox, QFileDialog
from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtGui import QImage, QPixmap, QColor, QDoubleValidator

from backend.core.event_manager import event_manager

from gui.style import *

class VisionWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Vision")
        self.setGeometry(100, 100, 400, 300)
        self.setStyleSheet(style_widget)
        
        layout = QVBoxLayout(self)
        
        
        # Create the label to display the frame
        self.label_Image = QLabel("No camera connected")
        self.label_Image.setStyleSheet(style_label)
        self.label_Image.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(self.label_Image)

        
        self.label_video = QLabel("No camere connected")
        self.label_video.setStyleSheet(style_label)
        self.label_video.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        layout.addWidget(self.label_video)
        
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
        try:
            height, width, ch = image_RGB.shape        
            q_image = QImage(image_RGB.data, width, height, ch * width, QImage.Format_RGB888)
            
            self.label_video.setPixmap(QPixmap.fromImage(q_image))
        except:
            pass
        
    def GetLabelWidthImage(self):
        label_width = self.label_Image.width()
        return label_width
    
    def GetLabelHeightImage(self):
        label_height = self.label_Image.height()
        return label_height

        
    def LabelImageSetPixmap(self, image_RGB):
        height, width, ch = image_RGB.shape        
        q_image = QImage(image_RGB.data, width, height, ch * width, QImage.Format_RGB888)
         
        self.label_Image.setPixmap(QPixmap.fromImage(q_image))

