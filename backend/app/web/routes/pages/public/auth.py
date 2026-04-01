from fastapi import APIRouter, Request, Depends, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from backend.app.web.dependencies.use_cases import get_register_user, get_authenticate_user

from backend.app.application.use_cases.user.register import RegisterUserUseCase
from backend.app.application.use_cases.user.authenticate import AuthenticateUserUseCase

from backend.app.core.config import settings

from backend.app.infrastructure.security.recaptcha import verify_recaptcha

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
templates.env.globals["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

@router.post("/auth/login")
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    g_recaptcha_response: str = Form(None),
    uc: AuthenticateUserUseCase = Depends(get_authenticate_user),
):

    is_valid_captcha, captcha_error = await verify_recaptcha(g_recaptcha_response)
    user = uc.execute(email=email, password=password)

    if not is_valid_captcha:
        return RedirectResponse(f"/?error={captcha_error}", status_code=303)

    if not user:
        return RedirectResponse("/?error=invalid_credentials", status_code=303)

    response = RedirectResponse("/home", status_code=303)

    request.session.clear()
    request.session["user_id"] = user.id

    return response


@router.post("/auth/register")
async def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    terms: bool = Form(...),
    g_recaptcha_response: str = Form(None),
    uc: RegisterUserUseCase = Depends(get_register_user),
):

    is_valid_captcha, captcha_error = await verify_recaptcha(g_recaptcha_response)

    if not is_valid_captcha:
        return RedirectResponse(f"/?error={captcha_error}", status_code=303)

    if password != password2:
        return RedirectResponse("/?error=password_mismatch", status_code=303)
    
    if not terms:
        return RedirectResponse("/?error=terms_required", status_code=303)

    try:
        user = uc.execute(email=email, username=username, password=password)
    except ValueError as e:
        return RedirectResponse(f"/?error={str(e)}", status_code=303)

    response = RedirectResponse("/home", status_code=303)

    request.session["user_id"] = user.id

    return response


@router.post("/auth/logout")
async def logout_form(request: Request):
    
    request.session.clear()
    response = RedirectResponse("/", status_code=303)
    response.delete_cookie("csrf_token", path="/")
    
    return response