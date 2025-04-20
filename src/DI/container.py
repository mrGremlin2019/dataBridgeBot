import os
from dependency_injector import containers, providers
from src.api.user_service import UserService
from src.db.crud import UserRepository
from src.utils.google_sheets import GoogleSheetsClient
from aiogram import Bot
from src.bot.config_bot import settings


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.bot.handlers",
            "src.bot.webhook"
        ]
    )

    # Конфигурация бота
    bot = providers.Singleton(
        Bot,
        token=settings.TELEGRAM_TOKEN,
        parse_mode="HTML"
    )

    # Сервисы данных
    user_service = providers.Factory(
        UserService
    )

    # Репозиторий БД
    user_repo = providers.Factory(
        UserRepository
    )

    # Google Sheets клиент
    sheets_client = providers.Factory(
        GoogleSheetsClient,
        creds_path=os.getenv("GOOGLE_SHEETS_CREDENTIALS", "creds.json"),
        sheet_name=os.getenv("GOOGLE_SHEET_NAME", "UsersData")
    )