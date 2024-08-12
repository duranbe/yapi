from abc import ABC, abstractmethod

from src.request.request import Request
from src.response.response import Response


class Middleware(ABC):
    def __init__(self) -> None:
        pass

    @abstractmethod
    def _request_middleware(request: Request):
        pass

    @abstractmethod
    def _response_middleware(request: Request, response: Response):
        pass
