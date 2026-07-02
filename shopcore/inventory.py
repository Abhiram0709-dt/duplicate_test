from __future__ import annotations

from collections import defaultdict

from .models import CartItem


class InventoryError(ValueError):
    pass


class InventoryService:
    def __init__(self) -> None:
        self._available: dict[str, int] = defaultdict(int)

    def add_stock(self, sku: str, quantity: int) -> None:
        self._available[sku] += quantity

    def reserve(self, items: list[CartItem]) -> None:
        for item in items:
            available_quantity = self._available[item.sku]
            if available_quantity < item.quantity:
                raise InventoryError(f"Insufficient stock for {item.sku}")

        for item in items:
            self._available[item.sku] -= item.quantity

    def release(self, items: list[CartItem]) -> None:
        for item in items:
            self._available[item.sku] += item.quantity

    def low_stock_skus(self, threshold: int = 2) -> list[str]:
        low_stock = []
        for sku, quantity in self._available.items():
            if quantity <= threshold:
                low_stock.append(sku)
        return sorted(low_stock)
