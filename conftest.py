import pytest
import requests
import time
from faker import Faker
from curl import Url
from generators import generate_user_data, generate_order_body



faker = Faker()


@pytest.fixture(scope='function')
def user_data():
    """Генерирует уникальные данные пользователя с временной меткой"""
    timestamp = int(time.time() * 1000)  # Текущее время в миллисекундах
    return {
        "name": f"User_{timestamp}",
        "email": f"user_{timestamp}@example.com",
        "password": f"Password_{timestamp}"
    }

@pytest.fixture(autouse=True)
def wait_between_tests():
    yield
    time.sleep(0.5)

@pytest.fixture(scope='function')
def registered_user(user_data):
    """Создает зарегистрированного пользователя."""
    response = requests.post(f"{Url.BASE_URL}{Url.CREATE_USER_URL}", json=user_data)
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    yield {
        "data": user_data,
        "response": response
    }

    delete_response = requests.delete(
        f"{Url.BASE_URL}{Url.DELETE_URL}",
        headers={"Authorization": response.json().get('accessToken')}
    )
    assert delete_response.status_code in [200, 202], f"Failed to delete user: {delete_response.text}"


@pytest.fixture(scope='function')
def auth_token(registered_user):
    """Получает токен авторизации для созданного пользователя."""
    login_data = {
        "email": registered_user["data"]["email"],
        "password": registered_user["data"]["password"]
    }
    response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get('accessToken')
    assert token is not None, "Token not received"
    return token


@pytest.fixture(scope='function')
def headers(auth_token):
    """Создает заголовки с авторизацией."""
    return {"Authorization": auth_token}


@pytest.fixture(scope='module')
def available_ingredients():
    """Получает доступные ингредиенты."""
    response = requests.get(f"{Url.BASE_URL}{Url.INGREDIENTS_URL}")
    assert response.status_code == 200
    return response.json()["data"]


@pytest.fixture
def create_order(get_ingredients, auth_user):
    def _create_order(auth=True, ingredients=None, valid=True, count=2):
        if ingredients is None:
            if valid:
                ingredients = [ingredient["_id"] for ingredient in get_ingredients[:count]]
            else:
                ingredients = [f"invalid_{i}" for i in range(count)]

        payload = {"ingredients": ingredients}

        headers = {}
        if auth:
            _, token = auth_user
            headers = {"Authorization": token}

        return requests.post(
            f"{Url.BASE_URL}{Url.ORDER_URL}",
            json=payload,
            headers=headers,
            timeout=10
        )

    return _create_order


@pytest.fixture
def auth_user(registered_user):
    login_data = {
        "email": registered_user["data"]["email"],
        "password": registered_user["data"]["password"]
    }
    response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)
    assert response.status_code == 200
    token = response.json()["accessToken"]
    return registered_user, token

@pytest.fixture(scope="module")
def get_ingredients():
    response = requests.get(f"{Url.BASE_URL}{Url.INGREDIENTS_URL}")
    assert response.status_code == 200
    return response.json()["data"]

@pytest.fixture
def client():
    """Клиент для отправки запросов без авторизации"""
    return requests.Session()