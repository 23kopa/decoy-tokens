from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import httpx

from backend.app.web.core.dependencies.use_cases import get_register_user, get_authenticate_user
from backend.app.application.use_cases.user.register import RegisterUser
from backend.app.application.use_cases.user.authenticate import AuthenticateUser
from backend.app.core.config import settings

router = APIRouter()
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))
templates.env.globals["recaptcha_site_key"] = settings.RECAPTCHA_SITE_KEY

print(f"IS_DEV: {settings.IS_DEV}")
print(f"RECAPTCHA_SITE_KEY loaded: {bool(settings.RECAPTCHA_SITE_KEY)}")
print(f"RECAPTCHA_SITE_KEY value: {settings.RECAPTCHA_SITE_KEY[:20] if settings.RECAPTCHA_SITE_KEY else 'EMPTY'}...")
print(f"RECAPTCHA_SECRET_KEY loaded: {bool(settings.RECAPTCHA_SECRET_KEY)}")

async def verify_recaptcha(token: str) -> tuple[bool, str]:
    
    if settings.IS_DEV and not settings.RECAPTCHA_SECRET_KEY:
        return True, ""
    
    if not token:
        return False, "CAPTCHA verification required"
    
    url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        "secret": settings.RECAPTCHA_SECRET_KEY,
        "response": token
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, data=data)
            result = response.json()
        
        if result.get("success"):
            # Для reCAPTCHA v3 можно проверить score
            score = result.get("score", 1.0)
            if score < 0.5:
                return False, "CAPTCHA verification failed (low score)"
            return True, ""
        else:
            error_codes = result.get("error-codes", [])
            return False, f"CAPTCHA verification failed: {', '.join(error_codes)}"
    
    except httpx.TimeoutException:
        return False, "CAPTCHA verification timeout"
    except Exception as e:
        return False, f"CAPTCHA verification error: {str(e)}"


@router.post("/auth/login")
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    remember: bool = Form(False),
    g_recaptcha_response: str = Form(None),
    uc: AuthenticateUser = Depends(get_authenticate_user),
):

    is_valid_captcha, captcha_error = await verify_recaptcha(g_recaptcha_response)

    if not is_valid_captcha:
        return RedirectResponse(f"/?error={captcha_error}", status_code=303)

    user = uc.execute(email=email, password=password)

    if not user:
        return RedirectResponse("/?error=invalid_credentials", status_code=303)
    
    request.session["user_id"] = user.id

    #if remember:
        # Сессия на 30 дней
    #    request.session.set_expiry(60 * 60 * 24 * 30)
    #else:
        # Сессия на 1 час
    #    request.session.set_expiry(60 * 60)

    return RedirectResponse("/home", status_code=303)


@router.post("/auth/register")
async def register_form(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    password2: str = Form(...),
    terms: bool = Form(...),
    g_recaptcha_response: str = Form(None),
    uc: RegisterUser = Depends(get_register_user),
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
    
    request.session["user_id"] = user.id
    return RedirectResponse("/home", status_code=303)


@router.post("/auth/logout")
async def logout_form(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)