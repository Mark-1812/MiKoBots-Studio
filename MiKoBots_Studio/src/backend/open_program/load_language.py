import json
import backend.core.variables as var
from pathlib import Path

def LoadLanguage(file_mangement):
    
    path = file_mangement.LanguagePath('en')
    # print(path)

    # path = '/Users/markkleinjan/Library/CloudStorage/OneDrive-MiKoBots/Documenten - MiKoBots/General/Besturing/software/Mikobots studio/MiKoBots_Studio/assets/Language'
    path = 'C:/Users/MarkKleinJan/OneDrive - MiKoBots/Documenten - MiKoBots/General/Besturing/software/Mikobots studio/MiKoBots_Studio/assets/Language/en'
    lan_path = Path(path+".json")
    
    print(f"lanmgouge path {lan_path}")

    try:
        with open(lan_path, "r", encoding="utf-8") as f:
            var.LANGUAGE_DATA = json.load(f)
    except:
        print("could not find the language file")