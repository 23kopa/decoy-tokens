from typing import Optional
from starlette.responses import Response
from starlette.requests import Request

from backend.app.domain.entities.token import Token

GIF_1x1 = (
    b"GIF89a\x01\x00\x01\x00\x80\x00\x00"
    b"\x00\x00\x00\xff\xff\xff!\xf9\x04"
    b"\x01\x00\x00\x00\x00,\x00\x00\x00"
    b"\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
)

class EmailEngine:
    def render(self, token: Token, request: Optional[Request] = None):
        return Response(content=GIF_1x1, media_type="image/gif")
