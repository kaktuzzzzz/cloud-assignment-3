from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    PROJECT_NAME: str = "cloud-assignment.nguyenpanda.com"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    PUBLIC_DIR: Path = BASE_DIR / "public"
    
    PAGES_DIR: Path = PUBLIC_DIR / "pages"
    ERRORS_DIR: Path = PUBLIC_DIR / "errors"
    IMAGES_DIR: Path = PUBLIC_DIR / "images"
    
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    RELOAD: bool = True
    
    GDRIVE_ID: str | None = None
    
    model_config = SettingsConfigDict(env_file=".env", extra='ignore')

settings = Settings()
