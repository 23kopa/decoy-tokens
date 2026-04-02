from starlette.responses import RedirectResponse
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from backend.app.core.config import settings

from backend.app.domain.entities.token import Token

templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

class LinkEngine:
    def __init__(self):
        self.gif_url = settings.TRACKING_GIF_URL

    def render(self, token: Token, request: Request):
        if token.payload and token.payload.get("show_gif"):
          return templates.TemplateResponse(
              request=request,
              name="components/shared/gif_viewer.html",
              context={
                  "request": request,
                  "gif_url": self.gif_url,
                  "show_loading_text": token.payload.get("show_loading", False),
                  "redirect_url": token.payload.get("redirect_url"),
                  "delay_ms": token.payload.get("delay_ms", 3000),
              },
          )
        else:
            url = token.payload.get("redirect_url") or "/"
            return RedirectResponse(url=url, status_code=302)
