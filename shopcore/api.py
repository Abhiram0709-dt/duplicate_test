from __future__ import annotations

from decimal import Decimal

from .auth import AuthService
from .cart import CartService
from .inventory import InventoryService
from .models import CartItem, CheckoutResult, Order, PaymentResult, Product, User
from .invoice import InvoiceService
from .pricing import PricingService
from .payment import PaymentService
from .notification import NotificationService
from .shipping import ShippingService
from .utils import current_timestamp, money, stable_identifier
from .validators import validate_cart_items, validate_email


class ShopApplication:
    def __init__(self) -> None:
        self.products: dict[str, Product] = {}
        self.users: dict[str, User] = {}
        self.auth = AuthService()
        self.cart = CartService()
        self.inventory = InventoryService()
        self.pricing = PricingService()
        self.payments = PaymentService()
        self.shipping = ShippingService()
        self.notifications = NotificationService()
        self.invoices = InvoiceService()

    def seed_product(self, product: Product) -> None:
        self.products[product.sku] = product
        self.inventory.add_stock(product.sku, 0)

    def seed_stock(self, sku: str, quantity: int) -> None:
        self.inventory.add_stock(sku, quantity)

    def seed_user(self, user: User) -> None:
        self.users[user.user_id] = user
        self.auth.register_user(user)

    def authenticate(self, email: str, password: str) -> str:
        return self.auth.authenticate(email=email, password=password)

    def checkout(
        self,
        customer_id: str,
        email: str,
        cart_items: list[CartItem],
        shipping_country: str,
        payment_method: str,
        promotion_code: str | None = None,
    ) -> CheckoutResult:
        validate_email(email)
        validate_cart_items(cart_items)
        cart_summary = self.cart.summarize(cart_items)
        self.inventory.reserve(cart_items)
        shipping_quote = self.shipping.quote(shipping_country=shipping_country, item_count=cart_summary.item_count)
        breakdown = self.pricing.calculate(
            cart_items=cart_items,
            shipping_country=shipping_country,
            shipping_fee=shipping_quote.fee,
            promotion_code=promotion_code,
        )

        order_id = stable_identifier(customer_id, email, current_timestamp())
        payment = self.payments.capture(order_id=order_id, amount=breakdown.grand_total, payment_method=payment_method)
        invoice_number = self.invoices.generate(order_id=order_id)

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            items=cart_items,
            totals={
                "subtotal": breakdown.subtotal,
                "shipping_fee": breakdown.shipping_fee,
                "tax": breakdown.tax,
                "grand_total": breakdown.grand_total,
            },
            metadata={
                "shipping_country": shipping_country,
                "payment_method": payment_method,
                "shipping_method": shipping_quote.method,
                "item_count": cart_summary.item_count,
            },
        )
        self.notifications.send_confirmation(email=email, order_id=order_id, invoice_number=invoice_number)
        return CheckoutResult(order=order, payment=payment, invoice_number=invoice_number)

