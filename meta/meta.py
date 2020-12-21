import json

def read_meta():
    with open("meta/meta.json", "r", encoding="utf-8") as file:
        return json.load(file)