from __future__ import annotations

from decimal import Decimal

from .models import CartItem, CheckoutResult, Order, PaymentResult, Product, User
from .utils import current_timestamp, money, stable_identifier
from .validators import validate_cart_items, validate_email


class ShopApplication:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}
        self.users: dict[str, User] = {}

    def seed_product(self, product: Product) -> None:
        self.products[product.sku] = product

    def seed_user(self, user: User) -> None:
        self.users[user.user_id] = user

    def checkout(
        self,
        customer_id: str,
        email: str,
        cart_items: list[CartItem],
        shipping_country: str,
        payment_method: str,
    ) -> CheckoutResult:
        validate_email(email)
        validate_cart_items(cart_items)

        subtotal = sum((item.line_total for item in cart_items), start=Decimal("0.00"))
        shipping_fee = money("5.00" if shipping_country == "US" else "15.00")
        tax = money(subtotal * Decimal("0.07"))
        grand_total = money(subtotal + shipping_fee + tax)

        order_id = stable_identifier(customer_id, email, current_timestamp())
        transaction_id = stable_identifier(order_id, payment_method, "payment")
        invoice_number = f"INV-{order_id.upper()}"

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=cart_items,
            totals={
                "subtotal": money(subtotal),
                "shipping_fee": shipping_fee,
                "tax": tax,
                "grand_total": grand_total,
            },
            metadata={
                "shipping_country": shipping_country,
                "payment_method": payment_method,
            },
        )
        payment = PaymentResult(approved=True, transaction_id=transaction_id, captured_amount=grand_total)
        return CheckoutResult(order=order, payment=payment, invoice_number=invoice_number)
