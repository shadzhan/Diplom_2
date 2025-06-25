import pytest
import allure
from methods.create_order import create_order
from messages import GeneralMessages
from messages import OrderMessages

@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_authorized(self, get_ingredients, auth_user):
        create_order_fn = create_order(get_ingredients, auth_user)
        response = create_order_fn(auth=True)
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert json_data.get("name") != "", "Имя заказа не должно быть пустым"
        assert isinstance(json_data["order"]["number"], int), (
            "Номер заказа должен быть целым числом")

    @allure.title("Создание заказа без авторизации")
    def test_create_order_unauthorized(self, get_ingredients, auth_user):
        create_order_fn = create_order(get_ingredients, auth_user)
        response = create_order_fn(auth=False)
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
        assert json_data.get("name") != "", "Имя заказа не должно быть пустым"

        assert "owner" not in json_data["order"], (
            "Заказ не должен быть привязан к пользователю при создании без авторизации")

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, get_ingredients, auth_user):
        create_order_fn = create_order(get_ingredients, auth_user)
        response = create_order_fn(auth=True, ingredients=[])
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"

        json_data = response.json()
        assert json_data.get("success") == GeneralMessages.SUCCESS_FALSE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_FALSE}")
        assert OrderMessages.INGREDIENTS_REQUIRED in json_data.get("message", ""), (
            f"Ожидалось сообщение содержащее '{OrderMessages.INGREDIENTS_REQUIRED}', "
            f"получено '{json_data.get('message')}'")

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, get_ingredients, auth_user):
        create_order_fn = create_order(get_ingredients, auth_user)
        response = create_order_fn(valid=False, auth=True)
        assert response.status_code == 500, f"Ожидался 500, получен {response.status_code}"

        assert OrderMessages.INTERNAL_ERROR in response.text, (
            f"Ожидалось сообщение содержащее '{OrderMessages.INTERNAL_ERROR}', "
            f"получено '{response.text}'")

    @allure.title("Создание заказа с повторяющимися ингредиентами")
    def test_create_order_duplicate_ingredients(self, get_ingredients, auth_user):
        create_order_fn = create_order(get_ingredients, auth_user)
        ingredient_id = get_ingredients[0]["_id"]
        response = create_order_fn(auth=True, ingredients=[ingredient_id, ingredient_id])
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        json_data = response.json()
        assert json_data.get("success") == GeneralMessages.SUCCESS_TRUE, (
            f"Ожидалось success={GeneralMessages.SUCCESS_TRUE}")
