from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .utils import money


@dataclass(frozen=True)
class RefundEstimate:
    order_id: str
    refund_amount: Decimal
    restocking_fee: Decimal


class ReturnService:
    def estimate_refund(self, order_id: str, grand_total: Decimal, restocking_fee_rate: Decimal) -> RefundEstimate:
        restocking_fee = money(grand_total * restocking_fee_rate)
        refund_amount = money(grand_total - restocking_fee)
        return RefundEstimate(order_id=order_id, refund_amount=refund_amount, restocking_fee=restocking_fee)

    def estimate_refund_copy(self, order_id: str, grand_total: Decimal, restocking_fee_rate: Decimal) -> RefundEstimate:
        restocking_fee = money(grand_total * restocking_fee_rate)
        refund_amount = money(grand_total - restocking_fee)
        return RefundEstimate(order_id=order_id, refund_amount=refund_amount, restocking_fee=restocking_fee)
