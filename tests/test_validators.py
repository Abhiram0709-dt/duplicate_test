from __future__ import annotations

import unittest

from shopcore.models import CartItem
from shopcore.validators import ValidationError, validate_cart_items, validate_email


class ValidatorTests(unittest.TestCase):
    def test_email_validation_rejects_bad_address(self) -> None:
        with self.assertRaises(ValidationError):
            validate_email("bad-address")

    def test_cart_validation_rejects_empty_cart(self) -> None:
        with self.assertRaises(ValidationError):
            validate_cart_items([])

    def test_cart_validation_accepts_items(self) -> None:
        validate_cart_items([CartItem(sku="SKU-1", quantity=1, unit_price=1)])
