from http.client import responses

import allure
import httpx
from jsonschema import validate
from core.contracts import  LIST_RESOURCE_SCHEMA

BASE_URL = "https://reqres.in/"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"
EMAIL_ENDS = "reqres.in"
AVATAR_ENDS = "-image.jpg"
COLOR_STARTS = "#"


@allure.feature("Resources")
class TestResources:
    @allure.title("Проверка получения списка ресурсов")
    def test_list_resource(self):
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + LIST_RESOURCE}"):
            response = httpx.get(BASE_URL + LIST_RESOURCE)

        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401

        data = response.json()['data']
        for item in data:
            with allure.step(""):
                validate(item, LIST_RESOURCE_SCHEMA)
                with allure.step("Проверяем первый символ значения цвета"):
                    assert item["color"].startswith(COLOR_STARTS)
                with allure.step("Проверяем количество символов pantone_value"):
                    assert len(item["pantone_value"]) == 7 == 7, "Длина pantone_value отличается от ожидаемого"
                with allure.step("Проверяем наличие дефиса в pantone_value"):
                    assert (item["pantone_value"][2]) == "-", "Отсутствует дефис в pantone_value"


    @allure.title("Проверка получения одного ресурса")
    def test_single_resource(self):
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + SINGLE_RESOURCE}"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 200

        data = response.json()['data']

        with allure.step("Проверяем первый символ значения цвета"):
            assert data["color"].startswith(COLOR_STARTS)
        with allure.step("Проверяем количество символов pantone_value"):
            assert len(data["pantone_value"]) == 7 == 7, "Длина pantone_value не соответствует формату"
        with allure.step("Проверяем наличие дефиса в pantone_value"):
            assert (data["pantone_value"][2]) == "-", "Отсутствует дефис в pantone_value"


    @allure.title("Проверяем, что ресурс не найден")
    def test_single_resource_not_found(self):
        with allure.step(f"Отправляем запрос по адресу: {BASE_URL + SINGLE_RESOURCE_NOT_FOUND}"):
            response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
        with allure.step("Проверяем код ответа"):
            assert response.status_code == 401