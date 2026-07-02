from __future__ import annotations

from decimal import Decimal

from .utils import money


def calculate_total(subtotal: Decimal, shipping_fee: Decimal, tax: Decimal) -> Decimal:
    return money(subtotal + shipping_fee + tax)


def calculate_discount(subtotal: Decimal, discount_rate: Decimal) -> Decimal:
    return money(subtotal * discount_rate)


def process_order(order_id: str) -> str:
    return f"order:{order_id}:submitted"


def process_refund(order_id: str) -> str:
    return f"refund:{order_id}:queued"


def reserve_inventory(sku: str, quantity: int) -> str:
    return f"reserve:{sku}:{quantity}"


def release_inventory(sku: str, quantity: int) -> str:
    return f"release:{sku}:{quantity}"
