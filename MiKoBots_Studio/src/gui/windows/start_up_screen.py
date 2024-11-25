import sys
from PyQt5.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
import os

import backend.core.variables as var
from backend.file_managment.file_management import FileManagement

class StartupScreen(QDialog):
    def __init__(self, screen_geometry, current_version):
        file_management = FileManagement()
        
        super().__init__()
        self.setWindowTitle("Starting Up")
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
        self.setModal(True)  # Prevent user interaction with other windows
        self.setWindowModality(Qt.ApplicationModal)  # Block other windows
        self.setStyleSheet("background-color: white;")

        # Set up layout and widgets
        layout = QVBoxLayout()


        file_management = FileManagement()
        image_path = file_management.resource_path('start_up.png')
        pixmap = QPixmap(image_path)
        
        image_label = QLabel()      
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

        # Add a text label
        text_label = QLabel(f"Version V{current_version}", self)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(text_label)

        # Add a text label
        text_label = QLabel("The program is starting, please wait...", self)
        text_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
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