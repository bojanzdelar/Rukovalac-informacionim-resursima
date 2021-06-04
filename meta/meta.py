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

def get_information_resources(name, data_type):
    return list(read_meta()[name][data_type].keys())

def get_folders():
    return read_meta()["folders"]

def get_meta(name, data_type):
    for key, item in read_meta().items():
        if data_type in item and name in item[data_type]:
            return key, item

def get_display(name, data_type):
    _, meta = get_meta(name, data_type)
    return meta[data_type][name] if meta else ""

def get_tab_name(name, data_type):
    return get_display(name, data_type) + " - " + data_type[0:3]

def get_folder_display(folder_name):
    return read_meta()["folders"][folder_name]

def is_in_meta(name, data_type):
    for item in read_meta().values():
        if data_type in item and name in item[data_type]:
            return True
    return False

def folder_in_meta(folder_name):
    return folder_name in get_folders()

def same_meta(name_1, name_2, data_type):
    return get_meta(name_1, data_type) == get_meta(name_2, data_type)

def add_file(file_name, file_display, file_type, file_organization):
    meta = read_meta()
    file_meta = meta[file_type]
    file_meta[file_organization][file_name] = file_display
    meta[file_type] = file_meta
    save_meta(meta)

def remove_file(name, data_type):
    meta = read_meta()
    key, file_meta = get_meta(name, data_type)
    del file_meta[data_type][name]
    meta[key] = file_meta
    save_meta(meta)