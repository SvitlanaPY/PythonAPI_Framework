# Розглянемо метод створення користувача.
# Для створення користувача потрібно передати дані користувача, такі як: # username, password, firstName, lastName, email
# Спершу створимо негативний тест, який буде передавати вже існуючий email.
# В content-і приходить особлийвий вид строки, який почин-ся із символу b - це означає, що строка в форматі послідовності байтів
# і ще не приведена до якого-небудь кодування і перші, ніж порівнювати її зі звичайною строкою, її треба привести до одного із видів кодування,
# і у нашому випадку - це "utf-8"
# Створити користувача із існуючим email неможливо.
# То як же ж написати позитивний тест на створення новго користувача?
# Який би ми не вказали email для створення користувача, після запуску одного такого тесту потрібно створювати новий email.
# Давайте зробимо так, щоб email генерувався автоматично і для кожного запуску тестку відрізнявся від будь-якого іншого.
# І щоб це зробити, то можна до першої частини email-ла додавати наприклад дату.
# Оскільки генерувати email нам потрібно в кількох тестах, то винесимо це в setup нашого файлу test_4_1_create_user.py.
# згенерований email кладемо в змінну викликану через self, щоб вона була доступна в інших функціях тестів.
# При успішному створення користувача, в response-і повертається json із id створеного користувача. Це і перевіримо - що в json є поле id.
# .


import pytest
import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from datetime import datetime


class TestUserRegister(BaseCase):
    def setup_method(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"

    def test_create_user_successfully(self):
        credentials = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'password': '1234',
            'email': self.email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=credentials)
        # assert response.status_code == 200, f'Unexpected status code {response.status_code}'
        Assertions.assert_code_status(response, 200)

        # assert "id" in response.json(), f"Response json doesn't have key_name = 'id'"
        Assertions.assert_json_has_key(
            response,
            "id"
        )
        # print(response.content)

# >python -m pytest -s tests/test_user_register.py -k test_create_user_successfully

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        credentials = {
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'password': '1234',
            'email': email
        }

        response = requests.post("https://playground.learnqa.ru/api/user/", data=credentials)
        # assert response.status_code == 400, f"Unexpected status code {response.status_code}"
        Assertions.assert_code_status(response, 400)

        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"
        # print(response.status_code)
        # print(response.content)

# >python -m pytest -s tests/test_user_register.py
