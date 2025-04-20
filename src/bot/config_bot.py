from pydantic_settings import BaseSettings, SettingsConfigDict


class BotSettings(BaseSettings):
    """
    Настройки Telegram-бота, загружаемые из файла .env.

    Атрибуты:
        TELEGRAM_TOKEN: токен для доступа к Bot API
        WEBHOOK_HOST: хост для вебхука (с протоколом и доменом)
        WEBHOOK_PATH: путь для вебхука
    """
    TELEGRAM_TOKEN: str
    WEBHOOK_HOST: str = "https://your-domain.com"
    WEBHOOK_PATH: str = "/webhook"

    @property
    def full_webhook_url(self) -> str:
        """
        Полный URL для установки вебхука в формате: <WEBHOOK_HOST><WEBHOOK_PATH>
        """
        return f"{self.WEBHOOK_HOST.rstrip('/')}" \
               f"{self.WEBHOOK_PATH}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = BotSettings()