from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class NotificationService:
    sent_messages: list[dict[str, str]] = field(default_factory=list)

    def send_confirmation(self, email: str, order_id: str, invoice_number: str) -> None:
        payload = self.build_email_payload(email=email, order_id=order_id, invoice_number=invoice_number)
        self.sent_messages.append(payload)

    def send_webhook_confirmation(self, endpoint: str, order_id: str, invoice_number: str) -> None:
        payload = self.build_webhook_payload(endpoint=endpoint, order_id=order_id, invoice_number=invoice_number)
        self.sent_messages.append(payload)

    def build_email_payload(self, email: str, order_id: str, invoice_number: str) -> dict[str, str]:
        return {
            "email": email,
            "order_id": order_id,
            "invoice_number": invoice_number,
            "template": "order-confirmation",
        }

    def build_webhook_payload(self, endpoint: str, order_id: str, invoice_number: str) -> dict[str, str]:
        return {
            "endpoint": endpoint,
            "order_id": order_id,
            "invoice_number": invoice_number,
            "template": "order-confirmation",
        }
