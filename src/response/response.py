from src.exceptions.exceptions import ContentLengthNotMatchingException
from src.response.headers import CONTENT_LENGTH
from src.utils import CLRF

HTTP_PROTOCOL = "HTTP/1.1"


class Response:
    def __init__(self, status: str, headers: dict, body: str) -> None:
        self.status = status
        self.headers = headers
        self.body = "" if body is None else body
        self._response = "".join(
            [
                HTTP_PROTOCOL + " " + status,
                CLRF,
                self._headers(),
                CLRF,
                CLRF,
                str(self.body),
            ]
        )

    def _as_bytes(self):
        return self._response.encode()

    def _headers(self):
        if CONTENT_LENGTH not in self.headers:
            self.headers[CONTENT_LENGTH] = len(self.body)
        else:
            if self.headers[CONTENT_LENGTH] != len(self.body):
                raise ContentLengthNotMatchingException

        return CLRF.join(["{}: {}".format(h, v) for h, v in self.headers.items()])
