import allure
import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEMA

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USER = "api/users/2"
SINGLE_USER_NOT_FOUND = "api/users/23"
DELAYED_REQUEST = "api/users?delay=3"
EMAIL_ENDS = "reqres.in"
AVATAR_ENDS = "-image.jpg"
headers = {
    "x-api-key": "reqres-free-v1"  # API-ключ для авторизации
}


@allure.feature("Users")
class TestUsers:
    @allure.title("Получение списка пользователей")
    def test_list_users(self):

        with allure.step("Отправка запроса на получение списка пользователей"):
            response = httpx.get(BASE_URL + LIST_USERS, headers = headers)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        data = response.json()['data']
        for item in data:
            with allure.step("Проверка элемента из списка"):
                validate(item, USER_DATA_SCHEMA)
                with allure.step("Проверка окончания email адреса"):
                    assert item["email"].endswith(EMAIL_ENDS), "Окончание email не совпало с ожидаемым"
                with allure.step("Проверка наличия id в ссылке аватара"):
                    assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS), "id отсутствует в ссылке аватарки"

    @allure.title("Получение данных одного пользователя")
    def test_single_user(self):
        with allure.step("Отправка запроса на получение данных одого пользователя"):
            response = httpx.get(BASE_URL + SINGLE_USER, headers = headers)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

            data = response.json()['data']
        with allure.step("Проверка окончания email адреса"):
            assert data["email"].endswith(EMAIL_ENDS), "окончаниe email адреса не совпало с ожидаемым"
        with allure.step("Проверка наличия id в ссылке на аватарку"):
            assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS), "id отстутствует в ссылке на аватарку"

    @allure.title("Проверка, что пользователь не найден")
    def test_single_user_not_found(self):
        with allure.step("Отправка запроса на получение данных одого пользователя"):
            response = httpx.get(BASE_URL + SINGLE_USER_NOT_FOUND, headers = headers)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Проверка таймаута отложенного запроса получения списка пользователей")
    def test_delayed_user_list(self):
        with allure.step("Отправка запроса на получение списка пользователей с таймаутом"):
            response = httpx.get(BASE_URL + DELAYED_REQUEST, headers = headers, timeout=5)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

