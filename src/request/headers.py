from ..utils import CLRF


ACCEPT_ENCODING = "Accept-Encoding"
CONTENT_LENGTH = "Content-Length"
CONTENT_TYPE = "Content-Type"
USER_AGENT = "User-Agent"


def parse_headers(request) -> dict:
    splitted_request = request.split(CLRF)
    headers = {}
    for i in range(1, len(splitted_request) - 2):
        current_header = splitted_request[i]
        header_name = current_header.split(": ")[0]
        header_value = current_header.split(": ")[1]
        headers[header_name] = header_value

    return headers
