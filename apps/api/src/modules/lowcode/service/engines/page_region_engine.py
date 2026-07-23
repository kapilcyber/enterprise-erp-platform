"""PageRegion validation engine — Phase 3B layout metadata only."""

from modules.lowcode.domain.enums import REGION_TYPE_VALUES
from modules.lowcode.domain.exceptions import InvalidPageRegionState


class PageRegionEngine:
    def assert_valid_type(self, region_type: str | None) -> None:
        if not region_type or region_type not in REGION_TYPE_VALUES:
            raise InvalidPageRegionState(f"Unsupported region_type: {region_type}")

    def assert_display_order(self, display_order: int | None) -> None:
        if display_order is not None and display_order < 0:
            raise InvalidPageRegionState("display_order must be >= 0")

    def assert_region_name(self, region_name: str | None) -> None:
        if not region_name or not str(region_name).strip():
            raise InvalidPageRegionState("region_name is required")
