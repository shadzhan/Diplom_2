import pytest
import requests
import allure
from curl import Url
from data import (
    NAME_UPDATE_CASES,
    EMAIL_UPDATE_CASES,
    PASSWORD_UPDATE_CASES,
    UNAUTHORIZED_UPDATE_CASES,
)
from methods.update_user import (
    update_user_name,
    update_user_password,
)
from messages import GeneralMessages, UserUpdateMessages


@allure.feature("Обновление данных пользователя")
class TestUserUpdate:

    @allure.title("Изменение имени с авторизацией")
    @pytest.mark.parametrize("update_data", NAME_UPDATE_CASES)
    def test_update_name_authorized(self, headers, registered_user, update_data):
        response = update_user_name(headers, update_data["name"])
        assert response.status_code == 200, (
            f"Ожидался 200 OK, получен {response.status_code}")
        json_response = response.json()
        assert json_response.get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert json_response["user"]["name"] == update_data["name"]


    @allure.title("Изменение email с авторизацией")
    @pytest.mark.parametrize("update_data", EMAIL_UPDATE_CASES)
    def test_update_email_authorized(self, headers, registered_user, update_data):

        payload = {
            "email": update_data["email"],
            "name": registered_user["data"]["name"],  # Текущее имя
            "current_password": registered_user["data"]["password"]
        }
        response = requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers)

        assert response.status_code == 200, (
            f"Ожидался 200 OK, получен {response.status_code}")
        assert response.json().get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert response.json()["user"]["email"] == update_data["email"]


    @allure.title("Изменение пароля с авторизацией")
    @pytest.mark.parametrize("update_data", PASSWORD_UPDATE_CASES)
    def test_update_password_authorized(self, headers, registered_user, update_data):

        response = update_user_password(headers, update_data["password"], registered_user["data"]["password"], registered_user["data"]["email"])
        assert response.status_code == 200, (
            f"Ожидался 200 OK, получен {response.status_code}")
        json_response = response.json()
        assert json_response.get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")

        login_data = {
            "email": registered_user["data"]["email"],
            "password": update_data["password"]
        }
        login_response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)
        assert login_response.status_code == 200, (
            f"Ожидался 200 OK при входе, получен {login_response.status_code}")
        assert login_response.json().get("success") == GeneralMessages.SUCCESS_TRUE, (
            "Ожидался успешный вход после смены пароля")


    @allure.title("Изменение данных без авторизации")
    @pytest.mark.parametrize("update_data", UNAUTHORIZED_UPDATE_CASES)
    def test_update_user_unauthorized(self, update_data):
        response = requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data)
        assert response.status_code == 401, (
            f"Ожидался 401 Unauthorized, получен {response.status_code}")
        json_response = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserUpdateMessages.UNAUTHORIZED in json_response.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserUpdateMessages.UNAUTHORIZED}', "
            f"получено '{json_response.get('message')}'") in response.json().get("message")

    @allure.title("Изменение имени без авторизации")
    def test_update_name_unauthorized(self, client):
        update_data = {"name": "New Name"}
        response = client.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        json_response = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserUpdateMessages.UNAUTHORIZED in json_response.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserUpdateMessages.UNAUTHORIZED}', "
            f"получено '{json_response.get('message')}'") in response.json().get("message")

    @allure.title("Изменение email без авторизации")
    def test_update_email_unauthorized(self, client):
        update_data = {"email": "newemail@example.com"}
        response = client.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        json_response = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserUpdateMessages.UNAUTHORIZED in json_response.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserUpdateMessages.UNAUTHORIZED}', "
            f"получено '{json_response.get('message')}'") in response.json().get("message")

    @allure.title("Изменение пароля без авторизации")
    def test_update_password_unauthorized(self, client):
        update_data = {"password": "new_password"}
        response = client.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        json_response = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserUpdateMessages.UNAUTHORIZED in json_response.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserUpdateMessages.UNAUTHORIZED}', "
            f"получено '{json_response.get('message')}'") in response.json().get("message")

    @allure.title("Полное изменение данных без авторизации")
    def test_full_update_unauthorized(self, client):
        update_data = {"name": "Updated Name", "email": "updated@example.com", "password": "new_password"}
        response = client.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data)
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        json_response = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserUpdateMessages.UNAUTHORIZED in json_response.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserUpdateMessages.UNAUTHORIZED}', "
            f"получено '{json_response.get('message')}'") in response.json().get("message")
