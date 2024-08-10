from src.utils import CLRF
import re


HEADER_SPLITTER = ": "


class Request:
    def __init__(self, request: bytes) -> None:
        request: str = request.decode("utf-8")
        self._query_params_regex = re.compile("[\\?&]([^&=]+)=([^&=]+)")

        _request_line = request.split(CLRF)[0].split()
        self.headers = self._parse_headers(request)
        self.body = request.split(CLRF)[-1]

        self.method: str = _request_line[0]
        self._raw_endpoint: str = _request_line[1]
        self.endpoint: str = re.sub("\?.*$", "", _request_line[1])
        self.protocol: str = _request_line[2]

        self.query_params = self._parse_query_params()

    def _parse_headers(self, request) -> dict:
        splitted_request = request.split(CLRF)
        headers = {}
        for i in range(1, len(splitted_request) - 2):
            current_header = splitted_request[i]
            splitted_header = current_header.split(HEADER_SPLITTER)
            header_name = splitted_header[0]
            header_value = splitted_header[1]
            headers[header_name] = header_value

        return headers

    def _parse_query_params(self):
        results = self._query_params_regex.findall(self._raw_endpoint)
        return {k: v for k, v in results}
