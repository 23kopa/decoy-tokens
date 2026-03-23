import hashlib
import hmac
import secrets

def generate_secret() -> str:
    return secrets.token_urlsafe(24)

def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()

def verify_secret(secret: str, secret_hash: str) -> bool:
    return hmac.compare_digest(hash_secret(secret), secret_hash)
