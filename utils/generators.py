import uuid
from faker import Faker

fake = Faker("ru_RU")

def generate_name() -> str:
    return fake.first_name()

def generate_email() -> str:
    return f"test_{uuid.uuid4().hex[:8]}@yandex.ru"

def generate_password() -> str:
    return "123456"

def get_user_data() -> dict[str, str]:
    return {
        "name": generate_name(),
        "email": generate_email(),
        "password": generate_password(),
    }
