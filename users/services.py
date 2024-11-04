import string
import random


def generate_random_password(length=8):
    """Генерация случайного пароля."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
