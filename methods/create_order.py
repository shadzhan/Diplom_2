import requests
from curl import Url



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


class OrderCreation:
    @staticmethod
    def check_json(response):
        """Проверка, что ответ содержит JSON, и возвращение его."""
        content_type = response.headers.get('Content-Type', '')
        assert content_type.startswith('application/json'), \
        f"Ответ не в JSON формате: {response.text}"
        return response.json()


