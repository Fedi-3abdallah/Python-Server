import urllib.parse
from typing import Dict, Optional, Tuple


class HTTPRequest:
    def __init__(
        self,
        method: str,
        path: str,
        query_params: Dict[str, str],
        headers: Dict[str, str],
        body: bytes,
    ):
        self.method = method
        self.path = path
        self.query_params = query_params
        self.headers = headers
        self.body = body

    @classmethod
    async def parse_from_stream(cls, reader) -> Optional["HTTPRequest"]:
        try:
            request_line = await reader.readline()
            if not request_line:
                return None

            request_line_str = request_line.decode("utf-8").strip()
            parts = request_line_str.split(" ")
            if len(parts) != 3:
                return None

            method, full_path, _ = parts
            parsed_url = urllib.parse.urlparse(full_path)
            path = parsed_url.path

            query_params = {}
            if parsed_url.query:
                query_params = {
                    k: v[0] for k, v in urllib.parse.parse_qs(parsed_url.query).items()
                }

            headers = {}
            while True:
                line = await reader.readline()
                if line == b"\r\n" or line == b"\n" or not line:
                    break
                header_str = line.decode("utf-8").strip()
                if ":" in header_str:
                    key, val = header_str.split(":", 1)
                    headers[key.strip().lower()] = val.strip()

            body = b""
            content_length = int(headers.get("content-length", 0))
            if content_length > 0:
                body = await reader.readexactly(content_length)

            return cls(method, path, query_params, headers, body)
        except Exception:
            return None
