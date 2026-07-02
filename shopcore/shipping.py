from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .utils import money


@dataclass(frozen=True)
class ShippingQuote:
    method: str
    fee: Decimal
    eta_days: int


class ShippingService:
    def quote(self, shipping_country: str, item_count: int) -> ShippingQuote:
        if shipping_country == "US":
            if item_count > 3:
                return ShippingQuote(method="ground", fee=money("7.50"), eta_days=3)
            return ShippingQuote(method="standard", fee=money("5.00"), eta_days=5)

        return ShippingQuote(method="international", fee=money("15.00"), eta_days=10)
