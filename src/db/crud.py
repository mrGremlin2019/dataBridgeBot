from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.db.models import User
from src.schemas.user import User as UserSchema
from typing import List

class UserRepository:
    """
    Репозиторий для работы с пользователями в базе данных.
    """

    async def save_user(
        self,
        session: AsyncSession,
        user: UserSchema
    ) -> User:
        """
        Сохраняет одного пользователя в БД.

        :param session: асинхронная сессия SQLAlchemy
        :param user: Pydantic-схема пользователя
        :return: модель пользователя из БД
        """
        db_user = User(
            id=user.id,
            name=user.name,
            email=user.email,
            website=user.website
        )
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    async def save_users(
        self,
        session: AsyncSession,
        users: List[UserSchema]
    ) -> List[User]:
        """
        Сохраняет список пользователей в БД за одну сессию.

        :param session: асинхронная сессия SQLAlchemy
        :param users: список Pydantic-схем пользователей
        :return: список моделей пользователей из БД
        """
        saved: List[User] = []
        for user in users:
            saved_user = await self.save_user(session, user)
            saved.append(saved_user)
        return saved

    async def get_users(
        self,
        session: AsyncSession
    ) -> List[User]:
        """
        Возвращает всех пользователей из БД.

        :param session: асинхронная сессия SQLAlchemy
        :return: список моделей пользователей
        """
        result = await session.execute(select(User))
        return result.scalars().all()