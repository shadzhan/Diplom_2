

class OrderCreation:
    @staticmethod
    def check_json(response):
        """Проверка, что ответ содержит JSON, и возвращение его."""
        content_type = response.headers.get('Content-Type', '')
        assert content_type.startswith('application/json'), \
        f"Ответ не в JSON формате: {response.text}"
        return response.json()


