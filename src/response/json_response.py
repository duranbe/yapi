from src.exceptions.exceptions import ContentLengthNotMatchingException
from src.response.headers import CONTENT_LENGTH, CONTENT_TYPE
from src.response.response import Response
from src.utils import CLRF


class JsonResponse(Response):
    def __init__(self, status, headers, body):
        super().__init__(status=status, headers=headers, body=body)

    def _headers(self):
        if CONTENT_TYPE not in self.headers:
            self.headers[CONTENT_TYPE] = "application/json"
        if CONTENT_LENGTH not in self.headers:
            self.headers[CONTENT_LENGTH] = len(self.body)
        else:
            if self.headers[CONTENT_LENGTH] != len(self.body):
                raise ContentLengthNotMatchingException

        return CLRF.join(["{}: {}".format(h, v) for h, v in self.headers.items()])
