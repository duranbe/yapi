from src.utils import CLRF


class Response:
    def __init__(self, status: str, headers: dict, body: str) -> None:
        self.status = status
        self.headers = headers
        self.body = body
        self._response = CLRF.join(
            ["HTTP/1.1 " + status, self._headers(), CLRF, self.body]
        )

    def _send():
        pass

    def _headers(self):
        return CLRF.join(["${}: ${}".format(h, v) for h, v in self.headers.items()])
