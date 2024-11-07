



import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QSlider, QVBoxLayout, QWidget, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap


from gui.style import *

class ColorAdjuster(QMainWindow):
    def __init__(self, image_path, initial_hsv_ranges):
        super().__init__()

        # Load and convert the image to HSV
        self.image = cv2.imread(image_path)
        self.hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)

        # Initial HSV ranges
        self.hsv_ranges = initial_hsv_ranges

        # Set up the UI
        self.setWindowTitle('HSV Color Adjuster')
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout for sliders and image
        self.layout = QGridLayout(self.central_widget)

        # Label to display the resulting masked image
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label,0,0)

        # Create sliders for HSV ranges
        self.create_slider(1, 'Lower Hue', 0, 179, self.hsv_ranges[0], self.update_image)
        self.create_slider(2, 'Upper Hue', 0, 179, self.hsv_ranges[1], self.update_image)
        self.create_slider(3, 'Lower Sat', 0, 255, self.hsv_ranges[2], self.update_image)
        self.create_slider(4, 'Upper Sat', 0, 255, self.hsv_ranges[3], self.update_image)
        self.create_slider(5, 'Lower Val', 0, 255, self.hsv_ranges[4], self.update_image)
        self.create_slider(6, 'Upper Val', 0, 255, self.hsv_ranges[5], self.update_image)

        # Initial update to display the image
        self.update_image()

    def create_slider(self, row, name, min_val, max_val, init_val, callback):
        slider_layout = QGridLayout()
        
        # Label for the minimum value
        min_label = QLabel(str(min_val))
        min_label.setStyleSheet(style_label)
        min_label.setFixedWidth(10)
        slider_layout.addWidget(min_label, 0, 2)
        
        # Create a slider
        slider = QSlider(Qt.Horizontal)
        slider.setStyleSheet(style_slider)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(init_val)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(10)
        slider.valueChanged.connect(callback)
        slider.valueChanged.connect(lambda: self.updateLabel(name, slider.value()))
        slider.setObjectName(name)
        slider_layout.addWidget(slider, 0, 3)        

        # Label for the maximum value
        max_label = QLabel(str(max_val))
        max_label.setStyleSheet(style_label)
        max_label.setFixedWidth(20)
        slider_layout.addWidget(max_label, 0, 4)
        
        # Create a label to display the current slider value
        label = QLabel(f"{name}: ")
        label.setStyleSheet(style_label)
        label.setFixedWidth(120)
        slider_layout.addWidget(label, 0, 0)    
        
        value_label = QLabel(str(init_val))
        value_label.setObjectName(f"{name}_label")
        value_label.setStyleSheet(style_label)
        value_label.setFixedWidth(90)
        slider_layout.addWidget(value_label, 0, 1)        

        self.layout.addLayout(slider_layout, row, 0)
    
    def updateLabel(self, name, value):
        value_label = self.findChild(QLabel, f"{name}_label")
        if value_label:
            value_label.setText(str(value))

    def update_image(self):
        """Update the displayed image based on the current HSV slider values."""
        # Get HSV ranges from sliders
        lower_hue = self.findChild(QSlider, 'Lower Hue').value()
        upper_hue = self.findChild(QSlider, 'Upper Hue').value()
        lower_sat = self.findChild(QSlider, 'Lower Sat').value()
        upper_sat = self.findChild(QSlider, 'Upper Sat').value()
        lower_val = self.findChild(QSlider, 'Lower Val').value()
        upper_val = self.findChild(QSlider, 'Upper Val').value()
        

        # Define the lower and upper bounds as arrays
        lower_bound = np.array([lower_hue, lower_sat, lower_val])
        upper_bound = np.array([upper_hue, upper_sat, upper_val])

        # Create the mask and apply it to the image
        mask = cv2.inRange(self.hsv_image, lower_bound, upper_bound)
        masked_image = cv2.bitwise_and(self.image, self.image, mask=mask)

        # Convert the masked image to QImage format
        height, width, channel = masked_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(masked_image.data, width, height, bytes_per_line, QImage.Format_BGR888)

        # Display the image in the QLabel
        self.image_label.setPixmap(QPixmap.fromImage(q_image))

def main():
    app = QApplication(sys.argv)

    # Initial HSV range (e.g., red color range)
    initial_hsv_ranges = [0, 10, 100, 255, 100, 255]

    # Create and show the color adjuster window
    
    window = ColorAdjuster("C:/Users/MarkKleinJan/OneDrive - MiKoBots/Documenten - MiKoBots/General/Logo/LOGO vierkant.png", initial_hsv_ranges)
    window.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()


