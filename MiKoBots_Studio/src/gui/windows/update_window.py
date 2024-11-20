from PyQt5.QtCore import QObject, pyqtSignal, QUrl, QFile, Qt
from PyQt5.QtWidgets import QDialog, QCheckBox, QDialog, QWidget, QMenu, QPushButton, QLabel, QScrollArea, QComboBox, QFrame, QGridLayout, QLineEdit, QFileDialog
from PyQt5.QtGui import  QDesktopServices, QPixmap
from backend.core.event_manager import event_manager
import os

from gui.style import *
from backend.file_managment.file_management import FileManagement

class UpdateChecker(QDialog):
    def __init__(self, update_des, update_version, cur_version, parent = None):
        super(UpdateChecker, self).__init__(parent)
        
        
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setStyleSheet("background-color: lightgray;")
        
        self.setWindowTitle("Update Checker")
        #self.move_to_center(screen_geometry)

        label = QLabel("New Version Available!")
        label.setStyleSheet(style_label_bold)
        layout.addWidget(label, 0, 0)
        
        label = QLabel(f"Current version: V{cur_version}")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 1, 0)

        label = QLabel(f"New version: V{update_version}")
        label.setStyleSheet(style_label)
        layout.addWidget(label, 2, 0)


        label = QLabel(f"The update contains the following:")
        label.setStyleSheet(style_label_bold)
        layout.addWidget(label, 3, 0)
        
        label = QLabel(update_des)
        label.setStyleSheet(style_label)
        label.setWordWrap(True)
        layout.addWidget(label, 4, 0, 2, 1)

        SpaceWidget = QWidget()
        SpaceWidget.setStyleSheet(style_widget)
        layout.addWidget(SpaceWidget, 6, 0)

        button = QPushButton("Go to the download page")
        button.setStyleSheet(style_button)
        layout.addWidget(button, 7, 0, 1 ,3)
        button.clicked.connect(self.open_website)
        
        SpaceWidget = QWidget()
        SpaceWidget.setStyleSheet(style_widget)
        layout.addWidget(SpaceWidget, 0, 1, layout.columnCount() - 1, 1)
        
        
        file_management = FileManagement()
        image_path = file_management.resource_path('studio.png')
        
        pixmap = QPixmap(image_path)
        
        self.image_label = QLabel()      
        self.image_label.setPixmap(pixmap) 

        layout.addWidget(self.image_label, 0, 2, 5, 1)
        
        
    def move_to_center(self, screen_geometry):
        """Centers the main window on the primary screen."""
        # Center the main window on the primary screen
        frame_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())      
           
    def subscribeToEvents(self):
        event_manager.subscribe("request_update_window", self.show_update_dialog)

    def open_website(self):
        try:
            url = QUrl("https://mikobots.com/downloads-mikobots-studio/")  # Replace with the desired URL
            QDesktopServices.openUrl(url)  # Open the URL in the default web browser
        except:
            pass


