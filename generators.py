from faker import Faker
import random

faker = Faker()


def generate_user_data():
    """Генерирует уникальные данные пользователя."""
    return {
        "name": faker.name(),
        "email": faker.email(domain="example.com"),
        "password": faker.password(length=12)
    }


def generate_order_body(available_ingredients=None, count=2):
    """Генерирует тело заказа со случайными ингредиентами."""
    if available_ingredients is None:
        return {"ingredients": []}

    ingredient_ids = [ingredient["_id"] for ingredient in available_ingredients]
    return {
        "ingredients": random.sample(ingredient_ids, min(count, len(ingredient_ids)))
    }


def generate_missing_fields_user(missing_field):
    """Генерирует пользователя без одного обязательного поля."""
    user = generate_user_data()
    user.pop(missing_field)
    return user