import platform
from pathlib import Path
import ctypes

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
