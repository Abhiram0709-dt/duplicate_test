from __future__ import annotations

import unittest

from shopcore.auth import hash_password
from shopcore.api import ShopApplication
from shopcore.models import CartItem, Product, User
from shopcore.utils import money


class CheckoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.app = ShopApplication()
        self.app.seed_product(Product(sku="SKU-RED-01", name="Red Notebook", unit_price=money(12.50)))
        self.app.seed_product(Product(sku="SKU-USB-02", name="USB-C Cable", unit_price=money(8.99)))
        self.app.seed_stock("SKU-RED-01", 10)
        self.app.seed_stock("SKU-USB-02", 10)
        self.app.seed_user(
            User(
                user_id="user-100",
                email="customer@example.com",
                password_hash=hash_password("demo-pass", "user-100"),
            )
        )

    def test_checkout_generates_invoice_and_payment(self) -> None:
        token = self.app.authenticate(email="customer@example.com", password="demo-pass")
        self.assertTrue(token)

        result = self.app.checkout(
            customer_id="user-100",
            email="customer@example.com",
            cart_items=[
                CartItem(sku="SKU-RED-01", quantity=2, unit_price=money(12.50)),
                CartItem(sku="SKU-USB-02", quantity=1, unit_price=money(8.99)),
            ],
            shipping_country="US",
            payment_method="card",
        )

        self.assertTrue(result.payment.approved)
        self.assertTrue(result.invoice_number.startswith("INV-"))
        self.assertEqual(result.order.totals["grand_total"], money("41.37"))


if __name__ == "__main__":
    unittest.main()
