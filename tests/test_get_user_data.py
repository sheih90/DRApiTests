from http.client import responses

import httpx
from jsonschema import validate
from core.contracts import USER_DATA_SCHEMA, LIST_RESOURCE_SCHEMA

BASE_URL = "https://reqres.in/"
LIST_USERS = "api/users?page=2"
SINGLE_USER = "api/users/2"
SINGLE_USER_NOT_FOUND = "api/users/23"
LIST_RESOURCE = "api/unknown"
SINGLE_RESOURCE = "api/unknown/2"
SINGLE_RESOURCE_NOT_FOUND = "api/unknown/23"
EMAIL_ENDS = "reqres.in"
AVATAR_ENDS = "-image.jpg"
COLOR_STARTS = "#"

def test_list_users():
    response = httpx.get(BASE_URL + LIST_USERS)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, USER_DATA_SCHEMA)
        assert item["email"].endswith(EMAIL_ENDS)
        assert item["avatar"].endswith(str(item["id"]) + AVATAR_ENDS)


def test_single_user():
    response = httpx.get(BASE_URL + SINGLE_USER)
    assert response.status_code == 200
    data = response.json()['data']
    assert data["email"].endswith(EMAIL_ENDS)
    assert data["avatar"].endswith(str(data["id"]) + AVATAR_ENDS)


def test_single_user_not_found():
    response = httpx.get(BASE_URL + SINGLE_USER_NOT_FOUND)
    assert response.status_code == 404


def test_list_resource():
    response = httpx.get(BASE_URL + LIST_RESOURCE)
    assert response.status_code == 200
    data = response.json()['data']

    for item in data:
        validate(item, LIST_RESOURCE_SCHEMA)
        assert item["color"].startswith(COLOR_STARTS)
        assert len(item["pantone_value"]) == 7 == 7, "Длина pantone_value не соответствует формату"
        assert (item["pantone_value"][2]) == "-", "Отсутствует дефис в pantone_value"

def test_single_resource():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE)
    assert response.status_code == 200
    data = response.json()['data']
    assert data["color"].startswith(COLOR_STARTS)
    assert len( data["pantone_value"]) == 7 == 7, "Длина pantone_value не соответствует формату"
    assert (data["pantone_value"][2]) == "-", "Отсутствует дефис в pantone_value"

def test_single_resource_not_found():
    response = httpx.get(BASE_URL + SINGLE_RESOURCE_NOT_FOUND)
    assert response.status_code == 404