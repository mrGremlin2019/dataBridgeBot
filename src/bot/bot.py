from aiogram import Dispatcher, Bot
from dependency_injector.wiring import Provide, inject
from src.DI.container import Container

@inject
def create_dispatcher(
    bot: Bot = Provide[Container.bot]
) -> Dispatcher:
    """
    Создаёт и настраивает Dispatcher для Telegram-бота.

    :param bot: экземпляр aiogram.Bot, внедряется через DI
    :return: настроенный Dispatcher
    """
    dp = Dispatcher(bot=bot)
    return dp

# Инициализация Dispatcher
dp: Dispatcher = create_dispatcher()