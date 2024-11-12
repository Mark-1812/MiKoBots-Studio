from PyQt5.QtCore import QTranslator, QLocale, QCoreApplication
from PyQt5.QtWidgets import QApplication, QMainWindow, QComboBox, QVBoxLayout, QWidget, QLabel
import sys

class LanguageManager:
    def __init__(self, app):
        self.app = app
        self.translator = QTranslator()

    def set_language(self, language_code):
        # Unload any previous translation
        self.app.removeTranslator(self.translator)
        
        # Load new translation file based on language code
        translation_file = f"translations_{language_code}.qm"
        if self.translator.load(translation_file):
            self.app.installTranslator(self.translator)
            print(f"Language set to {language_code}")
        else:
            print(f"Failed to load language file for {language_code}")

class MainWindow(QMainWindow):
    def __init__(self, language_manager):
        super().__init__()
        self.language_manager = language_manager
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Language Example"))

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        self.setCentralWidget(central_widget)

        # Label to display translated text
        self.label = QLabel(QCoreApplication.translate("MainWindow", "Hello, world!"))
        layout.addWidget(self.label)

        # Dropdown for language selection
        self.language_combo = QComboBox()
        self.language_combo.addItem("English", "en")
        self.language_combo.addItem("Spanish", "es")
        self.language_combo.currentIndexChanged.connect(self.change_language)
        layout.addWidget(self.language_combo)

    def change_language(self):
        language_code = self.language_combo.currentData()
        self.language_manager.set_language(language_code)
        self.update_texts()

    def update_texts(self):
        # Update all translatable texts
        self.setWindowTitle(QCoreApplication.translate("MainWindow", "Language Example"))
        self.label.setText(QCoreApplication.translate("MainWindow", "Hello, world!"))

# Main Application
app = QApplication(sys.argv)

# Initialize Language Manager
language_manager = LanguageManager(app)

# Create and show main window
main_window = MainWindow(language_manager)
main_window.show()

sys.exit(app.exec_())
