from src.response import Response
from src.response.statuses import HTTP_200
from src.server import Server

server = Server("localhost", 4221)


@server.endpoint("/test", allowed_methods=["GET"])
def print_value():
    return Response(status=HTTP_200, headers={}, body="test")


if __name__ == "__main__":
    server.run()
