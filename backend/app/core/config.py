from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mining Calculations"

    class Config:
        case_sensitive = True

settings = Settings()
