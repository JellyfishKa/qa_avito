import random
import string


def seller_id():
    return random.randint(111111, 999999)


def item_name(prefix="Test item"):
    suffix = "".join(random.choices(string.ascii_lowercase, k=6))
    return f"{prefix} {suffix}"


def valid_item(seller=None):
    return {
        "sellerId": seller if seller is not None else seller_id(),
        "name": item_name(),
        "price": random.randint(100, 50000),
        "statistics": {
            "likes": random.randint(1, 100),
            "viewCount": random.randint(1, 1000),
            "contacts": random.randint(1, 50),
        },
    }
