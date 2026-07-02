from __future__ import annotations

import re
from decimal import Decimal

from .models import CartItem


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9\-\s]{6,18}$")


class ValidationError(ValueError):
    pass


def validate_email(email: str) -> None:
    if not EMAIL_PATTERN.match(email):
        raise ValidationError(f"Invalid email address: {email}")


def validate_cart_items(items: list[CartItem]) -> None:
    if not items:
        raise ValidationError("Cart must contain at least one item")

    for item in items:
        if item.quantity <= 0:
            raise ValidationError(f"Invalid quantity for {item.sku}")
        if item.unit_price < Decimal("0.00"):
            raise ValidationError(f"Invalid price for {item.sku}")


def validate_phone_number(phone_number: str) -> None:
    if not PHONE_PATTERN.match(phone_number):
        raise ValidationError(f"Invalid phone number: {phone_number}")


def validate_phone_number_copy(phone_number: str) -> None:
    if not PHONE_PATTERN.match(phone_number):
        raise ValidationError(f"Invalid phone number: {phone_number}")
