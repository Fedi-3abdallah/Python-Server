import argparse
import asyncio
import json
from http_parser import HTTPRequest
from response import HTTPResponse
from router import Router
from server import HTTPServer

router = Router()


async def home_handler(request: HTTPRequest) -> HTTPResponse:
    return HTTPResponse.text("Welcome to the Async HTTP Server from scratch!")


async def api_status_handler(request: HTTPRequest) -> HTTPResponse:
    return HTTPResponse.json(
        {
            "status": "online",
            "server": "AsyncioHTTP/1.0",
            "query_params": request.query_params,
        }
    )


async def echo_handler(request: HTTPRequest) -> HTTPResponse:
    try:
        data = json.loads(request.body.decode("utf-8")) if request.body else {}
        return HTTPResponse.json({"received": data}, status_code=201)
    except Exception:
        return HTTPResponse.json({"error": "Invalid JSON body"}, status_code=400)


router.add_route("GET", "/", home_handler)
router.add_route("GET", "/api/status", api_status_handler)
router.add_route("POST", "/api/echo", echo_handler)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Async HTTP Server")
    parser.add_argument(
        "-p", "--port", type=int, default=8080, help="Port to listen on (default: 8080)"
    )
    parser.add_argument(
        "-H",
        "--host",
        type=str,
        default="127.0.0.1",
        help="Host address (default: 127.0.0.1)",
    )
    args = parser.parse_args()

    server = HTTPServer(host=args.host, port=args.port, router=router)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServer shut down by user.")
