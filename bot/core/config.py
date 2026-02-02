from pydantic_settings import BaseSettings


class BotSettings(BaseSettings):
    bot_token: str


bot_settings = BotSettings()
