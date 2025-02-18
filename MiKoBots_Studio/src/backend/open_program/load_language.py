import json
import backend.core.variables as var
from pathlib import Path
from backend.file_managment import get_language_path

def LoadLanguage():
    
    path = get_language_path('en')
    # print(path)

    # path = '/Users/markkleinjan/Library/CloudStorage/OneDrive-MiKoBots/Documenten - MiKoBots/General/Besturing/software/Mikobots studio/MiKoBots_Studio/assets/Language'
    # path = 'C:/Users/MarkKleinJan/OneDrive - MiKoBots/Documenten - MiKoBots/General/Besturing/software/Mikobots studio/MiKoBots_Studio/assets/Language/en'
    # path = 'C:/Users/klein/OneDrive - MiKoBots/Documenten - MiKoBots/General/Besturing/software/Mikobots studio/MiKoBots_Studio/assets/Language/en'
    lan_path = Path(path+".json")
    
    # print(lan_path)
    try:
        with open(lan_path, "r", encoding="utf-8") as f:
            var.LANGUAGE_DATA = json.load(f)
    except:
        print("Error: Could not find the language file")