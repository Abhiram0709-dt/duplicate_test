from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, timezone
import hashlib
import re


MONEY_QUANTIZER = Decimal("0.01")


def money(value: Decimal | str | float | int) -> Decimal:
    amount = Decimal(str(value))
    return amount.quantize(MONEY_QUANTIZER, rounding=ROUND_HALF_UP)


def current_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def stable_identifier(*parts: str) -> str:
    payload = "|".join(parts).encode("utf-8")
    return hashlib.sha1(payload, usedforsecurity=False).hexdigest()[:12]


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return cleaned or "item"


@dataclass(frozen=True)
class Result:
    ok: bool
    message: str
