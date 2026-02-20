from __future__ import annotations

import secrets
import string

MIN_LENGTH = 8


# Наборы символов по классам.
CHARSETS = {
    "lower": string.ascii_lowercase,
    "upper": string.ascii_uppercase,
    "digits": string.digits,
    "special": string.punctuation,
}


def prompt_int(message: str, min_value: int) -> int:
    """Запрашивает целое число не меньше min_value с повтором при ошибке."""
    while True:
        raw_value = input(message).strip()
        try:
            value = int(raw_value)
            if value < min_value:
                print(f"Ошибка: введите число не меньше {min_value}.")
                continue
            return value
        except ValueError:
            print("Ошибка: введите корректное целое число.")


def prompt_yes_no(message: str) -> bool:
    """Запрашивает ответ да/нет. Поддерживаются: y/n, д/н, yes/no, да/нет."""
    valid_yes = {"y", "yes", "д", "да"}
    valid_no = {"n", "no", "н", "нет"}

    while True:
        answer = input(message).strip().lower()
        if answer in valid_yes:
            return True
        if answer in valid_no:
            return False
        print("Ошибка: введите 'y/д/да' или 'n/н/нет'.")


def secure_shuffle(items: list[str]) -> None:
    """Перемешивает список на месте с использованием secrets (Фишер-Йетс)."""
    for i in range(len(items) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        items[i], items[j] = items[j], items[i]


def generate_password(length: int, selected_charsets: list[str]) -> str:
    """Генерирует пароль заданной длины с обязательным включением всех выбранных классов."""
    # Сначала добавляем по одному символу из каждого обязательного набора.
    password_chars = [secrets.choice(charset) for charset in selected_charsets]

    # Общий алфавит для оставшихся позиций.
    all_chars = "".join(selected_charsets)
    remaining = length - len(password_chars)
    for _ in range(remaining):
        password_chars.append(secrets.choice(all_chars))

    # Перемешиваем, чтобы обязательные символы не стояли в начале.
    secure_shuffle(password_chars)
    return "".join(password_chars)


def evaluate_strength(length: int, classes_count: int) -> str:
    """Оценивает надежность по длине и разнообразию классов символов."""
    score = 0

    # Вклад длины.
    if length >= 8:
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    # Вклад разнообразия классов (от 1 до 4).
    score += max(0, classes_count - 1)

    if score <= 2:
        return "Слабый"
    if score <= 4:
        return "Средний"
    return "Сильный"


def ask_selected_charsets() -> list[str]:
    """Запрашивает у пользователя наборы символов и валидирует, что выбран хотя бы один."""
    while True:
        print("\nВыберите, какие наборы символов включать в пароль:")
        use_lower = prompt_yes_no("- Строчные буквы (a-z)? [y/n]: ")
        use_upper = prompt_yes_no("- Заглавные буквы (A-Z)? [y/n]: ")
        use_digits = prompt_yes_no("- Цифры (0-9)? [y/n]: ")
        use_special = prompt_yes_no("- Спецсимволы (!@#...)? [y/n]: ")

        selected = []
        if use_lower:
            selected.append(CHARSETS["lower"])
        if use_upper:
            selected.append(CHARSETS["upper"])
        if use_digits:
            selected.append(CHARSETS["digits"])
        if use_special:
            selected.append(CHARSETS["special"])

        if not selected:
            print("Ошибка: нужно выбрать хотя бы один набор символов.")
            continue

        return selected


def ask_password_length(min_allowed: int) -> int:
    """Запрашивает длину пароля с учетом минимальной длины и числа выбранных классов."""
    while True:
        length = prompt_int(f"\nВведите длину пароля (минимум {MIN_LENGTH}): ", MIN_LENGTH)
        if length < min_allowed:
            print(
                "Ошибка: длина должна быть не меньше количества выбранных классов "
                f"({min_allowed}), чтобы включить каждый класс хотя бы один раз."
            )
            continue
        return length


def main() -> None:
    """Точка входа CLI-программы."""
    print("=" * 56)
    print("Генератор безопасных паролей (secrets)")
    print("=" * 56)

    selected_charsets = ask_selected_charsets()
    length = ask_password_length(min_allowed=len(selected_charsets))
    count = prompt_int("Сколько паролей сгенерировать? (минимум 1): ", 1)

    strength = evaluate_strength(length=length, classes_count=len(selected_charsets))

    print("\nРезультат:")
    print("-" * 56)
    for idx in range(1, count + 1):
        password = generate_password(length, selected_charsets)
        print(f"{idx:>2}. {password}    [{strength}]")
    print("-" * 56)
    print("Готово.")


if __name__ == "__main__":
    main()