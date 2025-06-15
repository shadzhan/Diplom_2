import pytest
import requests
import allure
from curl import Url

@allure.feature("Получение заказов пользователя")
class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, headers):
        response = requests.get(f"{Url.BASE_URL}{Url.ALL_ORDERS_URL}", headers=headers)
        assert response.status_code == 200
        assert response.json().get("success") is True
        assert isinstance(response.json().get("orders"), list)

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{Url.BASE_URL}{Url.ORDER_URL}")
        assert response.status_code == 401, f"Expected 401, but got {response.status_code}"
