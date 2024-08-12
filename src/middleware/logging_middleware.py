import logging

from src.middleware.middleware import Middleware
from src.request.request import Request
from src.response.response import Response


class LoggingMiddleware(Middleware):
    def _request_middleware(request: Request) -> Request:
        return request

    def _response_middleware(request: Request, response: Response) -> Response:
        logging.info(f"{request.method} {request.endpoint} -> {response.status}")
        return response
