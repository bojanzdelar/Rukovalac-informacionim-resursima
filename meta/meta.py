import json
from config.config import read_config

def read_meta():
    path = read_config()["meta"]
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_files(file_type, file_organization):
    return read_meta()[file_type][file_organization]

def get_folders():
    return read_meta()["folders"]

def get_file_meta(file_name, file_organization):
    for item in read_meta().values():
        if file_organization in item and file_name in item[file_organization]:
            return item

def get_file_display(file_name, file_organization):
    meta = get_file_meta(file_name, file_organization)
    return meta[file_organization][file_name] if meta else ""

def get_folder_display(folder_name):
    return read_meta()["folders"][folder_name]

def file_in_meta(file_name, file_organization):
    for item in read_meta().values():
        if file_organization in item and file_name in item[file_organization]:
            return True
    return False

def folder_in_meta(folder_name):
    return folder_name in get_folders()

def add_file(file_name, file_display, file_organization):
    ...

def remove_file(file_name, file_organization):
    ...