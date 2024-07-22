from src.response.headers import CONTENT_LENGTH
from src.utils import CLRF


class Response:
    def __init__(self, status: str, headers: dict, body: str) -> None:
        self.status = status
        self.headers = headers
        self.body = body
        self._response = CLRF.join(
            ["HTTP/1.1 " + status, self._headers(), CLRF, str(self.body)]
        )

    def _send(self):
        pass

    def _as_bytes(self):
        return self._response.encode()

    def _headers(self):
        if CONTENT_LENGTH not in self.headers and self.body is not None:
            self.headers[CONTENT_LENGTH] = len(self.body)

        return CLRF.join(["${}: ${}".format(h, v) for h, v in self.headers.items()])
