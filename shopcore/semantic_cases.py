from __future__ import annotations

from decimal import Decimal

from .utils import money


def calculate_invoice_total(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    tax_amount = subtotal * tax_rate
    return money(subtotal + tax_amount + shipping_fee)


def calculate_invoice_total_copy(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    tax_amount = subtotal * tax_rate
    return money(subtotal + tax_amount + shipping_fee)
