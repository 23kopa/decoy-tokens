from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = Path(__file__).resolve().parents[3]

class Settings(BaseSettings):
    APP_ENV: str = "prod"  # dev | prod
    VITE_DEV_SERVER_URL: str = "http://localhost:5173"

    SESSION_SECRET_KEY: str
    DATABASE_URL: str
    PUBLIC_BASE_URL: str = "http://localhost:8000"

    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATES_DIR: Path = APP_DIR / "templates"

    @property
    def USE_VITE(self) -> bool:
        return self.APP_ENV == "dev"
    
    @property
    def GEOIP_CITY_PATH(self) -> Path:
        return self.STATIC_DIR / "geoip" / "GeoLite2-City.mmdb"
    
    @property
    def GEOIP_ASN_PATH(self) -> Path:
        return self.STATIC_DIR / "geoip" / "GeoLite2-ASN.mmdb"

    @property
    def TRACKING_GIF_URL(self) -> str:
        return f"{self.PUBLIC_BASE_URL}/static/images/gifs/spbgut.gif"    

    model_config = SettingsConfigDict(
        env_file=str(ROOT_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()  # type: ignore[call-arg]
