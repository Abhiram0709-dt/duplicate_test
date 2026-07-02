from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .discounts import DiscountEngine
from .models import CartItem
from .utils import money


@dataclass(frozen=True)
class PriceBreakdown:
    subtotal: Decimal
    shipping_fee: Decimal
    tax: Decimal
    grand_total: Decimal


class PricingService:
    def __init__(self) -> None:
        self.discounts = DiscountEngine()

    def calculate(
        self,
        cart_items: list[CartItem],
        shipping_country: str,
        shipping_fee: float | Decimal | None = None,
        promotion_code: str | None = None,
    ) -> PriceBreakdown:
        subtotal = sum((item.line_total for item in cart_items), start=Decimal("0.00"))
        discount = self.discounts.discount_for(cart_items=cart_items, promotion_code=promotion_code)
        discounted_subtotal = subtotal - discount
        if shipping_fee is None:
            shipping_fee = money("5.00" if shipping_country == "US" else "15.00")
        else:
            shipping_fee = money(shipping_fee)
        tax = calculate_tax(discounted_subtotal)
        grand_total = money(discounted_subtotal + shipping_fee + tax)
        return PriceBreakdown(
            subtotal=money(discounted_subtotal),
            shipping_fee=shipping_fee,
            tax=tax,
            grand_total=grand_total,
        )


def calculate_tax(amount: Decimal) -> Decimal:
    return money(amount * Decimal("0.07"))


def calculate_tax_copy(amount: Decimal) -> Decimal:
    return money(amount * Decimal("0.07"))


def calculate_tax_renamed(base_amount: Decimal) -> Decimal:
    computed_tax = base_amount * Decimal("0.07")
    normalized_tax = money(computed_tax)
    return normalized_tax


def calculate_service_tax(amount: Decimal) -> Decimal:
    tax_amount = amount * Decimal("0.07")
    return money(tax_amount)


def calculate_service_tax_copy(amount: Decimal) -> Decimal:
    tax_amount = amount * Decimal("0.07")
    return money(tax_amount)
