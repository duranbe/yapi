import socket
import threading


class Server:
    def __init__(self, hostname: str, port: int, process: callable) -> None:
        s = socket.socket()

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        server_address = ("localhost", port)
        s.bind(server_address)
        s.listen()
        while True:
            sock, addr = s.accept()  # wait for client
            t = threading.Thread(target=lambda: process(sock, addr))
            t.start()
