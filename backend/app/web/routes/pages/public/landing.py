from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from backend.app.web.dependencies.current_user import get_current_user
from backend.app.core.config import settings

router = APIRouter()

@router.get("/")
async def landing_page(request: Request, user=Depends(get_current_user)):

    if user:
        return RedirectResponse("/home", status_code=303)

    templates = request.app.state.templates

    context = {
        "request": request,
        "recaptcha_site_key": settings.RECAPTCHA_SITE_KEY,
    }
    
    return templates.TemplateResponse(
        request=request,
        name="pages/hello.html",
        context=context,
    )