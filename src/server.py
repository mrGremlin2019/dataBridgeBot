### Файл: src/server.py
from aiohttp import web
from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from src.bot.bot import dp
from src.bot.config_bot import settings
from src.bot.handlers import router
from src.bot.webhook import setup_webhook
from src.DI.container import Container

async def on_startup(app: web.Application) -> None:
    """
    Выполняется при запуске aiohttp-сервера.
    Регистрирует маршруты и устанавливает вебхук.

    :param app: aiohttp Application
    """
    # Подключаем роутер хендлеров
    dp.include_router(router)

    # Устанавливаем webhook
    await setup_webhook()


def create_app() -> web.Application:
    """
    Создает и настраивает aiohttp-приложение для Telegram-бота.

    :return: aiohttp Application
    """
    container = Container()
    container.wire(modules=[__name__])

    app = web.Application()
    # Регистрируем обработчик webhook
    SimpleRequestHandler(dispatcher=dp, bot=container.bot()).register(app, path=settings.WEBHOOK_PATH)
    app.on_startup.append(on_startup)
    return app
