### Файл: src/schemas/user.py
from pydantic import BaseModel
from typing import List, Optional

class Address(BaseModel):
    """
    Схема адреса пользователя.
    """
    street: str
    suite: str
    city: str
    zipcode: str

class Company(BaseModel):
    """
    Схема компании пользователя.
    """
    name: str
    catch_phrase: str  # ранее catchPhrase, теперь ключи преобразованы в snake_case
    bs: str

class User(BaseModel):
    """
    Схема пользователя из внешнего API.
    """
    id: int
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: Company

    class Config:
        # Allow using snake_case fields after конвертации ключей
        allow_population_by_field_name = True
