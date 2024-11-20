from backend.file_managment.file_management import FileManagement

from .folder_check import FolderCheck
from .load_language import LoadLanguage
from .open_settings import OpenSettings
from .check_for_updates import CheckUpdate

file_mangement = FileManagement()
update_checker = CheckUpdate()

def check_updates():
    update_version, update_description = update_checker.CheckUpdateSoftware()
    return update_version, update_description
    

def check_folders():
    FolderCheck(file_mangement)

def open_setting():
    OpenSettings(file_mangement)

def load_languages():
    LoadLanguage(file_mangement)