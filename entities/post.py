import json


class Post:

    def __init__(self):
        self.name = "Vasya"
        self.image = 123

    def get_name(self):
        return self.name

    def get_image(self):
        return self.image

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
