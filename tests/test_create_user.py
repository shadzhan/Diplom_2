import pytest
import requests
import allure
from curl import Url
from generators import generate_user_data, generate_missing_fields_user
from messages import GeneralMessages, UserCreationMessages


@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_data):
        user_data = generate_user_data()
        response = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response.status_code == 200 , (
            f"Ожидался 200 OK, получен {response.status_code}")
        assert response.json().get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert "accessToken" in response.json()

    @allure.title("Создание существующего пользователя")
    def test_create_existing_user(self, user_data):

        response1 = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)
        assert response1.status_code == 200, (
            "Пользователь не был создан перед проверкой дубликата")

        response2 = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response2.status_code == 403, (
            f"Ожидался 403 Forbidden, получен {response2.status_code}")

        assert response2.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")

        assert response2.json().get("message") == UserCreationMessages.USER_EXISTS, (
            f"Ожидалось сообщение '{UserCreationMessages.USER_EXISTS}', ")


    @allure.title("Создание пользователя без обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_fields(self, missing_field, user_data):
        user_data = generate_missing_fields_user(missing_field)
        response = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)

        assert response.status_code == 403, (
            f"Ожидался 403 Forbidden, получен {response.status_code}")
        json_data = response.json()
        assert response.json().get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert UserCreationMessages.MISSING_FIELDS in json_data.get("message", ""), (
            f"Ожидалось сообщение содержащее '{UserCreationMessages.MISSING_FIELDS}', "
            f"получено '{json_data.get('message')}'")