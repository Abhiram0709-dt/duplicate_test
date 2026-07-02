from __future__ import annotations

from dataclasses import dataclass, field

from .models import Order, PaymentResult


@dataclass(frozen=True)
class AuditEntry:
    category: str
    reference_id: str
    details: dict[str, str]


@dataclass
class AuditTrail:
    events: list[AuditEntry] = field(default_factory=list)

    def record(self, entry: AuditEntry) -> None:
        self.events.append(entry)


def build_checkout_audit(order: Order, payment: PaymentResult, invoice_number: str) -> AuditEntry:
    details = {
        "invoice_number": invoice_number,
        "order_total": str(order.totals["grand_total"]),
        "payment_status": "approved" if payment.approved else "declined",
    }
    return AuditEntry(category="checkout", reference_id=order.order_id, details=details)


def build_checkout_audit_copy(order: Order, payment: PaymentResult, invoice_number: str) -> AuditEntry:
    details = {
        "invoice_number": invoice_number,
        "order_total": str(order.totals["grand_total"]),
        "payment_status": "approved" if payment.approved else "declined",
    }
    return AuditEntry(category="checkout", reference_id=order.order_id, details=details)
