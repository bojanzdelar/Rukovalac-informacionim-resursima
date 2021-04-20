import json
from config.config import read_config

def read_meta():
    path = read_config()["meta"]
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def save_meta(meta):
    path = read_config()["meta"]
    with open(path, "w", encoding="utf-8") as file:
        json.dump(meta, file, indent=4)

def get_files(file_type, file_organization):
    return list(read_meta()[file_type][file_organization].keys())

def get_folders():
    return read_meta()["folders"]

def get_file_meta(file_name, file_organization):
    for key, item in read_meta().items():
        if file_organization in item and file_name in item[file_organization]:
            return key, item

def get_file_display(file_name, file_organization):
    _, meta = get_file_meta(file_name, file_organization)
    return meta[file_organization][file_name] if meta else ""

def get_file_tab_name(file_name, file_organization):
    return get_file_display(file_name, file_organization) + " - " + file_organization[0:3]

def get_folder_display(folder_name):
    return read_meta()["folders"][folder_name]

def is_in_meta(file_name, file_organization):
    for item in read_meta().values():
        if file_organization in item and file_name in item[file_organization]:
            return True
    return False

def folder_in_meta(folder_name):
    return folder_name in get_folders()

def same_file_meta(file_name_1, file_name_2, file_organization):
    return get_file_meta(file_name_1, file_organization) == get_file_meta(file_name_2, file_organization)

def add_file(file_name, file_display, file_type, file_organization):
    meta = read_meta()
    file_meta = meta[file_type]
    file_meta[file_organization][file_name] = file_display
    meta[file_type] = file_meta
    save_meta(meta)

def remove_file(file_name, file_organization):
    meta = read_meta()
    key, file_meta = get_file_meta(file_name, file_organization)
    del file_meta[file_organization][file_name]
    meta[key] = file_meta
    save_meta(meta)