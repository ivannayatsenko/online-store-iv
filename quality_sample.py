DISCOUNT_RATE = 0.10
DISCOUNTED_USER_TYPES = {"student", "teacher"}


def calculate_order_total(items, user_type, debug=False):
    """Обчислює підсумкову суму замовлення з базовою знижкою."""
    total = 0
    for item in items:
        total = total + item["price"] * item["qty"]

    if user_type in DISCOUNTED_USER_TYPES:
        total = total - total * DISCOUNT_RATE

    if debug:
        print("Calculated total:", total)

    return total
