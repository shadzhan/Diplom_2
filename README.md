# Diplom_2
Дипломная работа задание 2

Студент Альберт Шаджанов
Когорта #20
Проект тестирования API Stellar Burgers
Этот проект предназначен для автоматизированного тестирования API сервиса Stellar Burgers с использованием pytest, requests и allure-pytest. В рамках проекта реализованы тесты для проверки основных эндпоинтов, таких как получение ингредиентов, создание заказов, регистрация и авторизация пользователей, сброс пароля и получение данных о заказах.

Структура проекта
your_project/
│
├── requirements.txt          # Зависимости проекта
├── conftest.py               # Фикстуры pytest (в корне)
├── data.py                   # Тестовые данные
├── generators.py             # Генератор данных
├── messages.py               # Модуль сообщений от сервера
├── curl.py                   # Файл с URL
├── methods/                  # Методы
├── create_order.py           # Методы для создания заказа
├── update_user.py            # Методы для изменения данных пользователя
└── tests/                    # Тестовые сценарии

    ├── test_create_order.py  # Тесты для создания заказов
    ├── test_create_user.py   # Тесты для регистрации
    ├── test_auth_user.py     # Тесты для логина
    ├── test_update_user.py    # Тесты для обновления данных пользователя
    └── test_get_orders.py     # Тесты для получения заказов
Установка зависимостей
Для запуска тестов необходимо установить все зависимости:

bash
Copy code
pip install -r requirements.txt
Файл requirements.txt содержит:
pytest
requests
allure-pytest

Запуск тестов с помощью pytest и сохранение результатов отчёта:

pytest --alluredir=allure-results

Открыть отчёт в браузере:

allure serve allure-results
