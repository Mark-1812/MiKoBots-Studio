from backend.file_manager.save_open import SaveOpen

save_open = SaveOpen()

def save_file():
    save_open.SaveFile()
    
def save_as_file():
    save_open.SaveAsFile()
    
def open_file():
    save_open.OpenFile()
    
def new_file():
    save_open.NewFile()
    
def blockly_save(blockly):
    save_open.BlocklyConverting(blockly)
    
def open_file_from_path(file_path):
    save_open.OpenFileFromPath(file_path)
    