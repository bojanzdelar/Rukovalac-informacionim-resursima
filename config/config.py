import json

def read_config():
    with open("config/config.json", "r", encoding="utf-8") as file:
        return json.load(file)