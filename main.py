import argparse

from src.response.html_response import HtmlResponse
from src.response.response import Response
from src.request.request import Request
from src.server.server import Server
from src.response.statuses import HTTP_200, HTTP_404


def process(sock, addr):
    request = Request(sock.recv(4096))
    print(request.method, request.endpoint)
    request_endpoint = request.endpoint

    if request.endpoint == "/":
        response = Response(status=HTTP_200, headers={}, body=None)._as_bytes()
        sock.send(response)

    elif "/echo/" in request_endpoint:
        body = "<html><h2>" + request.endpoint.split("/")[2] + "</h2></html>"
        response = HtmlResponse(status=HTTP_200, headers={}, body=body)._as_bytes()
        sock.send(response)
    else:
        response = Response(status=HTTP_404, headers={}, body=None)._as_bytes()
        sock.send(response)

    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", dest="port", type=int, help="port to run server", default=4221
    )
    args = parser.parse_args()

    Server("localhost", args.port, process=process)
