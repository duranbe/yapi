from src.utils import CLRF


class Request:
    def __init__(self, request: bytes) -> None:
        request = request.decode("utf-8")

        _request_line = request.split(CLRF)[0].split()
        self.headers = self._parse_headers(request)
        self.body = request.split(CLRF)[-1]

        self.method = _request_line[0]
        self.endpoint = _request_line[1]
        self.protocol = _request_line[2]

    def _parse_headers(request) -> dict:
        splitted_request = request.split(CLRF)
        headers = {}
        for i in range(1, len(splitted_request) - 2):
            current_header = splitted_request[i]
            header_name = current_header.split(": ")[0]
            header_value = current_header.split(": ")[1]
            headers[header_name] = header_value

        return headers
