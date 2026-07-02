from __future__ import annotations

from .auth import hash_password
from .api import ShopApplication
from .models import CartItem, Product, User
from .utils import money


def build_demo_application() -> ShopApplication:
    app = ShopApplication()
    app.seed_product(Product(sku="SKU-RED-01", name="Red Notebook", unit_price=money(12.50)))
    app.seed_product(Product(sku="SKU-USB-02", name="USB-C Cable", unit_price=money(8.99)))
    app.seed_stock("SKU-RED-01", 10)
    app.seed_stock("SKU-USB-02", 10)
    app.seed_user(
        User(
            user_id="user-100",
            email="customer@example.com",
            password_hash=hash_password("demo-pass", "user-100"),
        )
    )
    return app


def run_demo() -> None:
    app = build_demo_application()
    app.authenticate(email="customer@example.com", password="demo-pass")
    result = app.checkout(
        customer_id="user-100",
        email="customer@example.com",
        cart_items=[
            CartItem(sku="SKU-RED-01", quantity=2, unit_price=money(12.50)),
            CartItem(sku="SKU-USB-02", quantity=1, unit_price=money(8.99)),
        ],
        shipping_country="US",
        payment_method="card",
    )
    print(result.invoice_number)
    print(result.payment.transaction_id)
    print(result.order.totals["grand_total"])


if __name__ == "__main__":
    run_demo()
