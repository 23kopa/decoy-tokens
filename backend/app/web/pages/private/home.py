from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse

from backend.app.web.core.dependencies.current_user import get_current_user

router = APIRouter()


@router.get("/home", response_class=HTMLResponse)

async def home_page(
    request: Request,
    user = Depends(get_current_user)
):
    if not user:
        return RedirectResponse("/", status_code=303)

    templates = request.app.state.templates

    context = {
        "request": request,
        "user": user,
        "token_types": ["link", "email", "file", "dns", "image", "word"]
    }

    return templates.TemplateResponse(
        request=request,
        name="pages/home.html",
        context=context,
    )