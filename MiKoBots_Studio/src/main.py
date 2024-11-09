import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QApplication, QDialog, QLabel, QVBoxLayout, QMainWindow

from PyQt5.QtCore import Qt, QTimer, QThread
from backend.core.event_manager import event_manager

from  backend import open_program

import robot_library

from gui.main_window import MainWindow
from gui.windows.start_up_screen import StartupScreen

           
class StartupWorker(QThread):
    """This class handles the startup process in the background."""
    def run(self): 
        open_program.run()

                  
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    

    primary_screen = app.primaryScreen()
    screen_geometry = primary_screen.geometry()
    
    startup_screen = StartupScreen(screen_geometry)
    startup_screen.show()

    startup_worker = StartupWorker()
    startup_worker.finished.connect(lambda: main_window.show_main(startup_screen, file_path))
    startup_worker.start()
    
    main_window = MainWindow(screen_geometry) 
    
    sys.exit(app.exec_())