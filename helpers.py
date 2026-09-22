import uuid
from faker import Faker

fake = Faker("ru_RU")


def generate_name() -> str:
    """
    Генерирует случайное имя пользователя на русском языке.
    
    Returns:
        str: Случайное имя.
    """
    return fake.first_name()


def generate_email() -> str:
    """
    Генерирует гарантированно уникальный email для тестовых пользователей.
    Формат: test_{8-символьный hex-идентификатор}@yandex.ru
    
    Returns:
        str: Уникальный email.
    """
    return f"test_{uuid.uuid4().hex[:8]}@yandex.ru"


def generate_password() -> str:
    """
    Возвращает фиксированный тестовый пароль.
    Используется только в автотестах на тестовом стенде.
    
    Returns:
        str: Пароль.
    """
    return "123456"


def get_user_data() -> dict[str, str]:
    """
    Формирует готовый словарь с тестовыми данными пользователя.
    
    Returns:
        dict[str, str]: Словарь с ключами: name, email, password.
    """
    return {
        "name": generate_name(),
        "email": generate_email(),
        "password": generate_password(),
    }
