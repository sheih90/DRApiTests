import json

import allure
import httpx
import pytest
from jsonschema import validate
from core.contracts import REGISTERED_USER_SCHEMA, LOGIN_USER_SCHEMA

BASE_URL = "https://reqres.in/"
REGISTER_USER = "api/register"
LOGIN_USER = "api/login"
headers = {
    "x-api-key": "reqres-free-v1"  # API-ключ для авторизации
}


json_file = open('core/new_users_data.json') #прописываем путь до нашего файла
users_data = json.load(json_file) #загружаем наш json файл

json_file_missingpassword_user = open('core/missingpassword_users_data.json')
missingpassword_users_data = json.load(json_file_missingpassword_user)


@allure.feature("Register and login")
class TestRegisterAndLogin:
    @allure.title("Успешная регистрация пользователя")
    @pytest.mark.parametrize('users_data', users_data) #делаем тест параметризованным
    def test_register_successful(self, users_data):
        with allure.step(f"Отправка запроса на регистрацию пользователя"):
            response = httpx.post(BASE_URL + REGISTER_USER, json=users_data, headers=headers)
        print(users_data)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Статус отличается от ожидаемого"

        validate(response.json(), REGISTERED_USER_SCHEMA)

    @allure.title("Успешный вход пользователя в свой аккаунт")
    @pytest.mark.parametrize('users_data', users_data)
    def test_login_successful(self, users_data):
        with allure.step(f"Отправка запроса на вход пользователя в свой аккаунт"):
            response = httpx.post(BASE_URL + LOGIN_USER, json=users_data, headers=headers)
        print(users_data)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        validate(response.json(), LOGIN_USER_SCHEMA)

    @allure.title("Неуспешная регистрация пользователя с пропущенным паролем")
    @pytest.mark.parametrize('missingpassword_users_data', missingpassword_users_data)
    def test_register_unsuccessful(self, missingpassword_users_data):
        with allure.step(f"Отправка запроса на регистрацию пользователя"):
            response = httpx.post(BASE_URL + REGISTER_USER, json=users_data, headers=headers)
        print(missingpassword_users_data)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, "Статус отличается от ожидаемого"
        with allure.step("Проверка текста ошибки"):
            assert response.text == '{"error":"Missing email or username"}'

    @allure.title("Неуспешный вход пользователя с пропущенным паролем")
    @pytest.mark.parametrize('missingpassword_users_data', missingpassword_users_data)
    def test_login_unsuccessful(self, missingpassword_users_data):
        with allure.step(f"Отправка запроса на вход пользователя в свой аккаунт"):
            response = httpx.post(BASE_URL + LOGIN_USER, json=users_data, headers=headers)
        print(missingpassword_users_data)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 400, "Статус отличается от ожидаемого"
        with allure.step("Проверка текста ошибки"):
            assert response.text == '{"error":"Missing email or username"}'

