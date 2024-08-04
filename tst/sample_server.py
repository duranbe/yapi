import json
from src.response import Response
from src.response import JsonResponse
from src.response import HtmlResponse
from src.response.statuses import HTTP_200
from src.server import Server

server = Server("localhost", 4221)


@server.endpoint("/test", allowed_methods=["GET"])
def print_value():
    return Response(status=HTTP_200, headers={}, body="test")

@server.endpoint("/test_json", allowed_methods=["GET"])
def print_value_json():
    return JsonResponse(status=HTTP_200, headers={}, body=json.dumps({"test": "json"}))

@server.endpoint("/test_html", allowed_methods=["GET"])
def print_value_html():
    return HtmlResponse(status=HTTP_200, headers={}, body="<html>test</html>")

if __name__ == "__main__":
    server.run()
