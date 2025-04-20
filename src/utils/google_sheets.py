"""Google Sheets интеграция."""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from typing import List, Dict


class GoogleSheetsClient:
    """
    Класс для работы с Google Sheets.
    """

    def __init__(self, creds_path: str, sheet_name: str):
        """
        Инициализация клиента Google Sheets.
        :param creds_path: Путь к JSON-файлу с ключами сервис-аккаунта
        :param sheet_name: Название таблицы
        """
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]

        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        self.sheet = client.open(sheet_name).sheet1

    def append_users(self, users: List[Dict]) -> None:
        """
        Добавляет пользователей в таблицу.
        :param users: Список словарей пользователей
        """
        for user in users:
            self.sheet.append_row([
                user["id"],
                user["name"],
                user["username"],
                user["email"],
                user["phone"],
                user["website"],
            ])
