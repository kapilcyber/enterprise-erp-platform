"""Monitoring value objects — Phase 0 shared helpers."""

from dataclasses import dataclass
from typing import Any


@dataclass
class PageResult:
    items: list
    total: int
    page: int
    page_size: int
    sort_by: str | None = None
    sort_dir: str = "asc"

    def to_dict(self) -> dict[str, Any]:
        return {
            "items": self.items,
            "total": self.total,
            "page": self.page,
            "page_size": self.page_size,
            "sort_by": self.sort_by,
            "sort_dir": self.sort_dir,
        }
