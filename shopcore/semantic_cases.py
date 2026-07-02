from __future__ import annotations

from decimal import Decimal

from .utils import money


def calculate_invoice_total(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    tax_amount = subtotal * tax_rate
    return money(subtotal + tax_amount + shipping_fee)


def calculate_invoice_total_copy(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    tax_amount = subtotal * tax_rate
    return money(subtotal + tax_amount + shipping_fee)


def calculate_invoice_total_renamed(amount_before_tax: Decimal, rate: Decimal, freight_cost: Decimal) -> Decimal:
    computed_tax = amount_before_tax * rate
    return money(amount_before_tax + computed_tax + freight_cost)


def calculate_invoice_total_reordered(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    total_before_tax = subtotal + shipping_fee
    tax_amount = subtotal * tax_rate
    final_total = total_before_tax + tax_amount
    return money(final_total)


def _tax_component(subtotal: Decimal, rate: Decimal) -> Decimal:
    return subtotal * rate


def _merge_invoice_total(subtotal: Decimal, shipping_fee: Decimal, tax_amount: Decimal) -> Decimal:
    return subtotal + shipping_fee + tax_amount


def calculate_invoice_total_with_helpers(subtotal: Decimal, tax_rate: Decimal, shipping_fee: Decimal) -> Decimal:
    tax_amount = _tax_component(subtotal, tax_rate)
    merged_total = _merge_invoice_total(subtotal, shipping_fee, tax_amount)
    return money(merged_total)
