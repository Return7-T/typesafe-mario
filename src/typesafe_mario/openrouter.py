"""Adapt TypeSafe's native wire format to OpenRouter Decisions."""

import json

import httpx2


class OpenRouterTransport(httpx2.BaseTransport):
    def __init__(self, transport: httpx2.BaseTransport | None = None) -> None:
        self._transport = transport or httpx2.HTTPTransport()

    def handle_request(self, request: httpx2.Request) -> httpx2.Response:
        body = json.loads(request.read())
        for question in body["questions"].values():
            if not isinstance(question["instructions"], str):
                question["instructions"] = json.dumps(question["instructions"])
        headers = dict(request.headers)
        headers.pop("content-length", None)
        headers.pop("host", None)
        headers["X-OpenRouter-Title"] = "TypeSafe Mario"
        adapted = httpx2.Request(
            "POST",
            "https://openrouter.ai/api/alpha/decisions",
            headers=headers,
            json=body,
            extensions=request.extensions,
        )
        return self._transport.handle_request(adapted)

    def close(self) -> None:
        self._transport.close()
