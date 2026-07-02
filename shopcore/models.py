from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any


@dataclass(frozen=True)
class User:
    user_id: str
    email: str
    role: str = "customer"


@dataclass(frozen=True)
class Product:
    sku: str
    name: str
    unit_price: Decimal
    taxable: bool = True


@dataclass(frozen=True)
class CartItem:
    sku: str
    quantity: int
    unit_price: Decimal

    @property
    def line_total(self) -> Decimal:
        return self.unit_price * self.quantity


@dataclass
class Cart:
    customer_id: str
    items: list[CartItem] = field(default_factory=list)

    def add_item(self, item: CartItem) -> None:
        self.items.append(item)

    def subtotal(self) -> Decimal:
        return sum((item.line_total for item in self.items), start=Decimal("0.00"))


@dataclass(frozen=True)
class Order:
    order_id: str
    customer_id: str
    items: list[CartItem]
    totals: dict[str, Decimal]
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PaymentResult:
    approved: bool
    transaction_id: str
    captured_amount: Decimal


@dataclass(frozen=True)
class CheckoutResult:
    order: Order
    payment: PaymentResult
    invoice_number: str
