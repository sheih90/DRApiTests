import allure
import httpx
from jsonschema import validate
from core.contracts import CREATED_USER_SCHEMA, UPDATED_USER_SCHEMA
import datetime

BASE_URL = "https://reqres.in/"
CREATE_USER = "api/users"
UPDATE_USER = "api/users/2"
DELETE_USER = "api/users/2"
headers = {
    "x-api-key": "reqres-free-v1"  # API-ключ для авторизации
}


@allure.feature("UserJob")
class TestUserWork:
    @allure.title("Создание пользователя с именем и работой")
    def test_create_user_with_name_and_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "job": "leader",
                "name": "morpheus"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 201, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["createdAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Создание пользователя без имени")
    def test_create_user_withouth_name(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "job": "leader"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 201

        response_json = response.json()
        creation_date = response_json["createdAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATED_USER_SCHEMA)
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем 15 символов даты создания и текущей даты

    @allure.title("Создание пользователя без работы")
    def test_create_user_withouth_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "name": "morpheus"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + CREATE_USER}"):
            response = httpx.post(BASE_URL + CREATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 201

        response_json = response.json()
        creation_date = response_json["createdAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, CREATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PUT с именем и работой")
    def test_update_user_the_PUT_metod_with_name_and_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "name": "morpheus",
                "job": "zion resident"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.put(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PUT без имени")
    def test_update_user_the_PUT_metod_without_name(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "job": "zion resident"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.put(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PUT без работы")
    def test_update_user_the_PUT_metod_without_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "name": "morpheus"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.put(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PATCH с именем и работой")
    def test_update_user_the_PATCH_metod_with_name_and_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "name": "morpheus",
                "job": "zion resident"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.patch(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PATCH без имени")
    def test_update_user_the_PATCH_metod_without_name(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "job": "zion resident"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.patch(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что job запроса совпадает с job ответа"):
            assert response_json["job"] == body["job"], "job в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Обновление пользователя методом PATCH без работы")
    def test_update_user_the_PATCH_metod_without_job(self):
        with allure.step("Подготовка данных для создания пользователя"):
            body = {
                "name": "morpheus"
            }
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + UPDATE_USER}"):
            response = httpx.patch(BASE_URL + UPDATE_USER, headers=headers, json=body)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        response_json = response.json()
        creation_date = response_json["updatedAt"].replace("T"," ")  # находим в дате создания букву Т и заменяем ее на пробел
        current_date = str(datetime.datetime.utcnow())

        validate(response_json, UPDATED_USER_SCHEMA)
        with allure.step("Проверяем, что name запроса совпадает с name ответа"):
            assert response_json["name"] == body["name"], "name в ответе не совпадает с отправленным"
        with allure.step("Проверяем, что дата создания совпадает с текущей датой"):
            assert creation_date[0:15] == current_date[0:15]  # сравниваем  диапазон в 15 символов даты создания и текущей даты

    @allure.title("Удаление пользователя")
    def test_delete_user(self):
        with allure.step("Отправка запроса на удаление пользователя"):
            response = httpx.delete(BASE_URL + DELETE_USER, headers = headers)
        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 204, "Код ответа не совпал с ожидаемым"

