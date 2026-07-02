from __future__ import annotations

import unittest
from decimal import Decimal

from shopcore.operations import (
    calculate_discount,
    calculate_total,
    process_order,
    process_refund,
    release_inventory,
    reserve_inventory,
)


class OperationTests(unittest.TestCase):
    def test_process_order_is_not_process_refund(self) -> None:
        self.assertEqual(process_order("A-1"), "order:A-1:submitted")
        self.assertEqual(process_refund("A-1"), "refund:A-1:queued")

    def test_inventory_reservation_and_release_are_distinct(self) -> None:
        self.assertEqual(reserve_inventory("SKU-1", 2), "reserve:SKU-1:2")
        self.assertEqual(release_inventory("SKU-1", 2), "release:SKU-1:2")

    def test_total_and_discount_calculations_have_different_results(self) -> None:
        subtotal = Decimal("100.00")
        discount = calculate_discount(subtotal, Decimal("0.10"))
        total = calculate_total(subtotal, Decimal("5.00"), Decimal("7.00"))

        self.assertEqual(discount, Decimal("10.00"))
        self.assertEqual(total, Decimal("112.00"))


if __name__ == "__main__":
    unittest.main()
