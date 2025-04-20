import aiohttp
from typing import List
from src.utils.converters import convert_dict_keys
from src.schemas.user import User

class UserService:
    """
    Сервис для получения и обработки данных пользователей из внешнего API.
    """

    API_URL = "https://jsonplaceholder.typicode.com/users"

    async def fetch_users(self) -> List[User]:
        """
        Получает список пользователей из API, валидирует и возвращает.
        :return: Список валидированных пользователей
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.API_URL) as response:
                data = await response.json()
                data_snake_case = convert_dict_keys(data)
                users = [User(**user) for user in data_snake_case]
                return users
