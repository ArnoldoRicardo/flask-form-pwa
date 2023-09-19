from pydantic_settings import BaseSettings


class Config(BaseSettings):
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"


config = Config()
