import tomllib
from pathlib import Path

class ConfigHandler():
    def __init__(self):
        with open('config.toml', "rb") as f:
            data = tomllib.load(f)
        data = data['database']
        d = {}
        for x in data:
            if x['name'] in d: 
                raise ValueError
            d[x['name']] = x 
            del d[x['name']]['name']
        print(d)

    def get(self, item: str):
        pass
