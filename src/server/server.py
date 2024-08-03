import socket
import threading

from src.request import Request
from src.response import Response
from src.response.statuses import HTTP_404, HTTP_405


class Server:
    def __init__(self, hostname: str, port: int) -> None:
        self.address_function_map = {}
        self.socket = socket.socket()

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_address = ("localhost", port)
        self.socket.bind(server_address)
        self.socket.listen()

    def endpoint(self, path, allowed_methods):
        def decorator(func):
            def wrapper(sock, request):
                response = func()._as_bytes()
                sock.send(response)
                sock.close()
                return

            self.address_function_map[path] = {
                "function": wrapper,
                "allowed_methods": allowed_methods,
            }

            return wrapper

        return decorator

    def run(self):
        while True:
            sock, addr = self.socket.accept()
            request = Request(sock.recv(4096))
            if request.endpoint not in self.address_function_map:
                sock.send(Response(HTTP_404, {}, None)._as_bytes())
                sock.close()
                continue

            url_mapping = self.address_function_map[request.endpoint]

            if request.method not in url_mapping["allowed_methods"]:
                allow_headers = ",".join(url_mapping["allowed_methods"])
                sock.send(
                    Response(HTTP_405, {"Allow": allow_headers}, None)._as_bytes()
                )
                sock.close()
                continue

            to_execute = url_mapping["function"]
            threading.Thread(target=lambda: to_execute(sock, request)).start()
