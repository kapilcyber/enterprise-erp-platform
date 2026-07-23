"""DataSource lifecycle engine — Phase 2C registry only."""

from modules.lowcode.domain.enums import (
    DATA_SOURCE_OPERATION_VALUES,
    DataSourceStatus,
)
from modules.lowcode.domain.exceptions import InvalidDataSourceState


class DataSourceEngine:
    def assert_module_contract(self, module_code: str | None, entity_type: str | None) -> None:
        if not module_code or not str(module_code).strip():
            raise InvalidDataSourceState("module_code is required for data source registry")
        if not entity_type or not str(entity_type).strip():
            raise InvalidDataSourceState("entity_type is required for data source registry")

    def assert_allowed_operations(self, allowed_operations: str | None) -> None:
        if not allowed_operations or not str(allowed_operations).strip():
            raise InvalidDataSourceState("allowed_operations is required")
        ops = [o.strip().lower() for o in str(allowed_operations).split(",") if o.strip()]
        if not ops:
            raise InvalidDataSourceState("allowed_operations must list at least one operation")
        for op in ops:
            if op not in DATA_SOURCE_OPERATION_VALUES:
                raise InvalidDataSourceState(
                    f"Unsupported data source operation '{op}' "
                    "(allowed: read, write, lookup)"
                )

    def assert_editable(self, row) -> None:
        if row.status == DataSourceStatus.RETIRED.value:
            raise InvalidDataSourceState("Retired data sources are read-only")

    def activate(self, row) -> None:
        if row.status == DataSourceStatus.ACTIVE.value:
            raise InvalidDataSourceState("Data source already active")
        if row.status == DataSourceStatus.RETIRED.value:
            raise InvalidDataSourceState("Retired data sources cannot be activated")
        row.status = DataSourceStatus.ACTIVE.value

    def retire(self, row) -> None:
        if row.status == DataSourceStatus.RETIRED.value:
            raise InvalidDataSourceState("Data source already retired")
        row.status = DataSourceStatus.RETIRED.value
