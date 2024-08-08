import socket
import threading
import logging
import re

from src.request import Request
from src.response import Response
from src.response.statuses import HTTP_404, HTTP_405


class Server:
    def __init__(self, hostname: str, port: int) -> None:
        self.address_function_map = {}
        self.regex_function_map = {}
        self.socket = socket.socket()
        logging.basicConfig(level=logging.INFO)
        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().handlers[0].setFormatter(
            logging.Formatter("\n" + hostname + ":" + str(port) + " %(message)s")
        )

        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_address = (hostname, port)
        self.socket.bind(server_address)
        self.socket.listen()

        self.url_matcher = re.compile(r"(<\w+>)+")

    def endpoint(self, path, allowed_methods):
        def decorator(func):
            def wrapper(**kwargs):
                return func(**kwargs)

            parameters = self.url_matcher.findall(path)

            if parameters:
                params = [p.strip("<>") for p in parameters]
                regex_endpoint = re.sub(r"(<\w+>)", "(\\\w+)", path)

                self.regex_function_map[re.compile(regex_endpoint)] = {
                    "function": wrapper,
                    "allowed_methods": allowed_methods,
                    "params": params,
                }

            else:
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

            logging.info(f"{request.method} {request.endpoint}")

            for compiled_regex in self.regex_function_map.keys():
                if compiled_regex.search(request.endpoint):
                    values = compiled_regex.search(request.endpoint).groups()
                    url_mapping = self.regex_function_map[compiled_regex]

                    params_mapping = {}
                    for k, v in zip(url_mapping["params"], values):
                        params_mapping[k] = v

                    to_execute = url_mapping["function"]

                    def f(sock, request):
                        response = to_execute(**params_mapping)
                        sock.send(response._as_bytes())
                        sock.close()

                    threading.Thread(target=lambda: f(sock, request)).start()
                    return

            if request.endpoint not in self.address_function_map:
                sock.send(Response(HTTP_404, {}, None)._as_bytes())
                sock.close()
                continue

            url_mapping = self.address_function_map[request.endpoint]

            self._allowed_methods_check(
                sock, request.method, url_mapping["allowed_methods"]
            )

            to_execute = url_mapping["function"]

            def f(sock, request):
                response = to_execute()
                sock.send(response._as_bytes())
                sock.close()

            threading.Thread(target=lambda: f(sock, request)).start()

    def _allowed_methods_check(
        self, sock: socket, method: str, allowed_method: list[str]
    ):
        if method not in allowed_method:
            allow_headers = ",".join(allowed_method)
            sock.send(Response(HTTP_405, {"Allow": allow_headers}, None)._as_bytes())
            sock.close()
            raise Exception("no method supported")
