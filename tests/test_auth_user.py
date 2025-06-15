import pytest
import requests
import allure
from curl import Url



@allure.feature("Авторизация пользователя")
class TestUserLogin:

    @allure.title("Успешный логин под существующим пользователем")
    def test_login_existing_user_success(self, registered_user):
        login_data = {
            "email": registered_user["data"]["email"],
            "password": registered_user["data"]["password"]
        }
        response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()

    @allure.title("Логин с неверными учетными данными")
    def test_login_invalid_credentials(self, registered_user):
        login_data = {
            "email": registered_user["data"]["email"],
            "password": "wrong_password"
        }
        response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert "email or password are incorrect" in response.json().get("message")