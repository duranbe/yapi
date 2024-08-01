from src.exceptions.exceptions import ContentLengthNotMatchingException
from src.response.headers import CONTENT_LENGTH, CONTENT_TYPE
from src.response.response import Response
from src.utils import CLRF


class HtmlResponse(Response):
    def __init__(self, status, headers, body):
        super().__init__(status=status, headers=headers, body=body)

    def _headers(self):
        if CONTENT_TYPE not in self.headers:
            self.headers[CONTENT_TYPE] = "text/html; charset=utf-8"
        if CONTENT_LENGTH not in self.headers:
            self.headers[CONTENT_LENGTH] = len(self.body)
            
        self._assert_content_length()

        return CLRF.join(["{}: {}".format(h, v) for h, v in self.headers.items()])
