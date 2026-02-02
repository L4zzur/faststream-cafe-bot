from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    rabbit_url: str = "amqp://guest:guest@localhost:5672/"
    cashier_api_url: str = "http://cashier:9010/"


settings = Settings()
