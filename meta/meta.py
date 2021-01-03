import json
from config.config import read_config

def read_meta():
    path = read_config()["meta"]
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)