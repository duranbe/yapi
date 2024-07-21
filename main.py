import socket
import threading
import argparse
import os
import gzip

from src.request.request import Request
from src.response.statuses import HTTP_200, HTTP_201, HTTP_404

ALLOWED_ENCODING = "gzip"


def process(sock, addr, doc_paths):
    request = Request(sock.recv(4096))
    print(request, request.method)
    request_type = request.method
    request_endpoint = request.endpoint
    # request_protocol = request_line.split()[2]
    headers = request.headers
    request_body = request.body
    print(headers)
    
    if request.endpoint == "/":
        print(HTTP_200)
        sock.send(HTTP_200)

    elif "/files/" in request_endpoint:
        filename = request.split(" ")[1].replace("/files/", "")

        if request_type == "POST":
            print(filename, request_body)

            if int(headers["Content-Length"]) != len(request_body):
                response = HTTP_404
            else:
                with open(doc_paths + filename, "w") as writer:
                    writer.write(request_body)
                response = HTTP_201

        if request_type == "GET":
            print(filename)
            data = ""
            if not os.path.isfile(doc_paths + filename):
                sock.send(HTTP_404)

            with open(doc_paths + filename, "r") as reader:
                line = reader.readline()
                while line != "":  # The EOF char is an empty string
                    data += line
                    line = reader.readline()

            response = str.encode(
                "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {}\r\n\r\n{}".format(
                    len(data), data
                )
            )
        sock.send(response)

    elif "/echo/" in request.split(" ")[1]:
        if headers.get("Accept-Encoding") is not None and ALLOWED_ENCODING in headers[
            "Accept-Encoding"
        ].split(", "):
            url = request.split(" ")[1].split("/")[2].encode()
            print(url)
            body = gzip.compress(url)
            response = (
                str.encode(
                    "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\nContent-Encoding: gzip\r\n\r\n".format(
                        len(body)
                    )
                )
                + body
            )
        else:
            url = request.split(" ")[1].split("/")[2]
            response = str.encode(
                "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(
                    len(url), url
                )
            )

        sock.send(response)
    elif "User-Agent" in headers.keys():
        data = headers["User-Agent"]
        response = str.encode(
            "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}".format(
                len(data), data
            )
        )
        sock.send(response)
    else:
        sock.send(HTTP_404)

    sock.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", dest="port", type=int, help="port to run server", default=4221)
    parser.add_argument("--directory", dest="doc_paths", type=str, help="path to doc")
    args = parser.parse_args()

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    server_address = ("localhost", args.port)
    s.bind(server_address)
    s.listen()
    while True:
        sock, addr = s.accept()  # wait for client
        t = threading.Thread(target=lambda: process(sock, addr, args.doc_paths))
        t.start()


if __name__ == "__main__":
    main()
