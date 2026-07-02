from __future__ import annotations

import unittest
from decimal import Decimal

from shopcore.returns import ReturnService


class ReturnServiceTests(unittest.TestCase):
    def test_refund_estimate_applies_restocking_fee(self) -> None:
        service = ReturnService()
        estimate = service.estimate_refund(order_id="order-1", grand_total=Decimal("100.00"), restocking_fee_rate=Decimal("0.10"))

        self.assertEqual(estimate.refund_amount, Decimal("90.00"))
        self.assertEqual(estimate.restocking_fee, Decimal("10.00"))


if __name__ == "__main__":
    unittest.main()
