import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow

from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal
from backend.core.event_manager import event_manager

from  backend.open_program import check_folders, check_updates, open_setting, load_languages

import robot_library

from gui.main_window import MainWindow
from gui.windows.start_up_screen import StartupScreen
from backend.robot_management import setup_robot
import blockly

import backend.core.variables as var
from gui.windows.update_window import UpdateChecker
from backend.file_manager import open_file_from_path

CURRENT_VERSION = 1.11

           
class StartupWorker(QThread):
    version = pyqtSignal(float, str)
    # This class handles the startup process in the background.
    
    def run(self): 
        update_version, update_description = check_updates()
        check_folders()
        load_languages()
        
        ## later set style here
        
        self.version.emit(update_version, update_description)
    
def updateScreen(update_version, update_description):
    if update_version >= CURRENT_VERSION:
        update_window = UpdateChecker(update_description, update_version, CURRENT_VERSION)  # Create an instance of UpdateChecker as a dialog
        update_window.exec_()  # Show it as a modal dialog
            
def showMainWindow(file_path):
    main_window = MainWindow(screen_geometry) 
    main_window.show()  
    
    open_setting()
    
    setup_robot()
    
    
    if file_path:
        open_file_from_path(file_path)
     
                  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    
    primary_screen = app.primaryScreen()
    screen_geometry = primary_screen.geometry()
    
    startup_screen = StartupScreen(screen_geometry, CURRENT_VERSION)
    startup_screen.show()

    startup_worker = StartupWorker()
    startup_worker.finished.connect(lambda: startup_screen.accept())
    startup_worker.finished.connect(lambda: showMainWindow(file_path))
    startup_worker.version.connect(lambda version, description: updateScreen(version, description))
    startup_worker.start()
    
    sys.exit(app.exec_())