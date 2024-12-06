from backend.file_managment.file_management import FileManagement
from .save_settings import SaveSettings


def run():
    file_management = FileManagement()

    SaveSettings(file_management)