import pytest
import requests
import time
from curl import Url


@pytest.fixture(scope='function')
def user_data():
    """Генерирует уникальные данные пользователя с временной меткой"""
    timestamp = int(time.time() * 1000)  # Текущее время в миллисекундах
    return {
        "name": f"User_{timestamp}",
        "email": f"user_{timestamp}@example.com",
        "password": f"Password_{timestamp}"
    }


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