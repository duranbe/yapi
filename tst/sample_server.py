from src.response import Response
from src.response.statuses import HTTP_200
from src.server import Server

server = Server("localhost", 4221)


@server.endpoint("/test")
def print_value():
    response = Response(status=HTTP_200, headers={}, body="test")._as_bytes()
    return response


if __name__ == "__main__":
    server.run()
