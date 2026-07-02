from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal

from .models import CartItem
from .utils import stable_identifier


@dataclass
class PricingCache:
    entries: dict[str, dict[str, object]] = field(default_factory=dict)

    def build_key(
        self,
        cart_items: list[CartItem],
        shipping_country: str,
        promotion_code: str | None,
    ) -> str:
        item_parts = [f"{item.sku}:{item.quantity}:{item.unit_price}" for item in cart_items]
        return build_cache_key(item_parts=item_parts, shipping_country=shipping_country, promotion_code=promotion_code)

    def get(self, key: str) -> dict[str, object] | None:
        return self.entries.get(key)

    def set(self, key: str, value: dict[str, object]) -> None:
        self.entries[key] = value


def build_cache_key(item_parts: list[str], shipping_country: str, promotion_code: str | None) -> str:
    promo_fragment = promotion_code or "none"
    return stable_identifier(shipping_country, promo_fragment, "|".join(item_parts))


def build_cache_key_copy(item_parts: list[str], shipping_country: str, promotion_code: str | None) -> str:
    promo_fragment = promotion_code or "none"
    return stable_identifier(shipping_country, promo_fragment, "|".join(item_parts))
