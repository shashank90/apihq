from typing import List


class SpecParams:
    def __init__(self, spec_id: str, data_dir: str):
        self.spec_id = spec_id
        self.data_dir = data_dir

        # To avoid mutable defaults. Use None as default for list __init__
        # (Refer: https://stackoverflow.com/questions/13144433/why-is-instance-variable-behaving-like-a-class-variable-in-python)
        # if postman_collections:
        # self.postman_collections: List[PostmanCollection] = postman_collections
        # else:
        # self.postman_collections = []

    def get_spec_id(self):
        return self.spec_id

    def get_data_dir(self):
        return self.data_dir
