### Файл: src/bot/webhook.py
from aiogram import Bot
import logging
from src.bot.config_bot import settings

async def setup_webhook() -> None:
    """
    Настраивает вебхук для Telegram-бота.
    """
    try:
        container_bot: Bot = Bot(token=settings.TELEGRAM_TOKEN, parse_mode="HTML")
        webhook_url = settings.full_webhook_url

        await container_bot.delete_webhook(drop_pending_updates=True)
        await container_bot.set_webhook(
            url=webhook_url,
            drop_pending_updates=True
        )
        logging.info(f"Webhook установлен на {webhook_url}")
    except Exception as e:
        logging.critical(f"Ошибка настройки вебхука: {e}")
        raise


