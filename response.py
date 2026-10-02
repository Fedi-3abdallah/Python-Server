import json
from typing import Dict, Union

STATUS_CODES = {
    200: "OK",
    201: "Created",
    400: "Bad Request",
    404: "Not Found",
    500: "Internal Server Error",
}


class HTTPResponse:
    def __init__(
        self,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        body: Union[str, bytes] = "",
    ):
        self.status_code = status_code
        self.headers = headers or {}
        self.body = body if isinstance(body, bytes) else body.encode("utf-8")

    def to_bytes(self) -> bytes:
        status_text = STATUS_CODES.get(self.status_code, "Unknown")
        response_line = f"HTTP/1.1 {self.status_code} {status_text}\r\n"

        if "content-length" not in self.headers:
            self.headers["Content-Length"] = str(len(self.body))
        if "connection" not in self.headers:
            self.headers["Connection"] = "close"

        header_lines = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        return (
            response_line.encode("utf-8")
            + header_lines.encode("utf-8")
            + b"\r\n"
            + self.body
        )

    @classmethod
    def json(cls, data: dict, status_code: int = 200) -> "HTTPResponse":
        body = json.dumps(data)
        headers = {"Content-Type": "application/json"}
        return cls(status_code=status_code, headers=headers, body=body)

    @classmethod
    def text(cls, text: str, status_code: int = 200) -> "HTTPResponse":
        headers = {"Content-Type": "text/plain"}
        return cls(status_code=status_code, headers=headers, body=text)
