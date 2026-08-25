from typing import Callable
users = []
def password_checker(func: Callable) -> Callable:
    """Простой декоратор для базовой проверки пароля."""
    def wrapper(password: str) -> str:
        if len(password) < 8:
            return "Ошибка: пароль должен быть не менее 8 символов."
        has_digit = any(char.isdigit() for char in password)
        has_upper = any(char.isupper() for char in password)
        has_lower = any(char.islower() for char in password)
        if not has_digit:
            return "Ошибка: пароль должен содержать хотя бы одну цифру."
        if not has_upper:
            return "Ошибка: пароль должен содержать хотя бы одну заглавную букву."
        if not has_lower:
            return "Ошибка: пароль должен содержать хотя бы одну строчную букву."
        return func(password)
    return wrapper
@password_checker
def register_user(password: str) -> str:
    """Функция регистрации пользователя."""
    return f"Пользователь успешно зарегистрирован с паролем: {password}"
def password_validator(
    min_length: int = 8,
    min_uppercase: int = 1,
    min_lowercase: int = 1,
    min_digits: int = 1,
    min_special_chars: int = 1
) -> Callable:
    """Декоратор с параметрами для гибкой настройки правил пароля."""
    def decorator(func: Callable) -> Callable:
        def wrapper(username: str, password: str) -> str:
            if len(password) < min_length:
                raise ValueError(f"Пароль слишком короткий. Минимум {min_length} символов.")
            digits_count = sum(1 for char in password if char.isdigit())
            uppercase_count = sum(1 for char in password if char.isupper())
            lowercase_count = sum(1 for char in password if char.islower())
            special_count = sum(1 for char in password if not char.isalnum())
            if digits_count < min_digits:
                raise ValueError(f"Недостаточно цифр в пароле. Требуется минимум {min_digits}.")
            if uppercase_count < min_uppercase:
                raise ValueError(f"Недостаточно заглавных букв. Требуется минимум {min_uppercase}.")
            if lowercase_count < min_lowercase:
                raise ValueError(f"Недостаточно строчных букв. Требуется минимум {min_lowercase}.")
            if special_count < min_special_chars:
                raise ValueError(f"Недостаточно специальных символов. Требуется минимум {min_special_chars}.")
            return func(username, password)
        return wrapper
    return decorator
def username_validator(func: Callable) -> Callable:
    """Декоратор для проверки имени пользователя."""
    def wrapper(username: str, password: str) -> str:
        if not username or username.strip() == "":
            raise ValueError("Имя пользователя не может быть пустым.")
        if " " in username:
            raise ValueError("Имя пользователя не должно содержать пробелы.")
        return func(username, password)
    return wrapper
@username_validator
@password_validator(min_length=8, min_uppercase=1, min_lowercase=1, min_digits=1, min_special_chars=1)
def register_account(username: str, password: str) -> str:
    """Основная функция регистрации аккаунта с двумя декораторами."""
    user_data = {"username": username, "password": password}
    users.append(user_data)
    return "Пользователь зарегистрирован"
print("--- Тестирование Part 1 (простой декоратор) ---")
print(register_user("short"))
print(register_user("alllowercase"))
print(register_user("GoodPass1"))
print("\n--- Тестирование Part 2 & 3 (сложные декораторы и try/except) ---")
test_cases = [
    ("Arseniy", "StrongPass1!"),
    ("ivan petrov", "StrongPass1!"),
    ("Oleksandr", "Short1!"),
    ("Maxim", "NoDigitsHere!!"),
    ("Dima", "nouppercase1!"),
    ("Anton", "NoSpecial1A"),
]
for name, pwd in test_cases:
    try:
        result = register_account(name, pwd)
        print(f"[УСПЕХ] {result}")
    except ValueError as e:
        print(f"[ОШИБКА] {e}")
print(f"\nИтоговый список пользователей ({len(users)} чел.):")
for user in users:
    print(user)
# Версия проекта обновлена до 0.2
# Добавлена проверка на корректность входных данных
# Проверка прошла успешно
print("Запуск обновленной версии приложения...")