import re
from typing import Any, Dict, List, Union


def camel_to_snake(name: str) -> str:
    """
    Преобразует строку из camelCase или PascalCase в snake_case.

    :param name: исходное имя в camelCase или PascalCase
    :return: строка в формате snake_case

    Пример:
        >>> camel_to_snake('camelCaseName')
        'camel_case_name'
    """
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    snake = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()
    return snake


def convert_dict_keys(
    data: Union[Dict[str, Any], List[Any]]
) -> Union[Dict[str, Any], List[Any]]:
    """
    Рекурсивно преобразует все ключи словаря из camelCase в snake_case.

    :param data: словарь или список для конвертации
    :return: структура с ключами в snake_case

    Пример:
        >>> convert_dict_keys({'userName': 'Alice', 'address': {'postalCode': 12345}})
        {'user_name': 'Alice', 'address': {'postal_code': 12345}}
    """
    if isinstance(data, list):
        return [convert_dict_keys(item) for item in data]
    if isinstance(data, dict):
        new_dict: Dict[str, Any] = {}
        for k, v in data.items():
            new_key = camel_to_snake(k)
            new_value = convert_dict_keys(v)
            new_dict[new_key] = new_value
        return new_dict
    return data