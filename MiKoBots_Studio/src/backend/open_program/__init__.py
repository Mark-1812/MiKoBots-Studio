from backend.file_managment.file_management import FileManagement

from .folder_check import FolderCheck
from .load_language import LoadLanguage
from .open_settings import OpenSettings
from .check_for_updates import CheckUpdate


def run():
    file_mangement = FileManagement()

    CheckUpdate()
    FolderCheck(file_mangement)
    LoadLanguage(file_mangement)
    OpenSettings(file_mangement)

