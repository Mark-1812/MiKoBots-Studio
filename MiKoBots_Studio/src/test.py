import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout, QLabel


class ExtraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Extra Window")
        self.setGeometry(200, 200, 400, 300)

        # Set up layout
        layout = QVBoxLayout()
        label = QLabel("This is the extra window.")
        layout.addWidget(label)
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 600, 400)

        # Button to open extra window
        self.button = QPushButton("Open Extra Window")
        self.button.clicked.connect(self.open_extra_window)

        # Set the central widget
        self.setCentralWidget(self.button)

        # Keep a reference to the extra window to avoid garbage collection
        self.extra_window = None

    def open_extra_window(self):
        if self.extra_window is None:
            self.extra_window = ExtraWindow()
        self.extra_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
