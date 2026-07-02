from __future__ import annotations

from decimal import Decimal

from .cart import CartService
from .models import CartItem
from .shipping import ShippingService
from .utils import money


def build_order_overview(customer_id: str, cart_items: list[CartItem], shipping_country: str) -> dict[str, object]:
    cart_service = CartService()
    shipping_service = ShippingService()

    cart_summary = cart_service.summarize(cart_items)
    shipping_quote = shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)

    overview_total = money(cart_summary.subtotal + Decimal("0.00"))
    return {
        "customer_id": customer_id,
        "item_count": cart_summary.item_count,
        "overview_total": overview_total,
        "shipping_method": shipping_quote.method,
        "shipping_country": shipping_country,
    }
