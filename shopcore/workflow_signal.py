from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProbeRecord:
    name: str
    value: str


def build_probe_record(name: str, value: str) -> ProbeRecord:
    return ProbeRecord(name=name, value=value.strip())
