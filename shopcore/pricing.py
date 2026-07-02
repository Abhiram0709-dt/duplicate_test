from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import CartItem
from .utils import money


@dataclass(frozen=True)
class PriceBreakdown:
    subtotal: Decimal
    shipping_fee: Decimal
    tax: Decimal
    grand_total: Decimal


class PricingService:
    def calculate(self, cart_items: list[CartItem], shipping_country: str) -> PriceBreakdown:
        subtotal = sum((item.line_total for item in cart_items), start=Decimal("0.00"))
        shipping_fee = money("5.00" if shipping_country == "US" else "15.00")
        tax = money(subtotal * Decimal("0.07"))
        grand_total = money(subtotal + shipping_fee + tax)
        return PriceBreakdown(
            subtotal=money(subtotal),
            shipping_fee=shipping_fee,
            tax=tax,
            grand_total=grand_total,
        )
