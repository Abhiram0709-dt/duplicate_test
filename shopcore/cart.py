from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import CartItem


@dataclass(frozen=True)
class CartSummary:
    item_count: int
    subtotal: Decimal


class CartService:
    def summarize(self, items: list[CartItem]) -> CartSummary:
        item_count = sum(item.quantity for item in items)
        subtotal = sum((item.line_total for item in items), start=Decimal("0.00"))
        return CartSummary(item_count=item_count, subtotal=subtotal)
