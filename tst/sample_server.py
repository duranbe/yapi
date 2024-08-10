import json
from src.request.request import Request
from src.response import Response
from src.response import JsonResponse
from src.response import HtmlResponse
from src.response.statuses import HTTP_200
from src.server import Server

server = Server("localhost", 4221)


@server.endpoint("/test", allowed_methods=["GET"])
def endpoint(request: Request):
    return Response(status=HTTP_200, headers={}, body="test")


@server.endpoint("/echo/<value1>/", allowed_methods=["GET"])
def echo_value(request: Request, value1: str):
    return Response(status=HTTP_200, headers={}, body=value1)


@server.endpoint("/query_params", allowed_methods=["GET"])
def query_params_in_request(request: Request):
    print(request.query_params)
    return Response(status=HTTP_200, headers={}, body=str(request.query_params))


@server.endpoint("/test_json", allowed_methods=["GET"])
def json_endpoint(request: Request):
    return JsonResponse(status=HTTP_200, headers={}, body=json.dumps({"test": "json"}))


@server.endpoint("/test_html", allowed_methods=["GET"])
def html_endpoint(request: Request):
    return HtmlResponse(status=HTTP_200, headers={}, body="<html>test</html>")


if __name__ == "__main__":
    server.run()
