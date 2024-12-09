from .file_management import FileManagement

management= FileManagement()

def get_path_folder():
    return management.GetPathFolder()

def get_file_path(file):
    return management.GetFilePath(file)

def get_language_path(language):
    return management.LanguagePath(language)

def get_image_path(image):
    return management.resource_path(image)

def get_platform():
    return management.platform