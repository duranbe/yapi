from src.request.headers import parse_headers
from src.utils import CLRF


class Request:
    def __init__(self, request: bytes) -> None:
        request = request.decode("utf-8")

        _request_line = request.split(CLRF)[0].split()
        self.headers = parse_headers(request)
        self.body = request.split(CLRF)[-1]

        self.method = _request_line[0]
        self.endpoint = _request_line[1]
        self.protocol = _request_line[2]
