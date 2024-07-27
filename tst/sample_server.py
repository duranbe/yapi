from src.response.response import Response
from src.response.statuses import HTTP_200
from src.server.server import Server


def process(sock, addr):
    response = Response(status=HTTP_200, headers={}, body=b"test")._as_bytes()
    sock.send(response)
    sock.close()


if __name__ == "__main__":
    Server("localhost", 4221, process=process)
