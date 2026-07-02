from __future__ import annotations


class InvoiceService:
    def __init__(self) -> None:
        self._sequence = 1000

    def generate(self, order_id: str) -> str:
        self._sequence += 1
        return f"INV-{self._sequence:06d}-{order_id[:6].upper()}"
