import pytest
import requests
import allure
from curl import Url
from messages import GeneralMessages



@allure.feature("Получение заказов пользователя")
class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_authorized(self, headers):
        response = requests.get(f"{Url.BASE_URL}{Url.ALL_ORDERS_URL}", headers=headers)
        assert response.status_code == 200, (
            f"Ожидался 200 OK, получен {response.status_code}")
        assert response.json().get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert isinstance(response.json().get("orders"), list), (
            "Поле 'orders' должно быть списком")

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_unauthorized(self):
        response = requests.get(f"{Url.BASE_URL}{Url.ORDER_URL}")
        assert response.status_code == 401, f"Expected 401, but got {response.status_code}"

        response_json = response.json()
        assert "message" in response_json, "Ответ не содержит ключ 'message'"
        expected_message = "You should be authorised"
        assert response_json["message"] == expected_message, \
            f"Ожидалось сообщение '{expected_message}', получено '{response_json['message']}'"
