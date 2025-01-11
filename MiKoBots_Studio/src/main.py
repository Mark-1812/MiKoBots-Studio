import sys
from PyQt5.QtWidgets import QApplication,  QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from PyQt5.QtCore import  QThread,  pyqtSignal
from gui.windows.start_up_screen import StartupScreen
from gui.windows.update_window import UpdateChecker
from backend.open_program import check_folders, check_updates, open_setting, load_languages
from gui.main_window import MainWindow

CURRENT_VERSION = 1.14 

class StartupWorker(QThread):
    version = pyqtSignal(float, str)

    def run(self): 
        update_version, update_description = check_updates()
        check_folders()
        load_languages()

        self.version.emit(update_version, update_description)

def updateScreen(update_version, update_description):
    if update_version > CURRENT_VERSION:
        update_window = UpdateChecker(update_description, update_version, CURRENT_VERSION)
        update_window.exec_() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    QGuiApplication.setAttribute(Qt.AA_EnableHighDpiScaling)  # Enable high DPI scaling
    QGuiApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  
     
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    

    primary_screen = app.primaryScreen()
    screen_geometry = primary_screen.geometry()
    
    startup_screen = StartupScreen(screen_geometry, CURRENT_VERSION)
    startup_screen.show()
    
    startup_worker = StartupWorker()
    startup_worker.finished.connect(lambda: startup_screen.accept())
    startup_worker.finished.connect(lambda: main_window.ShowMainWindow(file_path))
    startup_worker.version.connect(lambda version, description: updateScreen(version, description))
    startup_worker.start()

    main_window = MainWindow(screen_geometry, CURRENT_VERSION)

    sys.exit(app.exec_())

    
    