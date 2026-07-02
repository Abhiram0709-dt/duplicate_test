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
        promotion_code: str | None = None,
    ) -> PriceBreakdown:
        subtotal = sum((item.line_total for item in cart_items), start=Decimal("0.00"))
        discount = self.discounts.discount_for(cart_items=cart_items, promotion_code=promotion_code)
        discounted_subtotal = subtotal - discount
        shipping_fee = money("5.00" if shipping_country == "US" else "15.00")
        tax = money(discounted_subtotal * Decimal("0.07"))
        grand_total = money(discounted_subtotal + shipping_fee + tax)
        return PriceBreakdown(
            subtotal=money(discounted_subtotal),
            shipping_fee=shipping_fee,
            tax=tax,
            grand_total=grand_total,
        )
