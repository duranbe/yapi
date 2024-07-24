import argparse

from src.response.response import Response
from src.request.request import Request
from src.server.server import Server
from src.response.statuses import HTTP_200, HTTP_404


def process(sock, addr):
    request = Request(sock.recv(4096))
    print(request, request.method)
    request_endpoint = request.endpoint
    headers = request.headers
    print(headers)

    if request.endpoint == "/":
        response = Response(status=HTTP_200, headers={}, body=None)._as_bytes()
        sock.send(response)

    elif "/echo/" in request_endpoint:
        body = "<html><h2>" + request.endpoint.split("/")[2] + "</h2></html>"
        response_headers = {"Content-Type": "text/html; charset=utf-8"}
        response = Response(
            status=HTTP_200, headers=response_headers, body=body
        )._as_bytes()

        sock.send(response)
    else:
        response = Response(status=HTTP_404, headers={}, body=None)._as_bytes()
        sock.send(response)

    sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--port", dest="port", type=int, help="port to run server", default=4221
    )
    args = parser.parse_args()

    server = Server("localhost", args.port, process=process)


if __name__ == "__main__":
    main()
