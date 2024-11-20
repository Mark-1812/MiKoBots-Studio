import platform
from pathlib import Path
import ctypes
import os
import sys
from ctypes import wintypes
import locale

class FileManagement:
    def __init__(self):
        os_system = platform.system()
        self.platform = os_system

        # Set the documents folder name based on the language
        documents_folder = "Documents"  # Default to English

        if os_system == "Darwin":
            # macOS-specific code
            self.file_path = Path.home() / documents_folder / "MyAppData" / "MiKoBots"
        elif os_system == "Windows":
            # Windows-specific code
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(wintypes.MAX_PATH + 1)
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                self.file_path = Path(buf.value) / "MyAppData" / "MiKoBots"
            else:
                self.file_path = None
        elif os_system == "Linux":
            # Linux and other platforms
            self.file_path = Path.home() / "Documents" / "MyAppData" / "MiKoBots"
        
    def GetPathFolder(self):
        os_system = platform.system()
        self.platform = os_system
        
        if os_system == "Darwin":
            # macOS-specific code
            file_path = Path.home() / "Documents" / "MyAppData"
        elif os_system == "Windows":
            # Windows-specific code
            dll = ctypes.windll.shell32
            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH + 1)
            if dll.SHGetSpecialFolderPathW(None, buf, 0x0005, False):
                file_path = Path(buf.value) / "MyAppData"
            else:
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
    
    def LanguagePath(self, language):
        try:
            if self.platform == "Windows":
                base_path = os.path.dirname(sys.executable)
                language_path = os.path.join(base_path, 'assets', 'language', language)
                language_path = os.path.normpath(language_path)
            else:
                base_path = os.path.dirname(os.path.dirname(sys.executable))
                language_path= os.path.join(base_path, 'Resources', 'assets', 'language', language)
                language_path = os.path.normpath(language_path)
            
        except AttributeError:
            pass

        return language_path

    # Function to get the correct path to the assets directory
    def resource_path(self, image):
        """ Get the absolute path to the resource (image file). Handles PyInstaller's temp folder. """
        try:
            if self.platform == "Windows":
                base_path = os.path.dirname(sys.executable)
                image_path = os.path.join(base_path, 'assets', 'images', image)
                image_path = os.path.normpath(image_path)
            else:
                base_path = os.path.dirname(os.path.dirname(sys.executable))
                image_path = os.path.join(base_path, 'Resources', 'assets', 'images', image)
                image_path = os.path.normpath(image_path)
            
        except AttributeError:
            # If not bundled, use the current directory
            current_directory= os.path.dirname(__file__)
            
            image_path = os.path.join(current_directory, '../../..', 'assets', 'images', image)
            image_path = os.path.normpath(image_path)
            
        
        return image_path
