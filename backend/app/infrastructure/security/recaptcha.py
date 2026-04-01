import httpx
from backend.app.core.config import settings

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