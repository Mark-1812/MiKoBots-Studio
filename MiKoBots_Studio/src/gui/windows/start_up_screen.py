import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import os

from gui.style import *

import backend.core.variables as var
from backend.file_managment import get_image_path

class StartupScreen(QDialog):
    def __init__(self, screen_geometry, current_version):
        
        super().__init__()
        self.setWindowTitle("Starting Up")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
        self.setModal(True)  # Prevent user interaction with other windows
        self.setWindowModality(Qt.ApplicationModal)  # Block other windows
        self.setStyleSheet("background-color: white;")

        # Set up layout and widgets
        layout = QVBoxLayout()


        image_path = get_image_path('start_up.png')
        pixmap = QPixmap(image_path)
        


        # Add a text label
        text_label = QLabel(f"Version V{current_version}", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet(style_label)
        layout.addWidget(text_label)
        
        # add picture
        image_label = QLabel()      
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)

        # Add a text label
        text_label = QLabel("The program is starting, please wait...", self)
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setStyleSheet(style_label)
        layout.addWidget(text_label)
        
        # Set layout
        self.setLayout(layout)

        # Set size and center the startup screen on the same monitor as main window
        self.resize(400, 300)
        self.move_to_center(screen_geometry)

    def move_to_center(self, screen_geometry):
        """Centers the dialog on the primary screen."""
        # Center the window on the primary screen
        frame_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    # Override the closeEvent to prevent closing
    def closeEvent(self, event):
        event.ignore()