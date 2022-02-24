from zapv2 import ZAPv2

from backend.utils.constants import ZAP_KEY

HOST = "http://localhost:8080"


class ZAP:
    def __init__(self, host, apikey=None):
        self.host = host
        self.zap = ZAPv2(proxies={"http": host}, apikey=apikey)

    def get_zap(self):
        return self.zap


# Global var (Keeping a single instance)
zap_instance = ZAP(host=HOST, apikey=ZAP_KEY)


def get_zap():
    return zap_instance.get_zap()
