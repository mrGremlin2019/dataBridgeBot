import logging
from aiogram import Router, types, F
from aiogram.filters import CommandStart
from dependency_injector.wiring import inject, Provide

from src.api.user_service import UserService
from src.bot.keyboards import get_main_keyboard
from src.db.config_db import get_db
from src.db.crud import UserRepository
from src.utils.google_sheets import GoogleSheetsClient
from src.DI.container import Container

router = Router()
"""
Роутер для хендлеров Telegram-бота.
"""

@router.message(CommandStart())
@inject
async def start_handler(
    message: types.Message
) -> None:
    """
    Обрабатывает команду /start и выводит главное меню с инлайн-кнопками.

    :param message: объект входящего сообщения
    """
    try:
        await message.answer(
            "Привет! Я Telegram-бот. Выберите действие:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logging.error(f"Start handler error: {e}")
        await message.answer("❌ Произошла ошибка")

@router.callback_query(F.data == "get_data")
@inject
async def get_data_handler(
    callback: types.CallbackQuery,
    user_service: UserService = Provide[Container.user_service]
) -> None:
    """
    Получает данные из внешнего API и отправляет их пользователю.

    :param callback: объект callback-запроса
    :param user_service: сервис для получения данных (DI)
    """
    await callback.answer()
    try:
        users = await user_service.fetch_users()
        text = "\n\n".join(
            f"<b>{u.name}</b>\n📧 {u.email}\n🌍 {u.website}"
            for u in users
        )
        await callback.message.answer(f"📄 Пользователи:\n\n{text}")
    except Exception as e:
        logging.error(f"Get data error: {e}")
        await callback.message.answer("❌ Ошибка при получении данных")

@router.callback_query(F.data == "save_data")
@inject
async def save_data_handler(
    callback: types.CallbackQuery,
    user_service: UserService = Provide[Container.user_service],
    user_repo: UserRepository = Provide[Container.user_repo],
    sheets_client: GoogleSheetsClient = Provide[Container.sheets_client]
) -> None:
    """
    Сохраняет данные в базе данных и Google Sheets.

    :param callback: объект callback-запроса
    :param user_service: сервис для получения данных (DI)
    :param user_repo: репозиторий для БД (DI)
    :param sheets_client: клиент Google Sheets (DI)
    """
    await callback.answer()
    try:
        users = await user_service.fetch_users()
        async with get_db() as db:
            await user_repo.save_users(db, users)
        sheets_client.append_users([user.dict() for user in users])
        await callback.message.answer("✅ Данные сохранены!")
    except Exception as e:
        logging.error(f"Save data error: {e}")
        await callback.message.answer("❌ Ошибка при сохранении данных")
