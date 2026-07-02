from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NotificationService:
    sent_messages: list[dict[str, str]] = field(default_factory=list)

    def send_confirmation(self, email: str, order_id: str, invoice_number: str) -> None:
        self.sent_messages.append(
            {
                "email": email,
                "order_id": order_id,
                "invoice_number": invoice_number,
                "template": "order-confirmation",
            }
        )
