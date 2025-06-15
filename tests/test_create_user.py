import pytest
import requests
import allure
from curl import Url
from generators import generate_user_data, generate_missing_fields_user


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        user_data = generate_user_data()
        response = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert "accessToken" in response.json()

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, user_data):

        response1 = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)
        assert response1.status_code == 200

        response2 = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response2.status_code == 403
        assert response2.json().get("success") is False
        assert response2.json().get("message") == "User already exists"

    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_fields(self, missing_field, user_data):
        user_data = generate_missing_fields_user(missing_field)
        response = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response.status_code == 403
        assert response.json().get("success") is False
        assert "required fields" in response.json().get("message")