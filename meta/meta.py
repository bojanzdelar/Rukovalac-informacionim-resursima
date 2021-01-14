import json
from config.config import read_config

def read_meta():
    path = read_config()["meta"]
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)

def get_file_meta(file_name):
    for item in read_meta().values():
        if "files" in item and file_name in item["files"]:
            return item

def get_file_display(file_name):
    meta = get_file_meta(file_name)
    return meta["files"][file_name] if meta else ""

def file_in_meta(file_name):
    for item in read_meta().values():
        if "files" in item and file_name in item["files"]:
            return True
    return False
