# tests/test_app.py

import requests
import time
from random import randint

# URL, по которому будет доступно наше приложение в Docker-сети
BASE_URL = "http://localhost:8000"

def wait_for_health(timeout_seconds: int = 60):
    """Ждем готовности приложения по /health."""

    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=2)
            if response.status_code == 200:
                return
        except requests.RequestException:
            pass

        time.sleep(1)

    raise AssertionError("Приложение не стало доступно по /health за отведенное время.")

def test_read_root():
    """Тест доступности главной страницы."""
    wait_for_health()
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert "Менеджер Задач" in response.text

def test_create_and_check_task():
    """
    Функциональный тест:
    1. Создает новую задачу.
    2. Проверяет, что она появилась на главной странице.
    """
    wait_for_health()
    unique_task_title = f"Тестовая задача-{randint(1000, 9999)}"
    task_data = {
        "title": unique_task_title,
        "description": "Это описание тестовой задачи."
    }
    
    create_response = requests.post(f"{BASE_URL}/tasks", data=task_data, allow_redirects=True)
    
    assert create_response.status_code == 200
    assert "Менеджер Задач" in create_response.text
    get_response = requests.get(BASE_URL)
    
    assert get_response.status_code == 200

    assert unique_task_title in get_response.text