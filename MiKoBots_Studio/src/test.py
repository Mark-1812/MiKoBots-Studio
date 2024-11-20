from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QComboBox Popup Width Adjustment")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout(self)

        # Create a QComboBox with items
        self.combo_box = QComboBox(self)
        self.combo_box.addItems([
            "Short", 
            "A bit longer text", 
            "Much longer text that won't fit initially"
        ])
        self.combo_box.setMaximumWidth(100)
        layout.addWidget(self.combo_box)

        # Adjust popup width to fit contents
        self.combo_box.view().setMinimumWidth(self.get_popup_width())

    def get_popup_width(self):
        # Calculate the width needed for the longest item
        font_metrics = self.combo_box.fontMetrics()
        longest_item = max([font_metrics.width(self.combo_box.itemText(i)) for i in range(self.combo_box.count())])
        # Add some padding for aesthetics
        return longest_item + 20

# Create and run the application
app = QApplication([])
window = MyWindow()
window.show()
app.exec_()
