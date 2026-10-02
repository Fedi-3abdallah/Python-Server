from typing import Callable, Dict, Tuple
from http_parser import HTTPRequest
from response import HTTPResponse


class Router:
    def __init__(self):
        self.routes: Dict[Tuple[str, str], Callable] = {}

    def add_route(self, method: str, path: str, handler: Callable):
        self.routes[(method.upper(), path)] = handler

    async def handle_request(self, request: HTTPRequest) -> HTTPResponse:
        handler = self.routes.get((request.method, request.path))
        if handler:
            try:
                return await handler(request)
            except Exception as e:
                return HTTPResponse.json(
                    {"error": "Internal Server Error", "details": str(e)},
                    status_code=500,
                )

        return HTTPResponse.json({"error": "Route Not Found"}, status_code=404)
