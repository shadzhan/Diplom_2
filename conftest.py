import pytest
import random
import string
from generators import generate_user_data
import requests
from curl import Url

@pytest.fixture(scope='function')
def random_user_data():
    """Генерирует случайные данные пользователя для теста."""
    random_string = ''.join(random.choices(string.ascii_letters, k=8))
    return {
        "name": f"User_{random_string}",
        "email": f"user_{random_string}@gmail.com",
        "password": f"Password{random.randint(1000,9999)}"
    }

@pytest.fixture(scope='function')
def registered_user(random_user_data):
    """Создает зарегистрированного пользователя."""
    response = requests.post(
        f'{Url.BASE_URL}{Url.CREATE_USER_URL}',
        json=random_user_data
    )
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    yield random_user_data

@pytest.fixture(scope='function')
def create_user():
    """Создает уникального пользователя с помощью генератора."""
    user_data = generate_user_data()
    response = requests.post(
        f"{Url.BASE_URL}{Url.CREATE_USER_URL}",
        json=user_data
    )
    assert response.status_code == 200, f"Failed to create user: {response.text}"
    return {
        "response": response,
        "name": user_data["name"],
        "email": user_data["email"],
        "password": user_data["password"]
    }

@pytest.fixture(scope='function')
def auth_token(create_user):
    """Получает токен авторизации для созданного пользователя."""
    login_data = {
        "email": create_user["email"],
        "password": create_user["password"]
    }
    response = requests.post(f"{Url.BASE_URL}{Url.AUTH_URL}", json=login_data)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get('accessToken')
    assert token is not None, "Token not received"
    yield token

@pytest.fixture(scope='function')
def headers(auth_token):
    """Создает заголовки с авторизацией."""
    return {
        "Authorization": auth_token
    }

@pytest.fixture(scope='function')
def create_order(headers):
    def _create_order(ingredients=None, auth=True):
        payload = {"ingredients": ingredients or []}
        return requests.post(
            f"{Url.BASE_URL}{Url.ORDER_URL}",
            json=payload,
            headers=headers if auth else {}
        )
    return _create_order


@pytest.fixture(scope='session')
def available_ingredients():
    response = requests.get(f"{Url.BASE_URL}{Url.INGREDIENTS_URL}")
    assert response.status_code == 200
    return response.json()["data"]

