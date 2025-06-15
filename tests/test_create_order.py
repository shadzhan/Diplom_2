import pytest
import requests
import allure
from curl import Url
from methods.create_order import OrderCreation



@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized(self, create_order, get_ingredients):
        response = create_order(auth=True)
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") is True
        assert json_data.get("name") != ""
        assert isinstance(json_data["order"]["number"], int)

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, create_order, get_ingredients):
        response = create_order(auth=False)
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") is True
        assert json_data.get("name") != ""

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, create_order):
        response = create_order(ingredients=[], auth=True)
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") is False
        assert "ingredient" in json_data.get("message", "").lower()

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, create_order):
        response = create_order(valid=False, auth=True)
        assert response.status_code == 500, f"Ожидался 500, получен {response.status_code}"

        expected_error_message = "Internal Server Error"
        assert expected_error_message in response.text, f"Ожидалось сообщение 500, получен {expected_error_message}"


    @allure.title("Создание заказа с повторяющимися ингредиентами")
    def test_create_order_duplicate_ingredients(self, create_order, get_ingredients):
        ingredient_id = get_ingredients[0]["_id"]
        response = create_order(ingredients=[ingredient_id, ingredient_id], auth=True)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        json_data = response.json()
        assert json_data.get("success") is True