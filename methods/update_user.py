import requests
from curl import Url


def update_user_name(headers, new_name):
    """Обновляет имя пользователя"""
    payload = {"name": new_name}
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers, timeout=10)

def update_user_email(headers, new_email, current_password, current_name):
    """Обновляет email пользователя"""
    payload = {
        "email": new_email,
        "name": current_name,
        "current_password": current_password
    }
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers, timeout=10)

def update_user_password(headers, new_password, current_password, current_email):
    """Обновляет пароль пользователя"""
    payload = {
        "password": new_password,
        "current_password": current_password,
        "email": current_email
    }
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers, timeout=10)

def update_user_full(headers, new_email, new_name, new_password, current_password):
    """Полностью обновляет данные пользователя"""
    payload = {
        "email": new_email,
        "name": new_name,
        "password": new_password,
        "current_password": current_password
    }
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers, timeout=10)

def update_user_unauthorized(update_data):
    """Пытается обновить данные без авторизации"""
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=update_data, timeout=10)

def update_user_email_with_wrong_password(headers, new_email, wrong_password, current_name):
    """Пытается обновить email с неверным паролем"""
    payload = {
        "email": new_email,
        "name": current_name,
        "current_password": wrong_password
    }
    return requests.patch(f"{Url.BASE_URL}{Url.UPDATE_USER_URL}", json=payload, headers=headers, timeout=10)