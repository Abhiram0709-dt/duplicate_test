from __future__ import annotations

import unittest

from shopcore.batch import BatchCheckoutService, format_batch_line
from shopcore.models import CartItem
from shopcore.utils import money


class BatchCheckoutTests(unittest.TestCase):
    def test_batch_preview_reports_each_cart(self) -> None:
        service = BatchCheckoutService()
        preview = service.preview_batch(
            cart_groups=[
                [CartItem(sku="SKU-1", quantity=1, unit_price=money("10.00"))],
                [CartItem(sku="SKU-2", quantity=2, unit_price=money("12.00"))],
            ],
            shipping_country="US",
        )

        self.assertTrue(preview["batch_reference"].startswith("BATCH-"))
        self.assertEqual(len(preview["rows"]), 2)
        self.assertEqual(format_batch_line(1, 2, money("24.00")), "1:2:24.00")


if __name__ == "__main__":
    unittest.main()
