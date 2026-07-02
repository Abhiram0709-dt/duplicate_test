from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import CartItem
from .utils import money


@dataclass(frozen=True)
class DiscountRule:
    code: str
    minimum_subtotal: Decimal
    percentage_off: Decimal

    def applies_to(self, subtotal: Decimal) -> bool:
        return subtotal >= self.minimum_subtotal


class DiscountEngine:
    def __init__(self) -> None:
        self._rules = {
            "WELCOME10": DiscountRule(code="WELCOME10", minimum_subtotal=money("25.00"), percentage_off=Decimal("0.10")),
            "BULK15": DiscountRule(code="BULK15", minimum_subtotal=money("75.00"), percentage_off=Decimal("0.15")),
        }

    def discount_for(self, cart_items: list[CartItem], promotion_code: str | None) -> Decimal:
        subtotal = sum((item.line_total for item in cart_items), start=Decimal("0.00"))
        if promotion_code is None:
            return money("0.00")

        rule = self._rules.get(promotion_code.upper())
        if rule is None or not rule.applies_to(subtotal):
            return money("0.00")

        return money(subtotal * rule.percentage_off)
