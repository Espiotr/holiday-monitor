import json


class Config:

    def __init__(self):

        with open("config.json", encoding="utf8") as file:
            self.data = json.load(file)

    def get(self, key):

        return self.data[key]