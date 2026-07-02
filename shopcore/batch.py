from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .cart import CartService
from .models import CartItem
from .pricing import PricingService
from .shipping import ShippingService
from .utils import money, stable_identifier


@dataclass(frozen=True)
class BatchLineItem:
    index: int
    item_count: int
    grand_total: Decimal


class BatchInvoiceService:
    def __init__(self) -> None:
        self._sequence = 5000

    def generate_batch_reference(self, batch_size: int) -> str:
        self._sequence += 1
        return f"BATCH-{self._sequence:06d}-{batch_size:02d}"


class BatchCheckoutService:
    def __init__(self) -> None:
        self.cart_service = CartService()
        self.pricing_service = PricingService()
        self.shipping_service = ShippingService()
        self.invoice_service = BatchInvoiceService()

    def preview_batch(
        self,
        cart_groups: list[list[CartItem]],
        shipping_country: str,
        promotion_code: str | None = None,
    ) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        batch_total = Decimal("0.00")

        for index, cart_items in enumerate(cart_groups, start=1):
            cart_summary = self.cart_service.summarize(cart_items)
            shipping_quote = self.shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
            breakdown = self.pricing_service.calculate(
                cart_items=cart_items,
                shipping_country=shipping_country,
                shipping_fee=shipping_quote.fee,
                promotion_code=promotion_code,
            )
            batch_total += breakdown.grand_total
            rows.append(
                {
                    "index": index,
                    "item_count": cart_summary.item_count,
                    "grand_total": breakdown.grand_total,
                    "shipping_method": shipping_quote.method,
                }
            )

        batch_reference = self.invoice_service.generate_batch_reference(len(cart_groups))
        return {
            "batch_reference": batch_reference,
            "batch_total": money(batch_total),
            "rows": rows,
        }

    def preview_batch_copy(
        self,
        cart_groups: list[list[CartItem]],
        shipping_country: str,
        promotion_code: str | None = None,
    ) -> dict[str, object]:
        rows: list[dict[str, object]] = []
        batch_total = Decimal("0.00")

        for index, cart_items in enumerate(cart_groups, start=1):
            cart_summary = self.cart_service.summarize(cart_items)
            shipping_quote = self.shipping_service.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
            breakdown = self.pricing_service.calculate(
                cart_items=cart_items,
                shipping_country=shipping_country,
                shipping_fee=shipping_quote.fee,
                promotion_code=promotion_code,
            )
            batch_total += breakdown.grand_total
            rows.append(
                {
                    "index": index,
                    "item_count": cart_summary.item_count,
                    "grand_total": breakdown.grand_total,
                    "shipping_method": shipping_quote.method,
                }
            )

        batch_reference = self.invoice_service.generate_batch_reference(len(cart_groups))
        return {
            "batch_reference": batch_reference,
            "batch_total": money(batch_total),
            "rows": rows,
        }


def format_batch_line(index: int, item_count: int, total: Decimal) -> str:
    return f"{index}:{item_count}:{money(total)}"


def format_batch_line_copy(index: int, item_count: int, total: Decimal) -> str:
    return f"{index}:{item_count}:{money(total)}"
