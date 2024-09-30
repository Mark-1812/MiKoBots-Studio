import platform
from pathlib import Path
import ctypes
import os
import sys

from backend.core.event_manager import event_manager

import backend.core.variables as var

class FileManagement:
    def __init__(self):
        os_system = platform.system()
        self.platform = os_system
        
        if os_system == "darwin":
            # macOS-specific code
            self.file_path = Path.home() / "Documents" / "MyAppData" / "MiKoBots"
        elif os_system == "Windows":
            # Windows-specific code
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH + 1)
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                self.file_path = Path(buf.value) / "MyAppData" / "MiKoBots"
            else:
                print("Failure!")
                self.file_path = None
        elif os_system == "Linux":
            # Linux and other platforms
            self.file_path = Path.home() / "Documents" / "MyAppData" / "MiKoBots"
        
    def GetPathFolder(self):
        os_system = platform.system()
        self.platform = os_system
        
        if os_system == "darwin":
            # macOS-specific code
            file_path = Path.home() / "Documents" / "MyAppData"
        elif os_system == "Windows":
            # Windows-specific code
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH + 1)
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                file_path = Path(buf.value) / "MyAppData"
            else:
                print("Failure!")
                file_path = None
        elif os_system == "Linux":
            # Linux and other platforms
            file_path = Path.home() / "Documents" / "MyAppData"   
            
        return file_path    
            
            
        
    def GetFilePath(self, file):
        # Get the name of the folder of the current robot
        if self.platform == "Windows":
            file_path = Path(str(self.file_path) + file)
        elif self.platform == "Darwin" or self.platform == "Linux":
            file_path = Path(str(self.file_path) + file).as_posix() 
        return file_path
    
    
    # Function to get the correct path to the assets directory
    def resource_path(self, image):
        """ Get the absolute path to the resource (image file). Handles PyInstaller's temp folder. """
        try:
            # When running as a PyInstaller bundle, _MEIPASS is created
            #base_path = sys._MEIPASS
            base_path = os.path.dirname(sys.executable)
            image_path = os.path.join(base_path, 'assets', 'images', image)
            image_path = os.path.normpath(image_path)
            
        except AttributeError:
            # If not bundled, use the current directory
            current_directory= os.path.dirname(__file__)
            
            image_path = os.path.join(current_directory, '../../..', 'assets', 'images', image)
            image_path = os.path.normpath(image_path)
            
            pass
        
        
        var.Test = str(image_path)
        
        return image_path
