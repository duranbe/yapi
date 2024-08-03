import argparse

from src.response import Response
from src.server import Server
from src.response.statuses import HTTP_200

parser = argparse.ArgumentParser()
parser.add_argument(
    "--port", dest="port", type=int, help="port to run server", default=4221
)
args = parser.parse_args()

server = Server("localhost", args.port)


@server.endpoint(path="/test", allowed_methods=["GET"])
def test_endpoint():
    return Response(status=HTTP_200, headers={}, body=None)


if __name__ == "__main__":
    server.run()
