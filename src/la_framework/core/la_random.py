from decimal import Decimal
import random
import string


def random_str(min_length: int = 5, max_length: int = 10) -> str:
    length = random.randint(min_length, max_length)
    result = "".join(random.choices(string.ascii_letters, k=length))
    return result


def random_decimal(min_value: float = 0.0, max_value: float = 100.0) -> Decimal:
    value = random.uniform(min_value, max_value)
    return Decimal(str(value))
