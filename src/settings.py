from pydantic import Field
from pydantic_settings import SettingsConfigDict,BaseSettings
from enum import StrEnum
from shared.path import ENV_FILE_PATH,ENVIRONMENT
from shared.envs import Environment

class DatabaseType(StrEnum):
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE_PATH, extra="ignore", case_sensitive=True)
    ENVIRONMENT: Environment = ENVIRONMENT
    

    # Project 
    # ----------------------------------------------------------------
    
    PROJECT_NAME: str = "Basic API Users"
    VERSION: str = "1.0.0"
    AUTHOR: str = "Roni Hernandez"
    PROFILE_IMAGE_URL: str = "https://avatars.githubusercontent.com/u/40522363?s=400&u=6840da2e780e3ecdcca4c143e169da6950f2d9e3&v=4"
    
    # JWT
    # ----------------------------------------------------------------
    
    PRIVATE_KEY: str 
    PUBLIC_KEY: str
    JWT_ALGORITHM: str = "RS256"
    JWT_EXPIRATION_MINUTES: int = 10

    # Database
    # ----------------------------------------------------------------
    
    DATABASE_URL: str
    DATABASE_TYPE: DatabaseType

    # Swagger
    # ----------------------------------------------------------------
    
    LOGIN_SWAGGER_URL: str = "/v1/users/login-swagger"
    
    # URLs
    # ----------------------------------------------------------------
    
    PREFIX_API_USER : str = "/v1/users"

settings = Settings()
