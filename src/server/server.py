import socket
import threading

from src.request.request import Request
from src.response.response import Response
from src.response.statuses import HTTP_404


class Server:
    def __init__(self, hostname: str, port: int) -> None:
        self.address_function_map = {}
        self.socket = socket.socket()

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_address = ("localhost", port)
        self.socket.bind(server_address)
        self.socket.listen()

    def endpoint(self, path):
        def decorator(func):
            def wrapper(sock, request):
                sock.send(func())
                sock.close()
                return

            self.address_function_map[path] = wrapper

            return wrapper

        return decorator

    def run(self):
        while True:
            sock, addr = self.socket.accept()
            request = Request(sock.recv(4096))
            if request.endpoint not in self.address_function_map:
                sock.send(Response(HTTP_404, {}, None)._as_bytes())
                sock.close()
            else:
                to_execute = self.address_function_map[request.endpoint]
                t = threading.Thread(target=lambda: to_execute(sock, request))
                t.start()
