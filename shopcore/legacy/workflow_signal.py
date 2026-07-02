from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ProbeRecord:
    name: str
    value: str



# Used only to exercise history classification edge cases.
def build_probe_record(name: str, value: str) -> ProbeRecord:
    return ProbeRecord(name=name, value=value.strip())
