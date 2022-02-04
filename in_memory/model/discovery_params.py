from typing import List


class DiscoveryParams:
    def __init__(self, disc_id: str, disc_dir: str):
        self.disc_id = disc_id
        self.disc_dir = disc_dir

    def get_disc_id(self):
        return self.spec_id

    def get_disc_dir(self):
        return self.data_dir
