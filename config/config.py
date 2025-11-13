from pydantic_settings import BaseSettings
import os

from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    # google 
    GOOGLE_CLIENT_ID: str = os.environ.get("GOOGLE_CLIENT_ID", "")
    GOOGLE_CLIENT_SECRET: str = os.environ.get("GOOGLE_CLIENT_SECRET", "")
    GOOGLE_REDIRECT_URI: str = os.environ.get("GOOGLE_REDIRECT_URI", "")

    # JWT 
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 

    # database 
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"

settings = Settings()