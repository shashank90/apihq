from typing import Dict


class PostmanCollection:
    def __init__(self, path):
        self.path = path

    def get_path(self):
        return self.path

    def to_dict(self):
        return {"path": self.path}

    @classmethod
    def to_obj(cls, dct: Dict):
        return PostmanCollection(dct.get('path'))
