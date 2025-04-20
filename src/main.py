"""
Точка входа в приложение: запускает aiohttp-сервер с Telegram-ботом.
"""

import os
import logging
from aiohttp import web

from src.server import create_app
from src.DI.container import Container


def main() -> None:
    """
    Настраивает окружение и запускает aiohttp-сервер с Telegram-ботом.

    - Инициализирует логирование
    - Создает и настраивает DI-контейнер
    - Запускает веб-сервер с маршрутом для webhook
    """
    # Конфигурация логирования
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    logger = logging.getLogger(__name__)

    # Параметры сервера (можно переопределить через переменные окружения)
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", 8080))

    logger.info(f"Starting server on {host}:{port}")

    # Инициализация DI-контейнера
    container = Container()
    container.init_resources()
    container.wire(modules=["src.bot.handlers", "src.bot.webhook"])

    # Создание и запуск приложения
    app = create_app()
    web.run_app(
        app,
        host=host,
        port=port,
        access_log=logging.getLogger("aiohttp.access")
    )


if __name__ == "__main__":
    main()
