from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .models import PaymentResult
from .utils import stable_identifier


@dataclass(frozen=True)
class PaymentRequest:
    order_id: str
    amount: Decimal
    payment_method: str


class PaymentService:
    def capture(self, order_id: str, amount: Decimal, payment_method: str) -> PaymentResult:
        request = PaymentRequest(order_id=order_id, amount=amount, payment_method=payment_method)
        transaction_id = stable_identifier(request.order_id, request.payment_method, "payment")
        return PaymentResult(approved=True, transaction_id=transaction_id, captured_amount=request.amount)
