import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow
from gui.main_window import MainWindow
from PyQt5.QtCore import Qt, QTimer, QThread
from PyQt5.QtGui import QPixmap
from backend.core.event_manager import event_manager

from backend.core.open_program import FolderCheck
from backend.core.check_for_updates import CheckUpdate
import robot_library


from gui.start_up_screen import StartupScreen
        
class StartupWorker(QThread):
    """This class handles the startup process in the background."""
    def run(self): 
        update_checker = CheckUpdate()  
        update_checker.CheckUpdateSoftware()
        FolderCheck()
        
                  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    primary_screen = app.primaryScreen()
    screen_geometry = primary_screen.geometry()
    
    startup_screen = StartupScreen(screen_geometry)
    startup_screen.show()

    startup_worker = StartupWorker()
    startup_worker.finished.connect(lambda: main_window.show_main(startup_screen))
    startup_worker.start()

     
    main_window = MainWindow(screen_geometry) 


    sys.exit(app.exec_())