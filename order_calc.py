"""Розрахунок вартості замовлення навчального проєкту online-store.

Підсумкова сума: сума позицій -> знижка за типом користувача ->
бонусна знижка (за умови) -> податок.
"""

DISCOUNT_RATE = 0.1
TAX_RATE = 0.2
BONUS_THRESHOLD = 1000
BONUS_DISCOUNT = 50
DISCOUNTED_USER_TYPES = {"student", "teacher"}


def calculate_subtotal(items):
    """Обчислює початкову вартість усіх позицій (ціна × кількість)."""
    subtotal = 0
    for item in items:
        subtotal = subtotal + item["price"] * item["qty"]
    return subtotal


def apply_discount(total, user_type):
    """Застосовує знижку DISCOUNT_RATE для типів користувачів з DISCOUNTED_USER_TYPES."""
    if user_type in DISCOUNTED_USER_TYPES:
        return total - total * DISCOUNT_RATE
    return total


def should_apply_bonus(total, bonus_enabled, is_active):
    """Повертає True, якщо бонус увімкнено, сума більша за BONUS_THRESHOLD і користувач активний."""
    return bonus_enabled == 1 and total > BONUS_THRESHOLD and is_active == True


def apply_bonus_discount(total, bonus_enabled, is_active):
    """Віднімає фіксований BONUS_DISCOUNT, якщо виконано умови бонусної знижки."""
    if should_apply_bonus(total, bonus_enabled, is_active):
        return total - BONUS_DISCOUNT
    return total


def add_tax(total):
    """Додає податок TAX_RATE до поточної суми."""
    return total + total * TAX_RATE


def calculate_order_total(user, items, bonus_enabled):
    """Повертає підсумкову вартість замовлення з урахуванням знижок і податку.

    user: словник з ключами "type" і "active";
    items: список позицій з ключами "price" і "qty";
    bonus_enabled: 1, якщо бонусна знижка дозволена.
    """
    subtotal = calculate_subtotal(items)
    discounted_total = apply_discount(subtotal, user["type"])
    adjusted_total = apply_bonus_discount(
        discounted_total,
        bonus_enabled,
        user["active"],
    )
    return add_tax(adjusted_total)


def calculate_total_without_bonus(user, items):
    """Повертає вартість замовлення без бонусної знижки (знижка за типом і податок)."""
    subtotal = calculate_subtotal(items)
    discounted_total = apply_discount(subtotal, user["type"])
    return add_tax(discounted_total)


def p(u, items, x):
    """Сумісний виклик старого інтерфейсу: рахує суму та друкує її."""
    total = calculate_order_total(u, items, x)
    print("Total:", total)
    return total


def p2(u, items):
    """Сумісний виклик старого інтерфейсу для розрахунку без бонусу."""
    return calculate_total_without_bonus(u, items)


if __name__ == "__main__":
    user = {"type": "student", "active": True}
    cart = [{"price": 500, "qty": 2}, {"price": 200, "qty": 1}]
    print("Total:", calculate_order_total(user, cart, 1))
