import secrets
import string

ALPHABET = string.ascii_letters + string.digits

def generate_slug(leight: int = 10) -> str:
  return "".join(secrets.choice(ALPHABET) for _ in range(leight))