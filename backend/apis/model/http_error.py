class HttpResponse(Exception):
    def __init__(self, message: str, code: str, http_status: int, type: str):
        self.http_status = http_status
        self.message = message
        self.code = code
        self.type = type

    def get_http_status(self):
        return self.http_status
