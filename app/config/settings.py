import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    load_dotenv()

    ACCESS_TOKEN_LIFETIME:int = int(24 * 60 * 60)         #24hours

    EMAIL_USERNAME:str = str(os.getenv('EMAIL_USERNAME'))
    EMAIL_PASSWORD:str = str(os.getenv('EMAIL_PASSWORD'))
    
    DB_URL: str = os.getenv("DB_URL")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    HASHING_ALGORITHM: str = os.getenv("HASHING_ALGORITHM")

    AWS_BUCKET_NAME: str = str(os.getenv("AWS_BUCKET_NAME"))
    AWS_REGION: str = str(os.getenv("AWS_REGION"))
    AWS_ACCESS_KEY: str = str(os.getenv("AWS_ACCESS_KEY"))
    AWS_SECRET_KEY: str = str(os.getenv("AWS_SECRET_KEY"))

    BASE_URL:str = 'http://localhost:8000'

    class Config:
        env_file = ".env"
        extra = "allow"

    @property
    def POSTGRES_URL(self):
        return self.DB_URL


settings = Settings()
