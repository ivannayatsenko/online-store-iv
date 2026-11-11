def is_valid_quantity(value):
    """Повертає True, якщо кількість є цілим числом від 1 до 100 включно."""
    if not isinstance(value, int):
        return False
    return 1 <= value <= 100


def calculate_discount(total, user_type):
    """Застосовує 10 % знижку для student і teacher."""
    if user_type in {"student", "teacher"}:
        return total * 0.9
    return total
