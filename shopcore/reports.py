from __future__ import annotations

from decimal import Decimal

from .cart import CartService
from .models import CartItem
from .pricing import PricingService
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


def build_receipt_snapshot(
    customer_id: str,
    cart_items: list[CartItem],
    shipping_country: str,
    promotion_code: str | None = None,
) -> dict[str, object]:
    cart_service = CartService()
    shipping_service = ShippingService()
    pricing_service = PricingService()

    cart_summary = cart_service.summarize(cart_items)
    shipping_quote = shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
    breakdown = pricing_service.calculate(
        cart_items=cart_items,
        shipping_country=shipping_country,
        shipping_fee=shipping_quote.fee,
        promotion_code=promotion_code,
    )

    receipt_total = money(breakdown.grand_total)
    return {
        "customer_id": customer_id,
        "item_count": cart_summary.item_count,
        "subtotal": breakdown.subtotal,
        "shipping_fee": breakdown.shipping_fee,
        "receipt_total": receipt_total,
        "shipping_method": shipping_quote.method,
        "shipping_country": shipping_country,
    }


def build_confirmation_package(
    customer_id: str,
    cart_items: list[CartItem],
    shipping_country: str,
    promotion_code: str | None = None,
) -> dict[str, object]:
    cart_service = CartService()
    shipping_service = ShippingService()
    pricing_service = PricingService()

    cart_summary = cart_service.summarize(cart_items)
    shipping_quote = shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
    breakdown = pricing_service.calculate(
        cart_items=cart_items,
        shipping_country=shipping_country,
        shipping_fee=shipping_quote.fee,
        promotion_code=promotion_code,
    )

    totals = {
        "subtotal": breakdown.subtotal,
        "shipping_fee": breakdown.shipping_fee,
        "tax": breakdown.tax,
        "grand_total": breakdown.grand_total,
    }
    customer = {
        "customer_id": customer_id,
        "item_count": cart_summary.item_count,
        "shipping_country": shipping_country,
    }
    return {
        "customer": customer,
        "totals": totals,
        "shipping_method": shipping_quote.method,
        "confirmation_label": f"CONFIRM-{customer_id[:4].upper()}",
    }


def build_checkout_preview_card(
    cart_items: list[CartItem],
    shipping_country: str,
    promotion_code: str | None = None,
) -> dict[str, object]:
    cart_service = CartService()
    shipping_service = ShippingService()
    pricing_service = PricingService()

    cart_summary = cart_service.summarize(cart_items)
    shipping_quote = shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
    breakdown = pricing_service.calculate(
        cart_items=cart_items,
        shipping_country=shipping_country,
        shipping_fee=shipping_quote.fee,
        promotion_code=promotion_code,
    )

    return {
        "item_count": cart_summary.item_count,
        "subtotal": breakdown.subtotal,
        "shipping_fee": breakdown.shipping_fee,
        "tax": breakdown.tax,
        "grand_total": breakdown.grand_total,
        "shipping_method": shipping_quote.method,
        "eta_days": shipping_quote.eta_days,
        "preview_type": "checkout-card",
    }
