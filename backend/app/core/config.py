from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    APP_ENV: str = "dev"
    VITE_DEV_SERVER_URL: str = "http://localhost:5173"
    PUBLIC_BASE_URL: str = "http://localhost:8000"
    SESSION_SECRET_KEY: str

    DATABASE_URL: str
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""

    REDIS_URL: str = "redis://redis:6379/0"

    RECAPTCHA_SITE_KEY: str = ""
    RECAPTCHA_SECRET_KEY: str = ""

    TRUSTED_PROXIES: str = "127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16"

    STATIC_DIR: Path = APP_DIR / "static"
    DATA_DIR: Path = APP_DIR / "data"
    MEDIA_DIR: Path = DATA_DIR / "media"
    TEMPLATES_DIR: Path = APP_DIR / "templates"

    @property
    def IS_DEV(self) -> bool:
        return self.APP_ENV == "dev"
    
    @property
    def IS_PROD(self) -> bool:
        return self.APP_ENV == "prod"

    @property
    def USE_VITE(self) -> bool:
        return self.APP_ENV == "dev"

    @property
    def TRUSTED_PROXIES_SET(self) -> set[str]:
        return {
            item.strip()
            for item in self.TRUSTED_PROXIES.split(",")
            if item.strip()
        }

    @property
    def GEOIP_CITY_PATH(self) -> Path:
        return self.DATA_DIR / "geoip" / "GeoLite2-City.mmdb"
    
    @property
    def GEOIP_ASN_PATH(self) -> Path:
        return self.DATA_DIR / "geoip" / "GeoLite2-ASN.mmdb"

    @property
    def TRACKING_GIF_URL(self) -> str:
        return f"{self.PUBLIC_BASE_URL}/media/gifs/spbgut.gif"    

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()  # type: ignore[call-arg]
