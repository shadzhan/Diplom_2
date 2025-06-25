import pytest
import requests
import allure
from curl import Url
from messages import AuthMessages, GeneralMessages


@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешный логин под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        login_data = {
            "email": registered_user["data"]["email"],
            "password": registered_user["data"]["password"]
        }
        response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)

        assert response.status_code == 200 , (
            f"Ожидался статус 200, получен {response.status_code}")

        assert response.json().get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert "accessToken" in response.json()

    @allure.title("Логин с неверными учетными данными")
    def test_login_invalid_credentials(self, registered_user):
        login_data = {
            "email": registered_user["data"]["email"],
            "password": "wrong_password"
        }
        response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)

        assert response.status_code == 401 , (
            f"Ожидался статус 401, получен {response.status_code}")
        response_json = response.json()
        assert response_json.get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert AuthMessages.INVALID_CREDENTIALS in response_json.get("message", ""), (
            f"Ожидалось сообщение содержащее '{AuthMessages.INVALID_CREDENTIALS}', "
            f"получено '{response_json.get('message')}'")
