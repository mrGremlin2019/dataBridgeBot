from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator


class Settings(BaseSettings):

    """
    Настройки подключения к базе данных, загружаемые из файла .env.

    Атрибуты:
        MODE: режим работы приложения (test/prod)
        POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST,
        POSTGRES_PORT, POSTGRES_DB: параметры подключения
    """

    MODE: str

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    @property
    def DB_URL(self):
        return (f"postgresql+asyncpg://{self.POSTGRES_USER}:"
                f"{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_HOST}:"
                f"{self.POSTGRES_PORT}/"
                f"{self.POSTGRES_DB}")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Инициализация настроек и движка
settings = Settings()

engine = create_async_engine(settings.DB_URL, echo=True)
async_session = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Асинхронный генератор сессий для работы с БД"""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
