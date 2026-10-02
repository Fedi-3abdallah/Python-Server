import asyncio
from http_parser import HTTPRequest
from response import HTTPResponse
from router import Router


class HTTPServer:
    def __init__(
        self, host: str = "127.0.0.1", port: int = 8080, router: Router = None
    ):
        self.host = host
        self.port = port
        self.router = router or Router()

    async def handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        try:
            request = await HTTPRequest.parse_from_stream(reader)
            if request:
                response = await self.router.handle_request(request)
            else:
                response = HTTPResponse.json({"error": "Bad Request"}, status_code=400)

            writer.write(response.to_bytes())
            await writer.drain()
        except Exception:
            pass
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        print(f"HTTP Web Server listening on http://{self.host}:{self.port}")
        async with server:
            await server.serve_forever()
